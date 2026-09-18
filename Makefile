# AOSP Changelog Generator
#
#   make preview   regenerate index.html and serve the site at http://127.0.0.1:8000
#   make index     regenerate gh-pages/index.html
#   make build     compile the gitlog_to_html log formatter
#   make clean     remove build output
#
# Override HOST/PORT/PUBLISH_DIR on the command line, e.g.
#   make preview PORT=9000

SHELL := /bin/bash

BASE_DIR    := $(CURDIR)
PUBLISH_DIR ?= $(BASE_DIR)/../gh-pages
HOST        ?= 127.0.0.1
PORT        ?= 8000
CC          ?= cc
CFLAGS      ?= -O2

.PHONY: all build index serve preview clean

all: build

build: gitlog_to_html

gitlog_to_html: gitlog-to-html/gitlog_to_html.c
	$(CC) $(CFLAGS) -o $@ $<

index:
	./generate_index.sh

serve: index
	HOST=$(HOST) PORT=$(PORT) PUBLISH_DIR=$(PUBLISH_DIR) ./serve.sh

preview: serve

clean:
	rm -f gitlog_to_html
