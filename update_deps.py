#!/usr/bin/env python3
"""
Dependency update script for AI Information Gathering Agent
"""

import os
import sys
import subprocess
import json

def update_python_dependencies():
    """Update Python dependencies."""
    print("Updating Python dependencies...")
    try:
        # Check if requirements.txt exists
        if not os.path.exists('requirements.txt'):
            print("⚠ requirements.txt not found")
            return False
        
        # Update pip first
        print("Updating pip...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                      check=True, capture_output=True)
        print("✓ Pip updated successfully")
        
        # Update all Python dependencies
        print("Updating Python packages...")
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', '-r', 'requirements.txt'], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Python dependencies updated successfully")
            return True
        else:
            print(f"✗ Failed to update Python dependencies: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to update Python dependencies: {e}")
        return False
    except Exception as e:
        print(f"✗ Failed to update Python dependencies: {e}")
        return False

def update_node_dependencies():
    """Update Node.js dependencies."""
    print("Updating Node.js dependencies...")
    try:
        # Check if package.json exists
        if not os.path.exists('package.json'):
            print("⚠ package.json not found")
            return False
        
        # Check if Node.js is available
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("⚠ Node.js not found")
            return False
        
        # Update npm first
        print("Updating npm...")
        subprocess.run(['npm', 'install', '-g', 'npm'], check=True, capture_output=True)
        print("✓ npm updated successfully")
        
        # Update Node.js dependencies
        print("Updating Node.js packages...")
        result = subprocess.run(['npm', 'update'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Node.js dependencies updated successfully")
            return True
        else:
            print(f"✗ Failed to update Node.js dependencies: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to update Node.js dependencies: {e}")
        return False
    except Exception as e:
        print(f"✗ Failed to update Node.js dependencies: {e}")
        return False

def check_outdated_python_packages():
    """Check for outdated Python packages."""
    print("Checking for outdated Python packages...")
    try:
        # Run pip list --outdated
        result = subprocess.run([sys.executable, '-m', 'pip', 'list', '--outdated', '--format=json'], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            outdated_packages = json.loads(result.stdout)
            if outdated_packages:
                print("Outdated Python packages:")
                for package in outdated_packages:
                    print(f"  - {package['name']}: {package['version']} → {package['latest_version']}")
                return True
            else:
                print("✓ All Python packages are up to date")
                return True
        else:
            print(f"✗ Failed to check outdated Python packages: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Failed to check outdated Python packages: {e}")
        return False

def check_outdated_node_packages():
    """Check for outdated Node.js packages."""
    print("Checking for outdated Node.js packages...")
    try:
        # Check if package.json exists
        if not os.path.exists('package.json'):
            print("⚠ package.json not found")
            return False
        
        # Run npm outdated
        result = subprocess.run(['npm', 'outdated', '--json'], capture_output=True, text=True)
        if result.returncode == 0:
            # npm outdated returns 0 even when there are outdated packages
            try:
                outdated_packages = json.loads(result.stdout) if result.stdout.strip() else {}
                if outdated_packages:
                    print("Outdated Node.js packages:")
                    for package, info in outdated_packages.items():
                        current = info.get('current', 'N/A')
                        latest = info.get('latest', 'N/A')
                        print(f"  - {package}: {current} → {latest}")
                    return True
                else:
                    print("✓ All Node.js packages are up to date")
                    return True
            except json.JSONDecodeError:
                # Handle case where output is not JSON
                if result.stdout.strip():
                    print("Outdated Node.js packages:")
                    print(result.stdout)
                    return True
                else:
                    print("✓ All Node.js packages are up to date")
                    return True
        else:
            print(f"✗ Failed to check outdated Node.js packages: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Failed to check outdated Node.js packages: {e}")
        return False

def generate_requirements_txt():
    """Generate requirements.txt from current environment."""
    print("Generating requirements.txt...")
    try:
        # Generate requirements.txt
        with open('requirements.txt', 'w') as f:
            subprocess.run([sys.executable, '-m', 'pip', 'freeze'], stdout=f, check=True)
        
        print("✓ requirements.txt generated successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to generate requirements.txt: {e}")
        return False
    except Exception as e:
        print(f"✗ Failed to generate requirements.txt: {e}")
        return False

def generate_package_lock():
    """Generate package-lock.json by reinstalling dependencies."""
    print("Generating package-lock.json...")
    try:
        # Check if package.json exists
        if not os.path.exists('package.json'):
            print("⚠ package.json not found")
            return False
        
        # Remove existing package-lock.json and node_modules
        if os.path.exists('package-lock.json'):
            os.remove('package-lock.json')
            print("Removed existing package-lock.json")
        
        if os.path.exists('node_modules'):
            import shutil
            shutil.rmtree('node_modules')
            print("Removed existing node_modules")
        
        # Install dependencies to generate package-lock.json
        result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ package-lock.json generated successfully")
            return True
        else:
            print(f"✗ Failed to generate package-lock.json: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Failed to generate package-lock.json: {e}")
        return False

def main():
    """Main function to handle dependency updates."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Dependency update utility for AI Information Gathering Agent')
    parser.add_argument('--python', action='store_true', help='Update Python dependencies only')
    parser.add_argument('--node', action='store_true', help='Update Node.js dependencies only')
    parser.add_argument('--check', action='store_true', help='Check for outdated dependencies only')
    parser.add_argument('--generate', action='store_true', help='Generate dependency files (requirements.txt, package-lock.json)')
    parser.add_argument('--all', '-a', action='store_true', help='Perform all dependency operations')
    
    args = parser.parse_args()
    
    print("AI Information Gathering Agent - Dependency Update")
    print("=" * 45)
    
    # If no arguments provided, show help
    if not any([args.python, args.node, args.check, args.generate, args.all]):
        parser.print_help()
        return
    
    success = True
    
    # Check for outdated dependencies
    if args.all or args.check:
        print("\nChecking for outdated dependencies:")
        if not check_outdated_python_packages():
            success = False
        if not check_outdated_node_packages():
            success = False
    
    # Update Python dependencies
    if args.all or args.python:
        print("\nUpdating Python dependencies:")
        if not update_python_dependencies():
            success = False
    
    # Update Node.js dependencies
    if args.all or args.node:
        print("\nUpdating Node.js dependencies:")
        if not update_node_dependencies():
            success = False
    
    # Generate dependency files
    if args.all or args.generate:
        print("\nGenerating dependency files:")
        if not generate_requirements_txt():
            success = False
        if not generate_package_lock():
            success = False
    
    print("\n" + "=" * 45)
    if success:
        print("✓ Dependency operations completed successfully!")
    else:
        print("⚠ Some dependency operations failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()
