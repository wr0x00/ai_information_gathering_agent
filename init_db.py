#!/usr/bin/env python3
"""
Database initialization script for AI Information Gathering Agent
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ai_agent.ai_agent_project.settings')

def main():
    """Initialize the database and create necessary tables."""
    print("Initializing database for AI Information Gathering Agent...")
    
    try:
        # Setup Django
        django.setup()
        
        # Run migrations
        print("Applying database migrations...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("Database initialization completed successfully!")
        print("\nNext steps:")
        print("1. Create a superuser: python django_ai_agent/manage.py createsuperuser")
        print("2. Start the server: python django_ai_agent/manage.py runserver")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
