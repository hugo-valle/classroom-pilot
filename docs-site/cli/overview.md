# CLI Overview

Classroom Pilot provides a comprehensive command-line interface organized into logical command groups.

## 🏗️ Command Structure

The CLI is organized into four main command groups:

```bash
classroom-pilot [GLOBAL_OPTIONS] COMMAND [ARGS]...
```

### Command Groups

| Group | Purpose | Commands |
|-------|---------|----------|
| `assignments` | Assignment setup and orchestration | `setup`, `orchestrate`, `manage` |
| `repos` | Repository operations | `fetch`, `collaborator` |
| `secrets` | Secret and token management | `add`, `remove`, `list` |
| `automation` | Scheduling and batch processing | `scheduler`, `batch` |

### Legacy Commands

For backward compatibility:

| Command | Purpose | Modern Equivalent |
|---------|---------|-------------------|
| `setup` | Interactive assignment setup | `assignments setup` |
| `run` | Complete workflow execution | `assignments orchestrate` |
| `version` | Show version information | `version` |

## ⚙️ Global Options

Global options apply to all commands:

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--dry-run` | | Preview actions without executing | `classroom-pilot --dry-run assignments orchestrate` |
| `--verbose` | | Enable detailed logging | `classroom-pilot --verbose repos fetch` |
| `--config FILE` | | Use custom configuration file | `classroom-pilot --config my.conf secrets add` |
| `--help` | | Show help information | `classroom-pilot --help` |

## 📋 Quick Reference

### Assignment Management

```bash
# Interactive setup
classroom-pilot assignments setup

# Run complete workflow
classroom-pilot assignments orchestrate [--config FILE]

# Manage templates
classroom-pilot assignments manage [--config FILE]
```

### Repository Operations

```bash
# Discover student repositories
classroom-pilot repos fetch [--config FILE]

# Add collaborators
classroom-pilot repos collaborator add [--config FILE]

# Remove collaborators
classroom-pilot repos collaborator remove [--config FILE]
```

### Secret Management

```bash
# Add secrets to repositories
classroom-pilot secrets add [--config FILE] [--secrets LIST]

# Remove secrets
classroom-pilot secrets remove [--config FILE] [--secrets LIST]

# List existing secrets
classroom-pilot secrets list [--config FILE]
```

### Automation & Scheduling

```bash
# Setup automated scheduling
classroom-pilot automation scheduler setup [--config FILE]

# Check scheduler status
classroom-pilot automation scheduler status

# Run batch operations
classroom-pilot automation batch [--config FILE]
```

## 🔧 Configuration

All commands support configuration via:

1. **Configuration file** (default: `assignment.conf`)
2. **Environment variables**
3. **Command-line options**

### Configuration File Example

```bash
# assignment.conf
CLASSROOM_URL="https://classroom.github.com/classrooms/123/assignments/homework1"
TEMPLATE_REPO_URL="https://github.com/instructor/homework1-template"
ASSIGNMENT_FILE="homework1.py"
GITHUB_TOKEN_FILE="github_token.txt"
SECRETS_LIST="API_KEY,GRADING_TOKEN"
```

### Environment Variable Overrides

```bash
# Override configuration
export GITHUB_TOKEN="ghp_your_token"
export ASSIGNMENT_FILE="main.cpp"

# Run commands
classroom-pilot assignments orchestrate
```

## 💡 Usage Patterns

### Development & Testing

```bash
# Always preview first
classroom-pilot --dry-run assignments orchestrate --config assignment.conf

# Use verbose for debugging
classroom-pilot --verbose repos fetch --config assignment.conf

# Test with single repository
classroom-pilot --dry-run secrets add --config assignment.conf
```

### Production Workflows

```bash
# Complete assignment setup
classroom-pilot assignments setup

# Daily orchestration
classroom-pilot assignments orchestrate --config assignment.conf

# Emergency secret rotation
classroom-pilot secrets remove --config assignment.conf --secrets "OLD_TOKEN"
NEW_TOKEN="value" classroom-pilot secrets add --config assignment.conf --secrets "NEW_TOKEN"
```

### Batch Operations

```bash
# Multiple assignments
for config in assignment-*.conf; do
    classroom-pilot assignments orchestrate --config "$config"
done

# Specific operations across assignments
classroom-pilot secrets add --config hw1.conf
classroom-pilot secrets add --config hw2.conf
classroom-pilot secrets add --config midterm.conf
```

## 🆘 Help System

### Getting Help

```bash
# Main help
classroom-pilot --help

# Command group help
classroom-pilot assignments --help
classroom-pilot repos --help
classroom-pilot secrets --help
classroom-pilot automation --help

# Specific command help
classroom-pilot assignments orchestrate --help
classroom-pilot secrets add --help
```

### Error Messages

The CLI provides informative error messages:

- **Configuration errors**: Invalid file paths, missing required fields
- **Authentication errors**: Invalid tokens, insufficient permissions
- **API errors**: Rate limiting, repository access issues
- **Validation errors**: Invalid URLs, malformed configuration

## 🔍 Debugging

### Verbose Mode

Enable detailed logging for troubleshooting:

```bash
# Verbose output
classroom-pilot --verbose assignments orchestrate --config assignment.conf

# Combine with dry-run for detailed preview
classroom-pilot --dry-run --verbose assignments orchestrate --config assignment.conf
```

### Log Information

Verbose mode shows:

- Configuration loading and validation
- API calls and responses
- Repository discovery process
- Secret distribution status
- Error details and stack traces

## 📚 Related Documentation

- [Assignments](assignments.md) - Assignment management commands
- [Repositories](repositories.md) - Repository operation commands
- [Secrets](secrets.md) - Secret management commands
- [Automation](automation.md) - Automation and scheduling commands
