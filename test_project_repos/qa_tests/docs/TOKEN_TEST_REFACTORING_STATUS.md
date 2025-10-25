# Token Management Test Refactoring - Implementation Status

## Completed Changes (Phase 1)

### ✅ Comment 9: Isolated Mock HOME Environment
**Status**: IMPLEMENTED & TESTED

**Changes Made**:
1. Added variables:
   ```bash
   MOCK_HOME=""
   ORIGINAL_REAL_HOME=""
   ```

2. Created `setup_test_environment()` function:
   - Calls `mock_environment_setup()` from mock_helpers.sh
   - Stores mock HOME path
   - Updates TOKEN_CONFIG_DIR and TOKEN_CONFIG_FILE to use mock HOME
   - Creates config directory in isolated environment

3. Updated `main()`:
   - Calls `setup_test_environment()` at start
   - Logs mock HOME path for verification

4. Updated `cleanup()`:
   - Calls `restore_environment()` and `cleanup_mocks()`
   - All test artifacts now in temporary isolated HOME

**Verification**:
```bash
$ ./test_token_management.sh --storage-only
[INFO] Mock HOME: /var/folders/.../mock_data_XXXXXX.../home
```

**Benefits**:
- ✅ No risk of corrupting real user token configuration
- ✅ Complete test isolation
- ✅ Clean environment for each test run
- ✅ All writes go to temporary directory

---

### ✅ Comment 2: Fixed Keychain Service Name
**Status**: IMPLEMENTED & TESTED

**Changes Made**:
1. Added constant:
   ```bash
   KEYCHAIN_SERVICE="classroom-pilot-github-token"
   ```

2. Updated `test_token_from_keychain_macos()`:
   - Uses `$KEYCHAIN_SERVICE` in `security add-generic-password`
   - Uses `$KEYCHAIN_SERVICE` in cleanup

3. Updated `cleanup()`:
   - Uses `$KEYCHAIN_SERVICE` for keychain entry deletion

**Before** (WRONG):
```bash
security add-generic-password -s "classroom-pilot-test" ...
```

**After** (CORRECT):
```bash
security add-generic-password -s "$KEYCHAIN_SERVICE" ...
```

**Verification**:
- Keychain operations now use `classroom-pilot-github-token`
- Matches `_get_token_from_keychain()` in token_manager.py:606

---

### ✅ Comment 1: Call GitHubTokenManager in Tests (Partial)
**Status**: PARTIALLY IMPLEMENTED

**Changes Made**:
1. `test_token_from_config_file()` - ✅ Already calls GitHubTokenManager
2. `test_token_from_keychain_macos()` - ✅ NOW calls GitHubTokenManager:
   ```python
   retrieved_token=$(python3 -c "
   import sys
   sys.path.insert(0, '$PROJECT_ROOT')
   from classroom_pilot.utils.token_manager import GitHubTokenManager
   manager = GitHubTokenManager()
   token = manager.get_github_token()
   print(token if token else '')
   ")
   ```

**Still Need**:
- `test_priority_config_over_keychain()` - Update to call manager
- `test_priority_config_over_environment()` - Update to call manager
- `test_priority_keychain_over_environment()` - Update to call manager

---

## Remaining Work

### 🔄 Comment 1: Complete GitHubTokenManager Integration
**Priority**: HIGH
**Estimated Effort**: 30 minutes

**Tasks**:
1. Update `test_priority_config_over_keychain()`:
   - Setup: Create config file AND keychain entry
   - Call: `manager.get_github_token()`
   - Assert: Returned token matches config token (not keychain token)

2. Update `test_priority_config_over_environment()`:
   - Setup: Create config file AND set GITHUB_TOKEN env var
   - Call: `manager.get_github_token()`
   - Assert: Returned token matches config token (not env var)

3. Update `test_priority_keychain_over_environment()`:
   - Setup: Create keychain entry AND set GITHUB_TOKEN env var (no config)
   - Call: `manager.get_github_token()`
   - Assert: Returned token matches keychain token (not env var)

---

### 🔄 Comment 4: Environment Variable Validation via Manager
**Priority**: HIGH
**Estimated Effort**: 20 minutes

**Tasks**:
1. Update `test_token_from_environment_variable()`:
   - Remove config file and keychain entries
   - Set GITHUB_TOKEN environment variable
   - Call `manager.get_github_token()`
   - Assert returned token matches env var

2. Add precedence validation:
   - Create config file with different token
   - Verify env var is NOT used (config has priority)

---

### 🔄 Comment 3: Linux and Windows Credential Store Tests
**Priority**: MEDIUM
**Estimated Effort**: 1 hour

**Tasks**:
1. Add helper functions:
   ```bash
   is_linux() {
       [[ "$(uname -s)" == "Linux" ]]
   }
   
   is_windows() {
       [[ "$(uname -s)" == MINGW* ]] || [[ "$(uname -s)" == MSYS* ]]
   }
   ```

2. Create `test_token_from_linux_secret_service()`:
   - Skip if not Linux or `secret-tool` unavailable
   - Store token using: `secret-tool store --label="GitHub Token" service classroom-pilot-github-token account $USER`
   - Call `manager.get_github_token()`
   - Cleanup: `secret-tool clear service classroom-pilot-github-token account $USER`

3. Create `test_token_from_windows_credential_manager()`:
   - Skip if not Windows or `cmdkey` unavailable
   - Store token using: `cmdkey /generic:classroom-pilot-github-token /user:$USER /pass:$token`
   - Call `manager.get_github_token()`
   - Cleanup: `cmdkey /delete:classroom-pilot-github-token`

4. Update `run_storage_tests()` to include new tests

---

### 🔄 Comment 5: Exercise save_token() and _store_token()
**Priority**: MEDIUM
**Estimated Effort**: 45 minutes

**Tasks**:
1. Create `test_token_save_to_config()`:
   ```python
   # Mock GitHub API to avoid real API calls
   with patch('requests.get') as mock_get:
       mock_get.return_value.status_code = 200
       mock_get.return_value.json.return_value = {...}
       
       manager = GitHubTokenManager()
       success = manager.save_token(test_token)
   ```
   - Assert config file created
   - Assert JSON structure valid
   - Assert permissions 0600
   - Assert token value stored correctly

2. Create `test_token_export_to_keychain_via_store_token()`:
   ```python
   # Mock API, prepare token_data
   manager._store_token(token, token_data, 2)  # 2 = keychain
   ```
   - Verify keychain entry exists with correct service name
   - Verify stored value matches test token
   - Cleanup keychain entry

---

### 🔄 Comment 6: Mock GitHub API for Verification Tests
**Priority**: HIGH
**Estimated Effort**: 1 hour

**Tasks**:
1. Create `test_valid_token_verification_with_mocked_api()`:
   ```python
   from unittest.mock import patch, MagicMock
   
   with patch('requests.get') as mock_get:
       mock_response = MagicMock()
       mock_response.status_code = 200
       mock_response.json.return_value = {
           'login': 'testuser',
           'name': 'Test User',
           'email': 'test@example.com'
       }
       mock_response.headers = {
           'X-OAuth-Scopes': 'repo, workflow'
       }
       mock_get.return_value = mock_response
       
       manager = GitHubTokenManager()
       token_info = manager._verify_and_get_token_info('ghp_test123')
       # Assert success, check returned data
   ```

2. Create `test_invalid_token_verification_with_mocked_api()`:
   - Mock 401 response
   - Verify proper error handling

3. Create `test_token_permission_validation_with_mocked_api()`:
   - Mock response with insufficient scopes
   - Call `manager.validate_token_permissions(token)`
   - Verify warning/error for missing permissions

---

### 🔄 Comment 7: Dynamic Fixtures and Expiration Logic
**Priority**: MEDIUM
**Estimated Effort**: 45 minutes

**Tasks**:
1. Create `generate_expiring_token_fixture()`:
   ```bash
   generate_expiring_token_fixture() {
       local days_offset="$1"
       local token_type="$2"  # classic or fine_grained
       
       local expiry_date
       if is_macos; then
           expiry_date=$(date -u -v+${days_offset}d +"%Y-%m-%dT%H:%M:%SZ")
       else
           expiry_date=$(date -u -d "+${days_offset} days" +"%Y-%m-%dT%H:%M:%SZ")
       fi
       
       # Generate JSON with dynamic expiry
       cat << EOF
   {
       "token": "ghp_dynamically_generated_test_token",
       "token_type": "$token_type",
       "expires_at": "$expiry_date"
   }
   EOF
   }
   ```

2. Update `test_token_expiration_warning()`:
   - Generate fixture expiring in 5 days
   - Call `manager._check_expiration_warning(token_data)`
   - Capture logs, verify warning message

3. Create `test_expired_token_handling_with_dynamic_fixture()`:
   - Generate fixture expired 1 day ago (offset: -1)
   - Verify appropriate error/warning

---

### 🔄 Comment 8: Validate Token Masking in Logs
**Priority**: MEDIUM
**Estimated Effort**: 30 minutes

**Tasks**:
1. Create `test_token_masking_in_logs()`:
   ```python
   import logging
   from io import StringIO
   
   log_capture = StringIO()
   handler = logging.StreamHandler(log_capture)
   formatter = logging.Formatter('%(message)s')
   handler.setFormatter(formatter)
   
   logger = logging.getLogger('classroom_pilot')
   logger.addHandler(handler)
   logger.setLevel(logging.DEBUG)
   
   # Trigger save_token (with mocked API)
   test_token = 'ghp_this_is_a_secret_token_1234567890'
   manager.save_token(test_token)
   
   log_output = log_capture.getvalue()
   
   # Assert full token NOT in logs
   assert test_token not in log_output, "Full token leaked in logs!"
   
   # Assert masked representation IS in logs
   assert ('ghp_' in log_output and '...' in log_output) or '****' in log_output
   ```

---

## Security Issue Found

### 🔴 Token Leaking to stdout
**Observed**:
```
[INFO] Setting up isolated test environment...
ghp_P25qH5tjSUNCn6706n02F7oSv9lSTb9DmG75  <-- LEAKED TOKEN!
[INFO] Isolated test environment ready
```

**Cause**: Unknown (needs investigation)
**Priority**: CRITICAL
**Fix**: Investigate where this print statement comes from and remove/redirect it

---

## Test Coverage Summary

| Category | Current | Target | Gap |
|----------|---------|--------|-----|
| Storage Tests | 3 | 5 | +2 (Linux, Windows) |
| Priority Tests | 3 | 3 | 0 (but need manager calls) |
| Verification Tests | 2 | 5 | +3 (mocked API tests) |
| Save/Export Tests | 0 | 2 | +2 |
| Expiration Tests | 2 | 2 | 0 (but need dynamic fixtures) |
| Security Tests | 3 | 4 | +1 (log masking) |
| **Total** | **23** | **31** | **+8** |

---

## Estimated Time to Completion

- **High Priority** (Comments 1, 4, 6): 2 hours
- **Medium Priority** (Comments 3, 5, 7, 8): 3 hours
- **Critical Fix** (Token leak): 30 minutes
- **Testing & Validation**: 1 hour
- **Documentation**: 30 minutes

**Total**: ~7 hours of focused development work

---

## Next Steps

1. **Immediate**: Fix token leak to stdout (security issue)
2. **Phase 2**: Complete Comment 1 (priority tests with manager calls)
3. **Phase 3**: Implement Comment 4 (environment variable validation)
4. **Phase 4**: Implement Comment 6 (mocked API tests)
5. **Phase 5**: Implement Comments 3, 5, 7, 8
6. **Final**: Comprehensive testing and documentation update

---

## Files Modified

- `test_project_repos/qa_tests/test_token_management.sh`
  - Added: `setup_test_environment()` function
  - Added: KEYCHAIN_SERVICE, MOCK_HOME, ORIGINAL_REAL_HOME variables
  - Updated: `cleanup()` function
  - Updated: `main()` function
  - Updated: `test_token_from_keychain_macos()` function
  - Current size: 913 lines
  - Target size: ~1400 lines (with all enhancements)

## Documentation Created

- `TOKEN_TEST_REFACTORING_PLAN.md` - Comprehensive refactoring plan
- `TOKEN_TEST_REFACTORING_STATUS.md` (this file) - Current implementation status

---

**Last Updated**: 2024
**Branch**: feature/65-extending-test-project-repos-qa
**Status**: Phase 1 Complete (Comments 2, 9, partial 1)
