#!/usr/bin/env python3

import os
import re
import io
from os import path
from glob import glob

DESIGN_DIR = "design"
SAMPLE_IMAGE_DIR = path.join("img", "sample")
GFXFONT_HEADER_DIR = path.join("gfxfont", "cpp", "include")

ENC_LIST = ["HL", "HM", "VL", "VM"]


def get_gfx_size(src_path: str) -> int:
    with open(src_path, "r") as f:
        for line in f:
            if "Total" in line:
                match = re.search(
                    r"(\d+)\s+Bytes\s*\(\s*\d+(\.\d+)?\s*Bytes/glyph\s*\)", line
                )
                if match:
                    return int(match.group(1))
    print(f"Warning: Could not find total size in {src_path}")
    return 0


def get_mame_size(src_path: str) -> int:
    with open(src_path, "r") as f:
        for line in f:
            if "Total" in line:
                match = re.search(
                    r"(\d+)\s+Bytes\s*\(\s*\d+(\.\d+)?\s*Bytes/glyph\s*\)", line
                )
                if match:
                    return int(match.group(1))
    print(f"Warning: Could not find total size in {src_path}")
    return 0


def format_size(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    else:
        return f"{size / 1024:.2f} kB"


def make_family_catalog(f: io.TextIOWrapper, family_name: str, description: str):
    design_files = glob(path.join(DESIGN_DIR, f"{family_name}_*", "design.png"))
    design_files = sorted(design_files)
    f.write(f"\n")
    f.write(f"## {family_name}\n")
    f.write(f"\n")
    f.write(f"{description}\n")
    f.write(f"\n")
    f.write(f"|Sample|Downloads (Footprint)|\n")
    f.write(f"|:--|:--|\n")
    for design_file in design_files:
        design_name = path.basename(path.dirname(design_file))
        dim_id = re.sub(r"^" + family_name + r"_", "", design_name)

        mGray = re.search(r"g\d+", dim_id)
        is_gray = mGray and (int(mGray.group(0)[1:]) != 1)

        sample_url = path.join(SAMPLE_IMAGE_DIR, f"{design_name}.png")

        sim_url = None
        if not is_gray:
            sim_url = (
                f"https://shapoco.github.io/shapofont/sim/#u=/shapofont/{design_name}.h"
            )

        sample_thumb = f'<img src="{sample_url}" style="width: 250px;">'
        if sim_url:
            sample_link = f'<a href="{sim_url}" target="_blank">{sample_thumb}</a>'
        else:
            sample_link = f"{sample_thumb}<br>(Simulator not available)"

        gfx_url = None
        gfx_size = None
        gfx_link = "(GFXfont not available)"
        if not is_gray:
            gfx_url = path.join(GFXFONT_HEADER_DIR, f"{design_name}.h")
            gfx_size = get_gfx_size(gfx_url)
            gfx_link = f"[GFXfont]({gfx_url}) ({format_size(gfx_size)})"

        mame_url: dict[str, str] = {}
        mame_size: dict[str, int] = {}
        mame_link: dict[str, str] = {}
        for enc in ENC_LIST:
            mame_url[enc] = path.join(
                "mamefont", "cpp", enc, "include", f"{design_name}.hpp"
            )
            mame_size[enc] = get_mame_size(mame_url[enc])
            mame_link[enc] = (
                f"[MameFont-{enc}]({mame_url[enc]}) ({format_size(mame_size[enc])})"
            )
        mame_links = "<br>".join(mame_link.values())

        desc = f"**{dim_id}**"
        if gfx_link:
            desc += f"<br>{gfx_link}"
        if mame_link:
            desc += f"<br>{mame_links}"

        f.write(f"|{sample_link}|{desc}|\n")
    f.write(f"\n")


START_MARKER = "<!-- SHAPOFONT_START_OF_FONT_CATALOG -->\n"
END_MARKER = "<!-- SHAPOFONT_END_OF_FONT_CATALOG -->\n"

# README.md から、「<!-- SHAPOFONT_START_OF_FONT_CATALOG -->」より前の部分と「<!-- SHAPOFONT_END_OF_FONT_CATALOG -->」より後の部分を取得
with open("README.md", "r") as f:
    content = f.read()
    start_index = content.find(START_MARKER) + len(START_MARKER)
    end_index = content.find(END_MARKER)

    if start_index == -1 or end_index == -1:
        raise ValueError("Catalog markers not found in README.md")

    before_catalog = content[:start_index]
    after_catalog = content[end_index:]

with open("tmp.README.md", "w") as f:
    f.write(before_catalog)
    make_family_catalog(
        f,
        "ShapoSansP",
        "Proportional fonts for embedded projects",
    )
    make_family_catalog(
        f,
        "ShapoSansDigitP",
        "Proportional number fonts for embedded projects",
    )
    make_family_catalog(
        f,
        "ShapoSansMono",
        "Monospaced fonts for embedded projects",
    )
    make_family_catalog(
        f,
        "MameSansP",
        "Proportional fonts optimized for compression with MameFont",
    )
    make_family_catalog(
        f,
        "MameSansDigitP",
        "Proportional number fonts optimized for compression with MameFont",
    )
    make_family_catalog(
        f,
        "MameSeg7",
        "7-segment display fonts optimized for compression with MameFont",
    )
    make_family_catalog(
        f,
        "MameSquareWide",
        "Square wide fonts optimized for compression with MameFont",
    )
    f.write(after_catalog)

if path.exists("bak.README.md"):
    os.remove("bak.README.md")

try:
    os.rename("README.md", "bak.README.md")
    os.rename("tmp.README.md", "README.md")
except:
    os.rename("bak.README.md", "README.md")
    raise
