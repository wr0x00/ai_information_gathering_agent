#!/usr/bin/env python3
"""
Cleanup old database backups script for the AI Information Gathering Agent
"""
import os
import sys
import datetime

def cleanup_backups(days=7):
    """Clean up old database backups"""
    print(f"Cleaning up backups older than {days} days...")
    
    # Calculate cutoff date
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
    
    # List available backups
    backups = [f for f in os.listdir('.') if f.startswith('db_backup_') and f.endswith('.sqlite3')]
    
    if not backups:
        print("No backups found!")
        return
    
    deleted_count = 0
    
    for backup in backups:
        # Try to extract timestamp from filename
        try:
            timestamp_str = backup.replace('db_backup_', '').replace('.sqlite3', '')
            timestamp = datetime.datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
            
            # Check if backup is older than cutoff date
            if timestamp < cutoff_date:
                try:
                    os.remove(backup)
                    print(f"Deleted old backup: {backup}")
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting backup {backup}: {e}")
        except ValueError:
            # If we can't parse the timestamp, skip this backup
            print(f"Skipping backup with invalid timestamp: {backup}")
    
    print(f"Cleanup complete. Deleted {deleted_count} old backups.")

if __name__ == "__main__":
    # Check if days argument is provided
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
            cleanup_backups(days)
        except ValueError:
            print("Invalid days argument. Using default 7 days.")
            cleanup_backups()
    else:
        cleanup_backups()
