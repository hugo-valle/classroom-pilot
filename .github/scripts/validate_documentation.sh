#!/bin/bash
set -euo pipefail

# Comprehensive documentation validation script
# Validates README, CHANGELOG, and documentation structure

source "$(dirname "$0")/workflow_utils.sh"

print_message "step" "Running comprehensive documentation validation"

validation_errors=0

# Enhanced CHANGELOG validation
if [ ! -f "docs/CHANGELOG.md" ]; then
    print_message "error" "CHANGELOG.md not found in docs/"
    validation_errors=$((validation_errors + 1))
else
    print_message "info" "Validating CHANGELOG.md format"
    
    if ! grep -q "## \[Unreleased\]" docs/CHANGELOG.md; then
        print_message "error" "CHANGELOG.md missing [Unreleased] section"
        validation_errors=$((validation_errors + 1))
    fi
    
    if ! grep -q "### Added\|### Changed\|### Fixed\|### Removed" docs/CHANGELOG.md; then
        print_message "warning" "CHANGELOG.md could benefit from standard sections (Added, Changed, Fixed, Removed)"
    fi
fi

# Enhanced README validation
print_message "info" "Validating README.md structure"
if [ ! -f "README.md" ]; then
    print_message "error" "README.md not found in root directory"
    validation_errors=$((validation_errors + 1))
else
    # Check for essential README sections
    required_sections=("Installation" "Usage" "Contributing" "License")
    for section in "${required_sections[@]}"; do
        if ! grep -qi "##.*$section\|#.*$section" README.md; then
            print_message "warning" "README.md missing recommended section: $section"
        fi
    done
fi

# Check for documentation consistency
print_message "info" "Checking documentation file consistency"
if [ -d "docs/" ]; then
    doc_files=$(find docs/ -name "*.md" -type f | wc -l)
    print_message "info" "Found $doc_files documentation files in docs/"
    
    if [ "$doc_files" -eq 0 ]; then
        print_message "warning" "No documentation files found in docs/ directory"
    fi
fi

# Check for license file
if [ ! -f "LICENSE" ] && [ ! -f "LICENSE.md" ] && [ ! -f "LICENSE.txt" ]; then
    print_message "warning" "No LICENSE file found in root directory"
fi

if [ $validation_errors -gt 0 ]; then
    print_message "error" "Documentation validation failed with $validation_errors errors"
    exit 1
else
    print_message "success" "Documentation validation completed successfully"
fi