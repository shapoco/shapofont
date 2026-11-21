"""LVGL font (lv_font_fmt_txt, plain bitmap format) source generator.

The output follows the layout of lv_font_conv so that it works with LVGL v8
and v9. Glyph bitmaps are stored uncompressed, 1/2/4/8 bits per pixel,
packed MSB first with no padding between rows.
"""

from __future__ import annotations

from .cgen import c_char_comment, footprint_comment, format_byte_array
from .design import GrayBitmap
from .font import BitmapFont, RawGlyph

# Limits of lv_font_fmt_txt_glyph_dsc_t with LV_FONT_FMT_TXT_LARGE == 0
MAX_BITMAP_INDEX = (1 << 20) - 1
MAX_ADV_W = (1 << 12) - 1  # 1/16 px units
MAX_BOX_SIZE = 255

# Estimated struct sizes on a 32-bit target, for the footprint comment
GLYPH_DSC_SIZE = 8
CMAP_SIZE = 24
FONT_DSC_SIZE = 24
LV_FONT_SIZE = 32


class LvglGlyph:
    def __init__(self, code: int, bitmap: list[int], adv_w: int, box_w: int, box_h: int, ofs_x: int, ofs_y: int):
        self.code = code
        self.bitmap = bitmap
        self.bitmap_index = 0
        self.adv_w = adv_w  # 1/16 px
        self.box_w = box_w
        self.box_h = box_h
        self.ofs_x = ofs_x
        self.ofs_y = ofs_y  # bottom of the box, measured upward from the baseline

    def generate_struct_initializer(self) -> str:
        return (
            f"{{.bitmap_index = {self.bitmap_index}, .adv_w = {self.adv_w}, "
            f".box_w = {self.box_w}, .box_h = {self.box_h}, .ofs_x = {self.ofs_x}, .ofs_y = {self.ofs_y}}}"
        )


def pack_bitmap(bmp: GrayBitmap, x0: int, y0: int, w: int, h: int, bits_per_pixel: int) -> list[int]:
    """Pack a sub-rectangle as a continuous MSB-first stream of `bits_per_pixel`-bit values."""
    levels = (1 << bits_per_pixel) - 1
    packed: list[int] = []
    acc = 0
    n_bits = 0
    for y in range(h):
        for x in range(w):
            value = max(0, bmp.get(x0 + x, y0 + y))
            level = (value * levels + 127) // 255
            acc = (acc << bits_per_pixel) | level
            n_bits += bits_per_pixel
            if n_bits == 8:
                packed.append(acc)
                acc = 0
                n_bits = 0
    if n_bits > 0:
        packed.append(acc << (8 - n_bits))
    return packed


def contiguous_ranges(codes: list[int]) -> list[tuple[int, int]]:
    """Split sorted codes into (start, length) runs of consecutive values."""
    ranges: list[tuple[int, int]] = []
    for code in codes:
        if ranges and ranges[-1][0] + ranges[-1][1] == code:
            ranges[-1] = (ranges[-1][0], ranges[-1][1] + 1)
        else:
            ranges.append((code, 1))
    return ranges


def build_glyph(font: BitmapFont, glyph: RawGlyph) -> LvglGlyph:
    x_advance = font.x_advance_of(glyph)
    adv_w = x_advance * 16
    if not 0 <= adv_w <= MAX_ADV_W:
        raise ValueError(f"{font.full_name} U+{glyph.code:04X}: advance {x_advance} px out of range for LVGL.")

    box = glyph.bmp.bounding_box(threshold=1)
    if box is None:
        return LvglGlyph(glyph.code, [], adv_w, 0, 0, 0, 0)

    x_min, y_min, w, h = box
    if w > MAX_BOX_SIZE or h > MAX_BOX_SIZE:
        raise ValueError(f"{font.full_name} U+{glyph.code:04X}: glyph box {w}x{h} exceeds 255 px.")
    ofs_x = font.x_offset_of(glyph) + x_min
    ofs_y = font.baseline - (y_min + h)
    if not -128 <= ofs_x <= 127 or not -128 <= ofs_y <= 127:
        raise ValueError(f"{font.full_name} U+{glyph.code:04X}: glyph offset ({ofs_x}, {ofs_y}) out of int8 range.")
    bitmap = pack_bitmap(glyph.bmp, x_min, y_min, w, h, font.bits_per_pixel)
    return LvglGlyph(glyph.code, bitmap, adv_w, w, h, ofs_x, ofs_y)


def generate_lvgl_font(font: BitmapFont) -> str:
    """Generate an LVGL font C source for the font."""
    if font.bits_per_pixel not in (1, 2, 4, 8):
        raise ValueError(f"{font.full_name}: LVGL supports 1, 2, 4 or 8 bits per pixel (got {font.bits_per_pixel}).")
    if not font.glyphs:
        raise ValueError(f"{font.full_name}: font has no glyphs.")

    codes = sorted(font.glyphs)
    glyphs = [build_glyph(font, font.glyphs[code]) for code in codes]

    # Bitmap array; identical glyph bitmaps share one copy
    bitmap: list[int] = []
    bitmap_sections: list[tuple[int, str]] = []  # (offset, comment) for the source listing
    seen: dict[bytes, int] = {}
    for glyph in glyphs:
        key = bytes(glyph.bitmap)
        if glyph.bitmap and key in seen:
            glyph.bitmap_index = seen[key]
            continue
        glyph.bitmap_index = len(bitmap)
        if glyph.bitmap:
            seen[key] = glyph.bitmap_index
            bitmap_sections.append((glyph.bitmap_index, c_char_comment(glyph.code)))
            bitmap += glyph.bitmap
        if glyph.bitmap_index > MAX_BITMAP_INDEX:
            raise ValueError(f"{font.full_name}: bitmap data exceeds 1 MB.")

    # One FORMAT0_TINY cmap per run of consecutive codes. After each run an empty
    # padding glyph is inserted: LVGL v8 resolves the code just past a range to
    # glyph_id_start + range_length (off by one, fixed in v9), so the padding
    # keeps that lookup inside the table and renders nothing instead of a wrong glyph.
    cmaps = contiguous_ranges(codes)
    PADDING_GLYPH = "{.bitmap_index = 0, .adv_w = 0, .box_w = 0, .box_h = 0, .ofs_x = 0, .ofs_y = 0}"
    name = font.full_name
    guard = name.upper()
    num_glyphs = len(glyphs)
    effective_pixels = sum(g.bmp.width * g.bmp.height for g in font.glyphs.values())
    footprint_items = [
        ("Bitmap Data", len(bitmap), True),
        ("Glyph Table", (num_glyphs + 1 + len(cmaps)) * GLYPH_DSC_SIZE, True),
        ("Char Maps", len(cmaps) * CMAP_SIZE, False),
        ("Font Structs", FONT_DSC_SIZE + LV_FONT_SIZE, False),
    ]
    total_size = sum(size for _, size, _ in footprint_items)

    code = "/*\n"
    code += " * Generated by ShapoFont (https://github.com/shapoco/shapofont)\n"
    code += f" *   Font      : {name}\n"
    code += f" *   Bpp       : {font.bits_per_pixel}\n"
    code += f" *   Codes     : {len(codes)} glyphs, U+{codes[0]:04X}..U+{codes[-1]:04X}\n"
    code += f" *   Pixel Count: {effective_pixels} px (effective)\n"
    code += footprint_comment(footprint_items, num_glyphs, prefix=" *").replace(" *   Estimated Foot Print:", " *   Estimated Foot Print (32-bit target):")
    code += f" *   Memory Efficiency: {effective_pixels / total_size:6.3f} px/Byte\n"
    code += " */\n\n"
    code += "#ifdef LV_LVGL_H_INCLUDE_SIMPLE\n#include \"lvgl.h\"\n#else\n#include \"lvgl/lvgl.h\"\n#endif\n\n"
    code += f"#ifndef {guard}\n#define {guard} 1\n#endif\n\n"
    code += f"#if {guard}\n\n"

    code += "/*-----------------\n *    BITMAPS\n *----------------*/\n\n"
    code += "static LV_ATTRIBUTE_LARGE_CONST const uint8_t glyph_bitmap[] = {\n"
    if bitmap:
        for i, (offset, comment) in enumerate(bitmap_sections):
            end = bitmap_sections[i + 1][0] if i + 1 < len(bitmap_sections) else len(bitmap)
            code += f"    {comment}\n"
            code += format_byte_array(bitmap[offset:end], indent="    ")
            code += "\n"
    else:
        code += "    0x00, /* no glyph has pixels */\n"
    code += "};\n\n"

    code += "/*---------------------\n *  GLYPH DESCRIPTION\n *--------------------*/\n\n"
    code += "static const lv_font_fmt_txt_glyph_dsc_t glyph_dsc[] = {\n"
    code += f"    {PADDING_GLYPH}, /* id = 0 reserved */\n"
    glyph_iter = iter(glyphs)
    for start, length in cmaps:
        for _ in range(length):
            glyph = next(glyph_iter)
            code += f"    {glyph.generate_struct_initializer()}, {c_char_comment(glyph.code)}\n"
        code += f"    {PADDING_GLYPH}, /* padding after U+{start + length - 1:04X} (LVGL v8 off-by-one guard) */\n"
    code += "};\n\n"

    code += "/*---------------------\n *  CHARACTER MAPPING\n *--------------------*/\n\n"
    code += "static const lv_font_fmt_txt_cmap_t cmaps[] = {\n"
    glyph_id = 1
    for start, length in cmaps:
        code += "    {\n"
        code += f"        .range_start = {start}, .range_length = {length}, .glyph_id_start = {glyph_id},\n"
        code += "        .unicode_list = NULL, .glyph_id_ofs_list = NULL, .list_length = 0, .type = LV_FONT_FMT_TXT_CMAP_FORMAT0_TINY\n"
        code += "    },\n"
        glyph_id += length + 1  # +1 for the padding glyph
    code += "};\n\n"

    code += "/*--------------------\n *  ALL CUSTOM DATA\n *--------------------*/\n\n"
    code += "#if LVGL_VERSION_MAJOR == 8\n"
    code += "static lv_font_fmt_txt_glyph_cache_t cache;\n"
    code += "#endif\n\n"
    code += "static const lv_font_fmt_txt_dsc_t font_dsc = {\n"
    code += "    .glyph_bitmap = glyph_bitmap,\n"
    code += "    .glyph_dsc = glyph_dsc,\n"
    code += "    .cmaps = cmaps,\n"
    code += "    .kern_dsc = NULL,\n"
    code += "    .kern_scale = 0,\n"
    code += f"    .cmap_num = {len(cmaps)},\n"
    code += f"    .bpp = {font.bits_per_pixel},\n"
    code += "    .kern_classes = 0,\n"
    code += "    .bitmap_format = 0,\n"
    code += "#if LVGL_VERSION_MAJOR == 8\n"
    code += "    .cache = &cache,\n"
    code += "#endif\n"
    code += "};\n\n"

    code += "/*-----------------\n *  PUBLIC FONT\n *----------------*/\n\n"
    code += f"const lv_font_t {name} = {{\n"
    code += "    .get_glyph_dsc = lv_font_get_glyph_dsc_fmt_txt,\n"
    code += "    .get_glyph_bitmap = lv_font_get_bitmap_fmt_txt,\n"
    code += f"    .line_height = {font.line_height},\n"
    code += f"    .base_line = {font.descent + font.y_spacing},\n"
    code += "    .subpx = LV_FONT_SUBPX_NONE,\n"
    code += "    .underline_position = -1,\n"
    code += f"    .underline_thickness = {font.weight},\n"
    code += "    .dsc = &font_dsc,\n"
    code += "};\n\n"
    code += f"#endif /* #if {guard} */\n"
    return code
