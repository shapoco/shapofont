#pragma once

// Generated from ShapoFont
//   Pixel Count:
//     Effective:    64 px
//     Shrinked :    64 px
//   Estimated Foot Print:
//     Bitmap Data    :     8 Bytes (  8.00 Bytes/glyph)
//     Glyph Table    :     8 Bytes (  8.00 Bytes/glyph)
//     GFXfont Struct :    10 Bytes
//     Total          :    26 Bytes ( 26.00 Bytes/glyph)
//   Memory Efficiency:  2.462 px/Byte

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

const uint8_t TestF_s8w2Bitmaps[] PROGMEM = {
  0xFF, 0xFF, 0xC0, 0xC0, 0xFE, 0xFE, 0xC0, 0xC0,
};

const SHAPOFONT_GFXFONT_NAMESPACE GFXglyph TestF_s8w2Glyphs[] PROGMEM = {
  { 0x0000,  8,  8,  9,  0,  -8 },
};

const SHAPOFONT_GFXFONT_NAMESPACE GFXfont TestF_s8w2 PROGMEM = {
  (uint8_t*)TestF_s8w2Bitmaps,
  (GFXglyph*)TestF_s8w2Glyphs,
  0x46,
  0x46,
  10
};
