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


class BitmapGlyph:
    def __init__(self, code: int, bmp: GrayBitmap):
        self.code = code
        self.bmp = bmp


class BitmapFont:
    RE_OPTION = re.compile(r"(?P<k>s|c|w|h|a|p)(?P<v>\d+)")

    def __init__(self, dir_path: str):
        dir_path = dir_path.rstrip(path.sep)

        self.path = dir_path

        self.family_name = path.basename(path.dirname(dir_path))
        self.dim_identifier = path.basename(dir_path)
        self.full_name = f"{self.family_name}_{self.dim_identifier}"

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
        self.normal_x_spacing = dic.get("p", math.ceil(self.type_size / 16))

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

        # Find Glyphs
        self.glyphs: list[BitmapGlyph] = []
        marker_y = 1
        num_valid_glyphs = 0
        code_index = 0
        glyph_max_bmp_height = self.bitmap_height()
        while marker_y < self.bmp.height:
            # Find marker line
            found = False
            for x in range(self.bmp.width):
                col = self.bmp.get(x, marker_y)
                if (
                    col == Marker.VALID_BOTTOM_LINE
                    or col == Marker.DISABLED_BOTTOM_LINE
                ):
                    found = True
                    break
            if not found:
                marker_y += 1
                continue

            # Split into characters
            last_is_valid = False
            is_blue_marker = False
            start_x = 0
            for x in range(self.bmp.width):
                col = self.bmp.get(x, marker_y)
                curr_is_valid = col < 0
                if not last_is_valid and curr_is_valid:
                    # First pixel of marker line
                    start_x = x
                    is_blue_marker = col == Marker.DISABLED_BOTTOM_LINE
                else:
                    # Marker line continues
                    is_end_of_marker = last_is_valid and not curr_is_valid
                    is_end_of_line = curr_is_valid and x == self.bmp.width - 1
                    if is_end_of_marker or is_end_of_line:
                        if is_blue_marker:
                            glyph_width = 0
                        elif is_end_of_marker:
                            glyph_width = x - start_x
                        else:
                            glyph_width = x + 1 - start_x

                        bmp = self.bmp.crop(
                            start_x,
                            marker_y - glyph_max_bmp_height,
                            glyph_width,
                            glyph_max_bmp_height,
                        )

                        glyph = BitmapGlyph(self.codes[code_index], bmp)
                        self.glyphs.append(glyph)
                        glyph.valid = glyph_width != 0

                        if glyph.valid:
                            num_valid_glyphs += 1

                        code_index += 1

                last_is_valid = curr_is_valid

            marker_y += 1

    def bitmap_height(self) -> int:
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
            builder.add_glyph(
                glyph.code,
                glyph.bmp,
                y_offset=-(self.cap_height + self.ascender_spacing),
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

        builder = mamefont.MameFontBuilder(
            self.full_name,
            self.bitmap_height(),
            self.normal_x_spacing,
            self.line_height,
            vertical_frag=vertical_frag,
            msb1st=msb1st,
        )

        for glyph in self.glyphs:
            builder.add_glyph(
                glyph.code,
                glyph.bmp,
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
