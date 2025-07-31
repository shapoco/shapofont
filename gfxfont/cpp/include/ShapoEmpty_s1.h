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
//   Memory Efficiency:  0.056 px/Byte

#include <stdint.h>

#ifdef SHAPOFONT_INCLUDE_AVR_PGMSPACE
#include <avr/pgmspace.h>
#endif

#ifdef SHAPOFONT_INCLUDE_GFXFONT
#include <gfxfont.h>
#endif

#ifndef SHAPOFONT_PROGMEM
#ifdef PROGMEM
#define SHAPOFONT_PROGMEM PROGMEM
#else
#define SHAPOFONT_PROGMEM
#endif
#define SHAPOFONT_PROGMEM_SELF_DEFINED
#endif

#ifndef SHAPOFONT_GFXFONT_NAMESPACE
#define SHAPOFONT_GFXFONT_NAMESPACE
#define SHAPOFONT_GFXFONT_NAMESPACE_SELF_DEFINED
#endif

const uint8_t ShapoEmpty_s1Bitmaps[] SHAPOFONT_PROGMEM = {
};

const SHAPOFONT_GFXFONT_NAMESPACE GFXglyph ShapoEmpty_s1Glyphs[] SHAPOFONT_PROGMEM = {
  { 0x0000,  0,  0,  2,  1,   0 },
};

const SHAPOFONT_GFXFONT_NAMESPACE GFXfont ShapoEmpty_s1 SHAPOFONT_PROGMEM = {
  (uint8_t*)ShapoEmpty_s1Bitmaps,
  (GFXglyph*)ShapoEmpty_s1Glyphs,
  0x20,
  0x20,
  2
};

#ifdef SHAPOFONT_PROGMEM_SELF_DEFINED
#undef SHAPOFONT_PROGMEM
#endif

#ifdef SHAPOFONT_GFXFONT_NAMESPACE_SELF_DEFINED
#undef SHAPOFONT_GFXFONT_NAMESPACE
#endif
