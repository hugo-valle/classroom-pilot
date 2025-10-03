#!/bin/bash
set -euo pipefail

# Generate comprehensive CI summary
# Consolidates results from all CI jobs

source "$(dirname "$0")/workflow_utils.sh"

# Job results passed as arguments
TEST_RESULT="${1:-unknown}"
LINT_RESULT="${2:-unknown}"
SECURITY_RESULT="${3:-unknown}"
DOCS_RESULT="${4:-unknown}"

start_step_timing "ci_summary_generation"

# Determine overall status
overall_status="success"
if [[ "$TEST_RESULT" != "success" ]] || [[ "$LINT_RESULT" != "success" ]] || [[ "$DOCS_RESULT" != "success" ]]; then
    overall_status="failure"
fi

# Security is allowed to fail, so only warn
if [[ "$SECURITY_RESULT" != "success" ]]; then
    print_message "warning" "Security scan completed with warnings (non-blocking)"
fi

# Create comprehensive summary with workflow status integration
{
    echo "# 🔄 CI Pipeline Summary"
    echo ""
    echo "| Job | Status | Result |"
    echo "|-----|--------|--------|"
    echo "| 🧪 Tests | $([ "$TEST_RESULT" = "success" ] && echo "✅" || echo "❌") | $TEST_RESULT |"
    echo "| 🔍 Lint & Code Quality | $([ "$LINT_RESULT" = "success" ] && echo "✅" || echo "❌") | $LINT_RESULT |"
    echo "| 🛡️ Security Scan | $([ "$SECURITY_RESULT" = "success" ] && echo "✅" || echo "⚠️") | $SECURITY_RESULT |"
    echo "| 📚 Documentation | $([ "$DOCS_RESULT" = "success" ] && echo "✅" || echo "❌") | $DOCS_RESULT |"
    echo ""
    echo "## Overall Pipeline Status: $([ "$overall_status" = "success" ] && echo "✅ SUCCESS" || echo "❌ FAILURE")"
    echo ""
    echo "Generated at: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
} >> $GITHUB_STEP_SUMMARY

print_message "info" "CI Pipeline Status: $overall_status"

if [[ "$overall_status" != "success" ]]; then
    print_message "error" "CI pipeline failed - check individual job results"
    exit 1
else
    print_message "success" "CI pipeline completed successfully"
fi

end_step_timing "ci_summary_generation"