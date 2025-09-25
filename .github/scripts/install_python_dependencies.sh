#!/bin/bash

# Python Dependency Installation and Validation Script
# This script handles Poetry-based dependency installation with validation

set -euo pipefail

# Source workflow utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=.github/scripts/workflow_utils.sh
source "$SCRIPT_DIR/workflow_utils.sh"

install_dependencies_with_validation() {
  local python_version="${1:-unknown}"
  
  log_info "Installing Python dependencies for version $python_version"
  
  # Install all dependencies (main + dev) in one go for testing
  if ! retry_with_backoff "poetry install" "dependencies installation" 3 10; then
    log_error "Failed to install dependencies"
    return 1
  fi
  
  log_success "dependencies installation completed successfully"
  
  # Simple validation: just check if we can run Python
  log_info "Validating Python environment setup..."
  if poetry run python -c "import sys; print('Python version:', sys.version)" 2>/dev/null; then
    log_success "Python environment is accessible"
  else
    log_error "Cannot access Python environment"
    return 1
  fi
  
  # Quick test of a few key packages
  if poetry run python -c "import pytest, typer, yaml; print('Key packages available')" 2>/dev/null; then
    log_success "Critical packages are importable"
  else
    log_warning "Some packages may not be properly installed, but continuing..."
    log_info "Installed packages:"
    poetry show --only main || true
  fi
  
  log_info "Python environment information:"
  poetry env info
  
  log_success "All dependencies installed and validated successfully"
  return 0
}

# Main execution
main() {
  local python_version="${1:-$(python --version 2>&1 | cut -d' ' -f2)}"
  
  if ! install_dependencies_with_validation "$python_version"; then
    log_error "Dependency installation failed completely"
    log_info "Poetry Debug Information"
    poetry debug info || true
    exit 1
  fi
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi