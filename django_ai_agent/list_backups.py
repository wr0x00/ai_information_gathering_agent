#!/usr/bin/env python3
"""
List database backups script for the AI Information Gathering Agent
"""
import os
import sys
import datetime

def list_backups():
    """List all available database backups"""
    print("Listing database backups...")
    
    # List available backups
    backups = [f for f in os.listdir('.') if f.startswith('db_backup_') and f.endswith('.sqlite3')]
    
    if not backups:
        print("No backups found!")
        return
    
    print("Available backups:")
    for backup in sorted(backups, reverse=True):
        # Try to extract timestamp from filename
        try:
            timestamp_str = backup.replace('db_backup_', '').replace('.sqlite3', '')
            timestamp = datetime.datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
            print(f"- {backup} (Created: {timestamp.strftime('%Y-%m-%d %H:%M:%S')})")
        except ValueError:
            print(f"- {backup}")

if __name__ == "__main__":
    list_backups()
