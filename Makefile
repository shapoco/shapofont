.PHONY: all configure doc_test

TOOLS_DIR := tools
MAMEFONT_DIR := $(shell cd ../mamefont && pwd)

CMD_PYTHON := venv/bin/python3
SHAPOFONT_PY := $(TOOLS_DIR)/shapofont.py
GFXFONT_PY := $(TOOLS_DIR)/gfxfont.py

CMD_MAMEC := $(MAMEFONT_DIR)/bin/mamec

MAME_ENC_LIST := HL HM VL VM

DOC_TEST_DIR := docs
DOC_TEST_PORT := 51980

COMMON_DEPENDENCIES := \
	Makefile \
	$(SHAPOFONT_PY) \
	$(TOOLS_DIR)/design.py

all: gfx_all mame_all

configure:
	$(CMD_PYTHON) Makefile.update.py

include Makefile.batch.mk

doc_test:
	python3 -m http.server -d $(DOC_TEST_DIR) $(DOC_TEST_PORT)
