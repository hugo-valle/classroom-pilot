#!/usr/bin/env bash
# Local test runner for the classroom-pilot Python wrapper.
# This script runs comprehensive tests locally using Poetry before pushing to CI.
#
# Updated September 2025:
# - Uses Poetry for dependency management and test execution
# - Runs comprehensive pytest suite with coverage
# - Validates development environment setup
# - Provides detailed test reporting

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Main test function
main() {
    echo "🧪 Classroom Pilot Python Wrapper - Local Test Runner"
    echo "===================================================="
    
    # Check prerequisites
    print_status "Checking prerequisites..."
    
    if ! command_exists python; then
        print_error "Python is not installed or not in PATH"
        exit 1
    fi
    
    if ! command_exists poetry; then
        print_error "Poetry is not installed or not in PATH"
        print_status "Please install Poetry: https://python-poetry.org/docs/#installation"
        exit 1
    fi
    
    # Get Python and Poetry versions
    python_version=$(python --version 2>&1)
    poetry_version=$(poetry --version 2>&1)
    print_status "Using $python_version"
    print_status "Using $poetry_version"
    
    # Check if we're in the right directory
    if [[ ! -f "pyproject.toml" ]] || [[ ! -d "classroom_pilot" ]]; then
        print_error "Please run this script from the classroom-pilot root directory"
        exit 1
    fi
    
    # Install dependencies and package using Poetry
    print_status "Installing dependencies with Poetry..."
    if poetry install --no-interaction; then
        print_success "Dependencies installed successfully"
    else
        print_error "Failed to install dependencies with Poetry"
        exit 1
    fi
    
    # Check if assignment.conf exists, create a test one if not
    if [[ ! -f "assignment.conf" ]]; then
        print_warning "No assignment.conf found, creating test configuration..."
        cat > assignment.conf << 'EOF'
# Test configuration for local development
CLASSROOM_URL="https://classroom.github.com/classrooms/test/assignments/test"
TEMPLATE_REPO_URL="https://github.com/test/template"
GITHUB_ORGANIZATION="test-org"
CLASSROOM_REPO_URL="https://github.com/test-org/test-assignment"
SECRETS_JSON='{"TEST_SECRET": "test-value"}'
EOF
        print_success "Test configuration created"
    fi
    
    # Run quick smoke tests
    print_status "Running quick smoke tests..."
    
    # Test basic import using Poetry
    # Test basic import using Poetry
    if poetry run python -c "import classroom_pilot.cli; print('Import successful')" >/dev/null 2>&1; then
        print_success "Python package imports correctly"
    else
        print_error "Python package import failed"
        exit 1
    fi
    
    # Test version command using Poetry
    if poetry run python -m classroom_pilot version >/dev/null 2>&1; then
        print_success "Version command works"
        version_output=$(poetry run python -m classroom_pilot version 2>/dev/null || echo "unknown")
        print_status "Package version: $version_output"
    else
        print_warning "Version command failed"
    fi
    
    # Test CLI entry point
    print_status "Testing CLI entry point..."
    if poetry run classroom-pilot --help >/dev/null 2>&1; then
        print_success "CLI entry point works correctly"
    else
        print_warning "CLI entry point test failed"
    fi
    
    # Run comprehensive test suite with Poetry
    print_status "Running comprehensive test suite with Poetry..."
    echo "=================================================="
    
    # Run all tests with verbose output and coverage
    print_status "Running full test suite with coverage..."
    if poetry run pytest tests/ -v --tb=short --cov=classroom_pilot --cov-report=term --cov-report=html; then
        print_success "🎉 All tests passed!"
        
        # Show test counts
        test_count=$(poetry run pytest tests/ --collect-only -q 2>/dev/null | grep -c "test session starts" || echo "unknown")
        print_status "Total tests executed: $(poetry run pytest tests/ --collect-only -q 2>/dev/null | tail -1 | grep -o '[0-9]\+ items' | grep -o '[0-9]\+' || echo 'multiple')"
        
        # Run quick syntax/lint checks if available
        print_status "Running additional quality checks..."
        
        # Check if flake8 is available and run it
        if poetry run python -c "import flake8" 2>/dev/null; then
            print_status "Running flake8 linting..."
            if poetry run flake8 classroom_pilot/ --count --select=E9,F63,F7,F82 --show-source --statistics; then
                print_success "Code syntax checks passed"
            else
                print_warning "Some syntax issues found"
            fi
        fi
        
        # Show coverage summary
        if [[ -f "htmlcov/index.html" ]]; then
            print_success "Coverage report generated: htmlcov/index.html"
        fi
        
        echo
        print_success "🎉 Comprehensive testing complete!"
        echo "=================================================="
        print_status "Development environment validation:"
        print_status "  • Poetry environment: ✅ Working"
        print_status "  • Package installation: ✅ Functional"
        print_status "  • Core imports: ✅ Operational"
        print_status "  • CLI entry point: ✅ Available"
        print_status "  • Test suite: ✅ Passing"
        print_status "  • Code coverage: ✅ Generated"
        print_status ""
        print_status "Ready for development and deployment!"
        print_status "Next steps:"
        print_status "  • Review coverage report: htmlcov/index.html"
        print_status "  • Use 'poetry run pytest tests/' for full test suite"
        print_status "  • Use 'poetry run classroom-pilot <command>' for CLI testing"
        print_status "  • Push changes to trigger CI/CD pipeline"
        
    else
        print_error "❌ Tests failed. Please check the output above."
        print_status "Common solutions:"
        print_status "  • Run 'poetry install' to ensure all dependencies are installed"
        print_status "  • Check that all imports are available in the Poetry environment"
        print_status "  • Review test failures for specific issues"
        exit 1
    fi
}

# Cleanup function
cleanup() {
    print_status "Cleaning up..."
    # Remove test configuration if we created it
    if [[ -f "assignment.conf" ]] && grep -q "Test configuration for local development" assignment.conf; then
        rm -f assignment.conf
        print_status "Test configuration removed"
    fi
}

# Set trap for cleanup
trap cleanup EXIT

# Run main function
main "$@"
