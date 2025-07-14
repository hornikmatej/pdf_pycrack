from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CrackResult:
    """Base class for cracking results."""

    elapsed_time: float


@dataclass
class PasswordFound(CrackResult):
    """Result when the password is found."""

    password: str
    passwords_checked: int
    passwords_per_second: float
    status: str = field(default="found", init=False)


@dataclass
class PasswordNotFound(CrackResult):
    """Result when the password is not found."""

    passwords_checked: int
    passwords_per_second: float
    status: str = field(default="not_found", init=False)


@dataclass
class CrackingInterrupted(CrackResult):
    """Result when the cracking is interrupted."""

    passwords_checked: int
    status: str = field(default="interrupted", init=False)


@dataclass
class NotEncrypted(CrackResult):
    """Result when the PDF is not encrypted."""

    status: str = field(default="not_encrypted", init=False)


@dataclass
class FileReadError(CrackResult):
    """Result when the PDF file cannot be read."""

    error_message: str
    file_path: Optional[str] = None
    error_type: Optional[str] = None
    suggested_actions: List[str] = field(default_factory=list)
    status: str = field(default="file_read_error", init=False)


@dataclass
class InitializationError(CrackResult):
    """Result for initialization errors."""

    error_message: str
    error_type: Optional[str] = None
    suggested_actions: List[str] = field(default_factory=list)
    status: str = field(default="initialization_error", init=False)


@dataclass
class PDFCorruptedError(CrackResult):
    """Result when the PDF file is corrupted or malformed."""

    error_message: str
    file_path: Optional[str] = None
    corruption_type: Optional[str] = None
    suggested_actions: List[str] = field(default_factory=list)
    status: str = field(default="pdf_corrupted", init=False)


@dataclass
class PDFUnsupportedError(CrackResult):
    """Result when the PDF uses unsupported encryption or features."""

    error_message: str
    encryption_type: Optional[str] = None
    pdf_version: Optional[str] = None
    suggested_actions: List[str] = field(default_factory=list)
    status: str = field(default="pdf_unsupported", init=False)
