#pragma once

#include "mamefont_common.hpp"

namespace mamefont {

struct Glyph {
  const uint8_t *blob;
  bool isShrinked;

  Glyph() : blob(nullptr), isShrinked(false) {}
  Glyph(const uint8_t *data, bool isShrinked)
      : blob(data), isShrinked(isShrinked) {}

  MAMEFONT_INLINE int16_t entryPoint() const {
    if (isShrinked) {
      return static_cast<int16_t>(blob[0]) << 1;
    } else {
      return reinterpret_cast<const int16_t *>(blob)[0];
    }
  }

  MAMEFONT_INLINE bool isValid() const {
    return blob[0] != 0xff && blob[1] != 0xff;
  }

  MAMEFONT_INLINE uint8_t width() const {
    if (isShrinked) {
      return (blob[1] & 0x0f) + 1;
    } else {
      return (blob[2] & 0x3f) + 1;
    }
  }

  MAMEFONT_INLINE uint8_t xAdvance() const {
    if (isShrinked) {
      return ((blob[1] >> 4) & 0x0f) + 1;
    } else {
      return (blob[3] & 0x3f) + 1;
    }
  }
};

class Font {
 public:
  const uint8_t *blob;

  Font(const uint8_t *blob) : blob(blob) {}

  MAMEFONT_INLINE FontFlags flags() const {
    return static_cast<FontFlags>(blob[OFST_FONT_FLAGS]);
  }

  MAMEFONT_INLINE bool isShrinkedGlyphTable() const {
    return !!(flags() & FontFlags::SHRINKED_GLYPH_TABLE);
  }

  MAMEFONT_INLINE uint8_t glyphTableEntrySize() const {
    return isShrinkedGlyphTable() ? 2 : 4;
  }

  MAMEFONT_INLINE uint8_t firstCode() const { return blob[OFST_FIRST_CODE]; }

  MAMEFONT_INLINE uint8_t glyphTableLen() const {
    return blob[OFST_GLYPH_TABLE_LEN] + 1;
  }

  MAMEFONT_INLINE uint8_t lastCode() const {
    return firstCode() + glyphTableLen() - 1;
  }

  MAMEFONT_INLINE uint8_t lutSize() const { return blob[OFST_LUT_SIZE] + 1; }

  MAMEFONT_INLINE uint8_t fontHeight() const {
    return (blob[OFST_FONT_DIMENSION_0] & 0x3f) + 1;
  }

  MAMEFONT_INLINE const bool verticalScan() const {
    return blob[OFST_FONT_FLAGS] & 0x80;
  }

  MAMEFONT_INLINE const Glyph glyphTableEntry(uint8_t index) const {
    const uint8_t *ptr = blob + OFST_GLYPH_TABLE;
    ptr += isShrinkedGlyphTable() ? (index << 1) : (index << 2);
    return Glyph(ptr, isShrinkedGlyphTable());
  }

  Status getGlyph(uint8_t c, Glyph *glyph) const {
    uint8_t first = firstCode();
    uint8_t last = lastCode();
    if (c < first || last < c) return Status::CHAR_CODE_OUT_OF_RANGE;
    uint8_t index = c - first;

    auto g = glyphTableEntry(index);
    if (glyph) *glyph = g;

    return g.isValid() ? Status::SUCCESS : Status::GLYPH_NOT_DEFINED;
  }

  MAMEFONT_INLINE int16_t lutOffset() const {
    if (isShrinkedGlyphTable()) {
      return OFST_GLYPH_TABLE + glyphTableLen() * 2;
    } else {
      return OFST_GLYPH_TABLE + glyphTableLen() * 4;
    }
  }

  MAMEFONT_INLINE int16_t microCodeOffset() const {
    return lutOffset() + lutSize();
  }

  MAMEFONT_INLINE const uint8_t *getEntryPoint(const Glyph &glyph) const {
    return blob + microCodeOffset() + glyph.entryPoint();
  }

  const Glyph getMaxWideGlyph() const {
    uint8_t maxWidth = 0;
    Glyph maxGlyph;
    for (uint8_t i = 0; i < glyphTableLen(); i++) {
      const Glyph glyph = glyphTableEntry(i);
      if (!glyph.isValid()) continue;
      uint8_t width = glyph.width();
      if (width > maxWidth) {
        maxWidth = width;
        maxGlyph = glyph;
      }
    }
    return maxGlyph;
  }

  MAMEFONT_INLINE int16_t getRequiredGlyphBufferSize(const Glyph *glyph,
                                                     int16_t *stride) const {
    int16_t w = glyph->width();
    int16_t h = fontHeight();
    if (verticalScan()) {
      *stride = ((w + 7) / 8);
      return *stride * h;
    } else {
      *stride = w;
      return w * ((h + 7) / 8);
    }
  }

  MAMEFONT_INLINE int16_t getRequiredGlyphBufferSize(int16_t *stride) const {
    const Glyph maxGlyph = getMaxWideGlyph();
    return getRequiredGlyphBufferSize(&maxGlyph, stride);
  }
};

struct GlyphBuffer {
  uint8_t *data;
  int16_t stride;
};

class Renderer {
 public:
  FontFlags flags;
  const uint8_t *lut;
  const uint8_t *microcode;
  uint8_t fontHeight;

  uint8_t *buffData;
  // int16_t buffStride;

  int8_t laneBytes = 0;
  int8_t byteStride = 0;
  int8_t laneStride = 0;
  int8_t numLanesToGlyphEnd = 0;
  int8_t numBytesToLaneEnd = 0;

  uint16_t pc = 0;
  int16_t nextLanePos = 0;
  int16_t writePos = 0;
  uint8_t lastByte = 0;

  Renderer(const Font &font) {
    this->flags = font.flags();
    this->lut = font.blob + font.lutOffset();
    this->microcode = font.blob + font.microCodeOffset();
    this->fontHeight = font.fontHeight();
  }

  Status render(Glyph &glyph, GlyphBuffer &buff) {
    // buffStride = buff.stride;
    buffData = buff.data;

    int8_t glyphWidth = glyph.width();
    if (flags & FontFlags::VERTICAL_SCAN) {
      byteStride = buff.stride;
      laneStride = 1;
      laneBytes = fontHeight;
      numLanesToGlyphEnd = (glyphWidth + 7) / 8 + 1;
    } else {
      byteStride = 1;
      laneStride = buff.stride;
      laneBytes = glyphWidth;
      numLanesToGlyphEnd = (fontHeight + 7) / 8 + 1;
    }

    nextLanePos = 0;
    writePos = 0;
    stepLane();

    lastByte = 0x00;
    pc = glyph.entryPoint();

#if MAMEFONT_STM_VERBOSE
    printf("    entryPoint         : %d\n", pc);
    printf("    glyphWidth         : %d\n", glyphWidth);
    printf("    numLanesToGlyphEnd : %d\n", numLanesToGlyphEnd);
    printf("    numBytesToLaneEnd  : %d\n", numBytesToLaneEnd);
#endif

    while (numLanesToGlyphEnd > 0) {
      uint8_t inst = microcode[pc++];
      uint8_t seg;
      switch (inst & 0xf0) {
        case 0x00:  // LUS
        case 0x10:  // LUS
        case 0x20:  // LUS
        case 0x30:  // LUS
          LUS(inst);
          break;

        case 0x40:  // SLC
        case 0x50:  // SLS
        case 0x60:  // SRC
        case 0x70:  // SRS
          SLC_SLS_SRC_SRS(inst);
          break;

        case 0x80:  // LUD
        case 0x90:  // LUD
          LUD(inst);
          break;

        case 0xa0:  // CPY or LDI
        case 0xb0:  // CPY
          if (inst == 0xa0) {
            LDI(inst);
          } else {
            CPY_REV(inst, false);
          }
          break;

        case 0xc0:  // REV
        case 0xd0:  // REV
          if (inst == 0xc0) {
            return Status::UNKNOWN_OPCODE;
          } else if (inst == 0xd0) {
            return Status::UNKNOWN_OPCODE;
          } else {
            CPY_REV(inst, true);
          }
          break;

        case 0xe0:  // RPT
          RPT(inst);
          break;

        case 0xf0:  // XOR
          if (inst == 0xff) {
            return Status::UNKNOWN_OPCODE;
          } else {
            XOR(inst);
          }
          break;

        default:
          return Status::UNKNOWN_OPCODE;
      }
    }
    return Status::SUCCESS;
  }

  MAMEFONT_INLINE void LUS(uint8_t inst) {
    uint8_t index = inst & 0x3f;
    uint8_t byte = lut[index];

#if MAMEFONT_STM_VERBOSE
    stamp();
    char buff[64];
    snprintf(buff, sizeof(buff), "LUS(index=%d)", index);
#endif

    write(byte);

#if MAMEFONT_STM_VERBOSE
    printf("    %-40s --> 0x%02x\n", buff, byte);
#endif
  }

  MAMEFONT_INLINE void LUD(uint8_t inst) {
    uint8_t index = inst & 0x0f;
    uint8_t step = (inst >> 4) & 0x1;

#if MAMEFONT_STM_VERBOSE
    stamp();
    char buff[64];
    snprintf(buff, sizeof(buff), "LUD(index=%d, step=%d)", index, step);
#endif

    write(lut[index]);
    write(lut[index + step]);

#if MAMEFONT_STM_VERBOSE
    printf("    %-40s --> 0x%02x 0x%02x\n", buff, lut[index],
           lut[index + step]);
#endif
  }

  MAMEFONT_INLINE void SLC_SLS_SRC_SRS(uint8_t inst) {
    uint8_t shift_dir = inst & 0x20;
    uint8_t post_op = inst & 0x10;
    uint8_t shift_size = ((inst >> 2) & 0x3) + 1;
    uint8_t repeat_count = (inst & 0x03) + 1;

#if MAMEFONT_STM_VERBOSE
    stamp();
    char buff[64];
    snprintf(buff, sizeof(buff), "S%c%c(shift_size=%1d, repeat_count=%1d)",
             shift_dir ? 'R' : 'L', post_op ? 'S' : 'C', shift_size,
             repeat_count);
#endif

    uint8_t modifier = (1 << shift_size) - 1;
    if (shift_dir != 0) modifier <<= (8 - shift_size);
    if (post_op == 0) modifier = ~modifier;
    for (int8_t i = repeat_count; i != 0; i--) {
      if (shift_dir == 0) {
        lastByte <<= shift_size;
      } else {
        lastByte >>= shift_size;
      }
      if (post_op) {
        lastByte |= modifier;
      } else {
        lastByte &= modifier;
      }
      write(lastByte);
    }

#if MAMEFONT_STM_VERBOSE
    printf("    %-40s -->", buff);
    for (int i = 0; i < repeat_count; i++) {
      printf(" 0x%02x", read(writePos - repeat_count + i));
    }
    printf("\n");
#endif
  }

  MAMEFONT_INLINE void CPY_REV(uint8_t inst, bool reverse = false) {
    uint8_t offset = (inst >> 3) & 0x3;
    uint8_t length = (inst & 0x07) + 1;

#if MAMEFONT_STM_VERBOSE
    stamp();
    char buff[64];
    snprintf(buff, sizeof(buff), "%s(offset=%d, length=%d)",
             reverse ? "REV" : "CPY", offset, length);
#endif

    if (reverse) {
      int16_t rdPos = writePos - offset;
      for (int8_t i = length; i != 0; i--) {
        write(read(--rdPos));
      }
    } else {
      int16_t rdPos = writePos - length - offset;
      for (int8_t i = length; i != 0; i--) {
        write(read(rdPos++));
      }
    }

#if MAMEFONT_STM_VERBOSE
    printf("    %-40s -->", buff);
    for (int i = 0; i < length; i++) {
      printf(" 0x%02x", read(writePos - length + i));
    }
    printf("\n");
#endif
  }

  MAMEFONT_INLINE void LDI(uint8_t inst) {
    uint8_t seg = microcode[pc++];

#if MAMEFONT_STM_VERBOSE
    stamp();
    char buff[64];
    snprintf(buff, sizeof(buff), "LDI(byte=0x%02x)", seg);
#endif

    write(seg);

#if MAMEFONT_STM_VERBOSE
    printf("    %-40s --> 0x%02x\n", buff, seg);
#endif
  }

  MAMEFONT_INLINE void RPT(uint8_t inst) {
    uint8_t repeat_count = (inst & 0x0f) + 1;

#if MAMEFONT_STM_VERBOSE
    stamp();
    char buff[64];
    snprintf(buff, sizeof(buff), "RPT(repeat_count=%d)", repeat_count);
#endif

    for (int8_t i = repeat_count; i != 0; i--) {
      write(lastByte);
    }

#if MAMEFONT_STM_VERBOSE
    printf("    %-40s -->", buff);
    for (int i = 0; i < repeat_count; i++) {
      printf(" 0x%02x", read(writePos - repeat_count + i));
    }
    printf("\n");
#endif
  }

  MAMEFONT_INLINE void XOR(uint8_t inst) {
    uint8_t mask_width = ((inst >> 3) & 0x01) + 1;
    uint8_t mask_pos = inst & 0x07;
    uint8_t mask = (1 << mask_width) - 1;

#if MAMEFONT_STM_VERBOSE
    stamp();
    char buff[64];
    snprintf(buff, sizeof(buff), "XOR(mask_width=%d, mask_pos=%d)", mask_width,
             mask_pos);
#endif

    write(lastByte ^ (mask << mask_pos));

#if MAMEFONT_STM_VERBOSE
    printf("    %-40s --> 0x%02x\n", buff, lastByte);
#endif
  }

  void stepLane() {
    numLanesToGlyphEnd--;
    writePos = nextLanePos;
    nextLanePos += laneStride;
    numBytesToLaneEnd = laneBytes;
  }

  void write(uint8_t value) {
    buffData[writePos] = value;
    writePos += byteStride;
    lastByte = value;
    if (--numBytesToLaneEnd <= 0) {
      stepLane();
    }
  }

  uint8_t read(int16_t pos) const {
    if (pos < 0) return 0;
    return buffData[pos];
  }

  MAMEFONT_INLINE void stamp() const {
    printf("    wpos=%4d, last=0x%02x ", writePos, lastByte);
  }
};

}  // namespace mamefont
