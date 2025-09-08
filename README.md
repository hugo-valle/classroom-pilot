# GitHub Classroom Tools

A comprehensive automation suite for managing GitHub Classroom assignments with advanced workflow orchestration, repository discovery, and secret management capabilities. **Now with universal file type support and enhanced GitHub Classroom integration.**

## 🎯 Overview

This repository provides a complete set of tools for instructors to automate GitHub Classroom assignment management, including:

- **Universal assignment file support** - Works with any file type (.py, .cpp, .sql, .md, .html, .ipynb, etc.)
- **Automated repository discovery** from GitHub Classroom assignments with smart filtering
- **Batch secret management** across multiple student repositories  
- **Repository access management** with intelligent permission cycling for GitHub Classroom issues
- **Template synchronization** with GitHub Classroom repositories
- **Automated cron scheduling** for hands-off assignment management
- **Student assistance tools** for common workflow issues
- **Master workflow orchestration** through configuration files
- **Instructor repository filtering** to focus on student repositories only
- **Git submodule deployment** for cross-assignment reusability
- **Advanced repository context detection** for submodule environments
- **Clear URL distinction** between Classroom assignment pages and repository URLs

## 📊 Project Status - Phase 1: Alpha Implementation

**Current Release**: `v1.1.0-alpha.2` (Bash Implementation)

### ✅ Completed Features
- **🔄 Complete CI/CD Pipeline**: Automated testing, linting, and releases
- **🤖 Automated Release Management**: Both development and production workflows
- **🛡️ Security & Quality Gates**: ShellCheck, secret scanning, branch protection
- **📚 Comprehensive Documentation**: Usage guides, troubleshooting, best practices
- **🧪 Multi-Shell Testing**: Bash, zsh compatibility across platforms
- **🔍 Branch Naming Enforcement**: Automated validation of development workflows
- **🚀 Universal File Type Support**: Works with any assignment file type
- **📦 Batch Operations**: Repository discovery, secret management, template sync
- **🔧 Repository Access Management**: Intelligent permission cycling for GitHub Classroom issues
- **⏰ Automated Scheduling**: Cron-based background synchronization
- **🎯 Submodule Integration**: Easy deployment to assignment repositories

### 🎯 Phase 1 Goals (Current)
- ✅ **Finalize Bash-based CLI** as stable foundation
- ✅ **Comprehensive documentation** for installation and usage
- ✅ **Contribution guidelines** and development workflow
- ✅ **CI/CD pipeline** with automated testing and releases
- 🔄 **Performance optimization** and error handling improvements
- 🔄 **Beta testing** with real classroom environments

### 🚧 Upcoming Phases

#### Phase 2: Enhanced CLI & API Foundation
- **Go-based CLI rewrite** for better performance and cross-platform support
- **RESTful API server** for web-based management interfaces
- **Enhanced error handling** and retry mechanisms
- **Plugin architecture** for extensible functionality

#### Phase 3: Web Interface & Advanced Features  
- **React-based web dashboard** for visual assignment management
- **Real-time monitoring** and notification systems
- **Advanced analytics** and reporting capabilities
- **Multi-classroom management** features

### 🎯 Current Focus
This Phase 1 alpha release focuses on establishing a **robust, well-tested foundation** with the current Bash implementation while building the infrastructure for future enhancements.

**💡 Why Bash First?**
- **Universal availability** on all Unix-like systems
- **Educational transparency** - instructors can easily understand and modify
- **Rapid prototyping** of workflow concepts
- **Stable foundation** before complexity increases
- **Classroom-ready** for immediate use

## � Documentation

Comprehensive documentation is provided for all tools and workflows:

- **[Automation Suite Guide](docs/AUTOMATION-SUITE.md)** - Complete feature overview
- **[Assignment Orchestrator](docs/ASSIGNMENT-ORCHESTRATOR.md)** - Master workflow documentation
- **[Cycle Collaborator](docs/CYCLE-COLLABORATOR.md)** - Repository access fix guide
- **[Cron Automation](docs/CRON-AUTOMATION.md)** - Automated scheduling and background sync
- **[Classroom URL Integration](docs/CLASSROOM-URL-INTEGRATION.md)** - GitHub Classroom features
- **[System Summary](docs/ORCHESTRATION-SYSTEM-SUMMARY.md)** - Architecture overview
- **[Secrets Management](docs/SECRETS-MANAGEMENT.md)** - Token and secret handling
- **[Contributing Guidelines](docs/CONTRIBUTING.md)** - Development workflow and standards
- **[Workflow Documentation](.github/README.md)** - GitHub Actions automation guide

## �💡 Pro Tips
- Always use `--dry-run` first to preview changes
- Use `--one-student` when classroom repository URL issues occur
- Generated batch files are saved in `tools/generated/` and automatically git-ignored
- Scripts automatically detect submodule context and load `assignment.conf`
- Use `--help` on any script to see all available options
- Environment variables override `assignment.conf` settings for testing

## 🚀 Automation & CI/CD

The GitHub Classroom Tools now include comprehensive automation through GitHub Actions workflows for professional development and release management.

### Automated Release Management

The tools use **Git Flow** with semantic versioning for professional release management:

- **Alpha releases**: `v1.0.0-alpha.1` - Development snapshots with latest features
- **Beta releases**: `v1.0.0-beta.1` - Release candidates for testing
- **Stable releases**: `v1.0.0` - Production-ready versions

```bash
# Create and push a release tag to trigger automation
git tag v1.1.0-alpha.1
git push origin v1.1.0-alpha.1

# The automation will:
# 1. Run comprehensive tests and security scans
# 2. Generate release notes from CHANGELOG.md
# 3. Create GitHub release with assets
# 4. Update documentation
```

### GitHub Actions Workflows

#### 🔄 Release Workflow (`.github/workflows/release.yml`)
Triggered on: Git tags (v*.*.*)

**Capabilities:**
- **Multi-shell testing**: Validates scripts on bash, zsh, fish
- **Security scanning**: ShellCheck analysis for all bash scripts
- **Automated releases**: Creates GitHub releases with generated notes
- **Asset publishing**: Bundles and uploads release artifacts
- **Documentation updates**: Automatically updates changelog

```bash
# Manual workflow trigger (for testing)
gh workflow run release.yml
```

#### ✅ Continuous Integration (`.github/workflows/ci.yml`)
Triggered on: Push to main/develop, Pull Requests

**Capabilities:**
- **Syntax validation**: Ensures all scripts are syntactically correct
- **Shell compatibility**: Tests across bash 4.0+, zsh, and fish
- **Security checks**: Comprehensive ShellCheck scanning
- **Dependency validation**: Verifies GitHub CLI and git availability
- **Configuration testing**: Validates assignment.conf parsing

#### 🔧 Auto-Update Workflow (`.github/workflows/auto-update.yml`)
Triggered on: Weekly schedule, manual dispatch

**Capabilities:**
- **Dependency updates**: Automatically updates GitHub Actions versions
- **Security patches**: Creates PRs for security-related updates
- **Documentation sync**: Keeps README and docs synchronized
- **Maintenance tasks**: Automated cleanup and optimization

### Development Workflow

#### Branch Strategy
```bash
# Feature development
git checkout develop
git checkout -b feature/new-enhancement
# ... make changes ...
git commit -m "feat: add new enhancement"
git push origin feature/new-enhancement
# Create PR to develop branch

# Release preparation
git checkout develop
git checkout -b release/1.1.0
# Update CHANGELOG.md, bump versions
git commit -m "chore: prepare release 1.1.0"
git push origin release/1.1.0
# Create PR to main branch

# Create release tag
git checkout main
git tag v1.1.0
git push origin v1.1.0  # Triggers automated release
```

#### Release Process
1. **Development**: Work on `feature/*` branches from `develop`
2. **Integration**: Merge features to `develop` branch
3. **Release Preparation**: Create `release/*` branch, update CHANGELOG.md
4. **Release**: Merge to `main`, create Git tag
5. **Automation**: GitHub Actions handles testing, building, and publishing

### Monitoring & Maintenance

#### Workflow Status
```bash
# Check workflow runs
gh run list --workflow=release.yml
gh run list --workflow=ci.yml

# View specific run details
gh run view <run-id>

# Download workflow artifacts
gh run download <run-id>
```

#### Release Management
```bash
# List all releases
gh release list

# View specific release
gh release view v1.0.0

# Create manual release (bypasses automation)
gh release create v1.0.0 --generate-notes
```

### Automation Benefits

- **Quality Assurance**: Automated testing prevents regressions
- **Security**: Regular security scanning and dependency updates
- **Documentation**: Always up-to-date release notes and changelogs
- **Consistency**: Standardized release process across all versions
- **Efficiency**: Reduces manual release overhead by 90%
- **Reliability**: Automated validation ensures release quality

**🔧 Configuration Files:**
- `.github/workflows/`: All automation workflows
- `docs/CHANGELOG.md`: Professional changelog following Keep a Changelog format
- `.github/README.md`: Workflow documentation and usage guides

For detailed workflow documentation, see [`.github/README.md`](.github/README.md) and the [changelog](docs/CHANGELOG.md).

## 🚀 Quick Start

### 1. Add as Submodule to Your Assignment Repository

```bash
# In your assignment repository root
git submodule add https://github.com/hugo-valle/gh_classroom_tools.git tools
git submodule update --init --recursive
```

### 2. Configure Your Assignment

```bash
# Copy and customize the configuration template
cp tools/assignment-example.conf assignment.conf
vim assignment.conf

# Set your assignment file (supports any file type!)
# Examples:
# ASSIGNMENT_FILE="homework.py"        # Python assignment
# ASSIGNMENT_FILE="assignment.cpp"     # C++ assignment  
# ASSIGNMENT_FILE="queries.sql"        # SQL assignment
# ASSIGNMENT_FILE="notebook.ipynb"     # Jupyter notebook
```

### 3. Run the Complete Workflow

```bash
# Execute the full automation workflow
./tools/scripts/assignment-orchestrator.sh assignment.conf
```

### 4. Optional: Set Up Automated Cron Sync

For hands-off assignment management, install the automated cron job:

```bash
# Install 4-hour automated sync
./tools/scripts/manage-cron.sh install

# Monitor sync activity
./tools/scripts/manage-cron.sh logs

# Check status
./tools/scripts/manage-cron.sh status
```

The cron job will automatically:
- Sync template changes with GitHub Classroom every 4 hours
- Push tokens to student repositories as they accept assignments
- Log all activity for monitoring

See [Cron Automation Documentation](docs/CRON-AUTOMATION.md) for detailed setup and configuration.

## � Adding Tools to Your Assignment Repository

### Step-by-Step Submodule Setup

To use these GitHub Classroom automation tools in your assignment repository, you need to add them as a git submodule. **The submodule folder must be named `tools`** for the scripts to work correctly.

#### 1. Navigate to Your Assignment Repository

```bash
# Go to your assignment repository root directory
cd /path/to/your-assignment-repository

# Verify you're in the right place (should see your assignment files)
ls -la
# You should see files like: assignment.ipynb, README.md, requirements.txt, etc.
```

#### 2. Add the Tools Submodule

```bash
# Add the tools repository as a submodule named 'tools'
git submodule add https://github.com/hugo-valle/gh_classroom_tools.git tools

# Initialize and update the submodule
git submodule update --init --recursive
```

**⚠️ Important**: The submodule **must** be named `tools` because:
- All scripts expect to find themselves at `./tools/scripts/`
- Configuration files are loaded relative to the `tools/` directory
- The orchestrator automatically detects the repository root as the parent of `tools/`

#### 3. Verify the Setup

```bash
# Check that the submodule was added correctly
git status
# Should show: new file: .gitmodules and new file: tools

# Verify the tools are accessible
ls tools/scripts/
# Should show: assignment-orchestrator.sh, fetch-student-repos.sh, cycle-collaborator.sh, etc.

# Test the submodule setup
./tools/scripts/assignment-orchestrator.sh --help
# Should display the help message
```

#### 4. Commit the Submodule Addition

```bash
# Add and commit the submodule to your repository
git add .gitmodules tools
git commit -m "Add GitHub Classroom automation tools as submodule

- Added hugo-valle/gh_classroom_tools as tools/ submodule
- Provides complete workflow automation for GitHub Classroom
- Includes orchestrator, repository discovery, and secret management"

# Push to your repository
git push origin main
```

#### 5. Create Your Configuration

```bash
# Copy the example configuration and customize it for your assignment
cp tools/assignment-example.conf assignment.conf

# Edit the configuration for your specific assignment
vim assignment.conf  # or your preferred editor

# Key settings to configure:
# - CLASSROOM_URL: Your GitHub Classroom assignment URL
# - ASSIGNMENT_FILE: Your main assignment file (any type: .py, .cpp, .sql, .ipynb, etc.)
# - GITHUB_ORGANIZATION: Your GitHub organization name
# - SECRETS: Any secrets you want to add to student repositories
```

### Repository Structure After Setup

After adding the tools submodule, your assignment repository should look like this:

```
your-assignment-repository/
├── .gitmodules                    # Git submodule configuration (auto-created)
├── assignment.conf                # Your assignment configuration
├── your-assignment-file.*         # Your main assignment file (.py, .cpp, .sql, .ipynb, etc.)
├── README.md                      # Your assignment README
├── requirements.txt               # Dependencies (if applicable)
├── tools/                         # ← GitHub Classroom Tools (submodule)
│   ├── scripts/                   # Automation scripts
│   ├── docs/                      # Documentation
│   ├── assignment-example.conf    # Configuration template
│   └── README.md                  # Tools documentation
└── [other assignment files]       # Additional assignment resources
```

### Updating the Tools Submodule

When new features or fixes are added to the tools repository, you can update your submodule:

```bash
# Update to the latest version of the tools
git submodule update --remote tools

# Commit the submodule update
git add tools
git commit -m "Update tools submodule to latest version"
git push origin main
```

### Troubleshooting Submodule Setup

#### Common Issues and Solutions

**Issue**: `./tools/scripts/assignment-orchestrator.sh: No such file or directory`
```bash
# Solution: Initialize the submodule
git submodule update --init --recursive
```

**Issue**: Scripts can't find configuration or repository root
```bash
# Solution: Ensure submodule is named 'tools' (not 'gh_classroom_tools')
git submodule add https://github.com/hugo-valle/gh_classroom_tools.git tools
```

**Issue**: Permission denied when running scripts
```bash
# Solution: Make scripts executable
chmod +x tools/scripts/*.sh
```

**Issue**: Submodule appears empty after cloning
```bash
# Solution: Initialize submodules after cloning
git clone <your-repo-url>
cd <your-repo>
git submodule update --init --recursive
```

### For Team Repositories

If multiple instructors are working on the same assignment repository:

```bash
# When cloning the repository, always initialize submodules
git clone <assignment-repo-url>
cd <assignment-repo>
git submodule update --init --recursive

# When pulling updates that include submodule changes
git pull origin main
git submodule update --init --recursive
```

## �📁 Repository Structure

```
gh_classroom_tools/
├── scripts/                          # Core automation scripts
│   ├── assignment-orchestrator.sh    # Master workflow orchestrator
│   ├── fetch-student-repos.sh        # Repository discovery from classroom
│   ├── add-secrets-to-students.sh    # Batch secret management
│   ├── push-to-classroom.sh          # Template synchronization
│   ├── student-update-helper.sh      # Student assistance tools
│   ├── cycle-collaborator.sh         # Repository access fix tool
│   └── SECRETS-MANAGEMENT.md         # Secret management documentation
├── docs/                             # Comprehensive documentation
│   ├── AUTOMATION-SUITE.md           # Complete automation guide
│   ├── ASSIGNMENT-ORCHESTRATOR.md    # Orchestrator documentation
│   ├── CYCLE-COLLABORATOR.md         # Repository access fix guide
│   ├── CLASSROOM-URL-INTEGRATION.md  # Classroom URL features
│   └── ORCHESTRATION-SYSTEM-SUMMARY.md # System overview
├── assignment.conf                   # Main configuration template
├── assignment-example.conf           # Example configuration
└── README.md                         # This file
```

## 🛠️ Core Tools

### 1. Assignment Orchestrator (`assignment-orchestrator.sh`)
**Master control script** that manages the complete assignment workflow through configuration files.

```bash
# Run complete workflow
./tools/scripts/assignment-orchestrator.sh

# Preview without executing
./tools/scripts/assignment-orchestrator.sh --dry-run

# Run only specific step
./tools/scripts/assignment-orchestrator.sh --step secrets
```

**Key Features:**
- Configuration-driven workflow management
- Support for partial workflow execution
- Dry-run preview mode
- Comprehensive error handling and recovery
- **Generic assignment support** through ASSIGNMENT_NOTEBOOK variable
- **Submodule context detection** for proper repository root identification

### 2. Repository Discovery (`fetch-student-repos.sh`)
**Automated discovery** of student repositories from GitHub Classroom assignments.

```bash
# Basic discovery (uses assignment.conf settings automatically)
./tools/scripts/fetch-student-repos.sh

# Discover from classroom URL (auto-detects assignment name)
./tools/scripts/fetch-student-repos.sh --classroom-url https://classroom.github.com/classrooms/206604610-wsu-ml-dl-classroom-fall25/assignments/cs6600-m1-homework1

# Custom output file
./tools/scripts/fetch-student-repos.sh --output custom-student-list.txt

# Students only (exclude instructor and template repos)
./tools/scripts/fetch-student-repos.sh --exclude-instructor

# Dry run to preview what would be discovered
./tools/scripts/fetch-student-repos.sh --dry-run
```

**Key Features:**
- Direct GitHub Classroom URL integration
- Automatic assignment name extraction  
- Template repository filtering
- Batch file generation for downstream tools
- **Generic assignment notebook detection** through configuration
- **Improved error handling** with repository path context

### 3. Secret Management (`add-secrets-to-students.sh`)
**Batch secret management** with support for multiple tokens and age-based policies.

```bash
# Add secret to specific student (uses assignment.conf settings)
./tools/scripts/add-secrets-to-students.sh INSTRUCTOR_TESTS_TOKEN https://github.com/WSU-ML-DL/cs6600-m1-homework1-student123

# Batch add secrets to all students
./tools/scripts/add-secrets-to-students.sh INSTRUCTOR_TESTS_TOKEN --batch tools/generated/student-repos-students-only.txt

# Force update old secrets regardless of age
./tools/scripts/add-secrets-to-students.sh INSTRUCTOR_TESTS_TOKEN --force-update --batch student-repos.txt

# Custom token file and age policy
./tools/scripts/add-secrets-to-students.sh MY_TOKEN --token-file my_token.txt --max-age 30

# Check token permissions before operations
./tools/scripts/add-secrets-to-students.sh --check-token
```

**Key Features:**
- Multi-repository batch processing
- Age-based secret rotation policies
- Token validation and verification
- Comprehensive error reporting
- **Automatic configuration loading** from assignment.conf

### 4. Template Synchronization (`push-to-classroom.sh`)
**Safe deployment** of template updates to GitHub Classroom.

```bash
# Sync template to classroom (uses assignment.conf settings automatically)
./tools/scripts/push-to-classroom.sh

# Force push without confirmation prompts
./tools/scripts/push-to-classroom.sh --force

# Override assignment notebook for testing
ASSIGNMENT_NOTEBOOK="test.ipynb" ./tools/scripts/push-to-classroom.sh --force
```

**Key Features:**
- Merge conflict detection and resolution
- Backup and rollback capabilities
- Branch management
- Pre-deployment validation
- **Assignment-agnostic operation** through environment variables
- **Enhanced repository context awareness** for submodule deployment

### 5. Student Assistance (`student-update-helper.sh`)
**Automated assistance** for common student repository issues.

```bash
# Help specific student (uses assignment.conf settings automatically)
./tools/scripts/student-update-helper.sh https://github.com/WSU-ML-DL/cs6600-m1-homework1-student123

# NEW: Help single student using template directly (bypasses classroom repo)
./tools/scripts/student-update-helper.sh --one-student https://github.com/WSU-ML-DL/cs6600-m1-homework1-student123

# Help all students from batch file
./tools/scripts/student-update-helper.sh --batch tools/generated/student-repos-students-only.txt

# Check student status without making changes
./tools/scripts/student-update-helper.sh --status https://github.com/WSU-ML-DL/cs6600-m1-homework1-student123

# Dry run to preview what would be done
./tools/scripts/student-update-helper.sh https://github.com/WSU-ML-DL/cs6600-m1-homework1-student123 --dry-run

# Check classroom repository readiness
./tools/scripts/student-update-helper.sh --check-classroom
```

**Key Features:**
- Conflict resolution assistance
- Update guidance
- Batch processing support
- Educational feedback
- **Universal assignment compatibility** through variable-driven configuration
- **Advanced repository root detection** for submodule environments

### 6. Repository Access Fix (`cycle-collaborator.sh`)
**Intelligent repository access management** for fixing GitHub Classroom permission issues.

```bash
# Configuration mode (recommended) - fix access for all students
./tools/scripts/cycle-collaborator.sh --config assignment.conf --batch tools/generated/student-repos-students-only.txt --repo-urls

# Preview what would be done without making changes
./tools/scripts/cycle-collaborator.sh --config assignment.conf --batch tools/generated/student-repos-students-only.txt --repo-urls --dry-run

# Force cycling even when access appears correct
./tools/scripts/cycle-collaborator.sh --config assignment.conf --batch tools/generated/student-repos-students-only.txt --repo-urls --force

# Traditional mode - fix specific student
./tools/scripts/cycle-collaborator.sh assignment1 student-username organization

# List repository status without making changes
./tools/scripts/cycle-collaborator.sh --list assignment1 student-username organization
```

**Key Features:**
- **Intelligent cycling logic** - only cycles when access issues are detected
- **Force mode override** for troubleshooting persistent issues
- **Configuration-based integration** with assignment orchestrator (Step 5)
- **Repository URL batch processing** for seamless workflow integration
- **Comprehensive access verification** and detailed status reporting
- **Safe permission cycling** with pre-flight checks and validation

## ⚙️ Configuration System

### Main Configuration File
The `assignment.conf` file controls all aspects of the workflow:

```bash
# Assignment Information
CLASSROOM_URL="https://classroom.github.com/classrooms/ID/assignments/NAME"          # Assignment page URL
CLASSROOM_REPO_URL="https://github.com/ORG/classroom-semester-assignment"           # Optional: Classroom repo URL
TEMPLATE_REPO_URL="https://github.com/ORG/template.git"                             # Template repository
GITHUB_ORGANIZATION="YOUR-ORG"                                                      # GitHub organization

# Universal Assignment Support (v1.6+)
ASSIGNMENT_FILE="your_assignment_file"    # Any file type: .py, .cpp, .sql, .md, .ipynb, etc.

# Legacy support (deprecated - use ASSIGNMENT_FILE instead)
# ASSIGNMENT_NOTEBOOK="your_assignment.ipynb"  # Jupyter notebooks only

# Repository Discovery Options
INCLUDE_TEMPLATE_IN_BATCH=false           # Include template repository in batch operations
EXCLUDE_INSTRUCTOR_REPOS=false            # Exclude instructor-* repositories from student operations

# Secret Management
SECRETS=(
    "INSTRUCTOR_TESTS_TOKEN:instructor_token.txt:Description"
    "GRADING_TOKEN:grading_token.txt:Another description"
)

# Workflow Control
STEP_SYNC_TEMPLATE=true
STEP_DISCOVER_REPOS=true
STEP_MANAGE_SECRETS=true
STEP_ASSIST_STUDENTS=false

# Output Settings
OUTPUT_DIR="tools/generated"
```

### URL Configuration Guide

Understanding the difference between GitHub Classroom URLs is crucial for proper configuration:

#### `CLASSROOM_URL` (Required)
- **What it is**: The GitHub Classroom assignment management page URL
- **Used for**: Discovering student repositories, extracting assignment names
- **Format**: `https://classroom.github.com/classrooms/CLASSROOM-ID/assignments/ASSIGNMENT-NAME`
- **How to find**: Go to GitHub Classroom → Your Classroom → Assignments → Click your assignment → Copy URL from browser

#### `CLASSROOM_REPO_URL` (Optional)
- **What it is**: The actual git repository URL created by GitHub Classroom for the assignment
- **Used for**: Template synchronization with `push-to-classroom.sh`
- **Format**: `https://github.com/ORG/classroom-semester-assignment-template`
- **How to find**: Look for a repository in your organization with a name like `classroom-fall25-assignment-template`

```bash
# Example distinction:
CLASSROOM_URL="https://classroom.github.com/classrooms/12345/assignments/cs6600-homework1"     # Assignment page
CLASSROOM_REPO_URL="https://github.com/WSU-ML-DL/classroom-fall25-cs6600-homework1-template"  # Repository URL
```

### Universal File Type Support

The tools now support any assignment file type, not just Jupyter notebooks:

```bash
# Python assignments
ASSIGNMENT_FILE="homework.py"
ASSIGNMENT_FILE="main.py"

# C++ assignments  
ASSIGNMENT_FILE="assignment.cpp"
ASSIGNMENT_FILE="main.hpp"

# SQL assignments
ASSIGNMENT_FILE="queries.sql"
ASSIGNMENT_FILE="database_homework.sql"

# Web development
ASSIGNMENT_FILE="index.html"
ASSIGNMENT_FILE="styles.css"

# Documentation
ASSIGNMENT_FILE="README.md"
ASSIGNMENT_FILE="report.md"

# Jupyter notebooks (original support)
ASSIGNMENT_FILE="notebook.ipynb"
```

### Example Configurations
- `assignment-example.conf` - Ready-to-use template
- Safe defaults for testing and development
- Commented examples for all features

## 🔄 Workflow Integration

### Typical Assignment Lifecycle

```bash
# 1. Initial setup
git submodule add https://github.com/hugo-valle/gh_classroom_tools.git tools
cp tools/assignment-example.conf assignment.conf

# 2. Create assignment in GitHub Classroom
# Get the CLASSROOM_URL from GitHub Classroom interface

# 3. Configure for your specific assignment
vim assignment.conf  # Set ASSIGNMENT_NOTEBOOK="your_assignment.ipynb"

# 4. Run automation with enhanced generic support
./tools/scripts/assignment-orchestrator.sh assignment.conf --dry-run  # Preview
./tools/scripts/assignment-orchestrator.sh assignment.conf  # Execute

# 5. Ongoing maintenance
./tools/scripts/assignment-orchestrator.sh assignment.conf --step secrets  # Update secrets
./tools/scripts/assignment-orchestrator.sh assignment.conf --step assist   # Help students
./tools/scripts/assignment-orchestrator.sh assignment.conf --step cycle    # Fix repository access
```

### Integration with Assignment Repositories

```bash
# Assignment repository structure with submodule (v1.4 Enhanced)
your-assignment/
├── tools/                    # <- GitHub Classroom Tools (submodule)
├── assignment.conf           # <- Your assignment configuration with ASSIGNMENT_NOTEBOOK
├── instructor_token.txt      # <- Your GitHub token (git-ignored)
├── your_assignment.ipynb     # <- Assignment notebook (configurable name)
├── requirements.txt          # <- Assignment dependencies
├── .gitignore               # <- Includes tools/generated/ pattern
└── tools/generated/         # <- Auto-generated files (git-ignored)
```

### New in v1.4: Universal Assignment Support

The tools now automatically detect assignment files through the `ASSIGNMENT_FILE` configuration variable, making the same toolset work across different assignments and file types without modification:

```bash
# Different assignments, different file types, same tools
hw1/assignment.conf:  ASSIGNMENT_FILE="python_basics.py"
hw2/assignment.conf:  ASSIGNMENT_FILE="database_queries.sql"  
hw3/assignment.conf:  ASSIGNMENT_FILE="data_analysis.ipynb"
hw4/assignment.conf:  ASSIGNMENT_FILE="web_project.html"
final/assignment.conf: ASSIGNMENT_FILE="capstone_project.cpp"
```

## 🔒 Security and Best Practices

### Token Management
- **Store tokens in separate files** (not in configuration)
- **Use .gitignore** to prevent token commits
- **Rotate tokens regularly** using age-based policies
- **Validate token permissions** before operations

### Repository Access
- **Verify GitHub CLI authentication** before use
- **Check organization permissions** automatically
- **Handle access denied scenarios** gracefully
- **Provide clear error messages** for permission issues
- **Enhanced submodule context detection** for proper repository root identification

### Safe Operations
- **Dry-run mode** for testing configurations
- **User confirmation** before destructive operations
- **Partial failure handling** with detailed reporting
- **Backup and rollback** capabilities where applicable
- **Generic assignment validation** through configurable notebook detection

## � Running Scripts Directly

All scripts now automatically load settings from `assignment.conf`, making direct execution seamless. Here are practical examples for common instructor tasks:

### Complete Assignment Setup Workflow

```bash
# 1. Discover all student repositories
./tools/scripts/fetch-student-repos.sh --exclude-instructor

# 2. Add secrets to all students  
./tools/scripts/add-secrets-to-students.sh INSTRUCTOR_TESTS_TOKEN --batch tools/generated/student-repos-students-only.txt

# 3. Push template updates to classroom
./tools/scripts/push-to-classroom.sh

# 4. Help students who need updates
./tools/scripts/student-update-helper.sh --batch tools/generated/student-repos-students-only.txt --dry-run
```

### Individual Script Examples

```bash
# Repository Discovery with GitHub Classroom URL
./tools/scripts/fetch-student-repos.sh \
  --classroom-url https://classroom.github.com/classrooms/206604610-wsu-ml-dl-classroom-fall25/assignments/cs6600-m1-homework1 \
  --exclude-instructor \
  --output current-students.txt

# Secret Management with Custom Settings
./tools/scripts/add-secrets-to-students.sh GRADING_TOKEN \
  --token-file grading_token.txt \
  --max-age 30 \
  --batch current-students.txt

# Student Assistance for Specific Issues
./tools/scripts/student-update-helper.sh \
  https://github.com/WSU-ML-DL/cs6600-m1-homework1-student123 \
  --dry-run

# NEW: Single student help using template directly (bypasses classroom repo issues)
./tools/scripts/student-update-helper.sh --one-student \
  https://github.com/WSU-ML-DL/cs6600-m1-homework1-student123

# Template Sync with Environment Override (for testing)
ASSIGNMENT_NOTEBOOK="test_notebook.ipynb" ./tools/scripts/push-to-classroom.sh --force
```

### Batch Processing Workflows

```bash
# Generate different student lists for different purposes
./tools/scripts/fetch-student-repos.sh --exclude-instructor --output students-only.txt
./tools/scripts/fetch-student-repos.sh --include-template --output all-repos.txt

# Process different student groups
./tools/scripts/add-secrets-to-students.sh INSTRUCTOR_TESTS_TOKEN --batch students-only.txt
./tools/scripts/student-update-helper.sh --batch students-only.txt --dry-run

# Status checking across all students
while read repo; do
  echo "Checking: $repo"
  ./tools/scripts/student-update-helper.sh --status "$repo"
done < students-only.txt
```

### Troubleshooting and Validation

```bash
# Verify your token permissions
./tools/scripts/add-secrets-to-students.sh --check-token

# Test repository discovery without writing files
./tools/scripts/fetch-student-repos.sh --dry-run

# Check individual student status
./tools/scripts/student-update-helper.sh --status https://github.com/WSU-ML-DL/cs6600-m1-homework1-student123

# Validate classroom repository state
./tools/scripts/student-update-helper.sh --check-classroom
```

### Environment Variable Overrides

When you need to test or run scripts with different settings without modifying `assignment.conf`:

```bash
# Test with different assignment notebook
ASSIGNMENT_NOTEBOOK="test.ipynb" ./tools/scripts/fetch-student-repos.sh --dry-run

# Override GitHub organization for testing
GITHUB_ORGANIZATION="TEST-ORG" ./tools/scripts/fetch-student-repos.sh --dry-run

# Use different classroom URL temporarily
CLASSROOM_URL="https://classroom.github.com/test" ./tools/scripts/fetch-student-repos.sh --dry-run
```

### Quick Reference: Most Common Commands

```bash
# Daily instructor workflow
./tools/scripts/fetch-student-repos.sh --exclude-instructor  # Get current student list
./tools/scripts/push-to-classroom.sh                         # Sync any template changes
./tools/scripts/student-update-helper.sh --batch tools/generated/student-repos-students-only.txt --dry-run  # Check who needs help

# Weekly maintenance  
./tools/scripts/add-secrets-to-students.sh INSTRUCTOR_TESTS_TOKEN --batch tools/generated/student-repos-students-only.txt --max-age 7  # Refresh old secrets
./tools/scripts/cycle-collaborator.sh --config assignment.conf --batch tools/generated/student-repos-students-only.txt --repo-urls  # Fix any access issues

# Individual student help (when classroom repo has issues)
./tools/scripts/student-update-helper.sh --one-student https://github.com/ORG/student-repo  # Direct template-to-student update
```

**💡 Pro Tips:**
- Always use `--dry-run` first to preview changes
- Use `--one-student` when classroom repository URL issues occur
- Generated batch files are saved in `tools/generated/` and automatically git-ignored
- Scripts automatically detect submodule context and load `assignment.conf`
- Use `--help` on any script to see all available options
- Environment variables override `assignment.conf` settings for testing

## �📚 Documentation

Comprehensive documentation is provided for all tools and workflows:

- **[Automation Suite Guide](docs/AUTOMATION-SUITE.md)** - Complete feature overview
- **[Assignment Orchestrator](docs/ASSIGNMENT-ORCHESTRATOR.md)** - Master workflow documentation
- **[Cycle Collaborator](docs/CYCLE-COLLABORATOR.md)** - Repository access fix guide
- **[Classroom URL Integration](docs/CLASSROOM-URL-INTEGRATION.md)** - GitHub Classroom features
- **[System Summary](docs/ORCHESTRATION-SYSTEM-SUMMARY.md)** - Architecture overview
- **[Secrets Management](docs/SECRETS-MANAGEMENT.md)** - Token and secret handling

## 🚀 Advanced Usage

### Multiple Assignment Management (Enhanced in v1.4)
```bash
# Different configurations for different assignments with generic support
./tools/scripts/assignment-orchestrator.sh hw1.conf     # ASSIGNMENT_NOTEBOOK="hw1.ipynb"
./tools/scripts/assignment-orchestrator.sh hw2.conf     # ASSIGNMENT_NOTEBOOK="hw2.ipynb"
./tools/scripts/assignment-orchestrator.sh final.conf   # ASSIGNMENT_NOTEBOOK="final_project.ipynb"

# Direct environment variable override for testing
ASSIGNMENT_NOTEBOOK="test.ipynb" ./tools/scripts/push-to-classroom.sh --dry-run
```

### CI/CD Integration
```bash
# Automated workflows with no prompts
./tools/scripts/assignment-orchestrator.sh --yes --verbose
```

### Development and Testing
```bash
# Test configurations safely
./tools/scripts/assignment-orchestrator.sh --dry-run --verbose

# Debug specific steps
./tools/scripts/assignment-orchestrator.sh --step discover --verbose
```

## 📋 Requirements

- **GitHub CLI** (gh) installed and authenticated
- **Git** version control system
- **Bash** shell environment (Linux/macOS/WSL)
- **GitHub repository access** with appropriate permissions

### GitHub Permissions Required
- **Repository access** to template and student repositories
- **Secrets management** permissions for target repositories
- **Organization membership** for classroom access

## 🆘 Support and Troubleshooting

### Common Issues
1. **GitHub CLI not authenticated** - Run `gh auth login`
2. **Missing permissions** - Check organization membership and repository access
3. **Token file not found** - Create token files as specified in configuration
4. **Repository access denied** - Verify GitHub permissions and organization membership
5. **Assignment notebook not found** - Check ASSIGNMENT_NOTEBOOK variable in configuration
6. **Submodule context issues** - Ensure tools are properly initialized with `git submodule update --init`

### Getting Help
- Check the comprehensive documentation in `docs/`
- Run scripts with `--help` flag for usage information
- Use `--verbose` flag for detailed debugging output
- Test with `--dry-run` before making changes

### Contributing
This is an internal tool suite. For issues or improvements:
1. Test thoroughly with `--dry-run` mode
2. Update documentation for any changes
3. Verify backward compatibility with existing configurations

## 🔧 Troubleshooting

### Common URL Configuration Issues

#### "CLASSROOM_REPO_URL is not set" Error
```bash
# Error from push-to-classroom.sh
[ERROR] CLASSROOM_REPO_URL is not set in assignment.conf

# Solution: Add the GitHub Classroom repository URL (not the assignment page URL)
CLASSROOM_REPO_URL="https://github.com/ORG/classroom-semester-assignment-template"
```

#### Repository Discovery Issues
```bash
# No repositories found
[WARNING] No repositories found matching pattern: assignment-prefix-*

# Check your CLASSROOM_URL format:
# ✅ Correct: https://classroom.github.com/classrooms/12345/assignments/assignment-name
# ❌ Wrong: https://github.com/ORG/repository-name
```

#### Instructor Repository Filtering
```bash
# To exclude instructor repositories from student operations:
EXCLUDE_INSTRUCTOR_REPOS=true

# This filters out repositories with "instructor" in the name:
# ✅ Included: cs6600-homework1-student123
# ❌ Excluded: cs6600-homework1-instructor-tests
```

### File Type Support
```bash
# Universal file type examples:
ASSIGNMENT_FILE="homework.py"        # Python
ASSIGNMENT_FILE="assignment.cpp"     # C++
ASSIGNMENT_FILE="queries.sql"        # SQL
ASSIGNMENT_FILE="notebook.ipynb"     # Jupyter

# Legacy support (still works):
ASSIGNMENT_NOTEBOOK="notebook.ipynb"  # Will be converted to ASSIGNMENT_FILE
```

---

**GitHub Classroom Tools** - Streamlining assignment management through automation 🎓
