#!/usr/bin/env python3
"""
Maintenance script for AI Information Gathering Agent
"""

import os
import sys
import subprocess
import shutil
import django
from django.core.management import execute_from_command_line

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ai_agent.ai_agent_project.settings')

def clean_pyc():
    """Remove Python bytecode files."""
    print("Cleaning Python bytecode files...")
    try:
        import pathlib
        
        # Count removed files
        removed_count = 0
        
        # Walk through directories
        for root, dirs, files in os.walk('.'):
            # Skip hidden directories and virtual environments
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['venv', 'env']]
            
            for file in files:
                if file.endswith('.pyc') or file.endswith('.pyo'):
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        print(f"Removed: {file_path}")
                        removed_count += 1
                    except Exception as e:
                        print(f"Failed to remove {file_path}: {e}")
        
        # Remove __pycache__ directories
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['venv', 'env']]
            
            if '__pycache__' in dirs:
                pycache_path = os.path.join(root, '__pycache__')
                try:
                    shutil.rmtree(pycache_path)
                    print(f"Removed: {pycache_path}")
                    removed_count += 1
                except Exception as e:
                    print(f"Failed to remove {pycache_path}: {e}")
        
        print(f"✓ Cleaned {removed_count} Python bytecode files/directories")
        return True
        
    except Exception as e:
        print(f"✗ Failed to clean Python bytecode files: {e}")
        return False

def update_dependencies():
    """Update project dependencies."""
    print("Updating dependencies...")
    try:
        # Update pip
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                      check=True, capture_output=True)
        print("✓ Updated pip")
        
        # Update Python dependencies
        if os.path.exists('requirements.txt'):
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', '-r', 'requirements.txt'], 
                          check=True, capture_output=True)
            print("✓ Updated Python dependencies")
        else:
            print("⚠ requirements.txt not found")
        
        # Update Node.js dependencies
        if os.path.exists('package.json'):
            result = subprocess.run(['npm', 'update'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ Updated Node.js dependencies")
            else:
                print(f"⚠ npm update had output: {result.stdout}")
        else:
            print("⚠ package.json not found")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to update dependencies: {e}")
        return False
    except Exception as e:
        print(f"✗ Failed to update dependencies: {e}")
        return False

def run_migrations():
    """Run database migrations."""
    print("Running database migrations...")
    try:
        # Setup Django
        django.setup()
        
        # Run migrations
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("✓ Database migrations completed")
        return True
        
    except Exception as e:
        print(f"✗ Failed to run migrations: {e}")
        return False

def collect_static():
    """Collect static files."""
    print("Collecting static files...")
    try:
        # Setup Django
        django.setup()
        
        # Collect static files
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '-c'])
        
        print("✓ Static files collected")
        return True
        
    except Exception as e:
        print(f"✗ Failed to collect static files: {e}")
        return False

def build_frontend():
    """Build frontend assets."""
    print("Building frontend assets...")
    try:
        # Check if Node.js is available
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("⚠ Node.js not found, skipping frontend build")
            return True
        
        # Check if package.json exists
        if not os.path.exists('package.json'):
            print("⚠ package.json not found, skipping frontend build")
            return True
        
        # Run npm build
        result = subprocess.run(['npm', 'run', 'build'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Frontend assets built successfully")
            return True
        else:
            print(f"✗ Frontend build failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Failed to build frontend assets: {e}")
        return False

def check_security():
    """Check for security vulnerabilities."""
    print("Checking for security vulnerabilities...")
    try:
        # Check Python dependencies for vulnerabilities
        result = subprocess.run([sys.executable, '-m', 'pip', 'check'], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ No dependency conflicts found")
        else:
            print(f"⚠ Dependency conflicts found: {result.stdout}")
        
        # Try to run safety check if available
        try:
            result = subprocess.run([sys.executable, '-m', 'safety', 'check'], 
                                   capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ No known security vulnerabilities found")
            else:
                print(f"⚠ Security check output: {result.stdout}")
        except FileNotFoundError:
            print("ℹ Safety package not installed, skipping detailed security check")
            print("  Install with: pip install safety")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to check security: {e}")
        return False

def main():
    """Main function to run maintenance tasks."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Maintenance tasks for AI Information Gathering Agent')
    parser.add_argument('--clean', action='store_true', help='Clean Python bytecode files')
    parser.add_argument('--update-deps', action='store_true', help='Update dependencies')
    parser.add_argument('--migrate', action='store_true', help='Run database migrations')
    parser.add_argument('--collect-static', action='store_true', help='Collect static files')
    parser.add_argument('--build-frontend', action='store_true', help='Build frontend assets')
    parser.add_argument('--security-check', action='store_true', help='Check for security vulnerabilities')
    parser.add_argument('--all', '-a', action='store_true', help='Run all maintenance tasks')
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if not any([args.clean, args.update_deps, args.migrate, args.collect_static, 
                args.build_frontend, args.security_check, args.all]):
        parser.print_help()
        return
    
    print("AI Information Gathering Agent - Maintenance")
    print("=" * 45)
    
    # Define tasks
    tasks = []
    if args.all or args.clean:
        tasks.append(("Clean Python bytecode", clean_pyc))
    if args.all or args.update_deps:
        tasks.append(("Update dependencies", update_dependencies))
    if args.all or args.migrate:
        tasks.append(("Run migrations", run_migrations))
    if args.all or args.collect_static:
        tasks.append(("Collect static files", collect_static))
    if args.all or args.build_frontend:
        tasks.append(("Build frontend", build_frontend))
    if args.all or args.security_check:
        tasks.append(("Security check", check_security))
    
    # Execute tasks
    successful = 0
    total = len(tasks)
    
    for task_name, task_func in tasks:
        print(f"\n{task_name}:")
        try:
            if task_func():
                successful += 1
            else:
                print(f"✗ {task_name} failed")
        except Exception as e:
            print(f"✗ {task_name} failed with exception: {e}")
    
    print("\n" + "=" * 45)
    print(f"Maintenance Summary: {successful}/{total} tasks completed successfully")
    
    if successful == total:
        print("✓ All maintenance tasks completed successfully!")
        return 0
    else:
        print("⚠ Some maintenance tasks failed.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
