#!/usr/bin/env python3

import json5
import os
from os import path
import re
import math
import argparse
import gfxfont
from design import GrayBitmap, Marker
from PIL import Image

DIMENSION_INVALID = -9999


class RawGlyph:
    def __init__(
        self,
        code: int,
        bmp: GrayBitmap,
        left_anti_space: int = 0,
        right_anti_space: int = 0,
    ):
        self.code = code
        self.bmp = bmp
        self.left_anti_space = left_anti_space
        self.right_anti_space = right_anti_space


class BitmapFont:
    RE_OPTION = re.compile(r"(?P<k>s|c|w|h|a|p)(?P<v>\d+)")

    def __init__(self, dir_path: str):
        self.body_size = DIMENSION_INVALID
        self.cap_height = DIMENSION_INVALID
        self.weight = DIMENSION_INVALID
        self.ascender_spacing = DIMENSION_INVALID
        self.default_x_spacing = DIMENSION_INVALID
        self.y_spacing = DIMENSION_INVALID

        self.sample_text = ""
        self.sample_size = DIMENSION_INVALID

        dir_path = dir_path.rstrip(path.sep)

        self.path = dir_path

        self.full_name = path.basename(dir_path)

        last_underline_pos = self.full_name.rfind("_")
        self.family_name = self.full_name[:last_underline_pos]
        self.dim_identifier = self.full_name[last_underline_pos + 1 :]

        # Extract options from directory name
        tmp = self.dim_identifier
        dic = {}
        s = re.search(self.RE_OPTION, tmp)
        while s:
            dic[s.group("k")] = int(s.group("v"))
            tmp = tmp[s.end() :]
            s = re.search(self.RE_OPTION, tmp)

        # Parse options
        if "s" in dic:
            self.body_size = dic["s"]

        if "c" in dic:
            self.cap_height = dic["c"]

        if "w" in dic:
            self.weight = dic["w"]

        if "a" in dic:
            self.ascender_spacing = dic["a"]

        # Load the image
        self.bmp = GrayBitmap.from_file(path.join(dir_path, "design.png"))

        # Default ASCII range
        self.codes = list(range(0x20, 0x7F))

        # Load JSON
        json_path = path.join(dir_path, "design.json5")
        if not path.exists(json_path):
            json_path = path.join(dir_path, "design.json")
        if path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                json_data = json5.load(f)

            if "codes" in json_data:
                self.codes = []
                code_ranges = json_data["codes"]
                for code_range in code_ranges:
                    start_code = int(code_range["from"])
                    end_code = int(code_range["to"])
                    self.codes.extend(range(start_code, end_code + 1))

            def get_dim(obj: dict, key: str, default_val: int):
                if key in obj:
                    value = int(obj[key])
                    if value != default_val and default_val != DIMENSION_INVALID:
                        print(
                            f"Warning: {key} in JSON ({value}) does not match with filename ({default_val})."
                        )
                    return value
                return default_val

            if "dimensions" in json_data:
                dims = json_data["dimensions"]
                self.body_size = get_dim(dims, "body_size", self.body_size)
                self.cap_height = get_dim(dims, "cap_height", self.cap_height)
                self.weight = get_dim(dims, "weight", self.weight)
                self.ascender_spacing = get_dim(
                    dims, "ascender_spacing", self.ascender_spacing
                )
                self.default_x_spacing = get_dim(
                    dims, "x_spacing", self.default_x_spacing
                )
                self.y_spacing = get_dim(dims, "y_spacing", self.y_spacing)
            
            if "sample" in json_data:
                sample = json_data["sample"]
                if "text" in sample:
                    self.sample_text = sample["text"]
                if "size" in sample:
                    self.sample_size = int(sample["size"])

        if self.body_size <= 0:
            raise ValueError(f"Type size missing.")

        if self.default_x_spacing == DIMENSION_INVALID:
            self.default_x_spacing = math.ceil(self.body_size / 16)

        if self.cap_height == DIMENSION_INVALID:
            self.cap_height = self.body_size

        if self.weight == DIMENSION_INVALID:
            self.weight = 1

        if self.ascender_spacing == DIMENSION_INVALID:
            self.ascender_spacing = 0

        if self.default_x_spacing == DIMENSION_INVALID:
            self.default_x_spacing = math.ceil(self.body_size / 16.0)

        if self.y_spacing == DIMENSION_INVALID:
            self.y_spacing = math.ceil(
                (self.body_size - self.ascender_spacing) * 1.2 - self.body_size
            )

        # Find Glyphs
        self.glyphs: dict[int, RawGlyph] = {}
        glyph_index = 0
        y = self.body_size
        while y < self.bmp.height:
            # Find marker line
            found = False
            x = 0
            while x < self.bmp.width:
                if self.bmp.get(x, y) == Marker.GLYPH:
                    glyph = self.parse_glyph(x, y, self.codes[glyph_index])
                    glyph_index += 1

                    self.glyphs[glyph.code] = glyph
                    x += glyph.bmp.width

                    found = True
                else:
                    x += 1

            if found:
                y += 1 + self.body_size
            else:
                y += 1

    def parse_glyph(self, x: int, y: int, code: int) -> RawGlyph:
        # Find end of glyph marker
        w = 0
        while self.bmp.get(x + w, y, 0) == Marker.GLYPH:
            w += 1
        if w <= 0:
            raise ValueError("Glyph marker not found")
        glyph_width = w

        # Find left side anti spacer
        w = 0
        while self.bmp.get(x + w, y + 1, 0) == Marker.SPACING:
            w += 1
        left_anti_space = w

        # Find right side anti spacer
        if left_anti_space < glyph_width:
            w = 0
            while self.bmp.get(x + glyph_width - 1 - w, y + 1, 0) == Marker.SPACING:
                w += 1
            right_anti_space = w
        else:
            right_anti_space = 0

        # Extract Glyph Bitmap
        bmp = self.bmp.crop(
            x,
            y - self.body_size,
            glyph_width,
            self.body_size,
        )

        return RawGlyph(code, bmp, left_anti_space, right_anti_space)

    def to_gfx_font(self, outdir: str):
        out_file = path.join(outdir, f"{self.full_name}.h")
        # print(f"Generating GFXfont: {out_file}")

        builder = gfxfont.GFXfontBuilder(
            self.full_name,
            self.body_size + self.y_spacing,
            self.default_x_spacing,
        )

        for glyph in self.glyphs.values():
            x_offset = -glyph.left_anti_space
            y_offset = -(self.cap_height + self.ascender_spacing)
            x_advance = (
                self.default_x_spacing
                + x_offset
                + glyph.bmp.width
                - glyph.right_anti_space
            )
            builder.add_glyph(
                glyph.code,
                glyph.bmp,
                x_offset=x_offset,
                y_offset=y_offset,
                x_advance=x_advance,
            )
        gfx_font = builder.build()
        with open(out_file, "w") as f:
            f.write(gfx_font.generate_header())

    def draw_text(
        self,
        x_offset: int,
        y_offset: int,
        text: str,
        size: int = 1,
        bmp: GrayBitmap | None = None,
    ) -> tuple[int, int]:
        width = 0
        height = 0

        x = 0
        y = 0
        for c in text:
            if c == "\n":
                x = 0
                y += (self.body_size + self.y_spacing) * size
                continue
            glyph = self.glyphs[ord(c)]
            width = max(width, x + glyph.bmp.width * size)
            height = max(height, y + self.body_size * size)
            x -= glyph.left_anti_space * size
            if bmp:
                bmp.draw(glyph.bmp, x_offset + x, y_offset + y, size)
            x += glyph.bmp.width * size
            x += self.default_x_spacing * size
            x -= glyph.right_anti_space * size

        return width, height

    def generate_sample_image(self, out_file: str):
        has_all_ascii_chars = True
        for code in range(0x20, 0x7F):
            if code not in self.glyphs:
                has_all_ascii_chars = False
                break

        if len(self.sample_text) == 0:
            if has_all_ascii_chars:
                self.sample_text = self.family_name + "\n"
                self.sample_text += (
                    "The Quick Brown\nFox Jumps Over\nThe Lazy Dog.\n"
                    + "#0123456789.,:;\n\"(+)[-]{*}'=`!?\n@$%&<>/\\_|^~"
                )
            else:
                codes = sorted(self.glyphs.keys())
                cols = 16
                for i in range(len(codes)):
                    code = codes[i]
                    if 0x20 <= code < 0x7F:
                        self.sample_text += chr(code)
                    if (i + 1) % cols == 0:
                        self.sample_text += "\n"

        w, h = self.draw_text(0, 0, self.sample_text, 1)

        if self.sample_size < 1:
            self.sample_size = math.ceil(512 / w)

        w *= self.sample_size
        h *= self.sample_size

        PADDING = 20
        w += PADDING * 2
        h += PADDING * 2

        canvas = GrayBitmap.create(w, h)
        self.draw_text(PADDING, PADDING, self.sample_text, self.sample_size, canvas)

        canvas.export(out_file)

        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("--outdir_gfx_c")
    parser.add_argument("--sample_img")
    args = parser.parse_args()

    font = BitmapFont(args.input)

    if args.outdir_gfx_c:
        font.to_gfx_font(args.outdir_gfx_c)

    if args.sample_img:
        font.generate_sample_image(args.sample_img)


if __name__ == "__main__":
    main()
