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

const uint8_t TestF_s08w02Bitmaps[] SHAPOFONT_PROGMEM = {
  0xFF, 0xFF, 0xC0, 0xC0, 0xFE, 0xFE, 0xC0, 0xC0,
};

const SHAPOFONT_GFXFONT_NAMESPACE GFXglyph TestF_s08w02Glyphs[] SHAPOFONT_PROGMEM = {
  { 0x0000,  8,  8,  9,  0,  -8 },
};

const SHAPOFONT_GFXFONT_NAMESPACE GFXfont TestF_s08w02 SHAPOFONT_PROGMEM = {
  (uint8_t*)TestF_s08w02Bitmaps,
  (GFXglyph*)TestF_s08w02Glyphs,
  0x46,
  0x46,
  10
};

#ifdef SHAPOFONT_PROGMEM_SELF_DEFINED
#undef SHAPOFONT_PROGMEM
#endif

#ifdef SHAPOFONT_GFXFONT_NAMESPACE_SELF_DEFINED
#undef SHAPOFONT_GFXFONT_NAMESPACE
#endif
