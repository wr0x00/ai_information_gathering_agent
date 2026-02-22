#!/usr/bin/env python3
"""
Main entry point for the AI Information Gathering Agent
"""
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main function to run the AI agent"""
    print("AI Information Gathering Agent")
    print("==============================")
    print("1. Run CLI interface")
    print("2. Start web interface")
    print("3. Run tests")
    print("4. Exit")
    
    choice = input("Select an option (1-4): ").strip()
    
    if choice == "1":
        # Run CLI interface
        from cli import main as cli_main
        cli_main()
    elif choice == "2":
        # Start web interface
        print("Starting web interface...")
        print("Navigate to http://localhost:8000 in your browser")
        os.system("python manage.py runserver")
    elif choice == "3":
        # Run tests
        print("Running tests...")
        # Add test execution here
        print("Tests completed.")
    elif choice == "4":
        print("Exiting...")
        sys.exit(0)
    else:
        print("Invalid choice. Exiting...")
        sys.exit(1)

if __name__ == "__main__":
    main()
