#!/usr/bin/env python3
"""
Documentation generation script for the AI Information Gathering Agent
"""
import os
import sys
import django

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_agent_project.settings')

# Initialize Django
django.setup()

def generate_api_docs():
    """Generate API documentation"""
    print("Generating API documentation...")
    
    # Create documentation directory if it doesn't exist
    os.makedirs('docs', exist_ok=True)
    
    # Generate API documentation
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'drf_yasg', 'generate'])
        print("API documentation generated successfully!")
    except Exception as e:
        print(f"Error generating API documentation: {e}")
        print("Falling back to manual documentation generation...")
        generate_manual_docs()

def generate_manual_docs():
    """Generate manual documentation"""
    # Create a simple API documentation
    api_docs = """
# AI Information Gathering Agent API Documentation

## Overview

The AI Information Gathering Agent provides a RESTful API for accessing all features programmatically.

## Authentication

All API endpoints require authentication via API keys or session authentication.

## Endpoints

### Configuration Management

- `GET /api/config/` - Get current configuration
- `POST /api/config/` - Update configuration
- `DELETE /api/config/` - Reset configuration to defaults

### Keyword Management

- `GET /api/keywords/` - List all keywords
- `POST /api/keywords/` - Add new keywords
- `PUT /api/keywords/{id}/` - Update a keyword
- `DELETE /api/keywords/{id}/` - Delete a keyword

### Scanning

- `POST /api/scan/` - Start a new scan
- `GET /api/scan/{id}/` - Get scan status
- `GET /api/scan/{id}/results/` - Get scan results

### Reporting

- `GET /api/reports/` - List all reports
- `POST /api/reports/` - Generate a new report
- `GET /api/reports/{id}/` - Get report details
- `GET /api/reports/{id}/download/` - Download report

### Chat Interface

- `POST /api/chat/` - Send a message to the AI chat
- `GET /api/chat/history/` - Get chat history

## Request/Response Formats

All API requests and responses use JSON format.

### Example Request

```json
{
  "target": "example.com",
  "modules": ["whois", "domain", "port"]
}
```

### Example Response

```json
{
  "status": "success",
  "scan_id": "12345",
  "message": "Scan started successfully"
}
```

## Error Handling

All API errors follow standard HTTP status codes:

- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

### Error Response Format

```json
{
  "status": "error",
  "message": "Description of the error"
}
```
"""
    
    # Write API documentation to file
    with open('docs/api.md', 'w') as f:
        f.write(api_docs)
    
    print("Manual API documentation generated at docs/api.md")

def generate_user_guide():
    """Generate user guide"""
    user_guide = """
# AI Information Gathering Agent User Guide

## Installation

1. Clone the repository
2. Create a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Configure settings in `config.yaml`
5. Run database migrations: `python manage.py migrate`
6. Start the server: `python manage.py runserver`

## Configuration

Edit `config.yaml` to configure API keys and settings:

```yaml
platforms:
  github:
    api_key: "your_github_token"
    
ai_models:
  openai:
    api_key: "your_openai_key"
    model: "gpt-4"
```

## Web Interface

Access the web interface at `http://localhost:8000`:

1. Dashboard - Overview of system status
2. Scans - Configure and run information gathering scans
3. Results - View scan results
4. Reports - Generate and download reports
5. Configuration - Manage system settings
6. Chat - Interact with the AI assistant

## Command Line Interface

Use the CLI for automated tasks:

```bash
# Run a scan
python cli.py --target example.com --modules whois,domain,port

# Search for keywords
python cli.py --keywords "John Doe" --platforms github,linkedin

# Generate a report
python cli.py --report --format docx --output report.docx
```

## API Usage

Use the RESTful API for programmatic access:

```python
import requests

# Start a scan
response = requests.post('http://localhost:8000/api/scan/', json={
    'target': 'example.com',
    'modules': ['whois', 'domain']
})

# Get results
scan_id = response.json()['scan_id']
results = requests.get(f'http://localhost:8000/api/scan/{scan_id}/results/')
```

## Best Practices

1. Always obtain proper authorization before scanning any systems
2. Store API keys securely
3. Regularly update the tool to the latest version
4. Review and validate all findings before taking action
5. Comply with all applicable laws and regulations
"""
    
    # Write user guide to file
    with open('docs/user_guide.md', 'w') as f:
        f.write(user_guide)
    
    print("User guide generated at docs/user_guide.md")

def main():
    """Main function"""
    print("Generating documentation...")
    
    # Generate API documentation
    generate_api_docs()
    
    # Generate user guide
    generate_user_guide()
    
    print("Documentation generation complete!")

if __name__ == "__main__":
    main()
