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

const uint8_t TestF_s16w4Bitmaps[] SHAPOFONT_PROGMEM = {
  0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xF0, 0x00, 0xF0, 0x00, 0xF0, 0x00, 0xF0, 0x00,
  0xFF, 0xFC, 0xFF, 0xFC, 0xFF, 0xFC, 0xFF, 0xFC, 0xF0, 0x00, 0xF0, 0x00, 0xF0, 0x00, 0xF0, 0x00,
};

const SHAPOFONT_GFXFONT_NAMESPACE GFXglyph TestF_s16w4Glyphs[] SHAPOFONT_PROGMEM = {
  { 0x0000, 16, 16, 18,  0, -16 },
};

const SHAPOFONT_GFXFONT_NAMESPACE GFXfont TestF_s16w4 SHAPOFONT_PROGMEM = {
  (uint8_t*)TestF_s16w4Bitmaps,
  (GFXglyph*)TestF_s16w4Glyphs,
  0x46,
  0x46,
  20
};

#ifdef SHAPOFONT_PROGMEM_SELF_DEFINED
#undef SHAPOFONT_PROGMEM
#endif

#ifdef SHAPOFONT_GFXFONT_NAMESPACE_SELF_DEFINED
#undef SHAPOFONT_GFXFONT_NAMESPACE
#endif
