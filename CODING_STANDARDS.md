# Python Coding Standards

This document outlines the coding standards and development practices for this Flask application project.

## Code Style

### Black Code Formatting
- **Line Length**: 88 characters (Black default)
- **String Quotes**: Double quotes preferred
- **Trailing Commas**: Yes, for better diffs
- **Auto-formatting**: All Python code must be formatted with Black

### Import Organization (isort)
- **Profile**: Black-compatible
- **Sections**: Standard library, third-party, local imports
- **Line Length**: 88 characters
- **Multi-line Imports**: Parentheses for readability

### Linting (flake8)
- **Max Line Length**: 88 characters
- **Ignored Rules**:
  - E203: Whitespace before ':' (Black compatibility)
  - W503: Line break before binary operator (Black compatibility)
- **Additional Checks**:
  - flake8-docstrings: Docstring conventions
  - flake8-bugbear: Additional bug detection

### Type Checking (mypy)
- **Strict Mode**: Enabled for new code
- **Type Coverage**: Aim for 100% in application code
- **Exclusions**: Tests and documentation directories

## Development Workflow

### Pre-commit Hooks
All developers must install and use pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

Hooks will automatically run on `git commit`:
- Code formatting (Black)
- Import sorting (isort)
- Linting (flake8)
- Type checking (mypy)
- Basic file checks

### Testing
- **Framework**: pytest
- **Coverage**: Minimum 80% code coverage required
- **Test Organization**: Tests mirror source code structure
- **Naming**: `test_*.py` files with `test_*` functions

### Logging
- **Never use `print()` statements** in production code
- Use the structured logging system provided in `utils/logger.py`
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Include relevant context in log messages

## Project Structure

### Flask Application Structure
```
app/
├── __init__.py          # Application factory
├── models/              # Data models
├── routes/              # Route blueprints
├── services/            # Business logic services
├── templates/           # Jinja2 templates
└── static/              # Static assets (CSS, JS, images)
```

### Key Principles
- **Separation of Concerns**: Routes handle HTTP, services handle business logic
- **Blueprint Organization**: Related routes grouped in blueprints
- **Service Layer**: Business logic abstracted into services
- **Configuration Management**: Environment-based configuration

## Code Quality Guidelines

### General
- Write self-documenting code with clear variable names
- Add docstrings to all public functions, classes, and modules
- Keep functions small and focused on single responsibility
- Use type hints for function parameters and return values

### Error Handling
- Use specific exception types, not generic `Exception`
- Log errors with appropriate context
- Don't expose internal errors to users in production

### Security
- Validate all user inputs
- Use parameterized queries for database operations
- Store sensitive data securely (environment variables)
- Follow OWASP guidelines for web security

### Performance
- Avoid N+1 query problems
- Use appropriate data structures
- Cache expensive operations when beneficial
- Profile code before optimizing

## Git Workflow

### Branching Strategy
- `main`: Production-ready code
- `develop`: Integration branch
- Feature branches: `feature/REQ-XXX-description`
- Bug fixes: `fix/issue-description`

### Commit Messages
- Use imperative mood: "Add feature" not "Added feature"
- Keep first line under 50 characters
- Reference issue numbers: `REQ-002: Implement text submission system`
- Be descriptive but concise

### Pull Requests
- All changes require review
- CI/CD must pass (tests, linting, formatting)
- Include description of changes and testing done
- Squash commits when merging

## Documentation

### Code Documentation
- All public APIs must have docstrings
- Include type hints for parameters and return values
- Document exceptions that may be raised
- Update documentation when changing APIs

### Project Documentation
- Keep README.md up to date
- Document setup and deployment procedures
- Maintain API documentation
- Update changelog for releases

## Tooling

### Required Tools
- Python 3.9+
- pip for package management
- Virtual environment (venv)
- Git for version control

### Recommended IDE Setup
- VS Code with Python extension
- Pylance for type checking
- Black Formatter extension
- isort extension for import sorting

### CI/CD
- Automated testing on push/PR
- Code quality checks (linting, formatting)
- Security scanning
- Deployment automation

## Enforcement

These standards are enforced through:
- Pre-commit hooks (automatic)
- CI/CD pipeline checks
- Code review requirements
- Regular code quality audits

Violations will be caught during development and must be fixed before merging.