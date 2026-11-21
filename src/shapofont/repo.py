"""Layout of the ShapoFont repository (used by the `configure` and `catalog` commands)."""

from os import path

DESIGN_DIR = "design"
GFX_OUT_DIR = path.join("gfxfont", "cpp", "include")
LVGL_OUT_DIR = "lvgl"
SAMPLE_OUT_DIR = path.join("img", "sample")
BATCH_MAKEFILE = "Makefile.batch.mk"
README = "README.md"

SIM_URL = "https://shapoco.github.io/shapofont/sim/"

# Font families shown in the README catalog, in display order
FAMILIES: list[tuple[str, str]] = [
    ("ShapoSansP", "Proportional fonts for embedded projects"),
    ("ShapoSansDigitP", "Proportional number fonts for embedded projects"),
    ("ShapoSansMono", "Monospaced fonts for embedded projects"),
    ("ShapoSquareRoundP", "Proportional fonts for embedded projects"),
    ("MameSansP", "Proportional fonts"),
    ("MameSansDigitP", "Proportional number fonts"),
    ("MameSeg7", "7-segment display fonts"),
    ("MameSquareWide", "Square wide fonts"),
]


def bits_per_pixel_of(font_name: str) -> int:
    """Bits per pixel from the `g` option of a full font name (1 if absent)."""
    import re

    m = re.search(r"g(\d+)", font_name.rsplit("_", 1)[-1])
    return int(m.group(1)) if m else 1


def gfx_header_path(font_name: str) -> str | None:
    return path.join(GFX_OUT_DIR, f"{font_name}.h") if bits_per_pixel_of(font_name) == 1 else None


def lvgl_source_path(font_name: str) -> str:
    return path.join(LVGL_OUT_DIR, f"{font_name}.c")


def sample_image_path(font_name: str) -> str:
    return path.join(SAMPLE_OUT_DIR, f"{font_name}.png")


def sim_url(font_name: str) -> str:
    """URL that opens the font in the web simulator (GFXfont for 1 bpp, LVGL otherwise)."""
    if bits_per_pixel_of(font_name) == 1:
        return f"{SIM_URL}#u=/shapofont/{font_name}.h"
    return f"{SIM_URL}#u=/shapofont/lvgl/{font_name}.c"
