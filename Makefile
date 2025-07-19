.PHONY: all distclean

all:
	make -C bitmap TARGET_FAMILY=ShapoSansP all
	make -C bitmap TARGET_FAMILY=ShapoSansDigitP all

distclean:
	rm -f gfxfont/include/shapofont/*.h
