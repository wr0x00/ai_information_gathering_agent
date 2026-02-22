#!/usr/bin/env python3
"""
Health check script for AI Information Gathering Agent
"""

import os
import sys
import subprocess
import socket
import django
from django.core.management import execute_from_command_line

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ai_agent.ai_agent_project.settings')

def check_python():
    """Check Python version."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} OK")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} - Upgrade to Python 3.8 or higher")
        return False

def check_django():
    """Check Django installation."""
    print("Checking Django installation...")
    try:
        import django
        version = django.VERSION
        print(f"✓ Django {version[0]}.{version[1]}.{version[2]} OK")
        return True
    except ImportError:
        print("✗ Django not installed")
        return False

def check_dependencies():
    """Check required dependencies."""
    print("Checking dependencies...")
    required_packages = [
        'djangorestframework',
        'django-cors-headers',
        'httpx',
        ' beautifulsoup4',
        'python-whois',
        'aiodns',
        'aiohttp'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_').split()[0].strip())
            print(f"✓ {package} OK")
        except ImportError:
            print(f"✗ {package} missing")
            missing_packages.append(package)
    
    return len(missing_packages) == 0

def check_database():
    """Check database connectivity."""
    print("Checking database connectivity...")
    try:
        django.setup()
        from django.db import connection
        from django.db.utils import OperationalError
        
        try:
            connection.ensure_connection()
            print("✓ Database connection OK")
            return True
        except OperationalError as e:
            print(f"✗ Database connection failed: {e}")
            return False
    except Exception as e:
        print(f"✗ Database check failed: {e}")
        return False

def check_migrations():
    """Check if migrations are applied."""
    print("Checking database migrations...")
    try:
        django.setup()
        
        # Run migrate check command
        from django.core.management import execute_from_command_line
        import io
        from contextlib import redirect_stdout, redirect_stderr
        
        # Capture output
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            try:
                execute_from_command_line(['manage.py', 'migrate', '--check'])
                print("✓ All migrations applied")
                return True
            except SystemExit:
                # migrate --check exits with code 1 if migrations are not applied
                output = stdout_capture.getvalue() + stderr_capture.getvalue()
                if "unapplied migration(s)" in output:
                    print("⚠ Unapplied migrations detected")
                    return True  # Not a critical error
                else:
                    print("✗ Migration check failed")
                    return False
    except Exception as e:
        print(f"✗ Migration check failed: {e}")
        return False

def check_static_files():
    """Check if static files are collected."""
    print("Checking static files...")
    static_dir = os.path.join('django_ai_agent', 'staticfiles')
    if os.path.exists(static_dir) and os.listdir(static_dir):
        print("✓ Static files directory exists and is not empty")
        return True
    else:
        print("⚠ Static files not collected or directory is empty")
        return True  # Not a critical error

def check_frontend_build():
    """Check if frontend is built."""
    print("Checking frontend build...")
    bundle_path = os.path.join('django_ai_agent', 'frontend_app', 'static', 'frontend', 'js', 'bundle.js')
    if os.path.exists(bundle_path):
        print("✓ Frontend bundle exists")
        return True
    else:
        print("⚠ Frontend bundle not found - run 'npm run build'")
        return True  # Not a critical error

def check_ports(port=8000):
    """Check if required ports are available."""
    print(f"Checking port {port} availability...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        
        if result == 0:
            print(f"⚠ Port {port} is already in use")
            return True  # Not a critical error
        else:
            print(f"✓ Port {port} is available")
            return True
    except Exception as e:
        print(f"✗ Port check failed: {e}")
        return False

def main():
    """Main function to run all health checks."""
    print("AI Information Gathering Agent - Health Check")
    print("=" * 50)
    
    checks = [
        check_python,
        check_django,
        check_dependencies,
        check_database,
        check_migrations,
        check_static_files,
        check_frontend_build,
        check_ports
    ]
    
    passed = 0
    total = len(checks)
    
    for check in checks:
        try:
            if check():
                passed += 1
            print()  # Add spacing between checks
        except Exception as e:
            print(f"✗ Check failed with exception: {e}\n")
    
    print("=" * 50)
    print(f"Health Check Summary: {passed}/{total} checks passed")
    
    if passed == total:
        print("✓ All checks passed - Application is healthy!")
        return 0
    elif passed >= total * 0.8:
        print("⚠ Most checks passed - Application is mostly healthy but may have minor issues")
        return 0
    else:
        print("✗ Many checks failed - Application may not function properly")
        return 1

if __name__ == '__main__':
    sys.exit(main())
