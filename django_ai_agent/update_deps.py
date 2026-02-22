#!/usr/bin/env python3
"""
Dependency update script for the AI Information Gathering Agent
"""
import os
import sys
import subprocess

def update_pip():
    """Update pip to the latest version"""
    print("Updating pip...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        print("Pip updated successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error updating pip: {e}")

def update_dependencies():
    """Update all dependencies"""
    print("Updating dependencies...")
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("requirements.txt not found!")
        return
    
    try:
        # Update all dependencies
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', '-r', 'requirements.txt'])
        print("Dependencies updated successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error updating dependencies: {e}")

def update_specific_package(package):
    """Update a specific package"""
    print(f"Updating {package}...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', package])
        print(f"{package} updated successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error updating {package}: {e}")

def list_outdated_packages():
    """List outdated packages"""
    print("Checking for outdated packages...")
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'list', '--outdated'], 
                              capture_output=True, text=True)
        if result.stdout:
            print("Outdated packages:")
            print(result.stdout)
        else:
            print("All packages are up to date!")
    except subprocess.CalledProcessError as e:
        print(f"Error checking for outdated packages: {e}")

def main():
    """Main function"""
    print("Dependency update utility")
    print("========================")
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'pip':
            update_pip()
        elif command == 'all':
            update_dependencies()
        elif command == 'list':
            list_outdated_packages()
        elif command == 'package' and len(sys.argv) > 2:
            update_specific_package(sys.argv[2])
        else:
            print("Invalid command!")
            print("Usage: python update_deps.py [pip|all|list|package <package_name>]")
    else:
        # Interactive mode
        print("1. Update pip")
        print("2. Update all dependencies")
        print("3. List outdated packages")
        print("4. Update specific package")
        
        choice = input("Select an option (1-4): ").strip()
        
        if choice == '1':
            update_pip()
        elif choice == '2':
            update_dependencies()
        elif choice == '3':
            list_outdated_packages()
        elif choice == '4':
            package = input("Enter package name: ").strip()
            if package:
                update_specific_package(package)
            else:
                print("Package name cannot be empty!")
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
