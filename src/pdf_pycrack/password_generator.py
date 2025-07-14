import itertools
from typing import Iterator


def generate_passwords(min_len: int, max_len: int, charset: str) -> Iterator[str]:
    """Generator for passwords within a given length range and character set."""
    return (
        "".join(p_tuple)
        for length in range(min_len, max_len + 1)
        for p_tuple in itertools.product(charset, repeat=length)
    )
