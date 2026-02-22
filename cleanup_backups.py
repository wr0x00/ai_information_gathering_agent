#!/usr/bin/env python3
"""
Script to clean up old database backups for AI Information Gathering Agent
"""

import os
import sys
import datetime
from backup_db import list_backups, BACKUP_DIR

def cleanup_backups(backup_dir=BACKUP_DIR, keep_days=30, keep_count=10):
    """Clean up old database backups."""
    try:
        # List all backups
        backups = list_backups(backup_dir)
        
        if not backups:
            print("No backups found.")
            return True
            
        # Sort backups by modification time (newest first)
        backups.sort(key=lambda x: x['modified'], reverse=True)
        
        # Determine which backups to keep
        now = datetime.datetime.now()
        to_keep = []
        to_delete = []
        
        # First, keep the specified number of recent backups
        recent_backups = backups[:keep_count]
        older_backups = backups[keep_count:]
        
        # For older backups, only keep those newer than keep_days
        cutoff_date = now - datetime.timedelta(days=keep_days)
        
        for backup in recent_backups:
            to_keep.append(backup)
            
        for backup in older_backups:
            if backup['modified'] >= cutoff_date:
                to_keep.append(backup)
            else:
                to_delete.append(backup)
        
        # Report what would be deleted
        if not to_delete:
            print(f"No backups to clean up. Keeping all {len(backups)} backups.")
            return True
            
        print(f"Found {len(to_delete)} backup(s) to clean up:")
        for backup in to_delete:
            age = now - backup['modified']
            print(f"  - {backup['name']} ({age.days} days old)")
            
        # Confirm deletion
        confirm = input(f"\nDelete these {len(to_delete)} backup(s)? (y/N): ").lower().strip()
        if confirm != 'y' and confirm != 'yes':
            print("Cleanup cancelled.")
            return True
            
        # Delete backups
        deleted_count = 0
        for backup in to_delete:
            try:
                os.remove(backup['path'])
                print(f"Deleted: {backup['name']}")
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting {backup['name']}: {e}")
                
        print(f"\nCleanup completed. Deleted {deleted_count}/{len(to_delete)} backup(s).")
        print(f"Kept {len(to_keep)} backup(s).")
        
        return True
        
    except Exception as e:
        print(f"Error cleaning up backups: {e}")
        return False

def main():
    """Main function to handle backup cleanup operations."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Clean up old database backups for AI Information Gathering Agent')
    parser.add_argument('--backup-dir', default=BACKUP_DIR, help='Directory where backups are stored')
    parser.add_argument('--keep-days', type=int, default=30, 
                       help='Keep backups newer than this many days (default: 30)')
    parser.add_argument('--keep-count', type=int, default=10, 
                       help='Always keep at least this many recent backups (default: 10)')
    parser.add_argument('--dry-run', '-n', action='store_true', 
                       help='Show what would be deleted without actually deleting')
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("*** DRY RUN MODE ***")
        print("No files will be deleted.")
        
    print(f"Cleaning up backups in '{args.backup_dir}'...")
    print(f"Keeping backups newer than {args.keep_days} days")
    print(f"Keeping at least {args.keep_count} recent backups")
    
    if args.dry_run:
        # Just list what would be deleted
        try:
            backups = list_backups(args.backup_dir)
            
            if not backups:
                print("No backups found.")
                return
                
            # Sort backups by modification time (newest first)
            backups.sort(key=lambda x: x['modified'], reverse=True)
            
            # Determine which backups to keep
            now = datetime.datetime.now()
            to_keep = []
            to_delete = []
            
            # First, keep the specified number of recent backups
            recent_backups = backups[:args.keep_count]
            older_backups = backups[args.keep_count:]
            
            # For older backups, only keep those newer than keep_days
            cutoff_date = now - datetime.timedelta(days=args.keep_days)
            
            for backup in recent_backups:
                to_keep.append(backup)
                
            for backup in older_backups:
                if backup['modified'] >= cutoff_date:
                    to_keep.append(backup)
                else:
                    to_delete.append(backup)
            
            # Report what would be deleted
            if not to_delete:
                print(f"\nNo backups to clean up. Would keep all {len(backups)} backups.")
            else:
                print(f"\nWould delete {len(to_delete)} backup(s):")
                for backup in to_delete:
                    age = now - backup['modified']
                    print(f"  - {backup['name']} ({age.days} days old)")
                    
                print(f"\nWould keep {len(to_keep)} backup(s):")
                for backup in to_keep:
                    age = now - backup['modified']
                    print(f"  - {backup['name']} ({age.days} days old)")
                    
        except Exception as e:
            print(f"Error during dry run: {e}")
            sys.exit(1)
    else:
        # Actually perform cleanup
        if cleanup_backups(args.backup_dir, args.keep_days, args.keep_count):
            print("Backup cleanup completed successfully!")
        else:
            print("Backup cleanup failed!")
            sys.exit(1)

if __name__ == '__main__':
    main()
