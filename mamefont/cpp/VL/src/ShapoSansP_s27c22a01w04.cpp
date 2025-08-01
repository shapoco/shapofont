// Generated by MameFont
//   Format Version: 1
//   First Code      : 32
//   Glyph Count     : 95
//   Font Height     : 27 px
//   Max Glyph Width : 23 px
//   Total Pixels    : 33291 px
//   Fragment Shape  : Vertical
//   Bit Order       : LSB First
//   Shrinked Format : No
//   Estimated Footprint:
//     Header        :    8 Bytes
//     Glyph Table   :  380 Bytes (4 Bytes/glyph)
//     Lookup Table  :   58 Bytes (90.62% used)
//     Bytecodes     : 1531 Bytes (16.12 Bytes/glyph)
//     Total         : 1977 Bytes (20.81 Bytes/glyph)
//   Compression Performance:
//     CPX         :  720 -->  117 ( -12.23%)
//     CPY         :  643 -->  125 ( -10.50%)
//     LUD (step=0):  198 -->   99 (  -2.01%)
//     LUD (step=1):  148 -->   74 (  -1.50%)
//     LUP         :  615 -->  615 (  +0.00%)
//     RPT         : 2243 -->  347 ( -38.44%)
//     SFT         :  348 -->  134 (  -4.34%)
//     XOR         :   17 -->   17 (  +0.00%)
//     Total       : 4932 --> 1528 ( -69.02%)
//   Memory Efficiency: 16.839 px/Byte

#include <stdint.h>
#include <mamefont/mamefont.hpp>

#ifdef MAMEFONT_USE_PROGMEM
#include <avr/pgmspace.h>
#define MAMEFONT_PROGMEM PROGMEM
#else
#define MAMEFONT_PROGMEM
#endif

const uint8_t ShapoSansP_s27c22a01w04_blob[] MAMEFONT_PROGMEM = {
  // Font Header
  0x01, 0x80, 0x20, 0x5E, 0x39, 0x1A, 0x05, 0x16,
  // Glyph Table
  0x00, 0x00, 0x03, 0x12, 0x01, 0x00, 0x03, 0x12, 0x09, 0x00, 0x08, 0x12, 0x11, 0x00, 0x0E, 0x12,
  0x24, 0x00, 0x0F, 0x12, 0x37, 0x00, 0x16, 0x12, 0x4F, 0x00, 0x10, 0x12, 0x6F, 0x00, 0x03, 0x12,
  0x75, 0x00, 0x08, 0x12, 0x83, 0x00, 0x08, 0x12, 0x90, 0x00, 0x0F, 0x12, 0xA3, 0x00, 0x0D, 0x12,
  0xAE, 0x00, 0x03, 0x12, 0xB5, 0x00, 0x0B, 0x12, 0xBB, 0x00, 0x03, 0x12, 0xBE, 0x00, 0x0E, 0x12,
  0xCC, 0x00, 0x0D, 0x12, 0xD9, 0x00, 0x0D, 0x12, 0xE8, 0x00, 0x0D, 0x12, 0xFF, 0x00, 0x0D, 0x12,
  0x1C, 0x01, 0x0D, 0x12, 0x31, 0x01, 0x0D, 0x12, 0x47, 0x01, 0x0D, 0x12, 0x5E, 0x01, 0x0D, 0x12,
  0x71, 0x01, 0x0D, 0x12, 0x80, 0x01, 0x0D, 0x12, 0x97, 0x01, 0x03, 0x12, 0x9F, 0x01, 0x03, 0x12,
  0xA6, 0x01, 0x09, 0x12, 0xB7, 0x01, 0x0B, 0x12, 0xBF, 0x01, 0x09, 0x12, 0xCE, 0x01, 0x0E, 0x12,
  0xE1, 0x01, 0x11, 0x12, 0xFB, 0x01, 0x10, 0x12, 0x0E, 0x02, 0x0E, 0x12, 0x27, 0x02, 0x10, 0x12,
  0x37, 0x02, 0x0F, 0x12, 0x49, 0x02, 0x0C, 0x12, 0x58, 0x02, 0x0C, 0x12, 0x66, 0x02, 0x10, 0x12,
  0x80, 0x02, 0x0F, 0x12, 0x89, 0x02, 0x05, 0x12, 0x92, 0x02, 0x10, 0x12, 0xA3, 0x02, 0x0E, 0x12,
  0xB6, 0x02, 0x0D, 0x12, 0xC2, 0x02, 0x13, 0x12, 0xD8, 0x02, 0x0F, 0x12, 0xE6, 0x02, 0x10, 0x12,
  0xF3, 0x02, 0x0F, 0x12, 0x02, 0x03, 0x10, 0x12, 0x19, 0x03, 0x0F, 0x12, 0x35, 0x03, 0x0F, 0x12,
  0x51, 0x03, 0x11, 0x12, 0x5F, 0x03, 0x10, 0x12, 0x6F, 0x03, 0x10, 0x12, 0x83, 0x03, 0x12, 0x12,
  0x9A, 0x03, 0x11, 0x12, 0xAB, 0x03, 0x11, 0x12, 0xBC, 0x03, 0x0E, 0x12, 0xCB, 0x03, 0x05, 0x12,
  0xD3, 0x03, 0x0E, 0x12, 0xE1, 0x03, 0x05, 0x12, 0xEA, 0x03, 0x0B, 0x12, 0xF4, 0x03, 0x0B, 0x12,
  0xFA, 0x03, 0x06, 0x12, 0x00, 0x04, 0x0D, 0x12, 0x12, 0x04, 0x0D, 0x12, 0x28, 0x04, 0x0D, 0x12,
  0x3C, 0x04, 0x0D, 0x12, 0x4F, 0x04, 0x0D, 0x12, 0x63, 0x04, 0x09, 0x12, 0x73, 0x04, 0x0D, 0x12,
  0x8C, 0x04, 0x0D, 0x12, 0x9C, 0x04, 0x04, 0x12, 0xA6, 0x04, 0x06, 0x12, 0xB4, 0x04, 0x0C, 0x12,
  0xC4, 0x04, 0x04, 0x12, 0xCE, 0x04, 0x11, 0x12, 0xE2, 0x04, 0x0C, 0x12, 0xF1, 0x04, 0x0D, 0x12,
  0xFF, 0x04, 0x0D, 0x12, 0x14, 0x05, 0x0D, 0x12, 0x27, 0x05, 0x08, 0x12, 0x31, 0x05, 0x0D, 0x12,
  0x4D, 0x05, 0x09, 0x12, 0x5D, 0x05, 0x0D, 0x12, 0x6B, 0x05, 0x0F, 0x12, 0x78, 0x05, 0x11, 0x12,
  0x8A, 0x05, 0x0E, 0x12, 0x98, 0x05, 0x0F, 0x12, 0xAE, 0x05, 0x0D, 0x12, 0xC2, 0x05, 0x07, 0x12,
  0xD3, 0x05, 0x03, 0x12, 0xD7, 0x05, 0x07, 0x12, 0xE7, 0x05, 0x0D, 0x12,
  // Lookup Table
  0xFC, 0x3E, 0x1E, 0xFF, 0xFE, 0xF8, 0xE0, 0x7C, 0x78, 0x3C, 0x07, 0x1F, 0x0F, 0x3F, 0x7F, 0x00,
  0xC0, 0x03, 0x01, 0x38, 0x7E, 0xC3, 0x81, 0xE7, 0xCF, 0x87, 0x8F, 0x0E, 0x06, 0x80, 0x70, 0x60,
  0x04, 0x1C, 0x08, 0x30, 0x0C, 0x9F, 0xEF, 0x79, 0x31, 0xC1, 0xF7, 0xE3, 0xCE, 0xC7, 0x83, 0xDF,
  0x40, 0xE6, 0xF9, 0xF1, 0xF3, 0x02, 0xE1, 0x33, 0xBE, 0x20,
  // Bytecodes
  0xEF, 0x84, 0xE2, 0x8E, 0xE2, 0x88, 0xE2, 0x8F, 0xE2, 0x8C, 0xF6, 0x8E, 0x8D, 0x59, 0x4B, 0xEA,
  0xEE, 0x86, 0xE1, 0x35, 0xE1, 0xB1, 0x5A, 0x53, 0x96, 0x96, 0xB2, 0x3A, 0x99, 0x96, 0xB3, 0x5A,
  0x9A, 0x40, 0x2B, 0xDC, 0x35, 0xE0, 0x85, 0xC8, 0xC4, 0x64, 0x85, 0xF3, 0xA3, 0x40, 0x10, 0x80,
  0xC2, 0x83, 0xE2, 0x40, 0x1C, 0xD4, 0xED, 0x86, 0x85, 0xC0, 0xD1, 0x65, 0x86, 0x35, 0x84, 0x94,
  0x82, 0x9C, 0x2B, 0x92, 0x8A, 0xCC, 0x8B, 0xC2, 0xA5, 0xA6, 0x83, 0xE2, 0x40, 0x3B, 0xF4, 0x8F,
  0x3C, 0xC0, 0x84, 0xB8, 0x82, 0x66, 0xE2, 0x9D, 0x86, 0xB4, 0x3D, 0x8E, 0x61, 0xE1, 0xAA, 0xAB,
  0x86, 0x32, 0x9E, 0x40, 0x21, 0x80, 0xD7, 0x61, 0xCD, 0x21, 0x62, 0x94, 0xA1, 0x8F, 0xEF, 0x8C,
  0xF6, 0x8E, 0x8D, 0x8F, 0xEA, 0x9D, 0x38, 0x80, 0x31, 0x8B, 0x8A, 0x21, 0x83, 0xE2, 0x40, 0x12,
  0x88, 0x02, 0xE7, 0x12, 0x8B, 0x83, 0x01, 0x04, 0x09, 0xE3, 0x83, 0xE2, 0x40, 0x12, 0x88, 0xE5,
  0x9D, 0x86, 0x90, 0x90, 0x9D, 0x9D, 0xC5, 0x67, 0x96, 0x95, 0x95, 0x97, 0x97, 0x83, 0xE2, 0x40,
  0x1A, 0xD4, 0xEE, 0xE4, 0xC6, 0x66, 0x89, 0xE3, 0x83, 0xE2, 0x40, 0x18, 0xD0, 0xEC, 0xE7, 0xC8,
  0xC5, 0x8F, 0xB5, 0x91, 0x92, 0xEB, 0x88, 0xE4, 0x66, 0xE6, 0xEF, 0xE7, 0xC8, 0x65, 0xE6, 0x9D,
  0x36, 0x84, 0x94, 0x82, 0x9C, 0x2A, 0x9D, 0x37, 0x40, 0x19, 0xD4, 0xEC, 0x86, 0x85, 0xC0, 0xD1,
  0x82, 0x66, 0x83, 0xE2, 0x8F, 0xE4, 0x40, 0x26, 0xDC, 0xE1, 0xC6, 0x31, 0x84, 0xE2, 0x8F, 0xE4,
  0x92, 0x62, 0xC3, 0x62, 0xE8, 0xCE, 0x65, 0xED, 0x9F, 0x88, 0xC0, 0xD1, 0x82, 0x64, 0xD5, 0x0A,
  0x31, 0x33, 0x8E, 0x22, 0x91, 0x88, 0x94, 0x8E, 0xE2, 0xF2, 0xA7, 0x88, 0xE4, 0x8F, 0xEC, 0x8F,
  0x82, 0xE2, 0xF7, 0xF6, 0x84, 0xE1, 0x94, 0xD1, 0x8F, 0xE1, 0xA1, 0x82, 0x8B, 0xE3, 0x81, 0xC0,
  0xD5, 0xA0, 0xA1, 0xC1, 0xD7, 0x88, 0x62, 0x40, 0x0E, 0x80, 0x8F, 0xEC, 0xE1, 0x86, 0x84, 0xE1,
  0x81, 0xB5, 0x8F, 0xE4, 0x86, 0x3F, 0x95, 0x90, 0x51, 0x62, 0xE1, 0x91, 0xE5, 0xCE, 0x64, 0x8F,
  0xEC, 0x9D, 0x84, 0xE2, 0x82, 0xE6, 0x8F, 0x8B, 0xE2, 0x82, 0xE3, 0x81, 0xC0, 0xD5, 0xA0, 0xA1,
  0xC1, 0xD7, 0x40, 0x0E, 0x84, 0x8F, 0xEC, 0xE1, 0x90, 0x85, 0xC4, 0x81, 0x9C, 0x8F, 0xE4, 0x3C,
  0x3A, 0xDB, 0x8C, 0x62, 0xC4, 0x80, 0x04, 0xDA, 0xCD, 0xD7, 0x88, 0x66, 0x8F, 0xEC, 0x84, 0xE2,
  0x82, 0xE3, 0xF7, 0x84, 0xE2, 0x8F, 0xE5, 0x3B, 0x8D, 0x2A, 0xE2, 0xB0, 0x88, 0x8E, 0xE1, 0x2A,
  0xEF, 0x86, 0x85, 0xC0, 0xD1, 0x82, 0x66, 0xA9, 0xAA, 0x3D, 0x8E, 0xC1, 0x66, 0x40, 0x2A, 0xD8,
  0x86, 0x85, 0xC0, 0xD1, 0x82, 0x66, 0xDC, 0xCE, 0x85, 0xF3, 0xE0, 0x62, 0x39, 0x8E, 0x8C, 0x8F,
  0xE4, 0x9F, 0x87, 0xCE, 0x8B, 0x29, 0xEE, 0x9D, 0xE2, 0x8A, 0xE2, 0x88, 0xE2, 0x8F, 0xE2, 0xE7,
  0xC8, 0xC5, 0x8F, 0xB5, 0x91, 0x92, 0xE4, 0x33, 0x90, 0xA3, 0x88, 0x80, 0x31, 0x98, 0x99, 0x91,
  0x22, 0x62, 0x13, 0x81, 0xA4, 0x8F, 0xE8, 0x9D, 0xEA, 0x99, 0xEA, 0x8A, 0xEA, 0x8F, 0xEA, 0x35,
  0x03, 0xE4, 0x11, 0x99, 0x98, 0x83, 0x01, 0x88, 0xA3, 0xA4, 0x81, 0x21, 0x23, 0xEB, 0x86, 0x85,
  0xC0, 0xD1, 0xE1, 0x6E, 0x92, 0xE2, 0x21, 0x86, 0x85, 0x31, 0x8D, 0x22, 0x25, 0xE4, 0xC8, 0x65,
  0xEF, 0x35, 0x31, 0x89, 0xD1, 0xF7, 0xE1, 0x77, 0x83, 0xE1, 0xCF, 0x94, 0x59, 0x95, 0x62, 0x84,
  0x90, 0x90, 0x59, 0x8E, 0x40, 0x24, 0x88, 0x53, 0x8F, 0xE2, 0xEF, 0xE3, 0x3C, 0x84, 0xE1, 0x82,
  0x6C, 0xE4, 0x3F, 0xA5, 0x96, 0x9D, 0x6F, 0x9E, 0x8E, 0xE1, 0x25, 0xE3, 0x7F, 0xEF, 0x84, 0xE2,
  0x82, 0xE3, 0x81, 0xC0, 0xD5, 0x8F, 0x83, 0xE2, 0x82, 0xE3, 0x8B, 0x8D, 0x83, 0xAA, 0xB6, 0x9D,
  0x40, 0x1E, 0x84, 0x40, 0x1F, 0x84, 0xED, 0x35, 0x31, 0xD0, 0xD1, 0x82, 0x6B, 0xD7, 0xA3, 0x8F,
  0xC3, 0x62, 0x40, 0x22, 0x98, 0x2D, 0xEF, 0x84, 0xE2, 0x82, 0xE3, 0xC1, 0xC0, 0x01, 0x90, 0x83,
  0xE2, 0x8F, 0xE2, 0x67, 0x40, 0x20, 0x8C, 0x8F, 0xEE, 0x84, 0xE2, 0x82, 0xE7, 0x83, 0xE2, 0x89,
  0xE6, 0x8F, 0x8E, 0xE2, 0x9E, 0xE7, 0x8F, 0xEB, 0x84, 0xE2, 0x82, 0xE7, 0x83, 0xE2, 0x89, 0xE5,
  0x40, 0x1A, 0x80, 0x62, 0xE6, 0xED, 0x35, 0x31, 0xD0, 0xD1, 0x82, 0x64, 0xD7, 0xA3, 0x83, 0xE2,
  0x8F, 0xE3, 0x89, 0xE2, 0x80, 0xE2, 0x40, 0x22, 0x84, 0xE2, 0x89, 0xA1, 0x8E, 0xE2, 0x8F, 0xEF,
  0xC4, 0x65, 0x67, 0x33, 0x89, 0xE6, 0x40, 0x2C, 0xE0, 0x82, 0xC4, 0x63, 0x83, 0xE2, 0x40, 0x0C,
  0x84, 0xE4, 0xEC, 0xC4, 0x62, 0xEB, 0xC3, 0x62, 0xA4, 0x82, 0x81, 0x8D, 0xC7, 0xC8, 0x6B, 0x8D,
  0x21, 0x25, 0xEF, 0xC4, 0x62, 0x9D, 0x33, 0x21, 0x82, 0x9B, 0x9C, 0x83, 0xE4, 0x97, 0x95, 0x96,
  0x40, 0x1E, 0x90, 0x9F, 0x8F, 0xED, 0xC4, 0x62, 0xE8, 0xC3, 0x62, 0xE8, 0x8E, 0xE2, 0x88, 0xE8,
  0x8F, 0xEC, 0x84, 0xE5, 0x0A, 0x63, 0xE5, 0x33, 0x8F, 0x19, 0x59, 0x80, 0x66, 0xE2, 0x8E, 0xE2,
  0x8F, 0xE1, 0x92, 0xCC, 0x67, 0x62, 0xE2, 0xEF, 0x84, 0xE3, 0x07, 0xE2, 0x84, 0xE2, 0x33, 0x92,
  0x16, 0x84, 0x40, 0x1A, 0xD4, 0xEE, 0x35, 0x31, 0xD0, 0xD1, 0x82, 0x6F, 0x83, 0xE2, 0x8F, 0xE5,
  0x40, 0x2D, 0xE4, 0x84, 0xE2, 0x82, 0xE5, 0x81, 0xC0, 0xD5, 0x83, 0xE2, 0x40, 0x10, 0x88, 0x40,
  0x3C, 0xDC, 0x35, 0x31, 0xD0, 0xD1, 0x82, 0x6F, 0x83, 0xE2, 0x8F, 0xE1, 0x32, 0x6A, 0x40, 0x15,
  0xC8, 0xA7, 0xF1, 0xCE, 0x8D, 0x62, 0xB7, 0x8F, 0xEF, 0x84, 0xE2, 0x82, 0xE5, 0x81, 0xC0, 0xD5,
  0x83, 0xE2, 0x88, 0xE2, 0x85, 0xE1, 0x80, 0x40, 0x10, 0x80, 0x40, 0x24, 0xC4, 0x92, 0x16, 0x8E,
  0x87, 0x9E, 0xB0, 0x8F, 0xEE, 0x86, 0x85, 0xC0, 0xB8, 0x82, 0xE4, 0x81, 0xC7, 0x93, 0xB9, 0x92,
  0x12, 0x8C, 0x8B, 0x82, 0x81, 0x89, 0xD7, 0x40, 0x09, 0x02, 0x40, 0x1A, 0xC8, 0x87, 0x40, 0x3C,
  0xD0, 0x82, 0xE5, 0x84, 0xE1, 0x77, 0x8F, 0xE5, 0xC3, 0x62, 0xEC, 0xCE, 0x62, 0xEA, 0xEC, 0xC4,
  0x66, 0x6F, 0x33, 0x8F, 0xE3, 0x6F, 0x91, 0x8C, 0x11, 0x8D, 0xC7, 0xC8, 0x6E, 0x25, 0xEF, 0x9B,
  0x84, 0xE1, 0x85, 0x0F, 0x6F, 0x2D, 0x1D, 0xE1, 0x85, 0x0D, 0x6E, 0xE1, 0x63, 0x8E, 0xE1, 0x88,
  0x6C, 0xE3, 0xEF, 0x94, 0x84, 0xE1, 0x9D, 0x02, 0x9D, 0xE1, 0x7F, 0x8F, 0x83, 0xE2, 0x86, 0x36,
  0x8E, 0x83, 0x7F, 0xE1, 0x8E, 0xE2, 0x27, 0x6F, 0xE6, 0xEC, 0x9C, 0x82, 0x94, 0xC4, 0x07, 0x8F,
  0x77, 0x2A, 0x96, 0x97, 0x83, 0xE1, 0x94, 0x94, 0x40, 0x2E, 0xE8, 0x9C, 0x82, 0x94, 0xC4, 0x07,
  0x8F, 0x77, 0x2A, 0x92, 0x16, 0xD3, 0x66, 0xE8, 0xCE, 0x62, 0xEA, 0xEC, 0x82, 0xE5, 0xF7, 0x84,
  0xE2, 0x94, 0x82, 0x9C, 0x2A, 0x9D, 0x37, 0x40, 0x19, 0xD4, 0xEC, 0x83, 0xE2, 0x8A, 0x66, 0x53,
  0xC6, 0x8F, 0xE4, 0xE6, 0x9D, 0x36, 0x84, 0x94, 0x82, 0x9C, 0x2A, 0x9D, 0x37, 0x40, 0x19, 0xD4,
  0xEC, 0x91, 0x91, 0x83, 0xE2, 0x8F, 0x64, 0x86, 0x65, 0xE4, 0x86, 0x31, 0x22, 0x65, 0x91, 0x21,
  0xE2, 0x65, 0x57, 0xEF, 0xE7, 0xEF, 0x3C, 0xE4, 0x66, 0xEA, 0x8A, 0x12, 0x87, 0x06, 0xE6, 0xEC,
  0xEE, 0xAC, 0xAD, 0x97, 0xE4, 0x98, 0xD3, 0xD4, 0xDC, 0xDD, 0xA7, 0x9E, 0x9E, 0x62, 0xDD, 0xE1,
  0x8F, 0xEC, 0xC4, 0x62, 0xE8, 0x83, 0xE2, 0x82, 0x8C, 0xE2, 0x8B, 0xD3, 0xD4, 0x8E, 0xE2, 0x89,
  0x88, 0xE2, 0x87, 0x8E, 0xCD, 0x8C, 0x8F, 0xEC, 0xED, 0x3C, 0x80, 0xC4, 0xDB, 0xE3, 0x82, 0x81,
  0xA1, 0xA2, 0xDA, 0xCD, 0xD7, 0xE3, 0x89, 0x81, 0xA1, 0xA2, 0x8F, 0xEC, 0xE9, 0x84, 0xE2, 0x85,
  0x49, 0x83, 0xDB, 0xE2, 0xD2, 0xE2, 0xDC, 0xDD, 0xD7, 0xE2, 0x89, 0x8E, 0xE2, 0x8F, 0xEC, 0xED,
  0x3C, 0x80, 0xC4, 0x98, 0xAD, 0xAD, 0x66, 0xDA, 0xCD, 0xA7, 0xF3, 0xE0, 0x62, 0xA7, 0xA8, 0xA8,
  0x92, 0x8F, 0xEC, 0xE1, 0x3C, 0xC0, 0x84, 0x82, 0xE1, 0x89, 0xCC, 0x83, 0xE1, 0x71, 0xE2, 0x2D,
  0xCE, 0x62, 0xEC, 0xED, 0x85, 0xC4, 0x83, 0xDB, 0xE2, 0xD2, 0xE2, 0x91, 0x98, 0x9A, 0xA5, 0xA5,
  0xF0, 0xE2, 0x98, 0x83, 0xE2, 0x8F, 0x91, 0x8A, 0xE3, 0x6C, 0x91, 0x8F, 0xC4, 0x62, 0xE8, 0x83,
  0xE2, 0x82, 0x8C, 0xE2, 0x8B, 0xD3, 0xD4, 0x8E, 0xE2, 0x40, 0x2E, 0xD4, 0x8F, 0x82, 0xE2, 0x8A,
  0x83, 0xE2, 0x8F, 0xCE, 0x62, 0xE3, 0xE2, 0xC2, 0x63, 0x8A, 0x83, 0xE2, 0x9D, 0x9D, 0x90, 0x7C,
  0xE2, 0x91, 0x91, 0x8F, 0xC4, 0x62, 0xE7, 0x83, 0xE2, 0x86, 0x31, 0x21, 0x23, 0xCE, 0x67, 0x88,
  0x9E, 0x9F, 0x8F, 0xEB, 0x9B, 0x84, 0xE2, 0x8F, 0xC3, 0x62, 0x8E, 0xE1, 0x71, 0xE3, 0xE1, 0xEF,
  0x83, 0xE2, 0x9B, 0x8A, 0x8C, 0xC4, 0x85, 0x72, 0x8C, 0xD3, 0xD4, 0x8E, 0xE2, 0x8F, 0xE1, 0x4D,
  0x46, 0xEF, 0xEC, 0x83, 0xE2, 0x9B, 0x8A, 0xE1, 0x8C, 0xD3, 0xD4, 0x8E, 0xE2, 0x8F, 0xE3, 0x5D,
  0xEA, 0xED, 0x3C, 0x80, 0xC4, 0xDB, 0x8C, 0x66, 0xDA, 0xCD, 0xD7, 0x88, 0x66, 0x8F, 0xEC, 0xED,
  0x83, 0xE2, 0x82, 0x8C, 0xE2, 0x8B, 0xD3, 0xD4, 0x3B, 0x89, 0x88, 0xE2, 0x87, 0x8E, 0xCD, 0x8C,
  0x8A, 0xE2, 0x2A, 0xE6, 0xED, 0x85, 0xC4, 0x83, 0xDB, 0xE2, 0xD2, 0xE2, 0xDC, 0xDD, 0xD7, 0xE2,
  0x89, 0x83, 0xE2, 0x8F, 0xE8, 0x8A, 0xE2, 0xE8, 0x83, 0xE2, 0x82, 0x8C, 0xE2, 0x8E, 0xE2, 0x8F,
  0xEC, 0xED, 0x93, 0x94, 0x84, 0x83, 0xA6, 0x97, 0xAD, 0xE1, 0x99, 0x99, 0x9A, 0x9B, 0x82, 0x89,
  0x93, 0x88, 0x9E, 0x9E, 0xF0, 0xE1, 0xF1, 0xF3, 0x8E, 0xCD, 0x9B, 0x8F, 0xEC, 0xE1, 0x3C, 0xE0,
  0x65, 0x40, 0x06, 0x02, 0x62, 0xE2, 0x2D, 0xDC, 0xDD, 0xD7, 0xE1, 0x8F, 0xE8, 0xED, 0x83, 0xE2,
  0x5E, 0xE2, 0xDC, 0xDD, 0xD7, 0xE2, 0x89, 0x8E, 0xE2, 0x8F, 0xEC, 0xEF, 0x92, 0x19, 0xC3, 0x0B,
  0x77, 0xE1, 0x91, 0x8B, 0xCE, 0x94, 0x67, 0xEF, 0xE1, 0xEF, 0x8B, 0x83, 0xE1, 0x0D, 0x48, 0x84,
  0xE1, 0x77, 0x8F, 0x8A, 0x8E, 0xE3, 0x29, 0x66, 0x2F, 0xEF, 0xEE, 0x92, 0x16, 0x83, 0x06, 0x6E,
  0xB0, 0x9E, 0x87, 0xCE, 0x26, 0x6E, 0x8F, 0xED, 0xEF, 0x92, 0x19, 0xC3, 0x0A, 0x67, 0x9D, 0xE1,
  0xAE, 0xAF, 0xC3, 0x84, 0x61, 0x8E, 0x8B, 0x2B, 0x8A, 0xE6, 0x91, 0x91, 0x26, 0xE2, 0xED, 0x8C,
  0xE2, 0x9A, 0x98, 0xA6, 0x83, 0xE1, 0x23, 0x88, 0x87, 0x94, 0x8E, 0xE2, 0xF2, 0xA7, 0x88, 0xE3,
  0x8F, 0xEC, 0xE1, 0x85, 0x36, 0xCA, 0xC9, 0x83, 0xE1, 0x97, 0x8F, 0xE2, 0x8C, 0x8E, 0xC3, 0x90,
  0x90, 0x8F, 0xE6, 0x83, 0xE4, 0x66, 0xE2, 0xCA, 0xC3, 0xD4, 0x8F, 0xE2, 0x97, 0x83, 0xE1, 0xC9,
  0x90, 0x90, 0xC3, 0x8E, 0x8C, 0x8F, 0xE8, 0xED, 0x88, 0x01, 0xE1, 0x31, 0x85, 0x87, 0xC9, 0x93,
  0x88, 0x00, 0x0E, 0x92, 0xE1, 0x8F, 0xE6, 0xED, 0xFF, 0xFF, 0xFF,
};

extern const mamefont::Font ShapoSansP_s27c22a01w04(ShapoSansP_s27c22a01w04_blob);

#undef MAMEFONT_PROGMEM
