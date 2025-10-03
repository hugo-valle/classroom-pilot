#!/bin/bash
set -euo pipefail

# Poetry installation with retry logic
# Handles robust Poetry installation for CI environments

source "$(dirname "$0")/workflow_utils.sh"

PYTHON_VERSION="${1:-3.10}"

install_poetry_with_retry() {
    print_message "info" "Installing Poetry for Python $PYTHON_VERSION"
    
    if ! retry_with_backoff "pip install poetry" "Poetry installation" 3 5; then
        print_message "error" "Failed to install Poetry after 3 attempts"
        return 1
    fi
    
    poetry config virtualenvs.create true
    poetry config virtualenvs.in-project true
    poetry --version
    
    print_message "success" "Poetry installation completed successfully"
    return 0
}

if ! install_poetry_with_retry; then
    print_message "error" "Poetry installation failed completely"
    exit 1
fi