from shapofont.font import BitmapFont


def test_dimensions_from_name_and_json(simple_font_dir):
    font = BitmapFont(simple_font_dir)
    assert font.family_name == "TestF"
    assert font.dim_identifier == "s05c03a01"
    assert (font.body_size, font.cap_height, font.ascender_spacing, font.weight, font.bits_per_pixel) == (5, 3, 1, 1, 1)
    assert font.x_spacing == 1 and font.y_spacing == 2
    assert font.baseline == 4 and font.descent == 1 and font.line_height == 7


def test_glyphs_and_anti_spacers(simple_font_dir):
    font = BitmapFont(simple_font_dir)
    assert sorted(font.glyphs) == [0x2E, 0x41, 0x67]
    a = font.glyphs[0x41]
    assert (a.bmp.width, a.bmp.height) == (3, 5)
    assert a.bmp.get(1, 1) == 255 and a.bmp.get(0, 1) == 0
    assert font.x_advance_of(a) == 4
    dot = font.glyphs[0x2E]
    # Both anti-spacers: the left one consumes the whole marker, so the right one is 0
    assert (dot.left_anti_space, dot.right_anti_space) == (4, 0)
    assert font.x_offset_of(dot) == -4
    assert font.x_advance_of(dot) == 1


def test_draw_text_measures_and_skips_unknown(simple_font_dir, capsys):
    font = BitmapFont(simple_font_dir)
    w, h = font.draw_text(0, 0, "AgZ\nA")
    assert "no glyph" in capsys.readouterr().err
    assert w == 7  # 'A' advance 4 + 'g' width 3
    assert h == 7 + 5  # one line height + body of second line


def test_sample_image(simple_font_dir, tmp_path):
    from PIL import Image

    font = BitmapFont(simple_font_dir)
    out = tmp_path / "sample.png"
    font.generate_sample_image(str(out))
    with Image.open(out) as img:
        assert img.mode == "L" and img.width > 40


def test_grayscale_design(gray_font_dir):
    font = BitmapFont(gray_font_dir)
    assert font.bits_per_pixel == 2
    g = font.glyphs[0x41]
    assert [g.bmp.get(x, y) for y in range(2) for x in range(2)] == [255, 170, 0, 255]
