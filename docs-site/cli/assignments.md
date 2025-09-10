# Assignment Commands

The assignment commands provide comprehensive tools for managing GitHub Classroom assignments throughout their lifecycle.

## Overview

Assignment management in Classroom Pilot covers the complete workflow from initial setup through ongoing maintenance and automation.

## Commands

### `classroom-pilot assignments setup`

Initialize a new assignment with proper configuration and repository structure.

```bash
# Basic assignment setup
classroom-pilot assignments setup

# Setup with specific configuration
classroom-pilot assignments setup --config assignment.conf

# Dry run to preview changes
classroom-pilot assignments setup --dry-run

# Verbose output for debugging
classroom-pilot assignments setup --verbose
```

**Options:**
- `--config PATH`: Specify custom configuration file
- `--dry-run`: Show what would be done without making changes
- `--verbose`: Enable detailed output
- `--help`: Show command help

**Example:**
```bash
# Setup assignment with custom config
classroom-pilot assignments setup \
  --config assignments/hw01-config.yaml \
  --verbose
```

### `classroom-pilot assignments orchestrate`

Execute the complete assignment workflow including repository creation, secret distribution, and collaboration setup.

```bash
# Run full orchestration
classroom-pilot assignments orchestrate

# Orchestrate specific assignment
classroom-pilot assignments orchestrate --assignment "homework-01"

# Skip specific steps
classroom-pilot assignments orchestrate --skip-secrets

# Run with custom timing
classroom-pilot assignments orchestrate --delay 30
```

**Options:**
- `--assignment NAME`: Target specific assignment
- `--skip-secrets`: Skip secret distribution
- `--skip-collaborators`: Skip collaborator management
- `--delay SECONDS`: Delay between operations (default: 10)
- `--max-retries COUNT`: Maximum retry attempts (default: 3)
- `--dry-run`: Preview operations without execution

**Workflow Steps:**
1. **Repository Discovery**: Find student repositories
2. **Secret Distribution**: Add repository secrets
3. **Collaborator Management**: Configure access permissions
4. **Validation**: Verify setup completion
5. **Reporting**: Generate operation summary

### `classroom-pilot assignments status`

Check the current status of assignments and their repositories.

```bash
# Check all assignments
classroom-pilot assignments status

# Check specific assignment
classroom-pilot assignments status --assignment "homework-01"

# Detailed status report
classroom-pilot assignments status --detailed

# Export status to file
classroom-pilot assignments status --output status-report.json
```

**Options:**
- `--assignment NAME`: Check specific assignment
- `--detailed`: Include repository-level details
- `--output FILE`: Save report to file
- `--format FORMAT`: Output format (table, json, yaml)

### `classroom-pilot assignments validate`

Validate assignment configuration and repository state.

```bash
# Validate current configuration
classroom-pilot assignments validate

# Validate specific assignment
classroom-pilot assignments validate --assignment "homework-01"

# Validate with strict checking
classroom-pilot assignments validate --strict

# Generate validation report
classroom-pilot assignments validate --report validation.html
```

**Options:**
- `--assignment NAME`: Validate specific assignment
- `--strict`: Enable strict validation rules
- `--report FILE`: Generate HTML validation report
- `--fix`: Automatically fix detected issues

## Configuration

Assignment commands use configuration files to define:

```yaml
# assignment.conf
assignment:
  name: "homework-01"
  prefix: "hw01-"
  template_repo: "classroom-template"
  
github:
  organization: "my-class-org"
  token: "${GITHUB_TOKEN}"
  
automation:
  retry_count: 3
  delay_seconds: 10
  
validation:
  required_files:
    - "README.md"
    - "src/"
    - ".github/workflows/"
```

## Integration

Assignment commands integrate seamlessly with:

- **[Repository Operations](repositories.md)**: Manage student repositories
- **[Secret Management](secrets.md)**: Distribute assignment secrets
- **[Automation](automation.md)**: Schedule assignment workflows

## Examples

### Complete Assignment Setup

```bash
# 1. Setup assignment configuration
classroom-pilot assignments setup \
  --config assignments/midterm-project.yaml

# 2. Orchestrate full workflow
classroom-pilot assignments orchestrate \
  --assignment "midterm-project" \
  --verbose

# 3. Validate setup
classroom-pilot assignments validate \
  --assignment "midterm-project" \
  --report validation.html

# 4. Check status
classroom-pilot assignments status \
  --assignment "midterm-project" \
  --detailed
```

### Automated Assignment Management

```bash
# Setup automation for ongoing management
classroom-pilot automation schedule \
  --command "assignments orchestrate" \
  --cron "0 6 * * *" \
  --assignment "weekly-labs"

# Monitor assignment status
classroom-pilot assignments status \
  --output daily-report.json \
  --format json
```

## Troubleshooting

### Common Issues

**Configuration Errors:**
```bash
# Validate configuration
classroom-pilot assignments validate --strict

# Check configuration syntax
classroom-pilot config validate --file assignment.conf
```

**Repository Access Issues:**
```bash
# Verify GitHub token permissions
classroom-pilot auth check

# Test repository access
classroom-pilot repos list --assignment "homework-01"
```

**Orchestration Failures:**
```bash
# Run with verbose logging
classroom-pilot assignments orchestrate \
  --verbose \
  --max-retries 5 \
  --delay 60

# Check specific step failures
classroom-pilot assignments status --detailed
```

### Getting Help

```bash
# General help
classroom-pilot assignments --help

# Command-specific help
classroom-pilot assignments setup --help
classroom-pilot assignments orchestrate --help

# Configuration help
classroom-pilot config --help
```

## Best Practices

1. **Configuration Management**:
   - Use version control for assignment configurations
   - Test configurations with `--dry-run` before execution
   - Validate configurations before deployment

2. **Automation Setup**:
   - Schedule regular orchestration runs
   - Monitor assignment status daily
   - Set up alerts for failures

3. **Error Handling**:
   - Always use `--verbose` for troubleshooting
   - Implement retry logic for network operations
   - Maintain backup configurations

4. **Security**:
   - Store sensitive data in environment variables
   - Use GitHub tokens with minimal required permissions
   - Regularly rotate access tokens

## See Also

- [Repository Operations](repositories.md)
- [Secret Management](secrets.md)
- [Automation Commands](automation.md)
- [Configuration Guide](../getting-started/configuration.md)
