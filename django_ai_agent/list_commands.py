#!/usr/bin/env python3
"""
Management commands lister for the AI Information Gathering Agent
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

def list_commands():
    """List all available management commands"""
    from django.core.management import get_commands, load_command_class
    from django.core.management.base import BaseCommand
    
    print("Available management commands:")
    print("=" * 40)
    
    # Get all commands
    commands = get_commands()
    
    # Group commands by app
    app_commands = {}
    for command, app in commands.items():
        if app not in app_commands:
            app_commands[app] = []
        app_commands[app].append(command)
    
    # Sort apps and commands
    for app in sorted(app_commands.keys()):
        print(f"\n{app}:")
        for command in sorted(app_commands[app]):
            # Try to get command help text
            try:
                command_class = load_command_class(app, command)
                help_text = command_class.help if hasattr(command_class, 'help') else "No description available"
                print(f"  {command:<20} - {help_text}")
            except Exception:
                print(f"  {command:<20} - No description available")

def list_custom_commands():
    """List custom management scripts"""
    print("\nCustom management scripts:")
    print("=" * 40)
    
    custom_scripts = [
        ("init_db.py", "Initialize the database"),
        ("run_tests.py", "Run all tests"),
        ("create_superuser.py", "Create a superuser"),
        ("backup_db.py", "Backup the database"),
        ("restore_db.py", "Restore the database from backup"),
        ("list_backups.py", "List available database backups"),
        ("cleanup_backups.py", "Clean up old database backups"),
        ("check_health.py", "Check application health"),
        ("generate_docs.py", "Generate documentation"),
        ("maintenance.py", "Run maintenance tasks"),
        ("export_data.py", "Export data"),
        ("import_data.py", "Import data"),
        ("reset_db.py", "Reset the database"),
        ("update_deps.py", "Update dependencies"),
        ("run_prod.py", "Run in production mode"),
        ("show_version.py", "Show application version"),
        ("list_commands.py", "List all available commands")
    ]
    
    for script, description in custom_scripts:
        print(f"  {script:<20} - {description}")

def main():
    """Main function"""
    print("AI Information Gathering Agent - Management Commands")
    print("=" * 50)
    
    list_commands()
    list_custom_commands()
    
    print("\nUsage:")
    print("  python manage.py <command> [options]")
    print("  python <script_name> [options]")

if __name__ == "__main__":
    main()
