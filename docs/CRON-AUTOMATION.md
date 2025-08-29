# Automated Cron Sync Documentation

## Overview

The GitHub Classroom Tools now include comprehensive cron job automation for unattended assignment management. This system automatically synchronizes your template repository with GitHub Classroom and distributes tokens to student repositories as they accept assignments.

## Features

### 🕐 Automated Scheduling
- **Schedule**: Runs every 4 hours (00:00, 04:00, 08:00, 12:00, 16:00, 20:00)
- **Non-interactive**: No user prompts or manual intervention required
- **Background operation**: Runs silently with comprehensive logging

### 🔄 Sync Operations
- **Template synchronization**: Automatically pushes template changes to GitHub Classroom
- **Token distribution**: Distributes instructor tokens to student repositories
- **Repository discovery**: Continuously monitors for new student repositories
- **Error recovery**: Handles temporary failures and continues operation

### 📊 Monitoring & Logging
- **Detailed logs**: Timestamped entries for all operations
- **Log rotation**: Automatic rotation when logs exceed 10MB
- **Status monitoring**: Easy commands to check job health
- **Error tracking**: Comprehensive error reporting and debugging information

## Scripts

### 1. `cron-sync.sh`
**Purpose**: Main automation script designed for cron execution

**Features**:
- Non-interactive execution with comprehensive error handling
- Automatic log management and rotation
- Configuration validation and environment setup
- Integration with existing orchestrator workflow

**Usage**:
```bash
# Direct execution (for testing)
./scripts/cron-sync.sh

# With custom config
./scripts/cron-sync.sh /path/to/custom.conf
```

**Logging**: All output is logged to `tools/generated/cron-sync.log`

### 2. `manage-cron.sh`
**Purpose**: User-friendly cron job management utility

**Commands**:
```bash
# Install 4-hour sync job
./scripts/manage-cron.sh install

# Check installation status
./scripts/manage-cron.sh status

# View recent sync logs
./scripts/manage-cron.sh logs

# Remove cron job
./scripts/manage-cron.sh remove

# Show help
./scripts/manage-cron.sh help
```

## Installation

### Prerequisites
1. **Working assignment setup**: Ensure `assignment.conf` is properly configured
2. **GitHub access**: Verify GitHub CLI authentication and repository access
3. **Clean repository**: Commit any pending changes before installation

### Quick Setup
```bash
# Navigate to assignment root
cd /path/to/your/assignment

# Install the cron job
./tools/scripts/manage-cron.sh install

# Verify installation
./tools/scripts/manage-cron.sh status
```

### Verification
After installation, you can verify the cron job is working:

```bash
# Check current status
./tools/scripts/manage-cron.sh status

# Monitor logs in real-time
tail -f tools/generated/cron-sync.log

# Test manual execution
./tools/scripts/cron-sync.sh
```

## Configuration

### Assignment Configuration
The cron sync uses your existing `assignment.conf` file. Ensure these settings are configured:

```bash
# Required for sync operations
CLASSROOM_REPO_URL="https://github.com/ORG/classroom-semester-assignment"
TEMPLATE_REPO_URL="https://github.com/ORG/assignment-template"

# Optional: Control which steps run automatically
STEP_SYNC_TEMPLATE=true
STEP_DISCOVER_REPOS=true
STEP_MANAGE_SECRETS=false  # Usually disabled for cron
STEP_ASSIST_STUDENTS=false # Usually disabled for cron
```

### Cron Configuration
The default cron schedule is every 4 hours:
```cron
# GitHub Classroom Assignment Auto-Sync
0 */4 * * * /path/to/cron-sync.sh '/path/to/assignment.conf' >/dev/null 2>&1
```

To customize the schedule, edit your crontab manually:
```bash
crontab -e
```

## Monitoring

### Log Files
- **Location**: `tools/generated/cron-sync.log`
- **Format**: Timestamped entries with operation details
- **Rotation**: Automatic when file exceeds 10MB
- **Retention**: Old logs saved as `.old` files

### Status Checking
```bash
# Quick status check
./tools/scripts/manage-cron.sh status

# Recent activity
./tools/scripts/manage-cron.sh logs

# Real-time monitoring
tail -f tools/generated/cron-sync.log
```

### Common Log Entries
```bash
# Successful sync
[2025-08-29 12:00:01] INFO: Starting automated sync job
[2025-08-29 12:00:05] SUCCESS: Sync completed successfully

# Error conditions
[2025-08-29 12:00:01] ERROR: Configuration file not found
[2025-08-29 12:00:01] ERROR: Sync failed with exit code: 1
```

## Troubleshooting

### Common Issues

#### 1. "Configuration file not found"
**Cause**: Missing or incorrect path to `assignment.conf`
**Solution**: 
```bash
# Verify config file exists
ls -la assignment.conf

# Check cron job path
./tools/scripts/manage-cron.sh status
```

#### 2. "Template synchronization failed"
**Cause**: Usually uncommitted changes in repository
**Solution**:
```bash
# Check for uncommitted changes
git status

# Commit or stash changes
git add . && git commit -m "Update for cron sync"
```

#### 3. "Permission denied" errors
**Cause**: Script permissions or GitHub authentication issues
**Solution**:
```bash
# Fix script permissions
chmod +x tools/scripts/cron-sync.sh
chmod +x tools/scripts/manage-cron.sh

# Test GitHub access
gh auth status
```

#### 4. Cron job not running
**Cause**: Cron service issues or path problems
**Solution**:
```bash
# Check cron service
sudo systemctl status cron

# Verify cron job installation
./tools/scripts/manage-cron.sh status

# Test manual execution
./tools/scripts/cron-sync.sh
```

### Debugging
For detailed debugging, run the sync script manually:
```bash
# Enable verbose output
./tools/scripts/assignment-orchestrator.sh --step sync --yes --verbose

# Check recent logs
./tools/scripts/manage-cron.sh logs
```

## Security Considerations

### Secrets Management
- **Automatic secrets**: Disabled by default in cron mode for security
- **Token access**: Ensure GitHub CLI has appropriate repository permissions
- **Log security**: Logs may contain repository URLs but not sensitive tokens

### Repository Access
- **Authentication**: Uses existing GitHub CLI authentication
- **Permissions**: Requires push access to classroom repository
- **Scope**: Only accesses repositories defined in configuration

## Advanced Usage

### Custom Schedules
Modify the cron schedule for different frequencies:

```bash
# Every 2 hours
0 */2 * * * /path/to/cron-sync.sh

# Daily at 2 AM
0 2 * * * /path/to/cron-sync.sh

# Weekdays only, every 4 hours
0 */4 * * 1-5 /path/to/cron-sync.sh
```

### Multiple Assignments
For managing multiple assignments, install separate cron jobs:

```bash
# Assignment 1
0 */4 * * * /path/to/assignment1/tools/scripts/cron-sync.sh

# Assignment 2  
30 */4 * * * /path/to/assignment2/tools/scripts/cron-sync.sh
```

### Integration with CI/CD
The cron scripts can be integrated with CI/CD pipelines:

```yaml
# GitHub Actions example
- name: Sync Assignment
  run: ./tools/scripts/cron-sync.sh
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Best Practices

### 1. Testing
- Always test manual execution before installing cron job
- Monitor logs during initial deployment
- Verify GitHub access and permissions

### 2. Monitoring
- Check logs regularly during assignment periods
- Set up alerts for persistent failures
- Monitor disk space usage for log files

### 3. Maintenance
- Update cron jobs when moving assignment repositories
- Remove cron jobs when assignments are complete
- Keep assignment configuration files up to date

### 4. Documentation
- Document custom cron schedules for team members
- Record any configuration changes
- Maintain backup of working configurations

## Related Documentation

- [Assignment Orchestrator](ASSIGNMENT-ORCHESTRATOR.md) - Main workflow documentation
- [Automation Suite](AUTOMATION-SUITE.md) - Complete automation overview
- [Secrets Management](SECRETS-MANAGEMENT.md) - Token and secrets handling
- [Changelog](CHANGELOG.md) - Recent changes and version history

## Support

For issues with cron automation:

1. **Check logs**: `./tools/scripts/manage-cron.sh logs`
2. **Verify status**: `./tools/scripts/manage-cron.sh status`
3. **Test manually**: `./tools/scripts/cron-sync.sh`
4. **Review configuration**: Ensure `assignment.conf` is correct
5. **Check GitHub access**: Verify authentication and permissions

For additional help, see the main [README.md](../README.md) or create an issue in the repository.
