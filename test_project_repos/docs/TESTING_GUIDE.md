# 📚 Comprehensive Testing Guide for Classroom Pilot

This guide provides detailed instructions for testing the `classroom-pilot` Python package before releases.

## 🎯 Testing Philosophy

Our testing approach ensures:

- **Package Quality**: Comprehensive validation of all functionality
- **User Experience**: Real-world scenario testing
- **Cross-Platform**: Testing across different environments
- **Regression Prevention**: Validation of existing functionality
- **Performance**: Testing execution speed and resource usage

## 🧪 Test Environment Setup

### Prerequisites

- **Python**: 3.10+ (we test 3.10, 3.11, 3.12)
- **Poetry**: For package building and dependency management
- **Git**: For repository operations
- **GitHub CLI**: For API testing (optional)

### Environment Isolation

Always test in isolated environments to avoid conflicts:

```bash
# Option 1: Python venv
python -m venv test_env
source test_env/bin/activate  # macOS/Linux
# test_env\Scripts\activate   # Windows

# Option 2: Conda
conda create -n classroom_pilot_test python=3.11
conda activate classroom_pilot_test
```

## 📦 Installation Testing

### Package Building

```bash
# Build package with Poetry
cd /path/to/classroom_pilot
poetry build

# Verify build artifacts
ls -la dist/
# Expected: classroom_pilot-3.1.0a2-py3-none-any.whl
#           classroom_pilot-3.1.0a2.tar.gz
```

### Installation Methods

**Method 1: From Wheel**
```bash
pip install /path/to/classroom_pilot/dist/classroom_pilot-3.1.0a2-py3-none-any.whl
```

**Method 2: From Source**
```bash
pip install /path/to/classroom_pilot/
```

**Method 3: Editable Install**
```bash
pip install -e /path/to/classroom_pilot/
```

### Installation Validation

```bash
# Verify package installation
pip show classroom-pilot

# Test entry point
classroom-pilot --version

# Test Python import
python -c "import classroom_pilot; print(classroom_pilot.__version__)"
```

## 🖥️ CLI Interface Testing

### Command Structure Testing

```bash
# Main help
classroom-pilot --help

# Subcommand help
classroom-pilot assignments --help
classroom-pilot repos --help
classroom-pilot secrets --help
classroom-pilot automation --help

# Command-specific help
classroom-pilot assignments setup --help
classroom-pilot assignments orchestrate --help
classroom-pilot repos fetch --help
classroom-pilot repos collaborator --help
```

### Functional Testing

```bash
# Version information
classroom-pilot --version
classroom-pilot version

# Configuration commands
classroom-pilot assignments setup --dry-run
classroom-pilot assignments validate

# Repository commands (dry-run)
classroom-pilot repos fetch --dry-run --verbose
classroom-pilot repos collaborator --dry-run --verbose

# Help system completeness
classroom-pilot invalid-command  # Should show helpful error
```

### Error Handling Testing

```bash
# Invalid commands
classroom-pilot nonexistent-command

# Missing required parameters
classroom-pilot assignments setup

# Invalid configuration
echo "INVALID=true" > assignment.conf
classroom-pilot assignments validate
```

## 🐍 Python API Testing

### Import Testing

```python
# Test all major imports
import classroom_pilot
from classroom_pilot import ConfigLoader, ConfigValidator, BashWrapper
from classroom_pilot import setup_logging, get_logger
from classroom_pilot import AssignmentService, ReposService, SecretsService, AutomationService
from classroom_pilot.assignments.setup import AssignmentSetup

# Verify version
print(f"Version: {classroom_pilot.__version__}")
```

### Configuration System Testing

```python
from classroom_pilot import ConfigLoader, ConfigValidator

# Test configuration loading
config_data = {
    "CLASSROOM_URL": "https://classroom.github.com/test",
    "GITHUB_ORGANIZATION": "test-org",
    "TEMPLATE_REPO_URL": "https://github.com/test/template"
}

# Test validation
validator = ConfigValidator()
result = validator.validate_full_config(config_data)
print(f"Validation result: {result}")
```

### Logging System Testing

```python
from classroom_pilot import setup_logging, get_logger

# Test logging setup
setup_logging(verbose=True)
logger = get_logger("test")

# Test different log levels
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Service Layer Testing

```python
from classroom_pilot import AssignmentService, ReposService, SecretsService, AutomationService

# Test service instantiation
assignment_service = AssignmentService()
repos_service = ReposService()
secrets_service = SecretsService()
automation_service = AutomationService()

# Test service methods are available
assert hasattr(assignment_service, 'orchestrate')
assert hasattr(assignment_service, 'setup')
assert hasattr(repos_service, 'clone_repository')
assert hasattr(secrets_service, 'deploy_secrets')
assert hasattr(automation_service, 'schedule_task')

print("✓ All services instantiated successfully")
```

## 🔗 Integration Testing

### Sample Project Testing

Create realistic test scenarios:

```bash
# Basic assignment test
mkdir test_basic_assignment
cd test_basic_assignment

cat > assignment.conf << EOF
CLASSROOM_URL=https://classroom.github.com/classrooms/test-classroom
TEMPLATE_REPO_URL=https://github.com/test-org/python-basics
GITHUB_ORGANIZATION=test-classroom-org
ASSIGNMENT_FILE=assignment.conf
ASSIGNMENT_NAME=Python Basics
EOF

# Test workflow
classroom-pilot assignments setup --dry-run --verbose
classroom-pilot assignments orchestrate --dry-run --verbose
```

### Error Recovery Testing

```bash
# Test missing configuration
rm assignment.conf
classroom-pilot assignments setup --dry-run
# Expected: Graceful error with helpful message

# Test invalid URLs
echo "CLASSROOM_URL=invalid-url" > assignment.conf
classroom-pilot assignments validate
# Expected: Validation error with clear explanation
```

### Real Repository Testing

### Overview

Real repository testing validates classroom-pilot functionality using actual GitHub repositories and live data. This provides the most comprehensive validation possible, testing real-world scenarios with actual GitHub Classroom assignments.

### Prerequisites

1. **GitHub Repository Access**: Valid GitHub repository with classroom assignment
2. **GitHub Token**: Personal access token with appropriate permissions
3. **Conda Environment**: Conda installed and available
4. **Configuration Files**: Properly configured real repository settings

### Setup Instructions

#### 1. Configure Real Repository Settings

Navigate to `sample_projects/real_repo/` and edit the configuration:

```bash
cd sample_projects/real_repo/

# Edit repository configuration
vim real_repo_info.conf

# Required fields:
# CLASSROOM_URL - GitHub Classroom assignment URL
# TEMPLATE_REPO_URL - Template repository URL  
# GITHUB_ORGANIZATION - Organization name
# ASSIGNMENT_NAME - Assignment identifier
# ASSIGNMENT_FILE - Main assignment file
```

#### 2. Set Up GitHub Token

Create a GitHub Personal Access Token with these permissions:
- `repo` (Full control of private repositories)
- `read:org` (Read org and team membership)  
- `admin:repo_hook` (Admin access to repository hooks)

```bash
# Add token to configuration
echo "ghp_YOUR_TOKEN_HERE" > instructor_token.txt

# Verify token format
./scripts/test_real_repo.sh --dry-run
```

### Execution Modes

#### Quick Validation

```bash
# Validate configuration without making changes
./scripts/test_real_repo.sh --dry-run --verbose

# Test through main runner
./scripts/run_full_test.sh --real-repo
```

#### Step-by-Step Testing

```bash
# 1. Setup conda environment and clone repository
./scripts/test_real_repo.sh --setup-only

# 2. Run tests with existing environment
./scripts/test_real_repo.sh --test-only --verbose

# 3. Clean up everything
./scripts/test_real_repo.sh --cleanup-only
```

#### Development and Debugging

```bash
# Keep environment for inspection
./scripts/test_real_repo.sh --keep-env --keep-repo

# Skip cloning (use existing repository)
./scripts/test_real_repo.sh --skip-clone --test-only

# Verbose output for troubleshooting
./scripts/test_real_repo.sh --verbose --dry-run
```

### What Gets Tested

1. **Configuration Parsing**: Real repository configuration validation
2. **Environment Setup**: Conda environment creation with classroom-pilot
3. **Repository Operations**: Cloning actual GitHub repositories
4. **Assignment Setup**: Configuration generation and validation
5. **CLI Functionality**: Complete command-line interface testing
6. **Python API**: API integration with real configuration data
7. **Secrets Management**: Repository secrets handling (dry-run mode)
8. **Error Handling**: Graceful failure and recovery testing

### Security Considerations

- **Dry-Run Mode**: Most operations run in dry-run mode to prevent modifications
- **Environment Isolation**: Uses isolated conda environments
- **Token Security**: Tokens are validated but not logged
- **Automatic Cleanup**: Removes sensitive data from test environments
- **No Repository Modifications**: Real repositories are never modified

### Expected Output

```
[STEP] Validating prerequisites
[SUCCESS] ✓ Real repo config file exists
[SUCCESS] ✓ GitHub token format is valid
[STEP] Parsing real repository configuration
[DETAIL] Classroom URL: https://classroom.github.com/...
[DETAIL] Template Repo: https://github.com/org/repo
[STEP] Setting up conda test environment
[SUCCESS] ✓ Conda environment created
[STEP] Cloning student repository  
[SUCCESS] ✓ Repository cloned successfully
[STEP] Testing configuration validation
[SUCCESS] ✓ Configuration validation passed
[SUCCESS] All real repository tests passed! 🎉
```

### Troubleshooting

#### Common Issues

1. **Invalid Token**: Verify GitHub token permissions
2. **Repository Access**: Ensure token has access to specified repositories
3. **Network Issues**: Check internet connectivity and GitHub API access
4. **Conda Problems**: Verify conda installation and PATH configuration

#### Debug Commands

```bash
# Check configuration parsing
./scripts/test_real_repo.sh --dry-run

# Verify token access
curl -H "Authorization: token $(cat sample_projects/real_repo/instructor_token.txt)" https://api.github.com/user

# Test conda environment
conda info --envs

# Check repository access
git ls-remote https://github.com/ORG/REPO
```

## Performance Testing

```bash
# Test large configuration files
# Create config with many parameters
time classroom-pilot assignments validate

# Test multiple operations
time classroom-pilot assignments setup --dry-run
```

## 🔍 Advanced Testing Scenarios

### Cross-Shell Testing

```bash
# Test in different shells
bash -c "classroom-pilot --version"
zsh -c "classroom-pilot --version"
sh -c "classroom-pilot --version"
```

### Memory and Resource Testing

```python
# Memory usage testing
import psutil
import classroom_pilot

process = psutil.Process()
initial_memory = process.memory_info().rss

# Perform operations
from classroom_pilot import ConfigLoader
config = ConfigLoader()

final_memory = process.memory_info().rss
memory_increase = final_memory - initial_memory
print(f"Memory increase: {memory_increase / 1024 / 1024:.2f} MB")
```

### Dependency Conflict Testing

```bash
# Test with minimal dependencies
pip install --no-deps classroom-pilot
# Then install dependencies one by one to check conflicts

# Check for dependency issues
pip check
```

## 📊 Test Result Validation

### Success Criteria

**Installation Tests:**
- ✅ Package builds without errors
- ✅ Installs cleanly in fresh environment
- ✅ No dependency conflicts
- ✅ Entry points work correctly

**CLI Tests:**
- ✅ All commands show proper help
- ✅ Version information displays correctly
- ✅ Subcommands are accessible
- ✅ Error messages are helpful and clear

**API Tests:**
- ✅ All imports succeed
- ✅ Core functionality works
- ✅ Configuration system validates properly
- ✅ Logging system functions correctly

**Integration Tests:**
- ✅ Sample projects work end-to-end
- ✅ Error handling is graceful
- ✅ Performance is acceptable
- ✅ Memory usage is reasonable

### Failure Investigation

When tests fail:

1. **Check Environment**: Verify Python version, dependencies
2. **Review Logs**: Enable verbose logging for detailed output
3. **Isolate Issue**: Test individual components
4. **Check Documentation**: Verify expected behavior
5. **Report Issues**: Document bugs with reproduction steps

## 🔧 Test Automation

### Automated Test Script Structure

```bash
#!/bin/bash
# Main test orchestration script

set -euo pipefail

# Configuration
PACKAGE_NAME="classroom-pilot"
EXPECTED_VERSION="3.1.0a2"

# Test functions
test_installation() {
    echo "Testing installation..."
    # Implementation
}

test_cli_interface() {
    echo "Testing CLI interface..."
    # Implementation
}

test_python_api() {
    echo "Testing Python API..."
    # Implementation
}

test_integration() {
    echo "Testing integration scenarios..."
    # Implementation
}

# Main execution
main() {
    echo "Starting comprehensive test suite..."
    
    test_installation
    test_cli_interface
    test_python_api
    test_integration
    
    echo "All tests completed successfully!"
}

main "$@"
```

## 🚨 Common Issues and Solutions

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'classroom_pilot'`

**Solutions**:
- Verify package installation: `pip show classroom-pilot`
- Check Python path: `python -c "import sys; print(sys.path)"`
- Reinstall package: `pip uninstall classroom-pilot && pip install ...`

### CLI Entry Point Issues

**Problem**: `command not found: classroom-pilot`

**Solutions**:
- Check if scripts directory is in PATH
- Verify installation method (system vs user)
- Try `python -m classroom_pilot` as alternative

### Permission Errors

**Problem**: Permission denied when running scripts

**Solutions**:
- Make scripts executable: `chmod +x script.sh`
- Check directory permissions
- Use appropriate virtual environment

### Configuration Issues

**Problem**: Configuration validation failures

**Solutions**:
- Verify configuration file format
- Check required fields are present
- Validate URL formats
- Review file encoding (should be UTF-8)

## 📈 Continuous Improvement

### Adding New Tests

1. **Identify Gaps**: Areas not covered by current tests
2. **Create Test Cases**: Specific scenarios to validate
3. **Implement Tests**: Add to appropriate test scripts
4. **Document**: Update this guide with new procedures
5. **Integrate**: Add to main test orchestration

### Performance Monitoring

- Track test execution time
- Monitor memory usage during testing
- Identify slow operations
- Optimize test procedures

### Test Coverage Analysis

- Use coverage tools for Python API testing
- Ensure all CLI commands are tested
- Validate all configuration options
- Test error paths and edge cases

---

*This comprehensive testing guide ensures thorough validation of the classroom-pilot package across all use cases and environments.*