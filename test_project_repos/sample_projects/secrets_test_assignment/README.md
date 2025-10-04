# Calculator Assignment Test Repository

This is a test assignment repository for validating secrets management functionality in the Classroom Pilot tool.

## Assignment Overview
Students implement basic calculator functions (add, subtract, multiply, divide) with proper error handling.

## Files Structure
- `calculator.py` - Main assignment file (ASSIGNMENT_FILE)
- `assignment.ipynb` - Jupyter notebook version (ASSIGNMENT_NOTEBOOK)
- `solution.py` - Complete solution for instructor reference
- `assignment.conf` - Configuration file for classroom pilot
- `instructor_token.txt` - Token file for secrets management (gitignored)

## Testing Context
This repository is used to test:
1. Secrets management CLI commands (`classroom-pilot secrets add`)
2. BashWrapper directory context handling
3. Assignment template repository structure validation
4. Configuration file loading from different directory contexts

## Usage
```bash
# From main classroom-pilot directory
classroom-pilot secrets add --assignment-root ./test_project_repos/sample_projects/secrets_test_assignment

# Or from within this directory
cd test_project_repos/sample_projects/secrets_test_assignment
classroom-pilot secrets add
```

## Secret Configuration
- **SECRET_NAME**: INSTRUCTOR_TESTS_TOKEN
- **SECRET_VALUE**: ghp_test_token_for_instructor_tests_1234567890abcdef
- **INSTRUCTOR_TESTS_REPO**: https://github.com/test-classroom-secrets/calculator-instructor-tests