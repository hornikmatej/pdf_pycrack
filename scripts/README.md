# PDF Generation Script

This script generates a set of password-protected PDF files for testing the `pdf-pycrack` application. The generated PDFs are saved in the `tests/test_pdfs` directory, organized into subdirectories based on the character set of the password.

## Usage

To generate the test PDFs, run the following command from the root of the project:

```bash
uv run python scripts/generate_pdfs.py
```

The script will create the following directory structure:

```
tests/test_pdfs/
├───letters/
├───mixed/
├───numbers/
└───special_chars/
```

Each subdirectory will contain a set of PDFs with passwords corresponding to the category.

## Customization

You can customize the generated PDFs by modifying the `generate_test_pdfs` function in the script. For example, you can add new password lists or change the output directory.
