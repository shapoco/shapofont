.PHONY: all

REPO_DIR := ..

TOOLS_DIR = $(REPO_DIR)/tools
BUILD_DIR = $(REPO_DIR)/build
BITMAP_DIR = .
GFX_FONT_DIR = $(REPO_DIR)/gfxfont

CMD_SHAPOFONT = $(TOOLS_DIR)/shapofont.py

EXTRA_DEPENDENCIES = \
	Makefile \
	$(wildcard $(TOOLS_DIR)/*.py)

FONT_JSON_LIST = \
	$(wildcard $(BITMAP_DIR)/$(TARGET_FAMILY)/*/shapofont.json)

GFX_FONT_LIST = \
	$(patsubst $(BITMAP_DIR)/$(TARGET_FAMILY)/%/shapofont.json,$(GFX_FONT_DIR)/$(TARGET_FAMILY)_%.h,$(FONT_JSON_LIST))

all: $(GFX_FONT_LIST)
	@echo TARGET_FAMILY=$(TARGET_FAMILY)
	@echo $(FONT_JSON_LIST)
	@echo $(GFX_FONT_LIST)

$(GFX_FONT_DIR)/$(TARGET_FAMILY)_%.h: $(BITMAP_DIR)/$(TARGET_FAMILY)/%/design.png $(BITMAP_DIR)/$(TARGET_FAMILY)/%/shapofont.json $(EXTRA_DEPENDENCIES)
	@mkdir -p $(dir $@)
	python3 $(CMD_SHAPOFONT) \
		-i $(dir $<) \
		--gfx_outdir $(dir $@)
