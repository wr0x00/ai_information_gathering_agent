#!/usr/bin/env python3
"""
Health check script for the AI Information Gathering Agent
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
    
    # Check local modules
    local_modules = [
        'config',
        'http_client',
        'base_module',
        'modules.whois_module',
        'modules.domain_module',
        'modules.port_module',
        'modules.sensitive_info_module',
        'modules.github_module',
        'agent',
        'storage'
    ]
    
    print("Checking local modules...")
    for module in local_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module} - {e}")
            return False
    
    print("All health checks passed!")
    return True

if __name__ == "__main__":
    if check_health():
        sys.exit(0)
    else:
        sys.exit(1)
