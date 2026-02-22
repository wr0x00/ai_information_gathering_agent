#!/usr/bin/env python3
"""
Maintenance script for the AI Information Gathering Agent
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

def run_migrations():
    """Run database migrations"""
    from django.core.management import execute_from_command_line
    
    print("Running database migrations...")
    execute_from_command_line(['manage.py', 'migrate'])

def collect_static():
    """Collect static files"""
    from django.core.management import execute_from_command_line
    
    print("Collecting static files...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])

def clear_sessions():
    """Clear expired sessions"""
    from django.core.management import execute_from_command_line
    
    print("Clearing expired sessions...")
    execute_from_command_line(['manage.py', 'clearsessions'])

def backup_database():
    """Backup the database"""
    from django.conf import settings
    import shutil
    import datetime
    
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

def cleanup_backups(days=7):
    """Clean up old database backups"""
    import datetime
    
    print(f"Cleaning up backups older than {days} days...")
    
    # Calculate cutoff date
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
    
    # List available backups
    backups = [f for f in os.listdir('.') if f.startswith('db_backup_') and f.endswith('.sqlite3')]
    
    if not backups:
        print("No backups found!")
        return
    
    deleted_count = 0
    
    for backup in backups:
        # Try to extract timestamp from filename
        try:
            timestamp_str = backup.replace('db_backup_', '').replace('.sqlite3', '')
            timestamp = datetime.datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
            
            # Check if backup is older than cutoff date
            if timestamp < cutoff_date:
                try:
                    os.remove(backup)
                    print(f"Deleted old backup: {backup}")
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting backup {backup}: {e}")
        except ValueError:
            # If we can't parse the timestamp, skip this backup
            print(f"Skipping backup with invalid timestamp: {backup}")
    
    print(f"Cleanup complete. Deleted {deleted_count} old backups.")

def check_health():
    """Check the health of the application"""
    print("Checking application health...")
    
    # Check Django
    try:
        from django.conf import settings
        print("✓ Django is configured correctly")
    except Exception as e:
        print(f"✗ Django configuration error: {e}")
        return False
    
    # Check database connection
    try:
        from django.db import connection
        connection.ensure_connection()
        print("✓ Database connection is healthy")
    except Exception as e:
        print(f"✗ Database connection error: {e}")
        return False
    
    # Check required modules
    required_modules = [
        'httpx',
        'yaml',
        'docx',
        'reportlab',
        'openai',
        'anthropic',
        'bs4',
        'lxml',
        'aiodns',
        'aiomysql'
    ]
    
    print("Checking required modules...")
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module} - {e}")
            return False
    
    print("All health checks passed!")
    return True

def main():
    """Main function"""
    print("Running maintenance tasks...")
    
    # Run migrations
    run_migrations()
    
    # Collect static files
    collect_static()
    
    # Clear expired sessions
    clear_sessions()
    
    # Backup database
    backup_database()
    
    # Cleanup old backups
    cleanup_backups()
    
    # Check health
    check_health()
    
    print("Maintenance tasks completed!")

if __name__ == "__main__":
    main()
