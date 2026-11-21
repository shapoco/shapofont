import json
from os import path

import pytest
from PIL import Image

RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GRAY = (170, 170, 170)


def write_design(dir_path: str, body_size: int, glyphs: list[list[str]], codes: list[int], extra_json: dict | None = None):
    """Create design.png / design.json from ASCII art.

    Glyph rows use '#' for white, '+' for gray, '.' for black. A red marker line is
    added under each glyph, and a blue anti-spacer under marker columns marked with 'b'
    in an optional last row that starts with ':'.
    """
    gap = 1
    width = sum(len(g[0]) for g in glyphs) + gap * (len(glyphs) + 1)
    height = body_size + 2
    img = Image.new("RGB", (width, height), (0, 0, 0))
    x = gap
    for glyph in glyphs:
        rows = [r for r in glyph if not r.startswith(":")]
        spacer = next((r[1:] for r in glyph if r.startswith(":")), "")
        w = len(rows[0])
        assert len(rows) == body_size
        for y, row in enumerate(rows):
            for dx, ch in enumerate(row):
                if ch == "#":
                    img.putpixel((x + dx, y), WHITE)
                elif ch == "+":
                    img.putpixel((x + dx, y), GRAY)
        for dx in range(w):
            img.putpixel((x + dx, body_size), RED)
        for dx, ch in enumerate(spacer):
            if ch == "b":
                img.putpixel((x + dx, body_size + 1), BLUE)
        x += w + gap
    img.save(path.join(dir_path, "design.png"))
    data = {"codes": [{"from": c, "to": c} for c in codes]}
    data.update(extra_json or {})
    with open(path.join(dir_path, "design.json"), "w") as f:
        json.dump(data, f)


@pytest.fixture
def simple_font_dir(tmp_path):
    """TestF_s05c03a01: body 5 = 1 px ascender space + 3 px cap height + 1 px descent.

    Glyphs must appear in the image in code order: '.', 'A', 'g'.
    """
    d = tmp_path / "TestF_s05c03a01"
    d.mkdir()
    write_design(
        str(d),
        5,
        [
            ["....", "....", "....", ".##.", "....", ":bbbb"],  # '.' (0x2E): 4 px wide, all four columns anti-spaced
            ["...", ".#.", "#.#", "###", "..."],  # 'A' (0x41): sits on the baseline
            ["...", "##.", ".##", "..#", "###"],  # 'g' (0x67): descends 1 px below the baseline
        ],
        [0x2E, 0x41, 0x67],
        {"dimensions": {"x_spacing": 1, "y_spacing": 2}},
    )
    return str(d)


@pytest.fixture
def gray_font_dir(tmp_path):
    d = tmp_path / "TestG_s02g02"
    d.mkdir()
    write_design(str(d), 2, [["#+", ".#"]], [0x41])
    return str(d)
