#!/usr/bin/env python3
"""
Data export script for the AI Information Gathering Agent
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

def export_keywords(format='json'):
    """Export keywords data"""
    from keywords_app.models import Keyword
    
    print(f"Exporting keywords data in {format} format...")
    
    # Get all keywords
    keywords = Keyword.objects.all()
    
    if format == 'json':
        # Export as JSON
        data = []
        for keyword in keywords:
            data.append({
                'id': keyword.id,
                'name': keyword.name,
                'category': keyword.category,
                'created_at': keyword.created_at.isoformat() if keyword.created_at else None,
                'updated_at': keyword.updated_at.isoformat() if keyword.updated_at else None
            })
        
        with open('export_keywords.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print("Keywords exported to export_keywords.json")
    
    elif format == 'csv':
        # Export as CSV
        with open('export_keywords.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Name', 'Category', 'Created At', 'Updated At'])
            
            for keyword in keywords:
                writer.writerow([
                    keyword.id,
                    keyword.name,
                    keyword.category,
                    keyword.created_at.isoformat() if keyword.created_at else '',
                    keyword.updated_at.isoformat() if keyword.updated_at else ''
                ])
        
        print("Keywords exported to export_keywords.csv")

def export_config(format='json'):
    """Export configuration data"""
    from config_app.models import Configuration
    
    print(f"Exporting configuration data in {format} format...")
    
    # Get all configurations
    configs = Configuration.objects.all()
    
    if format == 'json':
        # Export as JSON
        data = []
        for config in configs:
            data.append({
                'id': config.id,
                'key': config.key,
                'value': config.value,
                'description': config.description,
                'created_at': config.created_at.isoformat() if config.created_at else None,
                'updated_at': config.updated_at.isoformat() if config.updated_at else None
            })
        
        with open('export_config.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print("Configuration exported to export_config.json")
    
    elif format == 'csv':
        # Export as CSV
        with open('export_config.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Key', 'Value', 'Description', 'Created At', 'Updated At'])
            
            for config in configs:
                writer.writerow([
                    config.id,
                    config.key,
                    config.value,
                    config.description,
                    config.created_at.isoformat() if config.created_at else '',
                    config.updated_at.isoformat() if config.updated_at else ''
                ])
        
        print("Configuration exported to export_config.csv")

def export_reports(format='json'):
    """Export reports data"""
    from reports_app.models import Report
    
    print(f"Exporting reports data in {format} format...")
    
    # Get all reports
    reports = Report.objects.all()
    
    if format == 'json':
        # Export as JSON
        data = []
        for report in reports:
            data.append({
                'id': report.id,
                'title': report.title,
                'content': report.content,
                'format': report.format,
                'created_at': report.created_at.isoformat() if report.created_at else None,
                'updated_at': report.updated_at.isoformat() if report.updated_at else None
            })
        
        with open('export_reports.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print("Reports exported to export_reports.json")
    
    elif format == 'csv':
        # Export as CSV
        with open('export_reports.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Title', 'Content', 'Format', 'Created At', 'Updated At'])
            
            for report in reports:
                writer.writerow([
                    report.id,
                    report.title,
                    report.content[:100] + '...' if len(report.content) > 100 else report.content,
                    report.format,
                    report.created_at.isoformat() if report.created_at else '',
                    report.updated_at.isoformat() if report.updated_at else ''
                ])
        
        print("Reports exported to export_reports.csv")

def main():
    """Main function"""
    print("Exporting data...")
    
    # Check if format argument is provided
    format = 'json'
    if len(sys.argv) > 1:
        format = sys.argv[1].lower()
        if format not in ['json', 'csv']:
            print("Invalid format. Using JSON format.")
            format = 'json'
    
    # Export data
    export_keywords(format)
    export_config(format)
    export_reports(format)
    
    print("Data export completed!")

if __name__ == "__main__":
    main()
