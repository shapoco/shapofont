#!/usr/bin/env python3

import os
import re

MAME_ARCH_LIST = ["HL", "HM", "VL", "VM"]
MAME_ARCH_VAR = "$(ARCH)"

BMP_DIR = "design"
GFX_C_OUT_DIR = os.path.join("gfxfont", "cpp", "include")
MAME_HPP_OUT_DIR = os.path.join("mamefont", "cpp", MAME_ARCH_VAR, "include")
MAME_CPP_OUT_DIR = os.path.join("mamefont", "cpp", MAME_ARCH_VAR, "src")
MAME_JSON_OUT_DIR = os.path.join("mamefont", "json", MAME_ARCH_VAR)


class Font:
    def __init__(self):
        self.design_dir: str = ""
        self.design_bmp: str = ""
        self.design_json: str = ""
        self.gfx_header: str = ""
        self.mame_hpp: str = ""
        self.mame_cpp: str = ""
        self.mame_json: str = ""


all_fonts: list[Font] = []

# Listup all font designs
for font_name in os.listdir(BMP_DIR):
    dim_dir = os.path.join(BMP_DIR, font_name)
    bmp_path = os.path.join(dim_dir, "design.png")
    if not os.path.exists(bmp_path):
        continue

    font = Font()
    font.design_dir = dim_dir
    font.design_bmp = os.path.join(dim_dir, "design.png")
    font.design_json = os.path.join(dim_dir, "shapofont.json5")
    font.gfx_header = os.path.join(GFX_C_OUT_DIR, f"{font_name}.h")
    font.mame_hpp = os.path.join(MAME_HPP_OUT_DIR, f"{font_name}.hpp")
    font.mame_cpp = os.path.join(MAME_CPP_OUT_DIR, f"{font_name}.cpp")
    font.mame_json = os.path.join(MAME_JSON_OUT_DIR, f"{font_name}.json")
    all_fonts.append(font)

# Sort fonts by size of bitmap for optimize batch processing
all_fonts = sorted(all_fonts, key=lambda x: os.path.getsize(x.design_bmp), reverse=True)

with open("tmp.Makefile.batch.mk", "w") as f:
    f.write(".PHONY: gfx_all mame_all\n")
    f.write(f".PHONY: {' '.join(f'mame_{arch}' for arch in MAME_ARCH_LIST)}\n")
    f.write(f".PHONY: mame_cpp mame_json\n")
    f.write(".PHONY: distclean_all distclean_gfx_all distclean_mame_all\n")
    f.write(
        f".PHONY: {' '.join(f'distclean_mame_{arch}' for arch in MAME_ARCH_LIST)}\n"
    )
    f.write(f".PHONY: distclean_mame_cpp distclean_mame_json\n")
    f.write("\n")

    f.write("all: gfx_all mame_all\n")
    f.write("\n")

    f.write("GFX_HEADER_LIST =")
    for font in all_fonts:
        f.write(f" \\\n\t{font.gfx_header}")
    f.write("\n\n")

    for arch in MAME_ARCH_LIST:
        f.write(f"MAME_{arch}_HPP_LIST =")
        for font in all_fonts:
            hpp_path = font.mame_hpp.replace(MAME_ARCH_VAR, arch)
            f.write(f" \\\n\t{hpp_path}")
        f.write("\n\n")
        f.write(f"MAME_{arch}_CPP_LIST =")
        for font in all_fonts:
            cpp_path = font.mame_cpp.replace(MAME_ARCH_VAR, arch)
            f.write(f" \\\n\t{cpp_path}")
        f.write("\n\n")
        f.write(f"MAME_{arch}_JSON_LIST =")
        for font in all_fonts:
            json_path = font.mame_json.replace(MAME_ARCH_VAR, arch)
            f.write(f" \\\n\t{json_path}")
        f.write("\n\n")
    f.write("\n")

    f.write("gfx_all: $(GFX_HEADER_LIST)\n")
    f.write("\n")

    f.write(f"mame_all: {' '.join(f'mame_{arch}' for arch in MAME_ARCH_LIST)}\n")
    for arch in MAME_ARCH_LIST:
        f.write(f"mame_{arch}: $(MAME_{arch}_HPP_LIST) $(MAME_{arch}_JSON_LIST)\n")
    f.write(
        f"mame_cpp: {' '.join(f'$(MAME_{arch}_HPP_LIST)' for arch in MAME_ARCH_LIST)}\n"
    )
    f.write(
        f"mame_json: {' '.join(f'$(MAME_{arch}_JSON_LIST)' for arch in MAME_ARCH_LIST)}\n"
    )
    f.write("\n")

    for font in all_fonts:
        # GFXfont
        dependencies = [
            font.design_bmp,
            font.design_json,
            "$(GFXFONT_PY)",
            "$(COMMON_DEPENDENCIES)",
        ]
        f.write(f"{font.gfx_header}: {' '.join(dependencies)}\n")
        f.write(f"\t@mkdir -p $(dir $@)\n")
        f.write(f"\t$(CMD_PYTHON) $(SHAPOFONT_PY)")
        f.write(f" --outdir_gfx_c $(dir $@)")
        f.write(f" -i {font.design_dir}\n")
        f.write("\n")

        # MameFont (C++)
        for arch in MAME_ARCH_LIST:
            hpp_path = font.mame_hpp.replace(MAME_ARCH_VAR, arch)
            cpp_path = font.mame_cpp.replace(MAME_ARCH_VAR, arch)
            outdir_hpp = os.path.dirname(hpp_path)
            dependencies = [
                font.design_bmp,
                font.design_json,
                "$(MAMEFONT_PY)",
                "$(COMMON_DEPENDENCIES)",
            ]
            f.write(f"{hpp_path}: {cpp_path}\n")
            f.write(f"{cpp_path}: {' '.join(dependencies)}\n")
            f.write(f"\t@mkdir -p {outdir_hpp} $(dir $@)\n")
            f.write(f"\t$(CMD_PYTHON) $(SHAPOFONT_PY)")
            f.write(f" --mame_arch {arch}")
            f.write(f" --outdir_mame_hpp {outdir_hpp}")
            f.write(f" --outdir_mame_cpp $(dir $@)")
            f.write(f" -i {font.design_dir}\n")
            f.write("\n")

        # MameFont (JSON)
        for arch in MAME_ARCH_LIST:
            json_path = font.mame_json.replace(MAME_ARCH_VAR, arch)
            dependencies = [
                font.design_bmp,
                font.design_json,
                "$(MAMEFONT_PY)",
                "$(COMMON_DEPENDENCIES)",
            ]
            f.write(f"{json_path}: {' '.join(dependencies)}\n")
            f.write(f"\t@mkdir -p $(dir $@)\n")
            f.write(f"\t$(CMD_PYTHON) $(SHAPOFONT_PY)")
            f.write(f" --mame_arch {arch}")
            f.write(f" --outdir_mame_json $(dir $@)")
            f.write(f" -i {font.design_dir}\n")
            f.write("\n")

    f.write("distclean_all: distclean_gfx_all distclean_mame_all\n")
    f.write("\n")

    f.write("distclean_gfx_all:\n")
    f.write(f"\trm -rf {GFX_C_OUT_DIR}\n")
    f.write("\n")

    f.write(
        f"distclean_mame_all: {' '.join(f'distclean_mame_{arch}' for arch in MAME_ARCH_LIST)}\n"
    )
    for arch in MAME_ARCH_LIST:
        f.write(f"distclean_mame_{arch}:\n")
        f.write(f"\trm -rf {MAME_HPP_OUT_DIR.replace(MAME_ARCH_VAR, arch)}\n")
        f.write(f"\trm -rf {MAME_CPP_OUT_DIR.replace(MAME_ARCH_VAR, arch)}\n")
        f.write(f"\trm -rf {MAME_JSON_OUT_DIR.replace(MAME_ARCH_VAR, arch)}\n")
        f.write("\n")

    f.write("distclean_mame_cpp:\n")
    for arch in MAME_ARCH_LIST:
        f.write(f"\trm -rf {MAME_HPP_OUT_DIR.replace(MAME_ARCH_VAR, arch)}\n")
        f.write(f"\trm -rf {MAME_CPP_OUT_DIR.replace(MAME_ARCH_VAR, arch)}\n")
    f.write("\n")

    f.write("distclean_mame_json:\n")
    for arch in MAME_ARCH_LIST:
        f.write(f"\trm -rf {MAME_JSON_OUT_DIR.replace(MAME_ARCH_VAR, arch)}\n")
    f.write("\n")


os.remove("Makefile.batch.mk")
os.rename("tmp.Makefile.batch.mk", "Makefile.batch.mk")
