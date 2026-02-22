#!/bin/bash

# AI Information Gathering Agent Startup Script

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the correct directory
if [ ! -f "manage.py" ] && [ ! -d "django_ai_agent" ]; then
    print_error "This script must be run from the project root directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_warning "Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Check if Node.js dependencies are installed
if [ ! -d "node_modules" ]; then
    print_warning "Node.js dependencies not found. Installing..."
    npm install
fi

# Build frontend
print_status "Building frontend..."
npm run build

# Check if database migrations are needed
print_status "Checking database migrations..."
python django_ai_agent/manage.py makemigrations --check --dry-run >/dev/null 2>&1
if [ $? -ne 0 ]; then
    print_warning "Database migrations needed. Applying migrations..."
    python django_ai_agent/manage.py migrate
else
    print_status "Database is up to date."
fi

# Collect static files
print_status "Collecting static files..."
python django_ai_agent/manage.py collectstatic --noinput -c

# Start the development server
print_status "Starting development server..."
print_status "Access the application at http://localhost:8000"
python django_ai_agent/manage.py runserver 0.0.0.0:8000
