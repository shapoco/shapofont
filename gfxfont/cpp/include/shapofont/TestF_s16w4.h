#pragma once

// Generated from ShapoFont
//   Pixel Count:
//     Effective:   256 px
//     Shrinked :   256 px
//   Estimated Foot Print:
//     Bitmap Data    :    32 Bytes ( 32.00 Bytes/glyph)
//     Glyph Table    :     8 Bytes (  8.00 Bytes/glyph)
//     GFXfont Struct :    10 Bytes
//     Total          :    50 Bytes ( 50.00 Bytes/glyph)
//   Memory Efficiency:  5.120 px/Byte

#include <stdint.h>

#ifdef SHAPOFONT_GFXFONT_INCLUDE_HEADER
#include <gfxfont.h>
#endif

#ifndef SHAPOFONT_GFXFONT_NAMESPACE
#define SHAPOFONT_GFXFONT_NAMESPACE
#endif

#ifndef PROGMEM
#define PROGMEM
#endif

const uint8_t TestF_s16w4Bitmaps[] PROGMEM = {
  0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xF0, 0x00, 0xF0, 0x00, 0xF0, 0x00, 0xF0, 0x00,
  0xFF, 0xFC, 0xFF, 0xFC, 0xFF, 0xFC, 0xFF, 0xFC, 0xF0, 0x00, 0xF0, 0x00, 0xF0, 0x00, 0xF0, 0x00,
};

const SHAPOFONT_GFXFONT_NAMESPACE GFXglyph TestF_s16w4Glyphs[] PROGMEM = {
  { 0x0000, 16, 16, 18,  0, -16 },
};

const SHAPOFONT_GFXFONT_NAMESPACE GFXfont TestF_s16w4 PROGMEM = {
  (uint8_t*)TestF_s16w4Bitmaps,
  (GFXglyph*)TestF_s16w4Glyphs,
  0x46,
  0x46,
  20
};
