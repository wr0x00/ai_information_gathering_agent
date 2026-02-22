#!/usr/bin/env python3
"""
Documentation generation script for AI Information Gathering Agent
"""

import os
import sys
import subprocess
import django
from django.core.management import execute_from_command_line

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ai_agent.ai_agent_project.settings')

def generate_api_docs():
    """Generate API documentation."""
    print("Generating API documentation...")
    try:
        # Setup Django
        django.setup()
        
        # Create docs directory if it doesn't exist
        docs_dir = os.path.join('docs', 'api')
        os.makedirs(docs_dir, exist_ok=True)
        
        # Generate API documentation using Django's inspectdb
        from django.core.management import execute_from_command_line
        import io
        from contextlib import redirect_stdout
        
        # Capture model information
        stdout_capture = io.StringIO()
        with redirect_stdout(stdout_capture):
            execute_from_command_line(['manage.py', 'inspectdb'])
        
        models_info = stdout_capture.getvalue()
        
        # Write to file
        api_doc_path = os.path.join(docs_dir, 'models.md')
        with open(api_doc_path, 'w', encoding='utf-8') as f:
            f.write("# API Models Documentation\n\n")
            f.write("## Database Schema\n\n")
            f.write("```\n")
            f.write(models_info)
            f.write("```\n")
        
        print(f"✓ API documentation generated at {api_doc_path}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to generate API documentation: {e}")
        return False

def generate_code_docs():
    """Generate code documentation."""
    print("Generating code documentation...")
    try:
        # Try to use sphinx to generate documentation
        docs_dir = 'docs'
        os.makedirs(docs_dir, exist_ok=True)
        
        # Create a basic conf.py if it doesn't exist
        conf_path = os.path.join(docs_dir, 'conf.py')
        if not os.path.exists(conf_path):
            with open(conf_path, 'w', encoding='utf-8') as f:
                f.write('''\
# Configuration file for the Sphinx documentation builder.

project = 'AI Information Gathering Agent'
copyright = '2026, AI Agent Team'
author = 'AI Agent Team'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']
''')
        
        # Create a basic index.rst if it doesn't exist
        index_path = os.path.join(docs_dir, 'index.rst')
        if not os.path.exists(index_path):
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write('''\
AI Information Gathering Agent Documentation
==========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api/models
   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
''')
        
        print("✓ Basic documentation structure created")
        print("⚠ Note: For full code documentation, install Sphinx and run 'sphinx-apidoc'")
        return True
        
    except Exception as e:
        print(f"✗ Failed to generate code documentation: {e}")
        return False

def generate_module_docs():
    """Generate documentation for modules."""
    print("Generating module documentation...")
    try:
        modules_dir = os.path.join('docs', 'modules')
        os.makedirs(modules_dir, exist_ok=True)
        
        # List of modules to document
        modules = [
            'agent.py',
            'storage.py',
            'cli.py',
            'config.py',
            'http_client.py',
            'base_module.py',
            os.path.join('modules', 'whois_module.py'),
            os.path.join('modules', 'domain_module.py'),
            os.path.join('modules', 'port_module.py'),
            os.path.join('modules', 'sensitive_info_module.py'),
            os.path.join('modules', 'github_module.py')
        ]
        
        module_doc_path = os.path.join(modules_dir, 'index.md')
        with open(module_doc_path, 'w', encoding='utf-8') as f:
            f.write("# Modules Documentation\n\n")
            f.write("## Overview\n\n")
            f.write("This section documents the core modules of the AI Information Gathering Agent.\n\n")
            f.write("## Module Index\n\n")
            
            for module in modules:
                if os.path.exists(module):
                    module_name = os.path.splitext(os.path.basename(module))[0]
                    f.write(f"- [{module_name}]({module_name}.md)\n")
                    
                    # Create individual module documentation
                    individual_doc_path = os.path.join(modules_dir, f'{module_name}.md')
                    with open(individual_doc_path, 'w', encoding='utf-8') as mf:
                        mf.write(f"# {module_name}\n\n")
                        mf.write(f"Documentation for {module}.\n\n")
                        mf.write("## Description\n\n")
                        mf.write(f"This module handles {module_name.replace('_', ' ')} functionality.\n\n")
                        
                        # Try to extract docstrings or comments
                        try:
                            with open(module, 'r', encoding='utf-8') as mod_file:
                                content = mod_file.read()
                                # Simple extraction of comments/docstrings
                                lines = content.split('\n')
                                for line in lines[:20]:  # Check first 20 lines
                                    if line.strip().startswith('#') or '"""' in line:
                                        mf.write(f"{line.strip()}\n")
                        except Exception:
                            pass
                        
                        mf.write("\n## Usage\n\n")
                        mf.write("Detailed usage instructions would go here.\n\n")
        
        print(f"✓ Module documentation generated at {module_doc_path}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to generate module documentation: {e}")
        return False

def generate_readme_docs():
    """Generate or update README documentation."""
    print("Generating README documentation...")
    try:
        # Check if README exists
        if os.path.exists('README.md'):
            print("✓ README.md already exists")
            return True
        
        # Create a basic README
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write('''\
# AI Information Gathering Agent

An intelligent agent for automated information gathering and analysis.

## Features

- Multi-source information gathering
- AI-powered analysis
- Web-based dashboard
- RESTful API
- Command-line interface
- Real-time monitoring

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd ai-information-gathering-agent

# Install dependencies
make setup

# Initialize database
python init_db.py

# Start the application
make run
```

## Usage

### Web Interface

Access the web interface at `http://localhost:8000`

### Command Line

```bash
# Run the agent
python main.py

# Check health
python check_health.py

# Run tests
python run_tests.py
```

## Documentation

See the `docs/` directory for detailed documentation.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
''')
        
        print("✓ README.md created")
        return True
        
    except Exception as e:
        print(f"✗ Failed to generate README documentation: {e}")
        return False

def main():
    """Main function to generate all documentation."""
    print("AI Information Gathering Agent - Documentation Generator")
    print("=" * 55)
    
    # Create docs directory
    os.makedirs('docs', exist_ok=True)
    
    # Generate different types of documentation
    generators = [
        generate_readme_docs,
        generate_api_docs,
        generate_module_docs,
        generate_code_docs
    ]
    
    generated = 0
    total = len(generators)
    
    for generator in generators:
        try:
            if generator():
                generated += 1
            print()  # Add spacing between generators
        except Exception as e:
            print(f"✗ Documentation generation failed with exception: {e}\n")
    
    print("=" * 55)
    print(f"Documentation Generation Summary: {generated}/{total} generators succeeded")
    
    if generated == total:
        print("✓ All documentation generated successfully!")
        print("Documentation is available in the 'docs/' directory.")
        return 0
    else:
        print("⚠ Some documentation generation failed.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
