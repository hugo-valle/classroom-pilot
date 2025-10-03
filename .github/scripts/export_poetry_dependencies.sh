#!/bin/bash
set -euo pipefail

# Export Poetry dependencies for security scanning
# This script handles Poetry export with fallback methods

source "$(dirname "$0")/workflow_utils.sh"

print_message "step" "Exporting Poetry dependencies"

# Try to install poetry export plugin if not available
if ! poetry export --help >/dev/null 2>&1; then
    print_message "info" "Installing Poetry export plugin"
    poetry self add poetry-plugin-export
fi

# Export dependencies with fallback
if poetry export -f requirements.txt --without-hashes -o requirements.txt 2>/dev/null; then
    print_message "success" "Dependencies exported to requirements.txt"
else
    print_message "warning" "Poetry export failed, creating requirements.txt from pyproject.toml"
    # Fallback: extract dependencies from pyproject.toml
    python -c "
import tomllib
with open('pyproject.toml', 'rb') as f:
    data = tomllib.load(f)
deps = data.get('tool', {}).get('poetry', {}).get('dependencies', {})
with open('requirements.txt', 'w') as f:
    for pkg, version in deps.items():
        if pkg != 'python':
            if isinstance(version, str):
                f.write(f'{pkg}{version}\n')
            else:
                f.write(f'{pkg}\n')
"
    print_message "success" "Requirements.txt created from pyproject.toml"
fi