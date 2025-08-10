# Contributing

Thank you for considering contributing to PDF-PyCrack! This guide will help you get started with development and understand our contribution process.

## 🚀 Quick Start

### Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/pdf_pycrack.git
   cd pdf_pycrack
   ```

2. **Install development dependencies:**
   ```bash
   uv sync
   ```

3. **Install pre-commit hooks:**
   ```bash
   uv run pre-commit install
   ```

4. **Verify setup:**
   ```bash
   # Run tests
   uv run pytest

   # Run linting
   uv run pre-commit run --all-files

   # Test the CLI
   uv run pdf-pycrack tests/test_pdfs/numbers/100.pdf --min-len 3 --max-len 3
   ```

## 🎯 Ways to Contribute

### 🐛 Bug Reports

Found a bug? Please [open an issue](https://github.com/hornikmatej/pdf_pycrack/issues) with:

- **Clear description** of the problem
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **System information** (OS, Python version, etc.)
- **Sample files** (if applicable and safe to share)

**Example bug report:**
```markdown
## Bug: Memory leak with large character sets

**Description:**
Memory usage grows continuously when using large custom character sets.

**Steps to reproduce:**
1. Run: `pdf-pycrack file.pdf --charset-custom "very_long_charset_here" --max-len 8`
2. Monitor memory usage over time
3. Memory grows from 100MB to 2GB+ over 10 minutes

**Environment:**
- OS: Ubuntu 22.04
- Python: 3.12.1
- PDF-PyCrack: 0.1.0
- RAM: 16GB

**Expected:** Memory should remain stable
**Actual:** Memory grows continuously
```

### 💡 Feature Requests

Have an idea? [Open a feature request](https://github.com/hornikmatej/pdf_pycrack/issues) with:

- **Clear description** of the feature
- **Use case** explaining why it's needed
- **Proposed implementation** (if you have ideas)
- **Alternatives considered**

### 🔧 Code Contributions

We welcome code contributions! Here are areas where help is especially appreciated:

#### 🚀 Performance Improvements
- Algorithm optimizations
- Better multiprocessing strategies
- Memory usage improvements
- GPU acceleration (future)

#### 🛠️ Features
- Dictionary attack mode
- Resume interrupted sessions
- Progress saving/loading
- Additional output formats

#### 📖 Documentation
- API documentation improvements
- More usage examples
- Performance tuning guides
- Video tutorials

#### 🧪 Testing
- Additional test cases
- Edge case coverage
- Performance benchmarks
- Cross-platform testing

## 🔄 Development Workflow

### 1. Create a Branch

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Or bug fix branch
git checkout -b fix/issue-number-description
```

### 2. Make Changes

Follow our coding standards:

- **Code style:** We use `black` for formatting
- **Imports:** Organized with `isort`
- **Linting:** `ruff` for code quality
- **Type hints:** Use type hints where appropriate
- **Docstrings:** Follow NumPy style

### 3. Test Your Changes

```bash
# Run all tests
uv run pytest

# Run specific test categories
uv run pytest -m numbers
uv run pytest -m letters

# Run with coverage
uv run pytest --cov=src/pdf_pycrack --cov-report=html

# Test CLI manually
uv run pdf-pycrack tests/test_pdfs/numbers/100.pdf
```

### 4. Run Quality Checks

```bash
# Run all pre-commit checks
uv run pre-commit run --all-files

# Or run individual tools
uv run black src/ tests/
uv run isort src/ tests/
uv run ruff check src/ tests/
```

### 5. Update Documentation

If your changes affect user-facing functionality:

```bash
# Update relevant documentation
# docs/getting-started/, docs/user-guide/, etc.

# Test documentation build
./docs-build.sh build

# Preview documentation
./docs-build.sh serve
```

### 6. Commit and Push

```bash
# Commit with clear message
git add .
git commit -m "feat: add dictionary attack mode

- Implement word list support
- Add --dictionary flag to CLI
- Include common password lists
- Update documentation

Closes #123"

# Push to your fork
git push origin feature/your-feature-name
```

### 7. Create Pull Request

- Open a PR from your fork to the main repository
- Fill out the PR template completely
- Reference any related issues
- Wait for review and address feedback

## 📝 Coding Standards

### Code Style

We use automated tools to maintain consistent code style:

```bash
# Format code
uv run black src/ tests/

# Sort imports
uv run isort src/ tests/

# Check for issues
uv run ruff check src/ tests/
```

### Type Hints

Use type hints for better code clarity:

```python
from typing import Optional, List, Union

def crack_passwords(
    file_path: str,
    charset: str,
    min_len: int,
    max_len: int,
    processes: Optional[int] = None
) -> CrackResult:
    """Crack PDF password with given parameters."""
    # Implementation
```

### Docstrings

Use NumPy-style docstrings:

```python
def generate_passwords(charset: str, length: int) -> Iterator[str]:
    """Generate all possible passwords of given length.

    Parameters
    ----------
    charset : str
        Characters to use in password generation.
    length : int
        Length of passwords to generate.

    Yields
    ------
    str
        Generated password string.

    Examples
    --------
    >>> list(generate_passwords("abc", 2))
    ['aa', 'ab', 'ac', 'ba', 'bb', 'bc', 'ca', 'cb', 'cc']
    """
```

### Error Handling

Provide clear error messages and suggested actions:

```python
if not os.path.exists(pdf_path):
    return FileReadError(
        error=f"File not found: {pdf_path}",
        suggested_action="Check the file path and ensure the file exists"
    )
```

## 🧪 Testing Guidelines

### Test Organization

Tests are organized by functionality:

```
tests/
├── test_cli_validation.py     # CLI argument validation
├── test_core.py              # Core functionality
├── test_error_handling.py    # Error scenarios
├── test_formatting.py        # Output formatting
└── test_pdf_cracking.py      # End-to-end cracking tests
```

### Test Categories

Tests are marked with categories:

```python
import pytest

@pytest.mark.numbers
def test_numeric_passwords():
    """Test cracking numeric passwords."""

@pytest.mark.letters
def test_alphabetic_passwords():
    """Test cracking letter passwords."""

@pytest.mark.mixed
def test_mixed_passwords():
    """Test cracking mixed character passwords."""
```

Run specific categories:

```bash
uv run pytest -m numbers      # Fast numeric tests
uv run pytest -m letters     # Letter-based tests
uv run pytest -m "not mixed" # Exclude slow mixed tests
```

### Writing Good Tests

#### Test Structure

```python
def test_feature_name():
    """Test description explaining what is being tested."""
    # Arrange - set up test data
    pdf_path = "tests/test_pdfs/numbers/123.pdf"

    # Act - perform the action
    result = crack_pdf_password(pdf_path, charset="123", min_len=3, max_len=3)

    # Assert - verify the result
    assert isinstance(result, PasswordFound)
    assert result.password == "123"
```

#### Test Coverage

Aim for high test coverage of critical paths:

- Happy path scenarios
- Error conditions
- Edge cases
- Performance boundaries

```bash
# Check coverage
uv run pytest --cov=src/pdf_pycrack --cov-report=term-missing
```

### Performance Testing

For performance-critical changes, include benchmarks:

```python
def test_performance_regression():
    """Ensure performance doesn't degrade."""
    start_time = time.time()

    result = crack_pdf_password(
        "tests/test_pdfs/numbers/100.pdf",
        charset="0123456789",
        min_len=3,
        max_len=3
    )

    duration = time.time() - start_time

    # Should complete in reasonable time
    assert duration < 5.0  # 5 seconds max
    assert isinstance(result, PasswordFound)
```

## 📊 Performance Guidelines

### Benchmarking Changes

Before and after making performance changes:

```bash
# Baseline benchmark
uv run python benchmark/benchmark.py --standard

# Make your changes...

# Compare performance
uv run python benchmark/benchmark.py --standard
```

### Performance Targets

- **Throughput**: Maintain or improve passwords/second
- **Memory**: Keep memory usage under 200MB for typical operations
- **Startup**: CLI should start in <1 second
- **Scalability**: Performance should scale with CPU cores

### Profiling

For deep performance analysis:

```python
import cProfile
import pstats

def profile_cracking():
    profiler = cProfile.Profile()
    profiler.enable()

    # Your code here
    crack_pdf_password("file.pdf")

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative').print_stats(20)
```

## 🔀 Git Workflow

### Commit Messages

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `perf`: Performance improvements

**Examples:**
```
feat(cli): add dictionary attack mode

fix(core): prevent memory leak in worker processes

docs(api): improve docstring examples

perf(generator): optimize password generation algorithm
```

### Branch Naming

- `feature/feature-name`: New features
- `fix/issue-number-description`: Bug fixes
- `docs/documentation-improvements`: Documentation
- `perf/performance-optimization`: Performance work

## 🎉 Recognition

Contributors are recognized in several ways:

- **GitHub contributors list**: Automatic recognition
- **Release notes**: Major contributions highlighted
- **Documentation**: Contributor acknowledgments
- **Special thanks**: In README for significant contributions

## 🤝 Code of Conduct

We follow a simple code of conduct:

- **Be respectful** and inclusive
- **Be constructive** in feedback
- **Be patient** with new contributors
- **Be collaborative** and helpful

## 📞 Getting Help

Need help contributing?

- **Discussions**: [GitHub Discussions](https://github.com/hornikmatej/pdf_pycrack/discussions)
- **Issues**: Ask questions in [issues](https://github.com/hornikmatej/pdf_pycrack/issues)
- **Email**: Contact maintainers directly

## 🚀 What's Next?

Check out our [development roadmap](https://github.com/hornikmatej/pdf_pycrack/issues?q=is%3Aopen+is%3Aissue+label%3Aenhancement) to see what features we're planning.

Ready to contribute? We can't wait to see what you build! 🎉
