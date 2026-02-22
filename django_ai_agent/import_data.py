#!/usr/bin/env python3
"""
Data import script for the AI Information Gathering Agent
"""
import os
import sys
import json
import csv
import django

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_agent_project.settings')

# Initialize Django
django.setup()

def import_keywords(file_path, format='json'):
    """Import keywords data"""
    from keywords_app.models import Keyword
    
    print(f"Importing keywords data from {file_path} in {format} format...")
    
    if format == 'json':
        # Import from JSON
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        imported_count = 0
        for item in data:
            # Check if keyword already exists
            if not Keyword.objects.filter(name=item['name']).exists():
                Keyword.objects.create(
                    name=item['name'],
                    category=item.get('category', ''),
                    created_at=item.get('created_at'),
                    updated_at=item.get('updated_at')
                )
                imported_count += 1
        
        print(f"Imported {imported_count} new keywords from {file_path}")
    
    elif format == 'csv':
        # Import from CSV
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            imported_count = 0
            for row in reader:
                # Check if keyword already exists
                if not Keyword.objects.filter(name=row['Name']).exists():
                    Keyword.objects.create(
                        name=row['Name'],
                        category=row.get('Category', ''),
                        created_at=row.get('Created At'),
                        updated_at=row.get('Updated At')
                    )
                    imported_count += 1
        
        print(f"Imported {imported_count} new keywords from {file_path}")

def import_config(file_path, format='json'):
    """Import configuration data"""
    from config_app.models import Configuration
    
    print(f"Importing configuration data from {file_path} in {format} format...")
    
    if format == 'json':
        # Import from JSON
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        imported_count = 0
        for item in data:
            # Check if configuration already exists
            if not Configuration.objects.filter(key=item['key']).exists():
                Configuration.objects.create(
                    key=item['key'],
                    value=item['value'],
                    description=item.get('description', ''),
                    created_at=item.get('created_at'),
                    updated_at=item.get('updated_at')
                )
                imported_count += 1
        
        print(f"Imported {imported_count} new configuration items from {file_path}")
    
    elif format == 'csv':
        # Import from CSV
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            imported_count = 0
            for row in reader:
                # Check if configuration already exists
                if not Configuration.objects.filter(key=row['Key']).exists():
                    Configuration.objects.create(
                        key=row['Key'],
                        value=row['Value'],
                        description=row.get('Description', ''),
                        created_at=row.get('Created At'),
                        updated_at=row.get('Updated At')
                    )
                    imported_count += 1
        
        print(f"Imported {imported_count} new configuration items from {file_path}")

def main():
    """Main function"""
    if len(sys.argv) < 3:
        print("Usage: python import_data.py <file_path> <data_type> [format]")
        print("  file_path: Path to the data file to import")
        print("  data_type: Type of data to import (keywords, config)")
        print("  format: Format of the data file (json, csv) - default: json")
        return
    
    file_path = sys.argv[1]
    data_type = sys.argv[2].lower()
    format = 'json'
    
    if len(sys.argv) > 3:
        format = sys.argv[3].lower()
        if format not in ['json', 'csv']:
            print("Invalid format. Using JSON format.")
            format = 'json'
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"File {file_path} not found!")
        return
    
    # Import data
    if data_type == 'keywords':
        import_keywords(file_path, format)
    elif data_type == 'config':
        import_config(file_path, format)
    else:
        print("Invalid data type. Supported types: keywords, config")

if __name__ == "__main__":
    main()
