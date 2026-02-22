#!/usr/bin/env python3
"""
Data export script for AI Information Gathering Agent
"""

import os
import sys
import json
import csv
import django
from django.core.serializers import serialize
from django.core.management import execute_from_command_line

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ai_agent.ai_agent_project.settings')

def export_to_json(output_dir='exports'):
    """Export all data to JSON format."""
    print("Exporting data to JSON format...")
    try:
        # Setup Django
        django.setup()
        
        # Import models
        from django_ai_agent.keywords_app.models import Keyword
        from django_ai_agent.reports_app.models import Report
        from django_ai_agent.config_app.models import Configuration
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Export Keywords
        keywords = Keyword.objects.all()
        keywords_data = serialize('json', keywords)
        with open(os.path.join(output_dir, 'keywords.json'), 'w', encoding='utf-8') as f:
            f.write(keywords_data)
        print(f"✓ Exported {keywords.count()} keywords to keywords.json")
        
        # Export Reports
        reports = Report.objects.all()
        reports_data = serialize('json', reports)
        with open(os.path.join(output_dir, 'reports.json'), 'w', encoding='utf-8') as f:
            f.write(reports_data)
        print(f"✓ Exported {reports.count()} reports to reports.json")
        
        # Export Configurations
        configs = Configuration.objects.all()
        configs_data = serialize('json', configs)
        with open(os.path.join(output_dir, 'configurations.json'), 'w', encoding='utf-8') as f:
            f.write(configs_data)
        print(f"✓ Exported {configs.count()} configurations to configurations.json")
        
        print("✓ JSON export completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Failed to export data to JSON: {e}")
        return False

def export_to_csv(output_dir='exports'):
    """Export all data to CSV format."""
    print("Exporting data to CSV format...")
    try:
        # Setup Django
        django.setup()
        
        # Import models
        from django_ai_agent.keywords_app.models import Keyword
        from django_ai_agent.reports_app.models import Report
        from django_ai_agent.config_app.models import Configuration
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Export Keywords
        keywords = Keyword.objects.all()
        with open(os.path.join(output_dir, 'keywords.csv'), 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Name', 'Created At', 'Updated At'])  # Header
            for keyword in keywords:
                writer.writerow([keyword.id, keyword.name, keyword.created_at, keyword.updated_at])
        print(f"✓ Exported {keywords.count()} keywords to keywords.csv")
        
        # Export Reports
        reports = Report.objects.all()
        with open(os.path.join(output_dir, 'reports.csv'), 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Title', 'Content', 'Created At', 'Updated At'])  # Header
            for report in reports:
                writer.writerow([report.id, report.title, report.content, report.created_at, report.updated_at])
        print(f"✓ Exported {reports.count()} reports to reports.csv")
        
        # Export Configurations
        configs = Configuration.objects.all()
        with open(os.path.join(output_dir, 'configurations.csv'), 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Key', 'Value', 'Created At', 'Updated At'])  # Header
            for config in configs:
                writer.writerow([config.id, config.key, config.value, config.created_at, config.updated_at])
        print(f"✓ Exported {configs.count()} configurations to configurations.csv")
        
        print("✓ CSV export completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Failed to export data to CSV: {e}")
        return False

def export_database(output_dir='exports'):
    """Export entire database using Django's dumpdata command."""
    print("Exporting entire database...")
    try:
        # Setup Django
        django.setup()
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Export using dumpdata
        from django.core.management import execute_from_command_line
        import io
        from contextlib import redirect_stdout
        
        # Capture output
        stdout_capture = io.StringIO()
        with redirect_stdout(stdout_capture):
            execute_from_command_line(['manage.py', 'dumpdata', '--format=json'])
        
        db_data = stdout_capture.getvalue()
        
        # Write to file
        db_export_path = os.path.join(output_dir, 'database_dump.json')
        with open(db_export_path, 'w', encoding='utf-8') as f:
            f.write(db_data)
        
        print(f"✓ Database exported to {db_export_path}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to export database: {e}")
        return False

def main():
    """Main function to handle data export operations."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Data export utility for AI Information Gathering Agent')
    parser.add_argument('--format', choices=['json', 'csv', 'database'], default='json',
                       help='Export format (default: json)')
    parser.add_argument('--output-dir', default='exports', help='Output directory for exported files')
    parser.add_argument('--all', '-a', action='store_true', help='Export in all formats')
    
    args = parser.parse_args()
    
    print("AI Information Gathering Agent - Data Export")
    print("=" * 45)
    
    # Create exports directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Export data based on arguments
    success = True
    
    if args.all:
        # Export in all formats
        if not export_to_json(args.output_dir):
            success = False
        if not export_to_csv(args.output_dir):
            success = False
        if not export_database(args.output_dir):
            success = False
    else:
        # Export in specified format
        if args.format == 'json':
            success = export_to_json(args.output_dir)
        elif args.format == 'csv':
            success = export_to_csv(args.output_dir)
        elif args.format == 'database':
            success = export_database(args.output_dir)
    
    print("\n" + "=" * 45)
    if success:
        print("✓ Data export completed successfully!")
        print(f"Exported files are available in '{args.output_dir}' directory.")
    else:
        print("✗ Data export failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()
