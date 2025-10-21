# Token Management Test Refactoring Plan

## Overview
This document outlines the complete refactoring of `test_token_management.sh` to implement all 9 verification comments. The refactoring ensures proper integration testing with GitHubTokenManager through actual API calls with mocking.

## Implementation Summary

### Comment 1: Exercise GitHubTokenManager in storage and priority tests
**Status**: Requires implementation
**Changes needed**:
- Replace `grep` checks with Python scripts calling `GitHubTokenManager.get_github_token()`
- Assert returned token matches expected source's token
- Ensure other sources are properly ignored
- Isolate each test by creating/removing config files and keychain entries

**Example pattern**:
```python
manager = GitHubTokenManager()
token = manager.get_github_token()
assert token == expected_token_from_specific_source
```

### Comment 2: Fix keychain service name mismatch
**Status**: Requires implementation
**Changes needed**:
- Change all keychain operations from `classroom-pilot-test` to `classroom-pilot-github-token`
- This matches `_get_token_from_keychain()` in token_manager.py
- Update cleanup to use correct service name

**Files affected**:
- All macOS keychain test functions
- Cleanup function

### Comment 3: Add Linux and Windows credential store tests
**Status**: Requires implementation
**New test functions needed**:
```bash
test_token_from_linux_secret_service()
test_token_from_windows_credential_manager()
```

**Implementation**:
- Add `is_linux()` and `is_windows()` helper functions
- Use `secret-tool` for Linux Secret Service
- Use `cmdkey` for Windows Credential Manager
- Skip gracefully when tools unavailable
- Call `GitHubTokenManager.get_github_token()` to verify retrieval

### Comment 4: Validate environment variable via manager
**Status**: Requires implementation
**Changes needed**:
- In `test_token_from_environment_variable()`: Remove config/keychain, set GITHUB_TOKEN, call manager
- Add second check where config/keychain present to confirm env is NOT selected (priority test)

### Comment 5: Exercise save/store paths
**Status**: Requires implementation
**New tests needed**:
```bash
test_token_save_to_config()  # Call save_token(), verify structure and permissions
test_token_export_to_keychain_via_store_token()  # Call _store_token(token, data, 2)
```

**Implementation**:
- Mock GitHub API responses
- Call `manager.save_token(token)`
- Verify config file structure, JSON validity, 0600 permissions
- For keychain: call `_store_token(token, token_data, 2)`, verify keychain entry exists

### Comment 6: Mock GitHub API for verification tests
**Status**: Requires implementation
**New test functions**:
```bash
test_valid_token_verification_with_mocked_api()
test_invalid_token_verification_with_mocked_api()
test_token_permission_validation_with_mocked_api()
```

**Implementation pattern**:
```python
from unittest.mock import patch, MagicMock

with patch('requests.get') as mock_get:
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {...}
    mock_response.headers = {'X-OAuth-Scopes': '...'}
    mock_get.return_value = mock_response
    
    manager = GitHubTokenManager()
    token_info = manager._verify_and_get_token_info(token)
    # Assert success/failure appropriately
```

### Comment 7: Dynamic fixtures and expiration logic testing
**Status**: Requires implementation
**Changes needed**:
- Replace static expiration fixtures with dynamic generation
- Create `generate_expiring_token_fixture(days_offset)` helper
- Call `_check_expiration_warning(token_data)` in Python
- Capture logs and assert warning/error messages

**New test functions**:
```bash
test_token_expiration_warning_with_dynamic_fixture()
test_expired_token_handling_with_dynamic_fixture()
```

**Dynamic fixture generation**:
```bash
# Generate token expiring in 5 days
date -u -v+5d +"%Y-%m-%dT%H:%M:%SZ"  # macOS
date -u -d "+5 days" +"%Y-%m-%dT%H:%M:%SZ"  # Linux
```

### Comment 8: Validate token masking in logs
**Status**: Requires implementation
**New test**: `test_token_masking_in_logs()`

**Implementation**:
```python
import logging
from io import StringIO

log_capture = StringIO()
handler = logging.StreamHandler(log_capture)
logging.getLogger().addHandler(handler)

# Trigger token operation (save_token with mocked API)
manager.save_token(test_token)

# Verify full token NOT in logs, masked representation IS present
log_output = log_capture.getvalue()
assert test_token not in log_output
assert ('ghp_' in log_output and '...' in log_output) or '****' in log_output
```

### Comment 9: Use isolated mock HOME
**Status**: Requires implementation
**Changes needed**:
1. Add `setup_test_environment()` function:
   ```bash
   setup_test_environment() {
       mock_environment_setup  # From mock_helpers.sh
       MOCK_HOME="$HOME"
       mkdir -p "$HOME/.config/classroom-pilot"
   }
   ```

2. Call at start of `main()`
3. Update cleanup to call `restore_environment` and `cleanup_mocks`
4. All tests now write to temporary mock HOME, not real HOME

**Benefits**:
- Complete isolation from real user environment
- No risk of corrupting actual token config
- Clean test environment for each run

## File Structure Changes

### Variables to Add
```bash
KEYCHAIN_SERVICE="classroom-pilot-github-token"  # Comment 2
MOCK_HOME=""  # Comment 9
ORIGINAL_REAL_HOME=""  # Comment 9
```

### New Helper Functions
```bash
is_linux()  # Comment 3
is_windows()  # Comment 3
setup_test_environment()  # Comment 9
generate_expiring_token_fixture(days_offset, token_type)  # Comment 7
```

### Test Functions to Add
```bash
# Comment 3
test_token_from_linux_secret_service()
test_token_from_windows_credential_manager()

# Comment 5
test_token_save_to_config()
test_token_export_to_keychain_via_store_token()

# Comment 6
test_valid_token_verification_with_mocked_api()
test_invalid_token_verification_with_mocked_api()
test_token_permission_validation_with_mocked_api()

# Comment 7
test_token_expiration_warning_with_dynamic_fixture()
test_expired_token_handling_with_dynamic_fixture()
```

### Test Functions to Modify
```bash
# Comment 1: Add Python scripts calling GitHubTokenManager
test_token_from_config_file()
test_priority_config_over_keychain()
test_priority_config_over_environment()
test_priority_keychain_over_environment()

# Comment 2: Update service name
test_token_from_keychain_macos()
cleanup()

# Comment 4: Add manager calls, priority checks
test_token_from_environment_variable()

# Comment 8: Add log capture and masking verification
test_token_masking_in_logs()
```

## Testing Checklist

After implementation, verify:
- [ ] All storage tests call `GitHubTokenManager.get_github_token()`
- [ ] Keychain service name is `classroom-pilot-github-token` everywhere
- [ ] Linux and Windows tests skip gracefully when tools unavailable
- [ ] Environment variable priority properly tested with manager
- [ ] `save_token()` and `_store_token()` exercised with verification
- [ ] GitHub API mocked for all verification tests (no real network calls)
- [ ] Expiration fixtures generated dynamically, not hard-coded dates
- [ ] Token masking validated via log capture
- [ ] All tests run in isolated mock HOME
- [ ] Cleanup properly restores environment

## Execution Plan

1. **Phase 1**: Implement isolated mock HOME (Comment 9)
   - Add setup_test_environment()
   - Update main() and cleanup()
   
2. **Phase 2**: Fix keychain service name (Comment 2)
   - Update all keychain operations
   - Test on macOS

3. **Phase 3**: Add GitHubTokenManager calls (Comments 1, 4)
   - Update storage tests
   - Update priority tests
   - Add environment variable validation

4. **Phase 4**: Add platform-specific tests (Comment 3)
   - Linux Secret Service
   - Windows Credential Manager

5. **Phase 5**: Add save/export tests (Comment 5)
   - test_token_save_to_config()
   - test_token_export_to_keychain_via_store_token()

6. **Phase 6**: Mock GitHub API for verification (Comment 6)
   - Add mocked verification tests
   - Test permission validation

7. **Phase 7**: Dynamic expiration fixtures (Comment 7)
   - Add generate_expiring_token_fixture()
   - Update expiration tests

8. **Phase 8**: Validate token masking (Comment 8)
   - Add log capture
   - Verify masking behavior

9. **Phase 9**: Integration testing
   - Run complete test suite
   - Verify 100% pass rate
   - Test on multiple platforms if available

## Notes

- File is ~880 lines currently, will grow to ~1400 lines with all changes
- Each phase can be tested independently
- Backward compatibility maintained for existing fixtures
- All changes are additive except for service name fix (Comment 2)

## Success Criteria

- [ ] 25+ test functions (up from 23)
- [ ] All tests call GitHubTokenManager methods directly
- [ ] No real GitHub API calls (all mocked)
- [ ] No real HOME directory modifications
- [ ] 100% test pass rate on macOS
- [ ] Graceful skips on Linux/Windows where appropriate
- [ ] Comprehensive log capture and verification
- [ ] Dynamic fixtures for time-sensitive tests
