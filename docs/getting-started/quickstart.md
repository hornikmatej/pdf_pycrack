# Quick Start

Get up and running with PDF-PyCrack in under 5 minutes! This guide will walk you through your first password cracking session.

## Prerequisites

Make sure you have PDF-PyCrack installed. If not, see the [Installation Guide](installation.md).

```bash
# Verify installation
pdf-pycrack --help
```

## Your First Password Crack

Let's start with a simple example using one of the test files included in the repository.

### Step 1: Get a Test PDF

If you installed from source, you can use the test files:

```bash
# Navigate to the project directory
cd pdf_pycrack

# Use a simple test file with password "100"
uv run pdf-pycrack tests/test_pdfs/numbers/100.pdf
```

If you don't have the test files, you can create a simple encrypted PDF for testing or use your own file.

### Step 2: Run Your First Crack

```bash
# Basic crack with default settings
pdf-pycrack your_file.pdf
```

You'll see output like this:

```
🔒 PDF-PyCrack v0.1.0
📄 File: your_file.pdf
🎯 Testing passwords: length 4-5, charset: 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
🖥️  Using 8 CPU cores, batch size: 100

Cracking: 100%|████████████████| 14776336/14776336 [00:45<00:00, 325891.23it/s]

✅ Password found: "secret"
⏱️  Time: 45.23 seconds
🔢 Passwords tested: 14,776,336
📊 Rate: 325,891 passwords/second
```

### Step 3: Understanding the Output

Let's break down what you're seeing:

- **🔒 Header**: Shows version and file being processed
- **🎯 Configuration**: Current settings (length range, character set)
- **🖥️ Resources**: CPU cores and batch size being used
- **Progress Bar**: Real-time progress with speed indication
- **✅ Result**: Password found with performance statistics

## Common Usage Patterns

### Scenario 1: Numeric Password

If you suspect the password is numeric only:

```bash
pdf-pycrack file.pdf --charset-numbers --min-len 4 --max-len 8
```

### Scenario 2: Simple Letter Password

For alphabetic passwords:

```bash
pdf-pycrack file.pdf --charset-letters --min-len 6 --max-len 10
```

### Scenario 3: Custom Character Set

If you know the password contains only specific characters:

```bash
pdf-pycrack file.pdf --charset-custom "abcdef123456" --min-len 5 --max-len 7
```

### Scenario 4: Full Brute Force

For unknown passwords (warning: this can take a very long time!):

```bash
pdf-pycrack file.pdf --charset-numbers --charset-letters --charset-special --min-len 1 --max-len 6
```

## Performance Tips for Beginners

### 1. Start Small
Begin with shorter password lengths and expand if needed:

```bash
# Start with 1-4 characters
pdf-pycrack file.pdf --min-len 1 --max-len 4

# If not found, try 5-6
pdf-pycrack file.pdf --min-len 5 --max-len 6
```

### 2. Use Specific Character Sets
The smaller the character set, the faster the cracking:

```bash
# Numbers only (10 characters) - fastest
pdf-pycrack file.pdf --charset-numbers

# Letters only (52 characters) - medium
pdf-pycrack file.pdf --charset-letters

# All characters (94 characters) - slowest
pdf-pycrack file.pdf --charset-numbers --charset-letters --charset-special
```

### 3. Optimize CPU Usage
Use all available cores but leave some headroom for system tasks:

```bash
# Use 6 cores instead of all 8 on an 8-core system
pdf-pycrack file.pdf --cores 6
```

## Using as a Python Library

You can also use PDF-PyCrack programmatically:

```python
from pdf_pycrack import crack_pdf_password, PasswordFound

# Basic usage
result = crack_pdf_password("encrypted_file.pdf")

# Custom parameters
result = crack_pdf_password(
    pdf_path="file.pdf",
    min_len=4,
    max_len=6,
    charset="0123456789",
    cores=4,
    batch_size=1000
)

# Handle results
if isinstance(result, PasswordFound):
    print(f"Success! Password: {result.password}")
    print(f"Time taken: {result.duration:.2f} seconds")
    print(f"Passwords tested: {result.passwords_tested:,}")
else:
    print(f"Failed: {result}")
```

## Time Estimates

Here are rough time estimates for different scenarios on a modern 8-core CPU:

| Password Type | Length | Character Set | Estimated Time |
|---------------|---------|---------------|----------------|
| Numeric | 4 digits | 0-9 | < 1 second |
| Numeric | 6 digits | 0-9 | < 10 seconds |
| Alphabetic | 4 letters | a-z | < 30 seconds |
| Alphabetic | 6 letters | a-z | ~10 minutes |
| Mixed | 4 chars | a-z, A-Z, 0-9 | ~2 minutes |
| Mixed | 6 chars | a-z, A-Z, 0-9 | ~6 hours |
| Full | 6 chars | All printable | ~24 hours |

!!! warning "Time Complexity"
    Password cracking time grows exponentially with length and character set size. A 8-character password with full character set could take years to crack!

## Common Beginner Mistakes

### ❌ Starting Too Broad
```bash
# DON'T do this first
pdf-pycrack file.pdf --min-len 1 --max-len 12 --charset-numbers --charset-letters --charset-special
```

### ✅ Start Focused
```bash
# DO this instead
pdf-pycrack file.pdf --min-len 4 --max-len 6 --charset-numbers
```

### ❌ Ignoring Error Messages
Read error messages carefully - they often contain helpful suggestions.

### ✅ Check File First
```bash
# Verify the file is actually encrypted
pdf-pycrack file.pdf --min-len 1 --max-len 1 --charset-numbers
```

## What's Next?

Now that you've run your first crack, explore more advanced features:

- 📚 **[Basic Usage](basic-usage.md)**: Learn all command-line options
- ⚙️ **[Configuration](../user-guide/configuration.md)**: Optimize settings for your needs
- 📊 **[Benchmarking](../performance/benchmarking.md)**: Measure and improve performance
- 🐍 **[Python Library](../user-guide/library.md)**: Integrate into your own applications

## Getting Help

If you run into issues:

1. Check the [Error Handling Guide](../user-guide/error-handling.md)
2. Review [Common Issues](#troubleshooting) below
3. Search [GitHub Issues](https://github.com/hornikmatej/pdf_pycrack/issues)
4. Open a new issue with details about your problem

## Troubleshooting

### Problem: "No password found"
**Solution**: Try expanding your search parameters:
```bash
# Increase length range
pdf-pycrack file.pdf --min-len 1 --max-len 8

# Try different character sets
pdf-pycrack file.pdf --charset-letters --charset-special
```

### Problem: "File not encrypted"
**Solution**: The PDF doesn't have a password. Verify with:
```bash
# Check if file opens without password in PDF viewer
```

### Problem: Cracking is too slow
**Solution**: Reduce search space:
```bash
# Use smaller character set or length range
pdf-pycrack file.pdf --charset-numbers --max-len 6
```

Happy cracking! 🔓
