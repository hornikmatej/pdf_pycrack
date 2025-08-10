# Error Handling

PDF-PyCrack provides comprehensive error handling with clear messages and suggested actions. This guide covers all error scenarios you might encounter and how to handle them effectively.

## Understanding Error Types

PDF-PyCrack uses a structured approach to error handling with specific result types for different error conditions.

## Common Error Scenarios

### File-Related Errors

#### File Not Found

**Scenario:** The specified PDF file doesn't exist.

```bash
$ pdf-pycrack nonexistent.pdf
❌ Error: File not found: nonexistent.pdf
💡 Suggestion: Check the file path and ensure the file exists
```

**Python API:**
```python
from pdf_pycrack import crack_pdf_password, FileReadError

result = crack_pdf_password("nonexistent.pdf")
if isinstance(result, FileReadError):
    print(f"Error: {result.error}")
    print(f"Suggestion: {result.suggested_action}")
```

**Solutions:**
- Check the file path for typos
- Use absolute paths to avoid confusion
- Verify the file exists with `ls` or `dir`

#### Permission Denied

**Scenario:** You don't have permission to read the PDF file.

```bash
$ pdf-pycrack protected_file.pdf
❌ Error: Permission denied: protected_file.pdf
💡 Suggestion: Check file permissions or run with appropriate privileges
```

**Solutions:**
```bash
# Check permissions
ls -la protected_file.pdf

# Fix permissions (Linux/macOS)
chmod 644 protected_file.pdf

# Run with sudo (if necessary)
sudo pdf-pycrack protected_file.pdf
```

#### Directory Instead of File

**Scenario:** You specified a directory instead of a file.

```bash
$ pdf-pycrack my_folder/
❌ Error: Is a directory: my_folder/
💡 Suggestion: Specify a PDF file, not a directory
```

**Solutions:**
- Specify the actual PDF file: `pdf-pycrack my_folder/document.pdf`
- List directory contents to find the file: `ls my_folder/`

### PDF-Related Errors

#### File Not Encrypted

**Scenario:** The PDF file is not password-protected.

```bash
$ pdf-pycrack unencrypted.pdf
ℹ️  PDF is not encrypted
```

**Python API:**
```python
from pdf_pycrack import crack_pdf_password, NotEncrypted

result = crack_pdf_password("unencrypted.pdf")
if isinstance(result, NotEncrypted):
    print("This PDF doesn't need a password")
```

**Solutions:**
- Verify the file is actually encrypted
- Use a different PDF file
- Check if the file was already decrypted

#### Corrupted PDF

**Scenario:** The PDF file is corrupted or invalid.

```bash
$ pdf-pycrack corrupted.pdf
❌ Error: Invalid or corrupted PDF file
💡 Suggestion: Verify the file is a valid PDF and not corrupted
```

**Solutions:**
- Try opening the file in a PDF viewer
- Re-download the file if possible
- Use PDF repair tools if necessary

#### Unsupported Encryption

**Scenario:** The PDF uses an encryption method not supported.

```bash
$ pdf-pycrack modern_encrypted.pdf
❌ Error: Unsupported encryption method
💡 Suggestion: This PDF uses encryption not yet supported by PDF-PyCrack
```

**Solutions:**
- Check if there's an updated version of PDF-PyCrack
- Try alternative tools for newer encryption methods
- Report the issue if it's a common encryption type

### Parameter Validation Errors

#### Invalid Length Range

**Scenario:** Minimum length is greater than maximum length.

```bash
$ pdf-pycrack file.pdf --min-len 8 --max-len 4
❌ Error: min_len (8) cannot be greater than max_len (4)
💡 Suggestion: Ensure min_len ≤ max_len
```

**Solutions:**
```bash
# Correct the range
pdf-pycrack file.pdf --min-len 4 --max-len 8
```

#### Invalid Core Count

**Scenario:** Specified more cores than available.

```bash
$ pdf-pycrack file.pdf --cores 32  # On 8-core system
⚠️  Warning: Requested 32 cores but only 8 available. Using 8 cores.
```

**Solutions:**
```bash
# Check available cores
nproc  # Linux
sysctl -n hw.ncpu  # macOS

# Use appropriate count
pdf-pycrack file.pdf --cores 8
```

#### Empty Character Set

**Scenario:** No character set specified or empty custom set.

```bash
$ pdf-pycrack file.pdf --charset-custom ""
❌ Error: Character set cannot be empty
💡 Suggestion: Provide a non-empty character set or use preset options
```

**Solutions:**
```bash
# Use preset character sets
pdf-pycrack file.pdf --charset-numbers

# Or provide custom characters
pdf-pycrack file.pdf --charset-custom "abc123"
```

### Runtime Errors

#### Memory Exhaustion

**Scenario:** System runs out of memory during cracking.

```bash
$ pdf-pycrack file.pdf --max-len 12 --charset-numbers --charset-letters --charset-special
❌ Error: Insufficient memory to continue operation
💡 Suggestion: Reduce search space or increase available memory
```

**Python handling:**
```python
import psutil

def check_memory_before_crack():
    """Check available memory before starting."""
    available_gb = psutil.virtual_memory().available / (1024**3)

    if available_gb < 2:
        print(f"Warning: Only {available_gb:.1f}GB memory available")
        print("Consider reducing batch size or process count")
        return False
    return True

if check_memory_before_crack():
    result = crack_pdf_password("file.pdf")
```

**Solutions:**
- Reduce search space: shorter lengths or smaller character sets
- Reduce process count: `--cores 2`
- Reduce batch size: `--batch-size 50`
- Close other applications to free memory

#### Process Spawn Failure

**Scenario:** Unable to create worker processes.

```bash
$ pdf-pycrack file.pdf --cores 16
❌ Error: Failed to spawn worker processes
💡 Suggestion: Reduce the number of processes or check system limits
```

**Solutions:**
```bash
# Check system limits
ulimit -u  # Max user processes

# Reduce process count
pdf-pycrack file.pdf --cores 4

# Or use single process for debugging
pdf-pycrack file.pdf --cores 1 --worker-errors
```

#### Worker Process Crash

**Scenario:** One or more worker processes crash during execution.

```bash
$ pdf-pycrack file.pdf --worker-errors
⚠️  Warning: Worker process 3 crashed, continuing with remaining workers
🔍 Worker error: Segmentation fault in password validation
```

**Solutions:**
- Enable worker error reporting: `--worker-errors`
- Reduce process count to isolate the issue
- Report the crash with details if it's reproducible

## Error Handling in Python API

### Comprehensive Error Handling

```python
from pdf_pycrack import (
    crack_pdf_password,
    PasswordFound,
    PasswordNotFound,
    NotEncrypted,
    FileReadError,
    CrackingInterrupted,
    InitializationError
)
import logging

def robust_crack_attempt(pdf_path: str, **kwargs):
    """Crack PDF with comprehensive error handling."""

    try:
        result = crack_pdf_password(pdf_path, **kwargs)

        if isinstance(result, PasswordFound):
            logging.info(f"Success! Password: {result.password}")
            return {"success": True, "password": result.password}

        elif isinstance(result, PasswordNotFound):
            logging.warning(f"Password not found after {result.passwords_tested:,} attempts")
            return {"success": False, "reason": "password_not_found"}

        elif isinstance(result, NotEncrypted):
            logging.info("PDF is not encrypted")
            return {"success": False, "reason": "not_encrypted"}

        elif isinstance(result, FileReadError):
            logging.error(f"File error: {result.error}")
            return {"success": False, "reason": "file_error", "details": result.error}

        elif isinstance(result, CrackingInterrupted):
            logging.warning("Cracking was interrupted")
            return {"success": False, "reason": "interrupted"}

        else:
            logging.error(f"Unexpected result type: {type(result)}")
            return {"success": False, "reason": "unknown_error"}

    except KeyboardInterrupt:
        logging.info("User interrupted the process")
        return {"success": False, "reason": "user_interrupt"}

    except MemoryError:
        logging.error("Out of memory - reduce search space")
        return {"success": False, "reason": "memory_error"}

    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
        return {"success": False, "reason": "permission_error"}

    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return {"success": False, "reason": "unexpected_error", "details": str(e)}

# Usage
result = robust_crack_attempt("document.pdf", min_len=4, max_len=6)
if result["success"]:
    print(f"Password found: {result['password']}")
else:
    print(f"Failed: {result['reason']}")
```

### Retry Logic

```python
import time
from typing import Dict, Any

def crack_with_retry(pdf_path: str, max_retries: int = 3, **kwargs) -> Dict[str, Any]:
    """Attempt cracking with retry logic for transient failures."""

    for attempt in range(max_retries):
        try:
            result = crack_pdf_password(pdf_path, **kwargs)

            # Success or definitive failure - don't retry
            if isinstance(result, (PasswordFound, PasswordNotFound, NotEncrypted, FileReadError)):
                return {"success": isinstance(result, PasswordFound), "result": result}

            # Transient failure - retry with backoff
            if isinstance(result, (CrackingInterrupted, InitializationError)):
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logging.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue

        except MemoryError:
            # Reduce load and retry
            if attempt < max_retries - 1:
                kwargs["num_processes"] = max(1, kwargs.get("num_processes", 4) // 2)
                kwargs["batch_size_arg"] = max(10, kwargs.get("batch_size_arg", 100) // 2)
                logging.warning(f"Memory error, reducing load and retrying...")
                continue

        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt == max_retries - 1:
                raise

    return {"success": False, "reason": "max_retries_exceeded"}
```

### Validation Before Cracking

```python
import os
import pikepdf
from pathlib import Path

def validate_inputs(pdf_path: str, **kwargs) -> Dict[str, str]:
    """Validate inputs before attempting to crack."""

    errors = []

    # File validation
    if not os.path.exists(pdf_path):
        errors.append(f"File not found: {pdf_path}")
    elif not os.path.isfile(pdf_path):
        errors.append(f"Path is not a file: {pdf_path}")
    elif not os.access(pdf_path, os.R_OK):
        errors.append(f"Cannot read file: {pdf_path}")
    elif Path(pdf_path).suffix.lower() != '.pdf':
        errors.append(f"File does not appear to be a PDF: {pdf_path}")

    # PDF validation
    if not errors:
        try:
            with pikepdf.open(pdf_path) as pdf:
                errors.append("PDF is not encrypted")
        except pikepdf.PasswordError:
            pass  # Good - file is encrypted
        except Exception as e:
            errors.append(f"Cannot read PDF: {e}")

    # Parameter validation
    min_len = kwargs.get("min_len", 4)
    max_len = kwargs.get("max_len", 5)
    if min_len > max_len:
        errors.append(f"min_len ({min_len}) > max_len ({max_len})")

    num_processes = kwargs.get("num_processes")
    if num_processes and num_processes > os.cpu_count():
        errors.append(f"Requested {num_processes} processes but only {os.cpu_count()} cores available")

    charset = kwargs.get("charset", "")
    if charset and len(charset) == 0:
        errors.append("Empty character set provided")

    return errors

def safe_crack_attempt(pdf_path: str, **kwargs):
    """Validate inputs before cracking."""

    errors = validate_inputs(pdf_path, **kwargs)
    if errors:
        return {
            "success": False,
            "reason": "validation_failed",
            "errors": errors
        }

    return robust_crack_attempt(pdf_path, **kwargs)
```

## Debugging Techniques

### Enable Verbose Logging

```python
import logging

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Enable worker error reporting
result = crack_pdf_password(
    "file.pdf",
    report_worker_errors_arg=True  # Show worker errors
)
```

### CLI Debugging

```bash
# Enable worker error reporting
pdf-pycrack file.pdf --worker-errors

# Use minimal settings for debugging
pdf-pycrack file.pdf --cores 1 --batch-size 10 --worker-errors

# Test with known good file
pdf-pycrack tests/test_pdfs/numbers/123.pdf --charset-custom "123" --min-len 3 --max-len 3
```

### System Resource Monitoring

```python
import psutil
import threading
import time

class ResourceMonitor:
    def __init__(self):
        self.monitoring = False
        self.stats = {"max_memory": 0, "max_cpu": 0}

    def start(self):
        self.monitoring = True
        self.thread = threading.Thread(target=self._monitor)
        self.thread.start()

    def stop(self):
        self.monitoring = False
        self.thread.join()
        return self.stats

    def _monitor(self):
        while self.monitoring:
            memory = psutil.virtual_memory().percent
            cpu = psutil.cpu_percent()

            self.stats["max_memory"] = max(self.stats["max_memory"], memory)
            self.stats["max_cpu"] = max(self.stats["max_cpu"], cpu)

            time.sleep(1)

# Usage
monitor = ResourceMonitor()
monitor.start()

try:
    result = crack_pdf_password("file.pdf")
finally:
    stats = monitor.stop()
    print(f"Peak memory: {stats['max_memory']:.1f}%")
    print(f"Peak CPU: {stats['max_cpu']:.1f}%")
```

## Best Practices

### 🛡️ Defensive Programming

1. **Always check result types** before accessing attributes
2. **Validate inputs** before processing
3. **Handle exceptions** gracefully
4. **Provide meaningful error messages** to users
5. **Log errors** for debugging

### 📊 Error Monitoring

1. **Track error patterns** to identify common issues
2. **Monitor system resources** during operation
3. **Use appropriate logging levels** for different scenarios
4. **Document known issues** and workarounds

### 🔄 Recovery Strategies

1. **Implement retry logic** for transient failures
2. **Graceful degradation** when resources are limited
3. **Fallback options** for unsupported features
4. **Clean resource cleanup** on errors

## Getting Help

### When to Report Issues

Report bugs when you encounter:
- **Crashes or segmentation faults**
- **Unexpected error messages**
- **Performance degradation**
- **Memory leaks**
- **Inconsistent behavior**

### What to Include in Bug Reports

1. **Complete error message** and stack trace
2. **Steps to reproduce** the issue
3. **System information** (OS, Python version, hardware)
4. **PDF file details** (if safe to share)
5. **Command or code** that triggered the error

### Community Resources

- **GitHub Issues:** Report bugs and request features
- **Discussions:** Ask questions and share experiences
- **Documentation:** Check guides and examples
- **Stack Overflow:** Community Q&A (tag: pdf-pycrack)

Remember: Good error handling makes the difference between a frustrating experience and a helpful tool! 🛡️
