#!/bin/bash
set -euo pipefail

# Export Poetry dependencies for security scanning
# This script handles Poetry export with fallback methods

source "$(dirname "$0")/workflow_utils.sh"

print_message "step" "Exporting Poetry dependencies"

# Check if Poetry is available
if ! command -v poetry >/dev/null 2>&1; then
    print_message "warning" "Poetry not found, installing Poetry..."
    
    # Install Poetry using the official installer
    if curl -sSL https://install.python-poetry.org | python3 -; then
        export PATH="$HOME/.local/bin:$PATH"
        print_message "success" "Poetry installed successfully"
    else
        print_message "error" "Failed to install Poetry, falling back to pyproject.toml parsing"
        
        # Fallback: Extract dependencies from pyproject.toml
        if command -v python3 >/dev/null 2>&1 && [[ -f pyproject.toml ]]; then
            print_message "info" "Extracting dependencies from pyproject.toml..."
            python3 -c "
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        import toml as tomllib_alt
        
        with open('pyproject.toml', 'r') as f:
            data = tomllib_alt.load(f)
        deps = data.get('tool', {}).get('poetry', {}).get('dependencies', {})
        with open('requirements.txt', 'w') as f:
            for pkg, version in deps.items():
                if pkg != 'python':
                    if isinstance(version, str):
                        f.write(f'{pkg}{version.replace(\"^\", \">=\")}\n')
                    else:
                        f.write(f'{pkg}\n')
        exit(0)

with open('pyproject.toml', 'rb') as f:
    data = tomllib.load(f)
deps = data.get('tool', {}).get('poetry', {}).get('dependencies', {})
with open('requirements.txt', 'w') as f:
    for pkg, version in deps.items():
        if pkg != 'python':
            if isinstance(version, str):
                f.write(f'{pkg}{version.replace(\"^\", \">=\")}\n')
            else:
                f.write(f'{pkg}\n')
" && print_message "success" "Dependencies extracted from pyproject.toml"
            return 0
        else
            print_message "error" "Cannot extract dependencies without Poetry or Python3"
            return 1
        fi
    fi
fi

# Try to install poetry export plugin if not available
if ! poetry export --help >/dev/null 2>&1; then
    print_message "info" "Installing Poetry export plugin"
    if ! poetry self add poetry-plugin-export; then
        print_message "warning" "Failed to install export plugin, continuing anyway"
    fi
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