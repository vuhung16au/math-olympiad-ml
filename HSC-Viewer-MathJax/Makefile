.PHONY: help install dev build start lint test generate generate-one generate-html-all generate-html-one benchmark-html-one watch clean deploy deploy-vercel deploy-collections deploy-all-prebuilt verify

help:
	@echo "HSC-Viewer-MathJax commands:"
	@echo "  make install                 - Install bun dependencies"
	@echo "  make dev                     - Start Next.js only"
	@echo "  make build                   - Generate HTML then build"
	@echo "  make start                   - Start production server"
	@echo "  make lint                    - Run ESLint"
	@echo "  make test                    - Run Playwright tests"
	@echo "  make generate                - Generate all booklet HTML"
	@echo "  make generate-one BOOKLET=HSC-Sequences"
	@echo "  make generate-html-all       - Full conversion for all booklets"
	@echo "  make generate-html-one BOOKLET=HSC-Collections"
	@echo "  make benchmark-html-one BOOKLET=HSC-Collections"
	@echo "  make watch                   - Watch LaTeX files and regenerate"
	@echo "  make clean                   - Remove local generated/build artifacts"
	@echo "  make deploy                  - Deploy current artifacts to Vercel"
	@echo "  make deploy-vercel           - Deploy current artifacts to Vercel"
	@echo "  make deploy-collections      - Prebuilt deploy for HSC-Collections only"
	@echo "  make deploy-all-prebuilt     - Prebuilt deploy for all booklets"
	@echo "  make verify                  - Lint, test, and build"

install:
	bun install

dev:
	if [ -n "$$PORT" ]; then \
		bun run dev -- --port $$PORT; \
	else \
		bun run dev; \
	fi

build: generate
	bun run build

start:
	if [ -n "$$PORT" ]; then \
		bun run start -- --port $$PORT; \
	else \
		bun run start; \
	fi

lint:
	bun run lint

test:
	bun run test

generate:
	bun run generate

generate-one:
	BOOKLET=$(BOOKLET) bun run generate:one

generate-html-all:
	TIMEOUT_MS=$${TIMEOUT_MS:-600000} bun run generate:html:all

generate-html-one:
	BOOKLET=$(BOOKLET) TIMEOUT_MS=$${TIMEOUT_MS:-600000} bun run generate:html:one

benchmark-html-one:
	BOOKLET=$(BOOKLET) TIMEOUT_MS=$${TIMEOUT_MS:-600000} bun run benchmark:html:one

watch:
	bun run watch

clean:
	rm -rf .next .generated/playwright .generated/booklets .generated/assets .generated/tmp
	mkdir -p .generated
	touch .generated/.gitkeep

deploy: deploy-vercel

deploy-vercel:
	bunx vercel --prod

deploy-collections:
	sh scripts/deploy-collections.sh

deploy-all-prebuilt:
	sh scripts/deploy-all-prebuilt.sh

verify: lint test build

.DEFAULT_GOAL := help
