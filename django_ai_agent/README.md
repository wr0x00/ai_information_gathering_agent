# AI Information Gathering Agent

An advanced AI-powered information gathering tool designed for cybersecurity professionals and researchers. This agent can collect information from various sources including WHOIS, domain records, port scanning, sensitive information discovery, and GitHub repositories.

## Features

- **Multi-source Information Gathering**: Collects data from multiple sources including:
  - WHOIS lookup
  - Domain information
  - Port scanning
  - Sensitive information discovery
  - GitHub repository search
  
- **Keyword-based Analysis**: Searches for specific keywords and personal information across platforms

- **AI-powered Processing**: Uses advanced AI models to analyze and correlate collected information

- **Report Generation**: Creates comprehensive reports in multiple formats (DOCX, PDF)

- **Web Interface**: User-friendly Django-based web interface for managing scans and viewing results

- **RESTful API**: Programmatic access to all features via REST API

## Architecture

The agent follows a modular architecture with the following components:

### Core Components

1. **Agent Framework** (`agent.py`)
   - Main orchestrator for all scanning operations
   - Manages concurrent execution of modules
   - Handles configuration and storage integration

2. **HTTP Client** (`http_client.py`)
   - Asynchronous HTTP client using httpx
   - Rate limiting and retry mechanisms
   - Proxy support for anonymous scanning

3. **Storage Layer** (`storage.py`)
   - SQLite database for storing results
   - Configuration management
   - Report storage

4. **Configuration Manager** (`config.py`)
   - YAML-based configuration
   - Platform-specific settings
   - API key management

### Information Gathering Modules

1. **WHOIS Module** (`modules/whois_module.py`)
   - Domain registration information
   - Contact details extraction

2. **Domain Module** (`modules/domain_module.py`)
   - DNS record lookup
   - Subdomain enumeration
   - Domain history analysis

3. **Port Scanner** (`modules/port_module.py`)
   - TCP/UDP port scanning
   - Service detection
   - Banner grabbing

4. **Sensitive Information Finder** (`modules/sensitive_info_module.py`)
   - File and directory discovery
   - Credential leakage detection
   - Configuration file analysis

5. **GitHub Search** (`modules/github_module.py`)
   - Repository code search
   - Commit history analysis
   - Issue and pull request mining

### Web Interface

1. **Frontend App** (`frontend_app/`)
   - Dashboard with statistics
   - Scan management interface
   - Results visualization

2. **API App** (`api_app/`)
   - RESTful endpoints for all features
   - Authentication and authorization
   - Rate limiting

3. **Reports App** (`reports_app/`)
   - Report generation in multiple formats
   - Template-based reporting
   - Export functionality

4. **Configuration App** (`config_app/`)
   - Platform configuration management
   - API key management
   - Settings interface

5. **Keywords App** (`keywords_app/`)
   - Keyword management
   - Search configuration
   - Tracking interface

6. **Chat App** (`chat_app/`)
   - AI-powered chat interface
   - Natural language query processing
   - Command execution

## Installation

### Prerequisites

- Python 3.8+
- Django 6.0+
- Node.js (for frontend development)
- SQLite (default database)

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai_information_gathering_agent
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

### Command Line Interface

```bash
# Basic scan
python cli.py --target example.com --modules whois,domain,port

# Keyword search
python cli.py --keywords "John Doe,Acme Corp" --platforms github,linkedin

# Generate report
python cli.py --report --format docx --output report.docx
```

### Web Interface

1. Navigate to `http://localhost:8000` in your browser
2. Use the dashboard to configure scans
3. View results in real-time
4. Generate and download reports

### API Endpoints

- `POST /api/scan/` - Start a new scan
- `GET /api/results/{scan_id}/` - Get scan results
- `POST /api/keywords/` - Manage keywords
- `GET /api/reports/{report_id}/` - Get generated reports

## Configuration

Create a `config.yaml` file in the project root:

```yaml
platforms:
  github:
    api_key: "your_github_token"
    rate_limit: 30
  linkedin:
    api_key: "your_linkedin_key"
    
ai_models:
  openai:
    api_key: "your_openai_key"
    model: "gpt-4"
  anthropic:
    api_key: "your_anthropic_key"
    model: "claude-3"

scan_settings:
  timeout: 30
  retries: 3
  concurrency: 10
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is intended for ethical security research and authorized penetration testing only. Users are responsible for complying with all applicable laws and regulations. Unauthorized scanning of systems you do not own or have explicit permission to test is illegal.
