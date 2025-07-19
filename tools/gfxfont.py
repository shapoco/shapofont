class GFXglyph:
    def __init__(
        self,
        bitmap_offset: int,
        width: int,
        height: int,
        x_advance: int,
        x_offset: int,
        y_offset: int,
    ):
        self.bitmap_offset = bitmap_offset
        self.width = width
        self.height = height
        self.x_advance = x_advance
        self.x_offset = x_offset
        self.y_offset = y_offset

    def generate_struct_initializer(self) -> str:
        return f"{{ {self.bitmap_offset}, {self.width}, {self.height}, {self.x_advance}, {self.x_offset}, {self.y_offset} }}"


class GFXfont:
    def __init__(
        self,
        name: str,
        bitmap: list[int],
        glyphs: list[GFXglyph],
        first: int,
        last: int,
        y_advance: int,
    ):
        self.name = name
        self.bitmap = bitmap
        self.glyphs = glyphs
        self.first = first
        self.last = last
        self.y_advance = y_advance

    def generate_header(self) -> str:
        header = "#pragma once\n\n"
        header += "#include <stdint.h>\n"
        header += "\n"
        header += "#ifdef SHAPOFONT_GFXFONT_INCLUDE_HEADER\n"
        header += "#include <gfxfont.h>\n"
        header += "#endif\n"
        header += "\n"
        header += "#ifndef SHAPOFONT_GFXFONT_NAMESPACE\n"
        header += "#define SHAPOFONT_GFXFONT_NAMESPACE\n"
        header += "#endif\n"
        header += "\n"
        header += "#ifndef PROGMEM\n"
        header += "#define PROGMEM\n"
        header += "#endif\n"
        header += "\n"
        header += f"const uint8_t {self.name}Bitmaps[] PROGMEM = {{\n"
        cols = 8
        for i, b in enumerate(self.bitmap):
            if i % cols == 0:
                header += "  "
            header += f"0x{b:02X},"
            if (i + 1) % cols == 0 or (i + 1) == len(self.bitmap):
                header += "\n"
            else:
                header += " "
        header += "};\n\n"

        header += f"const SHAPOFONT_GFXFONT_NAMESPACE GFXglyph {self.name}Glyphs[] PROGMEM = {{\n"
        for glyph in self.glyphs:
            header += f"  {glyph.generate_struct_initializer()},\n"
        header += "};\n\n"

        header += (
            f"const SHAPOFONT_GFXFONT_NAMESPACE GFXfont {self.name} PROGMEM = {{\n"
        )
        header += f"  (uint8_t*){self.name}Bitmaps,\n"
        header += f"  (GFXglyph*){self.name}Glyphs,\n"
        header += f"  0x{self.first:02X},\n"
        header += f"  0x{self.last:02X},\n"
        header += f"  {self.y_advance}\n"
        header += "};\n"

        return header


class GFXfontBuilder:
    def __init__(self, name: str, x_spacing: int, y_advance: int):
        self.name = name
        self.bitmaps: dict[int, list[int]] = {}
        self.glyphs: dict[int, GFXglyph] = {}
        self.x_spacing = x_spacing
        self.y_advance = y_advance

    def add_glyph(
        self,
        code: int,
        bmp_width: int,
        bmp_height: int,
        bitmap: list[int],
        bmp_offset: int = 0,
        bmp_stride: int = 0,
        y_offset: int = 0,
    ):
        if bmp_stride == 0:
            bmp_stride = bmp_width

        # Cropping
        x_min = bmp_width
        x_max = -1
        y_min = bmp_height
        y_max = -1
        for y in range(bmp_height):
            for x in range(bmp_width):
                col = bitmap[bmp_offset + y * bmp_stride + x]
                if col >= 128:
                    x_min = min(x, x_min)
                    x_max = max(x, x_max)
                    y_min = min(y, y_min)
                    y_max = max(y, y_max)

        type_w = x_max - x_min + 1
        type_h = y_max - y_min + 1
        if type_w <= 0 or type_h <= 0:
            type_w = 0
            type_h = 0

        # Pack bitmap into bytes
        packed_bmp: list[int] = []
        byte = 0
        i_bit = 7
        for y in range(type_h):
            for x in range(type_w):
                col = bitmap[bmp_offset + (y + y_min) * bmp_stride + (x + x_min)]
                if col >= 128:
                    byte |= 1 << i_bit
                if i_bit == 0 or (y == type_h - 1 and x == type_w - 1):
                    packed_bmp.append(byte)
                    byte = 0
                    i_bit = 7
                else:
                    i_bit -= 1

        glyph = GFXglyph(
            bitmap_offset=0,
            width=type_w,
            height=type_h,
            x_advance=bmp_width + self.x_spacing,
            x_offset=x_min,
            y_offset=y_offset + y_min,
        )

        self.bitmaps[code] = packed_bmp
        self.glyphs[code] = glyph

    def build(self) -> GFXfont:
        codes = sorted(self.bitmaps.keys())
        code_first = codes[0]
        code_last = code_first + len(codes) - 1

        glyphs: list[GFXglyph] = []

        bitmap: list[int] = []
        for code in range(code_first, code_last + 1):
            if code in self.bitmaps:
                glyph = self.glyphs[code]
                glyph.bitmap_offset = len(bitmap)
                bitmap.extend(self.bitmaps[code])
            else:
                glyph = GFXglyph(
                    bitmap_offset=0,
                    width=0,
                    height=0,
                    x_advance=0,
                    x_offset=0,
                    y_offset=0,
                )
            glyphs.append(glyph)

        return GFXfont(
            name=self.name,
            bitmap=bitmap,
            glyphs=glyphs,
            first=code_first,
            last=code_last,
            y_advance=self.y_advance,
        )
