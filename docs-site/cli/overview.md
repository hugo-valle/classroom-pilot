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

Classroom Pilot provides two types of global options based on their scope and placement:

### Main-Level Options

These options are placed **before** the subcommand group and control application-wide behavior:

| Option | Description | Example |
|--------|-------------|---------|
| `--version` | Display version information and exit | `classroom-pilot --version` |
| `--config <file>` | Specify custom configuration file (default: assignment.conf) | `classroom-pilot --config custom.conf assignments setup` |
| `--assignment-root <path>` | Specify assignment root directory containing configuration | `classroom-pilot --assignment-root /path/to/assignment repos fetch` |
| `--help` | Display main help information | `classroom-pilot --help` |

### Subcommand-Group-Level Options

These options are placed **after** the subcommand group name but **before** the individual command:

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--verbose` | `-v` | Enable detailed logging output (available for all subcommand groups) | `classroom-pilot assignments --verbose orchestrate` |
| `--dry-run` | | Show what would be done without executing (available for all subcommand groups) | `classroom-pilot repos --dry-run fetch` |
| `--help` | `-h` | Display help for the subcommand group or command | `classroom-pilot assignments --help` |

### Option Placement Examples

**Correct placement:**

```bash
# Main-level options (before subcommand)
classroom-pilot --config custom.conf assignments setup
classroom-pilot --assignment-root /path/to/assignment repos fetch

# Subcommand-group-level options (after subcommand group)
classroom-pilot assignments --verbose --dry-run orchestrate
classroom-pilot repos --dry-run fetch
classroom-pilot secrets --verbose add
classroom-pilot automation --dry-run cron-install sync
classroom-pilot config --verbose --dry-run set-token ghp_token
```

**Help at different levels:**

```bash
classroom-pilot --help                    # Main help
classroom-pilot assignments --help        # Assignments subcommand group help
classroom-pilot assignments setup --help  # Individual command help
```

### Global Options Behavior

#### Verbose Mode (`--verbose`, `-v`)

When enabled, verbose mode provides detailed logging output including:

- Configuration loading and parsing details
- API request and response information
- File system operations
- Progress indicators for long-running operations
- Debug-level messages for troubleshooting

**Example:**
```bash
# See detailed output during assignment orchestration
classroom-pilot assignments --verbose orchestrate

# Debug token validation issues
classroom-pilot config --verbose check-token
```

#### Dry-Run Mode (`--dry-run`)

Dry-run mode shows exactly what would be executed without making any actual changes:

- Displays planned operations with "DRY RUN:" prefix
- Shows which files would be modified
- Lists repositories that would be affected
- Previews secrets that would be deployed
- Validates configuration without executing

**Example:**
```bash
# Preview what orchestration would do
classroom-pilot assignments --dry-run orchestrate

# Check what token changes would occur
classroom-pilot config --dry-run set-token ghp_new_token
```

#### Combined Options

Options can be combined for maximum control during development and testing:

```bash
# Verbose dry-run: see detailed output without executing
classroom-pilot assignments --verbose --dry-run orchestrate

# Custom config with verbose output
classroom-pilot --config test.conf repos --verbose fetch

# All options together
classroom-pilot --verbose --assignment-root /path --config custom.conf assignments --dry-run setup
```

### Troubleshooting Tips

**Common Mistakes:**

1. **Wrong option placement:**
   ```bash
   # ❌ Wrong: verbose before subcommand
   classroom-pilot --verbose assignments orchestrate
   
   # ✅ Correct: verbose after subcommand group
   classroom-pilot assignments --verbose orchestrate
   ```

2. **Mixing main and subcommand options:**
   ```bash
   # ❌ Wrong: config after subcommand
   classroom-pilot assignments --config custom.conf setup
   
   # ✅ Correct: config before subcommand
   classroom-pilot --config custom.conf assignments setup
   ```

**Verification:**

- **Check verbose is working:** Look for "DEBUG" level messages or detailed configuration output in stderr
- **Check dry-run is working:** Look for "DRY RUN:" prefix in output messages
- **Verify option recognition:** Use `--help` to see available options at each level

**Best Practices:**

1. Use `--dry-run` first when testing new configurations
2. Combine `--verbose --dry-run` for maximum visibility during development
3. Use `--config` with test configurations before modifying production
4. Always verify `--help` at the command level if unsure about options

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
