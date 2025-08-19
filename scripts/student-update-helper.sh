#!/bin/bash

# =============================================================================
# student-update-helper.sh
# 
# Instructor helper script to assist students with repository updates
# 
# This script helps instructors troubleshoot and assist students who are
# having difficulty updating their repositories with template changes.
#
# Usage: 
#   ./scripts/student-update-helper.sh [student-repo-url]
#   ./scripts/student-update-helper.sh --batch [file-with-repo-urls]
#   ./scripts/student-update-helper.sh --status [student-repo-url]
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
TEMPLATE_REMOTE="origin"
CLASSROOM_REMOTE="classroom"
# NOTE: Update this URL when reusing this assignment in a different semester/class
# or when creating a new assignment. GitHub Classroom generates unique URLs for each assignment.
# Format: https://github.com/[ORG]/[classroom-semester-assignment-name]
CLASSROOM_URL="https://github.com/WSU-ML-DL/wsu-ml-dl-classroom-fall25-cs6600-m1-homework1-cs6600-m1-homework1-template"
BRANCH="main"
TEMP_DIR="/tmp/cs6600-student-helper"

# Function to print colored output
print_header() {
    echo -e "${PURPLE}=== $1 ===${NC}"
}

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_student() {
    echo -e "${CYAN}[STUDENT]${NC} $1"
}

# Function to show help
show_help() {
    cat << EOF
Student Update Helper Script - Instructor Tool

USAGE:
    $0 [student-repo-url]                    # Help specific student
    $0 --batch [file-with-urls]             # Help multiple students
    $0 --status [student-repo-url]          # Check student's update status
    $0 --check-classroom                    # Verify classroom repo is ready
    $0 --help                               # Show this help

EXAMPLES:
    # Help a specific student
    $0 https://github.com/WSU-ML-DL/cs6600-m1-homework1-student123

    # Check multiple students from a file
    $0 --batch student-repos.txt

    # Check if a student needs updates
    $0 --status https://github.com/WSU-ML-DL/cs6600-m1-homework1-student123

    # Verify classroom repository is ready for student updates
    $0 --check-classroom

FEATURES:
    - Check if students need updates
    - Clone and fix student repositories
    - Apply updates safely with backups
    - Generate status reports
    - Batch process multiple students
    - Provide update instructions for students

STUDENT REPOS FILE FORMAT (for --batch):
    https://github.com/WSU-ML-DL/cs6600-m1-homework1-student1
    https://github.com/WSU-ML-DL/cs6600-m1-homework1-student2
    https://github.com/WSU-ML-DL/cs6600-m1-homework1-student3

EOF
}

# Function to extract student name from repo URL
get_student_name() {
    local repo_url="$1"
    echo "$repo_url" | sed -E 's/.*cs6600-m1-homework1-(.+)$/\1/' | sed 's/.git$//'
}

# Function to validate repository URL
validate_repo_url() {
    local repo_url="$1"
    
    if [[ ! "$repo_url" =~ ^https://github\.com/WSU-ML-DL/.*cs6600-m1-homework1-.* ]]; then
        print_error "Invalid repository URL format"
        print_error "Expected: https://github.com/WSU-ML-DL/cs6600-m1-homework1-[student-name]"
        return 1
    fi
    
    return 0
}

# Function to check if classroom repository is ready
check_classroom_ready() {
    print_header "Checking Classroom Repository Status"
    
    print_status "Fetching classroom repository..."
    if ! git ls-remote "$CLASSROOM_URL" &>/dev/null; then
        print_error "Cannot access classroom repository: $CLASSROOM_URL"
        print_error "Please check the URL and your access permissions"
        return 1
    fi
    
    print_success "Classroom repository is accessible"
    
    # Get latest commit info
    local classroom_commit=$(git ls-remote "$CLASSROOM_URL" refs/heads/main | cut -f1)
    local local_commit=$(git rev-parse HEAD)
    
    echo "  Classroom commit: ${classroom_commit:0:8}"
    echo "  Local commit:     ${local_commit:0:8}"
    
    if [ "$classroom_commit" = "$local_commit" ]; then
        print_success "Classroom repository is up to date with local template"
    else
        print_warning "Classroom repository may not have latest changes"
        print_warning "Consider running: ./scripts/push-to-classroom.sh"
    fi
    
    return 0
}

# Function to check student repository status
check_student_status() {
    local repo_url="$1"
    local student_name
    student_name=$(get_student_name "$repo_url")
    
    print_header "Checking Status for Student: $student_name"
    
    # Check if repository is accessible
    print_status "Checking repository access..."
    if ! git ls-remote "$repo_url" &>/dev/null; then
        print_error "Cannot access student repository: $repo_url"
        print_error "Repository may be private or URL may be incorrect"
        return 1
    fi
    
    print_success "Student repository is accessible"
    
    # Get commit information
    local student_commit
    local classroom_commit
    local local_commit
    
    student_commit=$(git ls-remote "$repo_url" refs/heads/main | cut -f1)
    classroom_commit=$(git ls-remote "$CLASSROOM_URL" refs/heads/main | cut -f1)
    local_commit=$(git rev-parse HEAD)
    
    echo
    echo "Commit Status:"
    echo "  Student:   ${student_commit:0:8}"
    echo "  Classroom: ${classroom_commit:0:8}"
    echo "  Template:  ${local_commit:0:8}"
    
    if [ "$student_commit" = "$classroom_commit" ]; then
        print_success "Student is up to date with classroom repository"
        return 0
    elif [ "$student_commit" = "$local_commit" ]; then
        print_success "Student is up to date with template repository"
        return 0
    else
        print_warning "Student needs to update their repository"
        echo
        print_student "Student should run: ./scripts/update-assignment.sh"
        print_student "Or follow manual instructions in: docs/UPDATE-GUIDE.md"
        return 2  # Needs update
    fi
}

# Function to help a specific student
help_student() {
    local repo_url="$1"
    local student_name=$(get_student_name "$repo_url")
    local work_dir="$TEMP_DIR/$student_name"
    
    print_header "Helping Student: $student_name"
    
    # Validate URL
    if ! validate_repo_url "$repo_url"; then
        return 1
    fi
    
    # Check status first
    local status_result=0
    set +e  # Temporarily disable exit on error
    check_student_status "$repo_url"
    status_result=$?
    set -e  # Re-enable exit on error
    
    if [ $status_result -eq 0 ]; then
        print_success "Student is already up to date. No action needed."
        return 0
    elif [ $status_result -eq 1 ]; then
        print_error "Cannot proceed due to access issues"
        return 1
    fi
    
    # Ask for confirmation to proceed
    echo
    print_warning "This will clone the student's repository and apply updates"
    read -p "Do you want to proceed? [y/N] " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Operation cancelled"
        return 0
    fi
    
    # Setup work directory
    print_status "Setting up work directory..."
    rm -rf "$work_dir"
    mkdir -p "$work_dir"
    
    # Clone student repository
    print_status "Cloning student repository..."
    if ! git clone "$repo_url" "$work_dir"; then
        print_error "Failed to clone student repository"
        return 1
    fi
    
    cd "$work_dir"
    
    # Add classroom as remote
    print_status "Adding classroom remote..."
    git remote add upstream "$CLASSROOM_URL"
    
    # Fetch updates
    print_status "Fetching updates from classroom..."
    git fetch upstream
    
    # Create backup branch
    local backup_branch="backup-before-update-$(date +%Y%m%d-%H%M%S)"
    print_status "Creating backup branch: $backup_branch"
    git checkout -b "$backup_branch"
    git checkout main
    
    # Apply updates
    print_status "Applying updates..."
    if git merge upstream/main --no-edit --allow-unrelated-histories; then
        print_success "Updates applied successfully!"
        
        # Push changes
        print_status "Pushing updates to student repository..."
        if git push origin main && git push origin "$backup_branch"; then
            print_success "Successfully updated student repository!"
            
            # Generate summary
            echo
            print_header "Update Summary for $student_name"
            echo "✅ Backup created: $backup_branch"
            echo "✅ Updates applied from classroom repository"
            echo "✅ Changes pushed to student repository"
            echo
            print_student "Student can now pull the latest changes:"
            print_student "  git pull origin main"
            
        else
            print_error "Failed to push changes"
            print_error "You may need to resolve this manually"
        fi
        
    else
        print_warning "Merge conflicts detected!"
        echo
        print_status "Attempting automatic conflict resolution..."
        
        # Try to resolve automatically by favoring template changes for infrastructure files
        # but preserving student work in the main notebook
        git merge --abort 2>/dev/null || true
        
        if git merge upstream/main --no-edit --allow-unrelated-histories -X theirs; then
            print_status "Automatic resolution succeeded, preserving student notebook..."
            
            # Restore student's notebook from backup branch
            git checkout "$backup_branch" -- m1_homework1.ipynb 2>/dev/null || true
            
            # Commit the preserved student work
            if git diff --cached --quiet; then
                # No staged changes, add any modified files
                git add . 2>/dev/null || true
            fi
            
            if ! git diff --cached --quiet; then
                git commit -m "Preserve student work in notebook after template update" || true
            fi
            
            # Push changes
            print_status "Pushing updates to student repository..."
            if git push origin main && git push origin "$backup_branch"; then
                print_success "Successfully updated with automatic conflict resolution!"
                
                # Generate summary
                echo
                print_header "Update Summary for $student_name"
                echo "✅ Backup created: $backup_branch"
                echo "✅ Updates applied with automatic conflict resolution"
                echo "✅ Student notebook work preserved"
                echo "✅ Changes pushed to student repository"
                echo
                print_student "Student can now pull the latest changes:"
                print_student "  git pull origin main"
                
            else
                print_error "Failed to push changes after automatic resolution"
            fi
            
        else
            print_warning "Automatic resolution failed. Manual intervention required."
            echo
            print_status "Conflict resolution needed:"
            git status --porcelain | grep "^UU" | while read -r line; do
                echo "  - ${line:3}"
            done
            
            echo
            print_warning "Manual intervention required:"
            echo "1. Navigate to: $work_dir"
            echo "2. Resolve conflicts in the files listed above"
            echo "3. Run: git add <resolved-files>"
            echo "4. Run: git commit -m 'Resolve merge conflicts'"
            echo "5. Run: git push origin main && git push origin $backup_branch"
            echo
        fi
        
        print_status "Work directory preserved at: $work_dir"
        print_status "You can navigate there to resolve conflicts manually"
    fi
    
    cd - > /dev/null
    return 0
}

# Function to process multiple students
batch_help_students() {
    local repo_file="$1"
    
    if [ ! -f "$repo_file" ]; then
        print_error "Repository file not found: $repo_file"
        return 1
    fi
    
    print_header "Batch Processing Students"
    
    # Count total repositories
    local total_repos=$(grep -c "^https://" "$repo_file" || echo "0")
    print_status "Found $total_repos student repositories to process"
    
    if [ "$total_repos" -eq 0 ]; then
        print_error "No valid repository URLs found in file"
        return 1
    fi
    
    # Ask for confirmation
    echo
    read -p "Process all $total_repos repositories? [y/N] " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Batch processing cancelled"
        return 0
    fi
    
    # Process each repository
    local count=0
    local success_count=0
    local skip_count=0
    local error_count=0
    
    while IFS= read -r repo_url; do
        # Skip empty lines and comments
        [[ "$repo_url" =~ ^[[:space:]]*$ ]] && continue
        [[ "$repo_url" =~ ^[[:space:]]*# ]] && continue
        
        count=$((count + 1))
        local student_name=$(get_student_name "$repo_url")
        
        echo
        print_status "Processing $count/$total_repos: $student_name"
        
        # Check status first
        local status_result=0
        check_student_status "$repo_url" || status_result=$?
        
        if [ $status_result -eq 0 ]; then
            print_success "Already up to date - skipping"
            skip_count=$((skip_count + 1))
        elif [ $status_result -eq 1 ]; then
            print_error "Access error - skipping"
            error_count=$((error_count + 1))
        else
            # Try to help the student
            if help_student "$repo_url"; then
                success_count=$((success_count + 1))
            else
                error_count=$((error_count + 1))
            fi
        fi
        
    done < "$repo_file"
    
    # Summary
    echo
    print_header "Batch Processing Summary"
    echo "Total processed: $count"
    echo "Successfully updated: $success_count"
    echo "Already up to date: $skip_count"
    echo "Errors/skipped: $error_count"
    
    if [ $error_count -gt 0 ]; then
        print_warning "Some repositories had issues. Check output above for details."
    fi
    
    return 0
}

# Function to generate student instructions
generate_instructions() {
    local repo_url="$1"
    local student_name=$(get_student_name "$repo_url")
    
    print_header "Update Instructions for $student_name"
    
    cat << EOF

Dear $student_name,

There are updates available for the assignment template. Please follow these steps to update your repository:

OPTION 1 - Automated Script (Recommended):
1. Open your terminal in your assignment directory
2. Run: ./scripts/update-assignment.sh
3. Follow the prompts

OPTION 2 - Manual Process:
1. Save and commit your current work:
   git add .
   git commit -m "Save work before template update"

2. Add the template as a remote (one-time setup):
   git remote add upstream $CLASSROOM_URL

3. Get the updates:
   git fetch upstream
   git merge upstream/main

4. If there are conflicts, resolve them and commit:
   git add .
   git commit -m "Resolve merge conflicts"

OPTION 3 - Detailed Guide:
Follow the complete guide in: docs/UPDATE-GUIDE.md

If you encounter any issues, please:
- Check the troubleshooting section in docs/UPDATE-GUIDE.md
- Ask for help during office hours
- Contact the instructor

Best regards,
CS6600 Instructional Team

EOF
}

# Main script logic
main() {
    # Check if we're in the right repository
    if [ ! -f "m1_homework1.ipynb" ] || [ ! -d "scripts" ]; then
        print_error "This script must be run from the template repository root"
        print_error "Please navigate to cs6600-m1-homework1-template directory"
        exit 1
    fi
    
    # Parse arguments
    case "${1:-}" in
        --help|-h)
            show_help
            exit 0
            ;;
        --check-classroom)
            check_classroom_ready
            exit $?
            ;;
        --status)
            if [ -z "$2" ]; then
                print_error "Student repository URL required for --status"
                print_error "Usage: $0 --status [student-repo-url]"
                exit 1
            fi
            check_student_status "$2"
            exit $?
            ;;
        --batch)
            if [ -z "$2" ]; then
                print_error "Repository file required for --batch"
                print_error "Usage: $0 --batch [file-with-repo-urls]"
                exit 1
            fi
            batch_help_students "$2"
            exit $?
            ;;
        --instructions)
            if [ -z "$2" ]; then
                print_error "Student repository URL required for --instructions"
                exit 1
            fi
            generate_instructions "$2"
            exit 0
            ;;
        "")
            print_error "Student repository URL required"
            echo
            show_help
            exit 1
            ;;
        *)
            # Single student repository URL
            help_student "$1"
            exit $?
            ;;
    esac
}

# Cleanup function
cleanup() {
    if [ -d "$TEMP_DIR" ]; then
        print_status "Cleaning up temporary files..."
        rm -rf "$TEMP_DIR"
    fi
}

# Set up cleanup trap
trap cleanup EXIT

# Run main function
main "$@"
