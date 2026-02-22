#!/usr/bin/env python3
"""
Test runner script for the AI Information Gathering Agent
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

def run_tests():
    """Run all tests"""
    from django.core.management import execute_from_command_line
    
    print("Running tests...")
    
    # Run tests
    execute_from_command_line(['manage.py', 'test'])
    
    print("Tests completed!")

if __name__ == "__main__":
    run_tests()
