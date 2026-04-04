#!/usr/bin/env python3
"""Bootstrap script to install project dependencies and pre-commit hooks using uv."""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PRE_COMMIT_CONFIG = PROJECT_ROOT / ".pre-commit-config.yaml"


def _run(command: list[str], *, quiet: bool = False) -> None:
    """Execute a command in the project root, propagating errors."""
    stdout = subprocess.DEVNULL if quiet else None
    stderr = subprocess.DEVNULL if quiet else None
    subprocess.run(
        command,
        check=True,
        cwd=PROJECT_ROOT,
        stdout=stdout,
        stderr=stderr,
    )


def main() -> None:
    try:
        _run(["uv", "--version"], quiet=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("uv not found. Please install uv first.")
        print(
            "See https://docs.astral.sh/uv/getting-started/installation/ for instructions."
        )
        sys.exit(1)

    print("Syncing dependencies (including dev tools) with uv...")
    _run(["uv", "sync", "--extra", "dev"])

    print("Installing pre-commit hooks...")
    _run(
        [
            "uv",
            "run",
            "pre-commit",
            "install",
            "--config",
            str(PRE_COMMIT_CONFIG),
        ]
    )

    print("All set! Pre-commit hooks are installed.")


if __name__ == "__main__":
    main()
