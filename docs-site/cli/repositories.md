# Repository Commands

Repository commands provide comprehensive tools for managing student repositories in GitHub Classroom assignments.

## Overview

Repository management includes fetching student repositories, managing collaborators, and performing bulk operations across multiple repositories.

## Commands

### `classroom-pilot repos fetch`

Fetch and clone student repositories for an assignment.

```bash
# Fetch all student repositories
classroom-pilot repos fetch

# Fetch for specific assignment
classroom-pilot repos fetch --assignment "homework-01"

# Fetch to specific directory
classroom-pilot repos fetch --output-dir ./student-repos

# Fetch with filtering
classroom-pilot repos fetch --students student-list.txt
```

**Options:**
- `--assignment NAME`: Target specific assignment
- `--output-dir PATH`: Directory to clone repositories (default: current)
- `--students FILE`: File containing list of student usernames
- `--parallel COUNT`: Number of parallel fetch operations (default: 5)
- `--depth COUNT`: Git clone depth (default: full history)
- `--branch NAME`: Specific branch to fetch (default: main)

### `classroom-pilot repos list`

List repositories for an assignment with detailed information.

```bash
# List all repositories
classroom-pilot repos list

# List for specific assignment
classroom-pilot repos list --assignment "homework-01"

# List with detailed information
classroom-pilot repos list --detailed

# Export to file
classroom-pilot repos list --output repos.json --format json
```

**Options:**
- `--assignment NAME`: Filter by assignment
- `--detailed`: Include repository statistics
- `--format FORMAT`: Output format (table, json, yaml, csv)
- `--output FILE`: Save to file
- `--status STATUS`: Filter by repository status

### `classroom-pilot repos collaborator`

Manage repository collaborators and permissions.

```bash
# Add collaborator to all repositories
classroom-pilot repos collaborator add --user teaching-assistant

# Remove collaborator
classroom-pilot repos collaborator remove --user old-ta

# List collaborators
classroom-pilot repos collaborator list

# Cycle collaborators (advanced operation)
classroom-pilot repos collaborator cycle
```

**Subcommands:**
- `add`: Add collaborator to repositories
- `remove`: Remove collaborator from repositories
- `list`: List current collaborators
- `cycle`: Rotate collaborator assignments

**Options:**
- `--user USERNAME`: GitHub username
- `--permission LEVEL`: Permission level (read, write, admin)
- `--assignment NAME`: Target specific assignment
- `--dry-run`: Preview changes without execution

### `classroom-pilot repos sync`

Synchronize local repositories with remote changes.

```bash
# Sync all repositories
classroom-pilot repos sync

# Sync specific assignment
classroom-pilot repos sync --assignment "homework-01"

# Sync with specific branch
classroom-pilot repos sync --branch main

# Force sync (reset local changes)
classroom-pilot repos sync --force
```

**Options:**
- `--assignment NAME`: Target specific assignment
- `--branch NAME`: Branch to sync (default: main)
- `--force`: Reset local changes
- `--parallel COUNT`: Parallel sync operations
- `--timeout SECONDS`: Operation timeout

### `classroom-pilot repos status`

Check status of repository operations and health.

```bash
# Check all repository status
classroom-pilot repos status

# Check specific assignment
classroom-pilot repos status --assignment "homework-01"

# Health check with validation
classroom-pilot repos status --health-check

# Generate status report
classroom-pilot repos status --report status.html
```

**Options:**
- `--assignment NAME`: Target specific assignment
- `--health-check`: Perform repository validation
- `--report FILE`: Generate HTML report
- `--format FORMAT`: Output format

### `classroom-pilot repos execute`

Execute commands across multiple repositories.

```bash
# Run command in all repositories
classroom-pilot repos execute --command "git status"

# Run script across repositories
classroom-pilot repos execute --script update-dependencies.sh

# Execute with filtering
classroom-pilot repos execute \
  --command "npm test" \
  --assignment "final-project" \
  --filter "package.json"
```

**Options:**
- `--command CMD`: Command to execute
- `--script FILE`: Script file to run
- `--assignment NAME`: Target assignment
- `--filter PATTERN`: Filter repositories by file pattern
- `--parallel COUNT`: Parallel execution
- `--timeout SECONDS`: Command timeout

## Configuration

Repository commands use configuration for GitHub access and organization settings:

```yaml
# repository.conf
github:
  organization: "my-classroom-org"
  token: "${GITHUB_TOKEN}"
  api_url: "https://api.github.com"

repositories:
  clone_depth: 1
  parallel_operations: 5
  timeout_seconds: 300
  default_branch: "main"

assignments:
  prefix_pattern: "{assignment}-{username}"
  base_directory: "./student-work"
```

## Integration

Repository commands integrate with:

- **[Assignment Commands](assignments.md)**: Assignment lifecycle management
- **[Secret Management](secrets.md)**: Repository secret distribution
- **[Automation](automation.md)**: Scheduled repository operations

## Examples

### Fetch and Setup Student Repositories

```bash
# 1. Fetch all student repositories
classroom-pilot repos fetch \
  --assignment "midterm-project" \
  --output-dir ./midterm-submissions \
  --parallel 10

# 2. Check repository status
classroom-pilot repos status \
  --assignment "midterm-project" \
  --health-check

# 3. Add grading collaborator
classroom-pilot repos collaborator add \
  --user grading-assistant \
  --permission write \
  --assignment "midterm-project"
```

### Bulk Repository Operations

```bash
# Execute tests across all repositories
classroom-pilot repos execute \
  --assignment "lab-03" \
  --command "npm test" \
  --parallel 5 \
  --timeout 60

# Update dependencies in all repositories
classroom-pilot repos execute \
  --assignment "lab-03" \
  --script ./scripts/update-deps.sh \
  --filter "package.json"

# Generate status report
classroom-pilot repos status \
  --assignment "lab-03" \
  --report lab-03-status.html
```

### Repository Maintenance

```bash
# Sync all repositories with latest changes
classroom-pilot repos sync \
  --assignment "ongoing-project" \
  --branch development

# Clean up old collaborators
classroom-pilot repos collaborator remove \
  --user former-ta \
  --assignment "spring-2024"

# Validate repository health
classroom-pilot repos status \
  --health-check \
  --report health-check.html
```

## Advanced Operations

### Collaborator Cycling

The collaborator cycle feature automatically rotates grading responsibilities:

```bash
# Setup collaborator cycling
classroom-pilot repos collaborator cycle \
  --assignment "weekly-labs" \
  --collaborators ta1,ta2,ta3 \
  --strategy round-robin

# Manual cycle trigger
classroom-pilot repos collaborator cycle \
  --assignment "weekly-labs" \
  --next
```

### Repository Filtering

Filter repositories for targeted operations:

```bash
# Filter by file presence
classroom-pilot repos execute \
  --command "npm test" \
  --filter "package.json"

# Filter by student list
classroom-pilot repos fetch \
  --students advanced-students.txt \
  --assignment "bonus-project"

# Filter by repository status
classroom-pilot repos list \
  --status "needs-review" \
  --format table
```

## Troubleshooting

### Common Issues

**Authentication Problems:**
```bash
# Verify GitHub token
classroom-pilot auth check

# Test API access
classroom-pilot repos list --assignment "test"
```

**Clone Failures:**
```bash
# Fetch with verbose output
classroom-pilot repos fetch \
  --assignment "homework-01" \
  --verbose \
  --timeout 300

# Check repository permissions
classroom-pilot repos status --health-check
```

**Collaborator Issues:**
```bash
# List current collaborators
classroom-pilot repos collaborator list \
  --assignment "homework-01"

# Verify permissions
classroom-pilot repos collaborator list \
  --detailed \
  --format json
```

### Performance Optimization

```bash
# Increase parallel operations
classroom-pilot repos fetch \
  --parallel 20 \
  --depth 1

# Use shallow clones for faster operations
classroom-pilot repos fetch \
  --depth 1 \
  --branch main

# Set appropriate timeouts
classroom-pilot repos execute \
  --command "long-running-task" \
  --timeout 600
```

## Best Practices

1. **Repository Management**:
   - Use shallow clones for faster operations
   - Implement parallel processing for bulk operations
   - Regular health checks to maintain repository integrity

2. **Collaborator Management**:
   - Document collaborator responsibilities
   - Use automated cycling for fair distribution
   - Regular cleanup of inactive collaborators

3. **Security**:
   - Limit repository access permissions
   - Use tokens with minimal required scopes
   - Regular permission audits

4. **Performance**:
   - Optimize parallel operation counts
   - Use appropriate timeout values
   - Monitor resource usage during bulk operations

## See Also

- [Assignment Commands](assignments.md)
- [Secret Management](secrets.md)
- [Automation Commands](automation.md)
- [Configuration Guide](../getting-started/configuration.md)
