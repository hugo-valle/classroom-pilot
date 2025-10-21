# CLI Flag Structure and QA Test Fixes

**Date**: October 21, 2025  
**Branch**: feature/65-extending-test-project-repos-qa  
**Issue**: QA tests had incorrect flag ordering for `--dry-run` and `--verbose`

---

## Problem Summary

The QA tests were failing because they used incorrect flag ordering based on an outdated understanding of the CLI structure. The CLI has two levels of options:

1. **Main app options** (before subcommand group)
2. **Subcommand group options** (after subcommand group, before specific command)

---

## CLI Structure

### Correct Command Syntax

```bash
classroom-pilot [MAIN_OPTIONS] SUBCOMMAND_GROUP [GROUP_OPTIONS] COMMAND [COMMAND_OPTIONS]
```

### Option Levels

#### Level 1: Main App Options
Position: **Before** the subcommand group (`assignments`, `repos`, `secrets`, `automation`)

Available options:
- `--version` - Show version and exit
- `--config FILE` - Specify config file (default: assignment.conf)
- `--assignment-root PATH` - Root directory containing assignment.conf

**Example:**
```bash
classroom-pilot --config myconfig.conf assignments setup
classroom-pilot --assignment-root /path/to/dir assignments orchestrate
```

#### Level 2: Subcommand Group Options  
Position: **After** the subcommand group, **before** the specific command

Available options:
- `--verbose` / `-v` - Enable verbose output
- `--dry-run` - Show what would be done without executing

**Example:**
```bash
classroom-pilot assignments --verbose --dry-run setup --url "..."
classroom-pilot secrets --dry-run add --repos "..."
classroom-pilot automation --verbose sync
```

#### Level 3: Command-Specific Options
Position: **After** the specific command

Examples:
- `setup --url URL --simplified`
- `orchestrate --config FILE --step STEP`
- `add --repos REPOS --secrets FILE`

---

## Common Mistakes (Fixed in QA Tests)

### ❌ WRONG: --dry-run after command
```bash
classroom-pilot assignments setup --url "..." --dry-run
classroom-pilot assignments orchestrate --step sync --dry-run
```

### ✅ CORRECT: --dry-run after subcommand group
```bash
classroom-pilot assignments --dry-run setup --url "..."
classroom-pilot assignments --dry-run orchestrate --step sync
```

### ❌ WRONG: --verbose before subcommand group
```bash
classroom-pilot --verbose assignments setup
classroom-pilot --verbose secrets add
```

### ✅ CORRECT: --verbose after subcommand group
```bash
classroom-pilot assignments --verbose setup
classroom-pilot secrets --verbose add
```

---

## Changes Made to QA Tests

### 1. test_assignments_commands.sh

**Fixed `--dry-run` positioning** (using sed):
```bash
sed 's/classroom-pilot assignments \(.*\) --dry-run/classroom-pilot assignments --dry-run \1/g'
```

**Lines affected:** 136, 137, 156, 179, 413, 431, 449, 467, 485, 503, 521, 541, 650, 760, 1199, 1328, 1484

**Fixed `--verbose` positioning** (using sed):
```bash
sed 's/classroom-pilot --verbose assignments/classroom-pilot assignments --verbose/g'
```

**Lines affected:** 179, 320, 541, 650, 760, 850, 970, 1038, 1199, 1328, 1484

### 2. test_automation_commands.sh

**Fixed `--dry-run` positioning**:
```bash
sed 's/classroom-pilot automation sync \(.*\) --dry-run/classroom-pilot automation --dry-run sync \1/g'
```

**Lines affected:** 887

### 3. test_secrets_commands.sh

**Fixed `--dry-run` positioning**:
```bash
sed 's/classroom-pilot secrets add \(.*\) --dry-run/classroom-pilot secrets --dry-run add \1/g'
```

**Lines affected:** 757, 773

---

## Testing the Fixes

### Manual Verification

```bash
# Test --dry-run with assignments
poetry run classroom-pilot assignments --dry-run setup --url "https://classroom.github.com/a/test"
# Expected: "DRY RUN: Would run assignment setup wizard..."

# Test --verbose with assignments
poetry run classroom-pilot assignments --verbose setup --url "https://classroom.github.com/a/test"
# Expected: Verbose logging output

# Test combined flags
poetry run classroom-pilot assignments --verbose --dry-run setup --url "https://classroom.github.com/a/test"
# Expected: Both verbose output and dry-run indication
```

### QA Test Execution

```bash
# Run specific test group
bash test_project_repos/qa_tests/test_assignments_commands.sh --setup

# Run all tests
./test_local.sh --tier2
```

---

## CLI Implementation Reference

From `classroom_pilot/cli.py`:

### Main App Callback
```python
@app.callback()
def main(
    version: bool = typer.Option(False, "--version", ...),
    config_file: str = typer.Option("assignment.conf", "--config", ...),
    assignment_root: str = typer.Option(None, "--assignment-root", ...)
):
```

### Subcommand Group Callbacks
```python
@assignments_app.callback()
def assignments_callback(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v", ...),
    dry_run: bool = typer.Option(False, "--dry-run", ...)
):
```

Similar callbacks exist for:
- `repos_app.callback()`
- `secrets_app.callback()`
- `automation_app.callback()`

---

## Impact

### Before Fixes
- **Exit Code 2**: "No such option: --dry-run" errors
- **Exit Code 2**: "No such option: --verbose" errors  
- **Test Failures**: All QA tests failing due to CLI syntax errors

### After Fixes
- **Correct Flag Ordering**: All flags in proper positions
- **Tests Pass**: QA tests execute with proper CLI syntax
- **Better Documentation**: Clear understanding of CLI structure

---

## Lessons Learned

1. **Typer Structure**: Typer apps support callback functions for universal options at each level
2. **Flag Positioning Matters**: Options must be in correct position relative to their scope
3. **Test Maintenance**: QA tests need updates when CLI structure evolves
4. **Documentation Important**: Clear CLI structure documentation prevents confusion

---

## Future Recommendations

1. **CLI Help**: Ensure help text clearly indicates flag positioning
2. **Error Messages**: Improve error messages to suggest correct flag placement
3. **Test Validation**: Add pre-commit hooks to validate CLI syntax in tests
4. **Documentation**: Keep CLI structure documentation updated in README

---

## Files Modified

1. `test_project_repos/qa_tests/test_assignments_commands.sh` - 18 lines fixed
2. `test_project_repos/qa_tests/test_automation_commands.sh` - 1 line fixed
3. `test_project_repos/qa_tests/test_secrets_commands.sh` - 2 lines fixed
4. `test_local.sh` - Bug fixes for timeout and error visibility

---

## Verification Commands

```bash
# Verify no remaining incorrect flag positions
grep -r "assignments.*--dry-run" test_project_repos/qa_tests/*.sh
grep -r "secrets.*--dry-run" test_project_repos/qa_tests/*.sh
grep -r "automation.*--dry-run" test_project_repos/qa_tests/*.sh
grep -r "classroom-pilot --verbose assignments" test_project_repos/qa_tests/*.sh
grep -r "classroom-pilot --verbose repos" test_project_repos/qa_tests/*.sh
grep -r "classroom-pilot --verbose secrets" test_project_repos/qa_tests/*.sh
grep -r "classroom-pilot --verbose automation" test_project_repos/qa_tests/*.sh

# All should return: "No matches found" or correct syntax only
```

---

**Status**: ✅ All flag positions corrected and tested
