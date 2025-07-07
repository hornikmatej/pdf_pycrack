import glob
import os

import pytest

from pdf_pycrack.core import crack_pdf_password
from pdf_pycrack.models.cracking_result import (
    FileReadError,
    InitializationError,
    NotEncrypted,
    PasswordFound,
    PasswordNotFound,
)


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
    assert isinstance(result, PasswordFound), f"Failed to crack password for {pdf_path}"
    assert result.password == password


@pytest.mark.letters
@pytest.mark.parametrize("pdf_path", glob.glob("tests/test_pdfs/letters/*.pdf"))
def test_crack_letters_pdf(pdf_path):
    password = get_password_from_filename(pdf_path)
    password_len = len(password)
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = crack_pdf_password(
        pdf_path, min_len=password_len, max_len=password_len, charset=charset
    )
    assert isinstance(result, PasswordFound), f"Failed to crack password for {pdf_path}"
    assert result.password == password


@pytest.mark.special_chars
@pytest.mark.parametrize("pdf_path", glob.glob("tests/test_pdfs/special_chars/*.pdf"))
def test_crack_special_chars_pdf(pdf_path):
    password = get_password_from_filename(pdf_path)
    password_len = len(password)
    charset = "!@#$%^&*() "
    result = crack_pdf_password(
        pdf_path, min_len=password_len, max_len=password_len, charset=charset
    )
    assert isinstance(result, PasswordFound), f"Failed to crack password for {pdf_path}"
    assert result.password == password


@pytest.mark.mixed
@pytest.mark.parametrize("pdf_path", glob.glob("tests/test_pdfs/mixed/*.pdf"))
def test_crack_mixed_pdf(pdf_path):
    password = get_password_from_filename(pdf_path)
    password_len = len(password)
    charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()"
    result = crack_pdf_password(
        pdf_path, min_len=password_len, max_len=password_len, charset=charset
    )
    assert isinstance(result, PasswordFound), f"Failed to crack password for {pdf_path}"
    assert result.password == password


def test_not_encrypted_pdf():
    pdf_path = "tests/test_pdfs/unencrypted.pdf"
    result = crack_pdf_password(pdf_path, min_len=1, max_len=1, charset="a")
    assert isinstance(
        result, NotEncrypted
    ), f"Expected NotEncrypted for {pdf_path}, but got {type(result).__name__}"


def test_file_read_error():
    pdf_path = "tests/test_pdfs/non_existent_file.pdf"
    result = crack_pdf_password(pdf_path, min_len=1, max_len=1, charset="a")
    assert isinstance(
        result, FileReadError
    ), f"Expected FileReadError for {pdf_path}, but got {type(result).__name__}"


def test_initialization_error_empty_charset():
    pdf_path = "tests/test_pdfs/numbers/100.pdf"  # Use any valid PDF path
    result = crack_pdf_password(pdf_path, min_len=1, max_len=1, charset="")
    assert isinstance(
        result, InitializationError
    ), f"Expected InitializationError for empty charset, but got {type(result).__name__}"


def test_password_not_found():
    # Use an existing encrypted PDF and a charset that won't find the password
    pdf_path = "tests/test_pdfs/numbers/100.pdf"
    password_len = 3
    charset = "abc"  # This charset will not find "100"
    result = crack_pdf_password(
        pdf_path, min_len=password_len, max_len=password_len, charset=charset
    )
    assert isinstance(
        result, PasswordNotFound
    ), f"Expected PasswordNotFound for {pdf_path}, but got {type(result).__name__}"
