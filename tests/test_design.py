from shapofont.design import GrayBitmap, Marker, classify_pixel, quantize_gray

import pytest


def test_quantize_gray_1bpp():
    assert quantize_gray(0, 1) == 0
    assert quantize_gray(127, 1) == 0
    assert quantize_gray(128, 1) == 255
    assert quantize_gray(255, 1) == 255


def test_quantize_gray_2bpp():
    assert [quantize_gray(v, 2) for v in (0, 85, 170, 255)] == [0, 85, 170, 255]
    assert quantize_gray(90, 2) == 85
    assert quantize_gray(166, 2) == 170
    assert quantize_gray(195, 2) == 170


def test_classify_pixel_markers():
    assert classify_pixel((255, 0, 0), 1) == Marker.GLYPH
    assert classify_pixel((237, 28, 36), 1) == Marker.GLYPH  # mspaint red
    assert classify_pixel((0, 0, 255), 1) == Marker.SPACING
    assert classify_pixel((0, 75, 255), 1) == Marker.SPACING
    assert classify_pixel((200, 200, 200), 1) == 255
    assert classify_pixel((10, 10, 10), 1) == 0


def test_classify_pixel_rejects_unknown_colors():
    with pytest.raises(ValueError):
        classify_pixel((0, 255, 0), 1)
    with pytest.raises(ValueError):
        classify_pixel((128, 0, 0), 1)  # dark red: ambiguous


def test_crop_is_a_view_and_bounding_box():
    bmp = GrayBitmap.create(6, 4)
    bmp.set(2, 1, 255)
    bmp.set(4, 2, 255)
    view = bmp.crop(1, 1, 5, 3)
    assert view.get(1, 0) == 255
    assert view.get(3, 1) == 255
    assert view.bounding_box() == (1, 0, 3, 2)
    assert GrayBitmap.create(3, 3).bounding_box() is None
    with pytest.raises(IndexError):
        view.get(5, 0)
    assert view.get(5, 0, 7) == 7


def test_draw_blends_and_scales():
    canvas = GrayBitmap.create(4, 4)
    src = GrayBitmap([255, 0, 0, 128], 2, 2)
    canvas.draw(src, 0, 0, 2)
    assert canvas.get(0, 0) == 255 and canvas.get(1, 1) == 255
    assert canvas.get(2, 0) == 0
    assert canvas.get(2, 2) == 128
    canvas.draw(src, 2, 2)  # partly outside: must not raise
