#!/usr/bin/env python3

from PIL import Image
import json5
from os import path
import re
import math
import argparse
import gfxfont


class Marker:
    VALID_BOTTOM_LINE = -1
    DISABLED_BOTTOM_LINE = -2

class Bitmap:

    def __init__(self, data: list[int], w: int, h: int, offset: int, stride: int):
        self.data = data
        self.width = w
        self.height = h
        self.offset = offset
        self.stride = stride

    def from_file(file_path: str):
        pil_img = Image.open(file_path)
        w, h = pil_img.size
        data: list[int] = []
        for y in range(h):
            for x in range(w):
                (r, g, b, a) = pil_img.getpixel((x, y))
                if r > 192 and g < 64 and b < 64:
                    data.append(Marker.VALID_BOTTOM_LINE)
                elif r < 64 and g < 64 and b > 192:
                    data.append(Marker.DISABLED_BOTTOM_LINE)
                else:
                    gray = (r + g + b) // 3
                    data.append(gray)
                    
        pil_img.close()

        return Bitmap(data, w, h, 0, w)

    def get(self, x: int, y: int) -> Marker:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise IndexError(f"Index out of bounds: ({x}, {y})")
        return self.data[self.offset + y * self.stride + x]

    def crop(self, x: int, y: int, width: int, height: int):
        if x < 0 or y < 0 or x + width > self.width or y + height > self.height:
            raise IndexError("Crop dimensions out of bounds")
        return Bitmap(
            self.data, width, height, self.offset + y * self.stride + x, self.stride
        )


class BitmapGlyph:
    def __init__(self, code: int, bmp: Bitmap):
        self.code = code
        self.img = bmp


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
            raise ValueError(f"Missing 's' option in directory name: '{self.dim_identifier}'")
        self.type_size = dic["s"]
        self.cap_height = dic.get("c", self.type_size)
        self.weight = dic.get("w", 1)
        self.line_height = dic.get("h", math.ceil(self.type_size * 1.2))
        self.ascender_spacing = dic.get("a", 0)
        self.normal_x_spacing = dic.get(
            "p", 1 + math.floor(self.type_size / 12)
        )

        # Load the image
        self.bmp = Bitmap.from_file(path.join(dir_path, "design.png"))

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
                    start_code = int(code_range['from'])
                    end_code = int(code_range['to'])
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
                if col == Marker.VALID_BOTTOM_LINE or col == Marker.DISABLED_BOTTOM_LINE:
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
        return self.type_size + self.ascender_spacing

    def to_gfx_font(self, outdir: str):
        builder = gfxfont.GFXfontBuilder(
            self.full_name,
            self.line_height,
            self.normal_x_spacing,
        )
        for glyph in self.glyphs:
            bmp = glyph.img
            builder.add_glyph(
                glyph.code,
                bmp.width,
                bmp.height,
                bmp.data,
                bmp_offset=bmp.offset,
                bmp_stride=bmp.stride,
                y_offset=-self.bitmap_height(),
            )
        gfx_font = builder.build()
        with open(path.join(outdir, f"{self.full_name}.h"), "w") as f:
            f.write(gfx_font.generate_header())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("--outdir_gfx", required=True)
    args = parser.parse_args()

    font = BitmapFont(args.input)
    if args.outdir_gfx:
        font.to_gfx_font(args.outdir_gfx)


if __name__ == "__main__":
    main()
