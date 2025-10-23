# Repos Fixtures Directory

## Purpose

This directory contains test fixtures for QA testing of repos commands in the classroom-pilot CLI. These fixtures provide realistic test data for validating repository management operations including fetching, updating, pushing, and collaborator cycling.

The fixtures enable comprehensive testing of:
- **fetch** - Discover and fetch student repositories
- **update** - Update assignment configuration and student repositories  
- **push** - Sync template repository to GitHub Classroom repository
- **cycle-collaborator** - Cycle repository collaborator permissions

---

## Fixture Categories

### Configuration Files

#### `valid_repos_config.conf`
**Purpose**: Comprehensive valid configuration with all fields including CLASSROOM_REPO_URL

**Contains**:
- All required fields (CLASSROOM_URL, TEMPLATE_REPO_URL, GITHUB_ORGANIZATION, ASSIGNMENT_NAME, ASSIGNMENT_FILE)
- Optional CLASSROOM_REPO_URL (required for push command)
- Optional STUDENT_FILES
- Optional COLLABORATOR_USERS

**Use Cases**:
- Testing fetch command with full configuration
- Testing update command with student files preservation
- Testing push command (requires CLASSROOM_REPO_URL)
- Testing all commands with complete configuration

#### `minimal_repos_config.conf`
**Purpose**: Minimal valid configuration with only required fields

**Contains**:
- Only the 5 required fields (CLASSROOM_URL, TEMPLATE_REPO_URL, GITHUB_ORGANIZATION, ASSIGNMENT_NAME, ASSIGNMENT_FILE)
- No optional fields

**Use Cases**:
- Testing commands with minimal configuration
- Validating required field detection
- Testing fetch and update with minimal setup
- Note: push command may fail since CLASSROOM_REPO_URL is missing

#### `no_classroom_repo.conf`
**Purpose**: Configuration missing CLASSROOM_REPO_URL for testing push command error handling

**Contains**:
- All required fields except CLASSROOM_REPO_URL
- Intentionally omits CLASSROOM_REPO_URL

**Use Cases**:
- Testing push command error handling
- Validating error messages for missing CLASSROOM_REPO_URL
- Ensuring clear user feedback for configuration errors

### Repository Lists

#### `student_repos.txt`
**Purpose**: List of student repository URLs for testing fetch and update operations

**Format**: One URL per line, 8 repositories
**Pattern**: `https://github.com/test-org/test-assignment-studentN`

**Use Cases**:
- Testing fetch command with multiple repositories
- Testing update command batch operations
- Validating repository URL parsing
- Testing parallel operations

#### `usernames.txt`
**Purpose**: List of student usernames for testing cycle-collaborator operations

**Format**: One username per line, 8 usernames
**Pattern**: `studentN`

**Use Cases**:
- Testing cycle-collaborator command
- Combining usernames with assignment prefix
- Testing batch collaborator operations
- Validating username parsing

#### `empty_repos.txt`
**Purpose**: Empty file for error handling testing

**Contains**: Only comment header (effectively empty)

**Use Cases**:
- Testing error handling with empty input files
- Validating warning/error messages
- Ensuring graceful handling of edge cases

#### `invalid_repos.txt`
**Purpose**: Invalid repository URLs for error handling testing

**Contains**:
- Plain text (not a URL)
- Malformed protocols (htp://)
- Missing components (no repo name)
- Invalid formats
- URLs with spaces

**Use Cases**:
- Testing URL validation
- Validating error messages for invalid URLs
- Ensuring clear user feedback for malformed input
- Testing error recovery

---

## Usage Examples

### Test fetch with valid configuration
```bash
classroom-pilot repos fetch --config fixtures/repos/valid_repos_config.conf
```

### Test update with minimal configuration
```bash
classroom-pilot repos update --config fixtures/repos/minimal_repos_config.conf
```

### Test push with valid configuration (includes CLASSROOM_REPO_URL)
```bash
classroom-pilot repos push --config fixtures/repos/valid_repos_config.conf
```

### Test push error handling (missing CLASSROOM_REPO_URL)
```bash
classroom-pilot repos push --config fixtures/repos/no_classroom_repo.conf
# Expected: Error message about missing CLASSROOM_REPO_URL
```

### Test cycle-collaborator with parameters
```bash
classroom-pilot repos cycle-collaborator \
  --assignment-prefix test-assignment \
  --username student1 \
  --organization test-org
```

### Test cycle-collaborator list mode
```bash
classroom-pilot repos cycle-collaborator \
  --list \
  --assignment-prefix test-assignment \
  --username student1 \
  --organization test-org
```

### Test with global options
```bash
# Verbose mode
classroom-pilot --verbose repos fetch --config fixtures/repos/valid_repos_config.conf

# Dry-run mode
classroom-pilot repos --dry-run fetch --config fixtures/repos/valid_repos_config.conf

# Combined
classroom-pilot --verbose repos --dry-run fetch --config fixtures/repos/valid_repos_config.conf
```

---

## Configuration Field Reference

### Required Fields (for all repos commands)

- **CLASSROOM_URL** - GitHub Classroom assignment URL
  - Format: `https://classroom.github.com/classrooms/{id}/assignments/{name}`
  - Example: `https://classroom.github.com/classrooms/123456/assignments/test-assignment`

- **TEMPLATE_REPO_URL** - Source template repository URL
  - Format: `https://github.com/{org}/{repo}`
  - Example: `https://github.com/test-org/test-assignment-template`

- **GITHUB_ORGANIZATION** - GitHub organization name
  - Format: Alphanumeric, hyphens allowed
  - Example: `test-org`

- **ASSIGNMENT_NAME** - Assignment identifier/name
  - Format: Alphanumeric, hyphens, underscores allowed
  - Example: `test-assignment`

- **ASSIGNMENT_FILE** - Main assignment file
  - Format: Filename with extension
  - Example: `assignment.ipynb` or `README.md`

### Optional Fields

- **CLASSROOM_REPO_URL** - Central classroom repository URL (required for push command)
  - Format: `https://github.com/{org}/{repo}`
  - Example: `https://github.com/test-org/classroom-test-assignment`

- **STUDENT_FILES** - Files/directories to preserve during updates
  - Format: Comma-separated list
  - Example: `assignment.ipynb,student_work/,submissions/`

- **COLLABORATOR_USERS** - Usernames with collaborator access
  - Format: Comma-separated list of GitHub usernames
  - Example: `ta1,ta2,instructor`

---

## File Format Specifications

### Configuration Files (.conf)

**Format**: KEY=VALUE pairs, one per line

**Rules**:
- Comments start with `#`
- No spaces around `=` sign
- Values can contain spaces
- Keys are case-sensitive (UPPERCASE by convention)
- Blank lines are ignored

**Example**:
```bash
# Comment explaining the field
FIELD_NAME=field_value
ANOTHER_FIELD=value with spaces
```

### Repository Lists (.txt)

**Format**: One URL per line

**Rules**:
- Comments start with `#`
- Blank lines are skipped
- No trailing slashes
- Must be valid GitHub URLs

**Example**:
```
# Repository list
https://github.com/org/repo1
https://github.com/org/repo2
```

### Username Lists (.txt)

**Format**: One username per line

**Rules**:
- Alphanumeric, hyphens, underscores only
- Comments start with `#`
- Case-sensitive
- No @ prefix

**Example**:
```
# Username list
student1
student2
ta-username
```

---

## Command-Specific Requirements

### fetch command

**Requires**:
- CLASSROOM_URL
- TEMPLATE_REPO_URL
- GITHUB_ORGANIZATION
- ASSIGNMENT_NAME

**Optional**:
- ASSIGNMENT_FILE

**Behavior**:
- Uses organization and assignment name to discover repositories
- Fetches/clones discovered student repositories
- Can operate in dry-run mode to preview operations

**Test Fixtures**:
- `valid_repos_config.conf` - Full configuration
- `minimal_repos_config.conf` - Minimal required fields

### update command

**Requires**:
- CLASSROOM_URL
- TEMPLATE_REPO_URL
- GITHUB_ORGANIZATION
- ASSIGNMENT_NAME
- ASSIGNMENT_FILE

**Optional**:
- STUDENT_FILES (files to preserve during update)

**Behavior**:
- Updates student repositories with template changes
- Preserves files specified in STUDENT_FILES
- Maintains student work while syncing template updates

**Test Fixtures**:
- `valid_repos_config.conf` - With STUDENT_FILES
- `minimal_repos_config.conf` - Without STUDENT_FILES

### push command

**Requires**:
- CLASSROOM_URL
- TEMPLATE_REPO_URL
- GITHUB_ORGANIZATION
- ASSIGNMENT_NAME
- CLASSROOM_REPO_URL (must be present)

**Optional**:
- ASSIGNMENT_FILE

**Behavior**:
- Pushes template changes to central classroom repository
- Requires CLASSROOM_REPO_URL to be configured
- Fails with clear error if CLASSROOM_REPO_URL is missing

**Test Fixtures**:
- `valid_repos_config.conf` - Includes CLASSROOM_REPO_URL
- `no_classroom_repo.conf` - Missing CLASSROOM_REPO_URL (error test)

### cycle-collaborator command

**Requires** (via CLI args):
- `--assignment-prefix` - Assignment name prefix
- `--username` - Student username
- `--organization` - GitHub organization

**Optional**:
- `--config` for additional settings
- `--list` to list current collaborators
- `--force` to force cycling without confirmation

**Behavior**:
- Constructs repository URL from prefix, username, and organization
- Cycles collaborator permissions (add/remove)
- Can list current collaborators with --list flag
- Supports force mode with --force flag

**Test Fixtures**:
- `usernames.txt` - List of usernames for batch operations
- `valid_repos_config.conf` - Optional config for additional settings

---

## Adding New Fixtures

### Naming Conventions

1. **Valid configurations**: `valid_*.conf` or descriptive names
   - Example: `valid_repos_config.conf`, `full_config.conf`

2. **Invalid configurations**: `invalid_*.conf` or `no_*.conf` with clear description
   - Example: `no_classroom_repo.conf`, `invalid_urls.conf`

3. **List files**: Descriptive names indicating content
   - Example: `student_repos.txt`, `usernames.txt`, `ta_list.txt`

### Documentation Requirements

When adding a new fixture:

1. **Add comment header** explaining the purpose
2. **Update this README** with:
   - Fixture name and category
   - Description of contents
   - Use cases
   - Any special considerations
3. **Provide usage example** in this README
4. **Test the fixture** with relevant commands

### Validation Checklist

Before committing a new fixture:

- [ ] File follows correct format specification
- [ ] Contains descriptive comment header
- [ ] Uses realistic but non-existent test values
- [ ] Documented in this README
- [ ] Tested with relevant commands
- [ ] No actual GitHub URLs or sensitive data
- [ ] Follows naming conventions

### Example: Adding a New Config Fixture

```bash
# Create the file
cat > new_config.conf <<EOF
# New Configuration Description
# Explain the purpose and special characteristics

# Required fields
CLASSROOM_URL=https://classroom.github.com/classrooms/123456/assignments/new-test
TEMPLATE_REPO_URL=https://github.com/test-org/new-template
GITHUB_ORGANIZATION=test-org
ASSIGNMENT_NAME=new-assignment
ASSIGNMENT_FILE=new.ipynb

# Special field for this test case
SPECIAL_FIELD=special_value
EOF

# Test it
classroom-pilot repos fetch --config new_config.conf --dry-run

# Document it (add to this README)
```

---

## Related Documentation

- **`docs/QA_TESTING_GUIDE.md`** - Comprehensive QA testing guide for repos commands (lines 971-1150)
- **`test_project_repos/qa_tests/test_repos_commands.sh`** - Main test suite using these fixtures
- **`test_project_repos/lib/test_helpers.sh`** - Test helper functions and assertions
- **`test_project_repos/lib/mock_helpers.sh`** - Mocking utilities for GitHub API and file system
- **`classroom_pilot/cli.py`** - CLI implementation for repos commands (lines 974-1222)
- **`classroom_pilot/services/repos_service.py`** - ReposService implementation
- **`classroom_pilot/repos/`** - Repos module implementations (fetch.py, collaborator.py)

---

## Security Note

⚠️ **IMPORTANT**: All fixtures use test/mock data only. These are NOT real GitHub URLs, organizations, or credentials.

### Never commit:
- Real GitHub organization names
- Real repository URLs
- Actual GitHub tokens or credentials
- Real student usernames
- Production configuration files

### Security Best Practices:
- Use `test-org` or similar for organization names
- Use `test-assignment` or similar for assignment names
- Use `studentN` pattern for usernames
- Keep all URLs in `github.com/test-org` namespace
- Never use actual classroom URLs

---

## Testing Best Practices

### 1. Use Appropriate Fixtures
Select the fixture that matches your test scenario:
- Valid operations → `valid_repos_config.conf`
- Minimal setup → `minimal_repos_config.conf`
- Error testing → `no_classroom_repo.conf`, `invalid_repos.txt`

### 2. Test Error Cases
Use invalid fixtures to verify error handling:
- Test with missing required fields
- Test with malformed URLs
- Test with empty files
- Verify error messages are clear and actionable

### 3. Clean Up
Remove temporary files created during testing:
```bash
rm -f /tmp/test_config.conf
rm -rf /tmp/test_repos/
```

### 4. Isolate Tests
- Don't rely on external state
- Each test should be independent
- Use fresh fixtures for each test
- Clean up between test runs

### 5. Mock External Calls
Use mock helpers to avoid real GitHub API calls:
```bash
source lib/mock_helpers.sh
mock_environment_setup
setup_mock_github_token
```

### 6. Verify Messages
Check that error messages are clear:
- Error messages should explain what went wrong
- Error messages should suggest how to fix the issue
- Success messages should confirm what was done

### 7. Test All Options
Verify each command option works correctly:
- Test with and without optional parameters
- Test flag combinations
- Test short and long flag formats

### 8. Test Global Options
Verify `--verbose` and `--dry-run` work with all commands:
- `--verbose` should show detailed logging
- `--dry-run` should preview without executing
- Combined options should work together

### 9. Test Exit Codes
Verify commands return appropriate exit codes:
- 0 for success
- Non-zero for errors
- Consistent codes for specific error types

### 10. Performance Testing
For batch operations, test with:
- Small lists (8 items) - basic functionality
- Medium lists (50 items) - scalability
- Large lists (200+ items) - performance limits

---

## Fixture Statistics

**Total Fixtures**: 8 files  
**Configuration Files**: 3 (.conf files)  
**List Files**: 4 (.txt files)  
**Documentation**: 1 (this README)

**Commands Supported**: 4
- fetch
- update
- push
- cycle-collaborator

**Test Coverage**:
- Repository discovery and fetching
- Repository updating with template sync
- Pushing changes to classroom repository
- Collaborator permission management

---

## Maintenance

### Regular Updates
- Review fixtures when commands change
- Update examples when CLI changes
- Add fixtures for new command options
- Remove deprecated fixtures

### Quality Checks
- Verify all fixtures are valid
- Test fixtures with current CLI version
- Check documentation is up-to-date
- Ensure no real data has been committed

### Version History
- **v1.0.0** (October 20, 2025) - Initial fixtures for repos commands testing
  - 3 configuration files
  - 4 list files
  - Comprehensive README

---

**Last Updated**: October 20, 2025  
**Fixture Count**: 8 files  
**Commands Supported**: 4 repos commands (fetch, update, push, cycle-collaborator)  
**Test Coverage**: Repository management operations
