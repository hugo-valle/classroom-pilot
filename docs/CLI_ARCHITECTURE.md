# Classroom Pilot v3.0 - Modular CLI Architecture

## Overview

Classroom Pilot v3.0 introduces a comprehensive modular CLI architecture designed for scalability, maintainability, and future expansion. The new structure supports enterprise-scale development patterns and enables clean integration for future GUI and web application development.

## Installation

```bash
# Clone the repository
git clone https://github.com/hugo-valle/classroom-pilot.git
cd classroom-pilot

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## New CLI Structure

The CLI is now organized into logical subcommands that group related functionality:

### Main Commands

```bash
# Show help for all commands
python -m classroom_pilot --help

# Show version information
python -m classroom_pilot version
```

### Assignment Management

```bash
# Interactive assignment setup wizard (Python)
python -m classroom_pilot assignments setup

# Run complete assignment orchestration workflow
python -m classroom_pilot assignments orchestrate [--dry-run] [--verbose]

# High-level assignment lifecycle management
python -m classroom_pilot assignments manage
```

### Repository Operations

```bash
# Discover and fetch student repositories
python -m classroom_pilot repos fetch [--dry-run] [--verbose]

# Update assignment configuration and student repositories
python -m classroom_pilot repos update [--dry-run] [--verbose]

# Sync template repository to GitHub Classroom
python -m classroom_pilot repos push [--dry-run] [--verbose]

# Cycle repository collaborator permissions
python -m classroom_pilot repos cycle-collaborator [options]
```

### Secret Management

```bash
# Add or update secrets in student repositories
python -m classroom_pilot secrets add [--dry-run] [--verbose]

# Advanced secret and token management
python -m classroom_pilot secrets manage
```

### Automation & Scheduling

```bash
# Manage cron automation jobs
python -m classroom_pilot automation cron [--action status|install|remove]

# Execute scheduled synchronization tasks
python -m classroom_pilot automation sync [--dry-run] [--verbose]

# Run batch processing operations
python -m classroom_pilot automation batch
```

### Legacy Compatibility

For backward compatibility, the following legacy commands are still available:

```bash
# Legacy setup command (redirects to assignments setup)
python -m classroom_pilot setup

# Legacy run command (redirects to assignments orchestrate)
python -m classroom_pilot run [--dry-run] [--verbose]
```

## Package Architecture

### Modular Structure

```
classroom_pilot/
├── __init__.py              # Main package exports
├── __main__.py              # Module entry point
├── cli.py                   # Main CLI interface
├── cli_legacy.py            # Legacy CLI (deprecated)
├── bash_wrapper.py          # Bash script integration
├── config/                  # Configuration management
│   ├── __init__.py
│   ├── loader.py           # Configuration loading
│   └── validator.py        # Configuration validation
├── assignments/             # Assignment operations
│   ├── __init__.py
│   ├── setup.py            # Interactive setup wizard
│   ├── orchestrator.py     # Workflow orchestration
│   └── manage.py           # Lifecycle management
├── repos/                   # Repository operations
│   ├── __init__.py
│   ├── fetch.py            # Repository fetching
│   └── collaborator.py     # Collaborator management
├── secrets/                 # Secret management
│   ├── __init__.py
│   └── manager.py          # Token and secret operations
├── automation/              # Automation and scheduling
│   ├── __init__.py
│   └── scheduler.py        # Cron and batch processing
├── utils/                   # Shared utilities
│   ├── __init__.py
│   ├── logger.py           # Rich logging framework
│   ├── git.py              # Git operations
│   └── paths.py            # Path management
└── scripts/                 # Legacy bash scripts
    └── ...
```

### Design Principles

1. **Separation of Concerns**: Each package handles a specific domain
2. **Modular Architecture**: Independent modules with clear interfaces
3. **Rich Logging**: Comprehensive logging with colors and progress indicators
4. **Type Safety**: Full type hints for better development experience
5. **Future-Ready**: Architecture supports GUI and web development
6. **Backward Compatibility**: Legacy commands still work during transition

## Enhanced Features

### Rich Logging

- **Colored Output**: Different colors for info, warning, error messages
- **Progress Indicators**: Visual progress bars for long operations
- **File Logging**: Automatic log file generation with rotation
- **Structured Logging**: JSON-compatible log format for analysis

### Configuration Management

- **Shell Format Support**: Native support for bash-style configuration files
- **Validation**: Comprehensive validation for URLs, paths, and formats
- **Environment Integration**: Seamless integration with environment variables
- **Auto-Discovery**: Automatic configuration file discovery

### Git Integration

- **Repository Operations**: Clone, pull, status checking, and management
- **Workspace Management**: Automatic workspace discovery and setup
- **Status Tracking**: Real-time repository status monitoring
- **Error Handling**: Robust error handling with detailed reporting

## Migration from v1.x

### Command Mapping

| v1.x Command | v2.x Equivalent |
|--------------|-----------------|
| `python -m classroom_pilot setup` | `python -m classroom_pilot assignments setup` |
| `python -m classroom_pilot run` | `python -m classroom_pilot assignments orchestrate` |
| No direct equivalent | `python -m classroom_pilot repos fetch` |
| No direct equivalent | `python -m classroom_pilot secrets add` |
| No direct equivalent | `python -m classroom_pilot automation cron` |

### Configuration Files

Configuration files remain fully compatible. No changes required for existing setups.

### Bash Scripts

All existing bash scripts continue to work through the bash wrapper system. Python implementations will gradually replace bash scripts while maintaining full compatibility.

## Development Roadmap

### Phase 1: Foundation (Current)
- ✅ Modular CLI architecture
- ✅ Package structure implementation
- ✅ Enhanced utilities (logging, git, paths)
- ✅ Configuration management
- ✅ Assignment setup migration

### Phase 2: Core Migrations
- 🚧 Repository operations (fetch, update, push)
- 🚧 Secret management implementation
- 🚧 Automation and scheduling
- 🚧 Collaborator management

### Phase 3: Enhancement
- ⏳ GitHub API integration
- ⏳ Advanced batch processing
- ⏳ Comprehensive testing suite
- ⏳ Performance optimization

### Phase 4: Expansion
- ⏳ GUI application development
- ⏳ Web interface implementation
- ⏳ PyPI package publication
- ⏳ Plugin system architecture

## Contributing

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/hugo-valle/classroom-pilot.git
cd classroom-pilot

# Create development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt
pip install -e .

# Run tests
python -m pytest tests/
```

### Code Style

- **Type Hints**: All new code must include comprehensive type hints
- **Docstrings**: All public functions and classes must have docstrings
- **Logging**: Use the centralized logging system for all output
- **Error Handling**: Comprehensive error handling with user-friendly messages

### Package Guidelines

1. Each package should be self-contained with minimal dependencies
2. Use dependency injection for external dependencies
3. Implement comprehensive error handling and logging
4. Include type hints for all public interfaces
5. Write unit tests for all new functionality

## Support

For questions, issues, or contributions:

- **GitHub Issues**: https://github.com/hugo-valle/classroom-pilot/issues
- **Documentation**: See `docs/` directory for detailed documentation
- **Legacy Documentation**: See `docs/README_LEGACY.md` for v1.x documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.
