#!/usr/bin/env python3

import json5
import os
from os import path
import re
import math
import argparse
import gfxfont
import mamefont
from design import GrayBitmap, Marker


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
        if not "s" in dic:
            raise ValueError(
                f"Missing 's' option in directory name: '{self.dim_identifier}'"
            )
        self.type_size = dic["s"]
        self.cap_height = dic.get("c", self.type_size)
        self.weight = dic.get("w", 1)
        self.ascender_spacing = dic.get("a", 0)
        self.line_height = dic.get(
            "h", math.ceil((self.type_size - self.ascender_spacing) * 1.2)
        )

        self.normal_x_spacing = math.ceil(self.type_size / 16)

        # Load the image
        self.bmp = GrayBitmap.from_file(path.join(dir_path, "design.png"))

        # Default ASCII range
        self.codes = list(range(0x20, 0x7F))

        # Load JSON
        json_path = path.join(dir_path, "shapofont.json5")
        if not path.exists(json_path):
            json_path = path.join(dir_path, "shapofont.json")
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
            if "x_spacing" in json_data:
                x_spacing = json_data["x_spacing"]
                if "default" in x_spacing:
                    self.normal_x_spacing = int(x_spacing["default"])
            if "y_spacing" in json_data:
                y_spacing = json_data["y_spacing"]
                if "default" in y_spacing:
                    self.line_height = self.type_size + int(y_spacing["default"])

        # Find Glyphs
        self.glyphs: list[RawGlyph] = []
        glyph_index = 0
        max_glyph_height = self.max_glyph_height()
        y = max_glyph_height
        while y < self.bmp.height:
            # Find marker line
            found = False
            x = 0
            while x < self.bmp.width:
                if self.bmp.get(x, y) == Marker.GLYPH:
                    glyph = self.parse_glyph(x, y, self.codes[glyph_index])
                    glyph_index += 1

                    self.glyphs.append(glyph)
                    x += glyph.bmp.width

                    found = True
                else:
                    x += 1

            if found:
                y += 1 + max_glyph_height
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
        glyph_height = self.max_glyph_height()
        bmp = self.bmp.crop(
            x,
            y - glyph_height,
            glyph_width,
            glyph_height,
        )

        return RawGlyph(code, bmp, left_anti_space, right_anti_space)

    def max_glyph_height(self) -> int:
        return self.type_size

    def to_gfx_font(self, outdir: str):
        out_file = path.join(outdir, f"{self.full_name}.h")
        # print(f"Generating GFXfont: {out_file}")

        builder = gfxfont.GFXfontBuilder(
            self.full_name,
            self.line_height,
            self.normal_x_spacing,
        )

        for glyph in self.glyphs:
            x_offset = -glyph.left_anti_space
            y_offset = -(self.cap_height + self.ascender_spacing)
            x_advance = (
                self.normal_x_spacing
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

    def to_mame_font(
        self,
        hpp_outdir: str = None,
        cpp_outdir: str = None,
        json_outdir: str = None,
        vertical_frag: bool = False,
        msb1st: bool = False,
    ):
        # print(f"Generating MameFont: {self.full_name}")

        glyph_height = self.max_glyph_height()

        builder = mamefont.MameFontBuilder(
            self.full_name,
            glyph_height,
            self.line_height - glyph_height,
            vertical_frag=vertical_frag,
            msb1st=msb1st,
        )

        for glyph in self.glyphs:
            x_negative_offset = glyph.left_anti_space
            x_spacing = (
                self.normal_x_spacing - x_negative_offset - glyph.right_anti_space
            )
            builder.add_glyph(
                glyph.code,
                glyph.bmp,
                x_spacing,
                x_negative_offset,
            )

        mame_font = builder.build()

        if hpp_outdir:
            hpp_file = path.join(hpp_outdir, f"{self.full_name}.hpp")
            with open(hpp_file, "w") as f:
                f.write(mame_font.generate_cpp_header())

        if cpp_outdir:
            cpp_file = path.join(cpp_outdir, f"{self.full_name}.cpp")
            with open(cpp_file, "w") as f:
                f.write(mame_font.generate_cpp_source())

        if json_outdir:
            json_file = path.join(json_outdir, f"{self.full_name}.json")
            with open(json_file, "w") as f:
                f.write(mame_font.generate_json())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("--mame_arch", default="HL")
    parser.add_argument("--outdir_gfx_c")
    parser.add_argument("--outdir_mame_hpp")
    parser.add_argument("--outdir_mame_cpp")
    parser.add_argument("--outdir_mame_json")
    args = parser.parse_args()

    font = BitmapFont(args.input)

    if args.outdir_gfx_c:
        font.to_gfx_font(args.outdir_gfx_c)

    if args.outdir_mame_hpp or args.outdir_mame_cpp or args.outdir_mame_json:
        if args.mame_arch == "HL":
            vertical_frag = False
            msb1st = False
        elif args.mame_arch == "HM":
            vertical_frag = False
            msb1st = True
        elif args.mame_arch == "VL":
            vertical_frag = True
            msb1st = False
        elif args.mame_arch == "VM":
            vertical_frag = True
            msb1st = True
        else:
            raise ValueError(
                f"Unsupported memory architecture for MameFont: {args.mame_arch}"
            )

        font.to_mame_font(
            args.outdir_mame_hpp,
            args.outdir_mame_cpp,
            args.outdir_mame_json,
            vertical_frag=vertical_frag,
            msb1st=msb1st,
        )


if __name__ == "__main__":
    main()
