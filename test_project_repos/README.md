# 🧪 Local Testing Workflow for Classroom Pilot

This directory contains comprehensive testing tools and documentation for validating the `classroom-pilot` Python package before releases.

## Directory Structure

```
test_project_repos/
├── README.md                    # This file - overview and usage
├── docs/                        # Comprehensive documentation
│   ├── TESTING_GUIDE.md         # Detailed testing procedures (430+ lines)
│   ├── TEST_SCENARIOS.md        # Test scenario documentation (320+ lines)
│   └── TROUBLESHOOTING.md       # Issue resolution guide (490+ lines)
├── scripts/                     # Test automation scripts (all executable)
│   ├── run_full_test.sh         # Main test orchestration (400+ lines)
│   ├── config.sh                # Configuration management (200+ lines)
│   ├── setup_test_env.sh        # Environment setup (250+ lines)
│   ├── test_installation.sh     # Package installation testing (300+ lines)
│   ├── test_cli_interface.sh    # CLI functionality testing (400+ lines)
│   ├── test_python_api.py       # Python API testing (330+ lines)
│   ├── test_integration.sh      # Integration testing (350+ lines)
│   ├── test_real_repo.sh        # Real repository testing (600+ lines)
│   ├── test_runner.sh           # Individual test suite runner (400+ lines)
│   └── cleanup.sh               # Environment cleanup (300+ lines)
├── sample_projects/             # Test project examples
│   ├── basic_assignment/        # Simple assignment example
│   │   ├── assignment.conf      # Basic configuration
│   │   ├── README.md            # Assignment instructions
│   │   └── src/main.py          # Starter code
│   ├── advanced_assignment/     # Complex assignment example
│   │   └── assignment.conf      # Advanced configuration
│   ├── real_repo/               # Real repository testing configuration
│   │   ├── real_repo_info.conf  # Real repository configuration
│   │   └── instructor_token.txt # GitHub token for real testing
│   └── error_scenarios/         # Error condition examples (auto-generated)
└── reports/                     # Generated test reports (auto-created)
    ├── html/                    # HTML test reports
    ├── junit/                   # JUnit XML reports
    └── logs/                    # Test execution logs
```

## 🚀 Quick Start

### Run Complete Test Suite

```bash
# From the classroom_pilot root directory
cd test_project_repos
./scripts/run_full_test.sh
```

### Run Individual Test Components

```bash
# Test package installation
./scripts/test_installation.sh

# Test CLI interface
./scripts/test_cli_interface.sh

# Test Python API
python scripts/test_python_api.py

# Test integration scenarios
./scripts/test_integration.sh
```

## 📋 Test Coverage

### ✅ Installation Testing
- Package building with Poetry
- Clean environment installation
- Dependency resolution validation
- Cross-platform compatibility

### ✅ CLI Interface Testing
- Command structure validation
- Help system functionality
- Subcommand organization
- Error handling and user feedback

### ✅ Python API Testing
- Module imports and exports
- Core functionality validation
- Configuration system testing
- Logging and error handling

### ✅ Integration Testing
- Real-world workflow scenarios
- Sample project configurations
- End-to-end command execution
- Error recovery and validation

### ✅ Real Repository Testing
- Actual GitHub repository cloning and testing
- Real workflow validation with live repositories
- Conda environment setup and isolation
- Complete assignment configuration generation
- End-to-end testing with real data
- Automatic cleanup of test environments

## 🎯 Usage Scenarios

### Real Repository Testing (New!)

**Prerequisites:**
1. Set up configuration in `sample_projects/real_repo/`:
   - Edit `real_repo_info.conf` with your actual GitHub Classroom assignment details
   - Add your GitHub token to `instructor_token.txt`
   - See `sample_projects/real_repo/README.md` for detailed setup instructions

**Quick Start:**
```bash
# Test configuration setup (safe dry-run)
./scripts/test_real_repo.sh --dry-run

# Run complete real repository testing
./scripts/run_full_test.sh --real-repo

# Test specific real repository functionality
./scripts/test_runner.sh --real-repo --verbose
```

**Advanced Usage:**
```bash
# Setup environment only (for debugging)
./scripts/test_real_repo.sh --setup-only --keep-env

# Run tests with existing environment
./scripts/test_real_repo.sh --test-only --verbose

# Keep cloned repository for inspection
./scripts/test_real_repo.sh --keep-repo --verbose

# Clean up specific components
./scripts/test_real_repo.sh --cleanup-only
```

### Before Release Testing
```bash
# Complete validation before creating a release
./scripts/run_full_test.sh --comprehensive

# Test with real GitHub repository (requires real_repo_info.conf)
./scripts/run_full_test.sh --real-repo

# Generate detailed test report
./scripts/run_full_test.sh --report
```

### Development Testing
```bash
# Quick validation during development
./scripts/run_full_test.sh --quick

# Test specific functionality
# Test with real GitHub repository (requires setup)
./scripts/run_full_test.sh --real-repo

# Test specific real repository functionality
./scripts/test_runner.sh real-repo --verbose
```

### CI/CD Integration
```bash
# Automated testing in CI pipeline
./scripts/run_full_test.sh --ci-mode
```

## 📊 Test Reports

Test results are automatically generated in the `reports/` directory:

- `test_report_YYYYMMDD_HHMMSS.md` - Comprehensive test results
- `installation_log.txt` - Installation process details
- `cli_test_output.txt` - CLI command testing output
- `api_test_results.json` - Python API test results
- `integration_results.txt` - Integration test outcomes

## 🔧 Configuration

Edit `scripts/config.sh` to customize test behavior:

```bash
# Test environment settings
TEST_PYTHON_VERSIONS=("3.10" "3.11" "3.12")
TEST_ENVIRONMENTS=("venv" "conda")
COMPREHENSIVE_TESTING=true
CLEANUP_AFTER_TESTS=true

# Package settings
PACKAGE_NAME="classroom-pilot"
EXPECTED_VERSION="3.1.0a2"
CLI_COMMAND="classroom-pilot"
```

## 🆘 Troubleshooting

Common issues and solutions:

- **Permission Errors**: Ensure scripts are executable: `chmod +x scripts/*.sh`
- **Python Version Issues**: Install required Python versions or update config
- **Environment Conflicts**: Run cleanup script: `./scripts/cleanup_test_env.sh`
- **Package Build Failures**: Check Poetry configuration and dependencies

For detailed troubleshooting, see `docs/TROUBLESHOOTING.md`.

## 🤝 Contributing

To add new test scenarios:

1. Create test script in `scripts/`
2. Add sample project in `sample_projects/`
3. Update documentation in `docs/`
4. Add test case to main orchestration script

## 📚 Documentation

- [`docs/TESTING_GUIDE.md`](docs/TESTING_GUIDE.md) - Comprehensive testing documentation
- [`docs/TEST_SCENARIOS.md`](docs/TEST_SCENARIOS.md) - Detailed test scenarios
- [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) - Solutions for common issues
- [`docs/REAL_REPO_QUICK_REFERENCE.md`](docs/REAL_REPO_QUICK_REFERENCE.md) - Quick reference for real repository testing
- [`sample_projects/real_repo/README.md`](sample_projects/real_repo/README.md) - Real repository testing setup guide

---

*This testing framework ensures the `classroom-pilot` package is thoroughly validated before release, providing confidence in package quality and user experience.*