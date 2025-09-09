# Tests Directory

This directory contains all tests for the classroom-pilot Python wrapper.

## 📁 Test Organization

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # pytest configuration and fixtures
├── test_cli.py                 # CLI command tests
├── test_config.py              # Configuration loading tests
├── test_bash_wrapper.py        # BashWrapper functionality tests
├── test_comprehensive.py       # Comprehensive integration tests
└── fixtures/                   # Test data and fixtures
    ├── test_data.py            # Test data constants
    ├── test_config.conf        # Sample configuration file
    └── sample_batch.txt        # Sample batch operation file
```

## 🧪 Test Types

### Unit Tests (pytest-based)
- **test_cli.py**: Tests CLI commands and argument parsing
- **test_config.py**: Tests configuration loading and validation
- **test_bash_wrapper.py**: Tests BashWrapper methods and integration

### Integration Tests
- **test_comprehensive.py**: Full end-to-end testing of all functionality

### Test Fixtures
- **conftest.py**: Shared pytest fixtures and configuration
- **fixtures/**: Test data, sample files, and mock configurations

## 🚀 Running Tests

### Quick Test (Basic Functionality)
```bash
make test
```

### Unit Tests (pytest)
```bash
make test-unit
# or directly:
pytest tests/ -v
```

### Comprehensive Tests
```bash
make test-full
# or directly:
python tests/test_comprehensive.py
```

### Integration Tests
```bash
make test-integration
```

### All Tests
```bash
make check-all
```

### With Coverage
```bash
pytest tests/ --cov=classroom_pilot --cov-report=html
```

## 🔧 Test Configuration

### Environment Setup
Tests use shared fixtures defined in `conftest.py`:
- `test_config_data`: Sample configuration data
- `test_config`: Configuration instance for testing
- `test_wrapper`: BashWrapper instance with dry-run enabled
- `temp_config_file`: Temporary configuration file
- `temp_directory`: Temporary directory for file operations

### Test Data
Test fixtures and sample data are stored in `fixtures/`:
- `test_config.conf`: Valid test configuration
- `sample_batch.txt`: Sample batch operations file
- `test_data.py`: Python constants for test data

## 📋 Test Guidelines

### Writing Tests
1. **Use pytest fixtures** for shared setup and configuration
2. **Follow naming convention**: `test_*` for test functions
3. **Group related tests** in classes with descriptive names
4. **Use descriptive test names** that explain what is being tested
5. **Test both success and failure cases**

### Test Structure
```python
class TestFeatureName:
    """Test description."""
    
    def test_specific_behavior(self, fixture_name):
        """Test specific behavior description."""
        # Arrange
        # Act  
        # Assert
```

### Best Practices
- **Use dry-run mode** for tests that execute bash scripts
- **Mock external dependencies** when necessary
- **Test error conditions** as well as success paths
- **Keep tests independent** - no test should depend on another
- **Use temporary files/directories** for file system tests

## 🎯 Test Coverage

### Current Coverage Areas
- ✅ CLI command execution and argument parsing
- ✅ Configuration loading and validation
- ✅ BashWrapper script integration
- ✅ Error handling and edge cases
- ✅ Package structure and imports
- ✅ Environment variable handling

### Adding New Tests
When adding new functionality:
1. Add unit tests to the appropriate `test_*.py` file
2. Add integration tests to `test_comprehensive.py` if needed
3. Update fixtures in `conftest.py` if new test data is needed
4. Run the full test suite to ensure no regressions

## 🐛 Debugging Tests

### Running Specific Tests
```bash
# Single test file
pytest tests/test_cli.py -v

# Specific test class
pytest tests/test_cli.py::TestBasicCLI -v

# Specific test method
pytest tests/test_cli.py::TestBasicCLI::test_help_command -v
```

### Verbose Output
```bash
pytest tests/ -v -s  # -s shows print statements
```

### Failed Test Details
```bash
pytest tests/ --tb=long  # Detailed traceback
```

## 📊 Test Reports

Tests generate various reports:
- **JSON Report**: `test_report.json` (from comprehensive tests)
- **Coverage Report**: `htmlcov/` directory (when using --cov-report=html)
- **pytest Output**: Console output with test results

## 🔄 Continuous Integration

Tests are automatically run in CI/CD via:
- **GitHub Actions**: `.github/workflows/test-python-wrapper.yml`
- **Multi-Python Testing**: Python 3.10-3.12
- **Cross-Platform**: Linux, macOS, Windows (when configured)

## 🛠️ Development Workflow

1. **Before making changes**: Run `make test` for quick validation
2. **During development**: Run specific test files as needed
3. **Before committing**: Run `make test-unit` for full unit test suite
4. **Before pushing**: Run `make check-all` for comprehensive validation

This test organization ensures reliable, maintainable, and comprehensive testing of the classroom-pilot Python wrapper.
