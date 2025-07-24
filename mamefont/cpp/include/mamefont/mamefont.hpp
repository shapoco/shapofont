#pragma once

#include "mamefont_common.hpp"

namespace mamefont {

struct Glyph {
  const uint8_t *blob;
  bool isShrinked;

  Glyph() : blob(nullptr), isShrinked(false) {}
  Glyph(const uint8_t *data, bool isShrinked)
      : blob(data), isShrinked(isShrinked) {}

  MAMEFONT_ALWAYS_INLINE int16_t entryPoint() const {
    if (isShrinked) {
      return static_cast<int16_t>(blob[0]) << 1;
    } else {
      return reinterpret_cast<const int16_t *>(blob)[0];
    }
  }

  MAMEFONT_ALWAYS_INLINE bool isValid() const {
    return blob[0] != 0xff && blob[1] != 0xff;
  }

  MAMEFONT_ALWAYS_INLINE uint8_t width() const {
    if (isShrinked) {
      return (blob[1] & 0x0f) + 1;
    } else {
      return (blob[2] & 0x3f) + 1;
    }
  }

  MAMEFONT_ALWAYS_INLINE uint8_t xAdvance() const {
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

  MAMEFONT_ALWAYS_INLINE FontFlags flags() const {
    return static_cast<FontFlags>(blob[OFST_FONT_FLAGS]);
  }

  MAMEFONT_ALWAYS_INLINE bool isShrinkedGlyphTable() const {
    return !!(flags() & FontFlags::SHRINKED_GLYPH_TABLE);
  }

  MAMEFONT_ALWAYS_INLINE uint8_t glyphTableEntrySize() const {
    return isShrinkedGlyphTable() ? 2 : 4;
  }

  MAMEFONT_ALWAYS_INLINE uint8_t firstCode() const {
    return blob[OFST_FIRST_CODE];
  }

  MAMEFONT_ALWAYS_INLINE uint8_t glyphTableLen() const {
    return blob[OFST_GLYPH_TABLE_LEN] + 1;
  }

  MAMEFONT_ALWAYS_INLINE uint8_t lastCode() const {
    return firstCode() + glyphTableLen() - 1;
  }

  MAMEFONT_ALWAYS_INLINE uint8_t lutSize() const {
    return blob[OFST_LUT_SIZE] + 1;
  }

  MAMEFONT_ALWAYS_INLINE uint8_t fontHeight() const {
    return (blob[OFST_FONT_DIMENSION_0] & 0x3f) + 1;
  }

  MAMEFONT_ALWAYS_INLINE const bool verticalScan() const {
    return blob[OFST_FONT_FLAGS] & 0x80;
  }

  MAMEFONT_ALWAYS_INLINE const Glyph glyphTableEntry(uint8_t index) const {
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

  MAMEFONT_ALWAYS_INLINE int16_t lutOffset() const {
    if (isShrinkedGlyphTable()) {
      return OFST_GLYPH_TABLE + glyphTableLen() * 2;
    } else {
      return OFST_GLYPH_TABLE + glyphTableLen() * 4;
    }
  }

  MAMEFONT_ALWAYS_INLINE int16_t microCodeOffset() const {
    return lutOffset() + lutSize();
  }

  MAMEFONT_ALWAYS_INLINE const uint8_t *getEntryPoint(
      const Glyph &glyph) const {
    return blob + microCodeOffset() + glyph.entryPoint();
  }

  const Glyph getWidestGlyph() const {
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

  int16_t getRequiredGlyphBufferSize(const Glyph *glyph,
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

  int16_t getRequiredGlyphBufferSize(int16_t *stride) const {
    const Glyph maxGlyph = getWidestGlyph();
    return getRequiredGlyphBufferSize(&maxGlyph, stride);
  }
};

struct GlyphBuffer {
  uint8_t *data;
  int16_t stride;
};

class Renderer {
 public:
  struct AddrRule {
    int8_t lanesPerGlyph;     // Number of lanes per glyph
    int8_t fragsPerLane;      // Number of fragments per lane
    frag_index_t laneStride;  // Stride to next lane in bytes
    frag_index_t fragStride;  // Stride to next fragment in bytes
  };

  struct Cursor {
    frag_index_t offset;      // Offset from start of glyph in bytes
    frag_index_t laneOffset;  // Offset of first fragment of current lane
    int8_t fragIndex;         // Distance from start of current lane in bytes

    void reset() {
      offset = 0;
      laneOffset = 0;
      fragIndex = 0;
    }

    void add(const AddrRule &rule, frag_index_t delta) {
      if (delta >= 0) {
        while (delta >= rule.fragsPerLane) {
          delta -= rule.fragsPerLane;
          laneOffset += rule.laneStride;
          offset += rule.laneStride;
        }
        fragIndex += delta;
        offset += delta;
        if (fragIndex >= rule.fragsPerLane) {
          fragIndex -= rule.fragsPerLane;
          offset -= rule.fragsPerLane;
          laneOffset += rule.laneStride;
        }
      } else {
        delta = -delta;
        while (delta >= rule.fragsPerLane) {
          delta -= rule.fragsPerLane;
          laneOffset -= rule.laneStride;
          offset -= rule.laneStride;
        }
        fragIndex -= delta;
        offset -= delta;
        if (fragIndex < 0) {
          laneOffset -= rule.laneStride;
          fragIndex += rule.fragsPerLane;
          offset += rule.fragsPerLane;
        }
      }
    }

    frag_index_t postIncr(const AddrRule &rule) {
      frag_index_t oldOffset = offset;
      offset += rule.fragStride;
      fragIndex++;
      if (fragIndex >= rule.fragsPerLane) {
        fragIndex = 0;
        laneOffset += rule.laneStride;
        offset = laneOffset;
      }
      return oldOffset;
    }

    frag_index_t preDecr(const AddrRule &rule) {
      offset -= rule.fragStride;
      fragIndex--;
      if (fragIndex < 0) {
        fragIndex = rule.fragsPerLane - 1;
        laneOffset -= rule.laneStride;
        offset = laneOffset + fragIndex;
      }
      return offset;
    }
  };

  FontFlags flags;
  const fragment_t *lut;
  const uint8_t *microcode;
  uint8_t fontHeight;

  uint8_t *buffData;

  int8_t numLanesToGlyphEnd = 0;

  prog_cntr_t programCounter = 0;
  fragment_t lastFragment = 0;

  AddrRule rule;
  Cursor writeCursor;

  Renderer(const Font &font) {
    this->flags = font.flags();
    this->lut = font.blob + font.lutOffset();
    this->microcode = font.blob + font.microCodeOffset();
    this->fontHeight = font.fontHeight();

    if (flags & FontFlags::VERTICAL_SCAN) {
      rule.fragsPerLane = fontHeight;
      rule.laneStride = 1;
    } else {
      rule.lanesPerGlyph = (fontHeight + 7) / 8;
      rule.fragStride = 1;
    }
  }

  Status render(Glyph &glyph, GlyphBuffer &buff) {
    // buffStride = buff.stride;
    buffData = buff.data;

    int8_t glyphWidth = glyph.width();
    if (flags & FontFlags::VERTICAL_SCAN) {
      rule.fragStride = buff.stride;
      rule.lanesPerGlyph = (glyphWidth + 7) / 8;
    } else {
      rule.fragsPerLane = glyphWidth;
      rule.laneStride = buff.stride;
    }
    numLanesToGlyphEnd = rule.lanesPerGlyph;

    writeCursor.reset();

    lastFragment = 0x00;
    programCounter = glyph.entryPoint();

#ifdef MAMEFONT_STM_VERBOSE
    printf("  entryPoint    : %d\n", programCounter);
    printf("  glyphWidth    : %d\n", glyphWidth);
    printf("  fragsPerLane  : %d\n", rule.fragsPerLane);
    printf("  lanesPerGlyph : %d\n", rule.lanesPerGlyph);
    printf("  fragStride    : %d\n", rule.fragStride);
    printf("  laneStride    : %d\n", rule.laneStride);
#endif

    while (numLanesToGlyphEnd > 0) {
      uint8_t inst = microcode[programCounter++];
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

#ifdef MAMEFONT_STM_VERBOSE

#define MAMEFONT_BEFORE_OPERATION(fmt, ...)               \
  char logBuff[64];                                       \
  stamp();                                                \
  snprintf(logBuff, sizeof(logBuff), fmt, ##__VA_ARGS__); \
  printf("  %-32s -->", logBuff);                         \
  Cursor dumpCursor = writeCursor;

#define MAMEFONT_AFTER_OPERATION(len)                 \
  for (int i = 0; i < len; i++) {                     \
    printf(" %02X", read(dumpCursor.postIncr(rule))); \
  }                                                   \
  printf("\n");

#else

#define MAMEFONT_BEFORE_OPERATION(op, fmt, ...) \
  do {                                          \
  } while (0)

#define MAMEFONT_AFTER_OPERATION(len) \
  do {                                \
  } while (0)

#endif

  MAMEFONT_ALWAYS_INLINE void LUS(uint8_t inst) {
    uint8_t index = inst & 0x3f;
    fragment_t byte = lut[index];
    MAMEFONT_BEFORE_OPERATION("LUS (idx=%d)", index);
    write(byte);
    MAMEFONT_AFTER_OPERATION(1);
  }

  MAMEFONT_ALWAYS_INLINE void LUD(uint8_t inst) {
    uint8_t index = inst & 0x0f;
    uint8_t step = (inst >> 4) & 0x1;
    MAMEFONT_BEFORE_OPERATION("LUD (idx=%d, step=%d)", index, step);
    write(lut[index]);
    write(lut[index + step]);
    MAMEFONT_AFTER_OPERATION(2);
  }

  MAMEFONT_ALWAYS_INLINE void SLC_SLS_SRC_SRS(uint8_t inst) {
    uint8_t dir = inst & 0x20;
    uint8_t postOp = inst & 0x10;
    uint8_t size = ((inst >> 2) & 0x3) + 1;
    uint8_t rptCount = (inst & 0x03) + 1;

    const char *mne = dir ? (postOp ? "SRS" : "SRC") : (postOp ? "SLS" : "SLC");
    MAMEFONT_BEFORE_OPERATION("%s (size=%1d, rpt=%1d)", mne, size, rptCount);

    fragment_t modifier = (1 << size) - 1;
    if (dir != 0) modifier <<= (8 - size);
    if (postOp == 0) modifier = ~modifier;
    for (int8_t i = rptCount; i != 0; i--) {
      if (dir == 0) {
        lastFragment <<= size;
      } else {
        lastFragment >>= size;
      }
      if (postOp) {
        lastFragment |= modifier;
      } else {
        lastFragment &= modifier;
      }
      write(lastFragment);
    }

    MAMEFONT_AFTER_OPERATION(rptCount);
  }

  MAMEFONT_ALWAYS_INLINE void CPY_REV(uint8_t inst, bool reverse = false) {
    uint8_t offset = (inst >> 3) & 0x3;
    uint8_t length = (inst & 0x07) + 1;

    const char *mne = reverse ? "REV" : "CPY";
    MAMEFONT_BEFORE_OPERATION("%s (ofst=%d, len=%d)", mne, offset, length);

    if (reverse) {
      Cursor readCursor = writeCursor;
      readCursor.add(rule, -offset);
      for (int8_t i = length; i != 0; i--) {
        write(read(readCursor.preDecr(rule)));
      }
    } else {
      Cursor readCursor = writeCursor;
      readCursor.add(rule, -length - offset);
      for (int8_t i = length; i != 0; i--) {
        write(read(readCursor.postIncr(rule)));
      }
    }

    MAMEFONT_AFTER_OPERATION(length);
  }

  MAMEFONT_ALWAYS_INLINE void LDI(uint8_t inst) {
    fragment_t frag = microcode[programCounter++];
    MAMEFONT_BEFORE_OPERATION("LDI (frag=0x%02X)", frag);
    write(frag);
    MAMEFONT_AFTER_OPERATION(1);
  }

  MAMEFONT_ALWAYS_INLINE void RPT(uint8_t inst) {
    uint8_t repeatCount = (inst & 0x0f) + 1;
    MAMEFONT_BEFORE_OPERATION("RPT (rpt=%d)", repeatCount);
    for (int8_t i = repeatCount; i != 0; i--) {
      write(lastFragment);
    }
    MAMEFONT_AFTER_OPERATION(repeatCount);
  }

  MAMEFONT_ALWAYS_INLINE void XOR(uint8_t inst) {
    uint8_t width = ((inst >> 3) & 0x01) + 1;
    uint8_t pos = inst & 0x07;
    uint8_t mask = (1 << width) - 1;
    MAMEFONT_BEFORE_OPERATION("XOR (width=%d, pos=%d)", width, pos);
    write(lastFragment ^ (mask << pos));
    MAMEFONT_AFTER_OPERATION(1);
  }

  MAMEFONT_ALWAYS_INLINE void write(uint8_t value) {
    buffData[writeCursor.postIncr(rule)] = value;
    lastFragment = value;
    if (writeCursor.fragIndex == 0) {
      numLanesToGlyphEnd--;
    }
  }

  MAMEFONT_ALWAYS_INLINE uint8_t read(int16_t offset) const {
    if (offset < 0) return 0;
    return buffData[offset];
  }

  MAMEFONT_ALWAYS_INLINE void stamp() const {
    printf("    ofst=%4d, last=0x%02X ", (int)writeCursor.offset,
           (int)lastFragment);
  }
};

}  // namespace mamefont
