# Testing

PDF-PyCrack includes a comprehensive test suite designed to ensure reliability, performance, and correctness across different scenarios. This guide covers how to run tests, write new tests, and understand our testing strategy.

## 🚀 Quick Start

### Running All Tests

```bash
# Run the complete test suite
uv run pytest

# Run with verbose output
uv run pytest -v

# Run with coverage report
uv run pytest --cov=src/pdf_pycrack --cov-report=html
```

### Running Specific Test Categories

Tests are organized by character sets for efficient testing:

```bash
# Fast numeric tests (recommended for development)
uv run pytest -m numbers

# Letter-based tests
uv run pytest -m letters

# Special character tests
uv run pytest -m special_chars

# Mixed character tests (slower)
uv run pytest -m mixed

# Combine categories
uv run pytest -m "numbers or letters"

# Exclude slow tests
uv run pytest -m "not mixed"
```

## 📁 Test Structure

### Test Organization

```
tests/
├── test_cli_validation.py     # CLI argument validation tests
├── test_core.py              # Core functionality tests
├── test_error_handling.py    # Error scenario tests
├── test_formatting.py        # Output formatting tests
├── test_pdf_cracking.py      # End-to-end cracking tests
└── test_pdfs/               # Test PDF files
    ├── numbers/             # Numeric password PDFs
    ├── letters/             # Letter password PDFs
    ├── special_chars/       # Special character PDFs
    ├── mixed/              # Mixed character PDFs
    └── unencrypted.pdf     # Non-encrypted test file
```

### Test Categories

Tests are marked with pytest markers for selective execution:

| Marker | Description | Speed | Use Case |
|--------|-------------|--------|----------|
| `numbers` | Numeric passwords only | Fast | Development testing |
| `letters` | Alphabetic passwords | Medium | Feature testing |
| `special_chars` | Special characters | Medium | Edge case testing |
| `mixed` | Mixed character sets | Slow | Comprehensive testing |

## 🧪 Test Files

### Test PDF Structure

The test PDFs are organized by password type:

```bash
tests/test_pdfs/
├── numbers/
│   ├── 1.pdf          # Password: "1"
│   ├── 12.pdf         # Password: "12"
│   ├── 123.pdf        # Password: "123"
│   └── 100.pdf        # Password: "100"
├── letters/
│   ├── a.pdf          # Password: "a"
│   ├── ab.pdf         # Password: "ab"
│   └── abc.pdf        # Password: "abc"
├── special_chars/
│   ├── !.pdf          # Password: "!"
│   └── @#.pdf         # Password: "@#"
└── mixed/
    ├── a1.pdf         # Password: "a1"
    └── Test123.pdf    # Password: "Test123"
```

### Creating Test PDFs

To create new test PDFs, use the script generator:

```bash
# See available options
uv run python scripts/generate_pdfs.py --help

# Generate a new test PDF
uv run python scripts/generate_pdfs.py --password "newpass" --output tests/test_pdfs/custom/newpass.pdf
```

## 🔍 Test Categories Explained

### Numeric Tests (`@pytest.mark.numbers`)

Fast tests using numeric passwords:

```python
@pytest.mark.numbers
def test_simple_numeric_password():
    """Test cracking simple numeric passwords."""
    result = crack_pdf_password(
        "tests/test_pdfs/numbers/123.pdf",
        charset="0123456789",
        min_len=3,
        max_len=3
    )
    assert isinstance(result, PasswordFound)
    assert result.password == "123"
```

**Characteristics:**
- **Speed**: Very fast (seconds)
- **Character set**: `0123456789` (10 characters)
- **Use case**: Development and quick validation

### Letter Tests (`@pytest.mark.letters`)

Medium-speed tests with alphabetic passwords:

```python
@pytest.mark.letters
def test_alphabetic_password():
    """Test cracking alphabetic passwords."""
    result = crack_pdf_password(
        "tests/test_pdfs/letters/abc.pdf",
        charset="abcdefghijklmnopqrstuvwxyz",
        min_len=3,
        max_len=3
    )
    assert isinstance(result, PasswordFound)
    assert result.password == "abc"
```

**Characteristics:**
- **Speed**: Medium (tens of seconds)
- **Character set**: `a-z` (26 characters)
- **Use case**: Feature testing and validation

### Special Character Tests (`@pytest.mark.special_chars`)

Tests with special characters:

```python
@pytest.mark.special_chars
def test_special_character_password():
    """Test cracking passwords with special characters."""
    result = crack_pdf_password(
        "tests/test_pdfs/special_chars/!.pdf",
        charset="!@#$%^&*()_+-=[]{}|;:,.<>?",
        min_len=1,
        max_len=1
    )
    assert isinstance(result, PasswordFound)
    assert result.password == "!"
```

### Mixed Tests (`@pytest.mark.mixed`)

Comprehensive but slower tests:

```python
@pytest.mark.mixed
def test_mixed_character_password():
    """Test cracking mixed character passwords."""
    result = crack_pdf_password(
        "tests/test_pdfs/mixed/Test123.pdf",
        charset="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        min_len=7,
        max_len=7
    )
    assert isinstance(result, PasswordFound)
    assert result.password == "Test123"
```

**Characteristics:**
- **Speed**: Slow (minutes)
- **Character set**: Mixed (62+ characters)
- **Use case**: Final validation and stress testing

## 🎯 Test Development

### Writing New Tests

#### 1. Choose the Right Category

Select the appropriate marker based on test characteristics:

```python
import pytest

# Fast development test
@pytest.mark.numbers
def test_new_numeric_feature():
    pass

# Comprehensive validation test
@pytest.mark.mixed
def test_complex_scenario():
    pass
```

#### 2. Follow Test Structure

Use the Arrange-Act-Assert pattern:

```python
def test_feature_name():
    """Clear description of what is being tested."""
    # Arrange - set up test data
    pdf_path = "tests/test_pdfs/numbers/123.pdf"
    expected_password = "123"

    # Act - perform the action
    result = crack_pdf_password(
        pdf_path,
        charset="0123456789",
        min_len=3,
        max_len=3
    )

    # Assert - verify the result
    assert isinstance(result, PasswordFound)
    assert result.password == expected_password
    assert result.passwords_tested > 0
```

#### 3. Test Both Success and Failure

```python
@pytest.mark.numbers
def test_password_found():
    """Test successful password discovery."""
    result = crack_pdf_password("tests/test_pdfs/numbers/123.pdf", ...)
    assert isinstance(result, PasswordFound)

@pytest.mark.numbers
def test_password_not_found():
    """Test when password is not in search space."""
    result = crack_pdf_password(
        "tests/test_pdfs/numbers/123.pdf",
        charset="abcd",  # Wrong charset
        min_len=3,
        max_len=3
    )
    assert isinstance(result, PasswordNotFound)
```

### Error Testing

Test error conditions thoroughly:

```python
def test_file_not_found():
    """Test handling of non-existent files."""
    result = crack_pdf_password("nonexistent.pdf")
    assert isinstance(result, FileReadError)
    assert "not found" in result.error.lower()

def test_not_encrypted():
    """Test handling of unencrypted PDFs."""
    result = crack_pdf_password("tests/test_pdfs/unencrypted.pdf")
    assert isinstance(result, NotEncrypted)

def test_invalid_parameters():
    """Test invalid parameter combinations."""
    result = crack_pdf_password(
        "tests/test_pdfs/numbers/123.pdf",
        min_len=5,
        max_len=3  # Invalid: min > max
    )
    assert isinstance(result, (InitializationError, ValueError))
```

### Performance Testing

Include performance validation:

```python
import time

@pytest.mark.numbers
def test_performance_baseline():
    """Ensure performance doesn't regress."""
    start_time = time.time()

    result = crack_pdf_password(
        "tests/test_pdfs/numbers/100.pdf",
        charset="0123456789",
        min_len=3,
        max_len=3
    )

    duration = time.time() - start_time

    assert isinstance(result, PasswordFound)
    assert duration < 10.0  # Should complete in under 10 seconds
    assert result.rate > 100  # Minimum rate threshold
```

## 🔧 Test Configuration

### Pytest Configuration

The `pyproject.toml` includes pytest configuration:

```toml
[tool.pytest.ini_options]
pythonpath = "src"
markers = [
    "numbers: tests with numbers",
    "letters: tests with letters",
    "special_chars: tests with special characters",
    "mixed: tests with mixed characters",
]
```

### Coverage Configuration

Coverage settings ensure comprehensive testing:

```toml
[tool.coverage.run]
source = ["src/pdf_pycrack"]
omit = ["**/__init__.py"]

[tool.coverage.report]
fail_under = 90
show_missing = true
```

## 📊 Test Execution Strategies

### Development Workflow

During development, use fast tests:

```bash
# Quick validation during coding
uv run pytest -m numbers -x  # Stop on first failure

# Before committing
uv run pytest -m "numbers or letters"

# Before pushing
uv run pytest  # Full suite
```

### CI/CD Strategy

For continuous integration:

```bash
# Parallel execution
uv run pytest -n auto  # Requires pytest-xdist

# With coverage
uv run pytest --cov=src/pdf_pycrack --cov-report=xml

# Generate reports
uv run pytest --junitxml=test-results.xml
```

### Performance Testing

Regular performance validation:

```bash
# Run performance-focused tests
uv run pytest -m "numbers" -k "performance"

# With timing information
uv run pytest --durations=10

# Memory profiling (requires pytest-memray)
uv run pytest --memray
```

## 🐛 Debugging Tests

### Test Debugging Techniques

#### 1. Verbose Output

```bash
# Detailed test output
uv run pytest -v -s

# Show local variables on failure
uv run pytest --tb=long

# Drop into debugger on failure
uv run pytest --pdb
```

#### 2. Isolated Test Execution

```bash
# Run single test
uv run pytest tests/test_core.py::test_specific_function

# Run single test with debugging
uv run pytest tests/test_core.py::test_specific_function -v -s --pdb
```

#### 3. Test Data Inspection

```python
def test_with_debugging():
    """Test with debugging output."""
    result = crack_pdf_password("tests/test_pdfs/numbers/123.pdf")

    # Debug output
    print(f"Result type: {type(result)}")
    print(f"Result data: {result}")

    # Conditional debugging
    if not isinstance(result, PasswordFound):
        import pdb; pdb.set_trace()

    assert isinstance(result, PasswordFound)
```

### Common Test Issues

#### 1. Test File Problems

```bash
# Verify test files exist
ls -la tests/test_pdfs/numbers/

# Check file permissions
file tests/test_pdfs/numbers/123.pdf

# Verify PDF encryption
uv run python -c "
import pikepdf
try:
    pikepdf.open('tests/test_pdfs/numbers/123.pdf')
    print('Not encrypted')
except pikepdf.PasswordError:
    print('Encrypted (correct)')
"
```

#### 2. Environment Issues

```bash
# Check Python path
uv run python -c "import sys; print(sys.path)"

# Verify package installation
uv run python -c "import pdf_pycrack; print(pdf_pycrack.__file__)"

# Test dependencies
uv run python -c "import pikepdf, tqdm, rich; print('All deps OK')"
```

## 📈 Test Metrics

### Coverage Targets

- **Overall coverage**: >90%
- **Core modules**: >95%
- **CLI interface**: >85%
- **Error handling**: 100%

### Performance Targets

- **Fast tests** (`numbers`): <30 seconds total
- **Medium tests** (`letters`): <5 minutes total
- **Slow tests** (`mixed`): <30 minutes total
- **Individual test**: <60 seconds max

### Quality Metrics

```bash
# Generate comprehensive report
uv run pytest \
  --cov=src/pdf_pycrack \
  --cov-report=html \
  --cov-report=term-missing \
  --durations=10 \
  --tb=short
```

## 🚀 Continuous Integration

### GitHub Actions

Example workflow for automated testing:

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.12, 3.13]

    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        curl -LsSf https://astral.sh/uv/install.sh | sh
        uv sync

    - name: Run fast tests
      run: uv run pytest -m "numbers or letters" --cov=src/pdf_pycrack

    - name: Run slow tests
      run: uv run pytest -m "mixed" --maxfail=1
      if: github.event_name == 'push'  # Only on push, not PR
```

## 🎯 Best Practices

### Test Writing

1. **Keep tests focused** - one concept per test
2. **Use descriptive names** - explain what is being tested
3. **Make tests independent** - no shared state
4. **Use appropriate markers** - for selective execution
5. **Include edge cases** - test boundaries and errors

### Test Organization

1. **Group related tests** - in the same file
2. **Use setup/teardown** - for common test data
3. **Parameterize tests** - for multiple similar cases
4. **Document test intent** - with clear docstrings

### Performance Considerations

1. **Start with fast tests** - for quick feedback
2. **Use appropriate test data** - minimal but realistic
3. **Mock external dependencies** - when appropriate
4. **Profile slow tests** - to identify bottlenecks

## 🔮 Future Testing

### Planned Improvements

- **Property-based testing** with Hypothesis
- **Mutation testing** for test quality
- **Performance regression detection**
- **Cross-platform testing** (Windows, macOS, Linux)
- **Memory leak detection**
- **Stress testing** with large files

### Test Data Expansion

- **More diverse passwords** - different languages, patterns
- **Larger test files** - performance testing
- **Corrupted files** - error handling
- **Different PDF versions** - compatibility testing

Ready to write some tests? Check out the existing tests for examples and patterns! 🧪
