#!/bin/bash
set -euo pipefail

# Security health metrics collection script
# Collects and reports on security configuration checks

source "$(dirname "$0")/workflow_utils.sh"

print_message "step" "Collecting security health metrics"

# Basic security configuration checks
security_checks=0

# Check for security workflows
if ls .github/workflows/*security* >/dev/null 2>&1; then
    security_checks=$((security_checks + 1))
    print_message "success" "✅ Security workflows found"
else
    print_message "warning" "❌ No security workflows detected"
fi

# Check for CI workflows
if [[ -f ".github/workflows/ci.yml" ]]; then
    security_checks=$((security_checks + 1))
    print_message "success" "✅ CI workflow present"
else
    print_message "warning" "❌ CI workflow missing"
fi

# Check for automated dependency updates
if ls .github/workflows/*update* >/dev/null 2>&1 || ls .github/workflows/*dependabot* >/dev/null 2>&1; then
    security_checks=$((security_checks + 1))
    print_message "success" "✅ Dependency update automation found"
else
    print_message "warning" "❌ No dependency update automation detected"
fi

# Check for security policy
if [[ -f "SECURITY.md" ]] || [[ -f ".github/SECURITY.md" ]]; then
    security_checks=$((security_checks + 1))
    print_message "success" "✅ Security policy found"
else
    print_message "warning" "❌ Security policy missing"
fi

print_message "info" "Security configuration checks passed: $security_checks/4"

# Export security check count for use in other steps
echo "SECURITY_CHECKS_PASSED=$security_checks" >> $GITHUB_ENV

if [[ $security_checks -ge 3 ]]; then
    print_message "success" "Security configuration health: Good"
    exit 0
elif [[ $security_checks -ge 2 ]]; then
    print_message "warning" "Security configuration health: Fair"
    exit 0
else
    print_message "warning" "Security configuration health: Needs Improvement"
    exit 1
fi