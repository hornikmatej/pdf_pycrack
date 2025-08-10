# Models & Types

This page documents the data structures and result types used throughout PDF-PyCrack.

## Result Types

All cracking operations return one of these result types:

::: pdf_pycrack.models.cracking_result
    options:
      show_source: true
      show_root_heading: true
      show_root_toc_entry: false
      heading_level: 3

## Success Results

### PasswordFound

Returned when a password is successfully discovered:

```python
@dataclass
class PasswordFound:
    password: str              # The discovered password
    passwords_tested: int      # Number of passwords tested
    duration: float           # Time taken in seconds
    rate: float              # Passwords per second
    memory_usage: float      # Peak memory usage in MB
```

**Example:**
```python
if isinstance(result, PasswordFound):
    print(f"Password: '{result.password}'")
    print(f"Found after testing {result.passwords_tested:,} passwords")
    print(f"Rate: {result.rate:,.0f} passwords/second")
    print(f"Duration: {result.duration:.2f} seconds")
```

## Failure Results

### PasswordNotFound

Returned when all possible combinations have been exhausted:

```python
@dataclass
class PasswordNotFound:
    passwords_tested: int      # Total passwords tested
    duration: float           # Time taken in seconds
    rate: float              # Average passwords per second
    memory_usage: float      # Peak memory usage in MB
```

### NotEncrypted

Returned when the PDF file is not encrypted:

```python
@dataclass
class NotEncrypted:
    message: str = "PDF is not encrypted"
```

### FileReadError

Returned when there's an issue reading the PDF file:

```python
@dataclass
class FileReadError:
    error: str                # Description of the error
    suggested_action: str     # What the user should do
```

**Common errors:**
- File not found
- Permission denied
- Corrupted PDF file
- Invalid PDF format

### CrackingInterrupted

Returned when the cracking process is interrupted:

```python
@dataclass
class CrackingInterrupted:
    passwords_tested: int     # Passwords tested before interruption
    duration: float          # Time before interruption
    reason: str             # Why it was interrupted
```

## Error Types

### InitializationError

Raised when there's an error during initialization:

```python
@dataclass
class InitializationError:
    error: str                # Description of the initialization error
    suggested_action: str     # What the user should do
```

### PDFCorruptedError

Raised when the PDF file is corrupted or invalid:

```python
@dataclass
class PDFCorruptedError:
    error: str                # Description of the corruption
    suggested_action: str     # What the user should do
```

## Type Checking

Use `isinstance()` to check result types:

```python
from pdf_pycrack import crack_pdf_password, PasswordFound, PasswordNotFound

result = crack_pdf_password("file.pdf")

# Type checking
if isinstance(result, PasswordFound):
    # Handle success
    use_password(result.password)
elif isinstance(result, PasswordNotFound):
    # Handle failure
    try_different_parameters()
else:
    # Handle errors
    print(f"Error: {result}")
```

## Union Types

For type hints, you can use:

```python
from typing import Union
from pdf_pycrack import CrackResult

def process_result(result: CrackResult) -> None:
    """Process a cracking result."""
    if isinstance(result, PasswordFound):
        print(f"Success: {result.password}")
    # ... handle other types
```

## Performance Metrics

All result types that include performance data have these fields:

| Field | Type | Description |
|-------|------|-------------|
| `passwords_tested` | `int` | Number of passwords attempted |
| `duration` | `float` | Total time in seconds |
| `rate` | `float` | Passwords per second |
| `memory_usage` | `float` | Peak memory usage in MB |

## Best Practices

### Error Handling

Always check the result type before accessing specific fields:

```python
result = crack_pdf_password("file.pdf")

# ✅ Good - check type first
if isinstance(result, PasswordFound):
    print(result.password)
elif isinstance(result, FileReadError):
    print(f"Error: {result.error}")

# ❌ Bad - assumes success
print(result.password)  # AttributeError if not PasswordFound
```

### Logging Results

```python
import logging

def log_result(result: CrackResult) -> None:
    """Log the cracking result appropriately."""

    if isinstance(result, PasswordFound):
        logging.info(f"Password found: {result.password} "
                    f"({result.passwords_tested:,} attempts in {result.duration:.2f}s)")

    elif isinstance(result, PasswordNotFound):
        logging.warning(f"Password not found after {result.passwords_tested:,} attempts "
                       f"in {result.duration:.2f}s")

    elif isinstance(result, FileReadError):
        logging.error(f"File error: {result.error}")

    else:
        logging.error(f"Unexpected result: {result}")
```

## See Also

- [Core Functions](core.md): Main API functions
- [CLI Interface](cli.md): Command-line usage
- [User Guide](../user-guide/library.md): Practical usage examples
