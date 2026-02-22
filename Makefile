# Makefile for AI Information Gathering Agent

# Variables
PYTHON := python
PIP := pip
NPM := npm
MANAGE := django_ai_agent/manage.py

# Default target
.PHONY: help
help:
	@echo "AI Information Gathering Agent - Development Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  setup            Install all dependencies"
	@echo "  setup-dev        Install development dependencies"
	@echo "  run              Start development server"
	@echo "  build-frontend   Build React frontend"
	@echo "  dev-frontend     Start frontend development server"
	@echo "  migrate          Run database migrations"
	@echo "  makemigrations   Create database migrations"
	@echo "  test             Run tests"
	@echo "  test-coverage    Run tests with coverage"
	@echo "  clean            Clean Python cache files"
	@echo "  docker-build     Build Docker images"
	@echo "  docker-up        Start Docker containers"
	@echo "  docker-down      Stop Docker containers"
	@echo "  docker-logs      View Docker logs"
	@echo "  superuser        Create Django superuser"
	@echo "  collectstatic    Collect static files"
	@echo "  check            Run Django system checks"
	@echo "  shell            Open Django shell"
	@echo ""

# Setup commands
.PHONY: setup
setup:
	$(PIP) install -r requirements.txt
	$(NPM) install

.PHONY: setup-dev
setup-dev:
	$(PIP) install -r requirements.txt
	$(NPM) install

# Development commands
.PHONY: run
run:
	$(PYTHON) $(MANAGE) runserver

.PHONY: build-frontend
build-frontend:
	$(NPM) run build

.PHONY: dev-frontend
dev-frontend:
	$(NPM) run dev

# Database commands
.PHONY: migrate
migrate:
	$(PYTHON) $(MANAGE) migrate

.PHONY: makemigrations
makemigrations:
	$(PYTHON) $(MANAGE) makemigrations

# Testing commands
.PHONY: test
test:
	$(PYTHON) $(MANAGE) test

.PHONY: test-coverage
test-coverage:
	$(PYTHON) -m coverage run --source='.' $(MANAGE) test
	$(PYTHON) -m coverage report
	$(PYTHON) -m coverage html

# Cleanup commands
.PHONY: clean
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist

# Docker commands
.PHONY: docker-build
docker-build:
	docker-compose build

.PHONY: docker-up
docker-up:
	docker-compose up -d

.PHONY: docker-down
docker-down:
	docker-compose down

.PHONY: docker-logs
docker-logs:
	docker-compose logs -f

# Django management commands
.PHONY: superuser
superuser:
	$(PYTHON) $(MANAGE) createsuperuser

.PHONY: collectstatic
collectstatic:
	$(PYTHON) $(MANAGE) collectstatic --noinput

.PHONY: check
check:
	$(PYTHON) $(MANAGE) check

.PHONY: shell
shell:
	$(PYTHON) $(MANAGE) shell
