from unittest.mock import patch

import pytest

from pdf_pycrack.benchmark import benchmark_cracking


@pytest.fixture
def mock_crack_pdf_password():
    with patch("pdf_pycrack.benchmark.crack_pdf_password") as mock_crack:
        yield mock_crack


def test_benchmark_mode_enabled(mock_crack_pdf_password):
    mock_crack_pdf_password.return_value = {
        "status": "found",
        "password": "1234",
        "passwords_per_second": 100.0,
    }

    result = benchmark_cracking(
        "dummy.pdf", 4, 5, "0123456789", 4, 1000, False, benchmark_mode=True
    )

    assert result is not None
    assert result["status"] == "found"
    assert result["password"] == "1234"


def test_benchmark_mode_disabled(mock_crack_pdf_password):
    mock_crack_pdf_password.return_value = {
        "status": "not_found",
    }

    result = benchmark_cracking(
        "dummy.pdf", 4, 5, "0123456789", 4, 1000, False, benchmark_mode=False
    )

    assert result is not None
    assert result["status"] == "not_found"
