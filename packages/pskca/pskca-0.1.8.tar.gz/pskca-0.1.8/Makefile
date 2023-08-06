ROOT_DIR := $(shell dirname "$(realpath $(MAKEFILE_LIST))")

.PHONY = test

test:
	cd $(ROOT_DIR) && \
	tox --current-env
