import glob
import os

import pytest

from pdf_pycrack.core import crack_pdf_password


@pytest.fixture
def test_pdfs_dir():
    return "tests/test_pdfs"


def get_password_from_filename(pdf_path):
    return os.path.splitext(os.path.basename(pdf_path))[0]


@pytest.mark.numbers
@pytest.mark.parametrize("pdf_path", glob.glob("tests/test_pdfs/numbers/*.pdf"))
def test_crack_numbers_pdf(pdf_path):
    password = get_password_from_filename(pdf_path)
    password_len = len(password)
    charset = "0123456789"
    result = crack_pdf_password(
        pdf_path, min_len=password_len, max_len=password_len, charset=charset
    )
    assert result is not None, f"Failed to crack password for {pdf_path}"
    assert result["password"] == password


@pytest.mark.letters
@pytest.mark.parametrize("pdf_path", glob.glob("tests/test_pdfs/letters/*.pdf"))
def test_crack_letters_pdf(pdf_path):
    password = get_password_from_filename(pdf_path)
    password_len = len(password)
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = crack_pdf_password(
        pdf_path, min_len=password_len, max_len=password_len, charset=charset
    )
    assert result is not None, f"Failed to crack password for {pdf_path}"
    assert result["password"] == password


@pytest.mark.special_chars
@pytest.mark.parametrize("pdf_path", glob.glob("tests/test_pdfs/special_chars/*.pdf"))
def test_crack_special_chars_pdf(pdf_path):
    password = get_password_from_filename(pdf_path)
    password_len = len(password)
    charset = "!@#$%^&*()"
    result = crack_pdf_password(
        pdf_path, min_len=password_len, max_len=password_len, charset=charset
    )
    assert result is not None, f"Failed to crack password for {pdf_path}"
    assert result["password"] == password


@pytest.mark.mixed
@pytest.mark.parametrize("pdf_path", glob.glob("tests/test_pdfs/mixed/*.pdf"))
def test_crack_mixed_pdf(pdf_path):
    password = get_password_from_filename(pdf_path)
    password_len = len(password)
    charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()"
    result = crack_pdf_password(
        pdf_path, min_len=password_len, max_len=password_len, charset=charset
    )
    assert result is not None, f"Failed to crack password for {pdf_path}"
    assert result["password"] == password
