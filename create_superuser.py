#!/usr/bin/env python3
"""
Script to create Django superuser for AI Information Gathering Agent
"""

import os
import sys
import django
from django.contrib.auth import get_user_model
from django.core.management import execute_from_command_line
import getpass

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ai_agent.ai_agent_project.settings')

def main():
    """Create a Django superuser."""
    print("Creating Django superuser for AI Information Gathering Agent...")
    
    try:
        # Setup Django
        django.setup()
        
        User = get_user_model()
        
        # Check if superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            print("Superuser already exists.")
            # Ask if user wants to create another superuser
            create_another = input("Do you want to create another superuser? (y/N): ").lower().strip()
            if create_another != 'y' and create_another != 'yes':
                print("Exiting...")
                return
        
        # Get user input
        username = input("Username: ").strip()
        if not username:
            print("Username cannot be empty.")
            return
            
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            print(f"User '{username}' already exists.")
            return
            
        email = input("Email (optional): ").strip()
        password = getpass.getpass("Password: ")
        password_confirm = getpass.getpass("Password (confirm): ")
        
        if password != password_confirm:
            print("Passwords do not match.")
            return
            
        if len(password) < 8:
            print("Password must be at least 8 characters long.")
            return
        
        # Create superuser
        user = User.objects.create_superuser(
            username=username,
            email=email if email else '',
            password=password
        )
        
        print(f"Superuser '{username}' created successfully!")
        print(f"User ID: {user.id}")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"Error creating superuser: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
