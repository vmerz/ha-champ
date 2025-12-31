# Makefile for CHAMP development

.PHONY: help setup install test lint format type-check clean validate all

help:
	@echo "CHAMP Development Commands:"
	@echo ""
	@echo "  setup        - Set up development environment"
	@echo "  install      - Install dependencies"
	@echo "  test         - Run tests with coverage"
	@echo "  lint         - Run linters (ruff)"
	@echo "  format       - Format code (black, isort)"
	@echo "  type-check   - Run type checker (mypy)"
	@echo "  validate     - Run validation script"
	@echo "  clean        - Clean build artifacts"
	@echo "  all          - Run format, lint, type-check, and test"
	@echo ""

setup:
	@echo "Setting up development environment..."
	@bash setup.sh

install:
	@echo "Installing dependencies..."
	@pip install -r requirements-dev.txt

test:
	@echo "Running tests with coverage..."
	@python3 -m pytest

lint:
	@echo "Running ruff..."
	@python3 -m ruff check custom_components/

format:
	@echo "Formatting code with black and isort..."
	@python3 -m black custom_components/ tests/
	@python3 -m isort custom_components/ tests/

type-check:
	@echo "Running mypy type checker..."
	@python3 -m mypy custom_components/champ/

validate:
	@echo "Running validation script..."
	@python3 validate_champ.py

clean:
	@echo "Cleaning build artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name ".coverage" -delete
	@echo "Clean complete!"

all: format lint type-check test
	@echo ""
	@echo "✅ All checks complete!"