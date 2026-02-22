#!/usr/bin/env python3
"""
Database restore script for the AI Information Gathering Agent
"""
import os
import sys
import shutil
import django

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_agent_project.settings')

# Initialize Django
django.setup()

def restore_database():
    """Restore the database from a backup"""
    from django.conf import settings
    
    print("Restoring database...")
    
    # Get database path
    db_path = settings.DATABASES['default']['NAME']
    
    # List available backups
    backups = [f for f in os.listdir('.') if f.startswith('db_backup_') and f.endswith('.sqlite3')]
    
    if not backups:
        print("No backups found!")
        return
    
    print("Available backups:")
    for i, backup in enumerate(backups):
        print(f"{i+1}. {backup}")
    
    # Get user selection
    try:
        selection = int(input("Select backup to restore (number): ")) - 1
        if selection < 0 or selection >= len(backups):
            print("Invalid selection!")
            return
    except ValueError:
        print("Invalid input!")
        return
    
    backup_file = backups[selection]
    
    # Confirm restoration
    confirm = input(f"Are you sure you want to restore {backup_file}? This will overwrite the current database (y/N): ")
    if confirm.lower() != 'y':
        print("Restoration cancelled.")
        return
    
    # Restore database
    try:
        shutil.copy2(backup_file, db_path)
        print("Database restored successfully!")
    except Exception as e:
        print(f"Error restoring database: {e}")

if __name__ == "__main__":
    restore_database()
