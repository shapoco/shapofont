.PHONY: all gfx mame gfx_distclean mame_distclean distclean

MAME_ARCH_LIST := HL HM VL VM

all: gfx mame

gfx:
	make -C bitmap TARGET_FAMILY=ShapoSansP gfx
	make -C bitmap TARGET_FAMILY=ShapoSansMono gfx
	make -C bitmap TARGET_FAMILY=ShapoSansDigitP gfx
	make -C bitmap TARGET_FAMILY=ShapoEmpty gfx
	make -C bitmap TARGET_FAMILY=MameDigitP gfx

mame:
	@for i in $(MAME_ARCH_LIST); do \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansP mame; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansMono mame; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansDigitP mame; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoEmpty mame; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=MameDigitP mame; \
	done

distclean:
	@for i in $(MAME_ARCH_LIST); do \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansP distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansMono distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansDigitP distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoEmpty distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=MameDigitP distclean; \
	done

gfx_distclean:
	@for i in $(MAME_ARCH_LIST); do \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansP gfx_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansMono gfx_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansDigitP gfx_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoEmpty gfx_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=MameDigitP gfx_distclean; \
	done

mame_distclean:
	@for i in $(MAME_ARCH_LIST); do \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansP mame_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansMono mame_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoSansDigitP mame_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=ShapoEmpty mame_distclean; \
		make -C bitmap MAME_ARCH=$$i TARGET_FAMILY=MameDigitP mame_distclean; \
	done
