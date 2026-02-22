#!/usr/bin/env python3
"""
Superuser creation script for the AI Information Gathering Agent
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

def create_superuser():
    """Create a superuser"""
    from django.contrib.auth import get_user_model
    from django.core.management import execute_from_command_line
    
    User = get_user_model()
    
    print("Creating superuser...")
    
    # Check if superuser already exists
    if User.objects.filter(is_superuser=True).exists():
        print("Superuser already exists!")
        return
    
    # Create superuser
    username = input("Username: ")
    email = input("Email: ")
    password = input("Password: ")
    
    if not username or not email or not password:
        print("All fields are required!")
        return
    
    try:
        User.objects.create_superuser(username, email, password)
        print("Superuser created successfully!")
    except Exception as e:
        print(f"Error creating superuser: {e}")

if __name__ == "__main__":
    create_superuser()
