# Python Library

PDF-PyCrack provides a powerful Python API that allows you to integrate password cracking functionality directly into your applications. This guide covers everything you need to know about using PDF-PyCrack as a library.

## Basic Usage

### Simple Password Cracking

The most basic usage involves calling the main function with a PDF file path:

```python
from pdf_pycrack import crack_pdf_password

# Basic usage with defaults
result = crack_pdf_password("encrypted_file.pdf")
print(result)
```

### Handling Results

PDF-PyCrack returns different result types depending on the outcome:

```python
from pdf_pycrack import (
    crack_pdf_password,
    PasswordFound,
    PasswordNotFound,
    NotEncrypted,
    FileReadError,
    CrackingInterrupted
)

result = crack_pdf_password("file.pdf")

# Check result type and handle accordingly
if isinstance(result, PasswordFound):
    print(f"Success! Password: {result.password}")
    print(f"Time: {result.duration:.2f} seconds")
    print(f"Attempts: {result.passwords_tested:,}")

elif isinstance(result, PasswordNotFound):
    print("Password not found with current parameters")
    print(f"Total attempts: {result.passwords_tested:,}")
    print(f"Time: {result.duration:.2f} seconds")

elif isinstance(result, NotEncrypted):
    print("File is not encrypted")

elif isinstance(result, FileReadError):
    print(f"Cannot read file: {result.error}")

elif isinstance(result, CrackingInterrupted):
    print("Cracking was interrupted")
```

## Advanced Configuration

### Complete Parameter Control

```python
from pdf_pycrack import crack_pdf_password

result = crack_pdf_password(
    pdf_path="encrypted_document.pdf",
    min_len=6,                    # Minimum password length
    max_len=8,                    # Maximum password length
    charset="0123456789abcdef",   # Custom character set
    num_processes=4,              # Number of CPU cores to use
    batch_size_arg=1000,          # Passwords per batch
    report_worker_errors_arg=True # Enable detailed error reporting
)
```

### Character Set Helpers

While you can provide custom character sets, you might want to use common patterns:

```python
# Define common character sets
NUMBERS = "0123456789"
LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LETTERS = LOWERCASE + UPPERCASE
SPECIAL = "!@#$%^&*()_+-=[]{}|;:,.<>?"
ALL_CHARS = NUMBERS + LETTERS + SPECIAL

# Use combinations
result = crack_pdf_password(
    "file.pdf",
    charset=NUMBERS + LOWERCASE,  # Numbers and lowercase letters
    min_len=4,
    max_len=8
)
```

## Result Types Reference

### PasswordFound

Returned when a password is successfully found:

```python
@dataclass
class PasswordFound:
    password: str              # The discovered password
    passwords_tested: int      # Number of passwords tested
    duration: float           # Time taken in seconds
    rate: float              # Passwords per second
    memory_usage: float      # Peak memory usage in MB
```

**Example usage:**
```python
if isinstance(result, PasswordFound):
    print(f"Password: '{result.password}'")
    print(f"Found after testing {result.passwords_tested:,} passwords")
    print(f"Rate: {result.rate:,.0f} passwords/second")
    print(f"Memory used: {result.memory_usage:.1f} MB")

    # You can now use the password to open the PDF
    import pikepdf
    with pikepdf.open("file.pdf", password=result.password) as pdf:
        # Process the PDF
        pass
```

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

### Error Types

#### NotEncrypted
```python
@dataclass
class NotEncrypted:
    message: str = "PDF is not encrypted"
```

#### FileReadError
```python
@dataclass
class FileReadError:
    error: str                # Description of the file read error
    suggested_action: str     # What the user should do
```

#### CrackingInterrupted
```python
@dataclass
class CrackingInterrupted:
    passwords_tested: int     # Passwords tested before interruption
    duration: float          # Time before interruption
    reason: str             # Why it was interrupted
```

## Practical Examples

### Example 1: Batch Processing

Process multiple PDF files with error handling:

```python
import os
from pathlib import Path
from pdf_pycrack import crack_pdf_password, PasswordFound

def crack_multiple_pdfs(directory: str, charset: str = "0123456789"):
    """Crack passwords for all PDFs in a directory."""
    results = {}

    for pdf_file in Path(directory).glob("*.pdf"):
        print(f"Processing {pdf_file.name}...")

        try:
            result = crack_pdf_password(
                str(pdf_file),
                min_len=4,
                max_len=6,
                charset=charset,
                num_processes=4
            )

            if isinstance(result, PasswordFound):
                results[pdf_file.name] = result.password
                print(f"✅ Found: {result.password}")
            else:
                results[pdf_file.name] = None
                print(f"❌ Not found: {result}")

        except Exception as e:
            print(f"❌ Error processing {pdf_file.name}: {e}")
            results[pdf_file.name] = f"Error: {e}"

    return results

# Usage
results = crack_multiple_pdfs("/path/to/pdf/directory")
for filename, password in results.items():
    print(f"{filename}: {password}")
```

### Example 2: Progressive Search Strategy

Implement a smart search strategy that starts with common patterns:

```python
from pdf_pycrack import crack_pdf_password, PasswordFound

def smart_crack(pdf_path: str):
    """Use a progressive strategy to find passwords efficiently."""

    strategies = [
        # Strategy 1: Common numeric passwords (PINs, years, dates)
        {"charset": "0123456789", "min_len": 4, "max_len": 6},

        # Strategy 2: Simple lowercase words
        {"charset": "abcdefghijklmnopqrstuvwxyz", "min_len": 4, "max_len": 8},

        # Strategy 3: Mixed alphanumeric
        {"charset": "0123456789abcdefghijklmnopqrstuvwxyz", "min_len": 4, "max_len": 6},

        # Strategy 4: Full character set (shorter lengths only)
        {"charset": "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*",
         "min_len": 4, "max_len": 5},
    ]

    for i, strategy in enumerate(strategies, 1):
        print(f"Strategy {i}: {strategy['charset'][:20]}{'...' if len(strategy['charset']) > 20 else ''}")
        print(f"Length range: {strategy['min_len']}-{strategy['max_len']}")

        result = crack_pdf_password(pdf_path, **strategy)

        if isinstance(result, PasswordFound):
            print(f"✅ Success with strategy {i}!")
            return result
        else:
            print(f"❌ Strategy {i} failed: {result}")
            print()

    print("❌ All strategies exhausted")
    return None

# Usage
result = smart_crack("encrypted_file.pdf")
if result:
    print(f"Final result: {result.password}")
```

### Example 3: Integration with GUI

Create a simple progress callback system:

```python
import threading
import time
from pdf_pycrack import crack_pdf_password

class PasswordCracker:
    def __init__(self):
        self.is_running = False
        self.result = None
        self.thread = None

    def start_cracking(self, pdf_path, **kwargs):
        """Start cracking in a separate thread."""
        if self.is_running:
            return False

        self.is_running = True
        self.result = None
        self.thread = threading.Thread(
            target=self._crack_worker,
            args=(pdf_path,),
            kwargs=kwargs
        )
        self.thread.start()
        return True

    def _crack_worker(self, pdf_path, **kwargs):
        """Worker function that runs in separate thread."""
        try:
            self.result = crack_pdf_password(pdf_path, **kwargs)
        except Exception as e:
            self.result = f"Error: {e}"
        finally:
            self.is_running = False

    def is_finished(self):
        """Check if cracking is complete."""
        return not self.is_running

    def get_result(self):
        """Get the result (only call after is_finished() returns True)."""
        return self.result

    def stop(self):
        """Stop the cracking process (note: may take time to respond)."""
        # Note: PDF-PyCrack doesn't currently support stopping mid-process
        # This would require additional implementation
        pass

# Usage in a GUI application
cracker = PasswordCracker()

# Start cracking
cracker.start_cracking(
    "file.pdf",
    min_len=4,
    max_len=6,
    charset="0123456789",
    num_processes=2
)

# Check progress periodically
while not cracker.is_finished():
    print("Still cracking...")
    time.sleep(1)

# Get result
result = cracker.get_result()
print(f"Final result: {result}")
```

### Example 4: Custom Validation

Validate PDFs and handle edge cases:

```python
import os
import pikepdf
from pdf_pycrack import crack_pdf_password, NotEncrypted, FileReadError

def validate_and_crack(pdf_path: str):
    """Validate PDF file before attempting to crack."""

    # Check if file exists
    if not os.path.exists(pdf_path):
        return {"error": "File not found"}

    # Check file size
    file_size = os.path.getsize(pdf_path)
    if file_size == 0:
        return {"error": "File is empty"}

    if file_size > 100 * 1024 * 1024:  # 100MB
        print(f"Warning: Large file ({file_size / 1024 / 1024:.1f} MB)")

    # Try to determine if file is encrypted
    try:
        with pikepdf.open(pdf_path) as pdf:
            return {"error": "File is not encrypted"}
    except pikepdf.PasswordError:
        # Good - file is encrypted
        pass
    except Exception as e:
        return {"error": f"Cannot read PDF: {e}"}

    # Proceed with cracking
    print("File validated - starting crack attempt")
    result = crack_pdf_password(pdf_path)

    return {"result": result}

# Usage
validation_result = validate_and_crack("test.pdf")
if "error" in validation_result:
    print(f"Validation failed: {validation_result['error']}")
else:
    print(f"Crack result: {validation_result['result']}")
```

## Performance Considerations

### Memory Usage

Monitor memory usage for large-scale operations:

```python
import psutil
import os
from pdf_pycrack import crack_pdf_password

def crack_with_monitoring(pdf_path: str, **kwargs):
    """Crack password while monitoring system resources."""

    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB

    print(f"Initial memory: {initial_memory:.1f} MB")
    print(f"Available CPU cores: {psutil.cpu_count()}")
    print(f"Available memory: {psutil.virtual_memory().available / 1024 / 1024:.1f} MB")

    result = crack_pdf_password(pdf_path, **kwargs)

    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_delta = final_memory - initial_memory

    print(f"Final memory: {final_memory:.1f} MB")
    print(f"Memory increase: {memory_delta:.1f} MB")

    return result
```

### Optimal Process Count

Determine the optimal number of processes for your system:

```python
import multiprocessing
import time
from pdf_pycrack import crack_pdf_password

def benchmark_process_counts(pdf_path: str, max_processes: int = None):
    """Test different process counts to find optimal performance."""

    if max_processes is None:
        max_processes = multiprocessing.cpu_count()

    results = {}
    test_params = {
        "min_len": 4,
        "max_len": 5,
        "charset": "0123456789",
        "batch_size_arg": 1000
    }

    for proc_count in range(1, max_processes + 1):
        print(f"Testing with {proc_count} processes...")

        start_time = time.time()
        result = crack_pdf_password(
            pdf_path,
            num_processes=proc_count,
            **test_params
        )
        duration = time.time() - start_time

        results[proc_count] = {
            "duration": duration,
            "result": result,
            "rate": getattr(result, "rate", 0)
        }

        print(f"  Duration: {duration:.2f}s, Rate: {results[proc_count]['rate']:.0f} pwd/s")

    # Find optimal process count
    best_count = max(results.keys(), key=lambda k: results[k]["rate"])
    print(f"\nOptimal process count: {best_count}")
    print(f"Best rate: {results[best_count]['rate']:.0f} passwords/second")

    return results
```

## Error Handling Best Practices

### Comprehensive Error Handling

```python
from pdf_pycrack import crack_pdf_password, PasswordFound
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def robust_crack(pdf_path: str, **kwargs):
    """Crack PDF with comprehensive error handling."""

    try:
        logger.info(f"Starting crack attempt on {pdf_path}")

        result = crack_pdf_password(pdf_path, **kwargs)

        if isinstance(result, PasswordFound):
            logger.info(f"SUCCESS: Password found - {result.password}")
            return {"success": True, "password": result.password}
        else:
            logger.warning(f"FAILED: {type(result).__name__} - {result}")
            return {"success": False, "reason": str(result)}

    except KeyboardInterrupt:
        logger.info("User interrupted the process")
        return {"success": False, "reason": "Interrupted by user"}

    except MemoryError:
        logger.error("Out of memory - try reducing batch size or process count")
        return {"success": False, "reason": "Insufficient memory"}

    except PermissionError:
        logger.error(f"Permission denied accessing {pdf_path}")
        return {"success": False, "reason": "Permission denied"}

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return {"success": False, "reason": f"Unexpected error: {e}"}

# Usage
result = robust_crack("file.pdf", min_len=4, max_len=6)
if result["success"]:
    print(f"Password: {result['password']}")
else:
    print(f"Failed: {result['reason']}")
```

## Next Steps

Now that you understand the Python library:

- 📊 **[Performance Guide](../performance/optimization.md)**: Optimize for maximum speed
- 🔧 **[Configuration](configuration.md)**: Advanced configuration options
- 📖 **[API Reference](../api/core.md)**: Detailed API documentation
- 🛠️ **[Error Handling](error-handling.md)**: Handle all error scenarios
