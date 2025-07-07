import os

import pikepdf


def create_password_protected_pdf(output_path, password):
    pdf = pikepdf.new()
    # Add a blank page to the PDF
    pdf.add_blank_page()
    no_perms = pikepdf.Permissions(extract=False, modify_annotation=False)
    pdf.save(
        output_path,
        encryption=pikepdf.Encryption(owner=password, user=password, allow=no_perms),
    )
    print(f"Created: {output_path} with password '{password}'")


def generate_test_pdfs(base_dir="tests/test_pdfs"):
    # Ensure base directories exist
    os.makedirs(os.path.join(base_dir, "numbers"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "letters"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "special_chars"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "mixed"), exist_ok=True)

    # Generate number passwords
    for i in range(100, 105):
        password = str(i)
        create_password_protected_pdf(
            os.path.join(base_dir, "numbers", f"{password}.pdf"), password
        )

    # Generate letter passwords
    letter_passwords = ["ab", "df", "gi", "jk", "mn"]
    for password in letter_passwords:
        create_password_protected_pdf(
            os.path.join(base_dir, "letters", f"{password}.pdf"), password
        )

    # Generate special character passwords
    special_char_passwords = ["!@#", "$%^", "&*("]
    for password in special_char_passwords:
        create_password_protected_pdf(
            os.path.join(base_dir, "special_chars", f"{password}.pdf"), password
        )

    # Generate mixed passwords
    mixed_passwords = ["a1", "4!", "E$"]
    for password in mixed_passwords:
        create_password_protected_pdf(
            os.path.join(base_dir, "mixed", f"{password}.pdf"), password
        )


if __name__ == "__main__":
    generate_test_pdfs()
    generate_test_pdfs()
