#include <stdio.h>

#include "mamefont/ShapoSansP_s05.hpp"
#include "mamefont/mamefont.hpp"

int main(int argc, char** argv) {
  mamefont::Status ret;
  const auto& font = ShapoSansP_s05;

  int glyphHeight = font.glyphHeight();
  int numChars = font.glyphTableLen();
  int codeOffset = font.firstCode();
  bool verticalScan = font.verticalScanEnabled();

  printf("font32.glyphHeight()        : %d\n", glyphHeight);
  printf("font32.glyphTableLen()      : %d\n", numChars);
  printf("font32.firstCode()          : %d\n", codeOffset);
  printf("font32.verticalScanEnabled(): %d\n", verticalScan);
  fflush(stdout);

  uint8_t buff[font.calcGlyphBufferSize() * 2];
  uint8_t history[mamefont::HISTORY_SIZE];

  constexpr int X_ZOOM = 3;

  for (int i = 0; i < numChars; i++) {
    char code = codeOffset + i;
    mamefont::Glyph glyph;
    ret = font.getGlyph(code, &glyph);
    printf("#%-3d", (int)i);
    if (0x20 <= code && code <= 0x7e) {
      printf(" '%c'", code);
    }
    printf(" (0x%02x)\n", (int)code);
    if (ret == mamefont::Status::SUCCESS) {
      int glyphWidth = glyph.width();
      printf("  glyph.width: %d\n", glyphWidth);

      mamefont::RenderContext ctx;
      ctx.init(font.getEntryPoint(glyph), &glyph, buff);
      ret = font.renderGlyph(&ctx);
      if (ret != mamefont::Status::SUCCESS) {
        printf("  *ERROR CODE: %02x\n", (int)ret);
        return 1;
      }
      printf("  +");
      for (int x = 0; x < glyphWidth * X_ZOOM; x++) printf("-");
      printf("+\n");
      for (int y = 0; y < glyphHeight; y++) {
        printf("  |");
        for (int x = 0; x < glyphWidth; x++) {
          uint8_t bit;
          if (verticalScan) {
            uint8_t col = (x / mamefont::SEGMENT_HEIGHT);
            uint8_t seg = buff[y * glyphHeight + y];
            bit = (seg >> (x % mamefont::SEGMENT_HEIGHT)) & 0x1;
          } else {
            uint8_t row = (y / mamefont::SEGMENT_HEIGHT);
            uint8_t seg = buff[row * glyphWidth + x];
            bit = (seg >> (y % mamefont::SEGMENT_HEIGHT)) & 0x1;
          }
          for (int z = 0; z < X_ZOOM; z++) {
            printf("%s", bit ? "#" : " ");
          }
        }
        printf("|\n");
      }
      printf("  +");
      for (int x = 0; x < glyphWidth * X_ZOOM; x++) printf("-");
      printf("+\n");
      printf("\n");
    } else if (ret == mamefont::Status::GLYPH_NOT_DEFINED) {
      // ignore
    } else {
      printf("  *ERROR CODE: %02x\n", (int)ret);
      return 1;
    }
  }

  return 0;
}
