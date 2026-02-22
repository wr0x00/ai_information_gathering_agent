#!/usr/bin/env python3
"""
Test script to verify Django server can start without port permission issues
"""
import os
import sys
import subprocess
import time

def test_server_start():
    """Test that Django server starts correctly"""
    try:
        print("Testing Django server startup...")
        
        # Change to the django_ai_agent directory
        os.chdir("django_ai_agent")
        
        # Run migrations first
        print("Applying migrations...")
        subprocess.run([sys.executable, "manage.py", "migrate"], 
                      check=True, capture_output=True)
        
        # Try to start server on localhost only
        print("Starting server on localhost:8080...")
        process = subprocess.Popen([
            sys.executable, "manage.py", "runserver", "127.0.0.1:8080"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Give it a moment to start
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("SUCCESS: Server started successfully!")
            print("You can now access the web interface at http://localhost:8000")
            # Terminate the process
            process.terminate()
            process.wait()
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"ERROR: Server failed to start")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False
    finally:
        # Change back to original directory
        os.chdir("..")

if __name__ == "__main__":
    test_server_start()
