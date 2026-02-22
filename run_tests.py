#!/usr/bin/env python3
"""
Test runner script for AI Information Gathering Agent
"""

import os
import sys
import django
from django.core.management import execute_from_command_line
import argparse

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ai_agent.ai_agent_project.settings')

def main():
    """Run the test suite for the AI Information Gathering Agent."""
    parser = argparse.ArgumentParser(description='Run tests for AI Information Gathering Agent')
    parser.add_argument('--coverage', action='store_true', help='Run tests with coverage')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--pattern', '-p', default='test*.py', help='Test pattern to match')
    
    args = parser.parse_args()
    
    try:
        # Setup Django
        django.setup()
        
        if args.coverage:
            # Run tests with coverage
            print("Running tests with coverage...")
            try:
                import coverage
                
                # Start coverage
                cov = coverage.Coverage(source=['.'])
                cov.start()
                
                # Run tests
                test_args = ['manage.py', 'test']
                if args.verbose:
                    test_args.append('-v')
                    test_args.append('2')
                test_args.extend(['--pattern', args.pattern])
                
                execute_from_command_line(test_args)
                
                # Stop coverage and generate report
                cov.stop()
                cov.save()
                print("\nCoverage Report:")
                cov.report()
                cov.html_report(directory='htmlcov')
                print("HTML coverage report generated in htmlcov/")
                
            except ImportError:
                print("Coverage package not installed. Install with: pip install coverage")
                print("Running tests without coverage...")
                test_args = ['manage.py', 'test']
                if args.verbose:
                    test_args.append('-v')
                    test_args.append('2')
                test_args.extend(['--pattern', args.pattern])
                execute_from_command_line(test_args)
        else:
            # Run tests normally
            print("Running tests...")
            test_args = ['manage.py', 'test']
            if args.verbose:
                test_args.append('-v')
                test_args.append('2')
            test_args.extend(['--pattern', args.pattern])
            execute_from_command_line(test_args)
            
        print("\nTest execution completed!")
        
    except Exception as e:
        print(f"Error running tests: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
