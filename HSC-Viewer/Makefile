.PHONY: dev build deploy deploy-vercel deploy-cloudflare deploy-all thumbnails clean install lint test test-headed test-ui help

help:
	@echo "HSC Math Hub - Available commands:"
	@echo ""
	@echo "  make install           - Install all dependencies"
	@echo "  make dev               - Start development server"
	@echo "  make build             - Build for production"
	@echo "  make start             - Start production server"
	@echo "  make deploy            - Deploy to Cloudflare"
	@echo "  make deploy-cloudflare - Deploy to Cloudflare (alias)"
	@echo "  make deploy-vercel     - Deploy to Vercel"
	@echo "  make deploy-all        - Deploy to both Vercel and Cloudflare"
	@echo "  make thumbnails        - Generate thumbnails from PDFs"
	@echo "  make lint              - Run ESLint"
	@echo "  make test              - Run Playwright e2e tests"
	@echo "  make test-headed       - Run Playwright e2e tests in headed mode"
	@echo "  make test-ui           - Open Playwright UI mode"
	@echo "  make clean             - Clean build artifacts"

install:
	bun install

dev:
	bun run next dev

build:
	bun run next build

start:
	bun run next start

deploy:
	bun run deploy

deploy-cloudflare: deploy

deploy-vercel: clean build
	vercel --prod
	@echo "✓ Deployment current - check https://hsc-math-hub.vercel.app"

deploy-all: deploy-cloudflare deploy-vercel

thumbnails:
	bun run scripts/generate-thumbnails.js
	@echo "✓ Thumbnails generated successfully"

lint:
	bun run lint

test:
	bun run test:e2e

test-headed:
	bun run test:e2e:headed

test-ui:
	bun run test:e2e:ui

clean:
	rm -rf .next
	rm -rf out
	rm -rf .open-next
	@echo "✓ Build artifacts cleaned"

.DEFAULT_GOAL := help
