# GitHub Classroom Tools

A comprehensive automation suite for managing GitHub Classroom assignments with advanced workflow orchestration, repository discovery, and secret management capabilities. **Now with generic assignment support and git submodule architecture for maximum reusability.**

## 🎯 Overview

This repository provides a complete set of tools for instructors to automate GitHub Classroom assignment management, including:

- **Automated repository discovery** from GitHub Classroom assignments
- **Batch secret management** across multiple student repositories  
- **Template synchronization** with GitHub Classroom
- **Student assistance tools** for common issues
- **Master workflow orchestration** through configuration files
- **Generic assignment support** through variable-driven configuration
- **Git submodule deployment** for cross-assignment reusability
- **Advanced repository context detection** for submodule environments

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

# Set your assignment notebook file (key for generic support)
# Example: ASSIGNMENT_NOTEBOOK="m1_homework1.ipynb"
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
- **Generic assignment support** through ASSIGNMENT_NOTEBOOK variable
- **Submodule context detection** for proper repository root identification

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
- **Generic assignment notebook detection** through configuration
- **Improved error handling** with repository path context

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
- **Assignment-agnostic operation** through environment variables
- **Enhanced repository context awareness** for submodule deployment

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
- **Universal assignment compatibility** through variable-driven configuration
- **Advanced repository root detection** for submodule environments

## ⚙️ Configuration System

### Main Configuration File
The `assignment.conf` file controls all aspects of the workflow:

```bash
# Assignment Information
CLASSROOM_URL="https://classroom.github.com/classrooms/ID/assignments/NAME"
TEMPLATE_REPO_URL="https://github.com/ORG/template.git"
GITHUB_ORGANIZATION="YOUR-ORG"

# Generic Assignment Support (NEW in v1.4)
ASSIGNMENT_NOTEBOOK="your_assignment.ipynb"  # Makes tools assignment-agnostic

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
git submodule add https://github.com/hugo-valle/gh_classroom_tools.git tools
cp tools/assignment-example.conf assignment.conf

# 2. Create assignment in GitHub Classroom
# Get the classroom URL from GitHub Classroom interface

# 3. Configure for your specific assignment (NEW in v1.4)
vim assignment.conf  # Set ASSIGNMENT_NOTEBOOK="your_assignment.ipynb"

# 4. Run automation with enhanced generic support
./tools/scripts/assignment-orchestrator.sh assignment.conf --dry-run  # Preview
./tools/scripts/assignment-orchestrator.sh assignment.conf  # Execute

# 5. Ongoing maintenance
./tools/scripts/assignment-orchestrator.sh assignment.conf --step secrets  # Update secrets
./tools/scripts/assignment-orchestrator.sh assignment.conf --step assist   # Help students
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

The tools now automatically detect assignment notebooks through the `ASSIGNMENT_NOTEBOOK` configuration variable, making the same toolset work across different assignments without modification:

```bash
# Different assignments, same tools
hw1/assignment.conf:  ASSIGNMENT_NOTEBOOK="hw1_exercises.ipynb"
hw2/assignment.conf:  ASSIGNMENT_NOTEBOOK="hw2_project.ipynb"  
final/assignment.conf: ASSIGNMENT_NOTEBOOK="final_project.ipynb"
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

## 📚 Documentation

Comprehensive documentation is provided for all tools and workflows:

- **[Automation Suite Guide](docs/AUTOMATION-SUITE.md)** - Complete feature overview
- **[Assignment Orchestrator](docs/ASSIGNMENT-ORCHESTRATOR.md)** - Master workflow documentation
- **[Classroom URL Integration](docs/CLASSROOM-URL-INTEGRATION.md)** - GitHub Classroom features
- **[System Summary](docs/ORCHESTRATION-SYSTEM-SUMMARY.md)** - Architecture overview
- **[Secrets Management](scripts/SECRETS-MANAGEMENT.md)** - Token and secret handling

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

## 📈 Version History

- **v1.0** - Initial release with complete automation suite
- **v1.1** - GitHub Classroom URL integration
- **v1.2** - Master workflow orchestrator
- **v1.3** - Comprehensive documentation and configuration system
- **v1.4** - Generic assignment support, enhanced submodule architecture, and improved repository context detection

### What's New in v1.4
- **Generic Assignment Support**: Tools now work with any assignment through `ASSIGNMENT_NOTEBOOK` configuration
- **Enhanced Submodule Architecture**: Improved repository context detection for submodule deployment
- **Variable-Driven Configuration**: Assignment-agnostic operation through environment variables
- **Advanced Error Handling**: Better error messages with repository path context
- **Universal Compatibility**: Single toolset works across multiple assignments without modification
- **Production-Tested**: Validated with real GitHub Classroom integration

---

**GitHub Classroom Tools** - Streamlining assignment management through automation 🎓
