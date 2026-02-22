.PHONY: help install test run dev clean build docs deploy

# Default target
help:
	@echo "AI Information Gathering Agent - Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  help     - Show this help message"
	@echo "  install  - Install dependencies"
	@echo "  test     - Run tests"
	@echo "  run      - Run the Django development server"
	@echo "  dev      - Run the development server with hot reload"
	@echo "  clean    - Clean up generated files"
	@echo "  build    - Build the project"
	@echo "  docs     - Generate documentation"
	@echo "  deploy   - Deploy the application"

# Install dependencies
install:
	pip install -r requirements.txt

# Run tests
test:
	python test_installation.py

# Run the Django development server
run:
	python manage.py runserver

# Run the development server with hot reload
dev:
	python manage.py runserver

# Clean up generated files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf *.sqlite3
	rm -rf staticfiles/
	rm -rf media/

# Build the project
build:
	python setup.py sdist bdist_wheel

# Generate documentation
docs:
	@echo "Generating documentation..."

# Deploy the application
deploy:
	@echo "Deploying application..."
