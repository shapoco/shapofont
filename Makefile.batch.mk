.PHONY: gfx_all mame_all sample_all
.PHONY: mame_HL mame_HM mame_VL mame_VM
.PHONY: mame_cpp mame_json
.PHONY: distclean_all distclean_gfx_all distclean_mame_all distclean_sample_all
.PHONY: distclean_mame_HL distclean_mame_HM distclean_mame_VL distclean_mame_VM
.PHONY: distclean_mame_cpp distclean_mame_json

all: gfx_all mame_all

GFX_HEADER_LIST = \
	gfxfont/cpp/include/MameSansP_s48c40w08.h \
	gfxfont/cpp/include/MameSquareWide_s64c48a04w16.h \
	gfxfont/cpp/include/ShapoSansP_s27c22a01w04.h \
	gfxfont/cpp/include/ShapoSansP_s21c16a01w03.h \
	gfxfont/cpp/include/MameSansDigitP_s64w08.h \
	gfxfont/cpp/include/MameSansP_s15c12w02.h \
	gfxfont/cpp/include/MameSeg7_s40c38w06.h \
	gfxfont/cpp/include/ShapoSansP_s12c09a01w02.h \
	gfxfont/cpp/include/ShapoSansP_s08c07.h \
	gfxfont/cpp/include/ShapoSansMono_s08c07.h \
	gfxfont/cpp/include/ShapoSansDigitP_s32c30w04.h \
	gfxfont/cpp/include/ShapoSansDigitP_s24c23w04.h \
	gfxfont/cpp/include/ShapoSansP_s07c05a01.h \
	gfxfont/cpp/include/ShapoSansP_s05.h \
	gfxfont/cpp/include/ShapoSansDigitP_s16c14w02.h \
	gfxfont/cpp/include/TestF_s16w04.h \
	gfxfont/cpp/include/TestF_s08w02.h \
	gfxfont/cpp/include/Empty_s01.h

MAME_HL_HPP_LIST = \
	mamefont/cpp/HL/include/MameSansP_s48c40w08.hpp \
	mamefont/cpp/HL/include/MameSquareWide_s64c48a04w16.hpp \
	mamefont/cpp/HL/include/ShapoSansP_s27c22a01w04.hpp \
	mamefont/cpp/HL/include/MameSansP_s15c12w02g02.hpp \
	mamefont/cpp/HL/include/ShapoSansP_s21c16a01w03.hpp \
	mamefont/cpp/HL/include/MameSansDigitP_s64w08.hpp \
	mamefont/cpp/HL/include/MameSansP_s15c12w02.hpp \
	mamefont/cpp/HL/include/MameSeg7_s40c38w06.hpp \
	mamefont/cpp/HL/include/ShapoSansP_s12c09a01w02.hpp \
	mamefont/cpp/HL/include/ShapoSansP_s08c07.hpp \
	mamefont/cpp/HL/include/ShapoSansMono_s08c07.hpp \
	mamefont/cpp/HL/include/ShapoSansDigitP_s32c30w04.hpp \
	mamefont/cpp/HL/include/ShapoSansDigitP_s24c23w04.hpp \
	mamefont/cpp/HL/include/ShapoSansP_s07c05a01.hpp \
	mamefont/cpp/HL/include/ShapoSansP_s05.hpp \
	mamefont/cpp/HL/include/ShapoSansDigitP_s16c14w02.hpp \
	mamefont/cpp/HL/include/TestF_s16w04.hpp \
	mamefont/cpp/HL/include/TestF_s08w02.hpp \
	mamefont/cpp/HL/include/Empty_s01.hpp

MAME_HL_JSON_LIST = \
	mamefont/json/HL/MameSansP_s48c40w08.json \
	mamefont/json/HL/MameSquareWide_s64c48a04w16.json \
	mamefont/json/HL/ShapoSansP_s27c22a01w04.json \
	mamefont/json/HL/MameSansP_s15c12w02g02.json \
	mamefont/json/HL/ShapoSansP_s21c16a01w03.json \
	mamefont/json/HL/MameSansDigitP_s64w08.json \
	mamefont/json/HL/MameSansP_s15c12w02.json \
	mamefont/json/HL/MameSeg7_s40c38w06.json \
	mamefont/json/HL/ShapoSansP_s12c09a01w02.json \
	mamefont/json/HL/ShapoSansP_s08c07.json \
	mamefont/json/HL/ShapoSansMono_s08c07.json \
	mamefont/json/HL/ShapoSansDigitP_s32c30w04.json \
	mamefont/json/HL/ShapoSansDigitP_s24c23w04.json \
	mamefont/json/HL/ShapoSansP_s07c05a01.json \
	mamefont/json/HL/ShapoSansP_s05.json \
	mamefont/json/HL/ShapoSansDigitP_s16c14w02.json \
	mamefont/json/HL/TestF_s16w04.json \
	mamefont/json/HL/TestF_s08w02.json \
	mamefont/json/HL/Empty_s01.json

MAME_HM_HPP_LIST = \
	mamefont/cpp/HM/include/MameSansP_s48c40w08.hpp \
	mamefont/cpp/HM/include/MameSquareWide_s64c48a04w16.hpp \
	mamefont/cpp/HM/include/ShapoSansP_s27c22a01w04.hpp \
	mamefont/cpp/HM/include/MameSansP_s15c12w02g02.hpp \
	mamefont/cpp/HM/include/ShapoSansP_s21c16a01w03.hpp \
	mamefont/cpp/HM/include/MameSansDigitP_s64w08.hpp \
	mamefont/cpp/HM/include/MameSansP_s15c12w02.hpp \
	mamefont/cpp/HM/include/MameSeg7_s40c38w06.hpp \
	mamefont/cpp/HM/include/ShapoSansP_s12c09a01w02.hpp \
	mamefont/cpp/HM/include/ShapoSansP_s08c07.hpp \
	mamefont/cpp/HM/include/ShapoSansMono_s08c07.hpp \
	mamefont/cpp/HM/include/ShapoSansDigitP_s32c30w04.hpp \
	mamefont/cpp/HM/include/ShapoSansDigitP_s24c23w04.hpp \
	mamefont/cpp/HM/include/ShapoSansP_s07c05a01.hpp \
	mamefont/cpp/HM/include/ShapoSansP_s05.hpp \
	mamefont/cpp/HM/include/ShapoSansDigitP_s16c14w02.hpp \
	mamefont/cpp/HM/include/TestF_s16w04.hpp \
	mamefont/cpp/HM/include/TestF_s08w02.hpp \
	mamefont/cpp/HM/include/Empty_s01.hpp

MAME_HM_JSON_LIST = \
	mamefont/json/HM/MameSansP_s48c40w08.json \
	mamefont/json/HM/MameSquareWide_s64c48a04w16.json \
	mamefont/json/HM/ShapoSansP_s27c22a01w04.json \
	mamefont/json/HM/MameSansP_s15c12w02g02.json \
	mamefont/json/HM/ShapoSansP_s21c16a01w03.json \
	mamefont/json/HM/MameSansDigitP_s64w08.json \
	mamefont/json/HM/MameSansP_s15c12w02.json \
	mamefont/json/HM/MameSeg7_s40c38w06.json \
	mamefont/json/HM/ShapoSansP_s12c09a01w02.json \
	mamefont/json/HM/ShapoSansP_s08c07.json \
	mamefont/json/HM/ShapoSansMono_s08c07.json \
	mamefont/json/HM/ShapoSansDigitP_s32c30w04.json \
	mamefont/json/HM/ShapoSansDigitP_s24c23w04.json \
	mamefont/json/HM/ShapoSansP_s07c05a01.json \
	mamefont/json/HM/ShapoSansP_s05.json \
	mamefont/json/HM/ShapoSansDigitP_s16c14w02.json \
	mamefont/json/HM/TestF_s16w04.json \
	mamefont/json/HM/TestF_s08w02.json \
	mamefont/json/HM/Empty_s01.json

MAME_VL_HPP_LIST = \
	mamefont/cpp/VL/include/MameSansP_s48c40w08.hpp \
	mamefont/cpp/VL/include/MameSquareWide_s64c48a04w16.hpp \
	mamefont/cpp/VL/include/ShapoSansP_s27c22a01w04.hpp \
	mamefont/cpp/VL/include/MameSansP_s15c12w02g02.hpp \
	mamefont/cpp/VL/include/ShapoSansP_s21c16a01w03.hpp \
	mamefont/cpp/VL/include/MameSansDigitP_s64w08.hpp \
	mamefont/cpp/VL/include/MameSansP_s15c12w02.hpp \
	mamefont/cpp/VL/include/MameSeg7_s40c38w06.hpp \
	mamefont/cpp/VL/include/ShapoSansP_s12c09a01w02.hpp \
	mamefont/cpp/VL/include/ShapoSansP_s08c07.hpp \
	mamefont/cpp/VL/include/ShapoSansMono_s08c07.hpp \
	mamefont/cpp/VL/include/ShapoSansDigitP_s32c30w04.hpp \
	mamefont/cpp/VL/include/ShapoSansDigitP_s24c23w04.hpp \
	mamefont/cpp/VL/include/ShapoSansP_s07c05a01.hpp \
	mamefont/cpp/VL/include/ShapoSansP_s05.hpp \
	mamefont/cpp/VL/include/ShapoSansDigitP_s16c14w02.hpp \
	mamefont/cpp/VL/include/TestF_s16w04.hpp \
	mamefont/cpp/VL/include/TestF_s08w02.hpp \
	mamefont/cpp/VL/include/Empty_s01.hpp

MAME_VL_JSON_LIST = \
	mamefont/json/VL/MameSansP_s48c40w08.json \
	mamefont/json/VL/MameSquareWide_s64c48a04w16.json \
	mamefont/json/VL/ShapoSansP_s27c22a01w04.json \
	mamefont/json/VL/MameSansP_s15c12w02g02.json \
	mamefont/json/VL/ShapoSansP_s21c16a01w03.json \
	mamefont/json/VL/MameSansDigitP_s64w08.json \
	mamefont/json/VL/MameSansP_s15c12w02.json \
	mamefont/json/VL/MameSeg7_s40c38w06.json \
	mamefont/json/VL/ShapoSansP_s12c09a01w02.json \
	mamefont/json/VL/ShapoSansP_s08c07.json \
	mamefont/json/VL/ShapoSansMono_s08c07.json \
	mamefont/json/VL/ShapoSansDigitP_s32c30w04.json \
	mamefont/json/VL/ShapoSansDigitP_s24c23w04.json \
	mamefont/json/VL/ShapoSansP_s07c05a01.json \
	mamefont/json/VL/ShapoSansP_s05.json \
	mamefont/json/VL/ShapoSansDigitP_s16c14w02.json \
	mamefont/json/VL/TestF_s16w04.json \
	mamefont/json/VL/TestF_s08w02.json \
	mamefont/json/VL/Empty_s01.json

MAME_VM_HPP_LIST = \
	mamefont/cpp/VM/include/MameSansP_s48c40w08.hpp \
	mamefont/cpp/VM/include/MameSquareWide_s64c48a04w16.hpp \
	mamefont/cpp/VM/include/ShapoSansP_s27c22a01w04.hpp \
	mamefont/cpp/VM/include/MameSansP_s15c12w02g02.hpp \
	mamefont/cpp/VM/include/ShapoSansP_s21c16a01w03.hpp \
	mamefont/cpp/VM/include/MameSansDigitP_s64w08.hpp \
	mamefont/cpp/VM/include/MameSansP_s15c12w02.hpp \
	mamefont/cpp/VM/include/MameSeg7_s40c38w06.hpp \
	mamefont/cpp/VM/include/ShapoSansP_s12c09a01w02.hpp \
	mamefont/cpp/VM/include/ShapoSansP_s08c07.hpp \
	mamefont/cpp/VM/include/ShapoSansMono_s08c07.hpp \
	mamefont/cpp/VM/include/ShapoSansDigitP_s32c30w04.hpp \
	mamefont/cpp/VM/include/ShapoSansDigitP_s24c23w04.hpp \
	mamefont/cpp/VM/include/ShapoSansP_s07c05a01.hpp \
	mamefont/cpp/VM/include/ShapoSansP_s05.hpp \
	mamefont/cpp/VM/include/ShapoSansDigitP_s16c14w02.hpp \
	mamefont/cpp/VM/include/TestF_s16w04.hpp \
	mamefont/cpp/VM/include/TestF_s08w02.hpp \
	mamefont/cpp/VM/include/Empty_s01.hpp

MAME_VM_JSON_LIST = \
	mamefont/json/VM/MameSansP_s48c40w08.json \
	mamefont/json/VM/MameSquareWide_s64c48a04w16.json \
	mamefont/json/VM/ShapoSansP_s27c22a01w04.json \
	mamefont/json/VM/MameSansP_s15c12w02g02.json \
	mamefont/json/VM/ShapoSansP_s21c16a01w03.json \
	mamefont/json/VM/MameSansDigitP_s64w08.json \
	mamefont/json/VM/MameSansP_s15c12w02.json \
	mamefont/json/VM/MameSeg7_s40c38w06.json \
	mamefont/json/VM/ShapoSansP_s12c09a01w02.json \
	mamefont/json/VM/ShapoSansP_s08c07.json \
	mamefont/json/VM/ShapoSansMono_s08c07.json \
	mamefont/json/VM/ShapoSansDigitP_s32c30w04.json \
	mamefont/json/VM/ShapoSansDigitP_s24c23w04.json \
	mamefont/json/VM/ShapoSansP_s07c05a01.json \
	mamefont/json/VM/ShapoSansP_s05.json \
	mamefont/json/VM/ShapoSansDigitP_s16c14w02.json \
	mamefont/json/VM/TestF_s16w04.json \
	mamefont/json/VM/TestF_s08w02.json \
	mamefont/json/VM/Empty_s01.json


SAMPLE_IMAGE_LIST = \
	img/sample/MameSansP_s48c40w08.png \
	img/sample/MameSquareWide_s64c48a04w16.png \
	img/sample/ShapoSansP_s27c22a01w04.png \
	img/sample/MameSansP_s15c12w02g02.png \
	img/sample/ShapoSansP_s21c16a01w03.png \
	img/sample/MameSansDigitP_s64w08.png \
	img/sample/MameSansP_s15c12w02.png \
	img/sample/MameSeg7_s40c38w06.png \
	img/sample/ShapoSansP_s12c09a01w02.png \
	img/sample/ShapoSansP_s08c07.png \
	img/sample/ShapoSansMono_s08c07.png \
	img/sample/ShapoSansDigitP_s32c30w04.png \
	img/sample/ShapoSansDigitP_s24c23w04.png \
	img/sample/ShapoSansP_s07c05a01.png \
	img/sample/ShapoSansP_s05.png \
	img/sample/ShapoSansDigitP_s16c14w02.png \
	img/sample/TestF_s16w04.png \
	img/sample/TestF_s08w02.png \
	img/sample/Empty_s01.png

gfx_all: $(GFX_HEADER_LIST)

mame_all: mame_HL mame_HM mame_VL mame_VM
mame_HL: $(MAME_HL_HPP_LIST) $(MAME_HL_JSON_LIST)
mame_HM: $(MAME_HM_HPP_LIST) $(MAME_HM_JSON_LIST)
mame_VL: $(MAME_VL_HPP_LIST) $(MAME_VL_JSON_LIST)
mame_VM: $(MAME_VM_HPP_LIST) $(MAME_VM_JSON_LIST)
mame_cpp: $(MAME_HL_HPP_LIST) $(MAME_HM_HPP_LIST) $(MAME_VL_HPP_LIST) $(MAME_VM_HPP_LIST)
mame_json: $(MAME_HL_JSON_LIST) $(MAME_HM_JSON_LIST) $(MAME_VL_JSON_LIST) $(MAME_VM_JSON_LIST)

sample_all: $(SAMPLE_IMAGE_LIST)

gfxfont/cpp/include/MameSansP_s48c40w08.h: design/MameSansP_s48c40w08/design.png design/MameSansP_s48c40w08/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/MameSansP_s48c40w08

mamefont/cpp/HL/include/MameSansP_s48c40w08.hpp: mamefont/json/HL/MameSansP_s48c40w08.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HL/MameSansP_s48c40w08.json -o mamefont/cpp/HL/include/MameSansP_s48c40w08.hpp

mamefont/cpp/HM/include/MameSansP_s48c40w08.hpp: mamefont/json/HM/MameSansP_s48c40w08.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HM/MameSansP_s48c40w08.json -o mamefont/cpp/HM/include/MameSansP_s48c40w08.hpp

mamefont/cpp/VL/include/MameSansP_s48c40w08.hpp: mamefont/json/VL/MameSansP_s48c40w08.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VL/MameSansP_s48c40w08.json -o mamefont/cpp/VL/include/MameSansP_s48c40w08.hpp

mamefont/cpp/VM/include/MameSansP_s48c40w08.hpp: mamefont/json/VM/MameSansP_s48c40w08.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VM/MameSansP_s48c40w08.json -o mamefont/cpp/VM/include/MameSansP_s48c40w08.hpp

mamefont/json/HL/MameSansP_s48c40w08.json: design/MameSansP_s48c40w08/design.png design/MameSansP_s48c40w08/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HL -i design/MameSansP_s48c40w08/design.png -o $@

mamefont/json/HM/MameSansP_s48c40w08.json: design/MameSansP_s48c40w08/design.png design/MameSansP_s48c40w08/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HM -i design/MameSansP_s48c40w08/design.png -o $@

mamefont/json/VL/MameSansP_s48c40w08.json: design/MameSansP_s48c40w08/design.png design/MameSansP_s48c40w08/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VL -i design/MameSansP_s48c40w08/design.png -o $@

mamefont/json/VM/MameSansP_s48c40w08.json: design/MameSansP_s48c40w08/design.png design/MameSansP_s48c40w08/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VM -i design/MameSansP_s48c40w08/design.png -o $@

img/sample/MameSansP_s48c40w08.png: design/MameSansP_s48c40w08/design.png design/MameSansP_s48c40w08/design.json $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --sample_img $@ -i design/MameSansP_s48c40w08

gfxfont/cpp/include/MameSquareWide_s64c48a04w16.h: design/MameSquareWide_s64c48a04w16/design.png design/MameSquareWide_s64c48a04w16/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/MameSquareWide_s64c48a04w16

mamefont/cpp/HL/include/MameSquareWide_s64c48a04w16.hpp: mamefont/json/HL/MameSquareWide_s64c48a04w16.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HL/MameSquareWide_s64c48a04w16.json -o mamefont/cpp/HL/include/MameSquareWide_s64c48a04w16.hpp

mamefont/cpp/HM/include/MameSquareWide_s64c48a04w16.hpp: mamefont/json/HM/MameSquareWide_s64c48a04w16.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HM/MameSquareWide_s64c48a04w16.json -o mamefont/cpp/HM/include/MameSquareWide_s64c48a04w16.hpp

mamefont/cpp/VL/include/MameSquareWide_s64c48a04w16.hpp: mamefont/json/VL/MameSquareWide_s64c48a04w16.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VL/MameSquareWide_s64c48a04w16.json -o mamefont/cpp/VL/include/MameSquareWide_s64c48a04w16.hpp

mamefont/cpp/VM/include/MameSquareWide_s64c48a04w16.hpp: mamefont/json/VM/MameSquareWide_s64c48a04w16.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VM/MameSquareWide_s64c48a04w16.json -o mamefont/cpp/VM/include/MameSquareWide_s64c48a04w16.hpp

mamefont/json/HL/MameSquareWide_s64c48a04w16.json: design/MameSquareWide_s64c48a04w16/design.png design/MameSquareWide_s64c48a04w16/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HL -i design/MameSquareWide_s64c48a04w16/design.png -o $@

mamefont/json/HM/MameSquareWide_s64c48a04w16.json: design/MameSquareWide_s64c48a04w16/design.png design/MameSquareWide_s64c48a04w16/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HM -i design/MameSquareWide_s64c48a04w16/design.png -o $@

mamefont/json/VL/MameSquareWide_s64c48a04w16.json: design/MameSquareWide_s64c48a04w16/design.png design/MameSquareWide_s64c48a04w16/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VL -i design/MameSquareWide_s64c48a04w16/design.png -o $@

mamefont/json/VM/MameSquareWide_s64c48a04w16.json: design/MameSquareWide_s64c48a04w16/design.png design/MameSquareWide_s64c48a04w16/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VM -i design/MameSquareWide_s64c48a04w16/design.png -o $@

img/sample/MameSquareWide_s64c48a04w16.png: design/MameSquareWide_s64c48a04w16/design.png design/MameSquareWide_s64c48a04w16/design.json $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --sample_img $@ -i design/MameSquareWide_s64c48a04w16

gfxfont/cpp/include/ShapoSansP_s27c22a01w04.h: design/ShapoSansP_s27c22a01w04/design.png design/ShapoSansP_s27c22a01w04/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/ShapoSansP_s27c22a01w04

mamefont/cpp/HL/include/ShapoSansP_s27c22a01w04.hpp: mamefont/json/HL/ShapoSansP_s27c22a01w04.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HL/ShapoSansP_s27c22a01w04.json -o mamefont/cpp/HL/include/ShapoSansP_s27c22a01w04.hpp

mamefont/cpp/HM/include/ShapoSansP_s27c22a01w04.hpp: mamefont/json/HM/ShapoSansP_s27c22a01w04.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HM/ShapoSansP_s27c22a01w04.json -o mamefont/cpp/HM/include/ShapoSansP_s27c22a01w04.hpp

mamefont/cpp/VL/include/ShapoSansP_s27c22a01w04.hpp: mamefont/json/VL/ShapoSansP_s27c22a01w04.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VL/ShapoSansP_s27c22a01w04.json -o mamefont/cpp/VL/include/ShapoSansP_s27c22a01w04.hpp

mamefont/cpp/VM/include/ShapoSansP_s27c22a01w04.hpp: mamefont/json/VM/ShapoSansP_s27c22a01w04.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VM/ShapoSansP_s27c22a01w04.json -o mamefont/cpp/VM/include/ShapoSansP_s27c22a01w04.hpp

mamefont/json/HL/ShapoSansP_s27c22a01w04.json: design/ShapoSansP_s27c22a01w04/design.png design/ShapoSansP_s27c22a01w04/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HL -i design/ShapoSansP_s27c22a01w04/design.png -o $@

mamefont/json/HM/ShapoSansP_s27c22a01w04.json: design/ShapoSansP_s27c22a01w04/design.png design/ShapoSansP_s27c22a01w04/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HM -i design/ShapoSansP_s27c22a01w04/design.png -o $@

mamefont/json/VL/ShapoSansP_s27c22a01w04.json: design/ShapoSansP_s27c22a01w04/design.png design/ShapoSansP_s27c22a01w04/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VL -i design/ShapoSansP_s27c22a01w04/design.png -o $@

mamefont/json/VM/ShapoSansP_s27c22a01w04.json: design/ShapoSansP_s27c22a01w04/design.png design/ShapoSansP_s27c22a01w04/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VM -i design/ShapoSansP_s27c22a01w04/design.png -o $@

img/sample/ShapoSansP_s27c22a01w04.png: design/ShapoSansP_s27c22a01w04/design.png design/ShapoSansP_s27c22a01w04/design.json $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --sample_img $@ -i design/ShapoSansP_s27c22a01w04

mamefont/cpp/HL/include/MameSansP_s15c12w02g02.hpp: mamefont/json/HL/MameSansP_s15c12w02g02.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HL/MameSansP_s15c12w02g02.json -o mamefont/cpp/HL/include/MameSansP_s15c12w02g02.hpp

mamefont/cpp/HM/include/MameSansP_s15c12w02g02.hpp: mamefont/json/HM/MameSansP_s15c12w02g02.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HM/MameSansP_s15c12w02g02.json -o mamefont/cpp/HM/include/MameSansP_s15c12w02g02.hpp

mamefont/cpp/VL/include/MameSansP_s15c12w02g02.hpp: mamefont/json/VL/MameSansP_s15c12w02g02.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VL/MameSansP_s15c12w02g02.json -o mamefont/cpp/VL/include/MameSansP_s15c12w02g02.hpp

mamefont/cpp/VM/include/MameSansP_s15c12w02g02.hpp: mamefont/json/VM/MameSansP_s15c12w02g02.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VM/MameSansP_s15c12w02g02.json -o mamefont/cpp/VM/include/MameSansP_s15c12w02g02.hpp

mamefont/json/HL/MameSansP_s15c12w02g02.json: design/MameSansP_s15c12w02g02/design.png design/MameSansP_s15c12w02g02/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HL -i design/MameSansP_s15c12w02g02/design.png -o $@

mamefont/json/HM/MameSansP_s15c12w02g02.json: design/MameSansP_s15c12w02g02/design.png design/MameSansP_s15c12w02g02/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HM -i design/MameSansP_s15c12w02g02/design.png -o $@

mamefont/json/VL/MameSansP_s15c12w02g02.json: design/MameSansP_s15c12w02g02/design.png design/MameSansP_s15c12w02g02/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VL -i design/MameSansP_s15c12w02g02/design.png -o $@

mamefont/json/VM/MameSansP_s15c12w02g02.json: design/MameSansP_s15c12w02g02/design.png design/MameSansP_s15c12w02g02/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VM -i design/MameSansP_s15c12w02g02/design.png -o $@

img/sample/MameSansP_s15c12w02g02.png: design/MameSansP_s15c12w02g02/design.png design/MameSansP_s15c12w02g02/design.json $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --sample_img $@ -i design/MameSansP_s15c12w02g02

gfxfont/cpp/include/ShapoSansP_s21c16a01w03.h: design/ShapoSansP_s21c16a01w03/design.png design/ShapoSansP_s21c16a01w03/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/ShapoSansP_s21c16a01w03

mamefont/cpp/HL/include/ShapoSansP_s21c16a01w03.hpp: mamefont/json/HL/ShapoSansP_s21c16a01w03.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HL/ShapoSansP_s21c16a01w03.json -o mamefont/cpp/HL/include/ShapoSansP_s21c16a01w03.hpp

mamefont/cpp/HM/include/ShapoSansP_s21c16a01w03.hpp: mamefont/json/HM/ShapoSansP_s21c16a01w03.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HM/ShapoSansP_s21c16a01w03.json -o mamefont/cpp/HM/include/ShapoSansP_s21c16a01w03.hpp

mamefont/cpp/VL/include/ShapoSansP_s21c16a01w03.hpp: mamefont/json/VL/ShapoSansP_s21c16a01w03.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VL/ShapoSansP_s21c16a01w03.json -o mamefont/cpp/VL/include/ShapoSansP_s21c16a01w03.hpp

mamefont/cpp/VM/include/ShapoSansP_s21c16a01w03.hpp: mamefont/json/VM/ShapoSansP_s21c16a01w03.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VM/ShapoSansP_s21c16a01w03.json -o mamefont/cpp/VM/include/ShapoSansP_s21c16a01w03.hpp

mamefont/json/HL/ShapoSansP_s21c16a01w03.json: design/ShapoSansP_s21c16a01w03/design.png design/ShapoSansP_s21c16a01w03/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HL -i design/ShapoSansP_s21c16a01w03/design.png -o $@

mamefont/json/HM/ShapoSansP_s21c16a01w03.json: design/ShapoSansP_s21c16a01w03/design.png design/ShapoSansP_s21c16a01w03/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HM -i design/ShapoSansP_s21c16a01w03/design.png -o $@

mamefont/json/VL/ShapoSansP_s21c16a01w03.json: design/ShapoSansP_s21c16a01w03/design.png design/ShapoSansP_s21c16a01w03/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VL -i design/ShapoSansP_s21c16a01w03/design.png -o $@

mamefont/json/VM/ShapoSansP_s21c16a01w03.json: design/ShapoSansP_s21c16a01w03/design.png design/ShapoSansP_s21c16a01w03/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VM -i design/ShapoSansP_s21c16a01w03/design.png -o $@

img/sample/ShapoSansP_s21c16a01w03.png: design/ShapoSansP_s21c16a01w03/design.png design/ShapoSansP_s21c16a01w03/design.json $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --sample_img $@ -i design/ShapoSansP_s21c16a01w03

gfxfont/cpp/include/MameSansDigitP_s64w08.h: design/MameSansDigitP_s64w08/design.png design/MameSansDigitP_s64w08/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/MameSansDigitP_s64w08

mamefont/cpp/HL/include/MameSansDigitP_s64w08.hpp: mamefont/json/HL/MameSansDigitP_s64w08.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HL/MameSansDigitP_s64w08.json -o mamefont/cpp/HL/include/MameSansDigitP_s64w08.hpp

mamefont/cpp/HM/include/MameSansDigitP_s64w08.hpp: mamefont/json/HM/MameSansDigitP_s64w08.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HM/MameSansDigitP_s64w08.json -o mamefont/cpp/HM/include/MameSansDigitP_s64w08.hpp

mamefont/cpp/VL/include/MameSansDigitP_s64w08.hpp: mamefont/json/VL/MameSansDigitP_s64w08.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VL/MameSansDigitP_s64w08.json -o mamefont/cpp/VL/include/MameSansDigitP_s64w08.hpp

mamefont/cpp/VM/include/MameSansDigitP_s64w08.hpp: mamefont/json/VM/MameSansDigitP_s64w08.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VM/MameSansDigitP_s64w08.json -o mamefont/cpp/VM/include/MameSansDigitP_s64w08.hpp

mamefont/json/HL/MameSansDigitP_s64w08.json: design/MameSansDigitP_s64w08/design.png design/MameSansDigitP_s64w08/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HL -i design/MameSansDigitP_s64w08/design.png -o $@

mamefont/json/HM/MameSansDigitP_s64w08.json: design/MameSansDigitP_s64w08/design.png design/MameSansDigitP_s64w08/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HM -i design/MameSansDigitP_s64w08/design.png -o $@

mamefont/json/VL/MameSansDigitP_s64w08.json: design/MameSansDigitP_s64w08/design.png design/MameSansDigitP_s64w08/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VL -i design/MameSansDigitP_s64w08/design.png -o $@

mamefont/json/VM/MameSansDigitP_s64w08.json: design/MameSansDigitP_s64w08/design.png design/MameSansDigitP_s64w08/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VM -i design/MameSansDigitP_s64w08/design.png -o $@

img/sample/MameSansDigitP_s64w08.png: design/MameSansDigitP_s64w08/design.png design/MameSansDigitP_s64w08/design.json $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --sample_img $@ -i design/MameSansDigitP_s64w08

gfxfont/cpp/include/MameSansP_s15c12w02.h: design/MameSansP_s15c12w02/design.png design/MameSansP_s15c12w02/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/MameSansP_s15c12w02

mamefont/cpp/HL/include/MameSansP_s15c12w02.hpp: mamefont/json/HL/MameSansP_s15c12w02.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HL/MameSansP_s15c12w02.json -o mamefont/cpp/HL/include/MameSansP_s15c12w02.hpp

mamefont/cpp/HM/include/MameSansP_s15c12w02.hpp: mamefont/json/HM/MameSansP_s15c12w02.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HM/MameSansP_s15c12w02.json -o mamefont/cpp/HM/include/MameSansP_s15c12w02.hpp

mamefont/cpp/VL/include/MameSansP_s15c12w02.hpp: mamefont/json/VL/MameSansP_s15c12w02.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VL/MameSansP_s15c12w02.json -o mamefont/cpp/VL/include/MameSansP_s15c12w02.hpp

mamefont/cpp/VM/include/MameSansP_s15c12w02.hpp: mamefont/json/VM/MameSansP_s15c12w02.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VM/MameSansP_s15c12w02.json -o mamefont/cpp/VM/include/MameSansP_s15c12w02.hpp

mamefont/json/HL/MameSansP_s15c12w02.json: design/MameSansP_s15c12w02/design.png design/MameSansP_s15c12w02/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HL -i design/MameSansP_s15c12w02/design.png -o $@

mamefont/json/HM/MameSansP_s15c12w02.json: design/MameSansP_s15c12w02/design.png design/MameSansP_s15c12w02/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HM -i design/MameSansP_s15c12w02/design.png -o $@

mamefont/json/VL/MameSansP_s15c12w02.json: design/MameSansP_s15c12w02/design.png design/MameSansP_s15c12w02/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VL -i design/MameSansP_s15c12w02/design.png -o $@

mamefont/json/VM/MameSansP_s15c12w02.json: design/MameSansP_s15c12w02/design.png design/MameSansP_s15c12w02/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VM -i design/MameSansP_s15c12w02/design.png -o $@

img/sample/MameSansP_s15c12w02.png: design/MameSansP_s15c12w02/design.png design/MameSansP_s15c12w02/design.json $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --sample_img $@ -i design/MameSansP_s15c12w02

gfxfont/cpp/include/MameSeg7_s40c38w06.h: design/MameSeg7_s40c38w06/design.png design/MameSeg7_s40c38w06/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/MameSeg7_s40c38w06

mamefont/cpp/HL/include/MameSeg7_s40c38w06.hpp: mamefont/json/HL/MameSeg7_s40c38w06.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HL/MameSeg7_s40c38w06.json -o mamefont/cpp/HL/include/MameSeg7_s40c38w06.hpp

mamefont/cpp/HM/include/MameSeg7_s40c38w06.hpp: mamefont/json/HM/MameSeg7_s40c38w06.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HM/MameSeg7_s40c38w06.json -o mamefont/cpp/HM/include/MameSeg7_s40c38w06.hpp

mamefont/cpp/VL/include/MameSeg7_s40c38w06.hpp: mamefont/json/VL/MameSeg7_s40c38w06.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VL/MameSeg7_s40c38w06.json -o mamefont/cpp/VL/include/MameSeg7_s40c38w06.hpp

mamefont/cpp/VM/include/MameSeg7_s40c38w06.hpp: mamefont/json/VM/MameSeg7_s40c38w06.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VM/MameSeg7_s40c38w06.json -o mamefont/cpp/VM/include/MameSeg7_s40c38w06.hpp

mamefont/json/HL/MameSeg7_s40c38w06.json: design/MameSeg7_s40c38w06/design.png design/MameSeg7_s40c38w06/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HL -i design/MameSeg7_s40c38w06/design.png -o $@

mamefont/json/HM/MameSeg7_s40c38w06.json: design/MameSeg7_s40c38w06/design.png design/MameSeg7_s40c38w06/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HM -i design/MameSeg7_s40c38w06/design.png -o $@

mamefont/json/VL/MameSeg7_s40c38w06.json: design/MameSeg7_s40c38w06/design.png design/MameSeg7_s40c38w06/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VL -i design/MameSeg7_s40c38w06/design.png -o $@

mamefont/json/VM/MameSeg7_s40c38w06.json: design/MameSeg7_s40c38w06/design.png design/MameSeg7_s40c38w06/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VM -i design/MameSeg7_s40c38w06/design.png -o $@

img/sample/MameSeg7_s40c38w06.png: design/MameSeg7_s40c38w06/design.png design/MameSeg7_s40c38w06/design.json $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --sample_img $@ -i design/MameSeg7_s40c38w06

gfxfont/cpp/include/ShapoSansP_s12c09a01w02.h: design/ShapoSansP_s12c09a01w02/design.png design/ShapoSansP_s12c09a01w02/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/ShapoSansP_s12c09a01w02

mamefont/cpp/HL/include/ShapoSansP_s12c09a01w02.hpp: mamefont/json/HL/ShapoSansP_s12c09a01w02.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HL/ShapoSansP_s12c09a01w02.json -o mamefont/cpp/HL/include/ShapoSansP_s12c09a01w02.hpp

mamefont/cpp/HM/include/ShapoSansP_s12c09a01w02.hpp: mamefont/json/HM/ShapoSansP_s12c09a01w02.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HM/ShapoSansP_s12c09a01w02.json -o mamefont/cpp/HM/include/ShapoSansP_s12c09a01w02.hpp

mamefont/cpp/VL/include/ShapoSansP_s12c09a01w02.hpp: mamefont/json/VL/ShapoSansP_s12c09a01w02.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VL/ShapoSansP_s12c09a01w02.json -o mamefont/cpp/VL/include/ShapoSansP_s12c09a01w02.hpp

mamefont/cpp/VM/include/ShapoSansP_s12c09a01w02.hpp: mamefont/json/VM/ShapoSansP_s12c09a01w02.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VM/ShapoSansP_s12c09a01w02.json -o mamefont/cpp/VM/include/ShapoSansP_s12c09a01w02.hpp

mamefont/json/HL/ShapoSansP_s12c09a01w02.json: design/ShapoSansP_s12c09a01w02/design.png design/ShapoSansP_s12c09a01w02/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HL -i design/ShapoSansP_s12c09a01w02/design.png -o $@

mamefont/json/HM/ShapoSansP_s12c09a01w02.json: design/ShapoSansP_s12c09a01w02/design.png design/ShapoSansP_s12c09a01w02/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HM -i design/ShapoSansP_s12c09a01w02/design.png -o $@

mamefont/json/VL/ShapoSansP_s12c09a01w02.json: design/ShapoSansP_s12c09a01w02/design.png design/ShapoSansP_s12c09a01w02/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VL -i design/ShapoSansP_s12c09a01w02/design.png -o $@

mamefont/json/VM/ShapoSansP_s12c09a01w02.json: design/ShapoSansP_s12c09a01w02/design.png design/ShapoSansP_s12c09a01w02/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VM -i design/ShapoSansP_s12c09a01w02/design.png -o $@

img/sample/ShapoSansP_s12c09a01w02.png: design/ShapoSansP_s12c09a01w02/design.png design/ShapoSansP_s12c09a01w02/design.json $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --sample_img $@ -i design/ShapoSansP_s12c09a01w02

gfxfont/cpp/include/ShapoSansP_s08c07.h: design/ShapoSansP_s08c07/design.png design/ShapoSansP_s08c07/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/ShapoSansP_s08c07

mamefont/cpp/HL/include/ShapoSansP_s08c07.hpp: mamefont/json/HL/ShapoSansP_s08c07.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HL/ShapoSansP_s08c07.json -o mamefont/cpp/HL/include/ShapoSansP_s08c07.hpp

mamefont/cpp/HM/include/ShapoSansP_s08c07.hpp: mamefont/json/HM/ShapoSansP_s08c07.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HM/ShapoSansP_s08c07.json -o mamefont/cpp/HM/include/ShapoSansP_s08c07.hpp

mamefont/cpp/VL/include/ShapoSansP_s08c07.hpp: mamefont/json/VL/ShapoSansP_s08c07.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VL/ShapoSansP_s08c07.json -o mamefont/cpp/VL/include/ShapoSansP_s08c07.hpp

mamefont/cpp/VM/include/ShapoSansP_s08c07.hpp: mamefont/json/VM/ShapoSansP_s08c07.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VM/ShapoSansP_s08c07.json -o mamefont/cpp/VM/include/ShapoSansP_s08c07.hpp

mamefont/json/HL/ShapoSansP_s08c07.json: design/ShapoSansP_s08c07/design.png design/ShapoSansP_s08c07/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HL -i design/ShapoSansP_s08c07/design.png -o $@

mamefont/json/HM/ShapoSansP_s08c07.json: design/ShapoSansP_s08c07/design.png design/ShapoSansP_s08c07/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HM -i design/ShapoSansP_s08c07/design.png -o $@

mamefont/json/VL/ShapoSansP_s08c07.json: design/ShapoSansP_s08c07/design.png design/ShapoSansP_s08c07/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VL -i design/ShapoSansP_s08c07/design.png -o $@

mamefont/json/VM/ShapoSansP_s08c07.json: design/ShapoSansP_s08c07/design.png design/ShapoSansP_s08c07/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VM -i design/ShapoSansP_s08c07/design.png -o $@

img/sample/ShapoSansP_s08c07.png: design/ShapoSansP_s08c07/design.png design/ShapoSansP_s08c07/design.json $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --sample_img $@ -i design/ShapoSansP_s08c07

gfxfont/cpp/include/ShapoSansMono_s08c07.h: design/ShapoSansMono_s08c07/design.png design/ShapoSansMono_s08c07/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/ShapoSansMono_s08c07

mamefont/cpp/HL/include/ShapoSansMono_s08c07.hpp: mamefont/json/HL/ShapoSansMono_s08c07.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HL/ShapoSansMono_s08c07.json -o mamefont/cpp/HL/include/ShapoSansMono_s08c07.hpp

mamefont/cpp/HM/include/ShapoSansMono_s08c07.hpp: mamefont/json/HM/ShapoSansMono_s08c07.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HM/ShapoSansMono_s08c07.json -o mamefont/cpp/HM/include/ShapoSansMono_s08c07.hpp

mamefont/cpp/VL/include/ShapoSansMono_s08c07.hpp: mamefont/json/VL/ShapoSansMono_s08c07.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VL/ShapoSansMono_s08c07.json -o mamefont/cpp/VL/include/ShapoSansMono_s08c07.hpp

mamefont/cpp/VM/include/ShapoSansMono_s08c07.hpp: mamefont/json/VM/ShapoSansMono_s08c07.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VM/ShapoSansMono_s08c07.json -o mamefont/cpp/VM/include/ShapoSansMono_s08c07.hpp

mamefont/json/HL/ShapoSansMono_s08c07.json: design/ShapoSansMono_s08c07/design.png design/ShapoSansMono_s08c07/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HL -i design/ShapoSansMono_s08c07/design.png -o $@

mamefont/json/HM/ShapoSansMono_s08c07.json: design/ShapoSansMono_s08c07/design.png design/ShapoSansMono_s08c07/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HM -i design/ShapoSansMono_s08c07/design.png -o $@

mamefont/json/VL/ShapoSansMono_s08c07.json: design/ShapoSansMono_s08c07/design.png design/ShapoSansMono_s08c07/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VL -i design/ShapoSansMono_s08c07/design.png -o $@

mamefont/json/VM/ShapoSansMono_s08c07.json: design/ShapoSansMono_s08c07/design.png design/ShapoSansMono_s08c07/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VM -i design/ShapoSansMono_s08c07/design.png -o $@

img/sample/ShapoSansMono_s08c07.png: design/ShapoSansMono_s08c07/design.png design/ShapoSansMono_s08c07/design.json $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --sample_img $@ -i design/ShapoSansMono_s08c07

gfxfont/cpp/include/ShapoSansDigitP_s32c30w04.h: design/ShapoSansDigitP_s32c30w04/design.png design/ShapoSansDigitP_s32c30w04/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/ShapoSansDigitP_s32c30w04

mamefont/cpp/HL/include/ShapoSansDigitP_s32c30w04.hpp: mamefont/json/HL/ShapoSansDigitP_s32c30w04.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HL/ShapoSansDigitP_s32c30w04.json -o mamefont/cpp/HL/include/ShapoSansDigitP_s32c30w04.hpp

mamefont/cpp/HM/include/ShapoSansDigitP_s32c30w04.hpp: mamefont/json/HM/ShapoSansDigitP_s32c30w04.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HM/ShapoSansDigitP_s32c30w04.json -o mamefont/cpp/HM/include/ShapoSansDigitP_s32c30w04.hpp

mamefont/cpp/VL/include/ShapoSansDigitP_s32c30w04.hpp: mamefont/json/VL/ShapoSansDigitP_s32c30w04.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VL/ShapoSansDigitP_s32c30w04.json -o mamefont/cpp/VL/include/ShapoSansDigitP_s32c30w04.hpp

mamefont/cpp/VM/include/ShapoSansDigitP_s32c30w04.hpp: mamefont/json/VM/ShapoSansDigitP_s32c30w04.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VM/ShapoSansDigitP_s32c30w04.json -o mamefont/cpp/VM/include/ShapoSansDigitP_s32c30w04.hpp

mamefont/json/HL/ShapoSansDigitP_s32c30w04.json: design/ShapoSansDigitP_s32c30w04/design.png design/ShapoSansDigitP_s32c30w04/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HL -i design/ShapoSansDigitP_s32c30w04/design.png -o $@

mamefont/json/HM/ShapoSansDigitP_s32c30w04.json: design/ShapoSansDigitP_s32c30w04/design.png design/ShapoSansDigitP_s32c30w04/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HM -i design/ShapoSansDigitP_s32c30w04/design.png -o $@

mamefont/json/VL/ShapoSansDigitP_s32c30w04.json: design/ShapoSansDigitP_s32c30w04/design.png design/ShapoSansDigitP_s32c30w04/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VL -i design/ShapoSansDigitP_s32c30w04/design.png -o $@

mamefont/json/VM/ShapoSansDigitP_s32c30w04.json: design/ShapoSansDigitP_s32c30w04/design.png design/ShapoSansDigitP_s32c30w04/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VM -i design/ShapoSansDigitP_s32c30w04/design.png -o $@

img/sample/ShapoSansDigitP_s32c30w04.png: design/ShapoSansDigitP_s32c30w04/design.png design/ShapoSansDigitP_s32c30w04/design.json $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --sample_img $@ -i design/ShapoSansDigitP_s32c30w04

gfxfont/cpp/include/ShapoSansDigitP_s24c23w04.h: design/ShapoSansDigitP_s24c23w04/design.png design/ShapoSansDigitP_s24c23w04/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/ShapoSansDigitP_s24c23w04

mamefont/cpp/HL/include/ShapoSansDigitP_s24c23w04.hpp: mamefont/json/HL/ShapoSansDigitP_s24c23w04.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HL/ShapoSansDigitP_s24c23w04.json -o mamefont/cpp/HL/include/ShapoSansDigitP_s24c23w04.hpp

mamefont/cpp/HM/include/ShapoSansDigitP_s24c23w04.hpp: mamefont/json/HM/ShapoSansDigitP_s24c23w04.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HM/ShapoSansDigitP_s24c23w04.json -o mamefont/cpp/HM/include/ShapoSansDigitP_s24c23w04.hpp

mamefont/cpp/VL/include/ShapoSansDigitP_s24c23w04.hpp: mamefont/json/VL/ShapoSansDigitP_s24c23w04.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VL/ShapoSansDigitP_s24c23w04.json -o mamefont/cpp/VL/include/ShapoSansDigitP_s24c23w04.hpp

mamefont/cpp/VM/include/ShapoSansDigitP_s24c23w04.hpp: mamefont/json/VM/ShapoSansDigitP_s24c23w04.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VM/ShapoSansDigitP_s24c23w04.json -o mamefont/cpp/VM/include/ShapoSansDigitP_s24c23w04.hpp

mamefont/json/HL/ShapoSansDigitP_s24c23w04.json: design/ShapoSansDigitP_s24c23w04/design.png design/ShapoSansDigitP_s24c23w04/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HL -i design/ShapoSansDigitP_s24c23w04/design.png -o $@

mamefont/json/HM/ShapoSansDigitP_s24c23w04.json: design/ShapoSansDigitP_s24c23w04/design.png design/ShapoSansDigitP_s24c23w04/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HM -i design/ShapoSansDigitP_s24c23w04/design.png -o $@

mamefont/json/VL/ShapoSansDigitP_s24c23w04.json: design/ShapoSansDigitP_s24c23w04/design.png design/ShapoSansDigitP_s24c23w04/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VL -i design/ShapoSansDigitP_s24c23w04/design.png -o $@

mamefont/json/VM/ShapoSansDigitP_s24c23w04.json: design/ShapoSansDigitP_s24c23w04/design.png design/ShapoSansDigitP_s24c23w04/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VM -i design/ShapoSansDigitP_s24c23w04/design.png -o $@

img/sample/ShapoSansDigitP_s24c23w04.png: design/ShapoSansDigitP_s24c23w04/design.png design/ShapoSansDigitP_s24c23w04/design.json $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --sample_img $@ -i design/ShapoSansDigitP_s24c23w04

gfxfont/cpp/include/ShapoSansP_s07c05a01.h: design/ShapoSansP_s07c05a01/design.png design/ShapoSansP_s07c05a01/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/ShapoSansP_s07c05a01

mamefont/cpp/HL/include/ShapoSansP_s07c05a01.hpp: mamefont/json/HL/ShapoSansP_s07c05a01.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HL/ShapoSansP_s07c05a01.json -o mamefont/cpp/HL/include/ShapoSansP_s07c05a01.hpp

mamefont/cpp/HM/include/ShapoSansP_s07c05a01.hpp: mamefont/json/HM/ShapoSansP_s07c05a01.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HM/ShapoSansP_s07c05a01.json -o mamefont/cpp/HM/include/ShapoSansP_s07c05a01.hpp

mamefont/cpp/VL/include/ShapoSansP_s07c05a01.hpp: mamefont/json/VL/ShapoSansP_s07c05a01.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VL/ShapoSansP_s07c05a01.json -o mamefont/cpp/VL/include/ShapoSansP_s07c05a01.hpp

mamefont/cpp/VM/include/ShapoSansP_s07c05a01.hpp: mamefont/json/VM/ShapoSansP_s07c05a01.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VM/ShapoSansP_s07c05a01.json -o mamefont/cpp/VM/include/ShapoSansP_s07c05a01.hpp

mamefont/json/HL/ShapoSansP_s07c05a01.json: design/ShapoSansP_s07c05a01/design.png design/ShapoSansP_s07c05a01/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HL -i design/ShapoSansP_s07c05a01/design.png -o $@

mamefont/json/HM/ShapoSansP_s07c05a01.json: design/ShapoSansP_s07c05a01/design.png design/ShapoSansP_s07c05a01/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HM -i design/ShapoSansP_s07c05a01/design.png -o $@

mamefont/json/VL/ShapoSansP_s07c05a01.json: design/ShapoSansP_s07c05a01/design.png design/ShapoSansP_s07c05a01/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VL -i design/ShapoSansP_s07c05a01/design.png -o $@

mamefont/json/VM/ShapoSansP_s07c05a01.json: design/ShapoSansP_s07c05a01/design.png design/ShapoSansP_s07c05a01/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VM -i design/ShapoSansP_s07c05a01/design.png -o $@

img/sample/ShapoSansP_s07c05a01.png: design/ShapoSansP_s07c05a01/design.png design/ShapoSansP_s07c05a01/design.json $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --sample_img $@ -i design/ShapoSansP_s07c05a01

gfxfont/cpp/include/ShapoSansP_s05.h: design/ShapoSansP_s05/design.png design/ShapoSansP_s05/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/ShapoSansP_s05

mamefont/cpp/HL/include/ShapoSansP_s05.hpp: mamefont/json/HL/ShapoSansP_s05.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HL/ShapoSansP_s05.json -o mamefont/cpp/HL/include/ShapoSansP_s05.hpp

mamefont/cpp/HM/include/ShapoSansP_s05.hpp: mamefont/json/HM/ShapoSansP_s05.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HM/ShapoSansP_s05.json -o mamefont/cpp/HM/include/ShapoSansP_s05.hpp

mamefont/cpp/VL/include/ShapoSansP_s05.hpp: mamefont/json/VL/ShapoSansP_s05.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VL/ShapoSansP_s05.json -o mamefont/cpp/VL/include/ShapoSansP_s05.hpp

mamefont/cpp/VM/include/ShapoSansP_s05.hpp: mamefont/json/VM/ShapoSansP_s05.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VM/ShapoSansP_s05.json -o mamefont/cpp/VM/include/ShapoSansP_s05.hpp

mamefont/json/HL/ShapoSansP_s05.json: design/ShapoSansP_s05/design.png design/ShapoSansP_s05/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HL -i design/ShapoSansP_s05/design.png -o $@

mamefont/json/HM/ShapoSansP_s05.json: design/ShapoSansP_s05/design.png design/ShapoSansP_s05/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HM -i design/ShapoSansP_s05/design.png -o $@

mamefont/json/VL/ShapoSansP_s05.json: design/ShapoSansP_s05/design.png design/ShapoSansP_s05/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VL -i design/ShapoSansP_s05/design.png -o $@

mamefont/json/VM/ShapoSansP_s05.json: design/ShapoSansP_s05/design.png design/ShapoSansP_s05/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VM -i design/ShapoSansP_s05/design.png -o $@

img/sample/ShapoSansP_s05.png: design/ShapoSansP_s05/design.png design/ShapoSansP_s05/design.json $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --sample_img $@ -i design/ShapoSansP_s05

gfxfont/cpp/include/ShapoSansDigitP_s16c14w02.h: design/ShapoSansDigitP_s16c14w02/design.png design/ShapoSansDigitP_s16c14w02/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/ShapoSansDigitP_s16c14w02

mamefont/cpp/HL/include/ShapoSansDigitP_s16c14w02.hpp: mamefont/json/HL/ShapoSansDigitP_s16c14w02.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HL/ShapoSansDigitP_s16c14w02.json -o mamefont/cpp/HL/include/ShapoSansDigitP_s16c14w02.hpp

mamefont/cpp/HM/include/ShapoSansDigitP_s16c14w02.hpp: mamefont/json/HM/ShapoSansDigitP_s16c14w02.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HM/ShapoSansDigitP_s16c14w02.json -o mamefont/cpp/HM/include/ShapoSansDigitP_s16c14w02.hpp

mamefont/cpp/VL/include/ShapoSansDigitP_s16c14w02.hpp: mamefont/json/VL/ShapoSansDigitP_s16c14w02.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VL/ShapoSansDigitP_s16c14w02.json -o mamefont/cpp/VL/include/ShapoSansDigitP_s16c14w02.hpp

mamefont/cpp/VM/include/ShapoSansDigitP_s16c14w02.hpp: mamefont/json/VM/ShapoSansDigitP_s16c14w02.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VM/ShapoSansDigitP_s16c14w02.json -o mamefont/cpp/VM/include/ShapoSansDigitP_s16c14w02.hpp

mamefont/json/HL/ShapoSansDigitP_s16c14w02.json: design/ShapoSansDigitP_s16c14w02/design.png design/ShapoSansDigitP_s16c14w02/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HL -i design/ShapoSansDigitP_s16c14w02/design.png -o $@

mamefont/json/HM/ShapoSansDigitP_s16c14w02.json: design/ShapoSansDigitP_s16c14w02/design.png design/ShapoSansDigitP_s16c14w02/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HM -i design/ShapoSansDigitP_s16c14w02/design.png -o $@

mamefont/json/VL/ShapoSansDigitP_s16c14w02.json: design/ShapoSansDigitP_s16c14w02/design.png design/ShapoSansDigitP_s16c14w02/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VL -i design/ShapoSansDigitP_s16c14w02/design.png -o $@

mamefont/json/VM/ShapoSansDigitP_s16c14w02.json: design/ShapoSansDigitP_s16c14w02/design.png design/ShapoSansDigitP_s16c14w02/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VM -i design/ShapoSansDigitP_s16c14w02/design.png -o $@

img/sample/ShapoSansDigitP_s16c14w02.png: design/ShapoSansDigitP_s16c14w02/design.png design/ShapoSansDigitP_s16c14w02/design.json $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --sample_img $@ -i design/ShapoSansDigitP_s16c14w02

gfxfont/cpp/include/TestF_s16w04.h: design/TestF_s16w04/design.png design/TestF_s16w04/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/TestF_s16w04

mamefont/cpp/HL/include/TestF_s16w04.hpp: mamefont/json/HL/TestF_s16w04.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HL/TestF_s16w04.json -o mamefont/cpp/HL/include/TestF_s16w04.hpp

mamefont/cpp/HM/include/TestF_s16w04.hpp: mamefont/json/HM/TestF_s16w04.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HM/TestF_s16w04.json -o mamefont/cpp/HM/include/TestF_s16w04.hpp

mamefont/cpp/VL/include/TestF_s16w04.hpp: mamefont/json/VL/TestF_s16w04.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VL/TestF_s16w04.json -o mamefont/cpp/VL/include/TestF_s16w04.hpp

mamefont/cpp/VM/include/TestF_s16w04.hpp: mamefont/json/VM/TestF_s16w04.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VM/TestF_s16w04.json -o mamefont/cpp/VM/include/TestF_s16w04.hpp

mamefont/json/HL/TestF_s16w04.json: design/TestF_s16w04/design.png design/TestF_s16w04/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HL -i design/TestF_s16w04/design.png -o $@

mamefont/json/HM/TestF_s16w04.json: design/TestF_s16w04/design.png design/TestF_s16w04/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HM -i design/TestF_s16w04/design.png -o $@

mamefont/json/VL/TestF_s16w04.json: design/TestF_s16w04/design.png design/TestF_s16w04/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VL -i design/TestF_s16w04/design.png -o $@

mamefont/json/VM/TestF_s16w04.json: design/TestF_s16w04/design.png design/TestF_s16w04/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VM -i design/TestF_s16w04/design.png -o $@

img/sample/TestF_s16w04.png: design/TestF_s16w04/design.png design/TestF_s16w04/design.json $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --sample_img $@ -i design/TestF_s16w04

gfxfont/cpp/include/TestF_s08w02.h: design/TestF_s08w02/design.png design/TestF_s08w02/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/TestF_s08w02

mamefont/cpp/HL/include/TestF_s08w02.hpp: mamefont/json/HL/TestF_s08w02.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HL/TestF_s08w02.json -o mamefont/cpp/HL/include/TestF_s08w02.hpp

mamefont/cpp/HM/include/TestF_s08w02.hpp: mamefont/json/HM/TestF_s08w02.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HM/TestF_s08w02.json -o mamefont/cpp/HM/include/TestF_s08w02.hpp

mamefont/cpp/VL/include/TestF_s08w02.hpp: mamefont/json/VL/TestF_s08w02.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VL/TestF_s08w02.json -o mamefont/cpp/VL/include/TestF_s08w02.hpp

mamefont/cpp/VM/include/TestF_s08w02.hpp: mamefont/json/VM/TestF_s08w02.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VM/TestF_s08w02.json -o mamefont/cpp/VM/include/TestF_s08w02.hpp

mamefont/json/HL/TestF_s08w02.json: design/TestF_s08w02/design.png design/TestF_s08w02/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HL -i design/TestF_s08w02/design.png -o $@

mamefont/json/HM/TestF_s08w02.json: design/TestF_s08w02/design.png design/TestF_s08w02/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HM -i design/TestF_s08w02/design.png -o $@

mamefont/json/VL/TestF_s08w02.json: design/TestF_s08w02/design.png design/TestF_s08w02/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VL -i design/TestF_s08w02/design.png -o $@

mamefont/json/VM/TestF_s08w02.json: design/TestF_s08w02/design.png design/TestF_s08w02/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VM -i design/TestF_s08w02/design.png -o $@

img/sample/TestF_s08w02.png: design/TestF_s08w02/design.png design/TestF_s08w02/design.json $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --sample_img $@ -i design/TestF_s08w02

gfxfont/cpp/include/Empty_s01.h: design/Empty_s01/design.png design/Empty_s01/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/Empty_s01

mamefont/cpp/HL/include/Empty_s01.hpp: mamefont/json/HL/Empty_s01.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HL/Empty_s01.json -o mamefont/cpp/HL/include/Empty_s01.hpp

mamefont/cpp/HM/include/Empty_s01.hpp: mamefont/json/HM/Empty_s01.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/HM/Empty_s01.json -o mamefont/cpp/HM/include/Empty_s01.hpp

mamefont/cpp/VL/include/Empty_s01.hpp: mamefont/json/VL/Empty_s01.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VL/Empty_s01.json -o mamefont/cpp/VL/include/Empty_s01.hpp

mamefont/cpp/VM/include/Empty_s01.hpp: mamefont/json/VM/Empty_s01.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -i mamefont/json/VM/Empty_s01.json -o mamefont/cpp/VM/include/Empty_s01.hpp

mamefont/json/HL/Empty_s01.json: design/Empty_s01/design.png design/Empty_s01/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HL -i design/Empty_s01/design.png -o $@

mamefont/json/HM/Empty_s01.json: design/Empty_s01/design.png design/Empty_s01/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e HM -i design/Empty_s01/design.png -o $@

mamefont/json/VL/Empty_s01.json: design/Empty_s01/design.png design/Empty_s01/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VL -i design/Empty_s01/design.png -o $@

mamefont/json/VM/Empty_s01.json: design/Empty_s01/design.png design/Empty_s01/design.json $(CMD_MAMEC) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_MAMEC) -e VM -i design/Empty_s01/design.png -o $@

img/sample/Empty_s01.png: design/Empty_s01/design.png design/Empty_s01/design.json $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --sample_img $@ -i design/Empty_s01

distclean_all: distclean_gfx_all distclean_mame_all distclean_sample_all

distclean_gfx_all:
	rm -f gfxfont/cpp/include/*.h

distclean_mame_all: distclean_mame_HL distclean_mame_HM distclean_mame_VL distclean_mame_VM
distclean_mame_HL:
	rm -f mamefont/cpp/HL/include/*.hpp
	rm -f mamefont/json/HL/*.json

distclean_mame_HM:
	rm -f mamefont/cpp/HM/include/*.hpp
	rm -f mamefont/json/HM/*.json

distclean_mame_VL:
	rm -f mamefont/cpp/VL/include/*.hpp
	rm -f mamefont/json/VL/*.json

distclean_mame_VM:
	rm -f mamefont/cpp/VM/include/*.hpp
	rm -f mamefont/json/VM/*.json

distclean_mame_cpp:
	rm -f mamefont/cpp/HL/include/*.hpp
	rm -f mamefont/cpp/HM/include/*.hpp
	rm -f mamefont/cpp/VL/include/*.hpp
	rm -f mamefont/cpp/VM/include/*.hpp

distclean_mame_json:
	rm -f mamefont/json/HL/*.json
	rm -f mamefont/json/HM/*.json
	rm -f mamefont/json/VL/*.json
	rm -f mamefont/json/VM/*.json

distclean_sample_all:
	rm -f img/sample/*.png

