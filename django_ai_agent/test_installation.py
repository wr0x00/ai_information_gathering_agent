#!/usr/bin/env python3
"""
Test script to verify the installation of the AI Information Gathering Agent
"""
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    required_modules = [
        'django',
        'rest_framework',
        'httpx',
        'yaml',
        'docx',
        'reportlab',
        'openai',
        'anthropic',
        'bs4',
        'lxml',
        'aiodns',
        'aiomysql',
        'async_timeout'
    ]
    
    print("Testing module imports...")
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module} - {e}")
    
    print("\nImport test completed.")

def test_local_imports():
    """Test that all local modules can be imported"""
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
        'storage',
        'cli'
    ]
    
    print("\nTesting local module imports...")
    for module in local_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module} - {e}")
    
    print("\nLocal import test completed.")

def test_django_setup():
    """Test Django setup"""
    try:
        import django
        from django.conf import settings
        
        # Configure Django settings
        if not settings.configured:
            settings.configure(
                DEBUG=True,
                DATABASES={
                    'default': {
                        'ENGINE': 'django.db.backends.sqlite3',
                        'NAME': ':memory:',
                    }
                },
                INSTALLED_APPS=[
                    'django.contrib.admin',
                    'django.contrib.auth',
                    'django.contrib.contenttypes',
                    'django.contrib.sessions',
                    'django.contrib.messages',
                    'django.contrib.staticfiles',
                    'rest_framework',
                    'frontend_app',
                    'config_app',
                    'keywords_app',
                    'reports_app',
                    'chat_app',
                ],
                SECRET_KEY='test-secret-key-for-testing-purposes-only',
                USE_TZ=True,
            )
        
        django.setup()
        print("✓ Django setup")
    except Exception as e:
        print(f"✗ Django setup - {e}")

def main():
    """Main test function"""
    print("AI Information Gathering Agent - Installation Test")
    print("=" * 50)
    
    test_imports()
    test_local_imports()
    test_django_setup()
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    main()
