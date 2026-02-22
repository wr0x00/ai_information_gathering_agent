#!/usr/bin/env python3
"""
Version information script for AI Information Gathering Agent
"""

import os
import sys
import subprocess
import django
from django.core.management import execute_from_command_line

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ai_agent.ai_agent_project.settings')

def get_project_version():
    """Get the project version from various sources."""
    version = "Unknown"
    
    # Try to get version from pyproject.toml
    try:
        import toml
        if os.path.exists('django_ai_agent/pyproject.toml'):
            with open('django_ai_agent/pyproject.toml', 'r') as f:
                pyproject = toml.load(f)
                version = pyproject.get('tool', {}).get('poetry', {}).get('version', version)
    except ImportError:
        # Try to get version from setup.py
        try:
            if os.path.exists('django_ai_agent/setup.py'):
                # This is a simplified approach - in practice, you'd want to execute setup.py properly
                with open('django_ai_agent/setup.py', 'r') as f:
                    content = f.read()
                    if 'version=' in content:
                        # Extract version string (simplified)
                        import re
                        version_match = re.search(r"version\s*=\s*['\"]([^'\"]*)['\"]", content)
                        if version_match:
                            version = version_match.group(1)
        except Exception:
            pass
    except Exception:
        pass
    
    return version

def get_python_version():
    """Get Python version."""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

def get_django_version():
    """Get Django version."""
    try:
        import django
        return django.get_version()
    except ImportError:
        return "Not installed"

def get_installed_packages():
    """Get list of installed packages."""
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return "Failed to get package list"
    except Exception as e:
        return f"Error getting package list: {e}"

def get_git_info():
    """Get Git repository information."""
    try:
        # Get current branch
        branch_result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                                      capture_output=True, text=True)
        branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "Unknown"
        
        # Get latest commit hash
        commit_result = subprocess.run(['git', 'rev-parse', 'HEAD'], 
                                     capture_output=True, text=True)
        commit_hash = commit_result.stdout.strip() if commit_result.returncode == 0 else "Unknown"
        
        # Get latest commit message
        message_result = subprocess.run(['git', 'log', '-1', '--pretty=%B'], 
                                       capture_output=True, text=True)
        commit_message = message_result.stdout.strip() if message_result.returncode == 0 else "Unknown"
        
        # Get commit date
        date_result = subprocess.run(['git', 'log', '-1', '--pretty=%ci'], 
                                    capture_output=True, text=True)
        commit_date = date_result.stdout.strip() if date_result.returncode == 0 else "Unknown"
        
        return {
            'branch': branch,
            'commit_hash': commit_hash,
            'commit_message': commit_message,
            'commit_date': commit_date
        }
    except Exception as e:
        return {
            'branch': 'Unknown',
            'commit_hash': 'Unknown',
            'commit_message': 'Unknown',
            'commit_date': 'Unknown'
        }

def get_system_info():
    """Get system information."""
    import platform
    return {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'python_implementation': platform.python_implementation(),
        'python_version': platform.python_version()
    }

def main():
    """Main function to display version information."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Display version information for AI Information Gathering Agent')
    parser.add_argument('--detailed', '-d', action='store_true', help='Show detailed information')
    parser.add_argument('--packages', '-p', action='store_true', help='Show installed packages')
    parser.add_argument('--system', '-s', action='store_true', help='Show system information')
    
    args = parser.parse_args()
    
    print("AI Information Gathering Agent - Version Information")
    print("=" * 50)
    
    # Project version
    project_version = get_project_version()
    print(f"Project Version: {project_version}")
    
    # Python version
    python_version = get_python_version()
    print(f"Python Version: {python_version}")
    
    # Django version
    django_version = get_django_version()
    print(f"Django Version: {django_version}")
    
    # Git information
    if os.path.exists('.git'):
        git_info = get_git_info()
        print(f"Git Branch: {git_info['branch']}")
        print(f"Git Commit: {git_info['commit_hash'][:8]}")
        if args.detailed:
            print(f"Commit Message: {git_info['commit_message']}")
            print(f"Commit Date: {git_info['commit_date']}")
    
    # Detailed information
    if args.detailed:
        print("\nDetailed Information:")
        print("-" * 20)
        
        # Environment variables
        print("Environment Variables:")
        env_vars = ['DJANGO_SETTINGS_MODULE', 'PYTHONPATH', 'VIRTUAL_ENV']
        for var in env_vars:
            value = os.environ.get(var, 'Not set')
            print(f"  {var}: {value}")
    
    # System information
    if args.system or args.detailed:
        print("\nSystem Information:")
        print("-" * 18)
        system_info = get_system_info()
        for key, value in system_info.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
    
    # Installed packages
    if args.packages or args.detailed:
        print("\nInstalled Packages:")
        print("-" * 18)
        packages = get_installed_packages()
        print(packages)

if __name__ == '__main__':
    main()
