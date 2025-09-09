# Classroom Pilot

A comprehensive Python CLI tool for automating GitHub Classroom assignment management with modular workflow orchestration, repository operations, and secret management.

[![PyPI version](https://badge.fury.io/py/classroom-pilot.svg)](https://badge.fury.io/py/classroom-pilot)
[![Python Support](https://img.shields.io/pypi/pyversions/classroom-pilot.svg)](https://pypi.org/project/classroom-pilot/)
[![Tests](https://github.com/hugo-valle/classroom-pilot/workflows/Tests/badge.svg)](https://github.com/hugo-valle/classroom-pilot/actions)

## 🎯 Overview

Classroom Pilot provides instructors with a powerful, modern CLI to automate GitHub Classroom workflows:

- **🐍 Modern Python CLI** - Type-safe, intuitive commands with rich help and output
- **📦 PyPI Package** - Simple installation: `pip install classroom-pilot`
- **🔧 Modular Architecture** - Organized command structure for different workflow areas
- **🔍 Smart Repository Discovery** - Automated filtering and batch operations
- **🔐 Secret Management** - Secure distribution of tokens and credentials
- **⚙️ Configuration-Driven** - Flexible, reusable assignment setups
- **🛡️ Enterprise Support** - Custom GitHub hosts and internal Git systems
- **🎯 Instructor-Focused** - Excludes instructor repos from batch operations automatically

## 📦 Installation

### Quick Install (Recommended)

```bash
# Install from PyPI
pip install classroom-pilot

# Verify installation
classroom-pilot --help
```

### Development Installation

```bash
# Clone repository
git clone https://github.com/hugo-valle/classroom-pilot.git
cd classroom-pilot

# Install with Poetry
poetry install
poetry shell

# Or install in development mode
pip install -e .
```

### Requirements

- **Python 3.10+** (3.11+ recommended)
- **Git** for repository operations
- **GitHub CLI** (optional, for enhanced authentication)

## 🚀 Quick Start

### 1. Basic Configuration

Create an assignment configuration file:

```bash
# Create assignment.conf
cat > assignment.conf << 'EOF'
# GitHub Classroom Configuration
CLASSROOM_URL="https://classroom.github.com/classrooms/123/assignments/456"
TEMPLATE_REPO_URL="https://github.com/instructor/assignment-template"
ASSIGNMENT_FILE="homework.py"

# Authentication
GITHUB_TOKEN_FILE="github_token.txt"

# Optional: Secrets to distribute
SECRETS_LIST="API_KEY,DATABASE_URL"
EOF
```

### 2. Command Structure

Classroom Pilot uses a modular command structure:

```bash
# Main command groups
classroom-pilot assignments    # Assignment setup and orchestration
classroom-pilot repos         # Repository operations and collaboration
classroom-pilot secrets       # Secret and token management
classroom-pilot automation    # Scheduling and batch processing

# Legacy commands (for backward compatibility)
classroom-pilot setup         # Interactive assignment setup
classroom-pilot run           # Complete workflow execution
```

### 3. Common Workflows

```bash
# Setup a new assignment (interactive)
classroom-pilot assignments setup

# Discover student repositories
classroom-pilot repos fetch --config assignment.conf

# Add secrets to all student repos
classroom-pilot secrets add --config assignment.conf

# Run orchestrated workflow
classroom-pilot assignments orchestrate --config assignment.conf

# Check what would happen (dry-run)
classroom-pilot --dry-run assignments orchestrate
```

## 🔧 Command Reference

### Assignment Management

```bash
# Setup new assignment configuration
classroom-pilot assignments setup

# Orchestrate complete assignment workflow
classroom-pilot assignments orchestrate [--config FILE] [--dry-run]

# Manage assignment templates
classroom-pilot assignments manage [--config FILE]
```

### Repository Operations

```bash
# Fetch student repositories
classroom-pilot repos fetch [--config FILE]

# Manage collaborators
classroom-pilot repos collaborator add|remove [--config FILE]
```

### Secret Management

```bash
# Add secrets to repositories
classroom-pilot secrets add [--config FILE] [--secrets LIST]

# Remove secrets from repositories  
classroom-pilot secrets remove [--config FILE] [--secrets LIST]

# List existing secrets
classroom-pilot secrets list [--config FILE]
```

### Automation & Scheduling

```bash
# Setup cron jobs for automation
classroom-pilot automation scheduler setup [--config FILE]

# Run batch operations
classroom-pilot automation batch [--config FILE]
```

### Global Options

| Option | Description | Example |
|--------|-------------|---------|
| `--dry-run` | Preview actions without executing | `classroom-pilot --dry-run assignments orchestrate` |
| `--verbose` | Enable detailed logging | `classroom-pilot --verbose repos fetch` |
| `--config FILE` | Use custom configuration file | `classroom-pilot --config my.conf assignments setup` |
| `--help` | Show help for any command | `classroom-pilot assignments --help` |

## ⚙️ Configuration

### Assignment Configuration File

The `assignment.conf` file contains all settings for your assignment:

```bash
# Required: GitHub Classroom assignment URL
CLASSROOM_URL="https://classroom.github.com/classrooms/123/assignments/456"

# Required: Template repository URL
TEMPLATE_REPO_URL="https://github.com/instructor/assignment-template"

# Required: Assignment file to validate
ASSIGNMENT_FILE="homework.py"

# Optional: GitHub Enterprise support
GITHUB_HOSTS="github.enterprise.com,git.company.internal"

# Optional: Authentication
GITHUB_TOKEN_FILE="github_token.txt"

# Optional: Secrets management
SECRETS_LIST="API_KEY,DATABASE_URL,SECRET_TOKEN"

# Optional: Repository filtering
EXCLUDE_REPOS="template,example,demo"
INSTRUCTOR_REPOS="instructor-solution"
```

### Environment Variables

Override configuration with environment variables:

```bash
# Custom GitHub hosts
export GITHUB_HOSTS="git.company.internal,github.enterprise.com"

# GitHub token
export GITHUB_TOKEN="ghp_your_token_here"

# Custom assignment file
export ASSIGNMENT_FILE="main.cpp"

# Run with overrides
classroom-pilot assignments orchestrate
```

## 💡 Best Practices

### Workflow Recommendations

- **Always test with `--dry-run`** before making changes
- **Use `--verbose`** for debugging configuration issues
- **Keep configuration files in version control** with your assignment
- **Use environment variables** for sensitive information
- **Test with single student first** using filtered configuration

### Security Guidelines

- **Store GitHub tokens securely** using `GITHUB_TOKEN_FILE`
- **Use environment variables** for sensitive configuration
- **Review `--dry-run` output** before executing changes
- **Limit repository access** with proper filtering
- **Audit secret distribution** using verbose logging

### Configuration Management

- **Separate configs per assignment** for better organization
- **Use descriptive filenames** like `midterm-exam.conf`
- **Document custom GitHub hosts** in your assignment README
- **Validate URLs** before running batch operations

## 🛠️ Development

### Project Architecture

```
classroom_pilot/
├── __init__.py              # Package initialization
├── __main__.py             # CLI entry point
├── cli.py                  # Main Typer CLI interface
├── config.py               # Configuration management
├── bash_wrapper.py         # Legacy script wrapper
├── utils.py                # Utility functions
├── assignments/            # Assignment management
│   ├── setup.py           # Interactive setup
│   ├── orchestrator.py    # Workflow orchestration
│   └── manage.py          # Template management
├── repos/                  # Repository operations
│   ├── fetch.py           # Repository discovery
│   └── collaborator.py    # Collaborator management
├── secrets/                # Secret management
│   ├── add.py             # Secret distribution
│   ├── remove.py          # Secret removal
│   └── list.py            # Secret listing
├── automation/             # Automation & scheduling
│   ├── scheduler.py       # Cron job management
│   └── batch.py           # Batch processing
└── config/                 # Configuration system
    ├── loader.py          # Configuration loading
    ├── validator.py       # Validation logic
    └── generator.py       # Config generation
```

### Contributing

```bash
# Clone and setup development environment
git clone https://github.com/hugo-valle/classroom-pilot.git
cd classroom-pilot

# Install with Poetry
poetry install
poetry shell

# Run tests
poetry run pytest tests/ -v

# Test CLI functionality
poetry run classroom-pilot --help

# Format code
poetry run black classroom_pilot/
poetry run isort classroom_pilot/

# Type checking
poetry run mypy classroom_pilot/

# Create feature branch
git checkout -b feature/new-feature
```

### Testing

The project includes comprehensive testing:

- **153+ tests** across all modules
- **Unit tests** for individual components
- **Integration tests** for workflow validation
- **CLI tests** for command-line interface
- **100% test pass rate** requirement

```bash
# Run all tests
poetry run pytest tests/ -v

# Run specific test categories
poetry run pytest tests/test_assignments.py -v
poetry run pytest tests/test_cli.py -v

# Test with coverage
poetry run pytest tests/ --cov=classroom_pilot
```

## 📚 Documentation

### Key Resources

- **[PyPI Package](https://pypi.org/project/classroom-pilot/)** - Official package page
- **[GitHub Repository](https://github.com/hugo-valle/classroom-pilot)** - Source code and issues
- **[CI/CD Documentation](docs/CICD_WORKFLOW.md)** - Automated publishing workflow
- **[PyPI Publication Guide](docs/PYPI_PUBLICATION.md)** - Release process documentation

### Version Information

- **Current Version**: 3.1.0-alpha.1
- **Python Support**: 3.10, 3.11, 3.12
- **Package Distribution**: PyPI with automated CI/CD
- **Release Cycle**: Semantic versioning with automated publishing

## 🆘 Support

- **Documentation**: [GitHub Repository](https://github.com/hugo-valle/classroom-pilot)
- **Issues**: [GitHub Issues](https://github.com/hugo-valle/classroom-pilot/issues)
- **Package**: [PyPI Package](https://pypi.org/project/classroom-pilot/)
- **Discussions**: [GitHub Discussions](https://github.com/hugo-valle/classroom-pilot/discussions)

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Classroom Pilot** - Modern Python automation for GitHub Classroom assignment management.
