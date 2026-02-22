#!/bin/bash

# AI Information Gathering Agent - Startup Script

# Exit on any error
set -e

# Function to print status messages
print_status() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Check if we're running in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    print_status "Warning: Not running in a virtual environment"
else
    print_status "Running in virtual environment: $VIRTUAL_ENV"
fi

# Check if required files exist
if [[ ! -f "manage.py" ]]; then
    print_status "Error: manage.py not found. Please run this script from the project root directory."
    exit 1
fi

# Check if dependencies are installed
print_status "Checking dependencies..."
if ! python -c "import django" 2>/dev/null; then
    print_status "Installing dependencies..."
    pip install -r requirements.txt
fi

# Apply database migrations
print_status "Applying database migrations..."
python manage.py migrate

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput

# Start the Django development server
print_status "Starting Django development server..."
print_status "Access the application at http://localhost:8080"
python manage.py runserver 127.0.0.1:8080
