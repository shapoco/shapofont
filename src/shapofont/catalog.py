"""Regenerates the font catalog section of README.md."""

from __future__ import annotations

import os
import re
import sys
from glob import glob
from os import path

from . import repo

START_MARKER = "<!-- SHAPOFONT_START_OF_FONT_CATALOG -->\n"
END_MARKER = "<!-- SHAPOFONT_END_OF_FONT_CATALOG -->\n"
RE_TOTAL = re.compile(r"Total\s*:\s*(\d+)\s+Bytes")


def read_footprint(src_path: str) -> int | None:
    """Read the estimated total footprint from a generated font source's header comment."""
    try:
        with open(src_path, "r") as f:
            for line in f:
                m = RE_TOTAL.search(line)
                if m:
                    return int(m.group(1))
    except FileNotFoundError:
        pass
    print(f"Warning: could not read footprint from {src_path}", file=sys.stderr)
    return None


def format_size(size: int | None) -> str:
    if size is None:
        return "?"
    return f"{size} B" if size < 1024 else f"{size / 1024:.2f} kB"


def family_catalog(family_name: str, description: str, design_dir: str) -> str:
    design_files = sorted(glob(path.join(design_dir, f"{family_name}_*", "design.png")))
    out = f"\n## {family_name}\n\n{description}\n\n"
    out += "|Sample|Downloads (Footprint)|\n|:--|:--|\n"
    for design_file in design_files:
        name = path.basename(path.dirname(design_file))
        dim_id = name[len(family_name) + 1 :]
        thumb = f'<a href="{repo.sim_url(name)}" target="_blank"><img src="{repo.sample_image_path(name)}" style="width: 250px;"></a>'

        links = [f"**{dim_id}**"]
        gfx_header = repo.gfx_header_path(name)
        if gfx_header:
            links.append(f"[GFXfont]({gfx_header}) ({format_size(read_footprint(gfx_header))})")
        else:
            links.append("(GFXfont not available: grayscale)")
        lvgl_source = repo.lvgl_source_path(name)
        links.append(f"[LVGL]({lvgl_source}) ({format_size(read_footprint(lvgl_source))})")
        out += f"|{thumb}|{'<br>'.join(links)}|\n"
    return out + "\n"


def generate_catalog(design_dir: str = repo.DESIGN_DIR) -> str:
    return "".join(family_catalog(family, desc, design_dir) for family, desc in repo.FAMILIES)


def update_readme(readme_path: str = repo.README, design_dir: str = repo.DESIGN_DIR) -> None:
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
    start = content.find(START_MARKER)
    end = content.find(END_MARKER)
    if start < 0 or end < 0:
        raise ValueError(f"Catalog markers not found in {readme_path}")
    start += len(START_MARKER)

    new_content = content[:start] + generate_catalog(design_dir) + content[end:]
    tmp_path = readme_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    os.replace(tmp_path, readme_path)
