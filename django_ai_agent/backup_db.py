#!/usr/bin/env python3
"""
Database backup script for the AI Information Gathering Agent
"""
import os
import sys
import shutil
import datetime
import django

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_agent_project.settings')

# Initialize Django
django.setup()

def backup_database():
    """Backup the database"""
    from django.conf import settings
    
    print("Backing up database...")
    
    # Get database path
    db_path = settings.DATABASES['default']['NAME']
    
    # Check if database exists
    if not os.path.exists(db_path):
        print("Database not found!")
        return
    
    # Create backup filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"db_backup_{timestamp}.sqlite3"
    
    # Copy database to backup location
    try:
        shutil.copy2(db_path, backup_filename)
        print(f"Database backed up successfully to {backup_filename}")
    except Exception as e:
        print(f"Error backing up database: {e}")

if __name__ == "__main__":
    backup_database()
