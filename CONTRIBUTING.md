# ?? Contributing to NEO ONLINE JUDGE

Thank you for considering contributing to NEO ONLINE JUDGE! This document provides guidelines and instructions for contributing.

## ?? Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)

---

## ?? Code of Conduct

We are committed to providing a welcoming and inspiring community. Please read and abide by our Code of Conduct:

- Be respectful and inclusive
- Avoid offensive language
- Report inappropriate behavior
- Treat all community members with dignity

---

## ?? Getting Started

### Prerequisites

- Python 3.8+
- Git
- Firebase account
- OpenAI API key

### Development Setup

1. **Fork the repository**
   ```bash
   # On GitHub, click "Fork"
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/NEO-ONLINE-JUDGE.git
   cd NEO-ONLINE-JUDGE
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/II-Max/NEO-ONLINE-JUDGE.git
   ```

4. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development tools
   ```

6. **Setup .env file**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

---

## ?? Making Changes

### Project Structure

```
NEO-ONLINE-JUDGE/
??? judge.py              # Main judge server
??? public/               # Frontend files
?   ??? *.html           # Web pages
?   ??? *.css            # Styles (embedded)
??? KEY/                 # Resources
??? logs/                # Logs directory
??? tests/               # Unit tests
??? docs/                # Documentation
??? config/              # Configuration files
```

### Code Style

#### Python (PEP 8)

```python
# ? Good
def process_submission(user_id, code, language):
    """Process a code submission."""
    result = compile_code(language, "temp_file", code)
    if result['error']:
        return {'status': 'error', 'message': result['error']}
    return {'status': 'success'}

# ? Bad
def process(u,c,l):
    r=compile_code(l,"t",c)
    if r['e']:return {'s':'e','m':r['e']}
    return{'s':'s'}
```

#### Naming Conventions

- Variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Classes: `PascalCase`
- Functions: `snake_case`

```python
# Constants
MAX_SUBMISSION_PER_MINUTE = 5
DATABASE_TIMEOUT = 30

# Variables
user_email = "user@example.com"
test_case_count = 10

# Functions
def calculate_score(passed_tests, total_tests):
    pass

# Classes
class CodeJudge:
    pass
```

#### Comments & Documentation

```python
def execute_and_grade(run_cmd, input_data, expected_output):
    """
    Execute code and compare with expected output.

    Args:
        run_cmd (list): Command to run the code
        input_data (str): Input to pass to the program
        expected_output (str): Expected output

    Returns:
        tuple: (score, message)
            - score: 100 if correct, 0 if wrong
            - message: Description of result

    Raises:
        subprocess.TimeoutExpired: If execution exceeds timeout
    """
    # Implementation...
    pass
```

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_judge.py

# Run specific test
pytest tests/test_judge.py::test_compile_code
```

### Example Test

```python
# tests/test_judge.py
import pytest
from judge import compile_code, execute_and_grade

def test_compile_python_code():
    """Test Python code compilation."""
    code = "print('Hello')"
    cmd, err = compile_code('python', 'temp_test', code)
    assert err is None
    assert cmd is not None

def test_execute_correct_output():
    """Test execution with correct output."""
    score, msg = execute_and_grade(
        ['python', '-c', 'print(5)'],
        '',
        '5'
    )
    assert score == 100

def test_execute_wrong_output():
    """Test execution with wrong output."""
    score, msg = execute_and_grade(
        ['python', '-c', 'print(5)'],
        '',
        '10'
    )
    assert score == 0
```

---

## ?? Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (no functional change)
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Test addition/modification
- `chore`: Build, dependencies, etc.

### Examples

```bash
# Feature
git commit -m "feat(judge): add Java support for code compilation"

# Bug fix
git commit -m "fix(api): prevent duplicate submissions in queue"

# Documentation
git commit -m "docs: update README with new configuration options"

# Refactoring
git commit -m "refactor(judge): extract compile logic into separate module"

# Performance
git commit -m "perf(database): optimize query with indexing"
```

### Commit Best Practices

- Write clear, descriptive commit messages
- Commit related changes together
- Don't commit large chunks of unrelated work
- Reference issues: `fix: resolve timeout issue (#123)`

---

## ?? Pull Request Process

### Before Creating PR

1. **Sync with upstream**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feat/your-feature-name
   ```

3. **Make your changes**
   ```bash
   # Edit files...
   git add .
   git commit -m "feat: description"
   ```

4. **Push to your fork**
   ```bash
   git push origin feat/your-feature-name
   ```

### PR Template

```markdown
## Description
Brief description of the changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Related Issues
Fixes #123

## Testing
Describe tests you've run:
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

## Checklist
- [ ] My code follows the code style
- [ ] I've added comments for complex logic
- [ ] I've updated documentation
- [ ] Tests pass locally
- [ ] No new warnings generated
```

### PR Guidelines

- Keep PRs focused on single concerns
- Keep PRs reasonably sized (< 400 lines is ideal)
- Write descriptive PR titles and descriptions
- Link to related issues
- Respond to feedback promptly

---

## ?? Reporting Bugs

### Bug Report Template

```markdown
## Description
Clear description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Environment
- OS: Windows 10 / Ubuntu 20.04 / macOS
- Python version: 3.9
- Browser: Chrome / Firefox

## Screenshots/Logs
If applicable, add screenshots or error logs.
```

### Where to Report

1. [GitHub Issues](https://github.com/II-Max/NEO-ONLINE-JUDGE/issues)
2. Include version information
3. Include reproduction steps
4. Include error messages/logs

---

## ?? Feature Requests

### Feature Request Template

```markdown
## Description
Clear description of the feature.

## Motivation
Why this feature is needed.

## Proposed Solution
How should it work?

## Alternative Solutions
Other approaches considered.

## Additional Context
Any other context.
```

### Enhancement Ideas

Check [ROADMAP.md](ROADMAP.md) for planned features before suggesting new ones.

---

## ?? Additional Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Firebase Documentation](https://firebase.google.com/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Git Documentation](https://git-scm.com/doc)

---

## ?? Project Maintainers

- @II-Max - Project lead
- Contributors team

---

## ? Questions?

- ?? Email: support@neo-judge.io
- ?? GitHub Discussions
- ?? Twitter: @neo_judge

---

**Thank you for contributing! ??**
