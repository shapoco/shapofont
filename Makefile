.PHONY: all gfx mame gfx_distclean mame_distclean distclean doc_test

MAME_ARCH_LIST := HL HM VL VM

DOC_TEST_DIR := docs
DOC_TEST_PORT := 51980

all: gfx mame

gfx:
	make -j -C bitmap TARGET_FAMILY=ShapoSansP gfx
	make -j -C bitmap TARGET_FAMILY=ShapoSansMono gfx
	make -j -C bitmap TARGET_FAMILY=ShapoSansDigitP gfx
	make -j -C bitmap TARGET_FAMILY=MameSansP gfx
	make -j -C bitmap TARGET_FAMILY=MameSansDigitP gfx
	make -j -C bitmap TARGET_FAMILY=MameSeg7 gfx
	make -j -C bitmap TARGET_FAMILY=MameSquareWide gfx
	make -j -C bitmap TARGET_FAMILY=ShapoEmpty gfx
	make -j -C bitmap TARGET_FAMILY=TestF gfx

mame:
	@for i in $(MAME_ARCH_LIST); do \
		make -j -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansP mame; \
		make -j -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansMono mame; \
		make -j -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansDigitP mame; \
		make -j -C bitmap MAME_ARCH=$$i TARGET_FAMILY=MameSansP mame; \
		make -j -C bitmap MAME_ARCH=$$i TARGET_FAMILY=MameSansDigitP mame; \
		make -j -C bitmap MAME_ARCH=$$i TARGET_FAMILY=MameSeg7 mame; \
		make -j -C bitmap MAME_ARCH=$$i TARGET_FAMILY=MameSquareWide mame; \
		make -j -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoEmpty mame; \
		make -j -C bitmap MAME_ARCH=$$i TARGET_FAMILY=TestF mame; \
	done

distclean:
	@for i in $(MAME_ARCH_LIST); do \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansP distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansMono distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansDigitP distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=MameSansP distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=MameSansDigitP distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=MameSeg7 distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=MameSquareWide distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoEmpty distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=TestF distclean; \
	done

gfx_distclean:
	@for i in $(MAME_ARCH_LIST); do \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansP gfx_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansMono gfx_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansDigitP gfx_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=MameSansP gfx_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=MameSansDigitP gfx_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=MameSeg7 gfx_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=MameSquareWide gfx_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoEmpty gfx_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=TestF gfx_distclean; \
	done

mame_distclean:
	@for i in $(MAME_ARCH_LIST); do \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansP mame_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansMono mame_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansDigitP mame_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=MameSansP mame_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=MameSansDigitP mame_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=MameSeg7 mame_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=MameSquareWide mame_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoEmpty mame_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=TestF mame_distclean; \
	done

doc_test:
	python3 -m http.server -d $(DOC_TEST_DIR) $(DOC_TEST_PORT)
