#!/bin/bash
# Development setup script for Auto Clicker Pro

set -e

echo "🚀 Setting up Auto Clicker Pro development environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check Python version
print_status "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
print_status "Found Python $PYTHON_VERSION"

# Check if version is 3.8 or higher
if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"; then
    print_error "Python 3.8 or higher is required. Found Python $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing dependencies..."
pip install -r requirements.txt

# Install development dependencies
print_status "Installing development dependencies..."
pip install -e .[dev] || {
    print_warning "Failed to install with pip -e .[dev], installing dev dependencies manually..."
    pip install pytest pytest-cov pytest-mock black flake8 mypy isort bandit safety
}

# Run initial tests
print_status "Running initial tests..."
python -m pytest tests/ -v || print_warning "Some tests failed, but setup continues..."

# Check code quality
print_status "Checking code formatting..."
black --check src/ tests/ || {
    print_warning "Code formatting issues found. Run 'black src/ tests/' to fix them."
}

# Setup git hooks (if .git exists)
if [ -d ".git" ]; then
    print_status "Setting up git hooks..."
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Pre-commit hook for Auto Clicker Pro

echo "Running pre-commit checks..."

# Format code with black
black src/ tests/

# Sort imports
isort src/ tests/

# Run linting
flake8 src/ --max-line-length=100

# Run tests
python -m pytest tests/ -v

echo "Pre-commit checks completed!"
EOF
    chmod +x .git/hooks/pre-commit
    print_status "Git pre-commit hook installed"
fi

# Create development directories
print_status "Creating development directories..."
mkdir -p debug_images
mkdir -p logs

print_status "✅ Development environment setup complete!"
print_status ""
print_status "To get started:"
print_status "1. Activate the virtual environment: source venv/bin/activate"
print_status "2. Run the application: python main.py"
print_status "3. Run tests: python -m pytest tests/ -v"
print_status "4. Format code: black src/ tests/"
print_status "5. Check linting: flake8 src/ --max-line-length=100"
print_status ""
print_status "Happy coding! 🎉"
