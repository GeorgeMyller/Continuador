#!/bin/bash
# Code quality checker for Auto Clicker Pro

set -e

echo "🔍 Running code quality checks for Auto Clicker Pro..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
CHECKS_PASSED=0
CHECKS_TOTAL=0

# Function to print colored output
print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
    ((CHECKS_PASSED++))
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

check_command() {
    ((CHECKS_TOTAL++))
    if $1; then
        print_success "$2"
        return 0
    else
        print_error "$2"
        return 1
    fi
}

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    print_warning "Virtual environment not activated. Activating..."
    source venv/bin/activate 2>/dev/null || {
        print_error "Could not activate virtual environment. Please run 'source venv/bin/activate'"
        exit 1
    }
fi

print_header "Code Formatting with Black"
check_command "black --check --diff src/ tests/" "Code formatting check"

print_header "Import Sorting with isort"
check_command "isort --check-only --diff src/ tests/" "Import sorting check"

print_header "Linting with Flake8"
check_command "flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics" "Critical linting errors"
check_command "flake8 src/ --count --max-complexity=10 --max-line-length=100 --statistics" "Code quality linting"

print_header "Type Checking with MyPy"
check_command "mypy src/ --ignore-missing-imports" "Type checking"

print_header "Security Check with Bandit"
check_command "bandit -r src/ -f json -q" "Security vulnerability scan"

print_header "Dependency Security with Safety"
check_command "safety check --json --ignore 51457" "Dependency vulnerability check"

print_header "Running Tests"
check_command "python -m pytest tests/ -v --tb=short" "Unit tests"

print_header "Test Coverage"
check_command "python -m pytest tests/ --cov=src --cov-report=term --cov-fail-under=70" "Test coverage (minimum 70%)"

# Summary
echo -e "\n${BLUE}=== QUALITY CHECK SUMMARY ===${NC}"
echo -e "Checks passed: ${GREEN}$CHECKS_PASSED${NC}/$CHECKS_TOTAL"

if [ $CHECKS_PASSED -eq $CHECKS_TOTAL ]; then
    echo -e "${GREEN}🎉 All quality checks passed! Code is ready for commit.${NC}"
    exit 0
else
    echo -e "${RED}💥 Some quality checks failed. Please fix the issues before committing.${NC}"
    echo -e "\n${YELLOW}Quick fixes:${NC}"
    echo -e "  • Format code: ${BLUE}black src/ tests/${NC}"
    echo -e "  • Sort imports: ${BLUE}isort src/ tests/${NC}"
    echo -e "  • Fix linting: Check flake8 output above"
    echo -e "  • Fix types: Check mypy output above"
    exit 1
fi
