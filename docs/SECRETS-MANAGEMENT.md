# GitHub Secrets Management Script

This script automates adding secrets (like `INSTRUCTOR_TESTS_TOKEN`) to student repositories.

## Quick Setup

1. **Create token file**:
   ```bash
   echo "your_actual_github_token_here" > instructor_token.txt
   ```
   *(This file is automatically ignored by git)*

2. **Test your setup**:
   ```bash
   ./scripts/add-secrets-to-students.sh --check-token
   ```

## Usage Examples

### Add secret to single student
```bash
# Using default secret name and token file
./scripts/add-secrets-to-students.sh INSTRUCTOR_TESTS_TOKEN https://github.com/YOUR_ORG/assignment-name-student123

# Using custom token file
./scripts/add-secrets-to-students.sh INSTRUCTOR_TESTS_TOKEN --token-file my_token.txt https://github.com/YOUR_ORG/assignment-name-student123
```

### Add secrets to multiple students
```bash
# Edit student-repos-secrets.txt with your student URLs, then:
./scripts/add-secrets-to-students.sh INSTRUCTOR_TESTS_TOKEN --batch scripts/student-repos-secrets.txt
```

### Add custom secrets
```bash
# Add different types of secrets
./scripts/add-secrets-to-students.sh MY_CUSTOM_SECRET https://github.com/YOUR_ORG/assignment-name-student123
./scripts/add-secrets-to-students.sh API_KEY https://github.com/YOUR_ORG/assignment-name-student123
```

## Student Repository File Format

Create a file (like `student-repos-secrets.txt`) with one repository URL per line:
```text
# Student Repositories
https://github.com/YOUR_ORG/assignment-name-student1
https://github.com/YOUR_ORG/assignment-name-student2
https://github.com/YOUR_ORG/assignment-name-student3

# Lines starting with # are ignored
# Empty lines are also ignored
```

## Security Notes

- The `instructor_token.txt` file is automatically ignored by git
- Never commit token files to version control
- Use GitHub tokens with minimal required permissions
- Token needs `repo` and `admin:repo_hook` scopes for secret management

## Troubleshooting

**Token file not found**:
```bash
echo "your_token_here" > instructor_token.txt
```

**Permission errors**:
- Make sure your GitHub token has `repo` permissions
- Test with: `./scripts/add-secrets-to-students.sh --check-token`

**Repository access errors**:
- Verify repository URLs are correct
- Make sure you have access to student repositories
- Check if repositories exist in the organization
