#!/usr/bin/env python3
"""
Database initialization script for the AI Information Gathering Agent
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

def init_database():
    """Initialize the database"""
    from django.core.management import execute_from_command_line
    
    print("Initializing database...")
    
    # Apply migrations
    print("Applying migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Collect static files
    print("Collecting static files...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    print("Database initialization complete!")

if __name__ == "__main__":
    init_database()
