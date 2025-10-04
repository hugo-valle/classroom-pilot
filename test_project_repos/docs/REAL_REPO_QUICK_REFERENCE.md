# Real Repository Testing - Quick Reference

## 🚀 Quick Start

### 1. Setup Configuration
```bash
cd test_project_repos/sample_projects/real_repo/
# Edit real_repo_info.conf with your repository details
# Add your GitHub token to instructor_token.txt
```

### 2. Run Tests
```bash
# Quick validation (dry-run)
./scripts/test_real_repo.sh --dry-run

# Full testing
./scripts/run_full_test.sh --real-repo
```

## 📋 Command Reference

### Main Commands
| Command | Description |
|---------|-------------|
| `./scripts/run_full_test.sh --real-repo` | Complete real repository testing |
| `./scripts/test_runner.sh real-repo` | Real repository tests via test runner |
| `./scripts/test_real_repo.sh` | Direct real repository testing |

### Common Options
| Option | Description |
|--------|-------------|
| `--dry-run` | Show what would be done without executing |
| `--verbose` | Enable detailed output |
| `--setup-only` | Only set up the test environment |
| `--test-only` | Only run tests (assume environment exists) |
| `--cleanup-only` | Only clean up test environment |
| `--keep-env` | Keep conda environment after testing |
| `--keep-repo` | Keep cloned repository after testing |
| `--skip-clone` | Skip repository cloning (use existing) |

## 🔧 Configuration Files

### Required Files (in `sample_projects/real_repo/`)
- **`real_repo_info.conf`** - Repository and assignment configuration
- **`instructor_token.txt`** - GitHub personal access token

### Key Configuration Fields
```bash
CLASSROOM_URL="https://classroom.github.com/classrooms/ID/assignments/NAME"
TEMPLATE_REPO_URL="https://github.com/ORG/REPO"
GITHUB_ORGANIZATION="your-org"
ASSIGNMENT_NAME="assignment-name"
ASSIGNMENT_FILE="main.py"
```

## 🛠️ Common Workflows

### Development Testing
```bash
# Setup and keep environment for debugging
./scripts/test_real_repo.sh --setup-only --keep-env

# Run tests with existing environment
./scripts/test_real_repo.sh --test-only --verbose

# Clean up when done
./scripts/test_real_repo.sh --cleanup-only
```

### CI/CD Integration
```bash
# Complete testing with cleanup
./scripts/run_full_test.sh --real-repo --cleanup

# Headless testing
CI_MODE=1 ./scripts/test_real_repo.sh --verbose
```

### Debugging
```bash
# Dry-run with maximum verbosity
./scripts/test_real_repo.sh --dry-run --verbose

# Keep everything for inspection
./scripts/test_real_repo.sh --keep-env --keep-repo --verbose

# Test individual components
conda activate classroom-pilot-real-test
classroom-pilot --version
```

## 🔍 Troubleshooting

### Quick Diagnostics
```bash
# Check configuration format
./scripts/test_real_repo.sh --dry-run

# Verify GitHub token
curl -H "Authorization: token $(cat sample_projects/real_repo/instructor_token.txt)" \
     https://api.github.com/user

# Test repository access
git ls-remote https://github.com/ORG/REPO

# Check conda
conda --version && conda info
```

### Common Issues
| Issue | Solution |
|-------|----------|
| "Config file not found" | Check file path: `sample_projects/real_repo/real_repo_info.conf` |
| "Invalid token format" | Ensure token starts with `ghp_` and is 40 characters |
| "Repository access denied" | Verify token has `repo` permissions |
| "Conda environment failed" | Check conda installation and PATH |

## 📊 What Gets Tested

1. ✅ **Prerequisites Validation** - Configuration files, tokens, dependencies
2. ✅ **Configuration Parsing** - Real repository data extraction
3. ✅ **Environment Setup** - Conda environment with classroom-pilot
4. ✅ **Repository Operations** - Clone actual GitHub repositories
5. ✅ **Assignment Setup** - Configuration generation and validation
6. ✅ **CLI Testing** - Complete command-line interface validation
7. ✅ **Python API Testing** - API integration with real configuration
8. ✅ **Secrets Management** - Repository secrets handling (dry-run)
9. ✅ **Cleanup** - Environment and repository cleanup

## 🔒 Security Notes

- Most operations run in **dry-run mode** to prevent repository modifications
- Uses **isolated conda environments** to avoid system contamination
- **GitHub tokens** are validated but never logged or exposed
- **Automatic cleanup** removes sensitive data from test environments
- **Real repositories** are never modified during testing

## 📚 More Information

- **Setup Guide**: `sample_projects/real_repo/README.md`
- **Full Documentation**: `docs/TESTING_GUIDE.md`
- **Troubleshooting**: `docs/TROUBLESHOOTING.md`
- **Test Scenarios**: `docs/TEST_SCENARIOS.md`