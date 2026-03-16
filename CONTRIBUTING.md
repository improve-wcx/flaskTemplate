# Contributing to Flask Template

Thank you for your interest in contributing to this Flask application! This document provides guidelines and information for contributors.

## Development Setup

### Prerequisites
- Python 3.9 or higher
- Git
- Virtual environment tool (venv, virtualenv, or conda)

### Initial Setup
1. Fork and clone the repository:
   ```bash
   git clone https://github.com/your-username/flask-template.git
   cd flask-template
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv env
   # On Windows:
   env\Scripts\activate
   # On Unix/MacOS:
   source env/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements/base.txt
   pip install -r requirements/dev.txt
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

5. Run initial checks:
   ```bash
   pre-commit run --all-files
   ```

## Development Workflow

### 1. Choose an Issue
- Check the [Issues](../../issues) page for open tasks
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to indicate you're working on it

### 2. Create a Feature Branch
```bash
git checkout -b feature/REQ-XXX-description
# or for bug fixes:
git checkout -b fix/issue-description
```

### 3. Make Changes
- Follow the [Coding Standards](CODING_STANDARDS.md)
- Write tests for new functionality
- Update documentation as needed
- Run pre-commit hooks: `pre-commit run --all-files`

### 4. Test Your Changes
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_specific.py

# Run linting
flake8 app/ tests/

# Type checking
mypy app/
```

### 5. Commit Changes
```bash
git add .
git commit -m "REQ-XXX: Brief description of changes"
```

Pre-commit hooks will run automatically and may make additional changes.

### 6. Push and Create Pull Request
```bash
git push origin feature/your-branch-name
```

Then create a Pull Request on GitHub with:
- Clear title referencing the issue
- Description of changes made
- Screenshots/demo if applicable
- Testing done

## Code Review Process

### For Contributors
- Address review comments promptly
- Make requested changes as separate commits or amend existing ones
- Keep the PR focused on one issue/feature

### For Reviewers
- Check code style and standards compliance
- Verify tests pass and coverage is adequate
- Test the functionality manually if needed
- Suggest improvements constructively

## Testing Guidelines

### Unit Tests
- Place in `tests/` directory mirroring source structure
- Name files `test_*.py`
- Name functions `test_*`
- Use descriptive test names
- Test both success and failure cases

### Integration Tests
- Test API endpoints with realistic data
- Test database operations
- Test external service integrations

### Test Coverage
- Aim for 80%+ code coverage
- Focus on critical business logic
- Use `pytest-cov` for coverage reports

## Documentation

### Code Documentation
- Add docstrings to all public functions/classes
- Include parameter types and descriptions
- Document exceptions raised
- Update docstrings when changing functionality

### Project Documentation
- Update README.md for significant changes
- Add migration guides for breaking changes
- Update API documentation

## Issue Reporting

### Bug Reports
Please include:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Error messages/logs

### Feature Requests
Please include:
- Clear description of the feature
- Use case and benefits
- Mockups or examples if applicable

## Commit Message Guidelines

Follow conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

Examples:
```
feat(api): add user authentication endpoint
fix(routes): handle empty request body gracefully
docs(readme): update installation instructions
```

## Release Process

### Version Numbering
Follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- Breaking changes increment MAJOR
- New features increment MINOR
- Bug fixes increment PATCH

### Release Checklist
- [ ] All tests pass
- [ ] Code coverage meets requirements
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Pre-commit hooks pass
- [ ] CI/CD pipeline passes

## Getting Help

- Check existing [Issues](../../issues) and documentation
- Ask questions in [Discussions](../../discussions)
- Join our community chat (if available)

## Recognition

Contributors are recognized in:
- GitHub contributor statistics
- CHANGELOG.md for significant contributions
- Release notes

Thank you for contributing to make this project better!