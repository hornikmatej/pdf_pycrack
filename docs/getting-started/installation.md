# Installation

PDF-PyCrack requires Python 3.12 or higher and can be installed in several ways depending on your needs.

## Requirements

- **Python**: 3.12 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 4GB RAM minimum, 8GB+ recommended
- **CPU**: Multi-core processor recommended for best performance

## Installation Methods

### Option 1: Install from PyPI (Recommended)

The easiest way to install PDF-PyCrack is from PyPI using `uv` or `pip`:

=== "Using uv (Recommended)"

    ```bash
    # Install uv if you haven't already
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Install PDF-PyCrack
    uv pip install pdf-pycrack
    ```

=== "Using pip"

    ```bash
    pip install pdf-pycrack
    ```

### Option 2: Development Installation

If you want to contribute to the project or use the latest development version:

```bash
# Clone the repository
git clone https://github.com/hornikmatej/pdf_pycrack.git
cd pdf_pycrack

# Install dependencies and package in development mode
uv sync

# Verify installation
uv run pdf-pycrack --help
```

### Option 3: Using pipx (Isolated Installation)

For a completely isolated installation that doesn't affect your system Python:

```bash
# Install pipx if you haven't already
pip install pipx

# Install PDF-PyCrack in an isolated environment
pipx install pdf-pycrack

# Verify installation
pdf-pycrack --help
```

## Verification

After installation, verify that PDF-PyCrack is working correctly:

```bash
# Check version and basic help
pdf-pycrack --help

# Test with a sample file (if you have one)
pdf-pycrack sample.pdf --min-len 1 --max-len 3 --charset-numbers
```

Expected output:
```
usage: pdf-pycrack [-h] [--cores CORES] [--min_len MIN_LEN] [--max_len MAX_LEN]
                   [--batch_size BATCH_SIZE] [--worker_errors]
                   [--charset-numbers] [--charset-letters] [--charset-special]
                   [--charset-custom CHARSET_CUSTOM]
                   file

Crack PDF passwords using brute-force.
...
```

## Dependencies

PDF-PyCrack automatically installs these dependencies:

| Package | Version | Purpose |
|---------|---------|---------|
| `pikepdf` | ≥9.9.0 | PDF manipulation and password testing |
| `tqdm` | ≥4.67.1 | Progress bars and status display |
| `rich` | ≥13.7.1 | Beautiful terminal output and formatting |

## Development Dependencies

If you're installing for development, additional packages are included:

| Package | Purpose |
|---------|---------|
| `pytest` | Testing framework |
| `black` | Code formatting |
| `ruff` | Linting and code analysis |
| `pre-commit` | Git hooks for code quality |
| `isort` | Import sorting |
| `pytest-cov` | Test coverage reporting |

## Troubleshooting

### Common Installation Issues

#### Python Version Error
```
ERROR: This package requires Python 3.12 or higher
```

**Solution**: Update to Python 3.12+:
- **macOS**: Use Homebrew: `brew install python@3.12`
- **Ubuntu**: Use deadsnakes PPA: `sudo apt install python3.12`
- **Windows**: Download from [python.org](https://python.org)

#### Permission Denied (Linux/macOS)
```
ERROR: Permission denied
```

**Solution**: Use user installation:
```bash
pip install --user pdf-pycrack
# or
uv pip install --user pdf-pycrack
```

#### Missing Compiler (Development Installation)
```
ERROR: Microsoft Visual C++ 14.0 is required
```

**Solution**:
- **Windows**: Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- **Linux**: Install build essentials: `sudo apt install build-essential`
- **macOS**: Install Xcode command line tools: `xcode-select --install`

### Performance Issues

#### Slow Installation
If installation is slow, try using a different package index:

```bash
pip install -i https://pypi.org/simple/ pdf-pycrack
```

#### Import Errors
If you get import errors after installation, ensure you're using the correct Python environment:

```bash
# Check Python version
python --version

# Check if package is installed
python -c "import pdf_pycrack; print('Installation successful!')"
```

## Next Steps

Once installation is complete, you're ready to start using PDF-PyCrack!

- 🚀 **Quick Start**: [Try your first password crack](quickstart.md)
- 📖 **Basic Usage**: [Learn the command-line interface](basic-usage.md)
- 🔧 **Configuration**: [Customize settings for your needs](../user-guide/configuration.md)

## Uninstallation

To remove PDF-PyCrack:

=== "uv/pip Installation"

    ```bash
    uv pip uninstall pdf-pycrack
    # or
    pip uninstall pdf-pycrack
    ```

=== "pipx Installation"

    ```bash
    pipx uninstall pdf-pycrack
    ```

=== "Development Installation"

    ```bash
    # Remove the cloned directory
    rm -rf pdf_pycrack
    ```
