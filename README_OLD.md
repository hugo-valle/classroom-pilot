# Classroom Pilot

A comprehensive Python CLI tool for automating GitHub Classroom assignment management with modular workflow orchestration, repository operations, and secret management.

[![PyPI version](https://badge.fury.io/py/classroom-pilot.svg)](https://badge.fury.io/py/classroom-pilot)
[![Python Support](https://img.shields.io/pypi/pyversions/classroom-pilot.svg)](https://pypi.org/project/classroom-pilot/)
[![Tests](https://github.com/hugo-valle/classroom-pilot/workflows/Tests/badge.svg)](https://github.com/hugo-valle/classroom-pilot/actions)

## 🎯 Overview

Classroom Pilot provides instructors with a powerful, modern CLI to automate GitHub Classroom workflows:

- **🐍 Modern Python CLI** - Type-safe, intuitive commands with rich help and output
- **� PyPI Package** - Simple installation: `pip install classroom-pilot`
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
- ✅ **Enterprise GitHub support** for custom hosting environments
- ✅ **Comprehensive documentation** and testing infrastructure

### 🚧 Upcoming Features

#### Phase 2 Completion
- **Web API foundation** for future dashboard integration
- **Plugin architecture** for extensible functionality
- **Enhanced analytics** and reporting capabilities
- **Integration testing** with real classroom environments

#### Phase 3: Web Interface & Advanced Features
- **React-based web dashboard** for visual assignment management
- **Real-time monitoring** and notification systems
- **Multi-classroom management** with role-based access
- **Advanced analytics** and student progress tracking

## 📦 Installation

### Option 1: Install via pip (Recommended)

```bash
# Install the latest version
pip install classroom-pilot

# Or install from source
pip install git+https://github.com/hugo-valle/classroom-pilot.git

# Verify installation
classroom-pilot --help
```

### Option 2: Install with Poetry

```bash
# Clone the repository
git clone https://github.com/hugo-valle/classroom-pilot.git
cd classroom-pilot

# Install with Poetry
poetry install

# Activate the environment
poetry shell

# Verify installation
classroom-pilot --help
```

### Option 3: Development Installation

```bash
# Clone and install in development mode
git clone https://github.com/hugo-valle/classroom-pilot.git
cd classroom-pilot

# Install in editable mode
pip install -e .

# Or install development dependencies
pip install -r requirements-dev.txt
```

### Requirements

- **Python 3.10+** (3.11+ recommended)
- **Git** for repository operations
- **GitHub CLI** (gh) for authentication
- **Bash/Zsh** shell environment

## 🚀 Quick Start

### 1. Configure Your Assignment

Create an assignment configuration file:

```bash
# Create assignment.conf
cat > assignment.conf << 'EOF'
# Assignment Configuration
CLASSROOM_URL="https://classroom.github.com/classrooms/123/assignments/456"
TEMPLATE_REPO_URL="https://github.com/instructor/assignment-template"
ASSIGNMENT_FILE="homework.py"

# GitHub Configuration
GITHUB_TOKEN_FILE="github_token.txt"
SECRETS_LIST="API_KEY,DATABASE_URL"
EOF
```

### 2. Run Commands

```bash
# Show all available commands
classroom-pilot --help

# Sync template to GitHub Classroom (dry-run first)
classroom-pilot --dry-run sync

# Discover student repositories
classroom-pilot discover

# Add secrets to student repositories
classroom-pilot secrets

# Run complete workflow
classroom-pilot run

# Get detailed help for any command
classroom-pilot sync --help
```

### 3. Configuration Options

```bash
# Use custom configuration file
classroom-pilot --config-file my-assignment.conf sync

# Enable verbose logging
classroom-pilot --verbose discover

# Skip confirmation prompts
classroom-pilot --yes secrets

# Combine options
classroom-pilot --config-file assignment.conf --dry-run --verbose run
```

## 🔧 Configuration

### Assignment Configuration File

Create an `assignment.conf` file with your assignment settings:

```bash
# Required: GitHub Classroom assignment URL
CLASSROOM_URL="https://classroom.github.com/classrooms/123/assignments/456"

# Required: Template repository URL
TEMPLATE_REPO_URL="https://github.com/instructor/assignment-template"

# Required: Assignment file to validate
ASSIGNMENT_FILE="homework.py"

# Optional: GitHub Enterprise support
GITHUB_HOSTS="github.enterprise.com,git.company.internal"

# Optional: Secrets management
GITHUB_TOKEN_FILE="github_token.txt"
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
classroom-pilot sync
```

### Multi-line Arrays

Support for complex configuration arrays:

```bash
# Multi-line secrets list
SECRETS_LIST=(
    "API_KEY"
    "DATABASE_URL" 
    "SECRET_TOKEN"
    "WEBHOOK_SECRET"
)

# Multi-line exclude list
EXCLUDE_REPOS=(
    "template"
    "example" 
    "demo"
    "instructor-*"
)
```

## 📋 Commands Reference

### Main Commands

| Command | Description | Example |
|---------|-------------|---------|
| `run` | Execute complete workflow | `classroom-pilot run` |
| `sync` | Sync template to classroom | `classroom-pilot sync` |
| `discover` | Find student repositories | `classroom-pilot discover` |
| `secrets` | Manage repository secrets | `classroom-pilot secrets` |
| `assist` | Help students with issues | `classroom-pilot assist` |
| `version` | Show version information | `classroom-pilot version` |

### Global Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--dry-run` | `-n` | Preview without executing | `classroom-pilot --dry-run sync` |
| `--verbose` | `-v` | Enable detailed logging | `classroom-pilot --verbose discover` |
| `--config-file` | `-c` | Use custom config file | `classroom-pilot -c my.conf sync` |
| `--yes` | `-y` | Skip confirmation prompts | `classroom-pilot --yes secrets` |
| `--help` | | Show help information | `classroom-pilot --help` |

### Workflow Examples

```bash
# Complete assignment setup workflow
classroom-pilot --config-file assignment.conf run

# Sync template changes only
classroom-pilot --dry-run sync
classroom-pilot sync

# Update secrets for all students
classroom-pilot --verbose secrets

# Help specific students
classroom-pilot --config-file student-issues.conf assist

# Check what would happen
classroom-pilot --dry-run --verbose run
```

## 💡 Best Practices

### Development Workflow

- **Always test with `--dry-run`** before making changes
- **Use `--verbose`** for debugging configuration issues
- **Keep configuration files in version control** with your assignment
- **Use environment variables** for sensitive information
- **Test with single student first** using filtered configuration

### Configuration Management

- **Separate configs per assignment** for better organization
- **Use descriptive filenames** like `midterm-exam.conf`
- **Document custom GitHub hosts** in your assignment README
- **Validate URLs** before running batch operations

### Security Considerations

- **Store GitHub tokens securely** using `GITHUB_TOKEN_FILE`
- **Use environment variables** for sensitive configuration
- **Review `--dry-run` output** before executing changes
- **Limit repository access** with proper filtering
- **Audit secret distribution** using verbose logging

## 🛠️ Development

### Project Structure

```
classroom_pilot/
├── __init__.py          # Package initialization
├── __main__.py          # CLI entry point
├── cli.py               # Typer CLI implementation
├── config.py            # Configuration management
├── bash_wrapper.py      # Script execution wrapper
├── utils.py             # Utility functions
├── scripts/             # Bash scripts
│   ├── __init__.py
│   ├── *.sh             # Individual workflow scripts
└── docs/                # Documentation
```

### Contributing

```bash
# Clone and setup development environment
git clone https://github.com/hugo-valle/classroom-pilot.git
cd classroom-pilot

# Install development dependencies
pip install -r requirements-dev.txt
pip install -e .

# Run tests
make test              # Quick functionality tests
make test-unit         # Full pytest unit tests
pytest tests/ -v       # Run tests directly

# Run comprehensive tests
make test-full
python tests/test_comprehensive.py

# Format code
black classroom_pilot/
isort classroom_pilot/

# Type checking
mypy classroom_pilot/

# Create feature branch
git checkout -b feature/new-feature
```

### Architecture

- **Modern Python CLI** built with Typer for rich interaction
- **Configuration-driven** with validation and environment expansion  
- **Bash script compatibility** through wrapper execution
- **Cross-platform support** with proper path handling
- **Enterprise GitHub support** with custom host validation
- **Type safety** with comprehensive type annotations

## 📞 Support

- **Documentation**: [GitHub Repository](https://github.com/hugo-valle/classroom-pilot)
- **Issues**: [GitHub Issues](https://github.com/hugo-valle/classroom-pilot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/hugo-valle/classroom-pilot/discussions)

---

---

**Classroom Pilot** - Streamlining GitHub Classroom assignment management through modern automation.
