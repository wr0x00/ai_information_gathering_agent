#!/usr/bin/env python3
"""
Database reset script for the AI Information Gathering Agent
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

def reset_database():
    """Reset the database"""
    from django.conf import settings
    from django.core.management import execute_from_command_line
    
    print("Resetting database...")
    
    # Get database path
    db_path = settings.DATABASES['default']['NAME']
    
    # Confirm reset
    confirm = input(f"Are you sure you want to reset the database at {db_path}? This will delete all data (y/N): ")
    if confirm.lower() != 'y':
        print("Database reset cancelled.")
        return
    
    # Remove database file if it exists
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print("Database file deleted.")
        except Exception as e:
            print(f"Error deleting database file: {e}")
            return
    
    # Run migrations to create new database
    print("Creating new database...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Collect static files
    print("Collecting static files...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    print("Database reset completed!")

if __name__ == "__main__":
    reset_database()
