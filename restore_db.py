#!/usr/bin/env python3
"""
Database restore script for AI Information Gathering Agent
"""

import os
import sys
import shutil
import datetime
from backup_db import list_backups, BACKUP_DIR, DEFAULT_DB_PATH

def restore_backup(backup_name, db_path=DEFAULT_DB_PATH, backup_dir=BACKUP_DIR):
    """Restore a database backup."""
    try:
        # Check if database exists and warn user
        if os.path.exists(db_path):
            print(f"Warning: Database file already exists: {db_path}")
            confirm = input("Do you want to overwrite it? (y/N): ").lower().strip()
            if confirm != 'y' and confirm != 'yes':
                print("Restore cancelled.")
                return False
        
        # Check if backup exists
        backup_path = os.path.join(backup_dir, backup_name)
        if not os.path.exists(backup_path):
            print(f"Backup file not found: {backup_path}")
            return False
            
        # Create parent directory for database if it doesn't exist
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        
        # Copy backup to database location
        shutil.copy2(backup_path, db_path)
        
        print(f"Database restored successfully from: {backup_path}")
        return True
        
    except Exception as e:
        print(f"Error restoring database backup: {e}")
        return False

def main():
    """Main function to handle restore operations."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Database restore utility for AI Information Gathering Agent')
    parser.add_argument('backup_name', nargs='?', help='Name of the backup file to restore')
    parser.add_argument('--db-path', default=DEFAULT_DB_PATH, help='Path to the database file')
    parser.add_argument('--backup-dir', default=BACKUP_DIR, help='Directory where backups are stored')
    parser.add_argument('--list', '-l', action='store_true', help='List all available backups')
    
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
            print("\nTo restore a backup, run: python restore_db.py <backup_name>")
        else:
            print("No backups found.")
    elif args.backup_name:
        # Restore the specified backup
        print(f"Restoring database from backup: {args.backup_name}")
        if restore_backup(args.backup_name, args.db_path, args.backup_dir):
            print("Restore completed successfully!")
        else:
            print("Restore failed!")
            sys.exit(1)
    else:
        # Show usage
        parser.print_help()
        print("\nTo see available backups, run: python restore_db.py --list")

if __name__ == '__main__':
    main()
