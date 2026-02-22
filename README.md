# AI Information Gathering Agent

An intelligent system for automated information collection and analysis with a Django backend and React frontend.

## Features

- **Multi-source Information Gathering**: Collect data from WHOIS, DNS, Port scanning, GitHub, and more
- **Keyword-based Monitoring**: Track specific entities across multiple platforms
- **AI-Powered Analysis**: Utilize OpenAI and Anthropic models for intelligent processing
- **Comprehensive Reporting**: Generate detailed reports in multiple formats
- **Web-based Interface**: Modern React UI with multi-language support
- **Containerized Deployment**: Docker and Docker Compose for easy deployment

## Architecture

```
ai_information_gathering_agent/
├── django_ai_agent/              # Django backend
│   ├── ai_agent_project/         # Django project settings
│   ├── config_app/               # Configuration management
│   ├── frontend_app/             # Frontend integration
│   ├── keywords_app/             # Keyword management
│   ├── reports_app/              # Report generation
│   └── chat_app/                 # AI chat interface
├── modules/                      # Information gathering modules
│   ├── whois_module.py           # WHOIS lookup
│   ├── domain_module.py          # Domain information
│   ├── port_module.py            # Port scanning
│   ├── sensitive_info_module.py  # Sensitive information detection
│   └── github_module.py          # GitHub search
├── agent.py                      # Core agent logic
├── storage.py                    # Data persistence
├── cli.py                        # Command-line interface
└── config.py                     # Configuration management
```

## Prerequisites

- Python 3.11+
- Node.js 16+
- Docker and Docker Compose (for containerized deployment)
- PostgreSQL (when not using Docker)

## Installation

### Option 1: Using Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd ai_information_gathering_agent

# Build and start services
docker-compose up --build
```

The application will be available at http://localhost:8000

### Option 2: Manual Installation

```bash
# Clone the repository
git clone <repository-url>
cd ai_information_gathering_agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install

# Build frontend
npm run build

# Initialize database
python django_ai_agent/manage.py migrate

# Create superuser (optional)
python django_ai_agent/manage.py createsuperuser

# Start development server
python django_ai_agent/manage.py runserver
```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/database_name

# API Keys
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GITHUB_TOKEN=your_github_token

# Django
SECRET_KEY=your_django_secret_key
DEBUG=True
```

## Usage

### Web Interface

Access the web interface at http://localhost:8000 after starting the server.

### Command Line Interface

```bash
# Run information gathering agent
python main.py --target example.com --modules whois,domain,port

# Add keywords for monitoring
python main.py --add-keyword "Company Name" --description "Target company"

# Generate reports
python main.py --generate-report --format pdf
```

## Modules

- **WHOIS Module**: Retrieves domain registration information
- **Domain Module**: Gathers DNS records and domain details
- **Port Module**: Performs port scanning on target systems
- **Sensitive Information Module**: Searches for exposed sensitive data
- **GitHub Module**: Searches GitHub for relevant repositories and code

## Development

### Backend Development

```bash
# Run tests
python django_ai_agent/manage.py test

# Create new migrations
python django_ai_agent/manage.py makemigrations

# Apply migrations
python django_ai_agent/manage.py migrate
```

### Frontend Development

```bash
# Start development server with hot reloading
npm run dev

# Build production bundle
npm run build
```

## API Endpoints

- `/api/config/` - Configuration management
- `/api/keywords/` - Keyword operations
- `/api/reports/` - Report generation
- `/api/chat/` - AI chat interface
- `/api/scans/` - Scan operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Django and Django REST Framework
- Frontend powered by React
- AI capabilities provided by OpenAI and Anthropic
- Containerization with Docker
