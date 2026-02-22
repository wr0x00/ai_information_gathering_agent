#!/usr/bin/env python3
"""
Database reset script for AI Information Gathering Agent
"""

import os
import sys
import shutil
import django
from django.core.management import execute_from_command_line

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ai_agent.ai_agent_project.settings')

def reset_database(db_path='django_ai_agent/db.sqlite3'):
    """Reset the database by deleting it and recreating it."""
    print("Resetting database...")
    try:
        # Check if database exists
        if os.path.exists(db_path):
            # Warn user before deletion
            print(f"Warning: This will delete the database file: {db_path}")
            confirm = input("Are you sure you want to continue? (y/N): ").lower().strip()
            if confirm != 'y' and confirm != 'yes':
                print("Database reset cancelled.")
                return False
            
            # Delete database file
            try:
                os.remove(db_path)
                print(f"✓ Deleted database file: {db_path}")
            except Exception as e:
                print(f"✗ Failed to delete database file: {e}")
                return False
        else:
            print("Database file not found. Will create a new one.")
        
        # Setup Django
        django.setup()
        
        # Run migrations to create new database
        print("Creating new database with migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("✓ Database reset completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Failed to reset database: {e}")
        return False

def reset_migrations():
    """Reset migrations by deleting migration files and recreating them."""
    print("Resetting migrations...")
    try:
        # List of apps that might have migrations
        apps = [
            'django_ai_agent.keywords_app',
            'django_ai_agent.reports_app',
            'django_ai_agent.config_app',
            'django_ai_agent.chat_app',
            'django_ai_agent.frontend_app'
        ]
        
        deleted_count = 0
        
        # Delete migration files for each app
        for app in apps:
            app_path = app.replace('.', '/')
            migrations_path = os.path.join(app_path, 'migrations')
            
            if os.path.exists(migrations_path):
                # List files in migrations directory
                for file in os.listdir(migrations_path):
                    # Skip __init__.py
                    if file != '__init__.py' and file.endswith('.py'):
                        file_path = os.path.join(migrations_path, file)
                        try:
                            os.remove(file_path)
                            print(f"Deleted migration: {file_path}")
                            deleted_count += 1
                        except Exception as e:
                            print(f"Failed to delete {file_path}: {e}")
        
        print(f"✓ Deleted {deleted_count} migration files")
        
        # Create new migrations
        print("Creating new migrations...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        
        # Apply migrations
        print("Applying new migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("✓ Migrations reset completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Failed to reset migrations: {e}")
        return False

def main():
    """Main function to handle database reset operations."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Database reset utility for AI Information Gathering Agent')
    parser.add_argument('--db-path', default='django_ai_agent/db.sqlite3', 
                       help='Path to the database file (default: django_ai_agent/db.sqlite3)')
    parser.add_argument('--migrations-only', action='store_true',
                       help='Reset only migrations, not the entire database')
    parser.add_argument('--force', '-f', action='store_true',
                       help='Force reset without confirmation')
    
    args = parser.parse_args()
    
    print("AI Information Gathering Agent - Database Reset")
    print("=" * 45)
    
    # Confirm action if not forced
    if not args.force:
        if args.migrations_only:
            print("Warning: This will reset all migrations and recreate them.")
        else:
            print("Warning: This will delete the entire database and recreate it.")
        
        confirm = input("Are you sure you want to continue? (y/N): ").lower().strip()
        if confirm != 'y' and confirm != 'yes':
            print("Operation cancelled.")
            return
    
    # Perform reset based on arguments
    success = True
    
    if args.migrations_only:
        success = reset_migrations()
    else:
        success = reset_database(args.db_path)
    
    print("\n" + "=" * 45)
    if success:
        print("✓ Database reset completed successfully!")
        if not args.migrations_only:
            print("Note: You may need to create a new superuser.")
            print("Run: python create_superuser.py")
    else:
        print("✗ Database reset failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()
