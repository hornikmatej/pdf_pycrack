# Command Line Interface

This guide provides comprehensive documentation for PDF-PyCrack's command-line interface (CLI). The CLI is designed to be intuitive while offering powerful customization options for different password cracking scenarios.

## Basic Syntax

```bash
pdf-pycrack <pdf_file> [options]
```

## Required Arguments

### `file`
**Path to the PDF file to crack.**

```bash
pdf-pycrack document.pdf
pdf-pycrack /path/to/encrypted/file.pdf
pdf-pycrack "file with spaces.pdf"
```

The file path can be:
- Relative: `document.pdf`, `./pdfs/file.pdf`
- Absolute: `/home/user/documents/file.pdf`
- Contains spaces: Use quotes `"my document.pdf"`

## Optional Arguments

### Core Options

#### `--cores CORES`
**Number of CPU cores to use for parallel processing.**

```bash
# Use all available cores (default)
pdf-pycrack file.pdf

# Use specific number of cores
pdf-pycrack file.pdf --cores 4

# Use most cores but leave some for system
pdf-pycrack file.pdf --cores 6  # on 8-core system
```

- **Default**: All available CPU cores
- **Range**: 1 to system maximum
- **Recommendation**: Use `N-1` or `N-2` cores to leave resources for the system

#### `--min_len MIN_LEN`
**Minimum password length to test.**

```bash
# Start with 6-character passwords
pdf-pycrack file.pdf --min_len 6

# Test very short passwords (1-3 characters)
pdf-pycrack file.pdf --min_len 1 --max_len 3
```

- **Default**: 4
- **Range**: 1 to 50 (practical limit)
- **Strategy**: Start with shorter lengths for faster results

#### `--max_len MAX_LEN`
**Maximum password length to test.**

```bash
# Test up to 8-character passwords
pdf-pycrack file.pdf --max_len 8

# Test only specific length (6 characters)
pdf-pycrack file.pdf --min_len 6 --max_len 6
```

- **Default**: 5
- **Range**: `min_len` to 50
- **Warning**: Each additional character dramatically increases cracking time

#### `--batch_size BATCH_SIZE`
**Number of passwords each worker tests before reporting progress.**

```bash
# Smaller batches for more frequent updates
pdf-pycrack file.pdf --batch_size 50

# Larger batches for slightly better performance
pdf-pycrack file.pdf --batch_size 500
```

- **Default**: 100
- **Range**: 1 to 10,000
- **Trade-off**: Smaller = more updates, larger = slightly faster

### Character Set Options

Control which characters are included in password generation:

#### `--charset-numbers`
**Include numbers (0-9) in the character set.**

```bash
pdf-pycrack file.pdf --charset-numbers
```

Character set: `0123456789` (10 characters)

#### `--charset-letters`
**Include letters (a-z, A-Z) in the character set.**

```bash
pdf-pycrack file.pdf --charset-letters
```

Character set: `abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ` (52 characters)

#### `--charset-special`
**Include common special characters in the character set.**

```bash
pdf-pycrack file.pdf --charset-special
```

Character set: `!@#$%^&*()_+-=[]{}|;:,.<>?` (25 characters)

#### `--charset-custom CHARSET`
**Provide a custom character set.**

```bash
# Only specific characters
pdf-pycrack file.pdf --charset-custom "abcdef123456"

# Include spaces (use quotes)
pdf-pycrack file.pdf --charset-custom "hello world 123"

# Escape special characters if needed
pdf-pycrack file.pdf --charset-custom "abc\"def'123"
```

#### Character Set Combinations

You can combine multiple character set options:

```bash
# Numbers and letters
pdf-pycrack file.pdf --charset-numbers --charset-letters

# All standard characters
pdf-pycrack file.pdf --charset-numbers --charset-letters --charset-special

# Custom set plus numbers
pdf-pycrack file.pdf --charset-custom "abcdef" --charset-numbers
```

### Advanced Options

#### `--worker_errors`
**Enable detailed error reporting from worker processes.**

```bash
pdf-pycrack file.pdf --worker_errors
```

- **Default**: Disabled
- **Use case**: Debugging issues or understanding failures
- **Impact**: May slightly reduce performance

## Character Set Reference

### Default Behavior

If no character set options are specified, PDF-PyCrack uses numbers by default:

```bash
# These are equivalent
pdf-pycrack file.pdf
pdf-pycrack file.pdf --charset-numbers
```

### Available Character Sets

| Option | Characters | Count | Use Case |
|--------|------------|-------|----------|
| `--charset-numbers` | `0123456789` | 10 | PINs, years, dates |
| `--charset-letters` | `a-z, A-Z` | 52 | Words, names |
| `--charset-special` | `!@#$%^&*()_+-=[]{}|;:,.<>?` | 25 | Complex passwords |
| `--charset-custom` | User-defined | Variable | Specific patterns |

### Character Set Size Impact

The number of possible passwords grows exponentially with character set size:

| Length | Numbers (10) | Letters (52) | All (87) |
|--------|--------------|--------------|----------|
| 4 | 10,000 | 7.3M | 57.3M |
| 5 | 100,000 | 380M | 4.98B |
| 6 | 1,000,000 | 19.8B | 433B |

## Usage Examples

### Quick Numeric Passwords

```bash
# Test common numeric patterns
pdf-pycrack file.pdf --charset-numbers --min_len 4 --max_len 8
```

**Good for**: Birth years, dates, PINs, simple numeric passwords

### Dictionary Words

```bash
# Test alphabetic passwords
pdf-pycrack file.pdf --charset-letters --min_len 5 --max_len 10
```

**Good for**: Names, dictionary words, simple text passwords

### Alphanumeric Passwords

```bash
# Test mixed alphanumeric
pdf-pycrack file.pdf --charset-numbers --charset-letters --min_len 6 --max_len 8
```

**Good for**: Standard passwords with letters and numbers

### Complex Passwords

```bash
# Test with all character types
pdf-pycrack file.pdf --charset-numbers --charset-letters --charset-special --min_len 4 --max_len 6
```

**Good for**: Strong passwords (warning: can take very long)

### Custom Patterns

```bash
# Test specific pattern (e.g., you know it contains only these chars)
pdf-pycrack file.pdf --charset-custom "Password123!" --min_len 8 --max_len 12
```

### Performance-Optimized

```bash
# Balanced performance on 8-core system
pdf-pycrack file.pdf --cores 6 --batch_size 200 --charset-numbers --charset-letters --max_len 6
```

## Exit Codes

PDF-PyCrack returns different exit codes to indicate the result:

| Code | Meaning | Description |
|------|---------|-------------|
| 0 | Success | Password found |
| 1 | Not found | All combinations tested, no password found |
| 2 | File error | File not found, not encrypted, or corrupted |
| 3 | Invalid arguments | Command-line arguments are invalid |
| 4 | Interrupted | User interrupted with Ctrl+C |
| 5 | System error | System-related error (memory, permissions) |

### Using Exit Codes in Scripts

```bash
#!/bin/bash

pdf-pycrack document.pdf --charset-numbers --min_len 4 --max_len 6

case $? in
    0)
        echo "Password found successfully!"
        ;;
    1)
        echo "Password not found. Try different parameters."
        ;;
    2)
        echo "File error. Check file path and encryption status."
        ;;
    3)
        echo "Invalid arguments. Check command syntax."
        ;;
    4)
        echo "Process interrupted by user."
        ;;
    5)
        echo "System error. Check resources and permissions."
        ;;
    *)
        echo "Unknown error occurred."
        ;;
esac
```

## Tips and Best Practices

### 🎯 Start Smart

1. **Begin with specific character sets**:
   ```bash
   # Try numbers first (fastest)
   pdf-pycrack file.pdf --charset-numbers

   # Then letters if numbers fail
   pdf-pycrack file.pdf --charset-letters
   ```

2. **Use shorter lengths initially**:
   ```bash
   # Quick check for short passwords
   pdf-pycrack file.pdf --min_len 1 --max_len 4
   ```

### ⚡ Optimize Performance

1. **Use appropriate core count**:
   ```bash
   # Leave 1-2 cores for system on desktop
   pdf-pycrack file.pdf --cores $(($(nproc) - 2))
   ```

2. **Adjust batch size for your system**:
   ```bash
   # Larger batches on high-performance systems
   pdf-pycrack file.pdf --batch_size 500
   ```

### 🧠 Think Strategically

1. **Consider the context**:
   - Personal files: names, dates, simple words
   - Corporate files: policy-compliant passwords
   - Old files: simpler passwords were common

2. **Use character set intelligence**:
   ```bash
   # If you suspect it's a year
   pdf-pycrack file.pdf --charset-numbers --min_len 4 --max_len 4

   # If you think it's a name + number
   pdf-pycrack file.pdf --charset-numbers --charset-letters --min_len 5 --max_len 10
   ```

### ⏰ Manage Time Expectations

1. **Estimate before starting**:
   - 4-digit numbers: seconds
   - 6-digit numbers: seconds to minutes
   - 6-char mixed: minutes to hours
   - 8-char full: hours to days

2. **Use progressive strategy**:
   ```bash
   # Start narrow and expand
   pdf-pycrack file.pdf --charset-numbers --max_len 6
   # If fails, expand:
   pdf-pycrack file.pdf --charset-numbers --charset-letters --max_len 6
   ```

## Troubleshooting

### Common Issues

#### "No password found"
```bash
# Try expanding search space
pdf-pycrack file.pdf --min_len 1 --max_len 8 --charset-numbers --charset-letters
```

#### "File not found"
```bash
# Check file path
ls -la "your_file.pdf"
pdf-pycrack "$(pwd)/your_file.pdf"
```

#### "Permission denied"
```bash
# Check file permissions
chmod 644 your_file.pdf
```

#### Very slow performance
```bash
# Reduce search space
pdf-pycrack file.pdf --charset-numbers --max_len 6 --cores 4
```

### Getting Help

```bash
# Show all options
pdf-pycrack --help

# Check version
pdf-pycrack --version  # (if available)
```

## Integration Examples

### Shell Scripts

```bash
#!/bin/bash
# crack_pdf.sh - Progressive PDF cracking script

PDF_FILE="$1"
if [ -z "$PDF_FILE" ]; then
    echo "Usage: $0 <pdf_file>"
    exit 1
fi

echo "Starting progressive crack on $PDF_FILE"

# Strategy 1: Numbers only
echo "Trying numeric passwords..."
if pdf-pycrack "$PDF_FILE" --charset-numbers --min_len 4 --max_len 8; then
    exit 0
fi

# Strategy 2: Letters only
echo "Trying alphabetic passwords..."
if pdf-pycrack "$PDF_FILE" --charset-letters --min_len 4 --max_len 8; then
    exit 0
fi

# Strategy 3: Mixed alphanumeric
echo "Trying alphanumeric passwords..."
if pdf-pycrack "$PDF_FILE" --charset-numbers --charset-letters --min_len 4 --max_len 6; then
    exit 0
fi

echo "All strategies failed"
exit 1
```

### Batch Processing

```bash
#!/bin/bash
# batch_crack.sh - Process multiple PDFs

for pdf in *.pdf; do
    echo "Processing $pdf..."
    if pdf-pycrack "$pdf" --charset-numbers --min_len 4 --max_len 6 > "${pdf%.pdf}_result.txt" 2>&1; then
        echo "✅ $pdf: Password found"
    else
        echo "❌ $pdf: Failed"
    fi
done
```

## Next Steps

- 🐍 **[Python Library](library.md)**: Use PDF-PyCrack programmatically
- ⚙️ **[Configuration](configuration.md)**: Advanced configuration options
- 📊 **[Performance](../performance/optimization.md)**: Optimize for maximum speed
- 🛠️ **[Error Handling](error-handling.md)**: Handle errors and edge cases
