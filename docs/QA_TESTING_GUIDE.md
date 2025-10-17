# Classroom Pilot - Comprehensive QA Testing Guide

**Version:** 3.1.0-beta.2  
**Date:** October 17, 2025  
**Purpose:** Complete test scenarios for quality assurance validation

---

## Table of Contents

1. [Setup and Prerequisites](#setup-and-prerequisites)
2. [Global Options](#global-options)
3. [Assignments Commands](#assignments-commands)
4. [Repos Commands](#repos-commands)
5. [Secrets Commands](#secrets-commands)
6. [Automation Commands](#automation-commands)
7. [Test Execution Checklist](#test-execution-checklist)
8. [Expected Behaviors](#expected-behaviors)
9. [Common Issues and Troubleshooting](#common-issues-and-troubleshooting)

---

## Setup and Prerequisites

### Required Setup
1. **GitHub Token**: Configured in keychain or environment variable
2. **Test Repository**: A GitHub Classroom assignment to work with
3. **Configuration File**: `assignment.conf` in test directory
4. **Python Environment**: Python 3.10+ with classroom-pilot installed

### Installation
```bash
pip install classroom-pilot
# or for development
poetry install
```

### Test Data Requirements
- A GitHub organization with classroom access
- At least one test student repository
- Template repository with sample code
- Student list file (students.txt with GitHub usernames)
- Repository URLs file (repos.txt with full GitHub URLs)

---

## Global Options

These options work with ALL commands across all command groups.

### Main Application Options

| Option | Description | Test Scenarios |
|--------|-------------|----------------|
| `--version` | Show version | `classroom-pilot --version` |
| `--config TEXT` | Custom config file | `classroom-pilot --config custom.conf assignments setup` |
| `--assignment-root TEXT` | Root directory | `classroom-pilot --assignment-root /path/to/root assignments setup` |
| `--help` | Show help | `classroom-pilot --help` |

### Universal Command Options

These work with `assignments`, `repos`, `secrets`, and `automation` commands:

| Option | Description | Applies To |
|--------|-------------|------------|
| `--verbose` / `-v` | Verbose output | All command groups |
| `--dry-run` | Preview without executing | All command groups |
| `--help` | Command help | All commands |

**Test Scenarios:**
```bash
# Test verbose mode
classroom-pilot assignments --verbose orchestrate

# Test dry-run mode
classroom-pilot assignments --dry-run orchestrate

# Combine both
classroom-pilot repos --verbose --dry-run fetch

# Test help
classroom-pilot assignments --help
classroom-pilot assignments orchestrate --help
```

---

## GitHub Token Setup and Validation

**CRITICAL PREREQUISITE:** Before testing any commands, verify GitHub token configuration.

### Token Types

The application supports two types of GitHub Personal Access Tokens:

| Token Type | Permissions | Recommended For | Notes |
|------------|-------------|-----------------|-------|
| **Classic Token** | Full repository access | Development, Testing | Easier to set up, broader permissions |
| **Fine-Grained Token** | Specific repository/org access | Production, Limited scope | More secure, granular control |

### Token Storage Methods

The application uses a **centralized token management system** with the following priority order:

| Priority | Storage Method | Platform | Configuration | How to Set |
|----------|----------------|----------|---------------|------------|
| 1 | **Config File** | All | `INSTRUCTOR_TOKEN_VALUE=ghp_xxx` in `assignment.conf` | Manual edit or setup wizard |
| 2 | **Keychain** | macOS | Stored in macOS Keychain | Automatic via setup wizard |
| 3 | **Secret Service** | Linux | Stored in Secret Service (GNOME/KDE) | Automatic via setup wizard |
| 4 | **Windows Credential Manager** | Windows | Stored in Credential Manager | Automatic via setup wizard |
| 5 | **Environment Variable** | All | `GITHUB_TOKEN=ghp_xxx` | `export GITHUB_TOKEN=ghp_xxx` |

### Token Testing Scenarios

#### Test 1: Classic Token in Config File
```bash
# Create token at https://github.com/settings/tokens (classic)
# Required scopes: repo, workflow, admin:org, admin:repo_hook

# Add to assignment.conf
echo "INSTRUCTOR_TOKEN_VALUE=ghp_xxxxxxxxxxxx" >> assignment.conf

# Test
classroom-pilot assignments setup --url "https://classroom.github.com/..."
```

**Validate:**
- [ ] Token is read from config file
- [ ] Setup wizard doesn't prompt for token
- [ ] Token has sufficient permissions
- [ ] API calls succeed

#### Test 2: Fine-Grained Token in Config File
```bash
# Create token at https://github.com/settings/tokens?type=beta
# Required permissions: Contents (read/write), Pull requests (read/write), Workflows (read/write)

# Add to assignment.conf
echo "INSTRUCTOR_TOKEN_VALUE=github_pat_xxxxxxxxxxxx" >> assignment.conf

# Test
classroom-pilot assignments setup --url "https://classroom.github.com/..."
```

**Validate:**
- [ ] Fine-grained token accepted
- [ ] Proper repository/org scope enforced
- [ ] Limited permissions work correctly
- [ ] Clear error if missing required permissions

#### Test 3: Token in Keychain (macOS)
```bash
# Remove token from config file
# Setup wizard should store in keychain

classroom-pilot assignments setup

# When prompted, enter token
# Wizard will store in macOS Keychain automatically

# Verify storage
security find-generic-password -s "github-classroom-pilot" -w
```

**Validate:**
- [ ] Token stored in macOS Keychain
- [ ] Token retrieved automatically on subsequent runs
- [ ] Token not visible in config file
- [ ] Security: Token encrypted by system

#### Test 4: Token in Secret Service (Linux)
```bash
# Remove token from config file
# Setup wizard should store in Secret Service

classroom-pilot assignments setup

# When prompted, enter token
# Wizard will store in Secret Service (GNOME Keyring/KWallet)

# Verify with secret-tool (if available)
secret-tool lookup service github-classroom-pilot
```

**Validate:**
- [ ] Token stored in Secret Service
- [ ] Token retrieved automatically
- [ ] Token not in config file
- [ ] Works with GNOME/KDE environments

#### Test 5: Token in Windows Credential Manager (Windows)
```bash
# Remove token from config file
# Setup wizard should store in Windows Credential Manager

classroom-pilot assignments setup

# When prompted, enter token
# Wizard will store in Windows Credential Manager

# Verify in Control Panel > Credential Manager
```

**Validate:**
- [ ] Token stored in Credential Manager
- [ ] Token retrieved automatically
- [ ] Token not in config file
- [ ] Proper Windows security integration

#### Test 6: Token in Environment Variable
```bash
# Remove token from config file and keychain

# Set environment variable
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx

# Test
classroom-pilot assignments setup --url "https://classroom.github.com/..."
```

**Validate:**
- [ ] Token read from environment variable
- [ ] Lower priority than config file
- [ ] Works for all commands
- [ ] Session-based (not persistent)

#### Test 7: Token Import from Environment
```bash
# Set environment variable
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx

# Run setup wizard
classroom-pilot assignments setup

# Wizard should detect and offer to import token to keychain
```

**Validate:**
- [ ] Wizard detects environment token
- [ ] Offers to import to keychain
- [ ] Import successful
- [ ] Token accessible after import

#### Test 8: Missing Token Error Handling
```bash
# Remove token from all locations
# No config file token, no keychain, no environment variable

classroom-pilot assignments setup
```

**Validate:**
- [ ] Clear error message about missing token
- [ ] Instructions on how to create token
- [ ] Link to GitHub token creation page
- [ ] Option to enter token interactively

#### Test 9: Invalid Token Error Handling
```bash
# Set invalid token
echo "INSTRUCTOR_TOKEN_VALUE=invalid_token" >> assignment.conf

classroom-pilot assignments setup --url "https://classroom.github.com/..."
```

**Validate:**
- [ ] API authentication failure detected
- [ ] Clear error message
- [ ] Instructions to check token validity
- [ ] Suggestion to regenerate token

#### Test 10: Token Permission Validation
```bash
# Create token with insufficient permissions (e.g., only 'repo' scope)

classroom-pilot assignments orchestrate
```

**Validate:**
- [ ] Permission errors caught gracefully
- [ ] Specific missing permissions identified
- [ ] Instructions to update token permissions
- [ ] No partial operations executed

### Token Security Best Practices

**For QA Testing:**
- [ ] Never commit tokens to git repositories
- [ ] Use test organization, not production
- [ ] Rotate tokens after testing
- [ ] Test token revocation scenarios
- [ ] Verify tokens are not logged in verbose mode

**Expected Token Behavior:**
- Config file token takes highest priority
- Keychain/Secret Service preferred for security
- Environment variable for automation/CI
- Clear error messages for missing/invalid tokens
- Token masked in logs (shows only last 4 characters)

---

## Assignments Commands

### 1. `assignments setup`

**Purpose:** Launch interactive wizard to configure a new assignment.

**Command Variants:**

```bash
# Basic setup - interactive wizard
classroom-pilot assignments setup

# Simplified setup with minimal prompts
classroom-pilot assignments setup --simplified

# Setup with GitHub Classroom URL (auto-extracts info)
classroom-pilot assignments setup --url "https://classroom.github.com/classrooms/12345/assignments/abc123"

# Setup with global options
classroom-pilot assignments --verbose setup
classroom-pilot assignments --dry-run setup
classroom-pilot assignments --verbose --dry-run setup --simplified
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Interactive setup | `classroom-pilot assignments setup` | Wizard prompts for all configuration |
| Simplified setup | `classroom-pilot assignments setup --simplified` | Minimal prompts, uses defaults |
| URL-based setup | `classroom-pilot assignments setup --url "https://classroom.github.com/..."` | Auto-extracts org and assignment |
| Dry-run setup | `classroom-pilot assignments --dry-run setup` | Shows what would be configured |
| Verbose setup | `classroom-pilot assignments --verbose setup` | Detailed output during setup |
| Combined flags | `classroom-pilot assignments --verbose --dry-run setup --simplified` | Verbose dry-run simplified setup |

**What to Validate:**
- [ ] Assignment name extracted correctly
- [ ] Organization detected properly
- [ ] Configuration file created (`assignment.conf`)
- [ ] Token management options displayed
- [ ] All required fields populated
- [ ] Dry-run doesn't create files
- [ ] Verbose shows detailed steps

---

### 2. `assignments validate-config`

**Purpose:** Validate assignment configuration file.

**Command Variants:**

```bash
# Validate default config
classroom-pilot assignments validate-config

# Validate custom config
classroom-pilot assignments validate-config --config-file custom.conf
classroom-pilot assignments validate-config -c custom.conf

# With global options
classroom-pilot assignments --verbose validate-config
classroom-pilot assignments --dry-run validate-config
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Valid config | `classroom-pilot assignments validate-config` | ✅ Validation success message |
| Missing config | `classroom-pilot assignments validate-config -c nonexistent.conf` | ❌ Error: file not found |
| Invalid config | `classroom-pilot assignments validate-config -c broken.conf` | ❌ Error: specific validation failures |
| Custom config path | `classroom-pilot assignments validate-config -c /path/to/assignment.conf` | Validates specified file |
| Verbose mode | `classroom-pilot assignments --verbose validate-config` | Shows detailed validation steps |

**What to Validate:**
- [ ] All required fields present
- [ ] File paths exist and are accessible
- [ ] Repository URLs are valid
- [ ] GitHub organization format correct
- [ ] Error messages are clear and actionable

---

### 3. `assignments orchestrate`

**Purpose:** Execute complete assignment workflow with comprehensive orchestration.

**Command Variants:**

```bash
# Full orchestration (all steps)
classroom-pilot assignments orchestrate

# Auto-confirm all prompts
classroom-pilot assignments orchestrate --yes
classroom-pilot assignments orchestrate -y

# Execute specific step only
classroom-pilot assignments orchestrate --step sync
classroom-pilot assignments orchestrate --step discover
classroom-pilot assignments orchestrate --step secrets
classroom-pilot assignments orchestrate --step assist
classroom-pilot assignments orchestrate --step cycle

# Skip specific steps
classroom-pilot assignments orchestrate --skip sync
classroom-pilot assignments orchestrate --skip sync,discover
classroom-pilot assignments orchestrate --skip secrets,assist,cycle

# Custom config
classroom-pilot assignments orchestrate --config custom.conf
classroom-pilot assignments orchestrate -c custom.conf

# Combined options
classroom-pilot assignments --verbose --dry-run orchestrate --yes
classroom-pilot assignments orchestrate --step sync --yes --verbose
classroom-pilot assignments orchestrate --skip secrets,cycle -y -c custom.conf
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Full orchestration | `classroom-pilot assignments orchestrate` | Runs all workflow steps |
| Auto-confirm | `classroom-pilot assignments orchestrate -y` | No interactive prompts |
| Sync only | `classroom-pilot assignments orchestrate --step sync` | Only syncs template |
| Discover only | `classroom-pilot assignments orchestrate --step discover` | Only discovers repos |
| Secrets only | `classroom-pilot assignments orchestrate --step secrets` | Only manages secrets |
| Assist only | `classroom-pilot assignments orchestrate --step assist` | Only helps students |
| Cycle only | `classroom-pilot assignments orchestrate --step cycle` | Only cycles collaborators |
| Skip sync | `classroom-pilot assignments orchestrate --skip sync` | Runs all except sync |
| Skip multiple | `classroom-pilot assignments orchestrate --skip sync,secrets` | Runs all except specified |
| Dry-run full | `classroom-pilot assignments --dry-run orchestrate` | Shows what would execute |
| Verbose orchestration | `classroom-pilot assignments --verbose orchestrate -y` | Detailed execution output |

**What to Validate:**
- [ ] Steps execute in correct order
- [ ] Skipped steps are actually skipped
- [ ] Step-specific execution works
- [ ] Error handling between steps
- [ ] Dry-run doesn't execute actions
- [ ] Yes flag skips confirmations
- [ ] Progress indicators work
- [ ] Log files created properly

---

### 4. `assignments help-student`

**Purpose:** Help a specific student with repository updates.

**Command Variants:**

```bash
# Help single student (interactive)
classroom-pilot assignments help-student "https://github.com/org/assignment-student123"

# Use template directly (bypass classroom repo)
classroom-pilot assignments help-student --one-student "https://github.com/org/assignment-student123"

# Auto-confirm
classroom-pilot assignments help-student --yes "https://github.com/org/assignment-student123"
classroom-pilot assignments help-student -y "https://github.com/org/assignment-student123"

# Custom config
classroom-pilot assignments help-student --config custom.conf "https://github.com/org/assignment-student123"
classroom-pilot assignments help-student -c custom.conf "https://github.com/org/assignment-student123"

# Combined options
classroom-pilot assignments --verbose help-student --one-student --yes "https://github.com/org/assignment-student123"
classroom-pilot assignments --dry-run help-student -y -c custom.conf "https://github.com/org/assignment-student123"
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Basic help | `classroom-pilot assignments help-student "https://github.com/org/repo"` | Helps update student repo |
| One-student mode | `classroom-pilot assignments help-student --one-student "URL"` | Uses template directly |
| Auto-confirm | `classroom-pilot assignments help-student -y "URL"` | No prompts |
| Invalid URL | `classroom-pilot assignments help-student "invalid-url"` | ❌ Error: invalid URL |
| Non-existent repo | `classroom-pilot assignments help-student "https://github.com/org/fake"` | ❌ Error: repo not found |
| Dry-run help | `classroom-pilot assignments --dry-run help-student "URL"` | Shows what would be done |
| Verbose help | `classroom-pilot assignments --verbose help-student "URL"` | Detailed update process |

**What to Validate:**
- [ ] Repository access verified
- [ ] Updates applied correctly
- [ ] Conflicts handled properly
- [ ] Student notified (if configured)
- [ ] Dry-run doesn't modify repo
- [ ] One-student mode uses template
- [ ] Error messages clear

---

### 5. `assignments help-students`

**Purpose:** Help multiple students with repository updates (batch processing).

**Command Variants:**

```bash
# Batch help from file
classroom-pilot assignments help-students student-repos.txt

# Auto-confirm all
classroom-pilot assignments help-students --yes student-repos.txt
classroom-pilot assignments help-students -y student-repos.txt

# Custom config
classroom-pilot assignments help-students --config custom.conf student-repos.txt
classroom-pilot assignments help-students -c custom.conf student-repos.txt

# Combined options
classroom-pilot assignments --verbose help-students -y student-repos.txt
classroom-pilot assignments --dry-run help-students student-repos.txt
classroom-pilot assignments --verbose --dry-run help-students -y -c custom.conf student-repos.txt
```

**Test File Format (student-repos.txt):**
```
https://github.com/org/assignment-student1
https://github.com/org/assignment-student2
https://github.com/org/assignment-student3
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Batch help | `classroom-pilot assignments help-students repos.txt` | Helps all students in file |
| Auto-confirm | `classroom-pilot assignments help-students -y repos.txt` | No prompts for each student |
| Empty file | `classroom-pilot assignments help-students empty.txt` | ❌ Error or warning |
| Missing file | `classroom-pilot assignments help-students nonexistent.txt` | ❌ Error: file not found |
| Invalid URLs | `classroom-pilot assignments help-students invalid-urls.txt` | ❌ Error for bad URLs |
| Dry-run batch | `classroom-pilot assignments --dry-run help-students repos.txt` | Shows what would be done |
| Verbose batch | `classroom-pilot assignments --verbose help-students repos.txt` | Detailed progress |

**What to Validate:**
- [ ] All repos processed
- [ ] Errors don't stop batch
- [ ] Progress indicators work
- [ ] Summary report at end
- [ ] Failed repos reported
- [ ] Dry-run doesn't modify
- [ ] Log file created

---

### 6. `assignments check-student`

**Purpose:** Check the status of a student repository.

**Command Variants:**

```bash
# Check student status
classroom-pilot assignments check-student "https://github.com/org/assignment-student123"

# Custom config
classroom-pilot assignments check-student --config custom.conf "https://github.com/org/assignment-student123"
classroom-pilot assignments check-student -c custom.conf "https://github.com/org/assignment-student123"

# With global options
classroom-pilot assignments --verbose check-student "https://github.com/org/assignment-student123"
classroom-pilot assignments --dry-run check-student "https://github.com/org/assignment-student123"
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Valid repo | `classroom-pilot assignments check-student "URL"` | Shows repo status |
| Invalid URL | `classroom-pilot assignments check-student "bad-url"` | ❌ Error: invalid URL |
| Private repo | `classroom-pilot assignments check-student "private-repo-url"` | Status or access error |
| Non-existent | `classroom-pilot assignments check-student "https://github.com/org/fake"` | ❌ Error: not found |
| Verbose check | `classroom-pilot assignments --verbose check-student "URL"` | Detailed status info |

**What to Validate:**
- [ ] Repository exists
- [ ] Access permissions verified
- [ ] Commit history shown
- [ ] Branch status displayed
- [ ] Collaborators listed
- [ ] Error messages clear

---

### 7. `assignments student-instructions`

**Purpose:** Generate update instructions for a student.

**Command Variants:**

```bash
# Generate instructions (display)
classroom-pilot assignments student-instructions "https://github.com/org/assignment-student123"

# Save to file
classroom-pilot assignments student-instructions --output instructions.txt "https://github.com/org/assignment-student123"
classroom-pilot assignments student-instructions -o instructions.txt "https://github.com/org/assignment-student123"

# Custom config
classroom-pilot assignments student-instructions --config custom.conf "https://github.com/org/assignment-student123"
classroom-pilot assignments student-instructions -c custom.conf "https://github.com/org/assignment-student123"

# Combined options
classroom-pilot assignments --verbose student-instructions -o instructions.md "https://github.com/org/assignment-student123"
classroom-pilot assignments student-instructions -o inst.txt -c custom.conf "https://github.com/org/assignment-student123"
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Display instructions | `classroom-pilot assignments student-instructions "URL"` | Instructions shown in terminal |
| Save to file | `classroom-pilot assignments student-instructions -o file.txt "URL"` | Instructions saved to file |
| Invalid URL | `classroom-pilot assignments student-instructions "bad-url"` | ❌ Error: invalid URL |
| Overwrite file | `classroom-pilot assignments student-instructions -o existing.txt "URL"` | File overwritten or prompted |
| Verbose mode | `classroom-pilot assignments --verbose student-instructions "URL"` | Detailed generation process |

**What to Validate:**
- [ ] Instructions are complete
- [ ] Multiple methods provided
- [ ] Troubleshooting included
- [ ] File saved correctly
- [ ] Formatting is clear
- [ ] URLs are correct

---

### 8. `assignments check-classroom`

**Purpose:** Check if the classroom repository is ready for student updates.

**Command Variants:**

```bash
# Check classroom readiness
classroom-pilot assignments check-classroom

# Verbose check
classroom-pilot assignments check-classroom --verbose
classroom-pilot assignments check-classroom -v

# Custom config
classroom-pilot assignments check-classroom --config custom.conf
classroom-pilot assignments check-classroom -c custom.conf

# Combined options
classroom-pilot assignments --verbose check-classroom
classroom-pilot assignments --dry-run check-classroom
classroom-pilot assignments --verbose --dry-run check-classroom -c custom.conf
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Ready classroom | `classroom-pilot assignments check-classroom` | ✅ Ready status |
| Unready classroom | `classroom-pilot assignments check-classroom` | ⚠️ Issues listed |
| No config | `classroom-pilot assignments check-classroom` (no config file) | ❌ Error: config needed |
| Verbose check | `classroom-pilot assignments --verbose check-classroom` | Detailed status info |

**What to Validate:**
- [ ] Repository access verified
- [ ] Comparison with template
- [ ] Sync status shown
- [ ] Issues clearly listed
- [ ] Recommendations provided

---

### 9. `assignments manage`

**Purpose:** High-level interface for managing assignment lifecycle (placeholder).

**Command Variants:**

```bash
# Basic manage
classroom-pilot assignments manage

# With global options
classroom-pilot assignments --verbose manage
classroom-pilot assignments --dry-run manage
classroom-pilot assignments --verbose --dry-run manage
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Basic manage | `classroom-pilot assignments manage` | Shows placeholder message |
| Verbose manage | `classroom-pilot assignments --verbose manage` | Verbose placeholder |

**What to Validate:**
- [ ] Command recognized
- [ ] Placeholder message shown
- [ ] Future functionality noted

---

### 10. `assignments cycle-collaborator`

**Purpose:** Cycle collaborator permissions for a single repository.

**Command Variants:**

```bash
# Basic cycle
classroom-pilot assignments cycle-collaborator "https://github.com/org/assignment-student123" "student123"

# Force cycle (even if access appears correct)
classroom-pilot assignments cycle-collaborator --force "https://github.com/org/repo" "username"
classroom-pilot assignments cycle-collaborator -f "https://github.com/org/repo" "username"

# Custom config
classroom-pilot assignments cycle-collaborator --config custom.conf "URL" "username"
classroom-pilot assignments cycle-collaborator -c custom.conf "URL" "username"

# Combined options
classroom-pilot assignments --verbose cycle-collaborator "URL" "username"
classroom-pilot assignments --dry-run cycle-collaborator -f "URL" "username"
classroom-pilot assignments --verbose --dry-run cycle-collaborator -f -c custom.conf "URL" "username"
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Normal cycle | `classroom-pilot assignments cycle-collaborator "URL" "user"` | Cycles if needed |
| Force cycle | `classroom-pilot assignments cycle-collaborator -f "URL" "user"` | Always cycles |
| Invalid repo | `classroom-pilot assignments cycle-collaborator "bad-url" "user"` | ❌ Error: invalid URL |
| Invalid user | `classroom-pilot assignments cycle-collaborator "URL" "fakeuser"` | ❌ Error: user not found |
| Dry-run cycle | `classroom-pilot assignments --dry-run cycle-collaborator "URL" "user"` | Shows what would happen |
| Verbose cycle | `classroom-pilot assignments --verbose cycle-collaborator "URL" "user"` | Detailed permission changes |

**What to Validate:**
- [ ] Permission removal successful
- [ ] Re-invitation sent
- [ ] Access restored
- [ ] Only cycles when needed (unless forced)
- [ ] Dry-run doesn't change permissions
- [ ] Error messages clear

---

### 11. `assignments cycle-collaborators`

**Purpose:** Cycle collaborator permissions for multiple repositories (batch).

**Command Variants:**

```bash
# Batch cycle (usernames mode - default)
classroom-pilot assignments cycle-collaborators usernames.txt

# Repository URLs mode
classroom-pilot assignments cycle-collaborators --repo-urls repos.txt

# Force cycle all
classroom-pilot assignments cycle-collaborators --force usernames.txt
classroom-pilot assignments cycle-collaborators -f usernames.txt

# Custom config
classroom-pilot assignments cycle-collaborators --config custom.conf usernames.txt
classroom-pilot assignments cycle-collaborators -c custom.conf usernames.txt

# Combined options
classroom-pilot assignments --verbose cycle-collaborators --repo-urls --force repos.txt
classroom-pilot assignments --dry-run cycle-collaborators -f usernames.txt
classroom-pilot assignments --verbose --dry-run cycle-collaborators --repo-urls -f -c custom.conf repos.txt
```

**Test File Formats:**

**usernames.txt (username mode):**
```
student1
student2
student3
```

**repos.txt (repo URLs mode):**
```
https://github.com/org/assignment-student1
https://github.com/org/assignment-student2
https://github.com/org/assignment-student3
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Username batch | `classroom-pilot assignments cycle-collaborators users.txt` | Cycles for all users |
| Repo URL batch | `classroom-pilot assignments cycle-collaborators --repo-urls repos.txt` | Cycles for all repos |
| Force all | `classroom-pilot assignments cycle-collaborators -f users.txt` | Forces cycle for all |
| Empty file | `classroom-pilot assignments cycle-collaborators empty.txt` | ❌ Error or warning |
| Missing file | `classroom-pilot assignments cycle-collaborators fake.txt` | ❌ Error: file not found |
| Dry-run batch | `classroom-pilot assignments --dry-run cycle-collaborators users.txt` | Shows what would happen |
| Verbose batch | `classroom-pilot assignments --verbose cycle-collaborators users.txt` | Detailed progress |

**What to Validate:**
- [ ] All entries processed
- [ ] Errors don't stop batch
- [ ] Progress shown
- [ ] Summary report generated
- [ ] Failed cycles reported
- [ ] Dry-run doesn't modify

---

### 12. `assignments check-repository-access`

**Purpose:** Check repository access status for a specific user.

**Command Variants:**

```bash
# Check access
classroom-pilot assignments check-repository-access "https://github.com/org/assignment-student123" "student123"

# Verbose check
classroom-pilot assignments check-repository-access --verbose "URL" "username"
classroom-pilot assignments check-repository-access -v "URL" "username"

# Custom config
classroom-pilot assignments check-repository-access --config custom.conf "URL" "username"
classroom-pilot assignments check-repository-access -c custom.conf "URL" "username"

# Combined options
classroom-pilot assignments --verbose check-repository-access "URL" "username"
classroom-pilot assignments --verbose check-repository-access -v -c custom.conf "URL" "username"
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Has access | `classroom-pilot assignments check-repository-access "URL" "user"` | ✅ Access confirmed |
| No access | `classroom-pilot assignments check-repository-access "URL" "noncollab"` | ❌ No access |
| Pending invite | `classroom-pilot assignments check-repository-access "URL" "invited"` | ⚠️ Invitation pending |
| Invalid repo | `classroom-pilot assignments check-repository-access "bad-url" "user"` | ❌ Error: invalid URL |
| Invalid user | `classroom-pilot assignments check-repository-access "URL" "fakeuser"` | ❌ User not found |
| Verbose check | `classroom-pilot assignments --verbose check-repository-access "URL" "user"` | Detailed access info |

**What to Validate:**
- [ ] Access status accurate
- [ ] Collaborator role shown
- [ ] Pending invitations detected
- [ ] Error messages clear
- [ ] Recommendations provided

---

### 13. `assignments push-to-classroom`

**Purpose:** Push template repository changes to the classroom repository.

**Command Variants:**

```bash
# Interactive push (default)
classroom-pilot assignments push-to-classroom

# Force push without confirmation
classroom-pilot assignments push-to-classroom --force
classroom-pilot assignments push-to-classroom -f

# Non-interactive mode
classroom-pilot assignments push-to-classroom --non-interactive
classroom-pilot assignments push-to-classroom --non-interactive --force

# Specific branch
classroom-pilot assignments push-to-classroom --branch develop
classroom-pilot assignments push-to-classroom -b develop

# Custom config
classroom-pilot assignments push-to-classroom --config custom.conf
classroom-pilot assignments push-to-classroom -c custom.conf

# Combined options
classroom-pilot assignments --verbose push-to-classroom --force --branch main
classroom-pilot assignments --dry-run push-to-classroom -f -b develop
classroom-pilot assignments --verbose --dry-run push-to-classroom --non-interactive -f -b main -c custom.conf
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Interactive push | `classroom-pilot assignments push-to-classroom` | Prompts for confirmation |
| Force push | `classroom-pilot assignments push-to-classroom -f` | No confirmation |
| Non-interactive | `classroom-pilot assignments push-to-classroom --non-interactive` | No prompts |
| Specific branch | `classroom-pilot assignments push-to-classroom -b develop` | Pushes develop branch |
| Invalid branch | `classroom-pilot assignments push-to-classroom -b nonexistent` | ❌ Error: branch not found |
| No changes | `classroom-pilot assignments push-to-classroom` | ℹ️ Already up to date |
| Conflicts | `classroom-pilot assignments push-to-classroom` | ⚠️ Conflict warning |
| Dry-run push | `classroom-pilot assignments --dry-run push-to-classroom` | Shows what would push |
| Verbose push | `classroom-pilot assignments --verbose push-to-classroom` | Detailed push process |

**What to Validate:**
- [ ] Changes detected correctly
- [ ] Confirmation works (unless forced)
- [ ] Push successful
- [ ] Branch selection works
- [ ] Dry-run doesn't push
- [ ] Conflicts handled properly
- [ ] Error messages clear

---

## Repos Commands

### 14. `repos fetch`

**Purpose:** Discover and fetch student repositories from GitHub Classroom.

**Command Variants:**

```bash
# Basic fetch
classroom-pilot repos fetch

# Custom config
classroom-pilot repos fetch --config custom.conf
classroom-pilot repos fetch -c custom.conf

# With global options
classroom-pilot repos --verbose fetch
classroom-pilot repos --dry-run fetch
classroom-pilot repos --verbose --dry-run fetch
classroom-pilot repos --verbose --dry-run fetch -c custom.conf
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Basic fetch | `classroom-pilot repos fetch` | Discovers and clones all student repos |
| No config | `classroom-pilot repos fetch` (no config file) | ❌ Error: config required |
| No students | `classroom-pilot repos fetch` (empty student list) | ⚠️ No repos found |
| Dry-run fetch | `classroom-pilot repos --dry-run fetch` | Shows what would be fetched |
| Verbose fetch | `classroom-pilot repos --verbose fetch` | Detailed fetch progress |

**What to Validate:**
- [ ] All repos discovered
- [ ] Repos cloned successfully
- [ ] Directory structure correct
- [ ] Dry-run doesn't clone
- [ ] Progress indicators work
- [ ] Summary report generated

---

### 15. `repos update`

**Purpose:** Update assignment configuration and student repositories.

**Command Variants:**

```bash
# Basic update
classroom-pilot repos update

# Custom config
classroom-pilot repos update --config custom.conf
classroom-pilot repos update -c custom.conf

# With global options
classroom-pilot repos --verbose update
classroom-pilot repos --dry-run update
classroom-pilot repos --verbose --dry-run update
classroom-pilot repos --verbose --dry-run update -c custom.conf
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Basic update | `classroom-pilot repos update` | Updates all student repos |
| No changes | `classroom-pilot repos update` (no updates) | ℹ️ Already up to date |
| With changes | `classroom-pilot repos update` (changes exist) | Applies updates |
| Conflicts | `classroom-pilot repos update` (conflicts exist) | ⚠️ Conflict warnings |
| Dry-run update | `classroom-pilot repos --dry-run update` | Shows what would update |
| Verbose update | `classroom-pilot repos --verbose update` | Detailed update process |

**What to Validate:**
- [ ] All repos updated
- [ ] Changes applied correctly
- [ ] Conflicts detected
- [ ] Dry-run doesn't modify
- [ ] Progress shown
- [ ] Summary report generated

---

### 16. `repos push`

**Purpose:** Syncs the template repository to the GitHub Classroom repository.

**Command Variants:**

```bash
# Basic push
classroom-pilot repos push

# Custom config
classroom-pilot repos push --config custom.conf
classroom-pilot repos push -c custom.conf

# With global options
classroom-pilot repos --verbose push
classroom-pilot repos --dry-run push
classroom-pilot repos --verbose --dry-run push
classroom-pilot repos --verbose --dry-run push -c custom.conf
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Basic push | `classroom-pilot repos push` | Syncs template to classroom |
| No changes | `classroom-pilot repos push` (no changes) | ℹ️ Already up to date |
| With changes | `classroom-pilot repos push` (changes exist) | Pushes changes |
| Dry-run push | `classroom-pilot repos --dry-run push` | Shows what would push |
| Verbose push | `classroom-pilot repos --verbose push` | Detailed push process |

**What to Validate:**
- [ ] Changes detected
- [ ] Push successful
- [ ] Dry-run doesn't push
- [ ] Error messages clear
- [ ] Verification performed

---

### 17. `repos cycle-collaborator`

**Purpose:** Cycle repository collaborator permissions for assignments.

**Command Variants:**

```bash
# List collaborators
classroom-pilot repos cycle-collaborator --list

# Cycle specific user
classroom-pilot repos cycle-collaborator --username student123

# Cycle for assignment
classroom-pilot repos cycle-collaborator --assignment-prefix hw1

# Cycle for organization
classroom-pilot repos cycle-collaborator --organization myorg

# Force cycle
classroom-pilot repos cycle-collaborator --force --username student123

# Custom config
classroom-pilot repos cycle-collaborator --config custom.conf --username student123
classroom-pilot repos cycle-collaborator -c custom.conf --username student123

# Combined options
classroom-pilot repos --verbose cycle-collaborator --assignment-prefix hw1 --username student123 --organization myorg
classroom-pilot repos --dry-run cycle-collaborator --force --username student123
classroom-pilot repos --verbose --dry-run cycle-collaborator --list
classroom-pilot repos cycle-collaborator --assignment-prefix hw1 --username student123 --organization myorg --force -c custom.conf
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| List collaborators | `classroom-pilot repos cycle-collaborator --list` | Lists all collaborators |
| Cycle user | `classroom-pilot repos cycle-collaborator --username user` | Cycles user's permissions |
| Assignment prefix | `classroom-pilot repos cycle-collaborator --assignment-prefix hw1` | Cycles for hw1 repos |
| Organization | `classroom-pilot repos cycle-collaborator --organization org` | Cycles in org |
| Force cycle | `classroom-pilot repos cycle-collaborator --force --username user` | Forces cycle |
| Combined filters | `classroom-pilot repos cycle-collaborator --assignment-prefix hw1 --username user --organization org` | Cycles with filters |
| Dry-run cycle | `classroom-pilot repos --dry-run cycle-collaborator --username user` | Shows what would cycle |
| Verbose cycle | `classroom-pilot repos --verbose cycle-collaborator --list` | Detailed collaborator info |

**What to Validate:**
- [ ] List shows all collaborators
- [ ] Filters work correctly
- [ ] Cycle successful
- [ ] Force works
- [ ] Dry-run doesn't modify
- [ ] Multiple options combine properly

---

## Secrets Commands

### 18. `secrets add`

**Purpose:** Add or update secrets in student repositories.

**Command Variants:**

```bash
# Basic add (auto-discovery)
classroom-pilot secrets add

# Specify assignment root
classroom-pilot secrets add --assignment-root /path/to/template
classroom-pilot secrets add -r /path/to/template

# Specify repository URLs
classroom-pilot secrets add --repos "https://github.com/org/repo1,https://github.com/org/repo2"

# Combined options
classroom-pilot secrets add --assignment-root /path --repos "url1,url2"
classroom-pilot secrets add -r /path --repos "url1,url2"

# With global options
classroom-pilot secrets --verbose add
classroom-pilot secrets --dry-run add
classroom-pilot secrets --verbose --dry-run add
classroom-pilot secrets --verbose --dry-run add -r /path --repos "url1,url2"
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Auto-discovery | `classroom-pilot secrets add` | Discovers repos and adds secrets |
| Specific root | `classroom-pilot secrets add -r /path` | Uses specified template |
| Specific repos | `classroom-pilot secrets add --repos "url1,url2"` | Adds to specified repos |
| No secrets config | `classroom-pilot secrets add` (no secrets configured) | ⚠️ Warning or error |
| Invalid repos | `classroom-pilot secrets add --repos "bad-url"` | ❌ Error: invalid URL |
| Dry-run add | `classroom-pilot secrets --dry-run add` | Shows what secrets would be added |
| Verbose add | `classroom-pilot secrets --verbose add` | Detailed secret addition process |

**What to Validate:**
- [ ] Secrets added successfully
- [ ] All repos processed
- [ ] Encryption works
- [ ] Dry-run doesn't add secrets
- [ ] Error handling works
- [ ] Progress shown
- [ ] Summary generated

---

### 19. `secrets manage`

**Purpose:** Interface for advanced secret and token management (placeholder).

**Command Variants:**

```bash
# Basic manage
classroom-pilot secrets manage

# With global options
classroom-pilot secrets --verbose manage
classroom-pilot secrets --dry-run manage
classroom-pilot secrets --verbose --dry-run manage
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Basic manage | `classroom-pilot secrets manage` | Shows placeholder message |
| Verbose manage | `classroom-pilot secrets --verbose manage` | Verbose placeholder |

**What to Validate:**
- [ ] Command recognized
- [ ] Placeholder message shown
- [ ] Future functionality noted

---

## Automation Commands

### 20. `automation cron-install`

**Purpose:** Install cron job for automated workflow steps.

**Command Variants:**

```bash
# Install single step
classroom-pilot automation cron-install sync
classroom-pilot automation cron-install secrets
classroom-pilot automation cron-install cycle
classroom-pilot automation cron-install discover
classroom-pilot automation cron-install assist

# Install multiple steps
classroom-pilot automation cron-install sync secrets
classroom-pilot automation cron-install sync secrets cycle
classroom-pilot automation cron-install sync secrets cycle discover assist

# Custom schedule
classroom-pilot automation cron-install sync --schedule "0 2 * * *"
classroom-pilot automation cron-install sync -s "0 */4 * * *"

# Custom config
classroom-pilot automation cron-install sync --config custom.conf
classroom-pilot automation cron-install sync -c custom.conf

# Combined options
classroom-pilot automation --verbose cron-install sync secrets --schedule "0 2 * * *"
classroom-pilot automation --dry-run cron-install sync secrets cycle
classroom-pilot automation --verbose --dry-run cron-install sync -s "0 2 * * *" -c custom.conf
```

**Cron Schedule Examples:**
- `"0 2 * * *"` - Every day at 2:00 AM
- `"0 */4 * * *"` - Every 4 hours
- `"*/30 * * * *"` - Every 30 minutes
- `"0 0 * * 1"` - Every Monday at midnight
- `"0 12 * * 1-5"` - Weekdays at noon

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Install sync | `classroom-pilot automation cron-install sync` | Cron job created for sync |
| Install secrets | `classroom-pilot automation cron-install secrets` | Cron job for secrets |
| Install cycle | `classroom-pilot automation cron-install cycle` | Cron job for cycle |
| Install multiple | `classroom-pilot automation cron-install sync secrets` | Multiple jobs created |
| Custom schedule | `classroom-pilot automation cron-install sync -s "0 2 * * *"` | Uses custom schedule |
| Invalid schedule | `classroom-pilot automation cron-install sync -s "invalid"` | ❌ Error: invalid cron |
| Duplicate install | `classroom-pilot automation cron-install sync` (already exists) | Updates or warns |
| Dry-run install | `classroom-pilot automation --dry-run cron-install sync` | Shows what would install |
| Verbose install | `classroom-pilot automation --verbose cron-install sync` | Detailed installation |

**What to Validate:**
- [ ] Cron job created
- [ ] Schedule correct
- [ ] Command correct
- [ ] Multiple steps work
- [ ] Dry-run doesn't install
- [ ] Error messages clear

---

### 21. `automation cron-remove`

**Purpose:** Remove cron jobs for automated workflow steps.

**Command Variants:**

```bash
# Remove single step
classroom-pilot automation cron-remove sync
classroom-pilot automation cron-remove secrets
classroom-pilot automation cron-remove cycle

# Remove multiple steps
classroom-pilot automation cron-remove sync secrets
classroom-pilot automation cron-remove sync secrets cycle

# Remove all
classroom-pilot automation cron-remove all

# No arguments (remove all)
classroom-pilot automation cron-remove

# Custom config
classroom-pilot automation cron-remove sync --config custom.conf
classroom-pilot automation cron-remove sync -c custom.conf

# Combined options
classroom-pilot automation cron-remove sync secrets -c custom.conf
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Remove sync | `classroom-pilot automation cron-remove sync` | Removes sync cron job |
| Remove secrets | `classroom-pilot automation cron-remove secrets` | Removes secrets job |
| Remove multiple | `classroom-pilot automation cron-remove sync secrets` | Removes multiple jobs |
| Remove all | `classroom-pilot automation cron-remove all` | Removes all jobs |
| No jobs | `classroom-pilot automation cron-remove sync` (no jobs) | ℹ️ No jobs to remove |
| Non-existent | `classroom-pilot automation cron-remove fake-step` | ⚠️ Warning or error |

**What to Validate:**
- [ ] Jobs removed correctly
- [ ] Multiple removals work
- [ ] "all" removes everything
- [ ] Error messages clear
- [ ] Confirmation shown

---

### 22. `automation cron-status`

**Purpose:** Show status of installed cron jobs.

**Command Variants:**

```bash
# Basic status
classroom-pilot automation cron-status

# Custom config
classroom-pilot automation cron-status --config custom.conf
classroom-pilot automation cron-status -c custom.conf

# With global options
classroom-pilot automation --verbose cron-status
classroom-pilot automation --dry-run cron-status
classroom-pilot automation --verbose --dry-run cron-status -c custom.conf
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| With jobs | `classroom-pilot automation cron-status` | Lists all installed jobs |
| No jobs | `classroom-pilot automation cron-status` | ℹ️ No jobs installed |
| Verbose status | `classroom-pilot automation --verbose cron-status` | Detailed job information |

**What to Validate:**
- [ ] All jobs listed
- [ ] Schedules shown
- [ ] Commands shown
- [ ] Log activity shown
- [ ] Clear formatting

---

### 23. `automation cron-logs`

**Purpose:** Show recent workflow log entries.

**Command Variants:**

```bash
# Default (30 lines)
classroom-pilot automation cron-logs

# Specific number of lines
classroom-pilot automation cron-logs --lines 50
classroom-pilot automation cron-logs -n 100
classroom-pilot automation cron-logs -n 10

# Verbose mode
classroom-pilot automation cron-logs --verbose
classroom-pilot automation cron-logs -v

# Custom config
classroom-pilot automation cron-logs --config custom.conf
classroom-pilot automation cron-logs -c custom.conf

# Combined options
classroom-pilot automation cron-logs -n 50 -v -c custom.conf
classroom-pilot automation --verbose cron-logs -n 100
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Default lines | `classroom-pilot automation cron-logs` | Shows last 30 lines |
| 50 lines | `classroom-pilot automation cron-logs -n 50` | Shows last 50 lines |
| No logs | `classroom-pilot automation cron-logs` (no logs) | ℹ️ No logs available |
| Verbose logs | `classroom-pilot automation cron-logs -v` | Detailed log display |

**What to Validate:**
- [ ] Correct number of lines shown
- [ ] Most recent entries first
- [ ] Timestamps shown
- [ ] Error entries highlighted
- [ ] Clear formatting

---

### 24. `automation cron-schedules`

**Purpose:** List default schedules for workflow steps.

**Command Variants:**

```bash
# Show default schedules
classroom-pilot automation cron-schedules
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Show schedules | `classroom-pilot automation cron-schedules` | Lists all default schedules |

**What to Validate:**
- [ ] All steps shown
- [ ] Default schedules listed
- [ ] Descriptions included
- [ ] Examples provided
- [ ] Cron format explained

---

### 25. `automation cron-sync`

**Purpose:** Execute automated workflow cron job with specified steps.

**Command Variants:**

```bash
# Execute sync (default)
classroom-pilot automation cron-sync
classroom-pilot automation cron-sync sync

# Execute specific steps
classroom-pilot automation cron-sync discover
classroom-pilot automation cron-sync secrets
classroom-pilot automation cron-sync assist
classroom-pilot automation cron-sync cycle

# Execute multiple steps
classroom-pilot automation cron-sync sync secrets
classroom-pilot automation cron-sync sync discover secrets assist cycle

# Stop on failure
classroom-pilot automation cron-sync --stop-on-failure sync secrets
classroom-pilot automation cron-sync --stop-on-failure sync secrets cycle

# Show log after execution
classroom-pilot automation cron-sync --show-log sync
classroom-pilot automation cron-sync --show-log sync secrets

# Custom config
classroom-pilot automation cron-sync --config custom.conf sync
classroom-pilot automation cron-sync -c custom.conf sync

# Combined options
classroom-pilot automation --verbose cron-sync sync secrets --stop-on-failure
classroom-pilot automation --dry-run cron-sync --show-log sync secrets
classroom-pilot automation --verbose --dry-run cron-sync --stop-on-failure --show-log -c custom.conf sync secrets cycle
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Default sync | `classroom-pilot automation cron-sync` | Executes sync step |
| Sync step | `classroom-pilot automation cron-sync sync` | Executes sync |
| Discover step | `classroom-pilot automation cron-sync discover` | Executes discover |
| Multiple steps | `classroom-pilot automation cron-sync sync secrets` | Executes both |
| Stop on failure | `classroom-pilot automation cron-sync --stop-on-failure sync secrets` | Stops if sync fails |
| Show log | `classroom-pilot automation cron-sync --show-log sync` | Displays log after |
| Invalid step | `classroom-pilot automation cron-sync fake-step` | ❌ Error: invalid step |
| Dry-run sync | `classroom-pilot automation --dry-run cron-sync sync` | Shows what would execute |
| Verbose sync | `classroom-pilot automation --verbose cron-sync sync` | Detailed execution |

**What to Validate:**
- [ ] Steps execute in order
- [ ] Logs created
- [ ] Stop-on-failure works
- [ ] Show-log displays output
- [ ] Error handling works
- [ ] Dry-run doesn't execute
- [ ] Progress shown

---

### 26. `automation cron` (Legacy)

**Purpose:** Manage cron automation jobs via CLI (legacy command).

**Command Variants:**

```bash
# Status (default)
classroom-pilot automation cron
classroom-pilot automation cron --action status
classroom-pilot automation cron -a status

# Install
classroom-pilot automation cron --action install
classroom-pilot automation cron -a install

# Remove
classroom-pilot automation cron --action remove
classroom-pilot automation cron -a remove

# Custom config
classroom-pilot automation cron --config custom.conf
classroom-pilot automation cron -c custom.conf

# Combined options
classroom-pilot automation --verbose cron -a install
classroom-pilot automation --dry-run cron -a remove
classroom-pilot automation --verbose --dry-run cron -a status -c custom.conf
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Default status | `classroom-pilot automation cron` | Shows cron status |
| Status action | `classroom-pilot automation cron -a status` | Shows status |
| Install action | `classroom-pilot automation cron -a install` | Installs cron jobs |
| Remove action | `classroom-pilot automation cron -a remove` | Removes jobs |
| Invalid action | `classroom-pilot automation cron -a invalid` | ❌ Error: invalid action |
| Dry-run install | `classroom-pilot automation --dry-run cron -a install` | Shows what would install |

**What to Validate:**
- [ ] Legacy command works
- [ ] Actions work correctly
- [ ] Warning about new commands shown
- [ ] Redirects to new commands suggested

---

### 27. `automation sync`

**Purpose:** Execute scheduled synchronization tasks.

**Command Variants:**

```bash
# Basic sync
classroom-pilot automation sync

# Custom config
classroom-pilot automation sync --config custom.conf
classroom-pilot automation sync -c custom.conf

# With global options
classroom-pilot automation --verbose sync
classroom-pilot automation --dry-run sync
classroom-pilot automation --verbose --dry-run sync
classroom-pilot automation --verbose --dry-run sync -c custom.conf
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Basic sync | `classroom-pilot automation sync` | Executes scheduled sync |
| No changes | `classroom-pilot automation sync` (up to date) | ℹ️ No changes needed |
| With changes | `classroom-pilot automation sync` (changes exist) | Syncs changes |
| Dry-run sync | `classroom-pilot automation --dry-run sync` | Shows what would sync |
| Verbose sync | `classroom-pilot automation --verbose sync` | Detailed sync process |

**What to Validate:**
- [ ] Sync executes
- [ ] Changes detected
- [ ] Logs created
- [ ] Dry-run doesn't sync
- [ ] Error handling works

---

### 28. `automation batch`

**Purpose:** Run batch processing operations (placeholder).

**Command Variants:**

```bash
# Basic batch
classroom-pilot automation batch
```

**Test Scenarios:**

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| Basic batch | `classroom-pilot automation batch` | Shows placeholder message |

**What to Validate:**
- [ ] Command recognized
- [ ] Placeholder message shown
- [ ] Future functionality noted

---

## Test Execution Checklist

### Pre-Test Setup
- [ ] Python 3.10+ installed
- [ ] classroom-pilot installed (`pip install classroom-pilot`)
- [ ] GitHub token configured
- [ ] Test organization available
- [ ] Test repositories created
- [ ] Configuration file prepared
- [ ] Test data files ready (students.txt, repos.txt, etc.)

### Testing Approach

#### Phase 1: Basic Command Structure
- [ ] Test `--help` for all commands
- [ ] Test `--version`
- [ ] Verify all command groups accessible
- [ ] Check command typos/invalid commands show proper errors

#### Phase 2: Global Options
- [ ] Test `--verbose` with each command group
- [ ] Test `--dry-run` with each command group
- [ ] Test `--config` with custom config files
- [ ] Test combinations of global options

#### Phase 3: Assignments Commands
- [ ] Test `setup` with all variants
- [ ] Test `validate-config` with valid/invalid configs
- [ ] Test `orchestrate` with all step/skip combinations
- [ ] Test student help commands
- [ ] Test status checking commands
- [ ] Test collaborator cycling commands
- [ ] Test push-to-classroom with all options

#### Phase 4: Repos Commands
- [ ] Test `fetch` operations
- [ ] Test `update` operations
- [ ] Test `push` operations
- [ ] Test `cycle-collaborator` with all filters

#### Phase 5: Secrets Commands
- [ ] Test `add` with auto-discovery
- [ ] Test `add` with specific repos
- [ ] Test secret encryption
- [ ] Verify secrets added to GitHub

#### Phase 6: Automation Commands
- [ ] Test cron installation
- [ ] Test cron status
- [ ] Test cron logs
- [ ] Test cron removal
- [ ] Test automated sync execution

#### Phase 7: Error Scenarios
- [ ] Test with missing config files
- [ ] Test with invalid repository URLs
- [ ] Test with non-existent users
- [ ] Test with network issues
- [ ] Test with permission errors
- [ ] Test with invalid input files

#### Phase 8: Edge Cases
- [ ] Test with empty files
- [ ] Test with very long file lists
- [ ] Test with special characters in names
- [ ] Test with concurrent executions
- [ ] Test with interrupted operations

---

## Expected Behaviors

### Success Indicators (✅)
- Exit code: 0
- Success message displayed
- Operation completed as expected
- Log files created (if applicable)
- Progress indicators shown
- Summary reports generated

### Warning Indicators (⚠️)
- Exit code: 0 (usually)
- Warning message displayed
- Operation completed with issues
- Non-critical problems noted
- Recommendations provided

### Error Indicators (❌)
- Exit code: non-zero (typically 1)
- Error message displayed
- Operation failed or aborted
- Clear explanation provided
- Troubleshooting suggestions given

### Dry-Run Behavior
- No actual changes made
- Preview of actions shown
- Exit code: 0 (success)
- Message indicates dry-run mode
- Shows what would happen

### Verbose Behavior
- Detailed output shown
- Progress steps visible
- API calls logged (if applicable)
- Timing information included
- Debug information available

---

## Common Issues and Troubleshooting

### Configuration Issues

**Problem:** Configuration file not found  
**Test:** `classroom-pilot assignments validate-config -c nonexistent.conf`  
**Expected:** Clear error message indicating file not found  
**Solution:** Create config file or specify correct path

**Problem:** Invalid configuration format  
**Test:** Create malformed config file and validate  
**Expected:** Specific validation errors with line numbers  
**Solution:** Fix configuration according to error messages

### Authentication Issues

**Problem:** GitHub token not configured  
**Test:** Remove token and run any GitHub operation  
**Expected:** Error indicating token required  
**Solution:** Configure token via keychain or environment variable

**Problem:** Token lacks required permissions  
**Test:** Use token without correct scopes  
**Expected:** Error indicating permission denied  
**Solution:** Generate new token with correct scopes

### Repository Issues

**Problem:** Repository not found  
**Test:** Use non-existent repository URL  
**Expected:** Error indicating repository not found  
**Solution:** Verify repository URL is correct and accessible

**Problem:** No repository access  
**Test:** Use private repository without access  
**Expected:** Error indicating access denied  
**Solution:** Verify collaborator access or token permissions

### Network Issues

**Problem:** Network connection failure  
**Test:** Disconnect network and run command  
**Expected:** Error indicating connection failure  
**Solution:** Check network connection and retry

### File Issues

**Problem:** File not found  
**Test:** Reference non-existent file in command  
**Expected:** Error indicating file not found  
**Solution:** Verify file path is correct

**Problem:** Empty file  
**Test:** Use empty file for batch operations  
**Expected:** Warning indicating no entries to process  
**Solution:** Add entries to file or verify correct file used

---

## Test Result Template

Use this template to document test results:

```markdown
### Test: [Command Name]
**Date:** [Test Date]
**Tester:** [Your Name]
**Command:** `[Full Command]`

**Expected Result:**
[What should happen]

**Actual Result:**
[What actually happened]

**Status:** [✅ PASS / ❌ FAIL / ⚠️ WARNING]

**Notes:**
[Any observations, issues, or recommendations]

**Screenshots/Logs:**
[Attach if applicable]
```

---

## Quick Test Commands

### Smoke Test (Quick Validation)
```bash
# Test basic functionality
classroom-pilot --version
classroom-pilot --help
classroom-pilot assignments --help
classroom-pilot repos --help
classroom-pilot secrets --help
classroom-pilot automation --help

# Test dry-run mode
classroom-pilot assignments --dry-run validate-config
classroom-pilot repos --dry-run fetch
classroom-pilot automation --dry-run cron-status
```

### Full Test Suite (Comprehensive)
```bash
# Save this as test_all.sh and run it
#!/bin/bash

echo "=== Testing Global Options ==="
classroom-pilot --version
classroom-pilot --help

echo "=== Testing Assignments Commands ==="
classroom-pilot assignments --help
classroom-pilot assignments --dry-run setup --simplified
classroom-pilot assignments --dry-run validate-config
classroom-pilot assignments --dry-run orchestrate

echo "=== Testing Repos Commands ==="
classroom-pilot repos --help
classroom-pilot repos --dry-run fetch
classroom-pilot repos --dry-run update

echo "=== Testing Secrets Commands ==="
classroom-pilot secrets --help
classroom-pilot secrets --dry-run add

echo "=== Testing Automation Commands ==="
classroom-pilot automation --help
classroom-pilot automation cron-status
classroom-pilot automation cron-schedules

echo "=== All Tests Complete ==="
```

---

## Reporting Issues

When reporting issues found during QA testing, include:

1. **Command executed** (exact command with all options)
2. **Expected behavior** (what should have happened)
3. **Actual behavior** (what actually happened)
4. **Error messages** (full error text)
5. **Environment details** (OS, Python version, classroom-pilot version)
6. **Configuration** (relevant config file contents, sanitized)
7. **Steps to reproduce** (exact steps to trigger the issue)
8. **Screenshots/logs** (if applicable)

---

## Summary Statistics Tracking

Track these metrics during QA testing:

- **Total commands tested:** [Number]
- **Passed:** [Number] (✅)
- **Failed:** [Number] (❌)
- **Warnings:** [Number] (⚠️)
- **Not tested:** [Number]
- **Blocked:** [Number] (cannot test due to dependencies)

---

**End of QA Testing Guide**

For questions or clarifications, contact the development team.
