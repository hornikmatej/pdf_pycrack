# PDF-PyCrack

[![PyPI version](https://badge.fury.io/py/pdf-pycrack.svg)](https://badge.fury.io/py/pdf-pycrack)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A fast, parallel PDF password cracker written in Python.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Core Concepts](#core-concepts)
- [Contributing](#contributing)
- [License](#license)

## Features

-   **Multi-core Cracking:** Utilizes all available CPU cores to accelerate password searching.
-   **Efficient Memory Usage:** Optimized for low memory consumption, even with large PDF files.
-   **Resilient Workers:** Individual worker processes are designed to handle errors silently, ensuring the cracking process continues uninterrupted.
-   **Progress Tracking:** A real-time progress bar keeps you updated on the cracking process.
-   **Adjustable Parameters:** Fine-tune performance with options for password length, batch size, and progress reporting.

## Installation

Recommended to install with `uv`:

```bash
uv pip install pdf-pycrack
```

For development, clone the repository and sync the environment:

```bash
git clone https://github.com/your-username/pdf_pycrack.git
cd pdf_pycrack
uv sync
```

## Usage

To run the PDF cracker, use the following command:

```bash
uv run pdf-pycrack <path_to_pdf>
```

For a full list of options, run:

```bash
uv run pdf-pycrack --help
```

## Core Concepts

`pdf-pycrack` works by generating a vast number of password combinations and testing them in parallel. Here’s how it works:

1.  **Password Generation:** It generates passwords based on a specified character set and length range.
2.  **Parallel Processing:** The password list is divided into batches, and each batch is processed by a separate worker process.
3.  **Password Cracking:** Each worker attempts to decrypt the PDF with its batch of passwords.
4.  **Result Aggregation:** If a worker finds the correct password, it signals the main process, and the search stops.

## Contributing

Contributions are welcome! Please follow these steps to contribute.

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/pdf_pycrack.git
    cd pdf_pycrack
    ```
2.  **Create and sync the environment:**
    ```bash
    uv sync
    ```
3.  **Activate the virtual environment:**
    ```bash
    source .venv/bin/activate
    ```

### Static Checks

This project uses `pre-commit` for code formatting and linting.

-   **Install pre-commit hooks:**
    ```bash
    uv run pre-commit install
    ```
-   **Run checks manually:**
    ```bash
    uv run pre-commit run --all-files
    ```

### Unit Tests

Run tests using `pytest`:

```bash
uv run pytest
```

Tests are marked with categories. You can run specific subsets of tests using `-m <marker_name>`:

-   `numbers`: `uv run pytest -m numbers`
-   `letters`: `uv run pytest -m letters`
-   `special_chars`: `uv run pytest -m special_chars`
-   `mixed`: `uv run pytest -m mixed`

### Pull Requests

1.  Fork the repository.
2.  Create a feature branch.
3.  Make your changes and add/update tests.
4.  Ensure all tests and pre-commit hooks pass.
5.  Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
