"""Command line interface: `shapofont <command>`."""

from __future__ import annotations

import argparse
import sys
from os import path

from . import repo


def cmd_convert(args: argparse.Namespace) -> None:
    from .font import BitmapFont
    from .gfxfont import generate_gfxfont
    from .lvgl import generate_lvgl_font

    font = BitmapFont(args.input)
    if args.gfx_outdir:
        with open(path.join(args.gfx_outdir, f"{font.full_name}.h"), "w") as f:
            f.write(generate_gfxfont(font))
    if args.lvgl_outdir:
        with open(path.join(args.lvgl_outdir, f"{font.full_name}.c"), "w") as f:
            f.write(generate_lvgl_font(font))
    if args.sample_img:
        font.generate_sample_image(args.sample_img)


def cmd_configure(args: argparse.Namespace) -> None:
    from .configure import write_batch_makefile

    write_batch_makefile(args.design_dir, args.output)


def cmd_catalog(args: argparse.Namespace) -> None:
    from .catalog import update_readme

    update_readme(args.readme, args.design_dir)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="shapofont", description="Bitmap font tools for embedded projects.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("convert", help="convert a font design directory to font sources and a sample image")
    p.add_argument("-i", "--input", required=True, metavar="DIR", help="font design directory (<Family>_<dimensions>)")
    p.add_argument("--gfx-outdir", metavar="DIR", help="write a GFXfont header (<name>.h) into this directory")
    p.add_argument("--lvgl-outdir", metavar="DIR", help="write an LVGL font source (<name>.c) into this directory")
    p.add_argument("--sample-img", metavar="FILE", help="write a sample PNG image to this path")
    p.set_defaults(func=cmd_convert)

    p = sub.add_parser("configure", help=f"regenerate {repo.BATCH_MAKEFILE} from the design directory")
    p.add_argument("--design-dir", default=repo.DESIGN_DIR)
    p.add_argument("-o", "--output", default=repo.BATCH_MAKEFILE)
    p.set_defaults(func=cmd_configure)

    p = sub.add_parser("catalog", help=f"regenerate the font catalog in {repo.README}")
    p.add_argument("--design-dir", default=repo.DESIGN_DIR)
    p.add_argument("--readme", default=repo.README)
    p.set_defaults(func=cmd_catalog)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    try:
        args.func(args)
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
