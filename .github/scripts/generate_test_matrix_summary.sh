#!/bin/bash
set -euo pipefail

# Test matrix summary generator
# Creates comprehensive summary of Python test matrix results

source "$(dirname "$0")/workflow_utils.sh"

TEST_RESULT="${1:-success}"

print_message "info" "Python Test Matrix Summary"
echo "=================================="

success_count=0
failure_count=0

if [ "$TEST_RESULT" = "success" ]; then
    print_message "success" "Python wrapper tests: PASSED"
    success_count=$((success_count + 1))
else
    print_message "error" "Python wrapper tests: FAILED"
    failure_count=$((failure_count + 1))
fi

echo "Summary: $success_count passed, $failure_count failed"

if [ $failure_count -gt 0 ]; then
    print_message "error" "Some Python versions failed testing"
    exit 1
else
    print_message "success" "All Python versions passed testing successfully!"
fi