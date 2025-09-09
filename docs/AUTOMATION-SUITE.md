# CS6600 Instructor Automation Suite

This document describes the complete automation suite for managing CS6600 assignments, including repository discovery, secret management, and student assistance tools.

## 🎯 Overview

The automation suite provides instructors with powerful tools to:
- Automatically discover student repositories from GitHub Classroom
- Manage GitHub secrets across multiple student repositories
- Assist students with repository updates and conflict resolution
- Fix repository access issues through intelligent permission cycling
- Handle template repository updates and deployment

## 📋 Quick Start

### 1. Setup Requirements
```bash
# Install GitHub CLI
# See: https://cli.github.com/

# Authenticate with GitHub
gh auth login

# Create token file for secret management
echo "your_github_token_here" > instructor_token.txt
```

### 2. Discover Student Repositories
```bash
# Fetch all student repositories (excludes template by default)
./scripts/fetch-student-repos.sh

# Include template repository if needed
./scripts/fetch-student-repos.sh --include-template

# Custom assignment and organization
./scripts/fetch-student-repos.sh cs6600-m2-homework2 MY-ORG
```

### 3. Manage Secrets Across All Students
```bash
# Add secrets to all discovered students
./scripts/add-secrets-to-students.sh INSTRUCTOR_TESTS_TOKEN --batch student-repos-batch.txt

# Force update all secrets (regardless of age)
./scripts/add-secrets-to-students.sh INSTRUCTOR_TESTS_TOKEN --force-update --batch student-repos-batch.txt
```

### 4. Assist Students with Updates
```bash
# Help specific student
./scripts/student-update-helper.sh https://github.com/WSU-ML-DL/cs6600-m1-homework1-student123

# Help all students from discovered list
./scripts/student-update-helper.sh --batch student-repos-batch.txt
```

### 5. Fix Repository Access Issues
```bash
# Check and fix repository access for all students
./scripts/cycle-collaborator.sh --config assignment.conf --batch student-repos-batch.txt --repo-urls

# Preview what would be done first
./scripts/cycle-collaborator.sh --config assignment.conf --batch student-repos-batch.txt --repo-urls --dry-run
```

## 🛠️ Complete Automation Scripts

### 1. Repository Discovery Script

**File:** `scripts/fetch-student-repos.sh`

**Purpose:** Automatically discover and list all student repositories from GitHub Classroom.

**Key Features:**
- Auto-detects student repositories with pattern matching
- Excludes template repositories by default
- Supports custom organizations and assignment prefixes
- Generates batch files for other scripts
- Dry-run support for preview

**Usage Examples:**
```bash
# Basic usage - discover all cs6600-m1-homework1 repositories
./scripts/fetch-student-repos.sh

# Dry run to preview results
./scripts/fetch-student-repos.sh --dry-run

# Include template repository
./scripts/fetch-student-repos.sh --include-template

# Custom assignment
./scripts/fetch-student-repos.sh cs6600-final-project

# Custom output file
./scripts/fetch-student-repos.sh --output final-project-repos.txt

# Custom organization and assignment
./scripts/fetch-student-repos.sh cs6600-m2-homework2 CUSTOM-ORG
```

**Output Format:**
```
# Student Repository URLs for cs6600-m1-homework1
# Generated on Mon Aug 18 12:55:41 MDT 2025
# Organization: WSU-ML-DL
# Total repositories: 2
#
# Use this file with batch scripts:
# ./scripts/add-secrets-to-students.sh INSTRUCTOR_TESTS_TOKEN --batch student-repos-final.txt
# ./scripts/student-update-helper.sh --batch student-repos-final.txt

https://github.com/WSU-ML-DL/cs6600-m1-homework1-hugo-wsu
https://github.com/WSU-ML-DL/cs6600-m1-homework1-instructor-tests
```

### 2. Secret Management Script

**File:** `scripts/add-secrets-to-students.sh`

**Purpose:** Automated GitHub secrets management with expiration detection and batch processing.

**Key Features:**
- Token validation (format, permissions, accessibility)
- Secret age detection and expiration management
- Batch processing from repository files
- Force update capabilities
- Comprehensive error handling and logging

**Usage Examples:**
```bash
# Add secret to specific student
./scripts/add-secrets-to-students.sh INSTRUCTOR_TESTS_TOKEN https://github.com/WSU-ML-DL/cs6600-m1-homework1-student123

# Batch process all students
./scripts/add-secrets-to-students.sh INSTRUCTOR_TESTS_TOKEN --batch student-repos-batch.txt

# Use custom token file
./scripts/add-secrets-to-students.sh INSTRUCTOR_TESTS_TOKEN --token-file custom_token.txt

# Update secrets older than 30 days
./scripts/add-secrets-to-students.sh INSTRUCTOR_TESTS_TOKEN --max-age 30 --batch student-repos-batch.txt

# Force update all secrets regardless of age
./scripts/add-secrets-to-students.sh INSTRUCTOR_TESTS_TOKEN --force-update --batch student-repos-batch.txt

# Check token validity
./scripts/add-secrets-to-students.sh --check-token
```

**Secret Age Management:**
- Default expiration: 90 days
- Configurable with `--max-age` parameter
- Force update with `--force-update`
- Automatic detection of existing secret age

### 3. Student Update Helper Script

**File:** `scripts/student-update-helper.sh`

**Purpose:** Assists students with repository updates and merge conflict resolution.

**Key Features:**
- Automated merge conflict detection and resolution
- Template update assistance
- Batch processing for multiple students
- Safe update procedures with backup strategies
- Educational guidance for students

**Usage Examples:**
```bash
# Help specific student
./scripts/student-update-helper.sh https://github.com/WSU-ML-DL/cs6600-m1-homework1-student123

# Help all students from file
./scripts/student-update-helper.sh --batch student-repos-batch.txt

# Use custom template repository
./scripts/student-update-helper.sh --template https://github.com/CUSTOM/template-repo student-repo-url
```

### 4. Collaborator Cycling Script

**File:** `scripts/cycle-collaborator.sh`

**Purpose:** Fixes student repository access issues by cycling collaborator permissions.

**Key Features:**
- Intelligent detection of repository access problems
- Smart cycling logic (only cycles when needed)
- Force mode for manual override when troubleshooting
- Configuration-based integration with orchestrator
- Repository URL processing for batch operations
- Comprehensive access verification and reporting

**Usage Examples:**
```bash
# Check and fix access for specific student (traditional mode)
./scripts/cycle-collaborator.sh assignment1 student-username organization

# Configuration mode with batch processing (recommended)
./scripts/cycle-collaborator.sh --config assignment.conf --batch student-repos.txt --repo-urls

# Force cycling even when access appears correct
./scripts/cycle-collaborator.sh --config assignment.conf --batch student-repos.txt --repo-urls --force

# Dry run to preview actions
./scripts/cycle-collaborator.sh --config assignment.conf --batch student-repos.txt --repo-urls --dry-run

# List repository status without making changes
./scripts/cycle-collaborator.sh --list assignment1 student-username organization
```

**Intelligent Cycling Logic:**
- **Normal Mode:** Only cycles permissions when repository access issues are detected
- **Force Mode:** Cycles permissions anyway when `--force` flag is used
- **Smart Detection:** Verifies collaborator status before taking action
- **Clear Reporting:** Explains why cycling is or isn't performed

### 5. Template Deployment Script

**File:** `scripts/push-to-classroom.sh`

**Purpose:** Deploy template updates to GitHub Classroom.

**Key Features:**
- Safe deployment with backup procedures
- Branch management and conflict resolution
- Verification of successful deployment
- Rollback capabilities

## 🔄 Complete Workflow Examples

### Workflow 1: New Assignment Setup
```bash
# 1. Update template repository
git pull origin main

# 2. Deploy to classroom
./scripts/push-to-classroom.sh

# 3. Discover student repositories
./scripts/fetch-student-repos.sh

# 4. Add secrets to all students
./scripts/add-secrets-to-students.sh INSTRUCTOR_TESTS_TOKEN --batch student-repos-batch.txt

# 5. Fix any repository access issues (optional)
./scripts/cycle-collaborator.sh --config assignment.conf --batch student-repos-batch.txt --repo-urls
```

### Workflow 2: Mid-Semester Updates
```bash
# 1. Discover current student repositories
./scripts/fetch-student-repos.sh

# 2. Update expired secrets (older than 30 days)
./scripts/add-secrets-to-students.sh INSTRUCTOR_TESTS_TOKEN --max-age 30 --batch student-repos-batch.txt

# 3. Help students with any update issues
./scripts/student-update-helper.sh --batch student-repos-batch.txt

# 4. Fix any repository access issues that may have developed
./scripts/cycle-collaborator.sh --config assignment.conf --batch student-repos-batch.txt --repo-urls
```

### Workflow 3: Emergency Secret Update
```bash
# 1. Fetch current repositories
./scripts/fetch-student-repos.sh

# 2. Force update all secrets immediately
./scripts/add-secrets-to-students.sh INSTRUCTOR_TESTS_TOKEN --force-update --batch student-repos-batch.txt
```

### Workflow 4: Custom Assignment Management
```bash
# 1. Discover repositories for different assignment
./scripts/fetch-student-repos.sh cs6600-final-project MY-CUSTOM-ORG --output final-repos.txt

# 2. Manage secrets for final project
./scripts/add-secrets-to-students.sh FINAL_PROJECT_TOKEN --batch final-repos.txt

# 3. Assist students with final project updates
./scripts/student-update-helper.sh --batch final-repos.txt
```

### Workflow 5: Repository Access Troubleshooting
```bash
# 1. Discover student repositories
./scripts/fetch-student-repos.sh

# 2. Check repository access status
./scripts/cycle-collaborator.sh --config assignment.conf --batch student-repos-batch.txt --repo-urls --list

# 3. Fix any detected access issues
./scripts/cycle-collaborator.sh --config assignment.conf --batch student-repos-batch.txt --repo-urls

# 4. Force cycling for persistent issues
./scripts/cycle-collaborator.sh --config assignment.conf --batch student-repos-batch.txt --repo-urls --force
```

## 🔐 Security Features

### Token Management
- **Validation:** Automatic validation of GitHub token format (ghp_ prefix, 40+ characters)
- **Permissions:** Verification of required permissions (repo, admin:repo_hook)
- **Storage:** Secure file-based storage (git-ignored)
- **Expiration:** Detection and handling of expired tokens

### Secret Management
- **Age Tracking:** Automatic detection of secret creation/update dates
- **Expiration Policies:** Configurable expiration thresholds
- **Force Updates:** Override policies when security requires immediate updates
- **Audit Trail:** Comprehensive logging of all secret operations

### Repository Access
- **Access Verification:** Pre-flight checks for repository accessibility
- **Batch Validation:** Validation of all repositories before batch operations
- **Error Handling:** Graceful handling of access denied scenarios

## 📊 Output Management

### Clean Output Design
All scripts implement proper stdout/stderr separation:
- **stdout:** Clean data output (repository URLs, file contents)
- **stderr:** Status messages, warnings, errors, progress indicators

This design enables:
- **Piping:** Clean data can be piped to other commands
- **File Redirection:** Status messages remain visible while data is redirected
- **Script Integration:** Scripts can be composed together reliably

### File Generation
Scripts generate well-formatted files with:
- **Headers:** Metadata about generation time, parameters used
- **Comments:** Usage instructions and integration examples
- **Clean URLs:** One repository URL per line for easy processing

## 🚨 Error Handling

### Robust Error Management
- **Pre-flight Checks:** Validation before starting operations
- **Graceful Failures:** Partial success handling in batch operations
- **Informative Messages:** Clear error descriptions with resolution suggestions
- **Exit Codes:** Proper exit codes for script composition

### Common Issues and Solutions

**Issue:** GitHub CLI not authenticated
**Solution:** Run `gh auth login` and follow the prompts

**Issue:** Token permissions insufficient
**Solution:** Ensure token has 'repo' and 'admin:repo_hook' permissions

**Issue:** Repository not accessible
**Solution:** Verify organization membership and repository permissions

**Issue:** Secret already exists and is recent
**Solution:** Use `--force-update` to override age policies

## 📈 Performance Considerations

### Batch Processing
- **Parallel Operations:** Where safely possible, operations run in parallel
- **Rate Limiting:** Respect GitHub API rate limits
- **Progress Indicators:** Clear progress reporting for long operations
- **Resume Capability:** Ability to continue after interruptions

### Scalability
- **Large Organizations:** Efficient handling of organizations with many repositories
- **Configurable Limits:** Adjustable parameters for different scales
- **Memory Efficiency:** Streaming processing for large repository lists

## 🔧 Customization

### Configuration Options
All scripts support extensive customization through:
- **Command Line Arguments:** Override defaults on a per-run basis
- **Environment Variables:** Set organization-wide defaults
- **Configuration Files:** Store commonly used parameters

### Extension Points
The scripts are designed for easy extension:
- **Custom Filters:** Add repository filtering logic
- **Additional Secrets:** Support for multiple secret types
- **Custom Notifications:** Add Slack/email notifications
- **Audit Integration:** Connect to institutional audit systems

## 📚 Related Documentation

- [Update Guide](UPDATE-GUIDE.md) - Template repository update procedures
- [Development Environment Setup](setup/DEVELOPMENT_ENVIRONMENT_SETUP.md) - Developer environment configuration
- [Virtual Environment Setup](setup/VIRTUAL_ENVIRONMENT_SETUP.md) - Python environment management
- [Project Structure](project-structure/) - Repository organization documentation

## 🆘 Support and Troubleshooting

For issues with the automation suite:

1. **Check Prerequisites:** Ensure GitHub CLI is installed and authenticated
2. **Verify Permissions:** Confirm token has required permissions
3. **Review Logs:** Check script output for specific error messages
4. **Test Components:** Use individual scripts to isolate issues
5. **Consult Documentation:** Review specific script documentation

**Common Commands for Troubleshooting:**
```bash
# Test GitHub CLI authentication
gh auth status

# Verify token permissions
./scripts/add-secrets-to-students.sh --check-token

# Test repository access
gh repo view WSU-ML-DL/cs6600-m1-homework1-template

# Check organization access
gh repo list WSU-ML-DL --limit 5
```

---

**Note:** This automation suite is designed for instructors managing CS6600 assignments. It requires appropriate GitHub permissions and should be used in accordance with your institution's policies.
