# Contributing to AI Information Gathering Agent

Thank you for your interest in contributing to the AI Information Gathering Agent! We welcome contributions from the community to help improve this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Process](#development-process)
- [Style Guides](#style-guides)
- [Testing](#testing)
- [Documentation](#documentation)
- [Reporting Issues](#reporting-issues)
- [Pull Requests](#pull-requests)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/ai-information-gathering-agent.git`
3. Create a new branch for your feature or bugfix: `git checkout -b feature/your-feature-name`
4. Install dependencies:
   ```bash
   make setup-dev
   ```
5. Make your changes
6. Test your changes
7. Commit and push your changes
8. Create a Pull Request

## How to Contribute

### Reporting Bugs

Before submitting a bug report, please check if the issue has already been reported. If not, create a new issue with:

- A clear and descriptive title
- A detailed description of the problem
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Your environment information (OS, Python version, etc.)

### Suggesting Enhancements

We welcome suggestions for new features or improvements. Please create an issue with:

- A clear and descriptive title
- A detailed explanation of the proposed enhancement
- The problem it solves or benefit it provides
- Any implementation ideas you might have

### Code Contributions

1. Look for issues labeled "good first issue" or "help wanted" if you're new to the project
2. Comment on the issue to let others know you're working on it
3. Follow the development process outlined below

## Development Process

### Setting Up the Development Environment

```bash
# Clone your fork
git clone https://github.com/your-username/ai-information-gathering-agent.git
cd ai-information-gathering-agent

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make setup-dev

# Build frontend
make build-frontend
```

### Branching Strategy

- Use descriptive branch names: `feature/new-feature`, `bugfix/issue-description`, `hotfix/critical-fix`
- Keep branches focused on a single issue or feature
- Regularly sync with the main branch: `git fetch upstream && git rebase upstream/main`

### Making Changes

1. Write clean, readable, and well-documented code
2. Follow the project's style guides
3. Add tests for new functionality
4. Update documentation as needed
5. Run tests to ensure nothing is broken

## Style Guides

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines
- Use 4 spaces for indentation
- Keep lines under 88 characters
- Use meaningful variable and function names
- Write docstrings for public functions and classes

### JavaScript/React Code Style

- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use functional components when possible
- Use hooks for state management
- Write clear prop types
- Keep components small and focused

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- Consider starting the commit message with an applicable emoji:
  - :art: `:art:` when improving the format/structure of the code
  - :racehorse: `:racehorse:` when improving performance
  - :non-potable_water: `:non-potable_water:` when plugging memory leaks
  - :memo: `:memo:` when writing docs
  - :penguin: `:penguin:` when fixing something on Linux
  - :apple: `:apple:` when fixing something on macOS
  - :checkered_flag: `:checkered_flag:` when fixing something on Windows
  - :bug: `:bug:` when fixing a bug
  - :fire: `:fire:` when removing code or files
  - :green_heart: `:green_heart:` when fixing the CI build
  - :white_check_mark: `:white_check_mark:` when adding tests
  - :lock: `:lock:` when dealing with security
  - :arrow_up: `:arrow_up:` when upgrading dependencies
  - :arrow_down: `:arrow_down:` when downgrading dependencies
  - :shirt: `:shirt:` when removing linter warnings

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run tests with coverage
make test-coverage
```

### Writing Tests

- Write unit tests for new functionality
- Use descriptive test names
- Test edge cases and error conditions
- Keep tests independent and fast
- Use fixtures for setup and teardown

## Documentation

- Update README.md if you change functionality
- Add docstrings to new functions and classes
- Update CHANGELOG.md for user-facing changes
- Keep documentation up-to-date with code changes

## Reporting Issues

When reporting issues, please include:

1. A clear description of the problem
2. Steps to reproduce
3. Expected vs. actual behavior
4. Environment information (OS, Python version, etc.)
5. Screenshots or logs if applicable

## Pull Requests

### Before Submitting

- Ensure all tests pass
- Update documentation if needed
- Follow the style guides
- Write clear, descriptive commit messages
- Squash related commits

### Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a build
2. Update the README.md with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations and container parameters
3. Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent
4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you

### Code Review Process

All submissions require review. We use GitHub pull requests for this process. Consult [GitHub Help](https://help.github.com/articles/about-pull-requests/) for more information on using pull requests.

## Community

- Join our discussions on GitHub Issues
- Be respectful and inclusive
- Help others who are contributing
- Share your experiences and knowledge

Thank you for contributing to the AI Information Gathering Agent!
