.PHONY: install dev build start lint test all

install:
	@echo "Installing web dependencies..."
	npm install

dev:
	@echo "Starting Next.js dev server..."
	npm run dev

build:
	@echo "Building Next.js app..."
	npm run build

start:
	@echo "Starting Next.js production server..."
	npm run start

lint:
	@echo "Running Next.js lint..."
	npm run lint

test:
	@echo "Running tests (if configured)..."
	npm run test

all: lint build
