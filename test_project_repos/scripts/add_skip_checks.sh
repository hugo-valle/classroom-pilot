#!/bin/bash
################################################################################
# Add Skip Checks to Test Suites
#
# This script automatically adds skip checks to test functions based on the
# skipped_tests.sh configuration.
#
# Usage: ./scripts/add_skip_checks.sh [test_suite_name]
#        If no test_suite_name is provided, processes all configured suites
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
QA_TESTS_DIR="$PROJECT_ROOT/qa_tests"
LIB_DIR="$PROJECT_ROOT/lib"

# Source the skip list to get test names
source "$LIB_DIR/skipped_tests.sh"

# Function to add skip check to a test function
# Args: $1=test_file, $2=function_name, $3=test_display_name, $4=skip_reason
add_skip_check() {
    local test_file="$1"
    local function_name="$2"
    local test_display_name="$3"
    local skip_reason="$4"
    
    # Check if skip check already exists
    if grep -q "is_test_skipped.*${function_name}" "$test_file"; then
        echo "[INFO] Skip check already exists for $function_name"
        return 0
    fi
    
    # Find the function and add skip check after the opening brace
    # Pattern: test_function_name() {
    #          log_step ...
    # 
    # Should become:
    # test_function_name() {
    #     # Check if test should be skipped
    #     is_test_skipped "\${FUNCNAME[0]}" && mark_test_skipped "test_name" "\$(get_skip_reason "\${FUNCNAME[0]}")" && return
    #     
    #     log_step ...
    
    local temp_file=$(mktemp)
    awk -v fname="$function_name" -v display="$test_display_name" '
    /^'"$function_name"'\(\) \{$/ {
        print
        print "    # Check if test should be skipped"
        print "    is_test_skipped \"${FUNCNAME[0]}\" && mark_test_skipped \"" display "\" \"$(get_skip_reason \"${FUNCNAME[0]}\")\" && return"
        print ""
        next
    }
    { print }
    ' "$test_file" > "$temp_file"
    
    if [ -s "$temp_file" ]; then
        mv "$temp_file" "$test_file"
        echo "[SUCCESS] Added skip check to $function_name"
    else
        rm "$temp_file"
        echo "[ERROR] Failed to add skip check to $function_name"
        return 1
    fi
}

# Function to add test suite header (TEST_SUITE_NAME and source)
add_test_suite_header() {
    local test_file="$1"
    local suite_name="$2"
    
    # Check if already has TEST_SUITE_NAME
    if grep -q "^TEST_SUITE_NAME=" "$test_file"; then
        echo "[INFO] Test suite header already exists in $test_file"
        return 0
    fi
    
    # Find a good place to insert (after the initial comment block and before first function)
    # Usually after setup_test_environment() or before first test_ function
    local temp_file=$(mktemp)
    
    awk -v suite="$suite_name" '
    BEGIN { inserted = 0 }
    /^# Section:|^test_[a-z_]+\(\)/ {
        if (inserted == 0) {
            print "# Test Suite Configuration"
            print "TEST_SUITE_NAME=\"" suite "\""
            print "source \"$PROJECT_ROOT/test_project_repos/lib/skipped_tests.sh\""
            print ""
            inserted = 1
        }
    }
    { print }
    ' "$test_file" > "$temp_file"
    
    if [ -s "$temp_file" ]; then
        mv "$temp_file" "$test_file"
        echo "[SUCCESS] Added test suite header to $test_file"
    else
        rm "$temp_file"
        echo "[ERROR] Failed to add test suite header"
        return 1
    fi
}

# Process a single test suite
process_test_suite() {
    local suite_name="$1"
    local test_file="$QA_TESTS_DIR/${suite_name}.sh"
    
    if [ ! -f "$test_file" ]; then
        echo "[ERROR] Test file not found: $test_file"
        return 1
    fi
    
    echo ""
    echo "======================================================================"
    echo "Processing $suite_name"
    echo "======================================================================"
    
    # Add test suite header if needed
    add_test_suite_header "$test_file" "$suite_name"
    
    # Process each skip entry for this suite
    for entry in "${SKIP_LIST[@]}"; do
        local entry_suite=$(echo "$entry" | cut -d: -f1)
        local function_name=$(echo "$entry" | cut -d: -f2)
        local skip_reason=$(echo "$entry" | cut -d: -f3-)
        
        if [ "$entry_suite" = "$suite_name" ]; then
            # Extract display name from function name (remove test_ prefix and convert underscores)
            local display_name=$(echo "$function_name" | sed 's/^test_//' | sed 's/_/ /g')
            echo "[INFO] Adding skip check for: $function_name"
            add_skip_check "$test_file" "$function_name" "$display_name" "$skip_reason"
        fi
    done
    
    echo "[SUCCESS] Completed processing $suite_name"
}

# Main execution
main() {
    if [ $# -eq 0 ]; then
        # Process all test suites in SKIP_LIST
        local suites=$(printf '%s\n' "${SKIP_LIST[@]}" | cut -d: -f1 | sort -u)
        
        for suite in $suites; do
            # Skip test_secrets_commands since it's already done
            if [ "$suite" = "test_secrets_commands" ]; then
                echo "[INFO] Skipping $suite (already processed)"
                continue
            fi
            process_test_suite "$suite"
        done
    else
        # Process specific test suite
        process_test_suite "$1"
    fi
    
    echo ""
    echo "======================================================================"
    echo "All test suites processed successfully!"
    echo "======================================================================"
}

main "$@"
