#!/usr/bin/env python3
"""
Data import script for AI Information Gathering Agent
"""

import os
import sys
import json
import csv
import django
from django.core.serializers import deserialize
from django.core.management import execute_from_command_line

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ai_agent.ai_agent_project.settings')

def import_from_json(input_file):
    """Import data from JSON file."""
    print(f"Importing data from {input_file}...")
    try:
        # Setup Django
        django.setup()
        
        # Check if file exists
        if not os.path.exists(input_file):
            print(f"✗ File not found: {input_file}")
            return False
        
        # Read JSON data
        with open(input_file, 'r', encoding='utf-8') as f:
            data = f.read()
        
        # Deserialize and save data
        objects = deserialize('json', data)
        count = 0
        for obj in objects:
            obj.save()
            count += 1
        
        print(f"✓ Imported {count} objects from {input_file}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to import data from JSON: {e}")
        return False

def import_from_csv(input_file, model_name):
    """Import data from CSV file."""
    print(f"Importing {model_name} data from {input_file}...")
    try:
        # Setup Django
        django.setup()
        
        # Check if file exists
        if not os.path.exists(input_file):
            print(f"✗ File not found: {input_file}")
            return False
        
        # Import appropriate model
        if model_name.lower() == 'keyword':
            from django_ai_agent.keywords_app.models import Keyword
            model_class = Keyword
            field_mapping = {'name': 1}  # Column index for name field
        elif model_name.lower() == 'report':
            from django_ai_agent.reports_app.models import Report
            model_class = Report
            field_mapping = {'title': 1, 'content': 2}  # Column indices
        elif model_name.lower() == 'configuration':
            from django_ai_agent.config_app.models import Configuration
            model_class = Configuration
            field_mapping = {'key': 1, 'value': 2}  # Column indices
        else:
            print(f"✗ Unsupported model: {model_name}")
            return False
        
        # Read CSV data
        created_count = 0
        with open(input_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)  # Skip header row
            
            for row in reader:
                # Create object based on model
                if model_name.lower() == 'keyword':
                    obj = model_class(name=row[field_mapping['name']])
                elif model_name.lower() == 'report':
                    obj = model_class(title=row[field_mapping['title']], content=row[field_mapping['content']])
                elif model_name.lower() == 'configuration':
                    obj = model_class(key=row[field_mapping['key']], value=row[field_mapping['value']])
                
                obj.save()
                created_count += 1
        
        print(f"✓ Imported {created_count} {model_name}(s) from {input_file}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to import {model_name} data from CSV: {e}")
        return False

def import_database(input_file):
    """Import entire database using Django's loaddata command."""
    print(f"Importing database from {input_file}...")
    try:
        # Setup Django
        django.setup()
        
        # Check if file exists
        if not os.path.exists(input_file):
            print(f"✗ File not found: {input_file}")
            return False
        
        # Import using loaddata
        execute_from_command_line(['manage.py', 'loaddata', input_file])
        
        print(f"✓ Database imported from {input_file}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to import database: {e}")
        return False

def main():
    """Main function to handle data import operations."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Data import utility for AI Information Gathering Agent')
    parser.add_argument('input_file', help='Input file to import data from')
    parser.add_argument('--format', choices=['json', 'csv', 'database'], default='json',
                       help='Import format (default: json)')
    parser.add_argument('--model', help='Model name for CSV import (keyword, report, configuration)')
    
    args = parser.parse_args()
    
    print("AI Information Gathering Agent - Data Import")
    print("=" * 45)
    
    # Import data based on arguments
    success = True
    
    if args.format == 'json':
        success = import_from_json(args.input_file)
    elif args.format == 'csv':
        if not args.model:
            print("✗ Model name is required for CSV import")
            print("  Use --model with keyword, report, or configuration")
            sys.exit(1)
        success = import_from_csv(args.input_file, args.model)
    elif args.format == 'database':
        success = import_database(args.input_file)
    
    print("\n" + "=" * 45)
    if success:
        print("✓ Data import completed successfully!")
    else:
        print("✗ Data import failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()
