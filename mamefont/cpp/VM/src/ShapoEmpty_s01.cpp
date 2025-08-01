// Generated by MameFont
//   Format Version: 1
//   First Code      : 32
//   Glyph Count     : 1
//   Font Height     : 1 px
//   Max Glyph Width : 1 px
//   Total Pixels    : 1 px
//   Fragment Shape  : Vertical
//   Bit Order       : MSB First
//   Shrinked Format : Yes
//   Estimated Footprint:
//     Header        :    8 Bytes
//     Glyph Table   :    2 Bytes (2 Bytes/glyph)
//     Lookup Table  :    2 Bytes (3.12% used)
//     Bytecodes     :    5 Bytes (5.00 Bytes/glyph)
//     Total         :   17 Bytes (17.00 Bytes/glyph)
//   Compression Performance:
//     RPT         :    1 -->    1 (  +0.00%)
//     Total       :    1 -->    1 (  +0.00%)
//   Memory Efficiency:  0.059 px/Byte

#include <stdint.h>
#include <mamefont/mamefont.hpp>

#ifdef MAMEFONT_USE_PROGMEM
#include <avr/pgmspace.h>
#define MAMEFONT_PROGMEM PROGMEM
#else
#define MAMEFONT_PROGMEM
#endif

const uint8_t ShapoEmpty_s01_blob[] MAMEFONT_PROGMEM = {
  // Font Header
  0x01, 0xE0, 0x20, 0x00, 0x01, 0x00, 0x01, 0x00,
  // Glyph Table
  0x00, 0x10,
  // Lookup Table
  0x00, 0x00,
  // Bytecodes
  0xE0, 0xFF, 0xFF, 0xFF, 0xFF,
};

extern const mamefont::Font ShapoEmpty_s01(ShapoEmpty_s01_blob);

#undef MAMEFONT_PROGMEM
