from dataclasses import dataclass, field


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
    status: str = field(default="file_read_error", init=False)


@dataclass
class InitializationError(CrackResult):
    """Result for initialization errors."""

    error_message: str
    status: str = field(default="initialization_error", init=False)
