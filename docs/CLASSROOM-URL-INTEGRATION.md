# GitHub Classroom URL Integration

## 🎯 Overview

The `fetch-student-repos.sh` script now supports direct integration with GitHub Classroom URLs, making it much more convenient to use with classroom assignments.

## 🚀 New Feature: --classroom-url

### Usage
```bash
./scripts/fetch-student-repos.sh --classroom-url https://classroom.github.com/classrooms/206604610-wsu-ml-dl-classroom-fall25/assignments/cs6600-m1-homework1
```

### How it Works
The script automatically extracts the assignment name from the last part of the GitHub Classroom URL:
- **Input URL:** `https://classroom.github.com/classrooms/206604610-wsu-ml-dl-classroom-fall25/assignments/cs6600-m1-homework1`
- **Extracted Assignment:** `cs6600-m1-homework1`
- **Search Pattern:** `cs6600-m1-homework1-*`

## 🧪 Testing Results

### ✅ Successful URL Extraction
```bash
# Test with the actual classroom assignment
./scripts/fetch-student-repos.sh --classroom-url https://classroom.github.com/classrooms/206604610-wsu-ml-dl-classroom-fall25/assignments/cs6600-m1-homework1 --dry-run

# Output:
[INFO] Extracted assignment prefix: cs6600-m1-homework1
=== GitHub Classroom Repository Fetcher ===
[INFO] Assignment prefix: cs6600-m1-homework1
[SUCCESS] Found 2 student repositories

[INFO] Repositories that would be saved:
[FOUND] https://github.com/WSU-ML-DL/cs6600-m1-homework1-hugo-wsu
[FOUND] https://github.com/WSU-ML-DL/cs6600-m1-homework1-instructor-tests
```

### ✅ File Generation with Classroom URL
```bash
# Generate repository file directly from classroom URL
./scripts/fetch-student-repos.sh --classroom-url https://classroom.github.com/classrooms/206604610-wsu-ml-dl-classroom-fall25/assignments/cs6600-m1-homework1 --output scripts/classroom-url-test.txt

# Results in: scripts/classroom-url-test.txt
# Content:
# https://github.com/WSU-ML-DL/cs6600-m1-homework1-hugo-wsu
# https://github.com/WSU-ML-DL/cs6600-m1-homework1-instructor-tests
```

### ✅ Different Assignment Names
```bash
# Test with hypothetical different assignment
./scripts/fetch-student-repos.sh --classroom-url https://classroom.github.com/classrooms/123456/assignments/cs6600-final-project --dry-run

# Output:
[INFO] Extracted assignment prefix: cs6600-final-project
[INFO] Assignment prefix: cs6600-final-project
[WARNING] No repositories found matching pattern: cs6600-final-project-*
```

### ✅ Error Handling
```bash
# Test with invalid URL
./scripts/fetch-student-repos.sh --classroom-url https://invalid-url.com/something

# Output:
[ERROR] Could not extract assignment name from URL: https://invalid-url.com/something
[ERROR] Expected format: https://classroom.github.com/.../assignments/ASSIGNMENT-NAME
```

## 📋 Complete Usage Examples

### Direct Classroom URL Usage
```bash
# Basic usage with classroom URL
./scripts/fetch-student-repos.sh --classroom-url https://classroom.github.com/classrooms/206604610-wsu-ml-dl-classroom-fall25/assignments/cs6600-m1-homework1

# Dry run with classroom URL
./scripts/fetch-student-repos.sh --classroom-url https://classroom.github.com/classrooms/206604610-wsu-ml-dl-classroom-fall25/assignments/cs6600-m1-homework1 --dry-run

# Custom output file with classroom URL
./scripts/fetch-student-repos.sh --classroom-url https://classroom.github.com/classrooms/206604610-wsu-ml-dl-classroom-fall25/assignments/cs6600-m1-homework1 --output scripts/my-assignment.txt

# Include template with classroom URL
./scripts/fetch-student-repos.sh --classroom-url https://classroom.github.com/classrooms/206604610-wsu-ml-dl-classroom-fall25/assignments/cs6600-m1-homework1 --include-template
```

### Complete Workflow with Classroom URL
```bash
# Step 1: Fetch repositories from classroom URL
./scripts/fetch-student-repos.sh --classroom-url https://classroom.github.com/classrooms/206604610-wsu-ml-dl-classroom-fall25/assignments/cs6600-m1-homework1

# Step 2: Add secrets to all discovered repositories
./scripts/add-secrets-to-students.sh INSTRUCTOR_TESTS_TOKEN --batch scripts/student-repos-batch.txt

# Step 3: Assist students with updates
./scripts/student-update-helper.sh --batch scripts/student-repos-batch.txt
```

## 🔧 Technical Implementation

### URL Pattern Matching
The script uses bash regex to extract assignment names:
```bash
if [[ "$url" =~ /assignments/([^/?]+) ]]; then
    echo "${BASH_REMATCH[1]}"
else
    return 1
fi
```

### Supported URL Formats
- `https://classroom.github.com/classrooms/CLASSROOM-ID/assignments/ASSIGNMENT-NAME`
- `https://classroom.github.com/classrooms/CLASSROOM-ID/assignments/ASSIGNMENT-NAME?param=value`
- `https://classroom.github.com/classrooms/CLASSROOM-ID/assignments/ASSIGNMENT-NAME/`

### Assignment Name Extraction
- Extracts everything after `/assignments/` until the next `/`, `?`, or end of string
- Works with complex assignment names like `cs6600-m1-homework1`, `final-project-2025`, etc.
- Handles URL parameters and trailing slashes gracefully

## 🎯 Benefits

### 1. **Simplified Workflow**
Instead of manually extracting assignment names:
```bash
# OLD: Manual extraction required
./scripts/fetch-student-repos.sh cs6600-m1-homework1

# NEW: Direct URL usage
./scripts/fetch-student-repos.sh --classroom-url https://classroom.github.com/classrooms/206604610-wsu-ml-dl-classroom-fall25/assignments/cs6600-m1-homework1
```

### 2. **Reduced Errors**
- No manual typing of assignment names
- Automatic extraction eliminates typos
- Consistent naming between classroom and automation

### 3. **Better Integration**
- Direct copy-paste from GitHub Classroom
- Works with bookmarked classroom URLs
- Supports sharing URLs between instructors

### 4. **Flexible Usage**
- Can still use traditional assignment prefix method
- Classroom URL is an additional option, not a replacement
- Works with all existing script features (dry-run, custom output, etc.)

## 🔄 Backward Compatibility

All existing usage patterns continue to work:
```bash
# Traditional method still works
./scripts/fetch-student-repos.sh cs6600-m1-homework1

# All flags still work
./scripts/fetch-student-repos.sh --assignment cs6600-m1-homework1 --org WSU-ML-DL

# New classroom URL method is additive
./scripts/fetch-student-repos.sh --classroom-url CLASSROOM-URL
```

## 📊 Real-World Testing

**Assignment:** CS6600 Module 1 Homework 1  
**Classroom URL:** https://classroom.github.com/classrooms/206604610-wsu-ml-dl-classroom-fall25/assignments/cs6600-m1-homework1  
**Students Found:** 1 (hugo-wsu)  
**Result:** ✅ Perfect extraction and repository discovery

This feature has been tested with the actual CS6600 GitHub Classroom assignment and works perfectly for real-world instructor workflows.

---

**Note:** This enhancement makes the automation suite even more user-friendly while maintaining all existing functionality and robust error handling.
