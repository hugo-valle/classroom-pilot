# Configuration Guide

This guide covers how to configure Classroom Pilot for your GitHub Classroom environment.

## Configuration Overview

Classroom Pilot uses a hierarchical configuration system that supports:

- **Configuration files** (YAML/JSON)
- **Environment variables** 
- **Command-line arguments**
- **Default values**

Configuration is loaded in order of precedence (highest to lowest):
1. Command-line arguments
2. Environment variables  
3. Configuration files
4. Default values

## Configuration File Format

### Basic Configuration

Create a configuration file in YAML format:

```yaml
# classroom-pilot.yaml
classroom:
  url: "https://classroom.github.com/classrooms/123456"
  assignment_prefix: "assignment-"
  organization: "my-classroom-org"

github:
  token: "${GITHUB_TOKEN}"
  api_url: "https://api.github.com"
  timeout: 30

assignments:
  base_directory: "./assignments"
  clone_depth: 1
  parallel_operations: 5

automation:
  schedule_enabled: true
  max_concurrent_jobs: 3
  log_level: "info"

secrets:
  encryption_enabled: true
  rotation_schedule: "monthly"
  backup_enabled: true
```

### Advanced Configuration

```yaml
# Extended configuration with all options
classroom:
  url: "https://classroom.github.com/classrooms/123456"
  assignment_prefix: "hw-"
  organization: "cs101-fall2024"
  default_branch: "main"
  
github:
  token: "${GITHUB_TOKEN}"
  api_url: "https://api.github.com"
  timeout: 30
  retry_count: 3
  rate_limit_delay: 1000

assignments:
  base_directory: "./student-work"
  clone_depth: 1
  parallel_operations: 10
  timeout: 300
  required_files:
    - "README.md"
    - "src/"
  validation_rules:
    - "no_empty_commits"
    - "require_tests"

repositories:
  fetch_strategy: "shallow"
  sync_frequency: "daily"
  collaborator_permissions: "write"
  branch_protection: true

secrets:
  encryption_enabled: true
  encryption_algorithm: "AES-256-GCM"
  key_source: "environment"
  rotation_schedule: "monthly"
  backup_enabled: true
  backup_location: "./secret-backups"
  
automation:
  schedule_enabled: true
  timezone: "UTC"
  max_concurrent_jobs: 5
  retry_attempts: 3
  retry_delay: 300
  log_level: "info"
  log_retention_days: 30
  notification_webhook: "${WEBHOOK_URL}"

logging:
  level: "info"
  format: "json"
  file: "./logs/classroom-pilot.log"
  max_size: "100MB"
  backup_count: 5
```

## Environment Variables

### Required Variables

```bash
# GitHub authentication
export GITHUB_TOKEN="ghp_your_token_here"

# Optional: GitHub organization
export GITHUB_ORG="my-classroom-org"

# Optional: Classroom URL
export CLASSROOM_URL="https://classroom.github.com/classrooms/123456"
```

### Advanced Environment Variables

```bash
# GitHub API configuration
export GITHUB_API_URL="https://api.github.com"
export GITHUB_TIMEOUT="30"
export GITHUB_RETRY_COUNT="3"

# Assignment configuration
export ASSIGNMENT_PREFIX="hw-"
export ASSIGNMENT_BASE_DIR="./assignments"
export ASSIGNMENT_CLONE_DEPTH="1"

# Automation settings
export AUTOMATION_ENABLED="true"
export AUTOMATION_TIMEZONE="UTC"
export AUTOMATION_MAX_JOBS="5"

# Secret management
export SECRETS_ENCRYPTION_KEY="your-encryption-key"
export SECRETS_BACKUP_DIR="./secret-backups"
export WEBHOOK_URL="https://hooks.slack.com/your-webhook"

# Logging configuration
export LOG_LEVEL="info"
export LOG_FILE="./logs/classroom-pilot.log"
```

## Configuration File Locations

Classroom Pilot looks for configuration files in the following order:

1. File specified with `--config` option
2. `./classroom-pilot.yaml` (current directory)
3. `./classroom-pilot.yml`
4. `~/.config/classroom-pilot/config.yaml` (user config)
5. `/etc/classroom-pilot/config.yaml` (system config)

### Creating User Configuration

```bash
# Create user configuration directory
mkdir -p ~/.config/classroom-pilot

# Create user configuration file
cat > ~/.config/classroom-pilot/config.yaml << EOF
github:
  token: "${GITHUB_TOKEN}"
  organization: "my-default-org"

logging:
  level: "info"
  file: "~/.local/share/classroom-pilot/logs/app.log"
EOF
```

## Assignment-Specific Configuration

Create configuration files for individual assignments:

```yaml
# assignments/midterm-project.yaml
assignment:
  name: "midterm-project"
  description: "Comprehensive midterm project"
  due_date: "2024-03-15T23:59:59Z"
  
github:
  organization: "cs101-fall2024"
  template_repo: "midterm-template"
  
requirements:
  files:
    - "README.md"
    - "src/main.py"
    - "tests/"
    - "requirements.txt"
  
secrets:
    - name: "API_KEY"
      description: "External API key for project"
    - name: "DATABASE_URL" 
      description: "Database connection string"
      
validation:
  rules:
    - "has_readme"
    - "has_tests"
    - "code_compiles"
    - "tests_pass"
    
grading:
  rubric_file: "rubrics/midterm-rubric.yaml"
  auto_grade: true
  deadline_enforcement: "strict"
```

## Configuration Validation

### Validate Configuration

```bash
# Validate current configuration
classroom-pilot config validate

# Validate specific configuration file
classroom-pilot config validate --file ./custom-config.yaml

# Validate with detailed output
classroom-pilot config validate --detailed

# Check configuration and show resolved values
classroom-pilot config show --resolved
```

### Configuration Schema

Classroom Pilot validates configuration against a JSON schema:

```bash
# Generate configuration schema
classroom-pilot config schema > config-schema.json

# Validate against schema
classroom-pilot config validate --schema config-schema.json
```

## Common Configuration Patterns

### Development Environment

```yaml
# dev-config.yaml
github:
  token: "${GITHUB_TOKEN}"
  organization: "test-classroom"

assignments:
  base_directory: "./dev-assignments"
  
logging:
  level: "debug"
  file: "./dev.log"

automation:
  schedule_enabled: false
```

### Production Environment

```yaml
# prod-config.yaml
github:
  token: "${GITHUB_TOKEN}"
  organization: "cs101-fall2024"
  timeout: 60
  retry_count: 5

assignments:
  base_directory: "/var/classroom-pilot/assignments"
  parallel_operations: 20

automation:
  schedule_enabled: true
  max_concurrent_jobs: 10
  log_level: "info"

logging:
  level: "info"
  file: "/var/log/classroom-pilot/app.log"
  format: "json"
```

### Multi-Class Setup

```yaml
# multi-class-config.yaml
classes:
  cs101:
    github:
      organization: "cs101-fall2024"
    assignments:
      base_directory: "./cs101"
      
  cs201:
    github:
      organization: "cs201-fall2024"
    assignments:
      base_directory: "./cs201"

# Use with: classroom-pilot --class cs101 assignments setup
```

## Security Configuration

### Token Management

```bash
# Store token securely
echo "ghp_your_token_here" | gpg --encrypt > github-token.gpg

# Use encrypted token
export GITHUB_TOKEN=$(gpg --decrypt github-token.gpg)
```

### Secret Encryption

```yaml
# Enable secret encryption
secrets:
  encryption_enabled: true
  encryption_algorithm: "AES-256-GCM"
  key_source: "environment"  # or "file", "vault"
  key_file: "./encryption.key"  # if key_source is "file"
```

### Access Control

```yaml
# Restrict operations by user/role
access_control:
  enabled: true
  rules:
    - user: "instructor"
      permissions: ["all"]
    - user: "ta"
      permissions: ["repos:read", "secrets:add"]
    - role: "grader"
      permissions: ["assignments:grade"]
```

## Configuration Management

### Version Control

```bash
# Initialize configuration repository
git init classroom-config
cd classroom-config

# Add configuration files
cp ~/.config/classroom-pilot/config.yaml .
git add config.yaml
git commit -m "Initial configuration"

# Use versioned configuration
classroom-pilot --config ./classroom-config/config.yaml
```

### Configuration Templates

```yaml
# template-config.yaml
classroom:
  url: "{{ CLASSROOM_URL }}"
  organization: "{{ GITHUB_ORG }}"

github:
  token: "{{ GITHUB_TOKEN }}"

# Use with substitution
envsubst < template-config.yaml > resolved-config.yaml
```

## Troubleshooting Configuration

### Common Issues

**Invalid Configuration:**
```bash
# Check configuration syntax
classroom-pilot config validate --file config.yaml

# Show resolved configuration
classroom-pilot config show --resolved
```

**Missing Environment Variables:**
```bash
# Check required variables
classroom-pilot config check-env

# Show environment variables used
classroom-pilot config show --env-only
```

**Permission Issues:**
```bash
# Test GitHub token permissions
classroom-pilot auth check

# Verify organization access
classroom-pilot auth check --org my-classroom-org
```

### Debug Configuration Loading

```bash
# Show configuration sources
classroom-pilot --verbose config show

# Debug configuration resolution
classroom-pilot --debug config validate
```

## Configuration Best Practices

1. **Security**:
   - Never commit tokens to version control
   - Use environment variables for sensitive data
   - Enable encryption for stored secrets
   - Regularly rotate access tokens

2. **Organization**:
   - Use separate configurations for different environments
   - Version control non-sensitive configuration
   - Document configuration options and their purposes
   - Use consistent naming conventions

3. **Maintenance**:
   - Regularly validate configuration files
   - Monitor for deprecated options
   - Test configuration changes in development first
   - Backup critical configuration files

4. **Performance**:
   - Tune parallel operation limits
   - Set appropriate timeouts
   - Configure proper retry policies
   - Monitor resource usage

## See Also

- [Installation Guide](installation.md)
- [Quick Start Guide](quick-start.md)
- [CLI Reference](../cli/overview.md)
- [Security Best Practices](../development/security.md)
