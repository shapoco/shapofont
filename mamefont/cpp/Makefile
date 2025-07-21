.PHONY: build test

FONT_NAME = ShapoSansP_s05

test:
	mkdir -p build
	g++ \
		-Iinclude \
		-DMAMEFONT_STM_VERBOSE=1 \
		test/test.cpp \
		src/$(FONT_NAME).cpp \
		-o build/test
	./build/test

