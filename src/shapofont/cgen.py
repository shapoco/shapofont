"""Helpers shared by the C source generators."""

from __future__ import annotations


def format_byte_array(data: list[int], indent: str = "  ", cols: int = 16) -> str:
    lines = []
    for i in range(0, len(data), cols):
        lines.append(indent + " ".join(f"0x{b:02X}," for b in data[i : i + cols]))
    return "\n".join(lines) + ("\n" if lines else "")


def footprint_comment(items: list[tuple[str, int, bool]], num_glyphs: int, prefix: str = "//") -> str:
    """Render an "Estimated Foot Print" block.

    `items` is a list of (label, bytes, show_per_glyph). A "Total" line is appended;
    the catalog generator reads the total from that line.
    """
    label_width = max(len(label) for label, _, _ in items + [("Total", 0, True)])
    lines = [f"{prefix}   Estimated Foot Print:"]
    total = 0
    for label, size, per_glyph in items:
        total += size
        lines.append(f"{prefix}     {label:<{label_width}} : {size:5d} Bytes" + (f" ({size / num_glyphs:6.2f} Bytes/glyph)" if per_glyph else ""))
    lines.append(f"{prefix}     {'Total':<{label_width}} : {total:5d} Bytes ({total / num_glyphs:6.2f} Bytes/glyph)")
    return "\n".join(lines) + "\n"


def c_char_comment(code: int) -> str:
    """A comment like `/* U+0041 "A" */` for a code point."""
    if 0x20 <= code < 0x7F:
        ch = chr(code)
        if ch in '"\\':
            ch = "\\" + ch
        return f'/* U+{code:04X} "{ch}" */'
    return f"/* U+{code:04X} */"
