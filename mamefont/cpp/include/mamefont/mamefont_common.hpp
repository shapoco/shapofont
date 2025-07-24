#pragma once

#include <stdint.h>

#ifdef MAMEFONT_STM_VERBOSE
#include <stdio.h>
#endif

#define MAMEFONT_ALWAYS_INLINE inline __attribute__((always_inline))

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

using fragment_t = uint8_t;

#ifdef MAMEFONT_32BIT_ADDR
using frag_index_t = int32_t;
#elifdef MAMEFONT_8BIT_ADDR
using frag_index_t = int8_t;
#else
using frag_index_t = int16_t;
#endif

#ifdef MAMEFONT_8BIT_PC
using prog_cntr_t = uint8_t;
#else
using prog_cntr_t = uint16_t;
#endif

}  // namespace mamefont
