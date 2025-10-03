#!/bin/bash
#
# Test Environment Setup Script
#
# Creates isolated test environments for package testing
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Setup test environment
setup_test_environment() {
    local env_name="${1:-$(get_test_env_name)}"
    local python_version="${2:-$DEFAULT_PYTHON_VERSION}"
    local env_type="${3:-$PREFERRED_TEST_ENV}"
    
    log_info "Setting up test environment: $env_name"
    log_info "Python version: $python_version"
    log_info "Environment type: $env_type"
    
    # If conda is preferred, ensure it's available
    if [ "$env_type" = "conda" ]; then
        log_info "Checking conda availability..."
        if ! ensure_conda_available; then
            log_warning "Conda setup failed, falling back to venv"
            env_type="venv"
        fi
    fi
    
    local test_env_dir="$TEST_DIR/test_environments/$env_name"
    
    # Remove existing environment if present
    if [ -d "$test_env_dir" ]; then
        log_warning "Removing existing test environment"
        rm -rf "$test_env_dir"
    fi
    
    mkdir -p "$test_env_dir"
    
    case "$env_type" in
        "venv")
            setup_venv_environment "$test_env_dir" "$python_version"
            ;;
        "conda")
            setup_conda_environment "$env_name" "$python_version"
            ;;
        *)
            log_error "Unknown environment type: $env_type"
            return 1
            ;;
    esac
    
    log_success "Test environment setup completed: $env_name"
}

# Setup Python venv environment
setup_venv_environment() {
    local env_dir="$1"
    local python_version="$2"
    
    local python_exec=$(get_python_executable "$python_version")
    
    if [ -z "$python_exec" ]; then
        log_error "Python $python_version not found"
        return 1
    fi
    
    log_info "Creating virtual environment with $python_exec"
    
    # Create virtual environment
    "$python_exec" -m venv "$env_dir"
    
    # Activate environment
    source "$env_dir/bin/activate"
    
    # Upgrade pip
    log_info "Upgrading pip"
    pip install --upgrade pip setuptools wheel
    
    # Verify environment
    log_info "Python version: $(python --version)"
    log_info "Pip version: $(pip --version)"
    
    # Create activation script
    cat > "$env_dir/activate_test_env.sh" << EOF
#!/bin/bash
source "$env_dir/bin/activate"
echo "Test environment activated: $env_dir"
echo "Python: \$(python --version)"
echo "Pip: \$(pip --version)"
EOF
    
    chmod +x "$env_dir/activate_test_env.sh"
}

# Setup Conda environment
setup_conda_environment() {
    local env_name="$1"
    local python_version="$2"
    
    if ! command -v conda &> /dev/null; then
        log_error "Conda not found. Cannot create conda environment."
        return 1
    fi
    
    log_info "Creating conda environment: $env_name"
    
    # Remove existing environment
    conda remove --name "$env_name" --all -y 2>/dev/null || true
    
    # Create new environment
    conda create --name "$env_name" python="$python_version" -y
    
    # Activate environment
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate "$env_name"
    
    # Install pip and upgrade it
    conda install pip -y
    
    # Install requirements if requirements.txt exists
    local requirements_file="$TEST_DIR/requirements.txt"
    if [[ -f "$requirements_file" ]]; then
        log_info "Installing dependencies from requirements.txt"
        pip install -r "$requirements_file"
    else
        log_warning "No requirements.txt found at $requirements_file"
    fi
    
    # Verify environment
    log_info "Python version: $(python --version)"
    log_info "Conda environment: $CONDA_DEFAULT_ENV"
    log_info "Poetry version: $(poetry --version 2>/dev/null || echo 'Poetry not installed')"
    
    # Create activation script
    local env_dir="$TEST_DIR/test_environments/$env_name"
    mkdir -p "$env_dir"
    
    cat > "$env_dir/activate_test_env.sh" << EOF
#!/bin/bash
source "\$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$env_name"
echo "Test environment activated: $env_name"
echo "Python: \$(python --version)"
echo "Conda environment: \$CONDA_DEFAULT_ENV"
EOF
    
    chmod +x "$env_dir/activate_test_env.sh"
}

# Install package dependencies
install_test_dependencies() {
    log_info "Installing test dependencies"
    
    # Install basic testing tools
    pip install pytest pytest-cov pytest-mock
    
    # Install package dependencies if requirements file exists
    if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
        log_info "Installing from requirements.txt"
        pip install -r "$PROJECT_ROOT/requirements.txt"
    fi
    
    # Install development dependencies if available
    if [ -f "$PROJECT_ROOT/requirements-dev.txt" ]; then
        log_info "Installing development dependencies"
        pip install -r "$PROJECT_ROOT/requirements-dev.txt"
    fi
    
    log_success "Test dependencies installed"
}

# Verify test environment
verify_test_environment() {
    log_info "Verifying test environment"
    
    # Check Python version
    local python_version=$(python --version 2>&1)
    log_info "Python version: $python_version"
    
    # Check pip version
    local pip_version=$(pip --version 2>&1)
    log_info "Pip version: $pip_version"
    
    # Check available packages
    log_info "Installed packages:"
    # Show a subset of installed packages (avoid broken pipe)
    pip list 2>/dev/null | head -10 2>/dev/null || true
    
    # Verify essential tools
    if ! python -c "import sys; print('Python OK')" 2>/dev/null; then
        log_error "Python verification failed"
        return 1
    fi
    
    if ! pip --version >/dev/null 2>&1; then
        log_error "Pip verification failed"
        return 1
    fi
    
    log_success "Test environment verified successfully"
}

# Main execution
main() {
    local env_name="${1:-$(get_test_env_name)}"
    local python_version="${2:-$DEFAULT_PYTHON_VERSION}"
    local env_type="${3:-$PREFERRED_TEST_ENV}"
    
    log_info "Starting test environment setup"
    
    # Validate configuration
    if ! validate_config; then
        log_error "Configuration validation failed"
        exit 1
    fi
    
    # Setup environment
    setup_test_environment "$env_name" "$python_version" "$env_type"
    
    # Install dependencies
    install_test_dependencies
    
    # Verify environment
    verify_test_environment
    
    log_success "Test environment setup completed successfully"
    
    # Output activation instructions
    echo ""
    log_info "To activate this test environment:"
    case "$env_type" in
        "venv")
            echo "  source $TEST_DIR/test_environments/$env_name/bin/activate"
            ;;
        "conda")
            echo "  conda activate $env_name"
            ;;
    esac
    
    echo ""
    log_info "Or use the activation script:"
    echo "  source $TEST_DIR/test_environments/$env_name/activate_test_env.sh"
}

# Handle command line arguments
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi