"""Round-trip tests: generate an LVGL font source, parse it back, compare with the design."""

import re

from shapofont.design import GrayBitmap
from shapofont.font import BitmapFont
from shapofont.lvgl import contiguous_ranges, generate_lvgl_font, pack_bitmap

import pytest


def parse_lvgl_source(src: str):
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    bitmap_src = re.search(r"glyph_bitmap\[\] = \{(.*?)\};", src, re.S).group(1)
    bitmap = [int(b, 16) for b in re.findall(r"0x([0-9A-Fa-f]{2})", bitmap_src)]
    dsc_src = re.search(r"glyph_dsc\[\] = \{(.*?)\};", src, re.S).group(1)
    glyphs = []
    for m in re.finditer(r"\{([^}]*)\}", dsc_src):
        fields = dict(re.findall(r"\.(\w+) = (-?\d+)", m.group(1)))
        glyphs.append({k: int(v) for k, v in fields.items()})
    cmaps = []
    for m in re.finditer(r"\{\s*(\.range_start[^}]*)\}", src):
        fields = dict(re.findall(r"\.(\w+) = (-?\w+)", m.group(1)))
        cmaps.append(fields)
    font = dict(re.findall(r"\.(line_height|base_line|underline_thickness) = (-?\d+)", src))
    bpp = int(re.search(r"\.bpp = (\d+)", src).group(1))
    return bitmap, glyphs, cmaps, {k: int(v) for k, v in font.items()}, bpp


def decode_glyph(bitmap, g, bpp):
    """Decode a glyph the way LVGL does for plain format with stride 0."""
    levels = (1 << bpp) - 1
    pixels = []
    bit_pos = g["bitmap_index"] * 8
    for _ in range(g["box_w"] * g["box_h"]):
        byte = bitmap[bit_pos // 8]
        shift = 8 - bpp - (bit_pos % 8)
        pixels.append(((byte >> shift) & levels) * 255 // levels)
        bit_pos += bpp
    return pixels


def glyph_lookup(cmaps, code):
    for c in cmaps:
        start, length = int(c["range_start"]), int(c["range_length"])
        if start <= code < start + length:
            assert c["type"] == "LV_FONT_FMT_TXT_CMAP_FORMAT0_TINY"
            return int(c["glyph_id_start"]) + code - start
    return 0


def test_pack_bitmap_2bpp():
    bmp = GrayBitmap([255, 170, 85, 0, 255], 5, 1)
    assert pack_bitmap(bmp, 0, 0, 5, 1, 2) == [0b11100100, 0b11000000]


def test_contiguous_ranges():
    assert contiguous_ranges([46, 48, 49, 50, 65]) == [(46, 1), (48, 3), (65, 1)]


def test_roundtrip_1bpp(simple_font_dir):
    font = BitmapFont(simple_font_dir)
    src = generate_lvgl_font(font)
    bitmap, glyphs, cmaps, metrics, bpp = parse_lvgl_source(src)

    assert bpp == 1
    assert f"const lv_font_t {font.full_name} = " in src
    assert "#if LVGL_VERSION_MAJOR == 8" in src and ".cache = &cache" in src
    assert metrics == {"line_height": 7, "base_line": 3, "underline_thickness": 1}
    empty = {"bitmap_index": 0, "adv_w": 0, "box_w": 0, "box_h": 0, "ofs_x": 0, "ofs_y": 0}
    assert glyphs[0] == empty
    assert len(glyphs) == 1 + 3 + 3 and glyphs[2] == glyphs[4] == glyphs[6] == empty  # padding after each range
    assert [(int(c["range_start"]), int(c["range_length"]), int(c["glyph_id_start"])) for c in cmaps] == [(46, 1, 1), (65, 1, 3), (103, 1, 5)]

    for code, raw in font.glyphs.items():
        g = glyphs[glyph_lookup(cmaps, code)]
        assert g["adv_w"] == font.x_advance_of(raw) * 16
        x, y, w, h = raw.bmp.bounding_box()
        assert (g["box_w"], g["box_h"]) == (w, h)
        assert g["ofs_x"] == font.x_offset_of(raw) + x
        assert g["ofs_y"] == font.baseline - (y + h)
        expected = [raw.bmp.get(x + dx, y + dy) for dy in range(h) for dx in range(w)]
        assert decode_glyph(bitmap, g, bpp) == expected

    a, g = glyphs[glyph_lookup(cmaps, 0x41)], glyphs[glyph_lookup(cmaps, 0x67)]
    assert a["ofs_y"] == 0 and g["ofs_y"] == -1  # 'A' sits on the baseline, 'g' descends below it
    assert glyphs[glyph_lookup(cmaps, 0x2E)]["ofs_x"] == -3


def test_roundtrip_2bpp(gray_font_dir):
    font = BitmapFont(gray_font_dir)
    bitmap, glyphs, cmaps, _, bpp = parse_lvgl_source(generate_lvgl_font(font))
    assert bpp == 2
    g = glyphs[glyph_lookup(cmaps, 0x41)]
    assert decode_glyph(bitmap, g, bpp) == [255, 170, 0, 255]


def test_rejects_too_wide_advance(tmp_path):
    from conftest import write_design

    d = tmp_path / "Wide_s01"
    d.mkdir()
    write_design(str(d), 1, [["#" * 260]], [0x41])
    with pytest.raises(ValueError):
        generate_lvgl_font(BitmapFont(str(d)))
