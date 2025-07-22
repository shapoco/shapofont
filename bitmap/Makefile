.PHONY: all gfx mame gfx_distclean mame_distclean distclean

REPO_DIR := ..

TOOLS_DIR = $(REPO_DIR)/tools
BUILD_DIR = $(REPO_DIR)/build
BITMAP_DIR = .
GFX_FONT_INC_DIR = $(REPO_DIR)/gfxfont/include/shapofont
MAME_FONT_SRC_DIR = $(REPO_DIR)/mamefont/cpp/src/shapofont
MAME_FONT_INC_DIR = $(REPO_DIR)/mamefont/cpp/include/mamefont/shapofont

CMD_SHAPOFONT := $(TOOLS_DIR)/shapofont.py
CMD_PYTHON := $(REPO_DIR)/venv/bin/python3

EXTRA_DEPENDENCIES = \
	Makefile \
	$(wildcard $(TOOLS_DIR)/*.py)

FONT_JSON_LIST = \
	$(wildcard $(BITMAP_DIR)/$(TARGET_FAMILY)/*/shapofont.json5)

GFX_FONT_LIST = \
	$(patsubst $(BITMAP_DIR)/$(TARGET_FAMILY)/%/shapofont.json5,$(GFX_FONT_INC_DIR)/$(TARGET_FAMILY)_%.h,$(FONT_JSON_LIST))

MAME_FONT_HPP_LIST = \
	$(patsubst $(BITMAP_DIR)/$(TARGET_FAMILY)/%/shapofont.json5,$(MAME_FONT_INC_DIR)/$(TARGET_FAMILY)_%.hpp,$(FONT_JSON_LIST))

MAME_FONT_SRC_LIST = \
	$(patsubst $(BITMAP_DIR)/$(TARGET_FAMILY)/%/shapofont.json5,$(MAME_FONT_SRC_DIR)/$(TARGET_FAMILY)_%.cpp,$(FONT_JSON_LIST))

all: gfx 
gfx: $(GFX_FONT_LIST)
mame: $(MAME_FONT_SRC_LIST)

$(GFX_FONT_INC_DIR)/$(TARGET_FAMILY)_%.h: $(BITMAP_DIR)/$(TARGET_FAMILY)/%/design.png $(BITMAP_DIR)/$(TARGET_FAMILY)/%/shapofont.json5 $(EXTRA_DEPENDENCIES)
	@mkdir -p $(GFX_FONT_INC_DIR)
	$(CMD_PYTHON) $(CMD_SHAPOFONT) \
		-i $(dir $<) \
		--outdir_gfx $(dir $@)

$(MAME_FONT_SRC_DIR)/$(TARGET_FAMILY)_%.cpp: $(BITMAP_DIR)/$(TARGET_FAMILY)/%/design.png $(BITMAP_DIR)/$(TARGET_FAMILY)/%/shapofont.json5 $(EXTRA_DEPENDENCIES)
	@mkdir -p $(MAME_FONT_INC_DIR)
	@mkdir -p $(MAME_FONT_SRC_DIR)
	$(CMD_PYTHON) $(CMD_SHAPOFONT) \
		-i $(dir $<) \
		--outdir_mame_cpp $(dir $@) \
		--outdir_mame_hpp $(dir $(patsubst $(MAME_FONT_SRC_DIR)/%.cpp,$(MAME_FONT_INC_DIR)/%.hpp,$@))

distclean: gfx_distclean mame_distclean

gfx_distclean:
	rm -f $(GFX_FONT_INC_DIR)/$(TARGET_FAMILY)_*.h

mame_distclean:
	rm -f $(MAME_FONT_SRC_DIR)/$(TARGET_FAMILY)_*.cpp
	rm -f $(MAME_FONT_INC_DIR)/$(TARGET_FAMILY)_*.hpp

