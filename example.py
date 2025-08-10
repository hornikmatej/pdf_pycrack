#!/usr/bin/env python3
"""
Simple example showing the most common use case for pdf_pycrack.
"""

from pdf_pycrack import PasswordFound, crack_pdf_password


def crack_my_pdf(pdf_file_path: str) -> None:
    """
    Simple function to crack a PDF password.

    Args:
        pdf_file_path: Path to the PDF file you want to crack
    """
    print(f"Attempting to crack password for: {pdf_file_path}")

    # Try with common numeric passwords first (fastest)
    print("Trying short numeric passwords (1-3 digits)...")
    result = crack_pdf_password(
        pdf_path=pdf_file_path, min_len=1, max_len=3, charset="0123456789"
    )

    if isinstance(result, PasswordFound):
        print(f"🎉 SUCCESS! Password found: '{result.password}'")
        return

    # If numbers didn't work, try letters
    print("Short numeric passwords failed. Trying letters (4-6 characters)...")
    result = crack_pdf_password(
        pdf_path=pdf_file_path,
        min_len=4,
        max_len=6,
        charset="abcdefghijklmnopqrstuvwxyz",
    )

    if isinstance(result, PasswordFound):
        print(f"🎉 SUCCESS! Password found: '{result.password}'")
        return

    # If still no luck, try alphanumeric
    print("Letters failed. Trying alphanumeric (4-5 characters)...")
    result = crack_pdf_password(
        pdf_path=pdf_file_path,
        min_len=4,
        max_len=5,
        charset="0123456789abcdefghijklmnopqrstuvwxyz",
    )

    if isinstance(result, PasswordFound):
        print(f"🎉 SUCCESS! Password found: '{result.password}'")
        return

    print("😞 Could not find the password with the attempted character sets.")
    print("You might need to:")
    print("- Try longer password lengths")
    print("- Include uppercase letters or special characters")
    print("- Use a dictionary attack instead of brute force")


if __name__ == "__main__":
    # Example usage - replace with your PDF file path
    pdf_path = "tests/test_pdfs/numbers/42.pdf"  # This has password "42"
    crack_my_pdf(pdf_path)
