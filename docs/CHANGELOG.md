# Changelog

All notable changes to the GitHub Classroom Assignment Management Tools (gh_classroom_tools) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Note**: This tools package is designed to be used as a Git submodule in assignment template repositories.

## [Pre-released] - v1.1.0-alpha.1 - 2025-08-26

### Added
- **Flexible Secret Management Configuration**: Setup wizard now asks users whether they have tests in a separate private instructor repository or in the template repository
- **Conditional Secret Management**: STEP_MANAGE_SECRETS can be disabled when tests are included in the template repository
- **Enhanced Setup Wizard**: New Step 5 in setup-assignment.sh provides guided configuration for secret management scenarios
- **Improved Workflow Independence**: Template synchronization now works independently of repository discovery status
- **Graceful Error Handling**: Repository discovery failures no longer block template synchronization
- **Enhanced Configuration Documentation**: assignment.conf now includes comprehensive comments explaining both secret management scenarios

### Changed
- **Assignment Orchestrator Workflow**: Secret management and student assistance steps now only run when student repositories are successfully discovered
- **Setup Wizard Flow**: Increased total steps from 7 to 8 to accommodate new secret management configuration
- **Configuration File Generation**: create_config_file() now generates different SECRETS_CONFIG sections based on user choice
- **Token File Creation**: Token files are only created when secret management is enabled
- **Completion Screen**: Shows token files only when they were actually created

### Fixed
- **Template Sync Independence**: Template synchronization to GitHub Classroom now works even when no student repositories exist
- **SECRETS_CONFIG Parsing**: Added missing logic to parse multiline SECRETS_CONFIG into SECRETS array
- **Workflow Success Reporting**: Overall workflow now succeeds when template sync completes, regardless of repository discovery status

### Technical Details
- Updated `assignment-orchestrator.sh` workflow logic to make steps more independent
- Enhanced `setup-assignment.sh` with conditional token configuration
- Improved error messages to be more informative about skipped steps
- Added support for both "tests in template" and "tests in separate repo" scenarios

---

## [Pre-released] - v1.1.0-alpha.2 - 2025-08-29

### Added
- **Complete GitHub Classroom Assignment Management Suite**
- **Assignment Orchestrator**: Central workflow script (`assignment-orchestrator.sh`) that coordinates all assignment management tasks
- **Student Repository Discovery**: Automated discovery of student repositories using GitHub Classroom patterns
- **Secret Management**: Automated distribution of GitHub secrets (tokens) to student repositories
- **Template Synchronization**: Push template changes to GitHub Classroom repository
- **Interactive Setup Wizard**: Comprehensive setup script (`setup-assignment.sh`) with guided configuration
- **Batch Operations**: Support for batch processing of multiple student repositories
- **Configuration Management**: Centralized configuration through `assignment.conf`

### Core Components
- `assignment-orchestrator.sh` - Main workflow coordinator
- `setup-assignment.sh` - Interactive assignment setup wizard  
- `fetch-student-repos.sh` - Student repository discovery
- `add-secrets-to-students.sh` - Secret distribution to student repos
- `push-to-classroom.sh` - Template to classroom synchronization
- `student-update-helper.sh` - Bulk operations on student repositories

### Features
- **Multi-step Workflow**: Sync template → Discover repos → Manage secrets → Assist students
- **Dry Run Mode**: Test operations without making actual changes
- **Flexible Configuration**: Support for various assignment types and organizational structures
- **Secure Token Management**: Encrypted storage and distribution of API tokens
- **Progress Tracking**: Visual progress indicators and comprehensive logging
- **Error Handling**: Graceful error handling with informative messages
- **GitHub CLI Integration**: Seamless integration with GitHub's official CLI tool

### Installation & Usage
```bash
# Add tools as a submodule to your assignment repository
git submodule add https://github.com/hugo-valle/gh_classroom_tools.git tools

# Initialize and update the submodule
git submodule update --init --recursive

# Checkout specific version (for this alpha release)
cd tools
git checkout tags/v1.0.0-alpha.1
cd ..

# Run the setup wizard
./tools/scripts/setup-assignment.sh

# Execute the complete workflow
./tools/scripts/assignment-orchestrator.sh
```

### Requirements
- GitHub CLI (gh) installed and authenticated
- Bash 4.0 or higher
- Git
- Access to GitHub organization containing student repositories
- Appropriate permissions for repository and secret management

### Known Issues & Limitations
- ⚠️ Secret management requires repository discovery to succeed first
- ⚠️ Template synchronization depends on repository discovery workflow
- ⚠️ Limited error recovery in batch operations
- ⚠️ Minimal validation of GitHub Classroom URL formats
- ⚠️ Basic logging (enhanced logging planned for beta)

### Next Steps for v1.1.0-beta.1
- Enhanced error handling and recovery mechanisms
- Improved independence between workflow steps
- Better configuration validation
- Extended documentation and usage examples
- Performance optimizations for large batches

---

## Branching & Versioning Strategy

This project follows a Git Flow-inspired approach for release management:

### Branch Structure
- **`main`**: Production-ready code (tagged releases only)
- **`develop`**: Active development branch
- **`feature/*`**: Feature development branches
- **`release/*`**: Release preparation branches
- **`hotfix/*`**: Emergency fixes

### Versioning
We use [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

- **Alpha releases**: `v1.0.0-alpha.1, v1.0.0-alpha.2, ...`
- **Beta releases**: `v1.0.0-beta.1, v1.0.0-beta.2, ...`
- **Stable releases**: `v1.0.0, v1.1.0, v2.0.0, ...`

### Release Workflow
1. Develop features on `feature/xyz` → merge into `develop`
2. Create `release/vX.Y.Z-alpha.N` from `develop`
3. Test and finalize release branch
4. Tag the release: `git tag -a vX.Y.Z-alpha.N -m "Release message"`
5. Merge release branch into `main` and back into `develop`
6. Create GitHub Release with pre-release checkbox for alpha/beta versions

### GitHub Release Process
1. **Prepare Release Branch**:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b release/v1.1.0-alpha.1
   git push origin release/v1.1.0-alpha.1
   ```

2. **Tag the Release**:
   ```bash
   git tag -a v1.1.0-alpha.1 -m "Alpha release v1.1.0-alpha.1"
   git push origin v1.1.0-alpha.1
   ```

3. **Create GitHub Release**:
   - Go to GitHub → Releases → New Release
   - Select tag `v1.1.0-alpha.1`
   - Title: `Alpha Release v1.1.0-alpha.1`
   - Mark as "Pre-release" for alpha/beta versions
   - Include comprehensive release notes

4. **Merge Release**:
   ```bash
   git checkout main
   git merge release/v1.1.0-alpha.1
   git checkout develop  
   git merge release/v1.1.0-alpha.1
   git branch -d release/v1.1.0-alpha.1
   ```

---

## Contributing

When contributing to this project:

1. **Feature Development**: Create feature branches from `develop`
2. **Bug Fixes**: Create fix branches from `develop` (or `main` for hotfixes)
3. **Pull Requests**: Target the `develop` branch unless it's a hotfix
4. **Commit Messages**: Use conventional commit format for automated changelog generation
5. **Testing**: Ensure all tests pass before submitting PR

### Conventional Commit Format
```
feat: add conditional secret management configuration
fix: resolve template sync dependency on repository discovery  
docs: update setup wizard documentation
chore: bump version to v1.1.0-alpha.1
```

---

## Links
- [Tools Repository](https://github.com/hugo-valle/gh_classroom_tools)
- [Issues](https://github.com/hugo-valle/gh_classroom_tools/issues)
- [Releases](https://github.com/hugo-valle/gh_classroom_tools/releases)
- [Documentation](./README.md)
- [Example Assignment Template](https://github.com/WSU-ML-DL/cs6600-m1-homework2-template)
