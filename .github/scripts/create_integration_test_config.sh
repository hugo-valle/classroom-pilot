#!/bin/bash
set -euo pipefail

# Integration test configuration generator
# Creates test configuration files for various scenarios

source "$(dirname "$0")/workflow_utils.sh"

CONFIG_TYPE="${1:-basic}"
OUTPUT_DIR="${2:-integration_test_data}"

mkdir -p "$OUTPUT_DIR"

case "$CONFIG_TYPE" in
    "basic")
        print_message "step" "Creating basic test configuration"
        cat > "$OUTPUT_DIR/test_assignment.conf" << 'EOF'
ASSIGNMENT_NAME="Test Assignment"
ORGANIZATION="test-org"
TEMPLATE_REPO="test-template"
STUDENT_REPOS="repo1,repo2,repo3"
MAX_REPOS=3
DRY_RUN=true
EOF
        ;;
    "minimal")
        print_message "step" "Creating minimal test configuration"
        cat > "$OUTPUT_DIR/minimal_assignment.conf" << 'EOF'
ASSIGNMENT_NAME="Minimal Test Assignment"
ORGANIZATION="test-org"
TEMPLATE_REPO="template"
STUDENT_REPOS="repo1,repo2"
MAX_REPOS=2
DRY_RUN=true
EOF
        ;;
    "advanced")
        print_message "step" "Creating advanced test configuration"
        cat > "$OUTPUT_DIR/advanced_assignment.conf" << 'EOF'
ASSIGNMENT_NAME="Advanced Test Assignment"
ORGANIZATION="test-org"
TEMPLATE_REPO="advanced-template"
STUDENT_REPOS="repo1,repo2,repo3,repo4,repo5"
MAX_REPOS=5
SECRETS_FILE="advanced_secrets.yaml"
COLLABORATOR_PERMISSIONS="write"
ENABLE_ISSUES=true
ENABLE_WIKI=false
DRY_RUN=true
VERBOSE=true
EOF
        ;;
    "edge-case")
        print_message "step" "Creating edge case test configuration"
        cat > "$OUTPUT_DIR/edge_case_assignment.conf" << 'EOF'
ASSIGNMENT_NAME="Edge-Case_Test.Assignment!"
ORGANIZATION="test-org-with-dashes"
TEMPLATE_REPO="template_with_underscores"
STUDENT_REPOS="repo-1,repo_2,repo.3"
MAX_REPOS=3
DRY_RUN=true
EOF
        ;;
    "invalid")
        print_message "step" "Creating invalid test configuration"
        cat > "$OUTPUT_DIR/invalid_assignment.conf" << 'EOF'
ASSIGNMENT_NAME=""
ORGANIZATION=""
TEMPLATE_REPO=""
STUDENT_REPOS=""
MAX_REPOS=invalid
EOF
        ;;
    *)
        print_message "error" "Unknown configuration type: $CONFIG_TYPE"
        exit 1
        ;;
esac

print_message "success" "Created $CONFIG_TYPE configuration in $OUTPUT_DIR"