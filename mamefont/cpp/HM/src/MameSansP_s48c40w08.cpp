// Generated by MameFont
//   Format Version: 1
//   First Code      : 32
//   Glyph Count     : 95
//   Font Height     : 48 px
//   Max Glyph Width : 40 px
//   Total Pixels    : 107328 px
//   Fragment Shape  : Horizontal
//   Bit Order       : MSB First
//   Shrinked Format : No
//   Estimated Footprint:
//     Header        :    8 Bytes
//     Glyph Table   :  380 Bytes (4 Bytes/glyph)
//     Lookup Table  :   40 Bytes (62.50% used)
//     Bytecodes     : 2399 Bytes (25.25 Bytes/glyph)
//     Total         : 2827 Bytes (29.76 Bytes/glyph)
//   Compression Performance:
//     CPX         : 6716 -->  678 ( -44.14%)
//     CPY         :  661 -->  103 (  -4.08%)
//     LUD (step=0):  206 -->  103 (  -0.75%)
//     LUD (step=1):  154 -->   77 (  -0.56%)
//     LUP         :  566 -->  566 (  +0.00%)
//     RPT         : 4627 -->  594 ( -29.48%)
//     SFT         :  731 -->  256 (  -3.47%)
//     XOR         :   19 -->   19 (  +0.00%)
//     Total       : 13680 --> 2396 ( -82.49%)
//   Memory Efficiency: 37.965 px/Byte

#include <stdint.h>
#include <mamefont/mamefont.hpp>

#ifdef MAMEFONT_USE_PROGMEM
#include <avr/pgmspace.h>
#define MAMEFONT_PROGMEM PROGMEM
#else
#define MAMEFONT_PROGMEM
#endif

const uint8_t MameSansP_s48c40w08_blob[] MAMEFONT_PROGMEM = {
  // Font Header
  0x01, 0x40, 0x20, 0x5E, 0x27, 0x2F, 0x0A, 0x27,
  // Glyph Table
  0x00, 0x00, 0x07, 0x13, 0x03, 0x00, 0x07, 0x13, 0x0A, 0x00, 0x0D, 0x13, 0x18, 0x00, 0x17, 0x13,
  0x37, 0x00, 0x17, 0x13, 0x55, 0x00, 0x1F, 0x13, 0x7D, 0x00, 0x1C, 0x13, 0xC5, 0x00, 0x07, 0x13,
  0xCE, 0x00, 0x0E, 0x13, 0xEA, 0x00, 0x0E, 0x13, 0x04, 0x01, 0x17, 0x13, 0x12, 0x01, 0x17, 0x13,
  0x1D, 0x01, 0x07, 0x13, 0x26, 0x01, 0x17, 0x13, 0x31, 0x01, 0x07, 0x13, 0x37, 0x01, 0x1A, 0x13,
  0x4F, 0x01, 0x17, 0x13, 0x63, 0x01, 0x17, 0x13, 0x73, 0x01, 0x17, 0x13, 0xA3, 0x01, 0x17, 0x13,
  0xD0, 0x01, 0x17, 0x13, 0xF1, 0x01, 0x17, 0x13, 0x1F, 0x02, 0x17, 0x13, 0x45, 0x02, 0x17, 0x13,
  0x60, 0x02, 0x17, 0x13, 0x7D, 0x02, 0x17, 0x13, 0xA2, 0x02, 0x07, 0x13, 0xAA, 0x02, 0x07, 0x13,
  0xB6, 0x02, 0x17, 0x13, 0xC8, 0x02, 0x17, 0x13, 0xD4, 0x02, 0x17, 0x13, 0xE6, 0x02, 0x17, 0x13,
  0x0A, 0x03, 0x1F, 0x13, 0x3E, 0x03, 0x1F, 0x13, 0x63, 0x03, 0x1F, 0x13, 0x8D, 0x03, 0x1F, 0x13,
  0xB6, 0x03, 0x1F, 0x13, 0xD5, 0x03, 0x17, 0x13, 0xE6, 0x03, 0x17, 0x13, 0xF7, 0x03, 0x1F, 0x13,
  0x27, 0x04, 0x1F, 0x13, 0x35, 0x04, 0x0B, 0x13, 0x43, 0x04, 0x1F, 0x13, 0x69, 0x04, 0x1F, 0x13,
  0x85, 0x04, 0x1B, 0x13, 0x95, 0x04, 0x27, 0x13, 0xB4, 0x04, 0x1F, 0x13, 0xCF, 0x04, 0x1F, 0x13,
  0xEA, 0x04, 0x1F, 0x13, 0x06, 0x05, 0x1F, 0x13, 0x2D, 0x05, 0x1F, 0x13, 0x53, 0x05, 0x1F, 0x13,
  0x7A, 0x05, 0x1F, 0x13, 0x8A, 0x05, 0x1F, 0x13, 0xA3, 0x05, 0x1F, 0x13, 0xC4, 0x05, 0x27, 0x13,
  0xED, 0x05, 0x1F, 0x13, 0x08, 0x06, 0x1F, 0x13, 0x1F, 0x06, 0x1F, 0x13, 0x38, 0x06, 0x0F, 0x13,
  0x43, 0x06, 0x1A, 0x13, 0x5D, 0x06, 0x0F, 0x13, 0x67, 0x06, 0x0F, 0x13, 0x6F, 0x06, 0x17, 0x13,
  0x7A, 0x06, 0x0B, 0x13, 0x8B, 0x06, 0x17, 0x13, 0xAD, 0x06, 0x17, 0x13, 0xC6, 0x06, 0x17, 0x13,
  0xE5, 0x06, 0x17, 0x13, 0x00, 0x07, 0x17, 0x13, 0x1B, 0x07, 0x0F, 0x13, 0x31, 0x07, 0x17, 0x13,
  0x56, 0x07, 0x17, 0x13, 0x6C, 0x07, 0x09, 0x13, 0x7D, 0x07, 0x0C, 0x13, 0x95, 0x07, 0x17, 0x13,
  0xAA, 0x07, 0x09, 0x13, 0xB5, 0x07, 0x1F, 0x13, 0xD1, 0x07, 0x17, 0x13, 0xE7, 0x07, 0x17, 0x13,
  0xFD, 0x07, 0x17, 0x13, 0x16, 0x08, 0x17, 0x13, 0x2F, 0x08, 0x0F, 0x13, 0x3C, 0x08, 0x17, 0x13,
  0x6A, 0x08, 0x0F, 0x13, 0x81, 0x08, 0x17, 0x13, 0x96, 0x08, 0x17, 0x13, 0xB1, 0x08, 0x1F, 0x13,
  0xCC, 0x08, 0x17, 0x13, 0xE0, 0x08, 0x17, 0x13, 0x07, 0x09, 0x17, 0x13, 0x17, 0x09, 0x0F, 0x13,
  0x2F, 0x09, 0x07, 0x13, 0x34, 0x09, 0x0F, 0x13, 0x48, 0x09, 0x17, 0x13,
  // Lookup Table
  0x03, 0x07, 0x3F, 0x7F, 0xFF, 0x00, 0x01, 0x1F, 0x0F, 0xC3, 0x81, 0x80, 0xE0, 0xFC, 0xFE, 0x3C,
  0x38, 0x40, 0x78, 0xF8, 0xF9, 0xE1, 0xE7, 0x1E, 0x3E, 0x0C, 0x7E, 0xC0, 0x87, 0xE3, 0xC7, 0xEF,
  0x9F, 0xF1, 0x8F, 0xFD, 0x18, 0x30, 0x83, 0xC1,
  // Bytecodes
  0xEF, 0xEF, 0xEF, 0x84, 0xEA, 0xEF, 0xC5, 0x65, 0x67, 0xE3, 0x8D, 0xE6, 0xCF, 0x90, 0x00, 0xF4,
  0x91, 0x85, 0xE6, 0xEF, 0x40, 0x30, 0x28, 0xED, 0x80, 0xE2, 0x81, 0xE2, 0x84, 0xE6, 0x88, 0xE2,
  0x87, 0xE2, 0x40, 0x20, 0x8A, 0x83, 0xE2, 0x40, 0x24, 0x4A, 0xA1, 0xE2, 0x84, 0xE6, 0x9D, 0xE2,
  0x9E, 0xE2, 0x40, 0x48, 0xFC, 0x85, 0xE6, 0xE2, 0x15, 0x12, 0xD3, 0x01, 0x61, 0xC3, 0x23, 0x25,
  0xE4, 0xF3, 0x8F, 0x40, 0x1E, 0x48, 0xE6, 0x9A, 0xE1, 0x84, 0xE2, 0x72, 0xE3, 0x8E, 0xE3, 0x31,
  0x83, 0x40, 0x44, 0xFC, 0xE9, 0x81, 0x87, 0x11, 0x83, 0x8D, 0x93, 0xE1, 0x77, 0xEC, 0xC6, 0xC0,
  0xC1, 0xC8, 0xC7, 0x40, 0x30, 0x8C, 0x65, 0x94, 0x95, 0x40, 0x20, 0x00, 0x40, 0x26, 0xC6, 0x40,
  0x2E, 0x02, 0x40, 0x0E, 0x06, 0x85, 0xE6, 0x40, 0x44, 0xF8, 0x40, 0xA8, 0xA0, 0xE1, 0x13, 0x88,
  0xC7, 0x82, 0xE1, 0x65, 0x81, 0x12, 0xD2, 0xD3, 0xE2, 0x77, 0x81, 0x25, 0xE7, 0x40, 0x0B, 0x86,
  0x94, 0xCC, 0x9B, 0xE1, 0x31, 0x94, 0x3A, 0xE3, 0xF5, 0xA2, 0x81, 0x22, 0x31, 0xA1, 0x84, 0xE4,
  0x83, 0x85, 0xE6, 0x8B, 0x35, 0x31, 0x40, 0x4A, 0x04, 0x82, 0x11, 0xE2, 0x03, 0x93, 0xA3, 0x84,
  0xE3, 0x83, 0x63, 0x02, 0x07, 0xE9, 0x40, 0x2E, 0x06, 0x66, 0xF3, 0xA4, 0x90, 0x92, 0x93, 0xE3,
  0x01, 0x40, 0x0D, 0x48, 0xE5, 0x84, 0xE6, 0xC7, 0x97, 0xDF, 0xA5, 0x0D, 0xEF, 0xEF, 0xE3, 0x86,
  0x13, 0x87, 0xC2, 0xC3, 0x84, 0xE8, 0x40, 0x20, 0x54, 0x97, 0x98, 0x00, 0x40, 0x16, 0x80, 0x40,
  0x30, 0x02, 0xE1, 0x8B, 0xE1, 0x85, 0xE6, 0x40, 0x20, 0x54, 0x3C, 0x93, 0x20, 0x9A, 0xC2, 0xC7,
  0xC8, 0x81, 0xE1, 0x80, 0xE1, 0x86, 0xE3, 0x40, 0x22, 0x5C, 0x33, 0xE0, 0x40, 0x2F, 0x02, 0x8E,
  0xE8, 0x40, 0x20, 0x54, 0xE7, 0x37, 0xE3, 0x27, 0x63, 0x40, 0x24, 0x58, 0x84, 0xEE, 0xEF, 0x40,
  0x60, 0xB8, 0xEF, 0x84, 0xE6, 0x40, 0x28, 0x20, 0xE3, 0xEF, 0x40, 0x60, 0x3C, 0xEF, 0xEF, 0x84,
  0xE6, 0xC7, 0x97, 0xDF, 0xA5, 0x0D, 0xEF, 0x84, 0xE6, 0x40, 0x30, 0x28, 0xE3, 0x40, 0x60, 0x34,
  0xEF, 0xEF, 0xEF, 0x84, 0xE2, 0x64, 0xE6, 0xE7, 0xEF, 0xC6, 0xC0, 0xC1, 0xC8, 0x40, 0x0A, 0xC6,
  0x85, 0xE2, 0x40, 0x20, 0x18, 0x40, 0x1A, 0xD4, 0x40, 0x32, 0xDC, 0xEF, 0x40, 0xA2, 0xEC, 0xD5,
  0x81, 0x12, 0xD2, 0xD3, 0xED, 0x40, 0x20, 0x54, 0x9A, 0x84, 0xE5, 0x96, 0xCA, 0x85, 0xEE, 0x40,
  0x4E, 0xFC, 0xE4, 0xE2, 0xC6, 0x12, 0x82, 0xE4, 0x98, 0x90, 0x85, 0xEE, 0xEF, 0x40, 0x55, 0x26,
  0x40, 0x8D, 0x34, 0xD5, 0x81, 0x12, 0xD2, 0xD3, 0x84, 0x98, 0x99, 0x85, 0xE7, 0x86, 0x13, 0x87,
  0x82, 0x40, 0x17, 0x00, 0xE6, 0x85, 0xE6, 0x9A, 0x84, 0xE5, 0x96, 0x8A, 0x86, 0x85, 0x61, 0x86,
  0x12, 0x13, 0xE2, 0x03, 0xE0, 0xCC, 0x84, 0xE6, 0x40, 0x60, 0x8C, 0x8E, 0x33, 0x77, 0x03, 0xE6,
  0x40, 0x30, 0x0C, 0x87, 0xE2, 0x64, 0xE4, 0x12, 0xE2, 0x85, 0xE5, 0x99, 0x98, 0xC4, 0xC3, 0xC2,
  0x22, 0x25, 0xE7, 0x84, 0xE6, 0x81, 0x88, 0x13, 0xE5, 0x81, 0xC6, 0x22, 0x63, 0x8A, 0x96, 0x84,
  0xE5, 0x9A, 0x85, 0xE6, 0x8E, 0xE6, 0x02, 0x02, 0x40, 0x50, 0xC4, 0xE4, 0x77, 0x02, 0x06, 0xE6,
  0x80, 0xE2, 0x81, 0xE2, 0x88, 0xE2, 0x40, 0x0C, 0xC6, 0x83, 0xE2, 0x84, 0xE6, 0x85, 0xEE, 0x40,
  0x30, 0x0E, 0x89, 0xE2, 0xA6, 0xE2, 0x40, 0x20, 0x0A, 0x40, 0x6C, 0x58, 0x8D, 0xE6, 0x40, 0x30,
  0x56, 0x87, 0xE6, 0x82, 0xE6, 0x83, 0xE2, 0x85, 0xE5, 0x99, 0x98, 0xC4, 0x40, 0x11, 0x40, 0x22,
  0x25, 0xE7, 0x84, 0xE6, 0x8B, 0xE2, 0x8E, 0x84, 0xE5, 0x81, 0xC6, 0x22, 0x63, 0x8A, 0x96, 0x84,
  0xE5, 0x9A, 0x85, 0xE6, 0x8D, 0xE2, 0x65, 0x40, 0x4C, 0xC8, 0xE4, 0x77, 0x02, 0x05, 0xE7, 0x81,
  0xE2, 0x88, 0xE2, 0x87, 0xE2, 0x82, 0xE2, 0x83, 0xE2, 0x84, 0xE4, 0x6E, 0xC2, 0x22, 0x25, 0xE7,
  0x40, 0x2C, 0x0A, 0x8E, 0x84, 0xE5, 0x96, 0xCA, 0x85, 0xE2, 0x75, 0xE5, 0x9A, 0x85, 0xEA, 0x40,
  0x48, 0xD0, 0x40, 0x60, 0x94, 0x84, 0xE6, 0x8E, 0xE2, 0x40, 0x30, 0x28, 0x86, 0xE2, 0x80, 0xE2,
  0x81, 0xE2, 0x88, 0xE2, 0x40, 0x10, 0xCA, 0x40, 0x28, 0x06, 0x67, 0xE3, 0x40, 0x30, 0x1E, 0xE7,
  0xD5, 0x81, 0x12, 0xD2, 0xE1, 0x65, 0x64, 0x84, 0xE4, 0x77, 0x22, 0x26, 0xE6, 0x9A, 0x84, 0xE5,
  0xD9, 0x62, 0xE6, 0x96, 0xCA, 0x85, 0xE1, 0x66, 0xE5, 0x9A, 0x40, 0x60, 0xB4, 0xD5, 0x81, 0x12,
  0xD2, 0xD3, 0xE5, 0x40, 0x24, 0x5C, 0x9A, 0x84, 0xE5, 0x96, 0xCA, 0x85, 0xE1, 0x66, 0xE5, 0x83,
  0x80, 0xE2, 0x81, 0xE2, 0x88, 0xE2, 0x40, 0x60, 0x94, 0x7C, 0xE2, 0x40, 0x2C, 0x0A, 0x8C, 0xE2,
  0x85, 0xE6, 0xE7, 0x84, 0xE2, 0x64, 0xEA, 0x40, 0x18, 0x10, 0xE7, 0x84, 0xE2, 0x64, 0xE7, 0x77,
  0xE6, 0xC7, 0x97, 0xDF, 0xA5, 0x0D, 0xEC, 0x17, 0xE3, 0x77, 0x40, 0x2C, 0x20, 0x06, 0x67, 0x27,
  0xE4, 0xEF, 0x16, 0x40, 0x60, 0x16, 0x27, 0xEB, 0xE7, 0x84, 0xE2, 0x67, 0x67, 0x67, 0x40, 0x30,
  0x28, 0x40, 0x60, 0x3C, 0xE4, 0x37, 0xE3, 0x27, 0xE2, 0x67, 0xE3, 0x07, 0x40, 0x34, 0x1C, 0x40,
  0x58, 0x60, 0x40, 0x60, 0x16, 0xEF, 0xD5, 0x81, 0x12, 0xD2, 0xD3, 0x84, 0x98, 0x99, 0x2E, 0xEF,
  0xEF, 0x9A, 0x84, 0xE5, 0x96, 0x8A, 0x86, 0x85, 0x61, 0x86, 0x11, 0x13, 0xD3, 0xE4, 0xC5, 0x65,
  0x65, 0x40, 0x60, 0x8C, 0xE1, 0x67, 0x03, 0x40, 0x8E, 0xD4, 0xE1, 0x11, 0x13, 0xD2, 0x9A, 0xF1,
  0x8D, 0x93, 0x94, 0xE8, 0x40, 0x20, 0x54, 0x88, 0xD3, 0xE2, 0x0C, 0x9B, 0x9C, 0x87, 0x12, 0x84,
  0x8E, 0x93, 0x93, 0xF3, 0xE4, 0x40, 0x1A, 0x50, 0x40, 0x30, 0x9C, 0xE2, 0xF2, 0x8C, 0x09, 0x84,
  0xE4, 0x40, 0x90, 0x9C, 0xF5, 0xC4, 0xCE, 0x01, 0x8C, 0x09, 0x9B, 0xE1, 0x63, 0xE6, 0xEC, 0x86,
  0xE1, 0x80, 0xE2, 0x81, 0xE2, 0xC8, 0x87, 0xE1, 0x82, 0xE1, 0x83, 0xE2, 0x84, 0xE2, 0x85, 0xE6,
  0x40, 0x20, 0xC6, 0xC3, 0x40, 0x30, 0x0A, 0xE1, 0x84, 0xE6, 0x8B, 0xE2, 0x03, 0x40, 0x30, 0xA8,
  0x40, 0x90, 0xB8, 0x84, 0xE6, 0x40, 0x28, 0x22, 0x67, 0x67, 0x67, 0x40, 0x20, 0x18, 0x3C, 0x39,
  0xE4, 0x88, 0x21, 0x80, 0x64, 0xE6, 0x80, 0x22, 0x64, 0xE5, 0x8D, 0x85, 0xE8, 0x33, 0xE0, 0x93,
  0x93, 0x8D, 0xE1, 0x65, 0x8C, 0x32, 0xDD, 0x8E, 0x33, 0x77, 0x8C, 0x05, 0xE7, 0xE1, 0x11, 0x13,
  0xD2, 0xE1, 0xC4, 0x8E, 0xE8, 0x40, 0x20, 0x54, 0x88, 0xD3, 0xE4, 0x93, 0x8C, 0x02, 0xEA, 0x40,
  0x20, 0x54, 0x8D, 0x84, 0xE5, 0x81, 0x25, 0xE9, 0x40, 0x16, 0x50, 0xE7, 0xDB, 0x32, 0x32, 0x05,
  0x91, 0x85, 0xEA, 0x40, 0x20, 0x54, 0x84, 0xE6, 0x40, 0x28, 0x22, 0x67, 0x67, 0x40, 0x28, 0x22,
  0x3C, 0x39, 0xE4, 0x87, 0x81, 0x22, 0xEA, 0x40, 0x1C, 0x50, 0xE5, 0x31, 0x33, 0xDD, 0xE1, 0x31,
  0x83, 0xE8, 0x40, 0x20, 0x54, 0x84, 0xE6, 0x40, 0x28, 0x22, 0x67, 0x67, 0x67, 0x67, 0x40, 0x28,
  0x22, 0x3C, 0xE6, 0x40, 0x20, 0x14, 0x84, 0xE6, 0x40, 0x28, 0x22, 0x67, 0x67, 0x64, 0xE6, 0x40,
  0x38, 0x26, 0x3C, 0xE2, 0x64, 0xE6, 0xEF, 0xE1, 0x11, 0x13, 0xD2, 0xE1, 0xC4, 0x8E, 0xE8, 0x40,
  0x20, 0x54, 0x88, 0xD3, 0xE4, 0x93, 0x8C, 0x02, 0xEA, 0x40, 0x20, 0x54, 0x8D, 0x84, 0xE5, 0x81,
  0x25, 0xE4, 0x84, 0xE3, 0x77, 0x11, 0x88, 0x84, 0xE5, 0x93, 0x85, 0xE7, 0xDB, 0x32, 0x32, 0x05,
  0x91, 0x07, 0x84, 0xE6, 0xEF, 0x85, 0xE6, 0x84, 0xEA, 0xEF, 0x40, 0x28, 0x22, 0x40, 0x48, 0x32,
  0x67, 0xE3, 0x40, 0x90, 0x3C, 0x84, 0xE6, 0x82, 0xEE, 0x40, 0x20, 0x54, 0x3C, 0xE6, 0x9B, 0xEE,
  0x40, 0x20, 0x54, 0xEA, 0xEF, 0xF1, 0x88, 0x15, 0xC3, 0x82, 0x23, 0x85, 0xE6, 0xEF, 0xEE, 0x31,
  0x34, 0x84, 0xE5, 0x87, 0x40, 0x2F, 0x20, 0x12, 0x87, 0x84, 0xE4, 0x8E, 0x08, 0x0E, 0xE4, 0x83,
  0xE8, 0xEF, 0xC4, 0x8E, 0xE1, 0xCD, 0x02, 0x02, 0xE8, 0x40, 0x29, 0x26, 0x85, 0xEC, 0x13, 0x13,
  0xE2, 0x02, 0x66, 0x23, 0x23, 0xEC, 0x81, 0x12, 0x40, 0x1E, 0x90, 0x40, 0x20, 0x54, 0x84, 0x03,
  0x03, 0xEE, 0x40, 0x20, 0x54, 0x40, 0x29, 0x26, 0x40, 0x50, 0x28, 0x67, 0xE3, 0xEF, 0x40, 0x48,
  0x7C, 0x3C, 0xE2, 0x64, 0xE6, 0x84, 0xEA, 0x40, 0x28, 0x22, 0xCB, 0x9B, 0x9B, 0xCC, 0xF4, 0xE0,
  0x40, 0x0A, 0xC6, 0x40, 0x12, 0xCC, 0xEF, 0xEF, 0xCA, 0xC9, 0x96, 0x96, 0x84, 0xE8, 0x40, 0x52,
  0x6C, 0x40, 0xC0, 0x3C, 0x84, 0xEA, 0x40, 0x28, 0x22, 0xCC, 0xF4, 0xE0, 0x93, 0x93, 0xCD, 0xCE,
  0x32, 0x40, 0x0A, 0xC4, 0x40, 0x12, 0x06, 0xEA, 0xEF, 0x40, 0x58, 0xFC, 0xEF, 0x85, 0xE6, 0xE1,
  0x11, 0x13, 0xD2, 0xE1, 0xC4, 0x8E, 0xE8, 0x40, 0x20, 0x54, 0x88, 0xD3, 0xE4, 0x93, 0x8C, 0x02,
  0xEA, 0x40, 0x1C, 0x50, 0x40, 0x30, 0xA8, 0x40, 0x90, 0xB4, 0x84, 0xE6, 0x40, 0x28, 0x22, 0x67,
  0x67, 0x40, 0x2C, 0x62, 0x8D, 0x84, 0xE5, 0x80, 0x23, 0x40, 0x16, 0x50, 0xEF, 0xDB, 0x32, 0xDD,
  0x8E, 0x33, 0x40, 0x16, 0x50, 0xEE, 0xE1, 0x11, 0x13, 0xD2, 0xE1, 0xC4, 0x8E, 0xE8, 0x40, 0x20,
  0x54, 0x88, 0xD3, 0xE4, 0x93, 0x8C, 0x02, 0xE7, 0x13, 0x6A, 0x40, 0x1C, 0x48, 0x40, 0x30, 0x98,
  0x33, 0x33, 0x84, 0x22, 0x40, 0x78, 0xEC, 0xE1, 0x32, 0xDE, 0xA4, 0x85, 0xE6, 0x84, 0xE6, 0x40,
  0x28, 0x22, 0x67, 0x67, 0x40, 0x2C, 0x62, 0x8D, 0x84, 0xE5, 0x80, 0x22, 0x64, 0xE8, 0xC3, 0xC2,
  0xC7, 0xC8, 0x40, 0x0A, 0xC6, 0xE6, 0xDB, 0xF4, 0x40, 0x11, 0x06, 0x66, 0x02, 0x05, 0x40, 0x2E,
  0x0E, 0x85, 0xE6, 0xD5, 0x81, 0x12, 0xD2, 0xD3, 0xE2, 0x6D, 0x87, 0x81, 0x85, 0xE5, 0xF1, 0x88,
  0x15, 0x84, 0x83, 0x23, 0x27, 0xE5, 0x82, 0x84, 0xE5, 0x8C, 0x07, 0x31, 0x39, 0xE4, 0x87, 0x2D,
  0xE2, 0x40, 0x24, 0x50, 0x40, 0x28, 0xDC, 0x40, 0x88, 0xFC, 0x84, 0xE6, 0x40, 0x30, 0x28, 0xE3,
  0x88, 0xEE, 0xEF, 0x40, 0x30, 0x9C, 0xEF, 0x40, 0x90, 0x34, 0x8E, 0xE8, 0xEF, 0x31, 0x83, 0xE1,
  0xC2, 0x21, 0x23, 0xE6, 0xEF, 0xED, 0x32, 0x93, 0x84, 0xE4, 0x83, 0x88, 0x2F, 0x40, 0x30, 0xA8,
  0x40, 0x90, 0xB4, 0x84, 0xE2, 0x83, 0xE2, 0x82, 0xE1, 0x87, 0xE1, 0xC8, 0x81, 0xE2, 0x80, 0xE2,
  0x86, 0xE1, 0x85, 0xE6, 0xEE, 0x40, 0x30, 0x1A, 0x40, 0x0C, 0xC4, 0xE1, 0x40, 0x30, 0xA8, 0x93,
  0xE2, 0x40, 0x90, 0xB4, 0x84, 0xE6, 0x83, 0xE6, 0x82, 0xE6, 0x87, 0xE6, 0x88, 0xE6, 0x85, 0xEE,
  0x8B, 0xE2, 0x8A, 0xE2, 0x89, 0xE2, 0x9E, 0xE2, 0x9F, 0xE2, 0x84, 0xEA, 0x85, 0xE7, 0x77, 0xEE,
  0x96, 0xE2, 0x40, 0x40, 0x44, 0x85, 0xE2, 0x40, 0x60, 0xAC, 0x40, 0xC0, 0xB4, 0xC4, 0xC3, 0xC2,
  0xC7, 0xC8, 0x40, 0x0A, 0xC6, 0xE3, 0x40, 0x1C, 0x54, 0x40, 0x2E, 0x12, 0x83, 0xE2, 0x40, 0x32,
  0x12, 0xE1, 0x40, 0x30, 0xA8, 0x40, 0x90, 0xB4, 0xC4, 0xC3, 0xC2, 0xC7, 0xC8, 0x40, 0x0A, 0xC6,
  0xEF, 0x40, 0x20, 0xD8, 0x40, 0x12, 0x0A, 0xED, 0x40, 0x30, 0xA0, 0xEB, 0x40, 0x90, 0xB4, 0x84,
  0xE2, 0x64, 0xED, 0x13, 0x13, 0xE8, 0x40, 0x30, 0x10, 0xE2, 0x13, 0x13, 0xE2, 0x03, 0x01, 0x40,
  0x30, 0x10, 0x40, 0x50, 0xFC, 0x40, 0xB0, 0x18, 0x84, 0xE6, 0x40, 0x28, 0x22, 0x65, 0x65, 0xEF,
  0x40, 0x20, 0x54, 0xC4, 0xC3, 0xC2, 0xC7, 0xC8, 0x40, 0x0A, 0xC6, 0xED, 0xEF, 0x40, 0x30, 0x0E,
  0x40, 0x40, 0x08, 0x40, 0x40, 0x38, 0x85, 0xE6, 0x40, 0x40, 0x24, 0x85, 0xE6, 0xC4, 0x62, 0xEA,
  0x40, 0x24, 0x1C, 0x40, 0x58, 0x2A, 0xE3, 0x13, 0x13, 0x03, 0x03, 0xEF, 0x40, 0x41, 0x7C, 0xEF,
  0xEF, 0x84, 0xE6, 0x40, 0x30, 0x28, 0xE3, 0x40, 0x60, 0x34, 0x84, 0x23, 0x23, 0xEA, 0xEF, 0xED,
  0xCB, 0x9B, 0x9B, 0xCC, 0xF4, 0xF7, 0xA5, 0x85, 0xE6, 0xEF, 0xEC, 0xEF, 0x88, 0x82, 0xE2, 0xA5,
  0x0D, 0x81, 0x87, 0x11, 0xD3, 0x84, 0xCE, 0x77, 0xE6, 0xEF, 0x84, 0xE3, 0x81, 0x25, 0x93, 0x37,
  0xA6, 0x86, 0x21, 0x77, 0xE6, 0xEF, 0xDB, 0x33, 0x8E, 0x84, 0xEF, 0x85, 0xE6, 0x84, 0xEA, 0xEF,
  0x40, 0x28, 0x22, 0x8F, 0x84, 0xE5, 0xD9, 0x85, 0xE2, 0x40, 0x18, 0x50, 0xEE, 0xDB, 0x32, 0xDD,
  0x8E, 0x33, 0x77, 0x8C, 0x06, 0xE6, 0x85, 0xEF, 0x86, 0x81, 0x12, 0xD2, 0xD3, 0xE2, 0x40, 0x16,
  0x50, 0xEE, 0x98, 0x84, 0xE5, 0xA7, 0x8B, 0x02, 0x40, 0x26, 0x60, 0x35, 0x32, 0x8E, 0x84, 0x8D,
  0x0B, 0x77, 0xF3, 0x06, 0xE6, 0x85, 0xEF, 0x86, 0x81, 0x12, 0xD2, 0xD3, 0xE2, 0x40, 0x16, 0x50,
  0xEE, 0x8F, 0x84, 0xE5, 0xD9, 0x85, 0xE2, 0x40, 0x10, 0x48, 0xE5, 0x40, 0x77, 0x26, 0x85, 0xE6,
  0x85, 0xEF, 0x86, 0x81, 0x12, 0xD2, 0xD3, 0xE2, 0x40, 0x16, 0x50, 0xEE, 0x8F, 0x84, 0xE4, 0x89,
  0xC5, 0x5B, 0x40, 0x34, 0xEC, 0xC5, 0x8D, 0xE1, 0x02, 0x06, 0xE6, 0xE1, 0x80, 0x11, 0x88, 0xC7,
  0x82, 0xE6, 0x84, 0xE2, 0x64, 0xEE, 0x85, 0xE2, 0x64, 0x84, 0xE5, 0x0C, 0x01, 0xE4, 0x40, 0x30,
  0x5E, 0x85, 0xEF, 0x86, 0x81, 0x12, 0xD2, 0xD3, 0xE1, 0x77, 0x27, 0x40, 0x0B, 0x00, 0x21, 0x25,
  0xEF, 0x8F, 0x84, 0xE5, 0xD9, 0x85, 0xE1, 0x7F, 0x8F, 0xC5, 0x86, 0x9E, 0x84, 0xE4, 0x85, 0xE7,
  0x77, 0xE6, 0xEF, 0x40, 0x60, 0x84, 0x84, 0xEA, 0xEF, 0x40, 0x28, 0x22, 0x8F, 0x84, 0xE5, 0xD9,
  0x85, 0xE6, 0xEF, 0xEE, 0xDB, 0x32, 0xDD, 0x8E, 0x84, 0xED, 0x85, 0xE6, 0x82, 0xE2, 0x64, 0xE6,
  0x84, 0xE6, 0x82, 0xEE, 0x40, 0x18, 0x0A, 0x67, 0x67, 0xE3, 0xEF, 0x07, 0xE3, 0x81, 0xE2, 0x64,
  0xE6, 0x87, 0xE6, 0x81, 0xEC, 0x11, 0x84, 0xE4, 0x8D, 0x40, 0x22, 0xC8, 0x85, 0x67, 0xE3, 0xEE,
  0xF3, 0xE0, 0xCC, 0x02, 0xE1, 0x84, 0xEA, 0xEF, 0x40, 0x28, 0x22, 0x80, 0x11, 0x13, 0xE1, 0x02,
  0x93, 0x40, 0x26, 0x60, 0x03, 0x03, 0xE6, 0x40, 0x18, 0x4C, 0x84, 0xE6, 0x82, 0xEE, 0xEF, 0x40,
  0x28, 0x1E, 0xEF, 0x07, 0xE3, 0xEF, 0x84, 0xEE, 0x40, 0x28, 0x5C, 0x8F, 0x84, 0xE5, 0xA0, 0x88,
  0xED, 0x85, 0xE6, 0xEF, 0x15, 0xA0, 0x40, 0x30, 0x9C, 0xEC, 0x35, 0x32, 0xE1, 0x84, 0xEF, 0x85,
  0xE6, 0xEF, 0x84, 0xEE, 0x40, 0x28, 0x5C, 0x8F, 0x84, 0xE5, 0xD9, 0x85, 0xE6, 0xEF, 0xEE, 0xDB,
  0x32, 0xDD, 0x8E, 0x84, 0xED, 0x85, 0xE6, 0x85, 0xEF, 0x86, 0x81, 0x12, 0xD2, 0xD3, 0xE2, 0x40,
  0x16, 0x50, 0xEE, 0x8F, 0x84, 0xE5, 0xD9, 0x85, 0xE2, 0x40, 0x40, 0xF8, 0xE5, 0xEF, 0x84, 0xEE,
  0xEF, 0x85, 0xEE, 0x8F, 0x84, 0xE5, 0xD9, 0x85, 0xE2, 0x40, 0x18, 0x50, 0xEE, 0xDB, 0x32, 0xDD,
  0x8E, 0x33, 0x77, 0x8C, 0x06, 0xE6, 0x85, 0xEF, 0x86, 0x81, 0x12, 0xD2, 0xD3, 0xE2, 0x40, 0x16,
  0x50, 0xEE, 0x8F, 0x84, 0xE5, 0xD9, 0x85, 0xE2, 0x40, 0x18, 0x50, 0xED, 0x84, 0xEE, 0xEF, 0xEF,
  0x84, 0xEE, 0x40, 0x28, 0x5C, 0x87, 0xD3, 0xE4, 0x9B, 0x01, 0xE6, 0xED, 0xEF, 0x15, 0x11, 0xD2,
  0x83, 0x67, 0x91, 0xF5, 0x92, 0x83, 0xE1, 0x82, 0x88, 0x29, 0xE6, 0xEF, 0x84, 0xE3, 0x0C, 0x9B,
  0x8B, 0x9B, 0x8E, 0x33, 0x82, 0x86, 0xD5, 0x81, 0x40, 0x1E, 0x4C, 0xEC, 0x9B, 0x93, 0x36, 0x83,
  0x88, 0x80, 0x21, 0x8C, 0x93, 0x31, 0x8E, 0x32, 0x76, 0xE6, 0xE7, 0x82, 0xE6, 0x84, 0xE2, 0x64,
  0xE6, 0xC7, 0xC8, 0x21, 0x26, 0xE6, 0x40, 0x2C, 0x52, 0x67, 0xE1, 0x31, 0x84, 0xE5, 0x82, 0x85,
  0xE6, 0xEF, 0x84, 0xED, 0xC3, 0xC2, 0x22, 0x25, 0xE5, 0xEF, 0xEF, 0x8A, 0x89, 0x84, 0xE5, 0x8F,
  0x85, 0xE6, 0xEF, 0x40, 0x78, 0x1E, 0xEF, 0x84, 0xE1, 0x83, 0xE1, 0xC2, 0x87, 0xE1, 0x88, 0xE1,
  0xC1, 0x80, 0x40, 0x11, 0xC6, 0xEC, 0xEC, 0x8A, 0xE1, 0xC9, 0x96, 0xE1, 0x84, 0xEB, 0x40, 0x60,
  0xB4, 0xEF, 0x84, 0xE6, 0x83, 0xE6, 0x82, 0xE6, 0x85, 0xEA, 0xEF, 0x88, 0xE2, 0xA0, 0xE2, 0xF5,
  0xE2, 0x40, 0x34, 0x84, 0x40, 0x30, 0xA8, 0x82, 0xE2, 0x40, 0x90, 0xB4, 0xEF, 0xC4, 0xC3, 0xC2,
  0xC7, 0xC8, 0x81, 0xE2, 0x40, 0x28, 0x60, 0xCA, 0xC9, 0x96, 0x96, 0x84, 0xE6, 0x40, 0x48, 0xFC,
  0xEF, 0x84, 0xE1, 0x83, 0xE1, 0xC2, 0x87, 0xE1, 0x88, 0xE1, 0xC1, 0x80, 0xE1, 0x86, 0xE1, 0x11,
  0x84, 0xE5, 0x8D, 0x85, 0xE2, 0xEE, 0x8A, 0xE1, 0xC9, 0x96, 0xE1, 0x84, 0xEA, 0x40, 0x43, 0x80,
  0x02, 0x06, 0x40, 0x60, 0xA0, 0x85, 0xE9, 0xEF, 0x84, 0xE2, 0x66, 0x13, 0x13, 0xE4, 0x40, 0x30,
  0x1C, 0xD2, 0x52, 0x40, 0x3E, 0xF8, 0xE6, 0xE1, 0x12, 0x81, 0x88, 0xE8, 0x87, 0x84, 0xE2, 0x40,
  0x16, 0x50, 0xE6, 0x82, 0x84, 0xE1, 0x8D, 0x01, 0xE8, 0xCC, 0x01, 0x63, 0x40, 0x20, 0x54, 0x84,
  0xEA, 0x40, 0x28, 0x22, 0x8D, 0x36, 0x82, 0x21, 0xE8, 0xC1, 0x21, 0x61, 0x40, 0x20, 0x58, 0x32,
  0x40, 0x30, 0x0A, 0x3B, 0x40, 0x16, 0x50, 0xE6, 0xEC, 0x88, 0x82, 0x11, 0xE3, 0x0C, 0x9B, 0x01,
  0xE6, 0xEF, 0xED, 0x35, 0x31, 0x37, 0x25, 0x81, 0x40, 0x42, 0xF4, 0xEE, 0xFF, 0xFF, 0xFF,
};

extern const mamefont::Font MameSansP_s48c40w08(MameSansP_s48c40w08_blob);

#undef MAMEFONT_PROGMEM
