#!/bin/bash
set -euo pipefail

# Integration test report generator
# Creates comprehensive test reports and summaries

source "$(dirname "$0")/workflow_utils.sh"

TEST_SCOPE="${1:-full}"
RESULTS_DIR="${2:-all_integration_results}"

start_step_timing "integration_report_generation"

# Create comprehensive integration test report
cat > integration_test_report.md << EOF
# Integration Test Results Summary

## Test Execution Overview
- **Test Scope**: $TEST_SCOPE
- **Execution Time**: $(date)
- **Trigger**: ${GITHUB_EVENT_NAME:-manual}

## Test Coverage Summary

### ✅ Completed Test Categories
- Full Workflow Simulation
- GitHub API Integration Testing  
- Error Recovery Testing
- Configuration Validation Testing
- Cross-Platform Compatibility Testing

### 📊 Test Results

| Test Category | Status | Details |
|---------------|--------|---------|
| Workflow Simulation | \${{ needs.full-workflow-simulation.result }} | End-to-end workflow testing |
| API Integration | \${{ needs.github-api-integration-testing.result }} | GitHub API functionality |
| Error Recovery | \${{ needs.error-recovery-testing.result }} | Error handling validation |
| Config Validation | \${{ needs.configuration-validation-testing.result }} | Configuration scenarios |
| Cross-Platform | \${{ needs.cross-platform-compatibility.result }} | Platform compatibility |

### 📈 Integration Metrics

See attached artifacts for detailed performance and timing metrics.

### 🔍 Test Details

EOF

# Append any available metric files
if [[ -d "$RESULTS_DIR" ]]; then
    for metric_file in "$RESULTS_DIR"/*.json; do
        if [[ -f "$metric_file" ]]; then
            echo "#### $(basename "$metric_file" .json)" >> integration_test_report.md
            echo '```json' >> integration_test_report.md
            cat "$metric_file" >> integration_test_report.md
            echo '```' >> integration_test_report.md
            echo "" >> integration_test_report.md
        fi
    done
fi

# Create step summary with integration test results
create_step_summary "integration-testing" \
    "Integration Testing Results" \
    "integration_test_report.md"

print_message "success" "Integration test report generated"

end_step_timing "integration_report_generation"