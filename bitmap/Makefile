.PHONY: all gfx mame gfx_distclean mame_distclean distclean

REPO_DIR := ..

TOOLS_DIR = $(REPO_DIR)/tools
BUILD_DIR = $(REPO_DIR)/build
BITMAP_DIR = .

GFX_C_INC_DIR = $(REPO_DIR)/gfxfont/cpp/include/shapofont

MAME_ARCH := HL
MAME_CPP_SRC_DIR = $(REPO_DIR)/mamefont/cpp/$(MAME_ARCH)/src
MAME_CPP_INC_DIR = $(REPO_DIR)/mamefont/cpp/$(MAME_ARCH)/include/shapofont
MAME_JS_JSON_DIR = $(REPO_DIR)/mamefont/json/$(MAME_ARCH)

CMD_SHAPOFONT := $(TOOLS_DIR)/shapofont.py
CMD_PYTHON := $(REPO_DIR)/venv/bin/python3

EXTRA_DEPENDENCIES = \
	Makefile \
	$(wildcard $(TOOLS_DIR)/*.py)

FONT_JSON_LIST = \
	$(wildcard $(BITMAP_DIR)/$(TARGET_FAMILY)/*/shapofont.json5)

GFX_C_HEADER_LIST = \
	$(patsubst $(BITMAP_DIR)/$(TARGET_FAMILY)/%/shapofont.json5,$(GFX_C_INC_DIR)/$(TARGET_FAMILY)_%.h,$(FONT_JSON_LIST))

MAME_CPP_HPP_LIST = \
	$(patsubst $(BITMAP_DIR)/$(TARGET_FAMILY)/%/shapofont.json5,$(MAME_CPP_INC_DIR)/$(TARGET_FAMILY)_%.hpp,$(FONT_JSON_LIST))

MAME_CPP_SRC_LIST = \
	$(patsubst $(BITMAP_DIR)/$(TARGET_FAMILY)/%/shapofont.json5,$(MAME_CPP_SRC_DIR)/$(TARGET_FAMILY)_%.cpp,$(FONT_JSON_LIST))

MAME_JS_JSON_LIST = \
	$(patsubst $(BITMAP_DIR)/$(TARGET_FAMILY)/%/shapofont.json5,$(MAME_JS_JSON_DIR)/$(TARGET_FAMILY)_%.json,$(FONT_JSON_LIST))

all: gfx 
gfx: $(GFX_C_HEADER_LIST)
mame: $(MAME_CPP_SRC_LIST)

$(GFX_C_INC_DIR)/$(TARGET_FAMILY)_%.h: $(BITMAP_DIR)/$(TARGET_FAMILY)/%/design.png $(BITMAP_DIR)/$(TARGET_FAMILY)/%/shapofont.json5 $(EXTRA_DEPENDENCIES)
	@mkdir -p $(GFX_C_INC_DIR)
	$(CMD_PYTHON) $(CMD_SHAPOFONT) \
		-i $(dir $<) \
		--outdir_gfx $(dir $@)

$(MAME_CPP_SRC_DIR)/$(TARGET_FAMILY)_%.cpp: $(BITMAP_DIR)/$(TARGET_FAMILY)/%/design.png $(BITMAP_DIR)/$(TARGET_FAMILY)/%/shapofont.json5 $(EXTRA_DEPENDENCIES)
	@mkdir -p $(MAME_CPP_INC_DIR)
	@mkdir -p $(MAME_CPP_SRC_DIR)
	@mkdir -p $(MAME_JS_JSON_DIR)
	$(CMD_PYTHON) $(CMD_SHAPOFONT) \
		-i $(dir $<) \
		--mame_arch $(MAME_ARCH) \
		--outdir_mame_cpp $(dir $@) \
		--outdir_mame_hpp $(dir $(patsubst $(MAME_CPP_SRC_DIR)/%.cpp,$(MAME_CPP_INC_DIR)/%.hpp,$@)) \
		--outdir_mame_json $(dir $(patsubst $(MAME_CPP_SRC_DIR)/%.cpp,$(MAME_JS_JSON_DIR)/%.json,$@))

distclean: gfx_distclean mame_distclean

gfx_distclean:
	rm -f $(GFX_C_INC_DIR)/$(TARGET_FAMILY)_*.h

mame_distclean:
	rm -f $(MAME_CPP_SRC_DIR)/$(TARGET_FAMILY)_*.cpp
	rm -f $(MAME_CPP_INC_DIR)/$(TARGET_FAMILY)_*.hpp
	rm -f $(MAME_JS_JSON_DIR)/$(TARGET_FAMILY)_*.json

