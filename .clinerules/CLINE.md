## Project Structure

-   **`src/`**: Main application code.
-   **`tests/`**: Unit and integration tests.
-   **`docs/`**: Documentation source files (MkDocs format).
-   **`pyproject.toml`**: Project metadata and dependencies, managed by `uv`.

## Dependency Management

This project uses `uv` for managing dependencies. To install or update dependencies, use the following commands:

-   **Install all dependencies:**

    ```bash
    uv sync
    ```

-   **Add a new dependency:**

    ```bash
    uv add <package-name>
    ```

-   **Add a new development dependency:**

    ```bash
    uv add --dev <package-name>
    ```

## Running the application

-   **Run the application:**

    ```bash
    uv run pdf-pycrack <path_to_pdf> [options]
    ```

## Documentation

Documentation is built with MkDocs and includes comprehensive guides, examples, and API reference.

-   **Serve documentation locally:**

    ```bash
    ./docs-build.sh serve
    # or: uv run mkdocs serve
    ```

-   **Build static documentation:**

    ```bash
    ./docs-build.sh build
    # or: uv run mkdocs build
    ```

-   **Deploy documentation:**

    ```bash
    ./docs-build.sh deploy
    # or: uv run mkdocs gh-deploy
    ```

Documentation includes:
- Getting started guides and tutorials
- Complete CLI and Python API reference
- Performance optimization and benchmarking guides
- Development and contribution guidelines

## Dependency Management

This project uses `uv` for managing dependencies. To install or update dependencies, use the following commands:

-   **Install all dependencies:**

    ```bash
    uv sync
    ```

-   **Add a new dependency:**

    ```bash
    uv add <package-name>
    ```

-   **Add a new development dependency:**

    ```bash
    uv add --dev <package-name>
    ```

## Running the application

-   **Run the application:**

    ```bash
    uv run pdf-pycrack <path_to_pdf> [options]
    ```

## Testing

Tests are located in the `tests/` directory and are run using `pytest`.

-   **Run all tests:**

    ```bash
    uv run pytest
    ```

-   **Run specific test subsets:**
    Tests are marked with categories based on the character set they use. You can run specific subsets of tests using `pytest -m <marker_name>`.

    -   Numbers only:
        ```bash
        uv run pytest -m numbers
        ```
    -   Letters only:
        ```bash
        uv run pytest -m letters
        ```
    -   Special characters only:
        ```bash
        uv run pytest -m special_chars
        ```
    -   Mixed characters:
        ```bash
        uv run pytest -m mixed
        ```
    You can also combine markers, for example, to run tests marked with `numbers` OR `letters`:
    ```bash
    uv run pytest -m "numbers or letters"
    ```

## Collaboration Guidelines
-   **Dependency Updates:** If a dependency needs to be updated, use the `uv add` command.
-   **Pre-commit Hooks:** Ensure all code changes pass pre-commit checks before committing. Run `uv run pre-commit install` to install the hooks and `uv run pre-commit run --all-files` to run checks manually.
-  **Updating this file** If you need to change/add new info to this file. Make sure to add it and change the old outdated information.
