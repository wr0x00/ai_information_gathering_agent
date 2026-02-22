#!/usr/bin/env python3
"""
Version display script for the AI Information Gathering Agent
"""
import os
import sys

def show_version():
    """Show the application version"""
    # Try to get version from __init__.py
    try:
        # Add the project root to the Python path
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # Import the version
        from __init__ import __version__
        print(f"AI Information Gathering Agent v{__version__}")
    except ImportError:
        print("AI Information Gathering Agent v1.0.0 (development version)")
    
    # Show Python version
    print(f"Python version: {sys.version}")
    
    # Show platform information
    import platform
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.architecture()[0]}")
    
    # Show Django version if available
    try:
        import django
        print(f"Django version: {django.get_version()}")
    except ImportError:
        print("Django: Not installed")

if __name__ == "__main__":
    show_version()
