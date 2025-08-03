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
        negative_offset: int = 0,
        explicit_advance: int | None = None,
    ):
        self.code = code
        self.bmp = bmp
        self.negative_offset = negative_offset
        self.explicit_advance = explicit_advance

    def design_width(self) -> int:
        if self.explicit_advance == None:
            return self.bmp.width
        else:
            return max(self.bmp.width, self.negative_offset + self.explicit_advance)


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
                    x += glyph.design_width()

                    found = True
                else:
                    x += 1

            if found:
                y += 1 + max_glyph_height
            else:
                y += 1

    def parse_glyph(self, x: int, y: int, code: int) -> RawGlyph:
        # Find end of glyph marker
        glyph_marker_width = 0
        while self.bmp.get(x + glyph_marker_width, y, 0) == Marker.GLYPH:
            glyph_marker_width += 1
        if glyph_marker_width <= 0:
            raise ValueError("Glyph marker not found")

        # Find negative offset marker
        negative_offset = 0
        while self.bmp.get(x - negative_offset - 1, y, 0) == Marker.SPACING:
            negative_offset += 1

        # Find advance marker
        x_advance = 0
        while self.bmp.get(x + x_advance, y + 1, 0) == Marker.SPACING:
            x_advance += 1
        if x_advance <= 0:
            x_advance = None

        # Extract Glyph Bitmap
        glyph_height = self.max_glyph_height()
        bmp = self.bmp.crop(
            x - negative_offset,
            y - glyph_height,
            negative_offset + glyph_marker_width,
            glyph_height,
        )

        return RawGlyph(code, bmp, negative_offset, x_advance)

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
            builder.add_glyph(
                glyph.code,
                glyph.bmp,
                x_offset=-glyph.negative_offset,
                y_offset=-(self.cap_height + self.ascender_spacing),
                x_advance=glyph.explicit_advance,
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
            self.max_glyph_height(),
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
