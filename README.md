# GitHub Classroom Tools

A comprehensive automation suite for managing GitHub Classroom assignments with advanced workflow orchestration, repository discovery, and secret management capabilities.

## 🎯 Overview

This repository provides a complete set of tools for instructors to automate GitHub Classroom assignment management, including:

- **Automated repository discovery** from GitHub Classroom assignments
- **Batch secret management** across multiple student repositories  
- **Template synchronization** with GitHub Classroom
- **Student assistance tools** for common issues
- **Master workflow orchestration** through configuration files

## 🚀 Quick Start

### 1. Add as Submodule to Your Assignment Repository

```bash
# In your assignment repository root
git submodule add https://github.com/YOUR-ORG/gh_classroom_tools.git tools
git submodule update --init --recursive
```

### 2. Configure Your Assignment

```bash
# Copy and customize the configuration template
cp tools/assignment-example.conf assignment.conf
vim assignment.conf
```

### 3. Run the Complete Workflow

```bash
# Execute the full automation workflow
./tools/scripts/assignment-orchestrator.sh assignment.conf
```

## 📁 Repository Structure

```
gh_classroom_tools/
├── scripts/                          # Core automation scripts
│   ├── assignment-orchestrator.sh    # Master workflow orchestrator
│   ├── fetch-student-repos.sh        # Repository discovery from classroom
│   ├── add-secrets-to-students.sh    # Batch secret management
│   ├── push-to-classroom.sh          # Template synchronization
│   ├── student-update-helper.sh      # Student assistance tools
│   └── SECRETS-MANAGEMENT.md         # Secret management documentation
├── docs/                             # Comprehensive documentation
│   ├── AUTOMATION-SUITE.md           # Complete automation guide
│   ├── ASSIGNMENT-ORCHESTRATOR.md    # Orchestrator documentation
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

### 2. Repository Discovery (`fetch-student-repos.sh`)
**Automated discovery** of student repositories from GitHub Classroom assignments.

```bash
# Discover from classroom URL
./tools/scripts/fetch-student-repos.sh --classroom-url https://classroom.github.com/.../assignments/YOUR-ASSIGNMENT

# Generate batch files for other tools
./tools/scripts/fetch-student-repos.sh --output student-repos.txt
```

**Key Features:**
- Direct GitHub Classroom URL integration
- Automatic assignment name extraction
- Template repository filtering
- Batch file generation for downstream tools

### 3. Secret Management (`add-secrets-to-students.sh`)
**Batch secret management** with support for multiple tokens and age-based policies.

```bash
# Add secret to all students
./tools/scripts/add-secrets-to-students.sh SECRET_NAME --batch student-repos.txt

# Force update old secrets
./tools/scripts/add-secrets-to-students.sh SECRET_NAME --force-update --batch student-repos.txt
```

**Key Features:**
- Multi-repository batch processing
- Age-based secret rotation policies
- Token validation and verification
- Comprehensive error reporting

### 4. Template Synchronization (`push-to-classroom.sh`)
**Safe deployment** of template updates to GitHub Classroom.

```bash
# Sync template to classroom
./tools/scripts/push-to-classroom.sh
```

**Key Features:**
- Merge conflict detection and resolution
- Backup and rollback capabilities
- Branch management
- Pre-deployment validation

### 5. Student Assistance (`student-update-helper.sh`)
**Automated assistance** for common student repository issues.

```bash
# Help all students
./tools/scripts/student-update-helper.sh --batch student-repos.txt

# Help specific student
./tools/scripts/student-update-helper.sh https://github.com/ORG/student-repo
```

**Key Features:**
- Conflict resolution assistance
- Update guidance
- Batch processing support
- Educational feedback

## ⚙️ Configuration System

### Main Configuration File
The `assignment.conf` file controls all aspects of the workflow:

```bash
# Assignment Information
CLASSROOM_URL="https://classroom.github.com/classrooms/ID/assignments/NAME"
TEMPLATE_REPO_URL="https://github.com/ORG/template.git"
GITHUB_ORGANIZATION="YOUR-ORG"

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

### Example Configurations
- `assignment-example.conf` - Ready-to-use template
- Safe defaults for testing and development
- Commented examples for all features

## 🔄 Workflow Integration

### Typical Assignment Lifecycle

```bash
# 1. Initial setup
git submodule add https://github.com/YOUR-ORG/gh_classroom_tools.git tools
cp tools/assignment-example.conf assignment.conf

# 2. Create assignment in GitHub Classroom
# Get the classroom URL from GitHub Classroom interface

# 3. Configure and run automation
vim assignment.conf  # Add classroom URL and settings
./tools/scripts/assignment-orchestrator.sh --dry-run  # Preview
./tools/scripts/assignment-orchestrator.sh  # Execute

# 4. Ongoing maintenance
./tools/scripts/assignment-orchestrator.sh --step secrets  # Update secrets
./tools/scripts/assignment-orchestrator.sh --step assist   # Help students
```

### Integration with Assignment Repositories

```bash
# Assignment repository structure with submodule
your-assignment/
├── tools/                    # <- GitHub Classroom Tools (submodule)
├── assignment.conf           # <- Your assignment configuration
├── instructor_token.txt      # <- Your GitHub token (git-ignored)
├── notebook.ipynb            # <- Assignment content
├── requirements.txt          # <- Assignment dependencies
└── .gitignore               # <- Includes tools/generated/ pattern
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

### Safe Operations
- **Dry-run mode** for testing configurations
- **User confirmation** before destructive operations
- **Partial failure handling** with detailed reporting
- **Backup and rollback** capabilities where applicable

## 📚 Documentation

Comprehensive documentation is provided for all tools and workflows:

- **[Automation Suite Guide](docs/AUTOMATION-SUITE.md)** - Complete feature overview
- **[Assignment Orchestrator](docs/ASSIGNMENT-ORCHESTRATOR.md)** - Master workflow documentation
- **[Classroom URL Integration](docs/CLASSROOM-URL-INTEGRATION.md)** - GitHub Classroom features
- **[System Summary](docs/ORCHESTRATION-SYSTEM-SUMMARY.md)** - Architecture overview
- **[Secrets Management](scripts/SECRETS-MANAGEMENT.md)** - Token and secret handling

## 🚀 Advanced Usage

### Multiple Assignment Management
```bash
# Different configurations for different assignments
./tools/scripts/assignment-orchestrator.sh hw1.conf
./tools/scripts/assignment-orchestrator.sh hw2.conf  
./tools/scripts/assignment-orchestrator.sh final-project.conf
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

## 📈 Version History

- **v1.0** - Initial release with complete automation suite
- **v1.1** - GitHub Classroom URL integration
- **v1.2** - Master workflow orchestrator
- **v1.3** - Comprehensive documentation and configuration system

---

**GitHub Classroom Tools** - Streamlining assignment management through automation 🎓
