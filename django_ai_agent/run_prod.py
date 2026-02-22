#!/usr/bin/env python3
"""
Production run script for the AI Information Gathering Agent
"""
import os
import sys
import django

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_agent_project.settings')

# Initialize Django
django.setup()

def run_production():
    """Run the application in production mode"""
    from django.core.management import execute_from_command_line
    
    print("Starting AI Information Gathering Agent in production mode...")
    
    # Collect static files
    print("Collecting static files...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    # Run migrations
    print("Applying database migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Start the production server
    print("Starting production server...")
    print("Access the application at http://0.0.0.0:8000")
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])

if __name__ == "__main__":
    run_production()
