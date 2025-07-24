#pragma once

// Generated from ShapoFont
//   Pixel Count:
//     Effective:     1 px
//     Shrinked :     0 px
//   Estimated Foot Print:
//     Bitmap Data    :     0 Bytes (  0.00 Bytes/glyph)
//     Glyph Table    :     8 Bytes (  8.00 Bytes/glyph)
//     GFXfont Struct :    10 Bytes
//     Total          :    18 Bytes ( 18.00 Bytes/glyph)

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

const uint8_t Empty_s1Bitmaps[] PROGMEM = {
};

const SHAPOFONT_GFXFONT_NAMESPACE GFXglyph Empty_s1Glyphs[] PROGMEM = {
  { 0x0000,  0,  0,  2,  1,   0 },
};

const SHAPOFONT_GFXFONT_NAMESPACE GFXfont Empty_s1 PROGMEM = {
  (uint8_t*)Empty_s1Bitmaps,
  (GFXglyph*)Empty_s1Glyphs,
  0x20,
  0x20,
  2
};
