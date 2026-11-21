.PHONY: all configure catalog test doc_test

CMD_SHAPOFONT := venv/bin/shapofont
CMD_PYTHON := venv/bin/python3

DOC_TEST_DIR := docs
DOC_TEST_PORT := 51980

COMMON_DEPENDENCIES := \
	Makefile \
	$(wildcard src/shapofont/*.py)

all: gfx_all lvgl_all sample_all

configure:
	$(CMD_SHAPOFONT) configure

include Makefile.batch.mk

catalog: all
	$(CMD_SHAPOFONT) catalog

test:
	$(CMD_PYTHON) -m pytest

doc_test:
	python3 -m http.server -d $(DOC_TEST_DIR) $(DOC_TEST_PORT)
