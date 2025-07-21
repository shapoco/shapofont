#pragma once

#include <stdint.h>

#if MAMEFONT_STM_VERBOSE
#include <stdio.h>
#endif

#define MAMEFONT_INLINE inline __attribute__((always_inline))

namespace mamefont {

static constexpr uint16_t ENTRYPOINT_DUMMY = 0xffffu;
static constexpr uint8_t HISTORY_SIZE = 32;
static constexpr uint8_t SEGMENT_HEIGHT = 8;

#define MAMEFONT_SUPPORT_RESUME (0)

enum class Status {
  SUCCESS = 0,
  CHAR_CODE_OUT_OF_RANGE,
  GLYPH_NOT_DEFINED,
  UNKNOWN_OPCODE,
};

struct Glyph {
  const uint8_t *blob;

  Glyph() : blob(nullptr) {}
  Glyph(const uint8_t *data) : blob(data) {}

  MAMEFONT_INLINE uint16_t entryPoint() const {
    return reinterpret_cast<const uint16_t *>(blob)[0];
  }

  MAMEFONT_INLINE bool isValid() const {
    return entryPoint() != ENTRYPOINT_DUMMY;
  }

  MAMEFONT_INLINE uint8_t width() const { return blob[2] & 0x3f; }
};

struct RenderContext {
  const Glyph *glyph;
  uint8_t *buff;
  uint16_t start;
  uint16_t end;
  uint16_t wrPos;
  uint8_t last;
#if MAMEFONT_SUPPORT_RESUME
  uint8_t *history;
#endif
  const uint8_t *microcode;

  void init(const uint8_t *entryPoint, const Glyph *glyph, uint8_t *buff,
            uint16_t start = 0, uint16_t end = 0xffff
#if MAMEFONT_SUPPORT_RESUME
            ,
            uint8_t *history = nullptr
#endif
  ) {
    this->glyph = glyph;
    this->buff = buff;
    this->start = start;
    this->end = end;
    this->wrPos = 0;
    this->last = 0;
#if MAMEFONT_SUPPORT_RESUME
    this->history = history;
#endif
    this->microcode = entryPoint;
  }

  void write(uint8_t value) {
    if (start <= wrPos && wrPos < end) {
      buff[wrPos++] = value;
    }
#if MAMEFONT_SUPPORT_RESUME
    if (history) {
      history[wrPos & (HISTORY_SIZE - 1)] = value;
    }
#endif
    this->last = value;
  }

  uint8_t read(uint16_t pos) const {
#if MAMEFONT_SUPPORT_RESUME
    if (history) {
      return history[pos & (HISTORY_SIZE - 1)];
    } else {
      return buff[pos];
    }
#else
    return buff[pos];
#endif
  }
};  // namespace mamefont

static MAMEFONT_INLINE void opSXX(RenderContext *ctx, uint8_t inst) {
  uint8_t last = ctx->last;
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
    ctx->write(last);
  }

#if MAMEFONT_STM_VERBOSE
  printf("    S%c%c(shift_size=%1d, repeat_count=%1d)\n", shift_dir ? 'R' : 'L',
         post_op ? 'S' : 'C', shift_size, repeat_count);
  printf("      --> 0x%02x\n", last);
#endif
}

static MAMEFONT_INLINE void opCPY(RenderContext *ctx, uint8_t inst) {
  uint8_t offset = (inst >> 4) & 0x3;
  uint8_t length = (inst & 0x0f) + 1;
  uint16_t rdPos = ctx->wrPos - length - offset;
  for (int i = length; i != 0; i--) {
    ctx->write(ctx->read(rdPos++));
  }
#if MAMEFONT_STM_VERBOSE
  printf("    CPY(offset=%d, length=%d)\n", offset, length);
  printf("      -->");
  for (int i = 0; i < length; i++) {
    printf(" 0x%02x", ctx->read(ctx->wrPos - length + i));
  }
  printf("\n");
#endif
}

static MAMEFONT_INLINE void opLDI(RenderContext *ctx, uint8_t inst) {
  uint8_t seg = *(ctx->microcode++);
  ctx->write(seg);
#if MAMEFONT_STM_VERBOSE
  printf("    LDI(segment=0x%02x)\n", seg);
  printf("      --> 0x%02x\n", seg);
#endif
}

static MAMEFONT_INLINE void opRPT(RenderContext *ctx, uint8_t inst) {
  uint8_t repeat_count = (inst & 0x0f) + 1;
  for (int i = repeat_count; i != 0; i--) {
    ctx->write(ctx->last);
  }
#if MAMEFONT_STM_VERBOSE
  printf("    RPT(repeat_count=%d)\n", repeat_count);
  printf("      --> 0x%02x\n", ctx->last);
#endif
}

static MAMEFONT_INLINE void opXOR(RenderContext *ctx, uint8_t inst) {
  uint8_t mask_width = ((inst >> 3) & 0x01) + 1;
  uint8_t mask_pos = inst & 0x07;
  uint8_t mask = (1 << mask_width) - 1;
  ctx->write(ctx->last ^ (mask << mask_pos));
#if MAMEFONT_STM_VERBOSE
  printf("    XOR(mask_width=%d, mask_pos=%d)\n", mask_width, mask_pos);
  printf("      --> 0x%02x\n", ctx->last);
#endif
}

class Font {
 public:
  static constexpr uint8_t OFST_FORMAT_VERSION = 0;
  static constexpr uint8_t OFST_FIRST_CODE = 1;
  static constexpr uint8_t OFST_GLYPH_TABLE_LEN = 2;
  static constexpr uint8_t OFST_LUT_SIZE = 3;
  static constexpr uint8_t OFST_FONT_DIMENSION_0 = 4;
  static constexpr uint8_t OFST_FONT_DIMENSION_1 = 5;
  static constexpr uint8_t OFST_FONT_FLAGS = 7;

  static constexpr uint8_t OFST_GLYPH_TABLE = 8;
  static constexpr uint8_t GLYPH_TABLE_ENTRY_SIZE = 4;

  static constexpr uint8_t OFST_ENTRY_POINT = 0;
  static constexpr uint8_t OFST_GLYPH_DIMENSION = 2;

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

  MAMEFONT_INLINE uint8_t glyphHeight() const {
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

  MAMEFONT_INLINE uint16_t lutOffset() const {
    return OFST_GLYPH_TABLE + glyphTableLen() * GLYPH_TABLE_ENTRY_SIZE;
  }

  MAMEFONT_INLINE uint16_t microCodeOffset() const {
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

  MAMEFONT_INLINE uint16_t calcGlyphBufferSize(const Glyph *glyph) const {
    uint16_t w = glyph->width();
    uint16_t h = glyphHeight();
    if (verticalScanEnabled()) {
      return ((w + 7) / 8) * h;
    } else {
      return w * ((h + 7) / 8);
    }
  }

  MAMEFONT_INLINE uint16_t calcGlyphBufferSize() const {
    const Glyph maxGlyph = getMaxWideGlyph();
    return calcGlyphBufferSize(&maxGlyph);
  }

  Status renderGlyph(RenderContext *ctx) const {
    const uint8_t *lut = blob + lutOffset();

    if (ctx->end == 0xffff) {
      ctx->end = calcGlyphBufferSize(ctx->glyph);
    }

    while (ctx->wrPos < ctx->end) {
      uint8_t inst = *(ctx->microcode++);
      uint8_t seg;
      switch (inst & 0xf0) {
        case 0x00:  // LKP
        case 0x10:  // LKP
        case 0x20:  // LKP
        case 0x30:  // LKP
          seg = lut[inst & 0x3f];
#if MAMEFONT_STM_VERBOSE
          printf("    LKP(index=%d)\n", inst & 0x3f);
          printf("      --> 0x%02x\n", seg);
#endif
          ctx->write(seg);
          break;

        case 0x40:  // SLC
        case 0x50:  // SLS
        case 0x60:  // SRC
        case 0x70:  // SRS
          opSXX(ctx, inst);
          break;

        case 0x80:  // CPY
        case 0x90:  // CPY
        case 0xa0:  // CPY
        case 0xb0:  // CPY
          opCPY(ctx, inst);
          break;

        case 0xc0:  // REV or LDI
        case 0xd0:  // REV
          if (inst == 0xc0) {
            opLDI(ctx, inst);
          } else {
            // REV
            return Status::UNKNOWN_OPCODE;
          }
          break;
          ;

        case 0xe0:  // RPT
          opRPT(ctx, inst);
          break;

        case 0xf0:  // XOR
          if (inst == 0xff) return Status::UNKNOWN_OPCODE;
          opXOR(ctx, inst);
          break;

        default:
          return Status::UNKNOWN_OPCODE;
      }
    }
    return Status::SUCCESS;
  }

  Status renderGlyph(uint8_t c, uint8_t *buff, uint8_t *width) const {
    Glyph glyph;
    Status ret = getGlyph(c, &glyph);
    if (ret != Status::SUCCESS) return ret;
    RenderContext ctx;
    ctx.init(getEntryPoint(glyph), &glyph, buff);
    if (width) *width = glyph.width();
    return renderGlyph(&ctx);
  }
};
}  // namespace mamefont
