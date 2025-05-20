# PDF-PyCrack

A fast, parallel PDF password cracker written in Python.

## Features

-   **Multi-core Cracking:** Utilizes all available CPU cores to accelerate password searching.
-   **Efficient Memory Usage:** Optimized for low memory consumption, even with large PDF files.
-   **Resilient Workers:** Individual worker processes are designed to handle errors silently, ensuring the cracking process continues uninterrupted.
-   **Progress Tracking:** A real-time progress bar keeps you updated on the cracking process.
-   **Adjustable Parameters:** Fine-tune performance with options for password length, batch size, and progress reporting.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/pdf_pycrack.git
    cd pdf_pycrack
    ```

2.  **Install dependencies using uv:**

    ```bash
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

## Development

This project uses `uv` for dependency management and `pytest` for testing.

- Install dependencies:
  ```bash
  uv sync
  ```

- Run tests:
  ```bash
  uv run pytest
  ```

- Run specific test subsets:
  Tests are marked with categories based on the character set they use. You can run specific subsets of tests using `pytest -m <marker_name>`.

  - Numbers only:
    ```bash
    uv run pytest -m numbers
    ```
  - Letters only:
    ```bash
    uv run pytest -m letters
    ```
  - Special characters only:
    ```bash
    uv run pytest -m special_chars
    ```
  - Mixed characters:
    ```bash
    uv run pytest -m mixed
    ```
  You can also combine markers, for example, to run tests marked with `numbers` OR `letters`:
  ```bash
  uv run pytest -m "numbers or letters"
  ```

- Format code:
  ```bash
  uv run -- black .
  ```

- Lint code:
  ```bash
  uv run -- ruff check .
  ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.