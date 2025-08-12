.PHONY: gfx_all mame_all
.PHONY: mame_HL mame_HM mame_VL mame_VM
.PHONY: mame_cpp mame_json
.PHONY: distclean_all distclean_gfx_all distclean_mame_all
.PHONY: distclean_mame_HL distclean_mame_HM distclean_mame_VL distclean_mame_VM
.PHONY: distclean_mame_cpp distclean_mame_json

all: gfx_all mame_all

GFX_HEADER_LIST = \
	gfxfont/cpp/include/MameSansP_s48c40w08.h \
	gfxfont/cpp/include/MameSquareWide_s64c48a04w16.h \
	gfxfont/cpp/include/ShapoSansP_s27c22a01w04.h \
	gfxfont/cpp/include/ShapoSansP_s21c16a01w03.h \
	gfxfont/cpp/include/MameSansDigitP_s64w08.h \
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
	mamefont/cpp/HL/include/ShapoSansP_s21c16a01w03.hpp \
	mamefont/cpp/HL/include/MameSansDigitP_s64w08.hpp \
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

MAME_HL_CPP_LIST = \
	mamefont/cpp/HL/src/MameSansP_s48c40w08.cpp \
	mamefont/cpp/HL/src/MameSquareWide_s64c48a04w16.cpp \
	mamefont/cpp/HL/src/ShapoSansP_s27c22a01w04.cpp \
	mamefont/cpp/HL/src/ShapoSansP_s21c16a01w03.cpp \
	mamefont/cpp/HL/src/MameSansDigitP_s64w08.cpp \
	mamefont/cpp/HL/src/MameSeg7_s40c38w06.cpp \
	mamefont/cpp/HL/src/ShapoSansP_s12c09a01w02.cpp \
	mamefont/cpp/HL/src/ShapoSansP_s08c07.cpp \
	mamefont/cpp/HL/src/ShapoSansMono_s08c07.cpp \
	mamefont/cpp/HL/src/ShapoSansDigitP_s32c30w04.cpp \
	mamefont/cpp/HL/src/ShapoSansDigitP_s24c23w04.cpp \
	mamefont/cpp/HL/src/ShapoSansP_s07c05a01.cpp \
	mamefont/cpp/HL/src/ShapoSansP_s05.cpp \
	mamefont/cpp/HL/src/ShapoSansDigitP_s16c14w02.cpp \
	mamefont/cpp/HL/src/TestF_s16w04.cpp \
	mamefont/cpp/HL/src/TestF_s08w02.cpp \
	mamefont/cpp/HL/src/Empty_s01.cpp

MAME_HL_JSON_LIST = \
	mamefont/json/HL/MameSansP_s48c40w08.json \
	mamefont/json/HL/MameSquareWide_s64c48a04w16.json \
	mamefont/json/HL/ShapoSansP_s27c22a01w04.json \
	mamefont/json/HL/ShapoSansP_s21c16a01w03.json \
	mamefont/json/HL/MameSansDigitP_s64w08.json \
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
	mamefont/cpp/HM/include/ShapoSansP_s21c16a01w03.hpp \
	mamefont/cpp/HM/include/MameSansDigitP_s64w08.hpp \
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

MAME_HM_CPP_LIST = \
	mamefont/cpp/HM/src/MameSansP_s48c40w08.cpp \
	mamefont/cpp/HM/src/MameSquareWide_s64c48a04w16.cpp \
	mamefont/cpp/HM/src/ShapoSansP_s27c22a01w04.cpp \
	mamefont/cpp/HM/src/ShapoSansP_s21c16a01w03.cpp \
	mamefont/cpp/HM/src/MameSansDigitP_s64w08.cpp \
	mamefont/cpp/HM/src/MameSeg7_s40c38w06.cpp \
	mamefont/cpp/HM/src/ShapoSansP_s12c09a01w02.cpp \
	mamefont/cpp/HM/src/ShapoSansP_s08c07.cpp \
	mamefont/cpp/HM/src/ShapoSansMono_s08c07.cpp \
	mamefont/cpp/HM/src/ShapoSansDigitP_s32c30w04.cpp \
	mamefont/cpp/HM/src/ShapoSansDigitP_s24c23w04.cpp \
	mamefont/cpp/HM/src/ShapoSansP_s07c05a01.cpp \
	mamefont/cpp/HM/src/ShapoSansP_s05.cpp \
	mamefont/cpp/HM/src/ShapoSansDigitP_s16c14w02.cpp \
	mamefont/cpp/HM/src/TestF_s16w04.cpp \
	mamefont/cpp/HM/src/TestF_s08w02.cpp \
	mamefont/cpp/HM/src/Empty_s01.cpp

MAME_HM_JSON_LIST = \
	mamefont/json/HM/MameSansP_s48c40w08.json \
	mamefont/json/HM/MameSquareWide_s64c48a04w16.json \
	mamefont/json/HM/ShapoSansP_s27c22a01w04.json \
	mamefont/json/HM/ShapoSansP_s21c16a01w03.json \
	mamefont/json/HM/MameSansDigitP_s64w08.json \
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
	mamefont/cpp/VL/include/ShapoSansP_s21c16a01w03.hpp \
	mamefont/cpp/VL/include/MameSansDigitP_s64w08.hpp \
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

MAME_VL_CPP_LIST = \
	mamefont/cpp/VL/src/MameSansP_s48c40w08.cpp \
	mamefont/cpp/VL/src/MameSquareWide_s64c48a04w16.cpp \
	mamefont/cpp/VL/src/ShapoSansP_s27c22a01w04.cpp \
	mamefont/cpp/VL/src/ShapoSansP_s21c16a01w03.cpp \
	mamefont/cpp/VL/src/MameSansDigitP_s64w08.cpp \
	mamefont/cpp/VL/src/MameSeg7_s40c38w06.cpp \
	mamefont/cpp/VL/src/ShapoSansP_s12c09a01w02.cpp \
	mamefont/cpp/VL/src/ShapoSansP_s08c07.cpp \
	mamefont/cpp/VL/src/ShapoSansMono_s08c07.cpp \
	mamefont/cpp/VL/src/ShapoSansDigitP_s32c30w04.cpp \
	mamefont/cpp/VL/src/ShapoSansDigitP_s24c23w04.cpp \
	mamefont/cpp/VL/src/ShapoSansP_s07c05a01.cpp \
	mamefont/cpp/VL/src/ShapoSansP_s05.cpp \
	mamefont/cpp/VL/src/ShapoSansDigitP_s16c14w02.cpp \
	mamefont/cpp/VL/src/TestF_s16w04.cpp \
	mamefont/cpp/VL/src/TestF_s08w02.cpp \
	mamefont/cpp/VL/src/Empty_s01.cpp

MAME_VL_JSON_LIST = \
	mamefont/json/VL/MameSansP_s48c40w08.json \
	mamefont/json/VL/MameSquareWide_s64c48a04w16.json \
	mamefont/json/VL/ShapoSansP_s27c22a01w04.json \
	mamefont/json/VL/ShapoSansP_s21c16a01w03.json \
	mamefont/json/VL/MameSansDigitP_s64w08.json \
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
	mamefont/cpp/VM/include/ShapoSansP_s21c16a01w03.hpp \
	mamefont/cpp/VM/include/MameSansDigitP_s64w08.hpp \
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

MAME_VM_CPP_LIST = \
	mamefont/cpp/VM/src/MameSansP_s48c40w08.cpp \
	mamefont/cpp/VM/src/MameSquareWide_s64c48a04w16.cpp \
	mamefont/cpp/VM/src/ShapoSansP_s27c22a01w04.cpp \
	mamefont/cpp/VM/src/ShapoSansP_s21c16a01w03.cpp \
	mamefont/cpp/VM/src/MameSansDigitP_s64w08.cpp \
	mamefont/cpp/VM/src/MameSeg7_s40c38w06.cpp \
	mamefont/cpp/VM/src/ShapoSansP_s12c09a01w02.cpp \
	mamefont/cpp/VM/src/ShapoSansP_s08c07.cpp \
	mamefont/cpp/VM/src/ShapoSansMono_s08c07.cpp \
	mamefont/cpp/VM/src/ShapoSansDigitP_s32c30w04.cpp \
	mamefont/cpp/VM/src/ShapoSansDigitP_s24c23w04.cpp \
	mamefont/cpp/VM/src/ShapoSansP_s07c05a01.cpp \
	mamefont/cpp/VM/src/ShapoSansP_s05.cpp \
	mamefont/cpp/VM/src/ShapoSansDigitP_s16c14w02.cpp \
	mamefont/cpp/VM/src/TestF_s16w04.cpp \
	mamefont/cpp/VM/src/TestF_s08w02.cpp \
	mamefont/cpp/VM/src/Empty_s01.cpp

MAME_VM_JSON_LIST = \
	mamefont/json/VM/MameSansP_s48c40w08.json \
	mamefont/json/VM/MameSquareWide_s64c48a04w16.json \
	mamefont/json/VM/ShapoSansP_s27c22a01w04.json \
	mamefont/json/VM/ShapoSansP_s21c16a01w03.json \
	mamefont/json/VM/MameSansDigitP_s64w08.json \
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


gfx_all: $(GFX_HEADER_LIST)

mame_all: mame_HL mame_HM mame_VL mame_VM
mame_HL: $(MAME_HL_HPP_LIST) $(MAME_HL_JSON_LIST)
mame_HM: $(MAME_HM_HPP_LIST) $(MAME_HM_JSON_LIST)
mame_VL: $(MAME_VL_HPP_LIST) $(MAME_VL_JSON_LIST)
mame_VM: $(MAME_VM_HPP_LIST) $(MAME_VM_JSON_LIST)
mame_cpp: $(MAME_HL_HPP_LIST) $(MAME_HM_HPP_LIST) $(MAME_VL_HPP_LIST) $(MAME_VM_HPP_LIST)
mame_json: $(MAME_HL_JSON_LIST) $(MAME_HM_JSON_LIST) $(MAME_VL_JSON_LIST) $(MAME_VM_JSON_LIST)

gfxfont/cpp/include/MameSansP_s48c40w08.h: design/MameSansP_s48c40w08/design.png design/MameSansP_s48c40w08/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/MameSansP_s48c40w08

mamefont/cpp/HL/include/MameSansP_s48c40w08.hpp: mamefont/cpp/HL/src/MameSansP_s48c40w08.cpp
mamefont/cpp/HL/src/MameSansP_s48c40w08.cpp: design/MameSansP_s48c40w08/design.png design/MameSansP_s48c40w08/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_hpp mamefont/cpp/HL/include --outdir_mame_cpp $(dir $@) -i design/MameSansP_s48c40w08

mamefont/cpp/HM/include/MameSansP_s48c40w08.hpp: mamefont/cpp/HM/src/MameSansP_s48c40w08.cpp
mamefont/cpp/HM/src/MameSansP_s48c40w08.cpp: design/MameSansP_s48c40w08/design.png design/MameSansP_s48c40w08/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_hpp mamefont/cpp/HM/include --outdir_mame_cpp $(dir $@) -i design/MameSansP_s48c40w08

mamefont/cpp/VL/include/MameSansP_s48c40w08.hpp: mamefont/cpp/VL/src/MameSansP_s48c40w08.cpp
mamefont/cpp/VL/src/MameSansP_s48c40w08.cpp: design/MameSansP_s48c40w08/design.png design/MameSansP_s48c40w08/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_hpp mamefont/cpp/VL/include --outdir_mame_cpp $(dir $@) -i design/MameSansP_s48c40w08

mamefont/cpp/VM/include/MameSansP_s48c40w08.hpp: mamefont/cpp/VM/src/MameSansP_s48c40w08.cpp
mamefont/cpp/VM/src/MameSansP_s48c40w08.cpp: design/MameSansP_s48c40w08/design.png design/MameSansP_s48c40w08/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_hpp mamefont/cpp/VM/include --outdir_mame_cpp $(dir $@) -i design/MameSansP_s48c40w08

mamefont/json/HL/MameSansP_s48c40w08.json: design/MameSansP_s48c40w08/design.png design/MameSansP_s48c40w08/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_json $(dir $@) -i design/MameSansP_s48c40w08

mamefont/json/HM/MameSansP_s48c40w08.json: design/MameSansP_s48c40w08/design.png design/MameSansP_s48c40w08/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_json $(dir $@) -i design/MameSansP_s48c40w08

mamefont/json/VL/MameSansP_s48c40w08.json: design/MameSansP_s48c40w08/design.png design/MameSansP_s48c40w08/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_json $(dir $@) -i design/MameSansP_s48c40w08

mamefont/json/VM/MameSansP_s48c40w08.json: design/MameSansP_s48c40w08/design.png design/MameSansP_s48c40w08/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_json $(dir $@) -i design/MameSansP_s48c40w08

gfxfont/cpp/include/MameSquareWide_s64c48a04w16.h: design/MameSquareWide_s64c48a04w16/design.png design/MameSquareWide_s64c48a04w16/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/MameSquareWide_s64c48a04w16

mamefont/cpp/HL/include/MameSquareWide_s64c48a04w16.hpp: mamefont/cpp/HL/src/MameSquareWide_s64c48a04w16.cpp
mamefont/cpp/HL/src/MameSquareWide_s64c48a04w16.cpp: design/MameSquareWide_s64c48a04w16/design.png design/MameSquareWide_s64c48a04w16/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_hpp mamefont/cpp/HL/include --outdir_mame_cpp $(dir $@) -i design/MameSquareWide_s64c48a04w16

mamefont/cpp/HM/include/MameSquareWide_s64c48a04w16.hpp: mamefont/cpp/HM/src/MameSquareWide_s64c48a04w16.cpp
mamefont/cpp/HM/src/MameSquareWide_s64c48a04w16.cpp: design/MameSquareWide_s64c48a04w16/design.png design/MameSquareWide_s64c48a04w16/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_hpp mamefont/cpp/HM/include --outdir_mame_cpp $(dir $@) -i design/MameSquareWide_s64c48a04w16

mamefont/cpp/VL/include/MameSquareWide_s64c48a04w16.hpp: mamefont/cpp/VL/src/MameSquareWide_s64c48a04w16.cpp
mamefont/cpp/VL/src/MameSquareWide_s64c48a04w16.cpp: design/MameSquareWide_s64c48a04w16/design.png design/MameSquareWide_s64c48a04w16/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_hpp mamefont/cpp/VL/include --outdir_mame_cpp $(dir $@) -i design/MameSquareWide_s64c48a04w16

mamefont/cpp/VM/include/MameSquareWide_s64c48a04w16.hpp: mamefont/cpp/VM/src/MameSquareWide_s64c48a04w16.cpp
mamefont/cpp/VM/src/MameSquareWide_s64c48a04w16.cpp: design/MameSquareWide_s64c48a04w16/design.png design/MameSquareWide_s64c48a04w16/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_hpp mamefont/cpp/VM/include --outdir_mame_cpp $(dir $@) -i design/MameSquareWide_s64c48a04w16

mamefont/json/HL/MameSquareWide_s64c48a04w16.json: design/MameSquareWide_s64c48a04w16/design.png design/MameSquareWide_s64c48a04w16/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_json $(dir $@) -i design/MameSquareWide_s64c48a04w16

mamefont/json/HM/MameSquareWide_s64c48a04w16.json: design/MameSquareWide_s64c48a04w16/design.png design/MameSquareWide_s64c48a04w16/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_json $(dir $@) -i design/MameSquareWide_s64c48a04w16

mamefont/json/VL/MameSquareWide_s64c48a04w16.json: design/MameSquareWide_s64c48a04w16/design.png design/MameSquareWide_s64c48a04w16/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_json $(dir $@) -i design/MameSquareWide_s64c48a04w16

mamefont/json/VM/MameSquareWide_s64c48a04w16.json: design/MameSquareWide_s64c48a04w16/design.png design/MameSquareWide_s64c48a04w16/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_json $(dir $@) -i design/MameSquareWide_s64c48a04w16

gfxfont/cpp/include/ShapoSansP_s27c22a01w04.h: design/ShapoSansP_s27c22a01w04/design.png design/ShapoSansP_s27c22a01w04/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/ShapoSansP_s27c22a01w04

mamefont/cpp/HL/include/ShapoSansP_s27c22a01w04.hpp: mamefont/cpp/HL/src/ShapoSansP_s27c22a01w04.cpp
mamefont/cpp/HL/src/ShapoSansP_s27c22a01w04.cpp: design/ShapoSansP_s27c22a01w04/design.png design/ShapoSansP_s27c22a01w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_hpp mamefont/cpp/HL/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s27c22a01w04

mamefont/cpp/HM/include/ShapoSansP_s27c22a01w04.hpp: mamefont/cpp/HM/src/ShapoSansP_s27c22a01w04.cpp
mamefont/cpp/HM/src/ShapoSansP_s27c22a01w04.cpp: design/ShapoSansP_s27c22a01w04/design.png design/ShapoSansP_s27c22a01w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_hpp mamefont/cpp/HM/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s27c22a01w04

mamefont/cpp/VL/include/ShapoSansP_s27c22a01w04.hpp: mamefont/cpp/VL/src/ShapoSansP_s27c22a01w04.cpp
mamefont/cpp/VL/src/ShapoSansP_s27c22a01w04.cpp: design/ShapoSansP_s27c22a01w04/design.png design/ShapoSansP_s27c22a01w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_hpp mamefont/cpp/VL/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s27c22a01w04

mamefont/cpp/VM/include/ShapoSansP_s27c22a01w04.hpp: mamefont/cpp/VM/src/ShapoSansP_s27c22a01w04.cpp
mamefont/cpp/VM/src/ShapoSansP_s27c22a01w04.cpp: design/ShapoSansP_s27c22a01w04/design.png design/ShapoSansP_s27c22a01w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_hpp mamefont/cpp/VM/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s27c22a01w04

mamefont/json/HL/ShapoSansP_s27c22a01w04.json: design/ShapoSansP_s27c22a01w04/design.png design/ShapoSansP_s27c22a01w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_json $(dir $@) -i design/ShapoSansP_s27c22a01w04

mamefont/json/HM/ShapoSansP_s27c22a01w04.json: design/ShapoSansP_s27c22a01w04/design.png design/ShapoSansP_s27c22a01w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_json $(dir $@) -i design/ShapoSansP_s27c22a01w04

mamefont/json/VL/ShapoSansP_s27c22a01w04.json: design/ShapoSansP_s27c22a01w04/design.png design/ShapoSansP_s27c22a01w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_json $(dir $@) -i design/ShapoSansP_s27c22a01w04

mamefont/json/VM/ShapoSansP_s27c22a01w04.json: design/ShapoSansP_s27c22a01w04/design.png design/ShapoSansP_s27c22a01w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_json $(dir $@) -i design/ShapoSansP_s27c22a01w04

gfxfont/cpp/include/ShapoSansP_s21c16a01w03.h: design/ShapoSansP_s21c16a01w03/design.png design/ShapoSansP_s21c16a01w03/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/ShapoSansP_s21c16a01w03

mamefont/cpp/HL/include/ShapoSansP_s21c16a01w03.hpp: mamefont/cpp/HL/src/ShapoSansP_s21c16a01w03.cpp
mamefont/cpp/HL/src/ShapoSansP_s21c16a01w03.cpp: design/ShapoSansP_s21c16a01w03/design.png design/ShapoSansP_s21c16a01w03/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_hpp mamefont/cpp/HL/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s21c16a01w03

mamefont/cpp/HM/include/ShapoSansP_s21c16a01w03.hpp: mamefont/cpp/HM/src/ShapoSansP_s21c16a01w03.cpp
mamefont/cpp/HM/src/ShapoSansP_s21c16a01w03.cpp: design/ShapoSansP_s21c16a01w03/design.png design/ShapoSansP_s21c16a01w03/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_hpp mamefont/cpp/HM/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s21c16a01w03

mamefont/cpp/VL/include/ShapoSansP_s21c16a01w03.hpp: mamefont/cpp/VL/src/ShapoSansP_s21c16a01w03.cpp
mamefont/cpp/VL/src/ShapoSansP_s21c16a01w03.cpp: design/ShapoSansP_s21c16a01w03/design.png design/ShapoSansP_s21c16a01w03/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_hpp mamefont/cpp/VL/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s21c16a01w03

mamefont/cpp/VM/include/ShapoSansP_s21c16a01w03.hpp: mamefont/cpp/VM/src/ShapoSansP_s21c16a01w03.cpp
mamefont/cpp/VM/src/ShapoSansP_s21c16a01w03.cpp: design/ShapoSansP_s21c16a01w03/design.png design/ShapoSansP_s21c16a01w03/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_hpp mamefont/cpp/VM/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s21c16a01w03

mamefont/json/HL/ShapoSansP_s21c16a01w03.json: design/ShapoSansP_s21c16a01w03/design.png design/ShapoSansP_s21c16a01w03/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_json $(dir $@) -i design/ShapoSansP_s21c16a01w03

mamefont/json/HM/ShapoSansP_s21c16a01w03.json: design/ShapoSansP_s21c16a01w03/design.png design/ShapoSansP_s21c16a01w03/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_json $(dir $@) -i design/ShapoSansP_s21c16a01w03

mamefont/json/VL/ShapoSansP_s21c16a01w03.json: design/ShapoSansP_s21c16a01w03/design.png design/ShapoSansP_s21c16a01w03/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_json $(dir $@) -i design/ShapoSansP_s21c16a01w03

mamefont/json/VM/ShapoSansP_s21c16a01w03.json: design/ShapoSansP_s21c16a01w03/design.png design/ShapoSansP_s21c16a01w03/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_json $(dir $@) -i design/ShapoSansP_s21c16a01w03

gfxfont/cpp/include/MameSansDigitP_s64w08.h: design/MameSansDigitP_s64w08/design.png design/MameSansDigitP_s64w08/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/MameSansDigitP_s64w08

mamefont/cpp/HL/include/MameSansDigitP_s64w08.hpp: mamefont/cpp/HL/src/MameSansDigitP_s64w08.cpp
mamefont/cpp/HL/src/MameSansDigitP_s64w08.cpp: design/MameSansDigitP_s64w08/design.png design/MameSansDigitP_s64w08/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_hpp mamefont/cpp/HL/include --outdir_mame_cpp $(dir $@) -i design/MameSansDigitP_s64w08

mamefont/cpp/HM/include/MameSansDigitP_s64w08.hpp: mamefont/cpp/HM/src/MameSansDigitP_s64w08.cpp
mamefont/cpp/HM/src/MameSansDigitP_s64w08.cpp: design/MameSansDigitP_s64w08/design.png design/MameSansDigitP_s64w08/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_hpp mamefont/cpp/HM/include --outdir_mame_cpp $(dir $@) -i design/MameSansDigitP_s64w08

mamefont/cpp/VL/include/MameSansDigitP_s64w08.hpp: mamefont/cpp/VL/src/MameSansDigitP_s64w08.cpp
mamefont/cpp/VL/src/MameSansDigitP_s64w08.cpp: design/MameSansDigitP_s64w08/design.png design/MameSansDigitP_s64w08/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_hpp mamefont/cpp/VL/include --outdir_mame_cpp $(dir $@) -i design/MameSansDigitP_s64w08

mamefont/cpp/VM/include/MameSansDigitP_s64w08.hpp: mamefont/cpp/VM/src/MameSansDigitP_s64w08.cpp
mamefont/cpp/VM/src/MameSansDigitP_s64w08.cpp: design/MameSansDigitP_s64w08/design.png design/MameSansDigitP_s64w08/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_hpp mamefont/cpp/VM/include --outdir_mame_cpp $(dir $@) -i design/MameSansDigitP_s64w08

mamefont/json/HL/MameSansDigitP_s64w08.json: design/MameSansDigitP_s64w08/design.png design/MameSansDigitP_s64w08/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_json $(dir $@) -i design/MameSansDigitP_s64w08

mamefont/json/HM/MameSansDigitP_s64w08.json: design/MameSansDigitP_s64w08/design.png design/MameSansDigitP_s64w08/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_json $(dir $@) -i design/MameSansDigitP_s64w08

mamefont/json/VL/MameSansDigitP_s64w08.json: design/MameSansDigitP_s64w08/design.png design/MameSansDigitP_s64w08/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_json $(dir $@) -i design/MameSansDigitP_s64w08

mamefont/json/VM/MameSansDigitP_s64w08.json: design/MameSansDigitP_s64w08/design.png design/MameSansDigitP_s64w08/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_json $(dir $@) -i design/MameSansDigitP_s64w08

gfxfont/cpp/include/MameSeg7_s40c38w06.h: design/MameSeg7_s40c38w06/design.png design/MameSeg7_s40c38w06/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/MameSeg7_s40c38w06

mamefont/cpp/HL/include/MameSeg7_s40c38w06.hpp: mamefont/cpp/HL/src/MameSeg7_s40c38w06.cpp
mamefont/cpp/HL/src/MameSeg7_s40c38w06.cpp: design/MameSeg7_s40c38w06/design.png design/MameSeg7_s40c38w06/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_hpp mamefont/cpp/HL/include --outdir_mame_cpp $(dir $@) -i design/MameSeg7_s40c38w06

mamefont/cpp/HM/include/MameSeg7_s40c38w06.hpp: mamefont/cpp/HM/src/MameSeg7_s40c38w06.cpp
mamefont/cpp/HM/src/MameSeg7_s40c38w06.cpp: design/MameSeg7_s40c38w06/design.png design/MameSeg7_s40c38w06/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_hpp mamefont/cpp/HM/include --outdir_mame_cpp $(dir $@) -i design/MameSeg7_s40c38w06

mamefont/cpp/VL/include/MameSeg7_s40c38w06.hpp: mamefont/cpp/VL/src/MameSeg7_s40c38w06.cpp
mamefont/cpp/VL/src/MameSeg7_s40c38w06.cpp: design/MameSeg7_s40c38w06/design.png design/MameSeg7_s40c38w06/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_hpp mamefont/cpp/VL/include --outdir_mame_cpp $(dir $@) -i design/MameSeg7_s40c38w06

mamefont/cpp/VM/include/MameSeg7_s40c38w06.hpp: mamefont/cpp/VM/src/MameSeg7_s40c38w06.cpp
mamefont/cpp/VM/src/MameSeg7_s40c38w06.cpp: design/MameSeg7_s40c38w06/design.png design/MameSeg7_s40c38w06/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_hpp mamefont/cpp/VM/include --outdir_mame_cpp $(dir $@) -i design/MameSeg7_s40c38w06

mamefont/json/HL/MameSeg7_s40c38w06.json: design/MameSeg7_s40c38w06/design.png design/MameSeg7_s40c38w06/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_json $(dir $@) -i design/MameSeg7_s40c38w06

mamefont/json/HM/MameSeg7_s40c38w06.json: design/MameSeg7_s40c38w06/design.png design/MameSeg7_s40c38w06/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_json $(dir $@) -i design/MameSeg7_s40c38w06

mamefont/json/VL/MameSeg7_s40c38w06.json: design/MameSeg7_s40c38w06/design.png design/MameSeg7_s40c38w06/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_json $(dir $@) -i design/MameSeg7_s40c38w06

mamefont/json/VM/MameSeg7_s40c38w06.json: design/MameSeg7_s40c38w06/design.png design/MameSeg7_s40c38w06/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_json $(dir $@) -i design/MameSeg7_s40c38w06

gfxfont/cpp/include/ShapoSansP_s12c09a01w02.h: design/ShapoSansP_s12c09a01w02/design.png design/ShapoSansP_s12c09a01w02/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/ShapoSansP_s12c09a01w02

mamefont/cpp/HL/include/ShapoSansP_s12c09a01w02.hpp: mamefont/cpp/HL/src/ShapoSansP_s12c09a01w02.cpp
mamefont/cpp/HL/src/ShapoSansP_s12c09a01w02.cpp: design/ShapoSansP_s12c09a01w02/design.png design/ShapoSansP_s12c09a01w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_hpp mamefont/cpp/HL/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s12c09a01w02

mamefont/cpp/HM/include/ShapoSansP_s12c09a01w02.hpp: mamefont/cpp/HM/src/ShapoSansP_s12c09a01w02.cpp
mamefont/cpp/HM/src/ShapoSansP_s12c09a01w02.cpp: design/ShapoSansP_s12c09a01w02/design.png design/ShapoSansP_s12c09a01w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_hpp mamefont/cpp/HM/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s12c09a01w02

mamefont/cpp/VL/include/ShapoSansP_s12c09a01w02.hpp: mamefont/cpp/VL/src/ShapoSansP_s12c09a01w02.cpp
mamefont/cpp/VL/src/ShapoSansP_s12c09a01w02.cpp: design/ShapoSansP_s12c09a01w02/design.png design/ShapoSansP_s12c09a01w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_hpp mamefont/cpp/VL/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s12c09a01w02

mamefont/cpp/VM/include/ShapoSansP_s12c09a01w02.hpp: mamefont/cpp/VM/src/ShapoSansP_s12c09a01w02.cpp
mamefont/cpp/VM/src/ShapoSansP_s12c09a01w02.cpp: design/ShapoSansP_s12c09a01w02/design.png design/ShapoSansP_s12c09a01w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_hpp mamefont/cpp/VM/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s12c09a01w02

mamefont/json/HL/ShapoSansP_s12c09a01w02.json: design/ShapoSansP_s12c09a01w02/design.png design/ShapoSansP_s12c09a01w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_json $(dir $@) -i design/ShapoSansP_s12c09a01w02

mamefont/json/HM/ShapoSansP_s12c09a01w02.json: design/ShapoSansP_s12c09a01w02/design.png design/ShapoSansP_s12c09a01w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_json $(dir $@) -i design/ShapoSansP_s12c09a01w02

mamefont/json/VL/ShapoSansP_s12c09a01w02.json: design/ShapoSansP_s12c09a01w02/design.png design/ShapoSansP_s12c09a01w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_json $(dir $@) -i design/ShapoSansP_s12c09a01w02

mamefont/json/VM/ShapoSansP_s12c09a01w02.json: design/ShapoSansP_s12c09a01w02/design.png design/ShapoSansP_s12c09a01w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_json $(dir $@) -i design/ShapoSansP_s12c09a01w02

gfxfont/cpp/include/ShapoSansP_s08c07.h: design/ShapoSansP_s08c07/design.png design/ShapoSansP_s08c07/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/ShapoSansP_s08c07

mamefont/cpp/HL/include/ShapoSansP_s08c07.hpp: mamefont/cpp/HL/src/ShapoSansP_s08c07.cpp
mamefont/cpp/HL/src/ShapoSansP_s08c07.cpp: design/ShapoSansP_s08c07/design.png design/ShapoSansP_s08c07/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_hpp mamefont/cpp/HL/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s08c07

mamefont/cpp/HM/include/ShapoSansP_s08c07.hpp: mamefont/cpp/HM/src/ShapoSansP_s08c07.cpp
mamefont/cpp/HM/src/ShapoSansP_s08c07.cpp: design/ShapoSansP_s08c07/design.png design/ShapoSansP_s08c07/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_hpp mamefont/cpp/HM/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s08c07

mamefont/cpp/VL/include/ShapoSansP_s08c07.hpp: mamefont/cpp/VL/src/ShapoSansP_s08c07.cpp
mamefont/cpp/VL/src/ShapoSansP_s08c07.cpp: design/ShapoSansP_s08c07/design.png design/ShapoSansP_s08c07/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_hpp mamefont/cpp/VL/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s08c07

mamefont/cpp/VM/include/ShapoSansP_s08c07.hpp: mamefont/cpp/VM/src/ShapoSansP_s08c07.cpp
mamefont/cpp/VM/src/ShapoSansP_s08c07.cpp: design/ShapoSansP_s08c07/design.png design/ShapoSansP_s08c07/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_hpp mamefont/cpp/VM/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s08c07

mamefont/json/HL/ShapoSansP_s08c07.json: design/ShapoSansP_s08c07/design.png design/ShapoSansP_s08c07/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_json $(dir $@) -i design/ShapoSansP_s08c07

mamefont/json/HM/ShapoSansP_s08c07.json: design/ShapoSansP_s08c07/design.png design/ShapoSansP_s08c07/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_json $(dir $@) -i design/ShapoSansP_s08c07

mamefont/json/VL/ShapoSansP_s08c07.json: design/ShapoSansP_s08c07/design.png design/ShapoSansP_s08c07/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_json $(dir $@) -i design/ShapoSansP_s08c07

mamefont/json/VM/ShapoSansP_s08c07.json: design/ShapoSansP_s08c07/design.png design/ShapoSansP_s08c07/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_json $(dir $@) -i design/ShapoSansP_s08c07

gfxfont/cpp/include/ShapoSansMono_s08c07.h: design/ShapoSansMono_s08c07/design.png design/ShapoSansMono_s08c07/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/ShapoSansMono_s08c07

mamefont/cpp/HL/include/ShapoSansMono_s08c07.hpp: mamefont/cpp/HL/src/ShapoSansMono_s08c07.cpp
mamefont/cpp/HL/src/ShapoSansMono_s08c07.cpp: design/ShapoSansMono_s08c07/design.png design/ShapoSansMono_s08c07/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_hpp mamefont/cpp/HL/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansMono_s08c07

mamefont/cpp/HM/include/ShapoSansMono_s08c07.hpp: mamefont/cpp/HM/src/ShapoSansMono_s08c07.cpp
mamefont/cpp/HM/src/ShapoSansMono_s08c07.cpp: design/ShapoSansMono_s08c07/design.png design/ShapoSansMono_s08c07/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_hpp mamefont/cpp/HM/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansMono_s08c07

mamefont/cpp/VL/include/ShapoSansMono_s08c07.hpp: mamefont/cpp/VL/src/ShapoSansMono_s08c07.cpp
mamefont/cpp/VL/src/ShapoSansMono_s08c07.cpp: design/ShapoSansMono_s08c07/design.png design/ShapoSansMono_s08c07/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_hpp mamefont/cpp/VL/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansMono_s08c07

mamefont/cpp/VM/include/ShapoSansMono_s08c07.hpp: mamefont/cpp/VM/src/ShapoSansMono_s08c07.cpp
mamefont/cpp/VM/src/ShapoSansMono_s08c07.cpp: design/ShapoSansMono_s08c07/design.png design/ShapoSansMono_s08c07/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_hpp mamefont/cpp/VM/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansMono_s08c07

mamefont/json/HL/ShapoSansMono_s08c07.json: design/ShapoSansMono_s08c07/design.png design/ShapoSansMono_s08c07/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_json $(dir $@) -i design/ShapoSansMono_s08c07

mamefont/json/HM/ShapoSansMono_s08c07.json: design/ShapoSansMono_s08c07/design.png design/ShapoSansMono_s08c07/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_json $(dir $@) -i design/ShapoSansMono_s08c07

mamefont/json/VL/ShapoSansMono_s08c07.json: design/ShapoSansMono_s08c07/design.png design/ShapoSansMono_s08c07/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_json $(dir $@) -i design/ShapoSansMono_s08c07

mamefont/json/VM/ShapoSansMono_s08c07.json: design/ShapoSansMono_s08c07/design.png design/ShapoSansMono_s08c07/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_json $(dir $@) -i design/ShapoSansMono_s08c07

gfxfont/cpp/include/ShapoSansDigitP_s32c30w04.h: design/ShapoSansDigitP_s32c30w04/design.png design/ShapoSansDigitP_s32c30w04/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/ShapoSansDigitP_s32c30w04

mamefont/cpp/HL/include/ShapoSansDigitP_s32c30w04.hpp: mamefont/cpp/HL/src/ShapoSansDigitP_s32c30w04.cpp
mamefont/cpp/HL/src/ShapoSansDigitP_s32c30w04.cpp: design/ShapoSansDigitP_s32c30w04/design.png design/ShapoSansDigitP_s32c30w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_hpp mamefont/cpp/HL/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansDigitP_s32c30w04

mamefont/cpp/HM/include/ShapoSansDigitP_s32c30w04.hpp: mamefont/cpp/HM/src/ShapoSansDigitP_s32c30w04.cpp
mamefont/cpp/HM/src/ShapoSansDigitP_s32c30w04.cpp: design/ShapoSansDigitP_s32c30w04/design.png design/ShapoSansDigitP_s32c30w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_hpp mamefont/cpp/HM/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansDigitP_s32c30w04

mamefont/cpp/VL/include/ShapoSansDigitP_s32c30w04.hpp: mamefont/cpp/VL/src/ShapoSansDigitP_s32c30w04.cpp
mamefont/cpp/VL/src/ShapoSansDigitP_s32c30w04.cpp: design/ShapoSansDigitP_s32c30w04/design.png design/ShapoSansDigitP_s32c30w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_hpp mamefont/cpp/VL/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansDigitP_s32c30w04

mamefont/cpp/VM/include/ShapoSansDigitP_s32c30w04.hpp: mamefont/cpp/VM/src/ShapoSansDigitP_s32c30w04.cpp
mamefont/cpp/VM/src/ShapoSansDigitP_s32c30w04.cpp: design/ShapoSansDigitP_s32c30w04/design.png design/ShapoSansDigitP_s32c30w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_hpp mamefont/cpp/VM/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansDigitP_s32c30w04

mamefont/json/HL/ShapoSansDigitP_s32c30w04.json: design/ShapoSansDigitP_s32c30w04/design.png design/ShapoSansDigitP_s32c30w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_json $(dir $@) -i design/ShapoSansDigitP_s32c30w04

mamefont/json/HM/ShapoSansDigitP_s32c30w04.json: design/ShapoSansDigitP_s32c30w04/design.png design/ShapoSansDigitP_s32c30w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_json $(dir $@) -i design/ShapoSansDigitP_s32c30w04

mamefont/json/VL/ShapoSansDigitP_s32c30w04.json: design/ShapoSansDigitP_s32c30w04/design.png design/ShapoSansDigitP_s32c30w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_json $(dir $@) -i design/ShapoSansDigitP_s32c30w04

mamefont/json/VM/ShapoSansDigitP_s32c30w04.json: design/ShapoSansDigitP_s32c30w04/design.png design/ShapoSansDigitP_s32c30w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_json $(dir $@) -i design/ShapoSansDigitP_s32c30w04

gfxfont/cpp/include/ShapoSansDigitP_s24c23w04.h: design/ShapoSansDigitP_s24c23w04/design.png design/ShapoSansDigitP_s24c23w04/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/ShapoSansDigitP_s24c23w04

mamefont/cpp/HL/include/ShapoSansDigitP_s24c23w04.hpp: mamefont/cpp/HL/src/ShapoSansDigitP_s24c23w04.cpp
mamefont/cpp/HL/src/ShapoSansDigitP_s24c23w04.cpp: design/ShapoSansDigitP_s24c23w04/design.png design/ShapoSansDigitP_s24c23w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_hpp mamefont/cpp/HL/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansDigitP_s24c23w04

mamefont/cpp/HM/include/ShapoSansDigitP_s24c23w04.hpp: mamefont/cpp/HM/src/ShapoSansDigitP_s24c23w04.cpp
mamefont/cpp/HM/src/ShapoSansDigitP_s24c23w04.cpp: design/ShapoSansDigitP_s24c23w04/design.png design/ShapoSansDigitP_s24c23w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_hpp mamefont/cpp/HM/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansDigitP_s24c23w04

mamefont/cpp/VL/include/ShapoSansDigitP_s24c23w04.hpp: mamefont/cpp/VL/src/ShapoSansDigitP_s24c23w04.cpp
mamefont/cpp/VL/src/ShapoSansDigitP_s24c23w04.cpp: design/ShapoSansDigitP_s24c23w04/design.png design/ShapoSansDigitP_s24c23w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_hpp mamefont/cpp/VL/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansDigitP_s24c23w04

mamefont/cpp/VM/include/ShapoSansDigitP_s24c23w04.hpp: mamefont/cpp/VM/src/ShapoSansDigitP_s24c23w04.cpp
mamefont/cpp/VM/src/ShapoSansDigitP_s24c23w04.cpp: design/ShapoSansDigitP_s24c23w04/design.png design/ShapoSansDigitP_s24c23w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_hpp mamefont/cpp/VM/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansDigitP_s24c23w04

mamefont/json/HL/ShapoSansDigitP_s24c23w04.json: design/ShapoSansDigitP_s24c23w04/design.png design/ShapoSansDigitP_s24c23w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_json $(dir $@) -i design/ShapoSansDigitP_s24c23w04

mamefont/json/HM/ShapoSansDigitP_s24c23w04.json: design/ShapoSansDigitP_s24c23w04/design.png design/ShapoSansDigitP_s24c23w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_json $(dir $@) -i design/ShapoSansDigitP_s24c23w04

mamefont/json/VL/ShapoSansDigitP_s24c23w04.json: design/ShapoSansDigitP_s24c23w04/design.png design/ShapoSansDigitP_s24c23w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_json $(dir $@) -i design/ShapoSansDigitP_s24c23w04

mamefont/json/VM/ShapoSansDigitP_s24c23w04.json: design/ShapoSansDigitP_s24c23w04/design.png design/ShapoSansDigitP_s24c23w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_json $(dir $@) -i design/ShapoSansDigitP_s24c23w04

gfxfont/cpp/include/ShapoSansP_s07c05a01.h: design/ShapoSansP_s07c05a01/design.png design/ShapoSansP_s07c05a01/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/ShapoSansP_s07c05a01

mamefont/cpp/HL/include/ShapoSansP_s07c05a01.hpp: mamefont/cpp/HL/src/ShapoSansP_s07c05a01.cpp
mamefont/cpp/HL/src/ShapoSansP_s07c05a01.cpp: design/ShapoSansP_s07c05a01/design.png design/ShapoSansP_s07c05a01/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_hpp mamefont/cpp/HL/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s07c05a01

mamefont/cpp/HM/include/ShapoSansP_s07c05a01.hpp: mamefont/cpp/HM/src/ShapoSansP_s07c05a01.cpp
mamefont/cpp/HM/src/ShapoSansP_s07c05a01.cpp: design/ShapoSansP_s07c05a01/design.png design/ShapoSansP_s07c05a01/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_hpp mamefont/cpp/HM/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s07c05a01

mamefont/cpp/VL/include/ShapoSansP_s07c05a01.hpp: mamefont/cpp/VL/src/ShapoSansP_s07c05a01.cpp
mamefont/cpp/VL/src/ShapoSansP_s07c05a01.cpp: design/ShapoSansP_s07c05a01/design.png design/ShapoSansP_s07c05a01/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_hpp mamefont/cpp/VL/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s07c05a01

mamefont/cpp/VM/include/ShapoSansP_s07c05a01.hpp: mamefont/cpp/VM/src/ShapoSansP_s07c05a01.cpp
mamefont/cpp/VM/src/ShapoSansP_s07c05a01.cpp: design/ShapoSansP_s07c05a01/design.png design/ShapoSansP_s07c05a01/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_hpp mamefont/cpp/VM/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s07c05a01

mamefont/json/HL/ShapoSansP_s07c05a01.json: design/ShapoSansP_s07c05a01/design.png design/ShapoSansP_s07c05a01/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_json $(dir $@) -i design/ShapoSansP_s07c05a01

mamefont/json/HM/ShapoSansP_s07c05a01.json: design/ShapoSansP_s07c05a01/design.png design/ShapoSansP_s07c05a01/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_json $(dir $@) -i design/ShapoSansP_s07c05a01

mamefont/json/VL/ShapoSansP_s07c05a01.json: design/ShapoSansP_s07c05a01/design.png design/ShapoSansP_s07c05a01/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_json $(dir $@) -i design/ShapoSansP_s07c05a01

mamefont/json/VM/ShapoSansP_s07c05a01.json: design/ShapoSansP_s07c05a01/design.png design/ShapoSansP_s07c05a01/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_json $(dir $@) -i design/ShapoSansP_s07c05a01

gfxfont/cpp/include/ShapoSansP_s05.h: design/ShapoSansP_s05/design.png design/ShapoSansP_s05/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/ShapoSansP_s05

mamefont/cpp/HL/include/ShapoSansP_s05.hpp: mamefont/cpp/HL/src/ShapoSansP_s05.cpp
mamefont/cpp/HL/src/ShapoSansP_s05.cpp: design/ShapoSansP_s05/design.png design/ShapoSansP_s05/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_hpp mamefont/cpp/HL/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s05

mamefont/cpp/HM/include/ShapoSansP_s05.hpp: mamefont/cpp/HM/src/ShapoSansP_s05.cpp
mamefont/cpp/HM/src/ShapoSansP_s05.cpp: design/ShapoSansP_s05/design.png design/ShapoSansP_s05/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_hpp mamefont/cpp/HM/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s05

mamefont/cpp/VL/include/ShapoSansP_s05.hpp: mamefont/cpp/VL/src/ShapoSansP_s05.cpp
mamefont/cpp/VL/src/ShapoSansP_s05.cpp: design/ShapoSansP_s05/design.png design/ShapoSansP_s05/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_hpp mamefont/cpp/VL/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s05

mamefont/cpp/VM/include/ShapoSansP_s05.hpp: mamefont/cpp/VM/src/ShapoSansP_s05.cpp
mamefont/cpp/VM/src/ShapoSansP_s05.cpp: design/ShapoSansP_s05/design.png design/ShapoSansP_s05/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_hpp mamefont/cpp/VM/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansP_s05

mamefont/json/HL/ShapoSansP_s05.json: design/ShapoSansP_s05/design.png design/ShapoSansP_s05/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_json $(dir $@) -i design/ShapoSansP_s05

mamefont/json/HM/ShapoSansP_s05.json: design/ShapoSansP_s05/design.png design/ShapoSansP_s05/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_json $(dir $@) -i design/ShapoSansP_s05

mamefont/json/VL/ShapoSansP_s05.json: design/ShapoSansP_s05/design.png design/ShapoSansP_s05/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_json $(dir $@) -i design/ShapoSansP_s05

mamefont/json/VM/ShapoSansP_s05.json: design/ShapoSansP_s05/design.png design/ShapoSansP_s05/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_json $(dir $@) -i design/ShapoSansP_s05

gfxfont/cpp/include/ShapoSansDigitP_s16c14w02.h: design/ShapoSansDigitP_s16c14w02/design.png design/ShapoSansDigitP_s16c14w02/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/ShapoSansDigitP_s16c14w02

mamefont/cpp/HL/include/ShapoSansDigitP_s16c14w02.hpp: mamefont/cpp/HL/src/ShapoSansDigitP_s16c14w02.cpp
mamefont/cpp/HL/src/ShapoSansDigitP_s16c14w02.cpp: design/ShapoSansDigitP_s16c14w02/design.png design/ShapoSansDigitP_s16c14w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_hpp mamefont/cpp/HL/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansDigitP_s16c14w02

mamefont/cpp/HM/include/ShapoSansDigitP_s16c14w02.hpp: mamefont/cpp/HM/src/ShapoSansDigitP_s16c14w02.cpp
mamefont/cpp/HM/src/ShapoSansDigitP_s16c14w02.cpp: design/ShapoSansDigitP_s16c14w02/design.png design/ShapoSansDigitP_s16c14w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_hpp mamefont/cpp/HM/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansDigitP_s16c14w02

mamefont/cpp/VL/include/ShapoSansDigitP_s16c14w02.hpp: mamefont/cpp/VL/src/ShapoSansDigitP_s16c14w02.cpp
mamefont/cpp/VL/src/ShapoSansDigitP_s16c14w02.cpp: design/ShapoSansDigitP_s16c14w02/design.png design/ShapoSansDigitP_s16c14w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_hpp mamefont/cpp/VL/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansDigitP_s16c14w02

mamefont/cpp/VM/include/ShapoSansDigitP_s16c14w02.hpp: mamefont/cpp/VM/src/ShapoSansDigitP_s16c14w02.cpp
mamefont/cpp/VM/src/ShapoSansDigitP_s16c14w02.cpp: design/ShapoSansDigitP_s16c14w02/design.png design/ShapoSansDigitP_s16c14w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_hpp mamefont/cpp/VM/include --outdir_mame_cpp $(dir $@) -i design/ShapoSansDigitP_s16c14w02

mamefont/json/HL/ShapoSansDigitP_s16c14w02.json: design/ShapoSansDigitP_s16c14w02/design.png design/ShapoSansDigitP_s16c14w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_json $(dir $@) -i design/ShapoSansDigitP_s16c14w02

mamefont/json/HM/ShapoSansDigitP_s16c14w02.json: design/ShapoSansDigitP_s16c14w02/design.png design/ShapoSansDigitP_s16c14w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_json $(dir $@) -i design/ShapoSansDigitP_s16c14w02

mamefont/json/VL/ShapoSansDigitP_s16c14w02.json: design/ShapoSansDigitP_s16c14w02/design.png design/ShapoSansDigitP_s16c14w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_json $(dir $@) -i design/ShapoSansDigitP_s16c14w02

mamefont/json/VM/ShapoSansDigitP_s16c14w02.json: design/ShapoSansDigitP_s16c14w02/design.png design/ShapoSansDigitP_s16c14w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_json $(dir $@) -i design/ShapoSansDigitP_s16c14w02

gfxfont/cpp/include/TestF_s16w04.h: design/TestF_s16w04/design.png design/TestF_s16w04/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/TestF_s16w04

mamefont/cpp/HL/include/TestF_s16w04.hpp: mamefont/cpp/HL/src/TestF_s16w04.cpp
mamefont/cpp/HL/src/TestF_s16w04.cpp: design/TestF_s16w04/design.png design/TestF_s16w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_hpp mamefont/cpp/HL/include --outdir_mame_cpp $(dir $@) -i design/TestF_s16w04

mamefont/cpp/HM/include/TestF_s16w04.hpp: mamefont/cpp/HM/src/TestF_s16w04.cpp
mamefont/cpp/HM/src/TestF_s16w04.cpp: design/TestF_s16w04/design.png design/TestF_s16w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_hpp mamefont/cpp/HM/include --outdir_mame_cpp $(dir $@) -i design/TestF_s16w04

mamefont/cpp/VL/include/TestF_s16w04.hpp: mamefont/cpp/VL/src/TestF_s16w04.cpp
mamefont/cpp/VL/src/TestF_s16w04.cpp: design/TestF_s16w04/design.png design/TestF_s16w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_hpp mamefont/cpp/VL/include --outdir_mame_cpp $(dir $@) -i design/TestF_s16w04

mamefont/cpp/VM/include/TestF_s16w04.hpp: mamefont/cpp/VM/src/TestF_s16w04.cpp
mamefont/cpp/VM/src/TestF_s16w04.cpp: design/TestF_s16w04/design.png design/TestF_s16w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_hpp mamefont/cpp/VM/include --outdir_mame_cpp $(dir $@) -i design/TestF_s16w04

mamefont/json/HL/TestF_s16w04.json: design/TestF_s16w04/design.png design/TestF_s16w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_json $(dir $@) -i design/TestF_s16w04

mamefont/json/HM/TestF_s16w04.json: design/TestF_s16w04/design.png design/TestF_s16w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_json $(dir $@) -i design/TestF_s16w04

mamefont/json/VL/TestF_s16w04.json: design/TestF_s16w04/design.png design/TestF_s16w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_json $(dir $@) -i design/TestF_s16w04

mamefont/json/VM/TestF_s16w04.json: design/TestF_s16w04/design.png design/TestF_s16w04/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_json $(dir $@) -i design/TestF_s16w04

gfxfont/cpp/include/TestF_s08w02.h: design/TestF_s08w02/design.png design/TestF_s08w02/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/TestF_s08w02

mamefont/cpp/HL/include/TestF_s08w02.hpp: mamefont/cpp/HL/src/TestF_s08w02.cpp
mamefont/cpp/HL/src/TestF_s08w02.cpp: design/TestF_s08w02/design.png design/TestF_s08w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_hpp mamefont/cpp/HL/include --outdir_mame_cpp $(dir $@) -i design/TestF_s08w02

mamefont/cpp/HM/include/TestF_s08w02.hpp: mamefont/cpp/HM/src/TestF_s08w02.cpp
mamefont/cpp/HM/src/TestF_s08w02.cpp: design/TestF_s08w02/design.png design/TestF_s08w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_hpp mamefont/cpp/HM/include --outdir_mame_cpp $(dir $@) -i design/TestF_s08w02

mamefont/cpp/VL/include/TestF_s08w02.hpp: mamefont/cpp/VL/src/TestF_s08w02.cpp
mamefont/cpp/VL/src/TestF_s08w02.cpp: design/TestF_s08w02/design.png design/TestF_s08w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_hpp mamefont/cpp/VL/include --outdir_mame_cpp $(dir $@) -i design/TestF_s08w02

mamefont/cpp/VM/include/TestF_s08w02.hpp: mamefont/cpp/VM/src/TestF_s08w02.cpp
mamefont/cpp/VM/src/TestF_s08w02.cpp: design/TestF_s08w02/design.png design/TestF_s08w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_hpp mamefont/cpp/VM/include --outdir_mame_cpp $(dir $@) -i design/TestF_s08w02

mamefont/json/HL/TestF_s08w02.json: design/TestF_s08w02/design.png design/TestF_s08w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_json $(dir $@) -i design/TestF_s08w02

mamefont/json/HM/TestF_s08w02.json: design/TestF_s08w02/design.png design/TestF_s08w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_json $(dir $@) -i design/TestF_s08w02

mamefont/json/VL/TestF_s08w02.json: design/TestF_s08w02/design.png design/TestF_s08w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_json $(dir $@) -i design/TestF_s08w02

mamefont/json/VM/TestF_s08w02.json: design/TestF_s08w02/design.png design/TestF_s08w02/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_json $(dir $@) -i design/TestF_s08w02

gfxfont/cpp/include/Empty_s01.h: design/Empty_s01/design.png design/Empty_s01/design.json $(GFXFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --outdir_gfx_c $(dir $@) -i design/Empty_s01

mamefont/cpp/HL/include/Empty_s01.hpp: mamefont/cpp/HL/src/Empty_s01.cpp
mamefont/cpp/HL/src/Empty_s01.cpp: design/Empty_s01/design.png design/Empty_s01/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_hpp mamefont/cpp/HL/include --outdir_mame_cpp $(dir $@) -i design/Empty_s01

mamefont/cpp/HM/include/Empty_s01.hpp: mamefont/cpp/HM/src/Empty_s01.cpp
mamefont/cpp/HM/src/Empty_s01.cpp: design/Empty_s01/design.png design/Empty_s01/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/HM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_hpp mamefont/cpp/HM/include --outdir_mame_cpp $(dir $@) -i design/Empty_s01

mamefont/cpp/VL/include/Empty_s01.hpp: mamefont/cpp/VL/src/Empty_s01.cpp
mamefont/cpp/VL/src/Empty_s01.cpp: design/Empty_s01/design.png design/Empty_s01/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VL/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_hpp mamefont/cpp/VL/include --outdir_mame_cpp $(dir $@) -i design/Empty_s01

mamefont/cpp/VM/include/Empty_s01.hpp: mamefont/cpp/VM/src/Empty_s01.cpp
mamefont/cpp/VM/src/Empty_s01.cpp: design/Empty_s01/design.png design/Empty_s01/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p mamefont/cpp/VM/include $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_hpp mamefont/cpp/VM/include --outdir_mame_cpp $(dir $@) -i design/Empty_s01

mamefont/json/HL/Empty_s01.json: design/Empty_s01/design.png design/Empty_s01/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HL --outdir_mame_json $(dir $@) -i design/Empty_s01

mamefont/json/HM/Empty_s01.json: design/Empty_s01/design.png design/Empty_s01/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch HM --outdir_mame_json $(dir $@) -i design/Empty_s01

mamefont/json/VL/Empty_s01.json: design/Empty_s01/design.png design/Empty_s01/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VL --outdir_mame_json $(dir $@) -i design/Empty_s01

mamefont/json/VM/Empty_s01.json: design/Empty_s01/design.png design/Empty_s01/design.json $(MAMEFONT_PY) $(COMMON_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(SHAPOFONT_PY) --mame_arch VM --outdir_mame_json $(dir $@) -i design/Empty_s01

distclean_all: distclean_gfx_all distclean_mame_all

distclean_gfx_all:
	rm -rf gfxfont/cpp/include

distclean_mame_all: distclean_mame_HL distclean_mame_HM distclean_mame_VL distclean_mame_VM
distclean_mame_HL:
	rm -rf mamefont/cpp/HL/include
	rm -rf mamefont/cpp/HL/src
	rm -rf mamefont/json/HL

distclean_mame_HM:
	rm -rf mamefont/cpp/HM/include
	rm -rf mamefont/cpp/HM/src
	rm -rf mamefont/json/HM

distclean_mame_VL:
	rm -rf mamefont/cpp/VL/include
	rm -rf mamefont/cpp/VL/src
	rm -rf mamefont/json/VL

distclean_mame_VM:
	rm -rf mamefont/cpp/VM/include
	rm -rf mamefont/cpp/VM/src
	rm -rf mamefont/json/VM

distclean_mame_cpp:
	rm -rf mamefont/cpp/HL/include
	rm -rf mamefont/cpp/HL/src
	rm -rf mamefont/cpp/HM/include
	rm -rf mamefont/cpp/HM/src
	rm -rf mamefont/cpp/VL/include
	rm -rf mamefont/cpp/VL/src
	rm -rf mamefont/cpp/VM/include
	rm -rf mamefont/cpp/VM/src

distclean_mame_json:
	rm -rf mamefont/json/HL
	rm -rf mamefont/json/HM
	rm -rf mamefont/json/VL
	rm -rf mamefont/json/VM

