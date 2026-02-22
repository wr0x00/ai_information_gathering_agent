#!/usr/bin/env python3
"""
Script to list database backups for AI Information Gathering Agent
"""

import os
import sys
import datetime
from backup_db import list_backups, BACKUP_DIR

def format_size(size_bytes):
    """Format file size in human readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

def main():
    """List all available database backups."""
    import argparse
    
    parser = argparse.ArgumentParser(description='List database backups for AI Information Gathering Agent')
    parser.add_argument('--backup-dir', default=BACKUP_DIR, help='Directory where backups are stored')
    parser.add_argument('--sort', choices=['name', 'size', 'date'], default='date', 
                       help='Sort backups by name, size, or date (default: date)')
    parser.add_argument('--reverse', '-r', action='store_true', help='Reverse sort order')
    
    args = parser.parse_args()
    
    try:
        # List all backups
        backups = list_backups(args.backup_dir)
        
        if not backups:
            print("No backups found.")
            return
            
        # Sort backups
        if args.sort == 'name':
            backups.sort(key=lambda x: x['name'], reverse=args.reverse)
        elif args.sort == 'size':
            backups.sort(key=lambda x: x['size'], reverse=args.reverse)
        else:  # date
            backups.sort(key=lambda x: x['modified'], reverse=not args.reverse)
        
        # Display backups
        print(f"\nDatabase backups in '{args.backup_dir}':")
        print("=" * 90)
        print(f"{'Name':<40} {'Size':<15} {'Modified':<25} {'Age'}")
        print("=" * 90)
        
        now = datetime.datetime.now()
        for backup in backups:
            # Calculate age
            age = now - backup['modified']
            if age.days > 0:
                age_str = f"{age.days}d"
            elif age.seconds > 3600:
                age_str = f"{age.seconds // 3600}h"
            elif age.seconds > 60:
                age_str = f"{age.seconds // 60}m"
            else:
                age_str = f"{age.seconds}s"
            
            size_str = format_size(backup['size'])
            date_str = backup['modified'].strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"{backup['name']:<40} {size_str:<15} {date_str:<25} {age_str}")
        
        print("=" * 90)
        print(f"Total: {len(backups)} backup(s)")
        
        # Show oldest and newest
        if backups:
            oldest = backups[-1]
            newest = backups[0]
            print(f"Oldest: {oldest['name']} ({oldest['modified'].strftime('%Y-%m-%d %H:%M:%S')})")
            print(f"Newest: {newest['name']} ({newest['modified'].strftime('%Y-%m-%d %H:%M:%S')})")
            
    except Exception as e:
        print(f"Error listing backups: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
