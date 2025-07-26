from design import GrayBitmap

WORD_SIZE = 2
LIB_NAME = "ShapoFont"
VERBOSE = True


def align_to_word_size(size: int) -> int:
    return (size + WORD_SIZE - 1) // WORD_SIZE * WORD_SIZE


class GFXglyph:
    STRUCT_SIZE = align_to_word_size(2 + 1 + 1 + 1 + 1 + 1)

    def __init__(
        self,
        bitmap_offset: int,
        width: int,
        height: int,
        x_advance: int,
        x_offset: int,
        y_offset: int,
        orig_bmp_width: int,
        orig_bmp_height: int,
    ):
        self.bitmap_offset = bitmap_offset  # uint16_t
        self.width = width  # uint8_t
        self.height = height  # uint8_t
        self.x_advance = x_advance  # uint8_t
        self.x_offset = x_offset  # uint8_t
        self.y_offset = y_offset  # uint8_t

        # for statistics
        self.orig_bmp_width = orig_bmp_width
        self.orig_bmp_height = orig_bmp_height

    def generate_struct_initializer(self) -> str:
        return f"{{ 0x{self.bitmap_offset:04X}, {self.width:2d}, {self.height:2d}, {self.x_advance:2d}, {self.x_offset:2d}, {self.y_offset:3d} }}"


class GFXfont:
    STRUCT_SIZE = align_to_word_size(2 + 2 + 2 + 2 + 1)

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
        self.bitmap = bitmap  # uint8_t *
        self.glyphs = glyphs  # GFXglyph *
        self.first = first  # uint16_t
        self.last = last  # uint16_t
        self.y_advance = y_advance  # uint8_t

    def generate_header(self) -> str:
        num_glyphs = len(self.glyphs)

        original_bmp_pixels = 0
        shrinked_bmp_pixels = 0
        for glyph in self.glyphs:
            original_bmp_pixels += glyph.orig_bmp_width * glyph.orig_bmp_height
            shrinked_bmp_pixels += glyph.width * glyph.height

        bitmap_array_size = len(self.bitmap)
        bitmap_size_per_glyph = bitmap_array_size / num_glyphs
        glyph_table_size = num_glyphs * GFXglyph.STRUCT_SIZE
        glyph_table_size_per_glyph = glyph_table_size / num_glyphs
        total_size = bitmap_array_size + glyph_table_size + GFXfont.STRUCT_SIZE
        total_size_per_glyph = total_size / num_glyphs
        
        pixels_per_byte = original_bmp_pixels / total_size if total_size > 0 else 0

        code = "#pragma once\n"
        code += "\n"
        code += "// Generated from ShapoFont\n"
        code += "//   Pixel Count:\n"
        code += f"//     Effective: {original_bmp_pixels:5d} px\n"
        code += f"//     Shrinked : {shrinked_bmp_pixels:5d} px\n"
        code += "//   Estimated Foot Print:\n"
        code += f"//     Bitmap Data    : {bitmap_array_size:5d} Bytes ({bitmap_size_per_glyph:6.2f} Bytes/glyph)\n"
        code += f"//     Glyph Table    : {glyph_table_size:5d} Bytes ({glyph_table_size_per_glyph:6.2f} Bytes/glyph)\n"
        code += f"//     GFXfont Struct : {GFXfont.STRUCT_SIZE:5d} Bytes\n"
        code += f"//     Total          : {total_size:5d} Bytes ({total_size_per_glyph:6.2f} Bytes/glyph)\n"
        code += f"//   Memory Efficiency: {pixels_per_byte:6.3f} px/Byte\n"
        code += "\n"
        code += "#include <stdint.h>\n"
        code += "\n"
        code += "#ifdef SHAPOFONT_GFXFONT_INCLUDE_HEADER\n"
        code += "#include <gfxfont.h>\n"
        code += "#endif\n"
        code += "\n"
        code += "#ifndef SHAPOFONT_GFXFONT_NAMESPACE\n"
        code += "#define SHAPOFONT_GFXFONT_NAMESPACE\n"
        code += "#endif\n"
        code += "\n"
        code += "#ifndef PROGMEM\n"
        code += "#define PROGMEM\n"
        code += "#endif\n"
        code += "\n"
        code += f"const uint8_t {self.name}Bitmaps[] PROGMEM = {{\n"
        cols = 16
        for i, b in enumerate(self.bitmap):
            if i % cols == 0:
                code += "  "
            code += f"0x{b:02X},"
            if (i + 1) % cols == 0 or (i + 1) == len(self.bitmap):
                code += "\n"
            else:
                code += " "
        code += "};\n\n"

        code += f"const SHAPOFONT_GFXFONT_NAMESPACE GFXglyph {self.name}Glyphs[] PROGMEM = {{\n"
        for glyph in self.glyphs:
            code += f"  {glyph.generate_struct_initializer()},\n"
        code += "};\n\n"

        code += f"const SHAPOFONT_GFXFONT_NAMESPACE GFXfont {self.name} PROGMEM = {{\n"
        code += f"  (uint8_t*){self.name}Bitmaps,\n"
        code += f"  (GFXglyph*){self.name}Glyphs,\n"
        code += f"  0x{self.first:02X},\n"
        code += f"  0x{self.last:02X},\n"
        code += f"  {self.y_advance}\n"
        code += "};\n"

        return code


class GFXfontBuilder:
    def __init__(self, name: str, y_advance: int, normal_x_spacing: int):
        self.name = name
        self.y_advance = y_advance
        self.normal_x_spacing = normal_x_spacing
        self.bitmaps: dict[int, list[int]] = {}
        self.glyphs: dict[int, GFXglyph] = {}

    def add_glyph(
        self,
        code: int,
        bmp: GrayBitmap,
        y_offset: int,
    ):
        # Cropping
        x_min = bmp.width
        x_max = -1
        y_min = bmp.height
        y_max = -1
        for y in range(bmp.height):
            for x in range(bmp.width):
                col = bmp.get(x, y)
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
                col = bmp.get(x + x_min, y + y_min)
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
            x_advance=bmp.width + self.normal_x_spacing,
            x_offset=x_min,
            y_offset=y_offset + y_min,
            orig_bmp_width=bmp.width,
            orig_bmp_height=bmp.height,
        )

        self.bitmaps[code] = packed_bmp
        self.glyphs[code] = glyph

    def build(self) -> GFXfont:
        codes = sorted(self.bitmaps.keys())
        code_first = codes[0]
        code_last = codes[-1]

        glyphs: list[GFXglyph] = []

        if VERBOSE:
            print(f"[{LIB_NAME}] Generating bitmap array...")

        bitmap: list[int] = []
        for code in range(code_first, code_last + 1):
            if code in self.bitmaps:
                glyph = self.glyphs[code]
                glyph.bitmap_offset = len(bitmap)
                bitmap += self.bitmaps[code]
            else:
                glyph = GFXglyph(
                    bitmap_offset=0,
                    width=0,
                    height=0,
                    x_advance=0,
                    x_offset=0,
                    y_offset=0,
                    orig_bmp_width=0,
                    orig_bmp_height=0,
                )
            glyphs.append(glyph)

        # Find duplicated byte sequences
        if VERBOSE:
            print(f"[{LIB_NAME}] Optimizing bitmap array...")
        total_bytes_deleted = 0
        deleted_codes = []
        for i_trial in range(10):
            print(f"  Trial #{i_trial + 1}:")
            num_deleted = 0
            for code in range(code_first, code_last + 1):
                if code in deleted_codes:
                    continue

                if code not in self.glyphs or code not in self.bitmaps:
                    continue
                size = len(self.bitmaps[code])

                if size <= 0:
                    continue

                glyph = self.glyphs[code]
                orig_offset = glyph.bitmap_offset

                new_offset = -1
                for i in range(0, orig_offset - size):
                    if bitmap[i : i + size] == bitmap[orig_offset : orig_offset + size]:
                        new_offset = i
                        break

                if new_offset < 0:
                    for i in range(orig_offset + size, len(bitmap) - size):
                        found_bytes = bitmap[i : i + size]
                        orig_bytes = bitmap[orig_offset : orig_offset + size]
                        if found_bytes == orig_bytes:
                            new_offset = i
                            break

                if new_offset < 0:
                    continue

                perfect_referers = []
                partial_referers = []
                for ref_code in range(code_first, code_last + 1):
                    if ref_code == code:
                        continue

                    if ref_code not in self.glyphs or ref_code not in self.bitmaps:
                        continue

                    ref_glyph = self.glyphs[ref_code]
                    if len(self.bitmaps[ref_code]) <= 0:
                        continue

                    ref_offset = ref_glyph.bitmap_offset
                    ref_size = len(self.bitmaps[ref_code])

                    overlapped = (
                        ref_offset < orig_offset + size
                        and orig_offset < ref_offset + ref_size
                    )
                    included = (
                        orig_offset <= ref_offset
                        and ref_offset + ref_size <= orig_offset + size
                    )

                    if included:
                        perfect_referers.append(ref_code)
                    elif overlapped:
                        partial_referers.append(ref_code)

                print(
                    f"    Duplication found: code=0x{code:02X}, offset={orig_offset}-->{new_offset}, size={ref_size}."
                )

                if len(partial_referers) > 0:
                    print(
                        f"      But this bitmap is area referenced by {len(partial_referers)} others. Skipping..."
                    )
                    continue
                
                # Update offset
                glyph.bitmap_offset = new_offset

                # Update referers
                for ref_code in perfect_referers:
                    ref_glyph = self.glyphs[ref_code]
                    ref_old_offset = ref_glyph.bitmap_offset
                    ref_new_offset = ref_old_offset + (new_offset - orig_offset)
                    ref_glyph.bitmap_offset = ref_new_offset
                    if VERBOSE:
                        print(
                            f"      Referer is also updated: code=0x{ref_code:02X}, offset={ref_old_offset}-->{ref_new_offset}."
                        )

                # Delete bitmap block
                bitmap = bitmap[:orig_offset] + bitmap[orig_offset + size :]
                
                # Update offsets of following glyphs
                for ref_code in range(code_first, code_last + 1):
                    if ref_code not in self.glyphs or ref_code not in self.bitmaps:
                        continue

                    ref_glyph = self.glyphs[ref_code]
                    if len(self.bitmaps[ref_code]) <= 0:
                        continue

                    if ref_glyph.bitmap_offset >= orig_offset + size:
                        ref_glyph.bitmap_offset -= size
                    elif ref_glyph.bitmap_offset >= orig_offset:
                        raise RuntimeError()

                deleted_codes.append(code)
                total_bytes_deleted += size
                num_deleted += 1

            if num_deleted == 0:
                if VERBOSE and i_trial > 0:
                    print(f"    No more duplications found.")
                break

        if VERBOSE:
            if total_bytes_deleted > 0:
                print(
                    f"  Totally {len(deleted_codes)} chars, {total_bytes_deleted} bytes duplications are deleted."
                )
            else:
                print(f"  No duplications found.")

        return GFXfont(
            name=self.name,
            bitmap=bitmap,
            glyphs=glyphs,
            first=code_first,
            last=code_last,
            y_advance=self.y_advance,
        )
