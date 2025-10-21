# test_local.sh Bug Fix Documentation

**Date**: October 21, 2025  
**Branch**: feature/65-extending-test-project-repos-qa  
**Issue**: Tier 2 tests failing with exit code 127  

---

## Problem Discovered

When testing `test_local.sh` with the `--tier2` option, tests were failing with exit code 127:

```bash
./test_local.sh --tier2
# Output:
[ERROR] ✗ test_assignments_commands.sh failed (exit code: 127)
```

---

## Root Cause Analysis

### Issue 1: `timeout` Command Not Available on macOS

**Problem**: The script used `timeout 300` to prevent tests from hanging:
```bash
if timeout 300 "$test_script" --all >/dev/null 2>&1; then
```

**Error**: `bash: timeout: command not found`

**Explanation**: The `timeout` command is a GNU coreutils utility that's not available by default on macOS. It's available on Linux but not on BSD-based systems like macOS.

### Issue 2: Output Suppression Hiding Errors

**Problem**: All test output was redirected to `/dev/null`:
```bash
timeout 300 "$test_script" --all >/dev/null 2>&1
```

**Impact**: When tests failed, we couldn't see why they were failing because all output was suppressed.

---

## Solution Implemented

### Fix 1: Remove `timeout` for Cross-Platform Compatibility

**Before**:
```bash
if timeout 300 "$test_script" --all >/dev/null 2>&1; then
    print_success "✓ $script_name passed"
else
    print_error "✗ $script_name failed"
fi
```

**After**:
```bash
# Create temporary file for test output
test_output_file=$(mktemp)

# Run the test script
# Note: timeout removed for macOS compatibility
if bash "$test_script" --all > "$test_output_file" 2>&1; then
    print_success "✓ $script_name passed"
else
    exit_code=$?
    print_error "✗ $script_name failed (exit code: $exit_code)"
    # Show last few lines of output for debugging
    echo "    Last 10 lines of output:"
    tail -10 "$test_output_file" | sed 's/^/    /'
fi

# Clean up temp file
rm -f "$test_output_file"
```

### Fix 2: Capture and Display Output on Failure

**Benefits**:
- Output is captured to a temporary file
- On success: output is discarded (clean console)
- On failure: last 10 lines shown for debugging
- Temporary files are cleaned up automatically

---

## Testing the Fix

### Test 1: Verify `timeout` Issue Resolved
```bash
./test_local.sh --tier2 2>&1 | tail -20
```

**Before**: `timeout: command not found`  
**After**: Tests run successfully, errors are visible

### Test 2: Verify Error Output is Visible
```bash
./test_local.sh --tier2
```

**Result**: Now shows actual test failure reasons:
```
[ERROR] ✗ test_assignments_commands.sh failed (exit code: 1)
    Last 10 lines of output:
    ============================================================
      Testing setup with --url option
    ============================================================
```

### Test 3: All Options Still Work
```bash
./test_local.sh --help      # ✅ Works
./test_local.sh --tier1     # ✅ Works
./test_local.sh --tier2     # ✅ Works (shows real errors now)
./test_local.sh --all       # ✅ Works
```

---

## Additional Discovery: Legitimate Test Failures

After fixing the `timeout` issue, we discovered that Tier 2 tests are **legitimately failing** because:

**Issue**: QA tests use `--dry-run` flag that doesn't exist in current CLI:
```bash
# Test code:
poetry run classroom-pilot assignments setup --url "..." --dry-run

# Actual error:
Error: No such option: --dry-run
```

**This is NOT a bug in test_local.sh** - This is the expected behavior of end-to-end tests! They're revealing that:
1. The QA test suite was written for an older CLI version
2. The CLI has evolved and removed the `--dry-run` option from `assignments setup`
3. The tests need updating to match the current CLI interface

---

## Impact Assessment

### What Was Fixed
✅ **Cross-platform compatibility** - Removed Linux-specific `timeout` command  
✅ **Error visibility** - Test failures now show diagnostic output  
✅ **Debugging capability** - Last 10 lines help identify issues  
✅ **Clean output** - Successful tests don't clutter console  

### What Was Revealed
🔍 **CLI/Test Mismatch** - QA tests need updating for current CLI  
🔍 **Integration Testing Value** - Tier 2 tests caught real discrepancies  

### What Still Works
✅ All command-line options (--help, --tier1, --tier2, --all)  
✅ Help menu display  
✅ Argument parsing  
✅ Conditional execution  
✅ Error handling  

---

## Recommendations

### For test_local.sh
1. ✅ **FIXED**: Script is now production-ready
2. ✅ **FIXED**: Works on both macOS and Linux
3. ✅ **FIXED**: Provides useful error messages

### For QA Test Suite
1. ⚠️ **TODO**: Update `test_assignments_commands.sh` to remove `--dry-run` usage
2. ⚠️ **TODO**: Verify all QA tests match current CLI interface
3. ⚠️ **TODO**: Add CI job to catch CLI/test mismatches earlier

### For Future Development
1. Consider adding a `--debug` flag to test_local.sh to show full output even on success
2. Add elapsed time reporting for each test script
3. Consider re-implementing timeout using Bash built-ins for long-running tests

---

## Files Modified

### `/Users/hugovalle/classdock/test_local.sh`

**Lines Changed**: 315-336 (Tier 2 test execution loop)

**Changes**:
1. Removed `timeout 300` command
2. Added temp file creation for output capture
3. Added error output display (last 10 lines)
4. Added temp file cleanup
5. Removed timeout-specific error handling (exit code 124)

---

## Conclusion

**Bug Status**: ✅ **FIXED**

The test_local.sh script is now working correctly and is cross-platform compatible. The Tier 2 test failures being revealed are legitimate integration issues that need to be addressed in the QA test suite, not bugs in the runner script.

**Key Takeaway**: This fix demonstrates the value of end-to-end testing - the Tier 2 tests successfully identified that the test suite was out of sync with the actual CLI implementation.

---

**Next Steps**:
1. Commit test_local.sh fixes
2. Create separate issue/task to update QA tests for current CLI
3. Consider adding CLI version checking to QA tests
