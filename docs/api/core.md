# Core Functions

This page documents the main functions and classes in the PDF-PyCrack core module.

## Main Function

::: pdf_pycrack.core.crack_pdf_password

## Core Modules

### PDF Validation

::: pdf_pycrack.validator

### Worker Management

::: pdf_pycrack.supervisor

### Password Generation

::: pdf_pycrack.password_generator

### Worker Processes

::: pdf_pycrack.worker

## Usage Examples

### Basic Usage

```python
from pdf_pycrack import crack_pdf_password

# Simple usage with defaults
result = crack_pdf_password("encrypted.pdf")
print(result)
```

### Advanced Configuration

```python
from pdf_pycrack import crack_pdf_password

# Custom configuration
result = crack_pdf_password(
    pdf_path="document.pdf",
    min_len=6,
    max_len=8,
    charset="0123456789abcdef",
    num_processes=4,
    batch_size_arg=1000,
    report_worker_errors_arg=True
)
```

### Error Handling

```python
from pdf_pycrack import (
    crack_pdf_password,
    PasswordFound,
    PasswordNotFound,
    FileReadError,
    NotEncrypted
)

result = crack_pdf_password("file.pdf")

if isinstance(result, PasswordFound):
    print(f"Success! Password: {result.password}")
elif isinstance(result, PasswordNotFound):
    print("Password not found with current parameters")
elif isinstance(result, FileReadError):
    print(f"File error: {result.error}")
elif isinstance(result, NotEncrypted):
    print("PDF is not encrypted")
```

## Performance Considerations

- **Process Count**: Optimal number is usually CPU cores - 1
- **Batch Size**: Larger batches reduce overhead but less responsive progress
- **Character Set**: Smaller character sets are exponentially faster
- **Length Range**: Each additional character dramatically increases time

## See Also

- [Models & Types](models.md): Data structures and result types
- [CLI Interface](cli.md): Command-line interface documentation
- [User Guide](../user-guide/library.md): Detailed usage guide
