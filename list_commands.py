#!/usr/bin/env python3
"""
Command listing script for AI Information Gathering Agent
"""

import os
import sys

def list_management_commands():
    """List Django management commands."""
    commands = [
        ("runserver", "Start the development server"),
        ("migrate", "Apply database migrations"),
        ("makemigrations", "Create new database migrations"),
        ("collectstatic", "Collect static files"),
        ("createsuperuser", "Create a superuser account"),
        ("shell", "Open Django shell"),
        ("dbshell", "Open database shell"),
        ("dumpdata", "Dump database data"),
        ("loaddata", "Load database data"),
        ("check", "Check for issues"),
        ("compilemessages", "Compile translation messages"),
        ("createcachetable", "Create cache table"),
        ("diffsettings", "Display differences in settings"),
        ("flush", "Remove all data from the database"),
        ("inspectdb", "Inspect database and output models"),
        ("loaddata", "Load data from fixture"),
        ("makemessages", "Create/update translation messages"),
        ("optimizemigration", "Optimize migration files"),
        ("showmigrations", "Show migration status"),
        ("sqlflush", "Return SQL for flushing database"),
        ("sqlmigrate", "Print SQL for migration"),
        ("squashmigrations", "Squash migrations"),
        ("startapp", "Create a new Django app"),
        ("test", "Run tests"),
    ]
    return commands

def list_custom_scripts():
    """List custom project scripts."""
    scripts = [
        ("init_db.py", "Initialize the database"),
        ("run_tests.py", "Run the test suite"),
        ("create_superuser.py", "Create a superuser account"),
        ("backup_db.py", "Backup the database"),
        ("restore_db.py", "Restore the database from backup"),
        ("list_backups.py", "List available database backups"),
        ("cleanup_backups.py", "Clean up old database backups"),
        ("check_health.py", "Check application health"),
        ("generate_docs.py", "Generate documentation"),
        ("maintenance.py", "Perform maintenance tasks"),
        ("export_data.py", "Export data from the database"),
        ("import_data.py", "Import data into the database"),
        ("reset_db.py", "Reset the database"),
        ("update_deps.py", "Update project dependencies"),
        ("run_prod.py", "Run in production mode"),
        ("show_version.py", "Show version information"),
        ("list_commands.py", "List available commands"),
    ]
    return scripts

def list_make_commands():
    """List Makefile commands."""
    commands = [
        ("make setup", "Install all dependencies"),
        ("make setup-dev", "Install development dependencies"),
        ("make run", "Start development server"),
        ("make build-frontend", "Build React frontend"),
        ("make dev-frontend", "Start frontend development server"),
        ("make migrate", "Run database migrations"),
        ("make makemigrations", "Create database migrations"),
        ("make test", "Run tests"),
        ("make test-coverage", "Run tests with coverage"),
        ("make clean", "Clean Python cache files"),
        ("make docker-build", "Build Docker images"),
        ("make docker-up", "Start Docker containers"),
        ("make docker-down", "Stop Docker containers"),
        ("make docker-logs", "View Docker logs"),
        ("make superuser", "Create Django superuser"),
        ("make collectstatic", "Collect static files"),
        ("make check", "Run Django system checks"),
        ("make shell", "Open Django shell"),
    ]
    return commands

def list_docker_commands():
    """List Docker commands."""
    commands = [
        ("docker-compose up", "Start all services"),
        ("docker-compose down", "Stop all services"),
        ("docker-compose build", "Build services"),
        ("docker-compose logs", "View service logs"),
        ("docker-compose exec", "Execute command in container"),
        ("docker ps", "List running containers"),
        ("docker images", "List images"),
        ("docker logs", "View container logs"),
    ]
    return commands

def main():
    """Main function to list all available commands."""
    import argparse
    
    parser = argparse.ArgumentParser(description='List available commands for AI Information Gathering Agent')
    parser.add_argument('--category', choices=['all', 'management', 'scripts', 'make', 'docker'], 
                       default='all', help='Command category to display')
    
    args = parser.parse_args()
    
    print("AI Information Gathering Agent - Available Commands")
    print("=" * 50)
    
    # Django Management Commands
    if args.category in ['all', 'management']:
        print("\nDjango Management Commands:")
        print("-" * 25)
        management_commands = list_management_commands()
        for cmd, desc in management_commands:
            print(f"  python manage.py {cmd:<20} - {desc}")
    
    # Custom Scripts
    if args.category in ['all', 'scripts']:
        print("\nCustom Scripts:")
        print("-" * 15)
        custom_scripts = list_custom_scripts()
        for script, desc in custom_scripts:
            print(f"  python {script:<20} - {desc}")
    
    # Make Commands
    if args.category in ['all', 'make']:
        print("\nMake Commands:")
        print("-" * 13)
        make_commands = list_make_commands()
        for cmd, desc in make_commands:
            print(f"  {cmd:<25} - {desc}")
    
    # Docker Commands
    if args.category in ['all', 'docker']:
        print("\nDocker Commands:")
        print("-" * 15)
        docker_commands = list_docker_commands()
        for cmd, desc in docker_commands:
            print(f"  {cmd:<25} - {desc}")
    
    print("\n" + "=" * 50)
    print("For more information on a specific command, use --help")
    print("Example: python init_db.py --help")

if __name__ == '__main__':
    main()
