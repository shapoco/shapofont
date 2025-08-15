#!/usr/bin/env python3

import os
import re

MAME_ENC_LIST = ["HL", "HM", "VL", "VM"]
MAME_ARCH_VAR = "$(ARCH)"

BMP_DIR = "design"
GFX_C_OUT_DIR = os.path.join("gfxfont", "cpp", "include")
MAME_HPP_OUT_DIR = os.path.join("mamefont", "cpp", MAME_ARCH_VAR, "include")
MAME_JSON_OUT_DIR = os.path.join("mamefont", "json", MAME_ARCH_VAR)
SAMPLE_OUT_DIR = os.path.join("img", "sample")


class Font:
    def __init__(self):
        self.design_dir: str = ""
        self.design_bmp: str = ""
        self.design_json: str = ""
        self.gfx_header: str = ""
        self.mame_hpp: str = ""
        self.mame_json: str = ""


all_fonts: list[Font] = []

# Listup all font designs
for font_name in os.listdir(BMP_DIR):
    dim_id = font_name.split("_")[-1]
    mGray = re.search(r"g\d+", dim_id)
    is_gray = mGray and (int(mGray.group(0)[1:]) != 1)

    font_dir = os.path.join(BMP_DIR, font_name)
    bmp_path = os.path.join(font_dir, "design.png")
    if not os.path.exists(bmp_path):
        continue

    font = Font()
    font.design_dir = font_dir
    font.design_bmp = os.path.join(font_dir, "design.png")
    font.design_json = os.path.join(font_dir, "design.json")
    font.sample_png = os.path.join(SAMPLE_OUT_DIR, f"{font_name}.png")
    if is_gray:
        font.gfx_header = None
    else:
        font.gfx_header = os.path.join(GFX_C_OUT_DIR, f"{font_name}.h")
    font.mame_hpp = os.path.join(MAME_HPP_OUT_DIR, f"{font_name}.hpp")
    font.mame_json = os.path.join(MAME_JSON_OUT_DIR, f"{font_name}.json")
    all_fonts.append(font)

# Sort fonts by size of bitmap for optimize batch processing
all_fonts = sorted(all_fonts, key=lambda x: os.path.getsize(x.design_bmp), reverse=True)

with open("tmp.Makefile.batch.mk", "w") as f:
    f.write(".PHONY: gfx_all mame_all sample_all\n")
    f.write(f".PHONY: {' '.join(f'mame_{enc}' for enc in MAME_ENC_LIST)}\n")
    f.write(f".PHONY: mame_cpp mame_json\n")
    f.write(
        ".PHONY: distclean_all distclean_gfx_all distclean_mame_all distclean_sample_all\n"
    )
    f.write(f".PHONY: {' '.join(f'distclean_mame_{enc}' for enc in MAME_ENC_LIST)}\n")
    f.write(f".PHONY: distclean_mame_cpp distclean_mame_json\n")
    f.write("\n")

    f.write("all: gfx_all mame_all\n")
    f.write("\n")

    f.write("GFX_HEADER_LIST =")
    for font in all_fonts:
        if font.gfx_header:
            f.write(f" \\\n\t{font.gfx_header}")
    f.write("\n\n")

    for enc in MAME_ENC_LIST:
        f.write(f"MAME_{enc}_HPP_LIST =")
        for font in all_fonts:
            if font.mame_hpp:
                hpp_path = font.mame_hpp.replace(MAME_ARCH_VAR, enc)
            f.write(f" \\\n\t{hpp_path}")
        f.write("\n\n")
        f.write(f"MAME_{enc}_JSON_LIST =")
        for font in all_fonts:
            if font.mame_json:
                json_path = font.mame_json.replace(MAME_ARCH_VAR, enc)
            f.write(f" \\\n\t{json_path}")
        f.write("\n\n")
    f.write("\n")

    f.write("SAMPLE_IMAGE_LIST =")
    for font in all_fonts:
        if font.sample_png:
            f.write(f" \\\n\t{font.sample_png}")
    f.write("\n\n")

    f.write("gfx_all: $(GFX_HEADER_LIST)\n")
    f.write("\n")

    f.write(f"mame_all: {' '.join(f'mame_{enc}' for enc in MAME_ENC_LIST)}\n")
    for enc in MAME_ENC_LIST:
        f.write(f"mame_{enc}: $(MAME_{enc}_HPP_LIST) $(MAME_{enc}_JSON_LIST)\n")
    f.write(
        f"mame_cpp: {' '.join(f'$(MAME_{enc}_HPP_LIST)' for enc in MAME_ENC_LIST)}\n"
    )
    f.write(
        f"mame_json: {' '.join(f'$(MAME_{enc}_JSON_LIST)' for enc in MAME_ENC_LIST)}\n"
    )
    f.write("\n")

    f.write("sample_all: $(SAMPLE_IMAGE_LIST)\n")
    f.write("\n")

    for font in all_fonts:
        # GFXfont
        if font.gfx_header:
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
        if font.mame_json and font.mame_hpp:
            for enc in MAME_ENC_LIST:
                json_path = font.mame_json.replace(MAME_ARCH_VAR, enc)
                hpp_path = font.mame_hpp.replace(MAME_ARCH_VAR, enc)
                outdir_hpp = os.path.dirname(hpp_path)
                dependencies = [
                    json_path,
                    "$(CMD_MAMEC)",
                    "$(COMMON_DEPENDENCIES)",
                ]
                f.write(f"{hpp_path}: {' '.join(dependencies)}\n")
                f.write(f"\t@mkdir -p $(dir $@)\n")
                f.write(f"\t$(CMD_MAMEC) -i {json_path} -o {hpp_path}\n")
                f.write("\n")

        # MameFont (JSON)
        if font.mame_hpp:
            for enc in MAME_ENC_LIST:
                json_path = font.mame_json.replace(MAME_ARCH_VAR, enc)
                dependencies = [
                    font.design_bmp,
                    font.design_json,
                    "$(CMD_MAMEC)",
                    "$(COMMON_DEPENDENCIES)",
                ]
                f.write(f"{json_path}: {' '.join(dependencies)}\n")
                f.write(f"\t@mkdir -p $(dir $@)\n")
                f.write(f"\t$(CMD_MAMEC) -e {enc} -i {font.design_bmp} -o $@\n")
                f.write("\n")

        # Sample Image
        if font.sample_png:
            dependencies = [
                font.design_bmp,
                font.design_json,
                "$(COMMON_DEPENDENCIES)",
            ]
            f.write(f"{font.sample_png}: {' '.join(dependencies)}\n")
            f.write(f"\t@mkdir -p $(dir $@)\n")
            f.write(f"\t$(CMD_PYTHON) $(SHAPOFONT_PY)")
            f.write(f" --sample_img $@")
            f.write(f" -i {font.design_dir}\n")
            f.write("\n")

    f.write(
        "distclean_all: distclean_gfx_all distclean_mame_all distclean_sample_all\n"
    )
    f.write("\n")

    f.write("distclean_gfx_all:\n")
    f.write(f"\trm -f {GFX_C_OUT_DIR}/*.h\n")
    f.write("\n")

    f.write(
        f"distclean_mame_all: {' '.join(f'distclean_mame_{enc}' for enc in MAME_ENC_LIST)}\n"
    )
    for enc in MAME_ENC_LIST:
        f.write(f"distclean_mame_{enc}:\n")
        f.write(f"\trm -f {MAME_HPP_OUT_DIR.replace(MAME_ARCH_VAR, enc)}/*.hpp\n")
        f.write(f"\trm -f {MAME_JSON_OUT_DIR.replace(MAME_ARCH_VAR, enc)}/*.json\n")
        f.write("\n")

    f.write("distclean_mame_cpp:\n")
    for enc in MAME_ENC_LIST:
        f.write(f"\trm -f {MAME_HPP_OUT_DIR.replace(MAME_ARCH_VAR, enc)}/*.hpp\n")
    f.write("\n")

    f.write("distclean_mame_json:\n")
    for enc in MAME_ENC_LIST:
        f.write(f"\trm -f {MAME_JSON_OUT_DIR.replace(MAME_ARCH_VAR, enc)}/*.json\n")
    f.write("\n")

    f.write("distclean_sample_all:\n")
    f.write(f"\trm -f {SAMPLE_OUT_DIR}/*.png\n")
    f.write("\n")


os.remove("Makefile.batch.mk")
os.rename("tmp.Makefile.batch.mk", "Makefile.batch.mk")
