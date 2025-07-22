#pragma once

#include "mamefont_common.hpp"

namespace mamefont {

struct Glyph {
  const uint8_t *blob;

  Glyph() : blob(nullptr) {}
  Glyph(const uint8_t *data) : blob(data) {}

  MAMEFONT_INLINE int16_t entryPoint() const {
    return reinterpret_cast<const int16_t *>(blob)[0];
  }

  MAMEFONT_INLINE bool isValid() const {
    return entryPoint() != ENTRYPOINT_DUMMY;
  }

  MAMEFONT_INLINE uint8_t width() const { return blob[2] & 0x3f; }
  MAMEFONT_INLINE uint8_t xAdvance() const { return blob[3] & 0x3f; }
};

struct StateMachine {
  const uint8_t *lut;
  const uint8_t *microcode;
  uint8_t *buff;
  int16_t endPos;

  int16_t wrPos;
  uint8_t last;

  void init(const uint8_t *lut, const uint8_t *entryPoint, uint8_t *buff,
            int16_t bytesToWrite) {
    this->lut = lut;
    this->microcode = entryPoint;
    this->buff = buff;
    this->endPos = bytesToWrite - 1;

    this->wrPos = 0;
    this->last = 0;
  }

  MAMEFONT_INLINE void write(uint8_t value) {
    buff[wrPos++] = value;
    last = value;
  }

  MAMEFONT_INLINE uint8_t read(int16_t pos) const {
    if (pos < 0) return 0;
    return buff[pos];
  }

  MAMEFONT_INLINE void LKP(uint8_t inst) {
    uint8_t seg = lut[inst & 0x3f];
#if MAMEFONT_STM_VERBOSE
    char buff[64];
    snprintf(buff, sizeof(buff), "LKP(index=%d)", inst & 0x3f);
    printf("    %-40s --> 0x%02x\n", buff, seg);
#endif
    write(seg);
  }

  MAMEFONT_INLINE void Sxx(uint8_t inst) {
    uint8_t shift_dir = inst & 0x20;
    uint8_t post_op = inst & 0x10;
    uint8_t shift_size = ((inst >> 2) & 0x3) + 1;
    uint8_t repeat_count = (inst & 0x03) + 1;

    uint8_t modifier = (1 << shift_size) - 1;
    if (shift_dir != 0) modifier <<= (8 - shift_size);
    if (post_op == 0) modifier = ~modifier;
    for (int8_t i = repeat_count; i != 0; i--) {
      if (shift_dir == 0) {
        last <<= shift_size;
      } else {
        last >>= shift_size;
      }
      if (post_op) {
        last |= modifier;
      } else {
        last &= modifier;
      }
      write(last);
    }

#if MAMEFONT_STM_VERBOSE
    char buff[64];
    snprintf(buff, sizeof(buff), "S%c%c(shift_size=%1d, repeat_count=%1d)",
             shift_dir ? 'R' : 'L', post_op ? 'S' : 'C', shift_size,
             repeat_count);
    printf("    %-40s -->", buff);
    for (int i = 0; i < repeat_count; i++) {
      printf(" 0x%02x", read(wrPos - repeat_count + i));
    }
    printf("\n");
#endif
  }

  MAMEFONT_INLINE void CPY_REV(uint8_t inst, bool reverse = false) {
    uint8_t offset = (inst >> 3) & 0x3;
    uint8_t length = (inst & 0x07) + 1;
    if (reverse) {
      int16_t rdPos = wrPos - offset;
      for (int8_t i = length; i != 0; i--) {
        write(read(--rdPos));
      }
    } else {
      int16_t rdPos = wrPos - length - offset;
      for (int8_t i = length; i != 0; i--) {
        write(read(rdPos++));
      }
    }

#if MAMEFONT_STM_VERBOSE
    char buff[64];
    snprintf(buff, sizeof(buff), "%s(offset=%d, length=%d)",
             reverse ? "REV" : "CPY", offset, length);
    printf("    %-40s -->", buff);
    for (int i = 0; i < length; i++) {
      printf(" 0x%02x", read(wrPos - length + i));
    }
    printf("\n");
#endif
  }

  MAMEFONT_INLINE void LDI(uint8_t inst) {
    uint8_t seg = *(microcode++);
    write(seg);
#if MAMEFONT_STM_VERBOSE
    char buff[64];
    snprintf(buff, sizeof(buff), "LDI(byte=0x%02x)", seg);
    printf("    %-40s --> 0x%02x\n", buff, seg);
#endif
  }

  MAMEFONT_INLINE void RPT(uint8_t inst) {
    uint8_t repeat_count = (inst & 0x0f) + 1;
    for (int8_t i = repeat_count; i != 0; i--) {
      write(last);
    }
#if MAMEFONT_STM_VERBOSE
    char buff[64];
    snprintf(buff, sizeof(buff), "RPT(repeat_count=%d)", repeat_count);
    printf("    %-40s -->", buff);
    for (int i = 0; i < repeat_count; i++) {
      printf(" 0x%02x", read(wrPos - repeat_count + i));
    }
    printf("\n");
#endif
  }

  MAMEFONT_INLINE void XOR(uint8_t inst) {
    uint8_t mask_width = ((inst >> 3) & 0x01) + 1;
    uint8_t mask_pos = inst & 0x07;
    uint8_t mask = (1 << mask_width) - 1;
    write(last ^ (mask << mask_pos));
#if MAMEFONT_STM_VERBOSE
    char buff[64];
    snprintf(buff, sizeof(buff), "XOR(mask_width=%d, mask_pos=%d)", mask_width,
             mask_pos);
    printf("    %-40s --> 0x%02x\n", buff, last);
#endif
  }

  Status run() {
    while (wrPos <= endPos) {
      uint8_t inst = *(microcode++);
      uint8_t seg;
      switch (inst & 0xf0) {
        case 0x00:  // LKP
        case 0x10:  // LKP
        case 0x20:  // LKP
        case 0x30:  // LKP
          LKP(inst);
          break;

        case 0x40:  // SLC
        case 0x50:  // SLS
        case 0x60:  // SRC
        case 0x70:  // SRS
          Sxx(inst);
          break;

        case 0x80:  // CPY
        case 0x90:  // CPY
        case 0xa0:  // CPY
        case 0xb0:  // CPY
          if (inst == 0x80) {
            LDI(inst);
          } else {
            CPY_REV(inst, false);
          }
          break;

        case 0xc0:  // REV or LDI
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
};

class Font {
 public:
  const uint8_t *blob;

  Font(const uint8_t *blob) : blob(blob) {}

  MAMEFONT_INLINE uint8_t firstCode() const { return blob[OFST_FIRST_CODE]; }

  MAMEFONT_INLINE uint8_t glyphTableLen() const {
    return blob[OFST_GLYPH_TABLE_LEN];
  }

  MAMEFONT_INLINE uint8_t lastCode() const {
    return firstCode() + glyphTableLen() - 1;
  }

  MAMEFONT_INLINE uint8_t lutSize() const { return blob[OFST_LUT_SIZE]; }

  MAMEFONT_INLINE uint8_t fontHeight() const {
    return blob[OFST_FONT_DIMENSION_0] & 0x3f;
  }

  MAMEFONT_INLINE const bool verticalScanEnabled() const {
    return blob[OFST_FONT_FLAGS] & 0x80;
  }

  MAMEFONT_INLINE const Glyph glyphTableEntry(uint8_t index) const {
    return Glyph(blob + OFST_GLYPH_TABLE + index * GLYPH_TABLE_ENTRY_SIZE);
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
    return OFST_GLYPH_TABLE + glyphTableLen() * GLYPH_TABLE_ENTRY_SIZE;
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

  MAMEFONT_INLINE int16_t calcGlyphBufferSize(const Glyph *glyph) const {
    int16_t w = glyph->width();
    int16_t h = fontHeight();
    if (verticalScanEnabled()) {
      return ((w + 7) / 8) * h;
    } else {
      return w * ((h + 7) / 8);
    }
  }

  MAMEFONT_INLINE int16_t calcGlyphBufferSize() const {
    const Glyph maxGlyph = getMaxWideGlyph();
    return calcGlyphBufferSize(&maxGlyph);
  }

  Status initStm(StateMachine &stm, Glyph &glyph, uint8_t *buff) const {
    stm.init(blob + lutOffset(), getEntryPoint(glyph), buff,
             calcGlyphBufferSize(&glyph));
    return Status::SUCCESS;
  }

  Status drawChar(uint8_t c, uint8_t *buff, uint8_t *xAdvance) const {
    Status ret;

    Glyph glyph;
    ret = getGlyph(c, &glyph);
    if (ret != Status::SUCCESS) goto advance;

    StateMachine stm;
    ret = initStm(stm, glyph, buff);
    if (ret != Status::SUCCESS) goto advance;

    ret = stm.run();

  advance:
    if (xAdvance) {
      *xAdvance = (ret == Status::SUCCESS) ? glyph.xAdvance() : 0;
    }
  }
};

}  // namespace mamefont
