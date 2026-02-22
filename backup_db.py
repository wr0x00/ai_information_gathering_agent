#!/usr/bin/env python3
"""
Database backup script for AI Information Gathering Agent
"""

import os
import sys
import shutil
import datetime
import sqlite3
from pathlib import Path

# Default database path
DEFAULT_DB_PATH = "django_ai_agent/db.sqlite3"
BACKUP_DIR = "backups"

def create_backup(db_path=DEFAULT_DB_PATH, backup_dir=BACKUP_DIR):
    """Create a backup of the SQLite database."""
    try:
        # Check if database exists
        if not os.path.exists(db_path):
            print(f"Database file not found: {db_path}")
            return False
            
        # Create backup directory if it doesn't exist
        os.makedirs(backup_dir, exist_ok=True)
        
        # Generate timestamped backup filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        db_name = os.path.basename(db_path)
        backup_filename = f"{db_name}_backup_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Copy database file
        shutil.copy2(db_path, backup_path)
        
        print(f"Database backup created successfully: {backup_path}")
        return True
        
    except Exception as e:
        print(f"Error creating database backup: {e}")
        return False

def list_backups(backup_dir=BACKUP_DIR):
    """List all available backups."""
    try:
        if not os.path.exists(backup_dir):
            print(f"Backup directory not found: {backup_dir}")
            return []
            
        backups = []
        for file in os.listdir(backup_dir):
            if file.endswith('.db'):
                file_path = os.path.join(backup_dir, file)
                stat = os.stat(file_path)
                backups.append({
                    'name': file,
                    'path': file_path,
                    'size': stat.st_size,
                    'modified': datetime.datetime.fromtimestamp(stat.st_mtime)
                })
        
        # Sort by modification time (newest first)
        backups.sort(key=lambda x: x['modified'], reverse=True)
        
        return backups
        
    except Exception as e:
        print(f"Error listing backups: {e}")
        return []

def main():
    """Main function to handle backup operations."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Database backup utility for AI Information Gathering Agent')
    parser.add_argument('--db-path', default=DEFAULT_DB_PATH, help='Path to the database file')
    parser.add_argument('--backup-dir', default=BACKUP_DIR, help='Directory to store backups')
    parser.add_argument('--list', '-l', action='store_true', help='List all backups')
    
    args = parser.parse_args()
    
    if args.list:
        # List all backups
        backups = list_backups(args.backup_dir)
        if backups:
            print(f"\nAvailable backups in '{args.backup_dir}':")
            print("-" * 80)
            print(f"{'Name':<30} {'Size':<15} {'Modified':<20}")
            print("-" * 80)
            for backup in backups:
                size_kb = backup['size'] / 1024
                print(f"{backup['name']:<30} {size_kb:.1f} KB{'':<8} {backup['modified'].strftime('%Y-%m-%d %H:%M:%S'):<20}")
        else:
            print("No backups found.")
    else:
        # Create a new backup
        print("Creating database backup...")
        if create_backup(args.db_path, args.backup_dir):
            print("Backup completed successfully!")
        else:
            print("Backup failed!")
            sys.exit(1)

if __name__ == '__main__':
    main()
