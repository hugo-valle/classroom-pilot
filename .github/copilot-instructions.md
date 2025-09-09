# GitHub Copilot Instructions for Classroom Pilot

This document provides comprehensive instructions for AI assistants working on the `classroom-pilot` project.

## 🎯 Project Overview

**Classroom Pilot** is a comprehensive Python CLI tool for automating GitHub Classroom assignment management. It provides modular functionality for repository operations, assignment orchestration, secret management, and automation workflows.

### Key Information
- **Language**: Python 3.10+
- **CLI Framework**: Typer + Click
- **Package Manager**: Poetry
- **Testing**: pytest (153+ comprehensive tests)
- **Architecture**: Modular package structure
- **Current Version**: 3.0.1-alpha.2

## 📁 Project Structure

```
classroom_pilot/
├── classroom_pilot/          # Main package
│   ├── __init__.py          # Package initialization
│   ├── __main__.py          # Entry point
│   ├── cli.py               # Main CLI interface (Typer)
│   ├── bash_wrapper.py      # Shell command wrapper
│   ├── config.py            # Configuration management
│   ├── utils.py             # Utility functions
│   ├── assignments/         # Assignment management
│   ├── automation/          # Scheduling and batch processing
│   ├── config/              # Configuration system
│   ├── repos/               # Repository operations
│   ├── scripts/             # Shell scripts
│   └── secrets/             # Secret management
├── tests/                   # Comprehensive test suite (153 tests)
├── docs/                    # Documentation
├── .github/workflows/       # CI/CD automation
└── pyproject.toml          # Poetry configuration
```

## 🔧 Development Guidelines

### Code Standards

1. **Python Style**:
   - Follow PEP 8 conventions
   - Use type hints where applicable
   - Maintain consistent docstring format
   - Prefer f-strings for string formatting

2. **CLI Development**:
   - Use Typer for command definitions
   - Organize commands in logical sub-applications
   - Provide helpful descriptions and examples
   - Include proper error handling

3. **Testing Requirements**:
   - Maintain 100% test pass rate
   - Write tests for all new functionality
   - Use pytest fixtures for setup/teardown
   - Follow existing test patterns

### Dependency Management

**Critical Compatibility Requirements**:
```toml
python = "^3.10"
click = ">=8.0.0,<8.2.0"      # Compatible with typer
typer = ">=0.12.0"            # Latest stable version
pyyaml = "^6.0.1"
requests = "^2.31.0"
```

**Never use**:
- `typer < 0.12.0` with `click >= 8.1.3` (causes make_metavar() errors)
- Unpinned major versions for core dependencies

### Version Management

- **Semantic Versioning**: `MAJOR.MINOR.PATCH-prerelease`
- **Pre-release Format**: `alpha.X`, `beta.X`, `rc.X`
- **Version Locations** (keep synchronized):
  - `pyproject.toml` → `version = "X.Y.Z"`
  - `classroom_pilot/__init__.py` → `__version__ = "X.Y.Z"`
  - `classroom_pilot/cli.py` → version command output

## 🏗️ Architecture Patterns

### CLI Structure
```python
# Main app with sub-applications
app = typer.Typer(help="Main description")
assignments_app = typer.Typer(help="Assignment commands")
repos_app = typer.Typer(help="Repository commands")

# Add sub-apps to main app
app.add_typer(assignments_app, name="assignments")
app.add_typer(repos_app, name="repos")

# Command pattern
@assignments_app.command()
def setup(
    dry_run: bool = typer.Option(False, help="Show what would be done"),
    verbose: bool = typer.Option(False, help="Enable verbose output")
):
    """Setup assignment configuration."""
    pass
```

### Configuration Management
- Use `ConfigLoader` class for configuration handling
- Support both file-based and environment variable configuration
- Provide sensible defaults for all options
- Validate configuration before use

### Error Handling
```python
try:
    # Operation
    pass
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    raise typer.Exit(code=1)
```

## 🧪 Testing Patterns

### Test Organization
```python
# tests/test_<module>.py
import pytest
from classroom_pilot.<module> import Class

class TestClass:
    def test_method_success(self, mock_config):
        """Test successful operation."""
        pass
    
    def test_method_failure(self, mock_config):
        """Test error handling."""
        pass
```

### Fixture Usage
```python
# Use existing fixtures from conftest.py
def test_function(mock_config, temp_dir, mock_bash_wrapper):
    # Test implementation
    pass
```

### Test Categories
- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction
- **CLI Tests**: Command-line interface validation
- **Error Tests**: Exception and error handling

## 📝 Documentation Standards

### Docstring Format
```python
def function_name(param1: str, param2: int = 0) -> bool:
    """
    Brief description of function purpose.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter with default
        
    Returns:
        Description of return value
        
    Raises:
        SpecificException: When specific condition occurs
    """
    pass
```

### CLI Help Text
```python
@app.command()
def command_name(
    param: str = typer.Option(..., help="Clear, concise parameter description")
):
    """
    Command description with example usage.
    
    Example:
        classroom-pilot command-name --param value
    """
    pass
```

## 🚀 CI/CD Integration

### GitHub Actions Workflow
- **Triggers**: Git tags (`v*`), main branch updates to `pyproject.toml`
- **Testing**: Multi-Python versions (3.10, 3.11, 3.12)
- **Publishing**: Automated PyPI publication
- **Requirements**: `PYPI_API_TOKEN` repository secret

### Release Process
1. Update version in all locations
2. Update CHANGELOG.md
3. Commit changes: `git commit -m "bump: version X.Y.Z"`
4. Create tag: `git tag vX.Y.Z`
5. Push: `git push origin main --tags`
6. CI/CD handles the rest automatically

## 🔍 Common Issues and Solutions

### Typer/Click Compatibility
- **Problem**: `make_metavar() missing argument` error
- **Solution**: Use `typer >= 0.12.0` with `click >= 8.0.0,<8.2.0`

### Test Failures
- **Check**: Fixture configuration in `conftest.py`
- **Verify**: Mock objects are properly configured
- **Ensure**: Test isolation (no shared state)

### Import Errors
- **Verify**: Package structure matches imports
- **Check**: `__init__.py` files exist in all packages
- **Confirm**: Dependencies are properly installed

### CLI Issues
- **Test locally**: `poetry run classroom-pilot --help`
- **Check logs**: Enable verbose mode for debugging
- **Verify config**: Ensure configuration files are valid

## 📚 Key Resources

### Documentation Files
- `docs/PYPI_PUBLICATION.md` - PyPI publishing guide
- `docs/CICD_WORKFLOW.md` - CI/CD pipeline documentation
- `docs/PROJECT_STATUS_V3_ALPHA1.md` - Current project status

### Important Files
- `pyproject.toml` - Project configuration and dependencies
- `conftest.py` - Test fixtures and configuration
- `.github/workflows/publish.yml` - Automated publishing workflow

### External Links
- **PyPI Package**: https://pypi.org/project/classroom-pilot/
- **Repository**: https://github.com/hugo-valle/classroom-pilot
- **Documentation**: Repository README and docs/ folder

## ⚠️ Critical Reminders

1. **Always run tests** before making changes: `poetry run pytest tests/ -v`
2. **Update version** in all three locations when bumping
3. **Test CLI locally** after dependency changes
4. **Check compatibility** when updating typer/click versions
5. **Follow semantic versioning** for all releases
6. **Maintain 100% test pass rate** - no exceptions
7. **Use Poetry** for all dependency management
8. **Test in clean environment** before publishing

## 🎯 Development Workflow

1. **Start**: Create feature branch from main
2. **Develop**: Implement changes with tests
3. **Test**: Run comprehensive test suite
4. **Verify**: Test CLI functionality locally
5. **Update**: Bump version if needed
6. **Document**: Update relevant documentation
7. **Commit**: Use conventional commit messages
8. **PR**: Create pull request with clear description
9. **Merge**: Merge to main after review
10. **Release**: Tag for automated publishing

---

*This project maintains high standards for code quality, testing, and documentation. Always prioritize reliability and user experience in all changes.*
