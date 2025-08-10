# Basic Usage

This guide covers all the essential command-line options and usage patterns for PDF-PyCrack. Whether you're a security professional, researcher, or someone trying to recover a forgotten password, this guide will help you use the tool effectively.

## Command Structure

The basic command structure is:

```bash
pdf-pycrack <pdf_file> [options]
```

## Core Options

### File Selection

```bash
pdf-pycrack /path/to/encrypted.pdf
```

The only required argument is the path to your encrypted PDF file. PDF-PyCrack will automatically detect if the file is encrypted and start the cracking process.

### Password Length

Control the range of password lengths to test:

```bash
# Test passwords from 4 to 8 characters
pdf-pycrack file.pdf --min-len 4 --max-len 8

# Test only 6-character passwords
pdf-pycrack file.pdf --min-len 6 --max-len 6

# Test very short passwords (1-3 characters)
pdf-pycrack file.pdf --min-len 1 --max-len 3
```

!!! tip "Length Strategy"
    Start with shorter lengths first. If you don't find the password, gradually increase the maximum length. Each additional character dramatically increases cracking time.

### Character Sets

Define which characters to include in password attempts:

=== "Individual Sets"

    ```bash
    # Numbers only (0-9)
    pdf-pycrack file.pdf --charset-numbers

    # Letters only (a-z, A-Z)
    pdf-pycrack file.pdf --charset-letters

    # Special characters only (!@#$%^&*()_+-=[]{}|;:,.<>?)
    pdf-pycrack file.pdf --charset-special
    ```

=== "Combined Sets"

    ```bash
    # Numbers and letters
    pdf-pycrack file.pdf --charset-numbers --charset-letters

    # All common characters
    pdf-pycrack file.pdf --charset-numbers --charset-letters --charset-special
    ```

=== "Custom Set"

    ```bash
    # Only specific characters
    pdf-pycrack file.pdf --charset-custom "abcdef123456"

    # Custom with spaces (quote the string)
    pdf-pycrack file.pdf --charset-custom "hello world 123"
    ```

### Performance Tuning

#### CPU Cores

```bash
# Use all available cores (default)
pdf-pycrack file.pdf

# Use specific number of cores
pdf-pycrack file.pdf --cores 4

# Use fewer cores to leave headroom for other tasks
pdf-pycrack file.pdf --cores 6  # on an 8-core system
```

#### Batch Size

The batch size controls how many passwords each worker tests before reporting progress:

```bash
# Smaller batches = more frequent updates, slightly slower
pdf-pycrack file.pdf --batch-size 50

# Default batch size (good balance)
pdf-pycrack file.pdf --batch-size 100

# Larger batches = less frequent updates, slightly faster
pdf-pycrack file.pdf --batch-size 500
```

### Error Reporting

```bash
# Enable detailed error reporting from worker processes
pdf-pycrack file.pdf --worker-errors
```

This is useful for debugging issues but may slow down the cracking process slightly.

## Common Usage Patterns

### 1. Quick Numeric Password Check

Perfect for simple numeric passwords like dates, years, or PIN codes:

```bash
pdf-pycrack file.pdf --charset-numbers --min-len 4 --max-len 8
```

**Use cases:**
- Birth years (1950-2023)
- Simple PINs (1234, 0000)
- Document dates (20230815)

### 2. Dictionary Word Attack

For passwords that might be common words or names:

```bash
pdf-pycrack file.pdf --charset-letters --min-len 5 --max-len 12
```

**Use cases:**
- Person names (john, mary, smith)
- Common words (password, secret, admin)
- Company names

### 3. Mixed Character Passwords

For more complex but short passwords:

```bash
pdf-pycrack file.pdf --charset-numbers --charset-letters --min-len 4 --max-len 6
```

**Use cases:**
- Alphanumeric passwords (abc123, test42)
- Simple mixed passwords (Pass1, Admin2)

### 4. Full Brute Force (Use Carefully!)

For unknown passwords when you have time:

```bash
pdf-pycrack file.pdf --charset-numbers --charset-letters --charset-special --min-len 1 --max-len 4
```

!!! warning "Time Warning"
    Full brute force with long passwords can take days, weeks, or even years. Always start with shorter lengths and specific character sets.

## Advanced Examples

### Example 1: Corporate Environment
Testing passwords in a corporate setting where you know the password policy:

```bash
# Company policy: 8-12 chars, letters + numbers, no special chars
pdf-pycrack corporate_doc.pdf \
  --charset-numbers --charset-letters \
  --min-len 8 --max-len 12 \
  --cores 6  # Leave cores for other work
```

### Example 2: Personal Document Recovery
You forgot your personal PDF password but remember some details:

```bash
# You remember it was your cat's name + birth year
# Cat name was 4-6 letters, birth year 1990-2000
pdf-pycrack personal_doc.pdf \
  --charset-letters \
  --min-len 8 --max-len 10  # 4-6 letters + 4 numbers
```

Then try with numbers added:
```bash
pdf-pycrack personal_doc.pdf \
  --charset-numbers --charset-letters \
  --min-len 8 --max-len 10
```

### Example 3: Security Testing
Testing password strength for security assessment:

```bash
# Start with weak passwords
pdf-pycrack test_doc.pdf --charset-numbers --min-len 1 --max-len 6

# Progress to stronger passwords
pdf-pycrack test_doc.pdf --charset-letters --min-len 6 --max-len 8

# Test complex passwords (if previous steps failed)
pdf-pycrack test_doc.pdf \
  --charset-numbers --charset-letters --charset-special \
  --min-len 6 --max-len 8
```

## Understanding Output

### Progress Display

```
🔒 PDF-PyCrack v0.1.0
📄 File: document.pdf
🎯 Testing passwords: length 4-6, charset: 0123456789abcdef
🖥️  Using 8 CPU cores, batch size: 100

Cracking: 45%|██████     | 2891/6400 [00:15<00:18, 185.32it/s]
```

**Elements explained:**
- **File**: Path to the PDF being cracked
- **Testing passwords**: Current length range and character set
- **CPU cores**: Number of worker processes
- **Progress bar**: Percentage complete, current/total combinations, elapsed time, ETA, speed

### Success Output

```
✅ Password found: "secret123"
⏱️  Time: 45.23 seconds
🔢 Passwords tested: 2,891,456
📊 Rate: 63,891 passwords/second
💾 Memory usage: 45.2 MB peak
```

### Failure Output

```
❌ Password not found
⏱️  Time: 120.45 seconds
🔢 Passwords tested: 14,776,336 (all combinations)
📊 Rate: 122,673 passwords/second
💡 Suggestion: Try longer passwords or different character sets
```

## Performance Optimization

### 1. Character Set Optimization

Order character sets by likelihood:

```bash
# Start with most likely
pdf-pycrack file.pdf --charset-numbers --min-len 4 --max-len 6

# Then try letters if numbers fail
pdf-pycrack file.pdf --charset-letters --min-len 4 --max-len 6

# Finally try combined if both fail
pdf-pycrack file.pdf --charset-numbers --charset-letters --min-len 4 --max-len 6
```

### 2. Length Progression

Build up length gradually:

```bash
# Quick check for very short passwords
pdf-pycrack file.pdf --min-len 1 --max-len 3 --charset-numbers --charset-letters

# Standard range
pdf-pycrack file.pdf --min-len 4 --max-len 6 --charset-numbers --charset-letters

# Extended range if needed
pdf-pycrack file.pdf --min-len 7 --max-len 8 --charset-numbers --charset-letters
```

### 3. Resource Management

```bash
# High performance (use most cores)
pdf-pycrack file.pdf --cores 7 --batch-size 200  # on 8-core system

# Balanced (leave resources for other tasks)
pdf-pycrack file.pdf --cores 4 --batch-size 100

# Conservative (minimal system impact)
pdf-pycrack file.pdf --cores 2 --batch-size 50
```

## Exit Codes

PDF-PyCrack returns different exit codes based on the result:

| Exit Code | Meaning | Action |
|-----------|---------|---------|
| `0` | Password found successfully | Success! |
| `1` | Password not found (all combinations tried) | Try different parameters |
| `2` | File error (not found, not encrypted, etc.) | Check file path and encryption |
| `3` | Invalid parameters | Review command-line arguments |
| `4` | Interrupted by user (Ctrl+C) | Restart with adjusted parameters |
| `5` | System error (memory, permissions, etc.) | Check system resources |

## Tips for Success

### 🎯 Start Focused
- Begin with specific character sets
- Use shorter password lengths initially
- Progress systematically to longer/broader searches

### 📊 Monitor Performance
- Watch the passwords/second rate
- If it's very slow, reduce search space
- Use `--worker-errors` to debug issues

### 🧠 Think Like the Password Creator
- Consider the context (personal, corporate, date-based)
- Remember common password patterns
- Think about character substitutions (@ for a, 3 for e)

### ⏰ Be Patient but Smart
- Brute force takes time - don't expect instant results
- Use time estimates to decide if a search is worth continuing
- Save complex searches for overnight or weekend runs

## Next Steps

Now that you understand basic usage:

- 🔧 **[Configuration Guide](../user-guide/configuration.md)**: Learn advanced configuration options
- 🐍 **[Python Library](../user-guide/library.md)**: Use PDF-PyCrack in your own scripts
- 📊 **[Performance Guide](../performance/optimization.md)**: Optimize for maximum speed
- 🛠️ **[Error Handling](../user-guide/error-handling.md)**: Handle errors and edge cases
