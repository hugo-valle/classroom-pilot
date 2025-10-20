# Token Management Test Suite - Verification Comments Implementation Status

## Implementation Progress

### ✅ Comment 1: COMPLETED
**Storage/priority tests now call GitHubTokenManager and assert exact tokens**

**Changes Made:**
1. `test_token_from_config_file()` - Parses expected token from fixture JSON, calls manager, asserts exact match
2. `test_token_from_environment_variable()` - Mocks keychain to fail, asserts env token returned  
3. `test_priority_config_over_environment()` - Parses config token, sets different env var, asserts config wins
4. `test_priority_config_over_keychain()` - Parses config token, mocks keychain with different token, asserts config wins
5. `test_priority_keychain_over_environment()` - Already correct, mocks keychain, asserts keychain wins over env

**Pattern Used:**
```python
# Parse expected token
with open(TOKEN_CONFIG_FILE, 'r') as f:
    config = json.load(f)
expected_token = config['github_token']['token']

# Call manager
manager = GitHubTokenManager()
actual_token = manager.get_github_token()

# Return for assertion
print(f'{actual_token}|{expected_token}')
```

---

### ✅ Comment 2: COMPLETED  
**Added Linux Secret Service and Windows Credential Manager tests**

**New Tests Created:**
1. `test_token_from_secret_service_linux()` - Gates on Linux, checks for secret-tool, mocks subprocess
2. `test_token_from_credential_manager_windows()` - Gates on Windows, checks for cmdkey, mocks subprocess

**Implementation:**
- Both tests use OS detection (`uname -s`)
- Check for required tools (secret-tool, cmdkey)
- Skip gracefully if not available
- Monkeypatch `_get_token_from_keychain()` to simulate platform-specific retrieval
- Mock `subprocess.run()` to return controlled token values
- Assert manager returns expected token

**Added to:** `run_storage_tests()` function

---

### ✅ Comment 3: COMPLETED
**Env token tests verify precedence properly**

**Integrated with Comment 1:**
- `test_token_from_environment_variable()` - Mocks keychain to fail (returncode=1)
- `test_priority_config_over_environment()` - Asserts config token returned, not env
- `test_priority_keychain_over_environment()` - Already implemented correctly

---

### ⏳ Comment 4: PENDING
**Import/export tests must call save_token() and _store_token()**

**Current State:**
- `test_token_import_from_environment()` - Currently just checks file presence
- `test_token_export_to_keychain()` - Uses mocked subprocess but doesn't call _store_token

**Required Implementation:**

#### test_save_token_from_environment()
```python
import subprocess
from unittest.mock import patch, MagicMock
import os

# Mock requests.get for API verification
def mock_requests_get(url, **kwargs):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {
        'X-OAuth-Scopes': 'repo, read:org, workflow',
        'X-RateLimit-Remaining': '5000'
    }
    mock_response.json.return_value = {
        'login': 'testuser',
        'name': 'Test User',
        'email': 'test@example.com'
    }
    return mock_response

with patch('requests.get', side_effect=mock_requests_get):
    manager = GitHubTokenManager()
    test_token = os.environ['GITHUB_TOKEN']
    result = manager.save_token(test_token)
    
    # Assert save succeeded
    assert result == True
    
    # Verify config file created
    assert os.path.exists(TOKEN_CONFIG_FILE)
    
    # Verify permissions
    import stat
    mode = os.stat(TOKEN_CONFIG_FILE).st_mode
    assert stat.S_IMODE(mode) == 0o600
    
    # Verify structure
    with open(TOKEN_CONFIG_FILE, 'r') as f:
        config = json.load(f)
    assert config['storage_type'] == 'config_file'
    assert config['github_token']['token'] == test_token
```

#### test_store_token_to_keychain()
```python
# Mock requests.get for token verification
with patch('requests.get', side_effect=mock_requests_get):
    manager = GitHubTokenManager()
    test_token = 'ghp_test_export_token_123456'
    
    # Get token_data via verification
    token_data = manager._verify_and_get_token_info(test_token)
    assert token_data is not None
    
    # Mock subprocess for keychain operations
    def mock_subprocess_run(cmd, **kwargs):
        mock_result = MagicMock()
        if 'security' in cmd and 'add-generic-password' in cmd:
            mock_result.returncode = 0
        elif 'security' in cmd and 'find-generic-password' in cmd:
            mock_result.returncode = 0
            mock_result.stdout = test_token
        else:
            mock_result.returncode = 1
            mock_result.stdout = ''
        return mock_result
    
    with patch('subprocess.run', side_effect=mock_subprocess_run):
        # Call _store_token with choice=2 (keychain)
        manager._store_token(test_token, token_data, 2)
        
        # Verify retrieval works
        rm -f TOKEN_CONFIG_FILE  # Remove config
        retrieved = manager.get_github_token()
        assert retrieved == test_token
```

---

### ⏳ Comment 5: PENDING
**Verification tests must call _verify_and_get_token_info() and validate_token_permissions()**

**Current State:**
- `test_valid_token_verification()` - Greps fixture
- `test_invalid_token_verification()` - Greps fixture  
- `test_token_permission_validation()` - Greps fixture

**Required Implementation:**

#### test_valid_token_verification_with_api()
```python
def mock_requests_get(url, **kwargs):
    mock_response = MagicMock()
    if '/user' in url:
        mock_response.status_code = 200
        mock_response.headers = {
            'X-OAuth-Scopes': 'repo, read:org, workflow',
            'X-RateLimit-Remaining': '5000'
        }
        mock_response.json.return_value = {
            'login': 'testuser',
            'name': 'Test User'
        }
    return mock_response

with patch('requests.get', side_effect=mock_requests_get):
    manager = GitHubTokenManager()
    test_token = 'ghp_valid_test_token_12345'
    token_data = manager._verify_and_get_token_info(test_token)
    
    assert token_data is not None
    assert token_data['login'] == 'testuser'
    assert 'repo' in token_data['scopes']
```

#### test_invalid_token_verification_with_api()
```python
def mock_requests_get_401(url, **kwargs):
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.json.return_value = {'message': 'Bad credentials'}
    return mock_response

with patch('requests.get', side_effect=mock_requests_get_401):
    manager = GitHubTokenManager()
    token_data = manager._verify_and_get_token_info('ghp_invalid')
    assert token_data is None
```

#### test_token_permission_validation_with_api()
```python
def mock_requests_get_insufficient(url, **kwargs):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {
        'X-OAuth-Scopes': 'repo',  # Missing read:org
        'X-RateLimit-Remaining': '5000'
    }
    mock_response.json.return_value = {'login': 'testuser'}
    return mock_response

with patch('requests.get', side_effect=mock_requests_get_insufficient):
    manager = GitHubTokenManager()
    token_data = manager._verify_and_get_token_info('ghp_test')
    success, message = manager.validate_token_permissions('ghp_test')
    
    assert success == False
    assert 'read:org' in message
```

---

### ⏳ Comment 6: PENDING
**Expiration tests must use dynamic dates and capture logs**

**Current State:**
- `test_token_expiration_warning()` - Greps for hardcoded date
- `test_expired_token_handling()` - Greps for hardcoded date

**Required Implementation:**

#### test_token_expiration_warning_dynamic()
```python
from datetime import datetime, timedelta
import logging
from io import StringIO

# Create token_data with dynamic expiration (5 days from now)
expires_at = (datetime.utcnow() + timedelta(days=5)).strftime('%Y-%m-%dT%H:%M:%SZ')
token_data = {
    'token': 'ghp_test',
    'token_type': 'fine-grained',
    'expires_at': expires_at
}

# Capture logs
log_capture = StringIO()
handler = logging.StreamHandler(log_capture)
handler.setLevel(logging.WARNING)
logger = logging.getLogger('classroom_pilot.utils.token_manager')
logger.addHandler(handler)

manager = GitHubTokenManager()
manager._check_expiration_warning(token_data)

logs = log_capture.getvalue()
assert 'expires in' in logs.lower()
assert '5 day' in logs.lower() or '4 day' in logs.lower()  # Allow for rounding

logger.removeHandler(handler)
```

#### test_expired_token_handling_dynamic()
```python
# Create token_data expired 1 day ago
expires_at = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
token_data = {
    'token': 'ghp_test',
    'token_type': 'fine-grained',
    'expires_at': expires_at
}

log_capture = StringIO()
handler = logging.StreamHandler(log_capture)
handler.setLevel(logging.ERROR)
logger = logging.getLogger('classroom_pilot.utils.token_manager')
logger.addHandler(handler)

manager = GitHubTokenManager()
manager._check_expiration_warning(token_data)

logs = log_capture.getvalue()
assert 'expired' in logs.lower()

logger.removeHandler(handler)
```

---

### ⏳ Comment 7: PENDING
**Log masking test must capture logs and verify token not present**

**Current State:**
- `test_token_masking_in_logs()` - Just checks config file existence

**Required Implementation:**

#### test_token_masking_validation()
```python
import logging
from io import StringIO

# Mock API
def mock_requests_get(url, **kwargs):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {
        'X-OAuth-Scopes': 'repo, read:org',
        'X-RateLimit-Remaining': '5000'
    }
    mock_response.json.return_value = {'login': 'testuser'}
    return mock_response

# Capture all logs
log_capture = StringIO()
handler = logging.StreamHandler(log_capture)
handler.setLevel(logging.DEBUG)

# Add handler to all relevant loggers
logger_names = ['classroom_pilot', 'classroom_pilot.utils.token_manager']
loggers = [logging.getLogger(name) for name in logger_names]
for logger in loggers:
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

test_token = 'ghp_this_is_a_secret_token_that_should_not_appear_in_logs_1234567890'

with patch('requests.get', side_effect=mock_requests_get):
    manager = GitHubTokenManager()
    manager.save_token(test_token)

logs = log_capture.getvalue()

# Assert full token NOT in logs
assert test_token not in logs, f"SECURITY: Full token found in logs!"

# Assert masked representation IS in logs (implementation specific)
# Check for common masking patterns
has_masking = (
    ('ghp_' in logs and '...' in logs) or  # ghp_...
    ('****' in logs) or  # ****
    (test_token[:10] in logs and test_token[10:] not in logs)  # Partial masking
)
assert has_masking, "Token masking not found in logs"

# Cleanup
for logger in loggers:
    logger.removeHandler(handler)
```

---

## Implementation Strategy

### Phase 1: ✅ COMPLETED
- Comment 1: Storage/priority tests
- Comment 2: Linux/Windows tests  
- Comment 3: Env precedence (integrated with 1)

### Phase 2: Next Steps
1. **Comment 4:** Update import/export tests
   - Find `test_token_import_from_environment`
   - Replace with `test_save_token_from_environment`
   - Find `test_token_export_to_keychain`
   - Update to call `_store_token()`

2. **Comment 5:** Update verification tests
   - Replace `test_valid_token_verification`
   - Replace `test_invalid_token_verification`
   - Replace `test_token_permission_validation`

3. **Comment 6:** Update expiration tests
   - Replace `test_token_expiration_warning`
   - Replace `test_expired_token_handling`

4. **Comment 7:** Update masking test
   - Replace `test_token_masking_in_logs`

### Testing Strategy

After each comment implementation:
1. Run `bash -n test_token_management.sh` - syntax check
2. Run specific test section to verify
3. Check for regressions in other tests

---

## Current File Status

- **File:** `test_project_repos/qa_tests/test_token_management.sh`
- **Size:** ~1200 lines (estimated after all changes)
- **Test Count:** Will increase from 23 to ~27-30 tests
- **Syntax:** ✅ Valid (last checked)

---

## Key Patterns Established

### Token Parsing
```bash
retrieved_token=$(cd "$PROJECT_ROOT" && poetry run python3 -c "
import json
with open('$TOKEN_CONFIG_FILE', 'r') as f:
    config = json.load(f)
expected_token = config['github_token']['token']
print(f'{actual}|{expected}')
")
actual=$(echo "$retrieved_token" | cut -d'|' -f1)
expected=$(echo "$retrieved_token" | cut -d'|' -f2)
```

### API Mocking
```python
from unittest.mock import patch, MagicMock

def mock_requests_get(url, **kwargs):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {'X-OAuth-Scopes': 'repo, read:org'}
    mock_response.json.return_value = {'login': 'testuser'}
    return mock_response

with patch('requests.get', side_effect=mock_requests_get):
    # Test code
```

### Log Capture
```python
from io import StringIO
import logging

log_capture = StringIO()
handler = logging.StreamHandler(log_capture)
logger = logging.getLogger('classroom_pilot.utils.token_manager')
logger.addHandler(handler)

# Operations that log

logs = log_capture.getvalue()
assert 'expected_message' in logs
logger.removeHandler(handler)
```

---

**Last Updated:** October 20, 2025  
**Branch:** feature/65-extending-test-project-repos-qa  
**Status:** Phase 1 Complete (Comments 1-3), Phase 2 Pending (Comments 4-7)
