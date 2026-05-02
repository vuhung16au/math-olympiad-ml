# Delegate HSC booklet orchestration to HSC-Common (see HSC-Common/Makefile).

.PHONY: help build-all clean-all pdf-all release-all

help build-all clean-all pdf-all release-all:
	@$(MAKE) -C HSC-Common $@
