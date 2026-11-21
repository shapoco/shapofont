"""Parsing of a font design directory into glyph bitmaps and metrics."""

from __future__ import annotations

import json
import math
import re
import sys
from os import path

from .design import GrayBitmap, Marker

DESIGN_IMAGE_NAME = "design.png"
DESIGN_JSON_NAME = "design.json"


class RawGlyph:
    def __init__(self, code: int, bmp: GrayBitmap, left_anti_space: int = 0, right_anti_space: int = 0):
        self.code = code
        self.bmp = bmp  # body_size pixels tall, glyph-width pixels wide
        self.left_anti_space = left_anti_space
        self.right_anti_space = right_anti_space


class BitmapFont:
    """A font loaded from a design directory.

    The directory name is the full font name: `<Family>_<dimension id>`, where
    the dimension id is a concatenation of options like `s12c09a01w02g02`:

    - s: body size (required)
    - c: cap height (default: s)
    - a: ascender spacing (default: 0)
    - w: weight (default: 1)
    - g: bits per pixel (default: 1)

    `design.json` in the directory lists the character codes and can override
    the dimensions.
    """

    RE_OPTION = re.compile(r"(?P<k>[scawg])(?P<v>\d+)")

    def __init__(self, dir_path: str):
        dir_path = dir_path.rstrip(path.sep)
        self.path = dir_path
        self.full_name = path.basename(dir_path)

        last_underline_pos = self.full_name.rfind("_")
        if last_underline_pos < 0:
            raise ValueError(f"Font directory name must be '<Family>_<dimensions>': {self.full_name}")
        self.family_name = self.full_name[:last_underline_pos]
        self.dim_identifier = self.full_name[last_underline_pos + 1 :]

        name_opts = {m.group("k"): int(m.group("v")) for m in self.RE_OPTION.finditer(self.dim_identifier)}

        body_size: int | None = name_opts.get("s")
        cap_height: int | None = name_opts.get("c")
        ascender_spacing: int | None = name_opts.get("a")
        weight: int | None = name_opts.get("w")
        bits_per_pixel: int | None = name_opts.get("g")
        x_spacing: int | None = None
        y_spacing: int | None = None

        self.codes: list[int] = list(range(0x20, 0x7F))
        self.sample_text = ""
        self.sample_size = 0

        json_path = path.join(dir_path, DESIGN_JSON_NAME)
        if path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)

            if "codes" in json_data:
                self.codes = []
                for code_range in json_data["codes"]:
                    self.codes.extend(range(int(code_range["from"]), int(code_range["to"]) + 1))

            def override(obj: dict, key: str, current: int | None) -> int | None:
                if key not in obj:
                    return current
                value = int(obj[key])
                if current is not None and value != current:
                    print(
                        f"Warning: {self.full_name}: {key} in JSON ({value}) does not match the directory name ({current}).",
                        file=sys.stderr,
                    )
                return value

            bits_per_pixel = override(json_data, "bits_per_pixel", bits_per_pixel)
            dims = json_data.get("dimensions", {})
            body_size = override(dims, "body_size", body_size)
            cap_height = override(dims, "cap_height", cap_height)
            weight = override(dims, "weight", weight)
            ascender_spacing = override(dims, "ascender_spacing", ascender_spacing)
            x_spacing = override(dims, "x_spacing", x_spacing)
            y_spacing = override(dims, "y_spacing", y_spacing)

            sample = json_data.get("sample", {})
            self.sample_text = sample.get("text", "")
            self.sample_size = int(sample.get("size", 0))

        if body_size is None or body_size <= 0:
            raise ValueError(f"{self.full_name}: body size (option 's') is missing.")

        self.body_size = body_size
        self.cap_height = body_size if cap_height is None else cap_height
        self.weight = 1 if weight is None else weight
        self.ascender_spacing = 0 if ascender_spacing is None else ascender_spacing
        self.bits_per_pixel = 1 if bits_per_pixel is None else bits_per_pixel
        self.x_spacing = math.ceil(body_size / 16) if x_spacing is None else x_spacing
        if y_spacing is None:
            y_spacing = math.ceil((body_size - self.ascender_spacing) * 1.2 - body_size)
        self.y_spacing = y_spacing

        self.bmp = GrayBitmap.from_file(path.join(dir_path, DESIGN_IMAGE_NAME), self.bits_per_pixel)
        self.glyphs: dict[int, RawGlyph] = {}
        self._find_glyphs()

    # Metrics -------------------------------------------------------------

    @property
    def baseline(self) -> int:
        """Distance from the top of the glyph body to the baseline, in pixels."""
        return self.cap_height + self.ascender_spacing

    @property
    def descent(self) -> int:
        """Distance from the baseline to the bottom of the glyph body, in pixels."""
        return self.body_size - self.baseline

    @property
    def line_height(self) -> int:
        return self.body_size + self.y_spacing

    def x_offset_of(self, glyph: RawGlyph) -> int:
        return -glyph.left_anti_space

    def x_advance_of(self, glyph: RawGlyph) -> int:
        return self.x_spacing + self.x_offset_of(glyph) + glyph.bmp.width - glyph.right_anti_space

    # Design parsing --------------------------------------------------------

    def _find_glyphs(self) -> None:
        glyph_index = 0
        y = self.body_size
        while y < self.bmp.height:
            found = False
            x = 0
            while x < self.bmp.width:
                if self.bmp.get(x, y) == Marker.GLYPH:
                    if glyph_index >= len(self.codes):
                        raise ValueError(
                            f"{self.full_name}: more glyph markers in the image than codes in {DESIGN_JSON_NAME} ({len(self.codes)})."
                        )
                    glyph = self._parse_glyph(x, y, self.codes[glyph_index])
                    glyph_index += 1
                    self.glyphs[glyph.code] = glyph
                    x += glyph.bmp.width
                    found = True
                else:
                    x += 1
            y += 1 + self.body_size if found else 1

        if glyph_index < len(self.codes):
            print(
                f"Warning: {self.full_name}: {len(self.codes)} codes listed but only {glyph_index} glyphs found.",
                file=sys.stderr,
            )

    def _parse_glyph(self, x: int, y: int, code: int) -> RawGlyph:
        glyph_width = 0
        while self.bmp.get(x + glyph_width, y, 0) == Marker.GLYPH:
            glyph_width += 1
        if glyph_width <= 0:
            raise ValueError("Glyph marker not found")

        left_anti_space = 0
        while self.bmp.get(x + left_anti_space, y + 1, 0) == Marker.SPACING:
            left_anti_space += 1

        right_anti_space = 0
        if left_anti_space < glyph_width:
            while self.bmp.get(x + glyph_width - 1 - right_anti_space, y + 1, 0) == Marker.SPACING:
                right_anti_space += 1

        bmp = self.bmp.crop(x, y - self.body_size, glyph_width, self.body_size)
        return RawGlyph(code, bmp, left_anti_space, right_anti_space)

    # Rendering ------------------------------------------------------------

    def draw_text(self, x_offset: int, y_offset: int, text: str, scale: int = 1, canvas: GrayBitmap | None = None) -> tuple[int, int]:
        """Draw `text` onto `canvas` (or just measure it when canvas is None).

        Returns the (width, height) of the rendered text in pixels.
        Characters not in the font are skipped with a warning.
        """
        width = 0
        height = 0
        x = 0
        y = 0
        for c in text:
            if c == "\n":
                x = 0
                y += self.line_height * scale
                continue
            glyph = self.glyphs.get(ord(c))
            if glyph is None:
                print(f"Warning: {self.full_name}: no glyph for {c!r} (U+{ord(c):04X}); skipped.", file=sys.stderr)
                continue
            x += self.x_offset_of(glyph) * scale
            width = max(width, x + glyph.bmp.width * scale)
            height = max(height, y + self.body_size * scale)
            if canvas:
                canvas.draw(glyph.bmp, x_offset + x, y_offset + y, scale)
            x += (self.x_advance_of(glyph) - self.x_offset_of(glyph)) * scale
        return width, height

    def default_sample_text(self) -> str:
        if all(code in self.glyphs for code in range(0x20, 0x7F)):
            return (
                self.family_name + "\n"
                "The Quick Brown\nFox Jumps Over\nThe Lazy Dog.\n"
                "#0123456789.,:;\n\"(+)[-]{*}'=`!?\n@$%&<>/\\_|^~"
            )
        cols = 16
        lines = []
        codes = [code for code in sorted(self.glyphs) if 0x20 <= code < 0x7F]
        for i in range(0, len(codes), cols):
            lines.append("".join(chr(code) for code in codes[i : i + cols]))
        return "\n".join(lines)

    def generate_sample_image(self, out_file: str) -> None:
        text = self.sample_text or self.default_sample_text()
        w, h = self.draw_text(0, 0, text)
        scale = self.sample_size if self.sample_size >= 1 else max(1, math.ceil(512 / max(1, w)))

        padding = 20
        canvas = GrayBitmap.create(w * scale + padding * 2, h * scale + padding * 2)
        self.draw_text(padding, padding, text, scale, canvas)
        canvas.export(out_file)
