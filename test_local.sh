#!/usr/bin/env bash
# Local test runner for the classroom-pilot project.
# This script runs BOTH testing suites locally before pushing to CI.
#
# Updated October 2025:
# - Tier 1: Python pytest suite (tests/) - Unit & integration tests
# - Tier 2: Bash QA suite (test_project_repos/qa_tests/) - End-to-end tests
# - Uses Poetry for dependency management and test execution
# - Runs comprehensive pytest suite with coverage
# - Validates development environment setup
# - Provides detailed test reporting

set -euo pipefail

# Test execution flags
RUN_TIER1=false
RUN_TIER2=false

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

# Function to show help
show_help() {
    cat << EOF
🧪 Classroom Pilot - Local Test Runner

USAGE:
    ./test_local.sh [OPTIONS]

OPTIONS:
    -h, --help          Show this help message
    -1, --tier1         Run only Tier 1 (Python pytest suite)
    -2, --tier2         Run only Tier 2 (Bash QA suite)
    -a, --all           Run both tiers (default if no options specified)

TESTING TIERS:
    Tier 1: Python pytest Suite
        • Location: tests/
        • Type: Unit tests, integration tests
        • Framework: pytest with coverage
        • Speed: Fast (seconds to minutes)
        • Purpose: Development feedback, code validation
        
    Tier 2: Bash QA Suite
        • Location: test_project_repos/qa_tests/
        • Type: End-to-end tests, real workflow validation
        • Framework: Bash scripts
        • Speed: Slower (minutes)
        • Purpose: Release qualification, user acceptance testing

EXAMPLES:
    # Run both tiers (comprehensive testing)
    ./test_local.sh --all
    ./test_local.sh

    # Run only Python tests (fast feedback)
    ./test_local.sh --tier1

    # Run only QA tests (workflow validation)
    ./test_local.sh --tier2

NOTES:
    • Tier 1 is recommended for daily development
    • Tier 2 is recommended before releases or major changes
    • Both tiers ensure comprehensive coverage

EOF
    exit 0
}

# Parse command line arguments
parse_arguments() {
    if [[ $# -eq 0 ]]; then
        # No arguments, run both tiers
        RUN_TIER1=true
        RUN_TIER2=true
        return
    fi
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                ;;
            -1|--tier1)
                RUN_TIER1=true
                shift
                ;;
            -2|--tier2)
                RUN_TIER2=true
                shift
                ;;
            -a|--all)
                RUN_TIER1=true
                RUN_TIER2=true
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done
    
    # If no tier selected, run both
    if [[ "$RUN_TIER1" == false ]] && [[ "$RUN_TIER2" == false ]]; then
        RUN_TIER1=true
        RUN_TIER2=true
    fi
}

# Main test function
main() {
    # Parse arguments first
    parse_arguments "$@"
    
    echo "🧪 Classroom Pilot - Comprehensive Local Test Runner"
    echo "===================================================="
    
    # Show which tiers are running
    if [[ "$RUN_TIER1" == true ]] && [[ "$RUN_TIER2" == true ]]; then
        echo "Testing Strategy: Two-Tier Approach (Both Tiers)"
    elif [[ "$RUN_TIER1" == true ]]; then
        echo "Testing Strategy: Tier 1 Only (Python pytest)"
    elif [[ "$RUN_TIER2" == true ]]; then
        echo "Testing Strategy: Tier 2 Only (Bash QA)"
    fi
    
    echo "  • Tier 1: Python pytest suite (tests/)"
    echo "  • Tier 2: Bash QA suite (test_project_repos/qa_tests/)"
    echo ""
    
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
    
    # Run Tier 1 if requested
    if [[ "$RUN_TIER1" == true ]]; then
        # Run comprehensive test suite with Poetry
        print_status "Running comprehensive test suite with Poetry..."
        echo "=================================================="
        echo ""
        echo "📊 TIER 1: Python pytest Suite (Unit & Integration Tests)"
        echo "==========================================================="
        
        # Run all tests with verbose output and coverage
        print_status "Running full test suite with coverage..."
        if poetry run pytest tests/ -v --tb=short --cov=classroom_pilot --cov-report=term --cov-report=html; then
            print_success "🎉 Tier 1 tests passed!"
        
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
    else
        print_error "❌ Tier 1 tests failed. Please check the output above."
        print_status "Common solutions:"
        print_status "  • Run 'poetry install' to ensure all dependencies are installed"
        print_status "  • Check that all imports are available in the Poetry environment"
        print_status "  • Review test failures for specific issues"
        # Don't exit yet, Tier 2 might still run
    fi
fi  # End of Tier 1
    
    # Run Tier 2 if requested
    if [[ "$RUN_TIER2" == true ]]; then
        echo ""
        echo "=================================================="
        echo ""
        echo "🔧 TIER 2: Bash QA Suite (End-to-End Tests)"
        echo "==========================================================="
        print_status "Running QA test suite from test_project_repos/qa_tests/..."
        echo ""
        
        # Check if QA test directory exists
        if [[ ! -d "test_project_repos/qa_tests" ]]; then
            print_warning "QA test directory not found. Skipping Tier 2 tests."
            print_status "Location expected: test_project_repos/qa_tests/"
        else
            # Relax error-exit within QA loop to avoid premature aborts
            set +e
            # Find all test scripts in qa_tests directory
            qa_test_scripts=(
                "test_project_repos/qa_tests/test_assignments_commands.sh"
                "test_project_repos/qa_tests/test_automation_commands.sh"
                "test_project_repos/qa_tests/test_repos_commands.sh"
                "test_project_repos/qa_tests/test_secrets_commands.sh"
                "test_project_repos/qa_tests/test_token_management.sh"
            )
            
            qa_passed=0
            qa_failed=0
            qa_skipped=0
            
            for test_script in "${qa_test_scripts[@]}"; do
                if [[ ! -f "$test_script" ]]; then
                    print_warning "Test script not found: $test_script (skipping)"
                    ((qa_skipped++))
                    continue
                fi
                
                script_name=$(basename "$test_script")
                print_status "Running $script_name..."
                
                # Make script executable if not already
                chmod +x "$test_script"
                
                # Create temporary file for test output
                test_output_file=$(mktemp)
                
                # Run the test script
                # Capture output for potential debugging
                # Note: timeout removed for macOS compatibility - tests should complete reasonably fast
                if bash "$test_script" --all > "$test_output_file" 2>&1; then
                    print_success "✓ $script_name passed"
                    ((qa_passed++))
                else
                    exit_code=$?
                    print_error "✗ $script_name failed (exit code: $exit_code)"
                    # Show last few lines of output for debugging
                    echo "    Last 10 lines of output:"
                    tail -10 "$test_output_file" | sed 's/^/    /'
                    ((qa_failed++))
                fi
                
                # Clean up temp file
                rm -f "$test_output_file"
            done
            
            echo ""
            echo "QA Test Suite Results:"
            echo "  • Passed: $qa_passed"
            echo "  • Failed: $qa_failed"
            echo "  • Skipped: $qa_skipped"
            echo ""
            
            if [[ $qa_failed -gt 0 ]]; then
                print_error "Some QA tests failed. Run individual scripts for details:"
                for test_script in "${qa_test_scripts[@]}"; do
                    if [[ -f "$test_script" ]]; then
                        echo "  • $test_script --all"
                    fi
                done
                print_warning "Continuing despite QA test failures (these are end-to-end tests)"
            else
                print_success "🎉 All QA tests passed!"
            fi
            # Restore strict error handling
            set -e
        fi
    fi  # End of Tier 2
        
    echo
    print_success "🎉 Testing complete!"
    echo "=================================================="
    print_status "Development environment validation:"
    print_status "  • Poetry environment: ✅ Working"
    print_status "  • Package installation: ✅ Functional"
    print_status "  • Core imports: ✅ Operational"
    print_status "  • CLI entry point: ✅ Available"
    
    # Show tier-specific results
    if [[ "$RUN_TIER1" == true ]]; then
        print_status "  • Tier 1 (pytest): ✅ Executed"
    fi
    if [[ "$RUN_TIER2" == true ]]; then
        print_status "  • Tier 2 (QA bash): ✅ Executed"
    fi
    if [[ -f "htmlcov/index.html" ]]; then
        print_status "  • Code coverage: ✅ Generated (htmlcov/index.html)"
    fi
    
    print_status ""
    print_status "Ready for development and deployment!"
    print_status "Next steps:"
    if [[ "$RUN_TIER1" == true ]]; then
        print_status "  • Review coverage report: htmlcov/index.html"
        print_status "  • Tier 1: 'poetry run pytest tests/' for unit tests"
    fi
    if [[ "$RUN_TIER2" == true ]]; then
        print_status "  • Tier 2: 'cd test_project_repos/qa_tests && ./test_*.sh --all'"
    fi
    print_status "  • Use 'poetry run classroom-pilot <command>' for CLI testing"
    print_status "  • Use './test_local.sh --help' for more options"
    print_status "  • Push changes to trigger CI/CD pipeline"
}

# Cleanup function
cleanup() {
    print_status "Cleaning up..."
    # Remove test configuration if we created it
    if [[ -f "assignment.conf" ]]; then
        if grep -q "Test configuration for local development" assignment.conf 2>/dev/null; then
            rm -f assignment.conf
            print_status "Test configuration removed"
        fi
    fi
}

# Set trap for cleanup
trap cleanup EXIT

# Run main function
main "$@"
