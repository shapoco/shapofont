#pragma once

#include <stdint.h>

#if MAMEFONT_STM_VERBOSE
#include <stdio.h>
#endif

#define MAMEFONT_INLINE inline __attribute__((always_inline))

namespace mamefont {

static constexpr int16_t ENTRYPOINT_DUMMY = 0xffff;
static constexpr uint8_t HISTORY_SIZE = 32;
static constexpr uint8_t SEGMENT_HEIGHT = 8;

static constexpr uint8_t OFST_FORMAT_VERSION = 0;
static constexpr uint8_t OFST_FIRST_CODE = 1;
static constexpr uint8_t OFST_GLYPH_TABLE_LEN = 2;
static constexpr uint8_t OFST_LUT_SIZE = 3;
static constexpr uint8_t OFST_FONT_DIMENSION_0 = 4;
static constexpr uint8_t OFST_FONT_DIMENSION_1 = 5;
static constexpr uint8_t OFST_FONT_FLAGS = 7;

static constexpr uint8_t OFST_GLYPH_TABLE = 8;

static constexpr uint8_t OFST_ENTRY_POINT = 0;
static constexpr uint8_t OFST_GLYPH_DIMENSION_0 = 2;
static constexpr uint8_t OFST_GLYPH_DIMENSION_1 = 3;

enum FontFlags : uint8_t {
  VERTICAL_SCAN = 0x80,
  BIT_REVERSE = 0x40,
  SHRINKED_GLYPH_TABLE = 0x20,
};

enum class Status {
  SUCCESS = 0,
  CHAR_CODE_OUT_OF_RANGE,
  GLYPH_NOT_DEFINED,
  UNKNOWN_OPCODE,
};

}  // namespace mamefont
