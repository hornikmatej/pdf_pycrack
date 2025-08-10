# CLI Interface

This page provides the complete API reference for PDF-PyCrack's command-line interface.

## Command Structure

```bash
pdf-pycrack <pdf_file> [options]
```

## CLI Module

::: pdf_pycrack.cli
    options:
      show_source: true
      show_root_heading: true
      show_root_toc_entry: false
      heading_level: 3

## Main Entry Point

::: pdf_pycrack.main
    options:
      show_source: true
      show_root_heading: true
      show_root_toc_entry: false
      heading_level: 3

## Arguments Reference

### Required Arguments

#### `file`
**Type:** `str`
**Description:** Path to the PDF file to crack.

```bash
pdf-pycrack document.pdf
pdf-pycrack /path/to/file.pdf
pdf-pycrack "file with spaces.pdf"
```

### Optional Arguments

#### `--cores CORES`
**Type:** `int`
**Default:** All available CPU cores
**Description:** Number of CPU cores to use for parallel processing.

```bash
pdf-pycrack file.pdf --cores 4
```

**Validation:**
- Must be positive integer
- Maximum is system CPU count
- Warns if exceeding available cores

#### `--min_len MIN_LEN`
**Type:** `int`
**Default:** `4`
**Description:** Minimum password length to test.

```bash
pdf-pycrack file.pdf --min_len 6
```

**Validation:**
- Must be positive integer
- Must be ≤ `max_len`

#### `--max_len MAX_LEN`
**Type:** `int`
**Default:** `5`
**Description:** Maximum password length to test.

```bash
pdf-pycrack file.pdf --max_len 8
```

**Validation:**
- Must be positive integer
- Must be ≥ `min_len`

#### `--batch_size BATCH_SIZE`
**Type:** `int`
**Default:** `100`
**Description:** Number of passwords each worker tests before reporting progress.

```bash
pdf-pycrack file.pdf --batch_size 500
```

**Validation:**
- Must be positive integer
- Recommended range: 10-1000

#### `--worker_errors`
**Type:** `bool` (flag)
**Default:** `False`
**Description:** Enable detailed error reporting from worker processes.

```bash
pdf-pycrack file.pdf --worker_errors
```

### Character Set Options

#### `--charset-numbers`
**Type:** `bool` (flag)
**Description:** Include numbers (0-9) in the character set.

```bash
pdf-pycrack file.pdf --charset-numbers
```

**Character Set:** `0123456789` (10 characters)

#### `--charset-letters`
**Type:** `bool` (flag)
**Description:** Include letters (a-z, A-Z) in the character set.

```bash
pdf-pycrack file.pdf --charset-letters
```

**Character Set:** `abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ` (52 characters)

#### `--charset-special`
**Type:** `bool` (flag)
**Description:** Include common special characters in the character set.

```bash
pdf-pycrack file.pdf --charset-special
```

**Character Set:** `!@#$%^&*()_+-=[]{}|;:,.<>?` (25 characters)

#### `--charset-custom CHARSET`
**Type:** `str`
**Description:** Provide a custom character set.

```bash
pdf-pycrack file.pdf --charset-custom "abcdef123456"
```

**Validation:**
- Cannot be empty string
- Duplicate characters are allowed but inefficient

## Character Set Combinations

Multiple character set options can be combined:

```bash
# Numbers and letters
pdf-pycrack file.pdf --charset-numbers --charset-letters

# All standard characters
pdf-pycrack file.pdf --charset-numbers --charset-letters --charset-special

# Custom plus numbers
pdf-pycrack file.pdf --charset-custom "abcdef" --charset-numbers
```

## Default Behavior

If no character set options are specified:
- Default charset is numbers only: `0123456789`

## Exit Codes

| Code | Name | Description |
|------|------|-------------|
| `0` | Success | Password found successfully |
| `1` | Not Found | Password not found (all combinations tried) |
| `2` | File Error | File not found, not encrypted, or corrupted |
| `3` | Invalid Arguments | Command-line arguments are invalid |
| `4` | Interrupted | User interrupted with Ctrl+C |
| `5` | System Error | System-related error (memory, permissions) |

## Examples

### Basic Usage

```bash
# Use defaults (4-5 chars, numbers only)
pdf-pycrack document.pdf
```

### Custom Length Range

```bash
# Test 6-8 character passwords
pdf-pycrack document.pdf --min_len 6 --max_len 8
```

### Custom Character Sets

```bash
# Numbers only
pdf-pycrack document.pdf --charset-numbers

# Letters only
pdf-pycrack document.pdf --charset-letters

# Mixed alphanumeric
pdf-pycrack document.pdf --charset-numbers --charset-letters

# Custom characters
pdf-pycrack document.pdf --charset-custom "Password123!"
```

### Performance Tuning

```bash
# Use 6 cores with larger batches
pdf-pycrack document.pdf --cores 6 --batch_size 200

# Enable worker error reporting
pdf-pycrack document.pdf --worker_errors
```

### Complex Example

```bash
# Full-featured command
pdf-pycrack "My Document.pdf" \
  --min_len 6 \
  --max_len 8 \
  --charset-numbers \
  --charset-letters \
  --cores 4 \
  --batch_size 500 \
  --worker_errors
```

## Argument Validation

The CLI performs comprehensive validation:

### File Validation
- Checks if file exists
- Verifies file is readable
- Confirms file is a PDF
- Tests if PDF is encrypted

### Parameter Validation
- Ensures numeric arguments are valid integers
- Checks ranges and constraints
- Validates character set combinations
- Warns about performance implications

### Example Validation Errors

```bash
# Invalid core count
$ pdf-pycrack file.pdf --cores 0
Error: Number of cores must be positive.

# Invalid length range
$ pdf-pycrack file.pdf --min_len 6 --max_len 4
Error: min_len (6) cannot be greater than max_len (4).

# Empty character set
$ pdf-pycrack file.pdf --charset-custom ""
Error: Custom character set cannot be empty.
```

## Integration Examples

### Shell Scripts

```bash
#!/bin/bash
# Progressive cracking script

PDF_FILE="$1"
if [ -z "$PDF_FILE" ]; then
    echo "Usage: $0 <pdf_file>"
    exit 1
fi

# Try different strategies
strategies=(
    "--charset-numbers --min_len 4 --max_len 6"
    "--charset-letters --min_len 4 --max_len 6"
    "--charset-numbers --charset-letters --min_len 4 --max_len 6"
)

for strategy in "${strategies[@]}"; do
    echo "Trying: $strategy"
    if pdf-pycrack "$PDF_FILE" $strategy; then
        echo "Success!"
        exit 0
    fi
done

echo "All strategies failed"
exit 1
```

### Batch Processing

```bash
#!/bin/bash
# Process multiple PDFs

for pdf in *.pdf; do
    echo "Processing $pdf..."
    pdf-pycrack "$pdf" --charset-numbers --min_len 4 --max_len 6 \
        > "${pdf%.pdf}_result.log" 2>&1

    if [ $? -eq 0 ]; then
        echo "✅ $pdf: Success"
    else
        echo "❌ $pdf: Failed"
    fi
done
```

## See Also

- [Core Functions](core.md): Python API reference
- [Models & Types](models.md): Result types and data structures
- [User Guide](../user-guide/cli.md): Detailed CLI usage guide
