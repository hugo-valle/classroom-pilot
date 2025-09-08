# Automated Cron Workflow Documentation

## Overview

The GitHub Classroom Tools include comprehensive cron job automation for flexible, unattended assignment management. This enhanced system allows you to schedule any combination of workflow steps (sync, secrets, cycle, discover, assist) with custom schedules tailored to your needs.

## Features

### 🕐 Flexible Scheduling
- **Individual steps**: Schedule each workflow step independently
- **Multiple steps**: Combine multiple steps in a single cron job
- **Custom schedules**: Override default schedules with cron expressions
- **Intelligent defaults**: Pre-configured schedules optimized for each step type

### 🔄 Multi-Step Operations
- **Template synchronization** (`sync`): Pushes template changes to GitHub Classroom
- **Repository discovery** (`discover`): Finds new student repositories
- **Secret management** (`secrets`): Distributes and updates tokens across repositories
- **Student assistance** (`assist`): Automated conflict resolution and help
- **Access management** (`cycle`): Fixes repository permission issues

### 📊 Enhanced Monitoring & Logging
- **Step-by-step logging**: Individual success/failure reporting for each step
- **Consolidated logs**: All workflow activities in a single log file
- **Log rotation**: Automatic rotation when logs exceed 10MB
- **Status monitoring**: Easy commands to check all installed cron jobs
- **Error tracking**: Comprehensive error reporting with step isolation

## Scripts

### 1. `cron-sync.sh`
**Purpose**: Enhanced automation script supporting multi-step workflow execution

**Features**:
- **Multi-step execution**: Execute multiple workflow steps in sequence
- **Step validation**: Validates each step name against allowed values
- **Individual error handling**: Step failures don't prevent other steps from running
- **Comprehensive logging**: Step-by-step execution reporting
- **Backward compatibility**: Still works with single sync step for legacy setups

**Usage**:
```bash
# Single step execution
./scripts/cron-sync.sh assignment.conf sync

# Multiple steps execution
./scripts/cron-sync.sh assignment.conf sync secrets cycle

# Default behavior (sync only for backward compatibility)
./scripts/cron-sync.sh assignment.conf
```

**Logging**: All output is logged to `tools/generated/cron-workflow.log`

### 2. `manage-cron.sh`
**Purpose**: Enhanced cron job management utility with flexible scheduling

**Commands**:
```bash
# Install sync job with default schedule (every 4 hours)
./scripts/manage-cron.sh install sync

# Install secrets management with default schedule (daily at 2 AM)
./scripts/manage-cron.sh install secrets

# Install multiple steps with default schedule (daily at 1 AM)
./scripts/manage-cron.sh install "sync secrets cycle"

# Install with custom schedule
./scripts/manage-cron.sh install cycle "0 6 * * 0"

# View default schedules for all steps
./scripts/manage-cron.sh list-schedules

# Check status of all installed jobs
./scripts/manage-cron.sh status

# View recent workflow logs
./scripts/manage-cron.sh logs

# Remove specific cron job
./scripts/manage-cron.sh remove secrets

# Remove all assignment cron jobs
./scripts/manage-cron.sh remove all

# Show help with all options
./scripts/manage-cron.sh help
```

## Default Schedules

The system provides intelligent default schedules for each workflow step:

| Step         | Default Schedule         | Description              | Cron Expression |
| ------------ | ------------------------ | ------------------------ | --------------- |
| **sync**     | Every 4 hours            | Template synchronization | `0 */4 * * *`   |
| **discover** | Daily at 1 AM            | Repository discovery     | `0 1 * * *`     |
| **secrets**  | Daily at 2 AM            | Secret management        | `0 2 * * *`     |
| **assist**   | Weekly on Sunday at 3 AM | Student assistance       | `0 3 * * 0`     |
| **cycle**    | Weekly on Sunday at 6 AM | Access management        | `0 6 * * 0`     |

## Installation

### Prerequisites
1. **Working assignment setup**: Ensure `assignment.conf` is properly configured
2. **GitHub access**: Verify GitHub CLI authentication and repository access
3. **Clean repository**: Commit any pending changes before installation

### Quick Setup Examples

#### Basic Sync Automation
```bash
# Navigate to assignment root
cd /path/to/your/assignment

# Install sync job (every 4 hours)
./tools/scripts/manage-cron.sh install sync

# Verify installation
./tools/scripts/manage-cron.sh status
```

#### Comprehensive Automation
```bash
# Install multiple workflow steps
./tools/scripts/manage-cron.sh install "sync discover secrets"

# Install access management (weekly)
./tools/scripts/manage-cron.sh install cycle

# Check all installed jobs
./tools/scripts/manage-cron.sh status
```

#### Custom Scheduling
```bash
# Sync every 2 hours instead of 4
./tools/scripts/manage-cron.sh install sync "0 */2 * * *"

# Secrets management twice daily
./tools/scripts/manage-cron.sh install secrets "0 2,14 * * *"

# Multiple steps with custom schedule
./tools/scripts/manage-cron.sh install "sync cycle" "0 6 * * 1"  # Mondays at 6 AM
```

### Verification
After installation, you can verify the cron jobs are working:

```bash
# Check current status of all jobs
./tools/scripts/manage-cron.sh status

# Monitor logs in real-time
tail -f tools/generated/cron-workflow.log

# Test manual execution with specific steps
./tools/scripts/cron-sync.sh assignment.conf sync secrets

# View default schedules
./tools/scripts/manage-cron.sh list-schedules
```

## Configuration

### Assignment Configuration
The cron workflow uses your existing `assignment.conf` file. Ensure these settings are configured:

```bash
# Required for all operations
CLASSROOM_URL="https://classroom.github.com/classrooms/ID/assignments/NAME"
TEMPLATE_REPO_URL="https://github.com/ORG/assignment-template"
GITHUB_ORGANIZATION="YOUR-ORG"

# Step controls (all steps can be enabled for cron automation)
STEP_SYNC_TEMPLATE=true
STEP_DISCOVER_REPOS=true
STEP_MANAGE_SECRETS=true      # Can be enabled for automated secret management
STEP_ASSIST_STUDENTS=false    # Usually disabled for cron (manual intervention)
STEP_CYCLE_COLLABORATORS=true # Can be enabled for automated access fixes

# Secret configuration for automated management
SECRETS=(
    "INSTRUCTOR_TESTS_TOKEN:instructor_token.txt:Token for accessing instructor tests"
)
```

### Multiple Cron Job Configuration
The system now supports multiple independent cron jobs with different schedules:

```bash
# Example: Comprehensive automation setup
./scripts/manage-cron.sh install sync "0 */4 * * *"      # Every 4 hours
./scripts/manage-cron.sh install secrets "0 2 * * *"     # Daily at 2 AM
./scripts/manage-cron.sh install cycle "0 6 * * 0"       # Weekly on Sunday
```

Example crontab entries:
```cron
# GitHub Classroom Assignment Auto-sync
0 */4 * * * /path/to/cron-sync.sh '/path/to/assignment.conf' sync >/dev/null 2>&1

# GitHub Classroom Assignment Auto-secrets  
0 2 * * * /path/to/cron-sync.sh '/path/to/assignment.conf' secrets >/dev/null 2>&1

# GitHub Classroom Assignment Auto-cycle
0 6 * * 0 /path/to/cron-sync.sh '/path/to/assignment.conf' cycle >/dev/null 2>&1
```

## Monitoring

### Log Files
- **Location**: `tools/generated/cron-workflow.log`
- **Format**: Timestamped entries with step-by-step operation details
- **Rotation**: Automatic when file exceeds 10MB
- **Retention**: Old logs saved as `.old` files

### Status Checking
```bash
# Quick status check of all jobs
./tools/scripts/manage-cron.sh status

# Recent activity across all workflows
./tools/scripts/manage-cron.sh logs

# Real-time monitoring
tail -f tools/generated/cron-workflow.log

# Check specific step schedules
./tools/scripts/manage-cron.sh list-schedules
```

### Common Log Entries
```bash
# Multi-step execution
[2025-09-08 14:59:08] INFO: Starting automated workflow job
[2025-09-08 14:59:08] INFO: Executing steps: sync secrets cycle
[2025-09-08 14:59:08] INFO: Executing step: sync
[2025-09-08 14:59:15] SUCCESS: Step 'sync' completed successfully
[2025-09-08 14:59:15] INFO: Executing step: secrets
[2025-09-08 14:59:20] SUCCESS: Step 'secrets' completed successfully
[2025-09-08 14:59:20] INFO: Executing step: cycle
[2025-09-08 14:59:25] SUCCESS: Step 'cycle' completed successfully
[2025-09-08 14:59:25] SUCCESS: All workflow steps completed successfully

# Error conditions
[2025-09-08 15:00:01] ERROR: Invalid step name: invalid
[2025-09-08 15:00:01] ERROR: Step 'secrets' failed with exit code: 1
[2025-09-08 15:00:01] WARNING: Some workflow steps failed - check log for details
```

## Workflow Step Details

Each workflow step performs specific operations when executed via cron:

### sync
- Synchronizes template repository with GitHub Classroom
- Updates classroom repository with latest template changes
- Ensures all students get template updates

### discover  
- Scans GitHub organization for new student repositories
- Updates batch files with current repository list
- Prepares data for other automated steps

### secrets
- Distributes instructor tokens to student repositories
- Updates expired secrets based on age policies
- Manages multiple secret types automatically

### assist
- Provides automated help for common student issues
- Resolves merge conflicts where possible
- Usually requires manual review, limited cron usage

### cycle
- Fixes repository access permission issues
- Cycles collaborator permissions to resolve GitHub Classroom glitches
- Ensures students maintain proper repository access

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

# Test manual execution with specific steps
./tools/scripts/cron-sync.sh assignment.conf sync
```

#### 5. "Invalid step name" errors
**Cause**: Typo in step name or unsupported step
**Solution**:
```bash
# Check valid step names
./tools/scripts/manage-cron.sh help

# Valid steps are: sync, discover, secrets, assist, cycle
```

#### 6. Step failures in multi-step execution
**Cause**: Individual step configuration or permission issues
**Solution**:
```bash
# Test each step individually
./tools/scripts/assignment-orchestrator.sh --step sync --dry-run
./tools/scripts/assignment-orchestrator.sh --step secrets --dry-run

# Check step-specific configuration
grep "STEP_" assignment.conf
```

### Debugging
For detailed debugging, run scripts manually with verbose output:
```bash
# Test specific workflow steps
./tools/scripts/assignment-orchestrator.sh --step sync --yes --verbose
./tools/scripts/assignment-orchestrator.sh --step cycle --yes --verbose

# Test multi-step cron execution
./tools/scripts/cron-sync.sh assignment.conf sync secrets --verbose

# Check recent logs with step details
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

### Custom Schedule Examples
Create sophisticated scheduling patterns for different workflow needs:

```bash
# High-frequency sync during active assignment periods
./tools/scripts/manage-cron.sh install sync "0 */2 * * 1-5"  # Every 2 hours, weekdays

# Comprehensive daily automation
./tools/scripts/manage-cron.sh install "discover secrets" "0 1 * * *"  # Daily at 1 AM

# Weekend maintenance
./tools/scripts/manage-cron.sh install "cycle assist" "0 6 * * 0"  # Sundays at 6 AM

# Custom intervals
./tools/scripts/manage-cron.sh install secrets "0 2,14 * * *"  # Twice daily at 2 AM and 2 PM
```

### Multiple Assignment Management
Each assignment repository can have independent cron automation:

```bash
# Assignment 1 - High frequency during active period
cd /path/to/assignment1
./tools/scripts/manage-cron.sh install "sync secrets" "0 */4 * * *"

# Assignment 2 - Lower frequency maintenance
cd /path/to/assignment2  
./tools/scripts/manage-cron.sh install sync "0 8 * * *"

# Final project - Comprehensive automation
cd /path/to/final-project
./tools/scripts/manage-cron.sh install "sync discover secrets cycle" "0 6 * * *"
```

### Seasonal Automation Patterns

#### Active Assignment Period
```bash
# Frequent sync and secret management
./tools/scripts/manage-cron.sh install sync "0 */2 * * 1-5"
./tools/scripts/manage-cron.sh install secrets "0 1 * * *"
./tools/scripts/manage-cron.sh install discover "0 0 * * *"
```

#### Maintenance Period
```bash
# Remove high-frequency jobs
./tools/scripts/manage-cron.sh remove sync

# Keep basic maintenance
./tools/scripts/manage-cron.sh install "sync cycle" "0 6 * * 0"
```

### Integration with CI/CD
Enhanced cron scripts work well with automated pipelines:

```yaml
# GitHub Actions example - Multi-step workflow
- name: Run Assignment Automation
  run: |
    ./tools/scripts/cron-sync.sh assignment.conf sync secrets
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

# GitLab CI example - Scheduled pipeline
workflow_automation:
  script:
    - ./tools/scripts/cron-sync.sh assignment.conf discover cycle
  only:
    - schedules
```

## Best Practices

### 1. Testing and Validation
- **Test individual steps**: Verify each workflow step works independently
- **Test multi-step execution**: Ensure step combinations work together
- **Monitor initial deployment**: Watch logs closely for first few executions
- **Validate configuration**: Ensure all required settings are present

```bash
# Testing workflow
./tools/scripts/assignment-orchestrator.sh --step sync --dry-run
./tools/scripts/cron-sync.sh assignment.conf sync secrets --dry-run
./tools/scripts/manage-cron.sh status
```

### 2. Monitoring and Maintenance
- **Regular log review**: Check logs weekly during active periods
- **Disk space monitoring**: Prevent log files from filling disk space
- **Schedule optimization**: Adjust frequencies based on actual needs
- **Error tracking**: Set up alerts for repeated failures

```bash
# Monitoring commands
./tools/scripts/manage-cron.sh logs | grep ERROR
du -h tools/generated/cron-workflow.log
./tools/scripts/manage-cron.sh status
```

### 3. Security and Access Management
- **Token rotation**: Regularly update GitHub tokens
- **Permission validation**: Verify access to all required repositories
- **Log security**: Ensure logs don't contain sensitive information
- **Cleanup**: Remove cron jobs when assignments complete

```bash
# Security maintenance
gh auth status
./tools/scripts/add-secrets-to-students.sh --check-token
./tools/scripts/manage-cron.sh remove all  # When assignment ends
```
### 4. Documentation and Change Management
- **Document schedules**: Record custom cron schedules for team members
- **Track changes**: Record any configuration or schedule modifications
- **Backup configurations**: Maintain backup of working configurations
- **Team communication**: Share cron setup with other instructors

```bash
# Documentation commands
./tools/scripts/manage-cron.sh status > cron-setup.txt
./tools/scripts/manage-cron.sh list-schedules >> cron-setup.txt
```

## Related Documentation

- [Assignment Orchestrator](ASSIGNMENT-ORCHESTRATOR.md) - Main workflow documentation with 5-step process
- [Cycle Collaborator](CYCLE-COLLABORATOR.md) - Repository access fix automation
- [Automation Suite](AUTOMATION-SUITE.md) - Complete automation overview
- [Secrets Management](SECRETS-MANAGEMENT.md) - Token and secrets handling
- [Changelog](CHANGELOG.md) - Recent changes and version history

## Support

For issues with cron automation:

1. **Check logs**: `./tools/scripts/manage-cron.sh logs`
2. **Verify status**: `./tools/scripts/manage-cron.sh status`
3. **Test individual steps**: `./tools/scripts/assignment-orchestrator.sh --step [step] --dry-run`
4. **Test multi-step execution**: `./tools/scripts/cron-sync.sh assignment.conf sync secrets`
5. **Review step schedules**: `./tools/scripts/manage-cron.sh list-schedules`
6. **Check configuration**: Ensure `assignment.conf` has all required settings
7. **Verify GitHub access**: Confirm authentication and repository permissions

### Quick Diagnostic Commands
```bash
# Comprehensive status check
./tools/scripts/manage-cron.sh status

# Recent activity review
./tools/scripts/manage-cron.sh logs | tail -20

# Test specific workflow step
./tools/scripts/assignment-orchestrator.sh --step cycle --dry-run --verbose

# Validate all steps individually
for step in sync discover secrets cycle; do
    echo "Testing $step..."
    ./tools/scripts/assignment-orchestrator.sh --step $step --dry-run
done
```

For additional help, see the main [README.md](../README.md) or create an issue in the repository.
