#!/usr/bin/env python3

import os
import re

MAME_ARCH_LIST = ["HL", "HM", "VL", "VM"]
MAME_ARCH_VAR = "$(ARCH)"

BMP_DIR = "bitmap"
GFX_C_OUT_DIR = os.path.join("gfxfont", "cpp", "include")
MAME_HPP_OUT_DIR = os.path.join("mamefont", "cpp", MAME_ARCH_VAR, "include")
MAME_CPP_OUT_DIR = os.path.join("mamefont", "cpp", MAME_ARCH_VAR, "src")
MAME_JSON_OUT_DIR = os.path.join("mamefont", "json", MAME_ARCH_VAR)

KEY_DIM_DIR = "design_dir"
KEY_DIM_BMP = "design_bmp"
KEY_DIM_JSON = "design_json"
KEY_GFX_HEADER = "gfx_header"
KEY_MAME_HPP = "mame_hpp"
KEY_MAME_CPP = "mame_cpp"
KEY_MAME_JSON = "mame_json"

families: dict[str, dict[str, dict[str, str]]] = {}

# Listup all font designs
for family in os.listdir(BMP_DIR):
    if not os.path.isdir(os.path.join("bitmap", family)):
        continue

    family_dir = os.path.join("bitmap", family)
    families[family] = {}

    for dim in os.listdir(family_dir):
        dim_dir = os.path.join(family_dir, dim)
        bmp_path = os.path.join(dim_dir, "design.png")
        if not os.path.exists(bmp_path):
            continue

        families[family][dim] = {
            KEY_DIM_DIR: dim_dir,
            KEY_DIM_BMP: os.path.join(dim_dir, "design.png"),
            KEY_DIM_JSON: os.path.join(dim_dir, "shapofont.json5"),
            KEY_GFX_HEADER: os.path.join(GFX_C_OUT_DIR, f"{family}_{dim}.h"),
            KEY_MAME_HPP: os.path.join(MAME_HPP_OUT_DIR, f"{family}_{dim}.hpp"),
            KEY_MAME_CPP: os.path.join(MAME_CPP_OUT_DIR, f"{family}_{dim}.cpp"),
            KEY_MAME_JSON: os.path.join(MAME_JSON_OUT_DIR, f"{family}_{dim}.json"),
        }

all_fonts = []
for family, dims in families.items():
    for dim, info in dims.items():
        all_fonts.append(info)

# Sort fonts by size of bitmap for optimize batch processing
all_fonts = sorted(
    all_fonts, key=lambda x: os.path.getsize(x[KEY_DIM_BMP]), reverse=True
)

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
    for info in all_fonts:
        f.write(f" \\\n\t{info[KEY_GFX_HEADER]}")
    f.write("\n\n")

    for arch in MAME_ARCH_LIST:
        f.write(f"MAME_{arch}_HPP_LIST =")
        for info in all_fonts:
            hpp_path = info[KEY_MAME_HPP].replace(MAME_ARCH_VAR, arch)
            f.write(f" \\\n\t{hpp_path}")
        f.write("\n\n")
        f.write(f"MAME_{arch}_CPP_LIST =")
        for info in all_fonts:
            cpp_path = info[KEY_MAME_CPP].replace(MAME_ARCH_VAR, arch)
            f.write(f" \\\n\t{cpp_path}")
        f.write("\n\n")
        f.write(f"MAME_{arch}_JSON_LIST =")
        for info in all_fonts:
            json_path = info[KEY_MAME_JSON].replace(MAME_ARCH_VAR, arch)
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

    for info in all_fonts:
        # GFXfont
        dependencies = [
            info[KEY_DIM_BMP],
            info[KEY_DIM_JSON],
            "$(GFXFONT_PY)",
            "$(COMMON_DEPENDENCIES)",
        ]
        f.write(f"{info[KEY_GFX_HEADER]}: {' '.join(dependencies)}\n")
        f.write(f"\t@mkdir -p $(dir $@)\n")
        f.write(f"\t$(CMD_PYTHON) $(SHAPOFONT_PY)")
        f.write(f" --outdir_gfx_c $(dir $@)")
        f.write(f" -i {info[KEY_DIM_DIR]}\n")
        f.write("\n")

        # MameFont (C++)
        for arch in MAME_ARCH_LIST:
            hpp_path = info[KEY_MAME_HPP].replace(MAME_ARCH_VAR, arch)
            cpp_path = info[KEY_MAME_CPP].replace(MAME_ARCH_VAR, arch)
            outdir_hpp = os.path.dirname(hpp_path)
            dependencies = [
                info[KEY_DIM_BMP],
                info[KEY_DIM_JSON],
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
            f.write(f" -i {info[KEY_DIM_DIR]}\n")
            f.write("\n")

        # MameFont (JSON)
        for arch in MAME_ARCH_LIST:
            json_path = info[KEY_MAME_JSON].replace(MAME_ARCH_VAR, arch)
            dependencies = [
                info[KEY_DIM_BMP],
                info[KEY_DIM_JSON],
                "$(MAMEFONT_PY)",
                "$(COMMON_DEPENDENCIES)",
            ]
            f.write(f"{json_path}: {' '.join(dependencies)}\n")
            f.write(f"\t@mkdir -p $(dir $@)\n")
            f.write(f"\t$(CMD_PYTHON) $(SHAPOFONT_PY)")
            f.write(f" --mame_arch {arch}")
            f.write(f" --outdir_mame_json $(dir $@)")
            f.write(f" -i {info[KEY_DIM_DIR]}\n")
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
