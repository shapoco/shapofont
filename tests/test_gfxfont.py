import re

from shapofont.font import BitmapFont
from shapofont.gfxfont import GFXfontBuilder, generate_gfxfont, pack_bitmap_1bpp
from shapofont.design import GrayBitmap

import pytest


def parse_header(src: str):
    bitmaps = [int(b, 16) for b in re.findall(r"0x([0-9A-F]{2}),", src.split("Bitmaps[]")[1].split("};")[0])]
    glyph_rows = re.findall(r"\{ 0x([0-9A-F]+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+) \}", src)
    glyphs = [(int(r[0], 16),) + tuple(int(v) for v in r[1:]) for r in glyph_rows]
    return bitmaps, glyphs


def test_pack_bitmap_1bpp_continuous_rows():
    bmp = GrayBitmap([255, 0, 0, 255, 255, 255], 3, 2)
    assert pack_bitmap_1bpp(bmp, 0, 0, 3, 2) == [0b10011100]


def test_generate_gfxfont_metrics(simple_font_dir):
    font = BitmapFont(simple_font_dir)
    src = generate_gfxfont(font)
    assert f"GFXfont {font.full_name} SHAPOFONT_PROGMEM" in src
    assert re.search(r"0x2E,\n\s*0x67,\n\s*7\n", src)  # first, last, yAdvance
    bitmaps, glyphs = parse_header(src)
    assert len(glyphs) == 0x67 - 0x2E + 1
    a = glyphs[0x41 - 0x2E]
    offset, w, h, x_adv, x_off, y_off = a
    assert (w, h, x_adv, x_off, y_off) == (3, 3, 4, 0, -3)  # top of 'A' is 3 px above the baseline
    g = glyphs[0x67 - 0x2E]
    assert (g[1], g[2], g[5]) == (3, 4, -3)
    dot = glyphs[0]
    assert (dot[1], dot[2], dot[3], dot[4], dot[5]) == (2, 1, 1, -3, -1)
    assert bitmaps[a[0]] == 0b01010111 and bitmaps[a[0] + 1] & 0x80


def test_generate_gfxfont_rejects_grayscale(gray_font_dir):
    with pytest.raises(ValueError):
        generate_gfxfont(BitmapFont(gray_font_dir))


def test_deduplication_shares_identical_bitmaps():
    builder = GFXfontBuilder("Dup", 8)
    bmp = GrayBitmap([255, 255, 0, 255], 2, 2)
    builder.add_glyph(0x41, bmp, 0, -2, 3)
    builder.add_glyph(0x42, bmp, 0, -2, 3)
    other = GrayBitmap([255, 0, 0, 255, 255, 255, 255, 255, 255], 3, 3)
    builder.add_glyph(0x43, other, 0, -3, 4)
    font = builder.build()
    assert font.glyphs[0].bitmap_offset == font.glyphs[1].bitmap_offset
    assert len(font.bitmap) == 1 + 2
