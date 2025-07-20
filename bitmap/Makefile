.PHONY: all

REPO_DIR := ..

TOOLS_DIR = $(REPO_DIR)/tools
BUILD_DIR = $(REPO_DIR)/build
BITMAP_DIR = .
GFX_FONT_INC_DIR = $(REPO_DIR)/gfxfont/include/shapofont

CMD_SHAPOFONT := $(TOOLS_DIR)/shapofont.py
CMD_PYTHON := $(REPO_DIR)/venv/bin/python3

EXTRA_DEPENDENCIES = \
	Makefile \
	$(wildcard $(TOOLS_DIR)/*.py)

FONT_JSON_LIST = \
	$(wildcard $(BITMAP_DIR)/$(TARGET_FAMILY)/*/shapofont.json5)

GFX_FONT_LIST = \
	$(patsubst $(BITMAP_DIR)/$(TARGET_FAMILY)/%/shapofont.json5,$(GFX_FONT_INC_DIR)/$(TARGET_FAMILY)_%.h,$(FONT_JSON_LIST))

all: $(GFX_FONT_LIST)
	@echo TARGET_FAMILY=$(TARGET_FAMILY)
	@echo $(FONT_JSON_LIST)
	@echo $(GFX_FONT_LIST)

$(GFX_FONT_INC_DIR)/$(TARGET_FAMILY)_%.h: $(BITMAP_DIR)/$(TARGET_FAMILY)/%/design.png $(BITMAP_DIR)/$(TARGET_FAMILY)/%/shapofont.json5 $(EXTRA_DEPENDENCIES)
	@mkdir -p $(dir $@)
	$(CMD_PYTHON) $(CMD_SHAPOFONT) \
		-i $(dir $<) \
		--outdir_gfx $(dir $@)
