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

# Setup with specific configuration (main-level option before subcommand)
classroom-pilot --config assignment.conf assignments setup

# Dry run to preview changes (group-level option after subcommand group)
classroom-pilot assignments --dry-run setup

# Verbose output for debugging (group-level option after subcommand group)
classroom-pilot assignments --verbose setup

# Combine verbose and dry-run
classroom-pilot assignments --verbose --dry-run setup
```

**Main-Level Options** (placed before `assignments`):
- `--config PATH`: Specify custom configuration file
- `--assignment-root PATH`: Specify assignment root directory

**Group-Level Options** (placed after `assignments`, before `setup`):
- `--dry-run`: Show what would be done without making changes
- `--verbose`: Enable detailed output
- `--help`: Show command help

**Example:**
```bash
# Setup assignment with custom config and verbose output
classroom-pilot --config assignments/hw01-config.yaml \
  assignments --verbose setup
```

### `classroom-pilot assignments orchestrate`

Execute the complete assignment workflow including repository creation, secret distribution, and collaboration setup.

```bash
# Run full orchestration
classroom-pilot assignments orchestrate

# Orchestrate with verbose output (group-level option)
classroom-pilot assignments --verbose orchestrate

# Dry run to preview operations (group-level option)
classroom-pilot assignments --dry-run orchestrate

# Combine verbose and dry-run for maximum visibility
classroom-pilot assignments --verbose --dry-run orchestrate

# With custom configuration (main-level option)
classroom-pilot --config custom.conf assignments orchestrate
```

**Main-Level Options** (placed before `assignments`):
- `--config PATH`: Specify custom configuration file
- `--assignment-root PATH`: Specify assignment root directory

**Group-Level Options** (placed after `assignments`, before `orchestrate`):
- `--dry-run`: Preview operations without execution
- `--verbose`: Enable detailed output
- `--help`: Show command help

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

### `classroom-pilot assignments check-classroom`

Check if the classroom repository is ready for student updates.

```bash
# Basic classroom status check
classroom-pilot assignments check-classroom

# Check with verbose output (group-level option)
classroom-pilot assignments --verbose check-classroom

# Dry run to preview the check (group-level option)
classroom-pilot assignments --dry-run check-classroom

# With custom configuration
classroom-pilot --config classroom.conf assignments check-classroom
```

**Group-Level Options** (placed after `assignments`, before `check-classroom`):
- `--verbose`: Enable detailed logging
- `--dry-run`: Preview check without execution
- `--help`: Show command help

This command verifies that the classroom repository is accessible and compares its state with the template repository to ensure it's ready for student assistance operations.

### `classroom-pilot assignments check-repository-access`

Check repository access status for a specific user.

```bash
# Interactive selection from student-repos.txt
classroom-pilot assignments check-repository-access

# Check specific repository
classroom-pilot assignments check-repository-access \
  https://github.com/org/assignment-student123

# Check with explicit username
classroom-pilot assignments check-repository-access \
  https://github.com/org/assignment-student123 student123

# Verbose output for debugging (group-level option)
classroom-pilot assignments --verbose check-repository-access

# Dry run to preview check (group-level option)
classroom-pilot assignments --dry-run check-repository-access
```

**Group-Level Options** (placed after `assignments`, before `check-repository-access`):
- `--verbose`: Enable detailed logging
- `--dry-run`: Preview check without execution
- `--help`: Show command help

**Command Options:**
- `--file PATH`: File containing student repository URLs (default: student-repos.txt)
- `--config PATH`: Configuration file path (default: assignment.conf)

This command checks whether a user has proper access to a repository, including collaborator status and pending invitations.

### `classroom-pilot assignments cycle-collaborator`

Cycle collaborator permissions for a specific repository.

```bash
# Interactive selection from student-repos.txt
classroom-pilot assignments cycle-collaborator

# Cycle specific repository
classroom-pilot assignments cycle-collaborator \
  https://github.com/org/repo-student123

# Cycle with explicit username
classroom-pilot assignments cycle-collaborator \
  https://github.com/org/repo student123

# Force permission cycle without prompts
classroom-pilot assignments cycle-collaborator \
  https://github.com/org/repo student123 --force

# Verbose output (group-level option)
classroom-pilot assignments --verbose cycle-collaborator

# Dry run to preview operation (group-level option)
classroom-pilot assignments --dry-run cycle-collaborator
```

**Group-Level Options** (placed after `assignments`, before `cycle-collaborator`):
- `--verbose`: Enable detailed logging
- `--dry-run`: Preview operation without execution
- `--help`: Show command help

**Command Options:**
- `--force`: Force operation without interactive prompts
- `--file PATH`: File containing student repository URLs (default: student-repos.txt)
- `--config PATH`: Configuration file path (default: assignment.conf)

This command removes and re-adds a collaborator to refresh their repository permissions.

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
