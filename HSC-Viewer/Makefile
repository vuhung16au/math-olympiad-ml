.PHONY: dev build deploy thumbnails clean install help

help:
	@echo "HSC Math Hub - Available commands:"
	@echo ""
	@echo "  make install      - Install all dependencies"
	@echo "  make dev          - Start development server"
	@echo "  make build        - Build for production"
	@echo "  make start        - Start production server"
	@echo "  make deploy       - Deploy to Vercel (requires thumbnail generation)"
	@echo "  make thumbnails   - Generate thumbnails from PDFs"
	@echo "  make lint         - Run ESLint"
	@echo "  make clean        - Clean build artifacts"

install:
	bun install

dev:
	bun run next dev

build:
	bun run next build

start:
	bun run next start

deploy: clean thumbnails build
	vercel --prod
	@echo "✓ Deployment complete - check https://hsc-math-hub.vercel.app"

thumbnails:
	bun run scripts/generate-thumbnails.js
	@echo "✓ Thumbnails generated successfully"

lint:
	bun run lint

clean:
	rm -rf .next
	rm -rf out
	@echo "✓ Build artifacts cleaned"

.DEFAULT_GOAL := help
