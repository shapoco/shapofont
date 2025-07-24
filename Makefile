.PHONY: all gfx mame gfx_distclean mame_distclean distclean

all: gfx mame

gfx:
	make -C bitmap TARGET_FAMILY=ShapoSansP gfx
	make -C bitmap TARGET_FAMILY=ShapoSansMono gfx
	make -C bitmap TARGET_FAMILY=ShapoSansDigitP gfx
	make -C bitmap TARGET_FAMILY=ShapoEmpty gfx

mame:
	make -C bitmap TARGET_FAMILY=ShapoSansP mame
	make -C bitmap TARGET_FAMILY=ShapoSansMono mame
	make -C bitmap TARGET_FAMILY=ShapoSansDigitP mame
	make -C bitmap TARGET_FAMILY=ShapoEmpty mame

distclean:
	make -C bitmap TARGET_FAMILY=ShapoSansP distclean
	make -C bitmap TARGET_FAMILY=ShapoSansMono distclean
	make -C bitmap TARGET_FAMILY=ShapoSansDigitP distclean
	make -C bitmap TARGET_FAMILY=ShapoEmpty distclean

gfx_distclean:
	make -C bitmap TARGET_FAMILY=ShapoSansP gfx_distclean
	make -C bitmap TARGET_FAMILY=ShapoSansMono gfx_distclean
	make -C bitmap TARGET_FAMILY=ShapoSansDigitP gfx_distclean
	make -C bitmap TARGET_FAMILY=ShapoEmpty gfx_distclean

mame_distclean:
	make -C bitmap TARGET_FAMILY=ShapoSansP mame_distclean
	make -C bitmap TARGET_FAMILY=ShapoSansMono mame_distclean
	make -C bitmap TARGET_FAMILY=ShapoSansDigitP mame_distclean
	make -C bitmap TARGET_FAMILY=ShapoEmpty mame_distclean
