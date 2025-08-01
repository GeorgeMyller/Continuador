# Contributing to Auto Clicker Pro

Thank you for your interest in contributing to Auto Clicker Pro! This document provides guidelines and information for contributors.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda, or uv)

### Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/yourusername/auto-clicker-pro.git
   cd auto-clicker-pro
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]  # Install development dependencies
   ```

4. **Run tests to ensure everything works:**
   ```bash
   python -m pytest tests/ -v
   ```

## 🔧 Development Guidelines

### Code Style

We follow PEP 8 and use automated tools to maintain code quality:

- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking
- **isort** for import sorting

Run these tools before committing:
```bash
# Format code
black src/ tests/

# Check linting
flake8 src/ --max-line-length=100

# Type checking
mypy src/

# Sort imports
isort src/ tests/
```

### Testing

- Write tests for new features and bug fixes
- Maintain or improve test coverage
- Use descriptive test names and docstrings
- Mock external dependencies appropriately

```bash
# Run specific test file
python -m pytest tests/test_specific.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Commit Messages

Use clear, descriptive commit messages following this format:

```
type(scope): brief description

Detailed explanation if needed

- Bullet points for multiple changes
- Reference issues with #123

Co-authored-by: Name <email@example.com>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(detector): add support for custom color ranges

- Allow users to define custom HSV ranges
- Add validation for color range parameters
- Update configuration system

Closes #45
```

## 📝 Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Follow the coding standards
   - Add tests for new functionality
   - Update documentation if needed

3. **Test your changes:**
   ```bash
   # Run all tests
   python -m pytest tests/ -v
   
   # Run linting
   flake8 src/ --max-line-length=100
   
   # Check types
   mypy src/
   ```

4. **Commit and push:**
   ```bash
   git add .
   git commit -m "feat(scope): your descriptive message"
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request:**
   - Use the PR template
   - Provide clear description of changes
   - Link related issues
   - Request review from maintainers

### PR Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Tests pass locally
- [ ] New tests added for features
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment details:**
   - OS (macOS, Windows, Linux)
   - Python version
   - Package versions

2. **Steps to reproduce:**
   - Clear, numbered steps
   - Expected vs actual behavior
   - Screenshots if applicable

3. **Additional context:**
   - Error messages/stack traces
   - Log files if available
   - Workarounds tried

Use the bug report template in GitHub Issues.

## 💡 Feature Requests

For new features:

1. **Search existing issues** to avoid duplicates
2. **Describe the problem** you're trying to solve
3. **Propose a solution** with implementation details
4. **Consider alternatives** and their trade-offs
5. **Provide examples** of usage

## 📋 Project Structure

```
auto-clicker-pro/
├── src/                    # Source code
│   ├── __init__.py        # Package metadata
│   ├── app.py             # Main application
│   ├── config.py          # Configuration management
│   ├── detector.py        # Button detection logic
│   ├── monitor.py         # Monitoring system
│   ├── ui.py              # User interface
│   └── utils.py           # Utility functions
├── tests/                 # Test suite
├── docs/                  # Documentation
├── legacy/                # Legacy code (for reference)
├── requirements.txt       # Dependencies
├── pyproject.toml         # Project configuration
└── README.md              # Project overview
```

## 🎯 Areas for Contribution

### High Priority
- 🧪 **Test Coverage**: Expand test suite, especially GUI components
- 📱 **Cross-platform**: Improve Windows/Linux compatibility
- 🔧 **Performance**: Optimize detection algorithms
- 📚 **Documentation**: API documentation, tutorials

### Medium Priority
- 🎨 **UI/UX**: Interface improvements and accessibility
- 🔌 **Plugins**: Plugin system for extensibility
- 📊 **Analytics**: Usage metrics and performance monitoring
- 🌐 **Internationalization**: Multi-language support

### Future Ideas
- 🤖 **AI Integration**: Machine learning for better detection
- 🌐 **Web Interface**: Browser-based control panel
- 📱 **Mobile App**: Companion mobile application
- ☁️ **Cloud Features**: Settings sync, remote control

## 📞 Communication

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: General questions, ideas
- **Pull Requests**: Code contributions

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for helping make Auto Clicker Pro better! 🚀
