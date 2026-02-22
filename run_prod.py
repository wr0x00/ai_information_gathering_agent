#!/usr/bin/env python3
"""
Production runner script for AI Information Gathering Agent
"""

import os
import sys
import subprocess
import django
from django.core.management import execute_from_command_line

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ai_agent.ai_agent_project.settings')

def check_production_ready():
    """Check if the application is ready for production."""
    print("Checking production readiness...")
    try:
        # Setup Django
        django.setup()
        
        # Check if DEBUG is disabled
        from django.conf import settings
        if settings.DEBUG:
            print("⚠ WARNING: DEBUG is enabled. Should be disabled in production.")
        else:
            print("✓ DEBUG is disabled")
        
        # Check if SECRET_KEY is properly set
        if not settings.SECRET_KEY or settings.SECRET_KEY == 'your-secret-key-here':
            print("✗ ERROR: SECRET_KEY is not properly configured for production.")
            return False
        else:
            print("✓ SECRET_KEY is properly configured")
        
        # Check if ALLOWED_HOSTS is configured
        if not settings.ALLOWED_HOSTS or settings.ALLOWED_HOSTS == ['*']:
            print("✗ ERROR: ALLOWED_HOSTS is not properly configured for production.")
            return False
        else:
            print("✓ ALLOWED_HOSTS is properly configured")
        
        # Check if static files are collected
        static_root = getattr(settings, 'STATIC_ROOT', None)
        if not static_root:
            print("⚠ WARNING: STATIC_ROOT is not configured.")
        elif not os.path.exists(static_root) or not os.listdir(static_root):
            print("⚠ WARNING: Static files are not collected. Run 'python manage.py collectstatic'.")
        else:
            print("✓ Static files are collected")
        
        # Check if database is migrated
        from django.core.management import execute_from_command_line
        import io
        from contextlib import redirect_stdout, redirect_stderr
        
        # Capture output
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            try:
                execute_from_command_line(['manage.py', 'migrate', '--check'])
                print("✓ Database migrations are up to date")
            except SystemExit:
                # migrate --check exits with code 1 if migrations are not applied
                output = stdout_capture.getvalue() + stderr_capture.getvalue()
                if "unapplied migration(s)" in output:
                    print("✗ ERROR: Unapplied migrations detected. Run 'python manage.py migrate'.")
                    return False
                else:
                    print("✓ Database migrations are up to date")
        
        print("✓ Production readiness check completed")
        return True
        
    except Exception as e:
        print(f"✗ Production readiness check failed: {e}")
        return False

def collect_static_files():
    """Collect static files for production."""
    print("Collecting static files...")
    try:
        # Setup Django
        django.setup()
        
        # Collect static files
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '-c'])
        
        print("✓ Static files collected successfully")
        return True
        
    except Exception as e:
        print(f"✗ Failed to collect static files: {e}")
        return False

def run_production_server(bind_address='0.0.0.0', port=8000, workers=4):
    """Run the production server using Gunicorn."""
    print(f"Starting production server on {bind_address}:{port}...")
    try:
        # Check if Gunicorn is available
        result = subprocess.run([sys.executable, '-m', 'gunicorn', '--version'], 
                               capture_output=True, text=True)
        if result.returncode != 0:
            print("⚠ Gunicorn not found. Installing...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'gunicorn'], 
                          check=True, capture_output=True)
            print("✓ Gunicorn installed successfully")
        
        # Run Gunicorn with Django application
        gunicorn_cmd = [
            sys.executable, '-m', 'gunicorn',
            '--bind', f'{bind_address}:{port}',
            '--workers', str(workers),
            '--timeout', '120',
            '--keep-alive', '5',
            '--max-requests', '1000',
            '--max-requests-jitter', '100',
            '--preload',
            'django_ai_agent.ai_agent_project.wsgi:application'
        ]
        
        print(f"Running: {' '.join(gunicorn_cmd)}")
        subprocess.run(gunicorn_cmd, check=True)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to start production server: {e}")
        return False
    except Exception as e:
        print(f"✗ Failed to start production server: {e}")
        return False

def run_docker_compose():
    """Run the application using Docker Compose."""
    print("Starting application with Docker Compose...")
    try:
        # Check if docker-compose.yml exists
        if not os.path.exists('docker-compose.yml'):
            print("✗ docker-compose.yml not found")
            return False
        
        # Run docker-compose up
        subprocess.run(['docker-compose', 'up', '-d'], check=True)
        
        print("✓ Application started with Docker Compose")
        print("Access the application at http://localhost:8000")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to start with Docker Compose: {e}")
        return False
    except Exception as e:
        print(f"✗ Failed to start with Docker Compose: {e}")
        return False

def main():
    """Main function to run the application in production mode."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Production runner for AI Information Gathering Agent')
    parser.add_argument('--bind', default='0.0.0.0', help='Bind address (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8000, help='Port to listen on (default: 8000)')
    parser.add_argument('--workers', type=int, default=4, help='Number of worker processes (default: 4)')
    parser.add_argument('--check', action='store_true', help='Check production readiness only')
    parser.add_argument('--collect-static', action='store_true', help='Collect static files only')
    parser.add_argument('--docker', action='store_true', help='Run with Docker Compose')
    
    args = parser.parse_args()
    
    print("AI Information Gathering Agent - Production Runner")
    print("=" * 45)
    
    # If Docker mode is selected
    if args.docker:
        if run_docker_compose():
            print("✓ Application is running in Docker containers")
        else:
            print("✗ Failed to start application with Docker Compose")
            sys.exit(1)
        return
    
    # Check production readiness
    if not check_production_ready():
        print("✗ Application is not ready for production!")
        print("Fix the issues above before running in production.")
        sys.exit(1)
    
    # If check only mode
    if args.check:
        print("✓ Application is ready for production!")
        return
    
    # Collect static files if requested
    if args.collect_static:
        if collect_static_files():
            print("✓ Static files collected successfully")
        else:
            print("✗ Failed to collect static files")
            sys.exit(1)
        return
    
    # Run production server
    print(f"\nStarting production server on {args.bind}:{args.port}...")
    if run_production_server(args.bind, args.port, args.workers):
        print("✓ Production server started successfully")
        print(f"Access the application at http://{args.bind}:{args.port}")
    else:
        print("✗ Failed to start production server")
        sys.exit(1)

if __name__ == '__main__':
    main()
