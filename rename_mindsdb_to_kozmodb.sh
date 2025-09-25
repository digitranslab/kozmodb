#!/bin/bash

# Script to rename mindsdb references to kozmodb in the project
# Handles case-sensitive renaming to avoid import issues

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
DRY_RUN=false
LOG_FILE="./rename_log_$(date +%Y%m%d_%H%M%S).txt"

# Directories to exclude from processing
EXCLUDE_DIRS=(".git" "node_modules" "__pycache__" ".pytest_cache" "env" ".venv" "venv" "build" "dist" "*.egg-info" ".tox" ".mypy_cache")

# Files to exclude from processing
EXCLUDE_FILES=("*.pyc" "*.pyo" "*.so" "*.dylib" "*.dll" "*.exe" "*.jpg" "*.png" "*.gif" "*.pdf" "*.zip" "*.tar.gz" "*.log")

# Function to print colored output
print_colored() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to log messages
log_message() {
    local message="$(date '+%Y-%m-%d %H:%M:%S') - $1"
    echo "$message" >> "$LOG_FILE"
    echo "$message"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --dry-run    Show what would be renamed without making changes"
    echo "  --execute    Actually perform the renaming"
    echo "  --help       Show this help message"
    echo ""
    echo "Case mappings:"
    echo "  mindsdb     -> kozmodb"
    echo "  Mindsdb     -> Kozmodb" 
    echo "  MindsDB     -> KozmoDB"
    echo "  MINDSDB     -> KOZMODB"
    echo "  MindSDB     -> KozmoDB"
    echo ""
}

# Function to build find exclude parameters
build_exclude_params() {
    local exclude_params=""
    
    # Exclude directories
    for dir in "${EXCLUDE_DIRS[@]}"; do
        exclude_params="$exclude_params -path ./$dir -prune -o"
    done
    
    # Exclude file patterns
    for pattern in "${EXCLUDE_FILES[@]}"; do
        exclude_params="$exclude_params -name '$pattern' -prune -o"
    done
    
    echo "$exclude_params"
}

# Function to check if file should be processed
should_process_file() {
    local file_path=$1
    
    # Skip if file is binary
    if file "$file_path" | grep -q "binary"; then
        return 1
    fi
    
    # Skip large files (>10MB)
    if [[ $(stat -c%s "$file_path" 2>/dev/null || stat -f%z "$file_path" 2>/dev/null) -gt 10485760 ]]; then
        return 1
    fi
    
    return 0
}


# Function to apply case-sensitive replacements in file content
apply_content_replacements() {
    local file_path=$1
    local changes_made=false
    
    if should_process_file "$file_path"; then
        local temp_file=$(mktemp)
        
        # Apply replacements in order (most specific first)
        sed 's/MindsDB/KozmoDB/g; s/MindSDB/KozmoDB/g; s/Mindsdb/Kozmodb/g; s/mindsdb/kozmodb/g; s/MINDSDB/KOZMODB/g' "$file_path" > "$temp_file"
        
        # Check if changes were made
        if ! cmp -s "$file_path" "$temp_file"; then
            if [[ $DRY_RUN == true ]]; then
                print_colored $YELLOW "Would modify content: $file_path"
                # Show diff
                diff -u "$file_path" "$temp_file" | head -20 || true
            else
                mv "$temp_file" "$file_path"
                log_message "Modified content in: $file_path"
                print_colored $GREEN "Modified content: $file_path"
            fi
            changes_made=true
        fi
        
        rm -f "$temp_file"
    fi
    
    return $([[ $changes_made == true ]] && echo 0 || echo 1)
}

# Function to rename files and directories
rename_paths() {
    local changes_made=false
    
    print_colored $BLUE "Scanning for files and directories to rename..."
    
    # Find files and directories containing mindsdb variations (case sensitive)
    # Process files first, then directories (to avoid path issues)
    
    exclude_params=$(build_exclude_params)
    
    # Find and rename files
    while IFS= read -r -d '' file; do
        local dirname=$(dirname "$file")
        local basename=$(basename "$file")
        local new_basename=""
        
        # Apply case-sensitive replacements to basename
        new_basename=$(echo "$basename" | sed 's/MindsDB/KozmoDB/g; s/MindSDB/KozmoDB/g; s/Mindsdb/Kozmodb/g; s/mindsdb/kozmodb/g; s/MINDSDB/KOZMODB/g')
        
        if [[ "$basename" != "$new_basename" ]]; then
            local new_path="$dirname/$new_basename"
            
            if [[ $DRY_RUN == true ]]; then
                print_colored $YELLOW "Would rename file: $file -> $new_path"
            else
                if [[ ! -e "$new_path" ]]; then
                    mv "$file" "$new_path"
                    log_message "Renamed file: $file -> $new_path"
                    print_colored $GREEN "Renamed file: $file -> $new_path"
                    changes_made=true
                else
                    print_colored $RED "Cannot rename $file to $new_path: destination exists"
                    log_message "ERROR: Cannot rename $file to $new_path: destination exists"
                fi
            fi
        fi
    done < <(eval "find . $exclude_params -type f -print0")
    
    # Find and rename directories (in reverse order to handle nested directories)
    while IFS= read -r -d '' dir; do
        local parent_dir=$(dirname "$dir")
        local dir_name=$(basename "$dir")
        local new_dir_name=""
        
        # Apply case-sensitive replacements to directory name
        new_dir_name=$(echo "$dir_name" | sed 's/MindsDB/KozmoDB/g; s/MindSDB/KozmoDB/g; s/Mindsdb/Kozmodb/g; s/mindsdb/kozmodb/g; s/MINDSDB/KOZMODB/g')
        
        if [[ "$dir_name" != "$new_dir_name" ]]; then
            local new_path="$parent_dir/$new_dir_name"
            
            if [[ $DRY_RUN == true ]]; then
                print_colored $YELLOW "Would rename directory: $dir -> $new_path"
            else
                if [[ ! -e "$new_path" ]]; then
                    mv "$dir" "$new_path"
                    log_message "Renamed directory: $dir -> $new_path"
                    print_colored $GREEN "Renamed directory: $dir -> $new_path"
                    changes_made=true
                else
                    print_colored $RED "Cannot rename $dir to $new_path: destination exists"
                    log_message "ERROR: Cannot rename $dir to $new_path: destination exists"
                fi
            fi
        fi
    done < <(eval "find . $exclude_params -type d -print0" | sort -rz)
    
    return $([[ $changes_made == true ]] && echo 0 || echo 1)
}

# Function to process file contents
process_file_contents() {
    local total_files=0
    local modified_files=0
    
    print_colored $BLUE "Processing file contents..."
    
    exclude_params=$(build_exclude_params)
    
    while IFS= read -r -d '' file; do
        ((total_files++))
        
        if apply_content_replacements "$file"; then
            ((modified_files++))
        fi
        
        # Show progress every 100 files
        if [[ $((total_files % 100)) -eq 0 ]]; then
            print_colored $BLUE "Processed $total_files files..."
        fi
        
    done < <(eval "find . $exclude_params -type f -print0")
    
    print_colored $BLUE "Processed $total_files files total, modified $modified_files files"
    log_message "Content processing complete: $total_files files processed, $modified_files modified"
}

# Function to show summary of what would be changed
show_dry_run_summary() {
    print_colored $BLUE "=== DRY RUN SUMMARY ==="
    print_colored $YELLOW "The following changes would be made:"
    echo ""
    
    print_colored $BLUE "Case mappings that will be applied:"
    echo "  mindsdb     -> kozmodb"
    echo "  Mindsdb     -> Kozmodb" 
    echo "  MindsDB     -> KozmoDB"
    echo "  MINDSDB     -> KOZMODB"
    echo "  MindSDB     -> KozmoDB"
    echo ""
    
    print_colored $BLUE "Excluded directories:"
    printf '  %s\n' "${EXCLUDE_DIRS[@]}"
    echo ""
    
    print_colored $BLUE "Excluded file patterns:"
    printf '  %s\n' "${EXCLUDE_FILES[@]}"
    echo ""
}

# Main execution function
main() {
    print_colored $GREEN "KozmoDB Renaming Script"
    print_colored $GREEN "======================"
    echo ""
    
    if [[ $DRY_RUN == true ]]; then
        print_colored $YELLOW "DRY RUN MODE - No changes will be made"
        show_dry_run_summary
    else
        print_colored $BLUE "EXECUTION MODE - Renaming files and content now..."
    fi
    
    log_message "Starting rename operation (DRY_RUN=$DRY_RUN)"
    
    # Step 1: Rename files and directories
    print_colored $BLUE "Step 1: Renaming files and directories..."
    rename_paths
    
    # Step 2: Process file contents
    print_colored $BLUE "Step 2: Processing file contents..."
    process_file_contents
    
    if [[ $DRY_RUN == true ]]; then
        print_colored $YELLOW "Dry run complete. Review the changes above."
        print_colored $YELLOW "To execute the changes, run: $0 --execute"
    else
        print_colored $GREEN "Renaming operation completed successfully!"
        print_colored $GREEN "Log file: $LOG_FILE"
    fi
}

# Parse command line arguments
case "${1:-}" in
    --dry-run)
        DRY_RUN=true
        ;;
    --execute)
        DRY_RUN=false
        ;;
    --help)
        show_usage
        exit 0
        ;;
    "")
        print_colored $YELLOW "No option specified. Use --help for usage information."
        print_colored $YELLOW "Use --dry-run to see what would be changed without making changes."
        print_colored $YELLOW "Use --execute to actually perform the renaming."
        exit 1
        ;;
    *)
        print_colored $RED "Unknown option: $1"
        show_usage
        exit 1
        ;;
esac

# Run the main function
main
