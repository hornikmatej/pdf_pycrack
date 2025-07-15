"""Command-line interface setup and configuration.

This module provides argument parsing and CLI setup for the PDF
password cracking application.
"""

import argparse
import multiprocessing


def setup_arg_parser() -> argparse.ArgumentParser:
    """Set up and return the argument parser for the command-line interface.

    Returns:
        Configured ArgumentParser instance with all CLI options.
    """
    parser = argparse.ArgumentParser(
        description="Crack PDF passwords using brute-force."
    )
    parser.add_argument("file", type=str, help="Path to the PDF file to crack.")

    parser.add_argument(
        "--cores",
        type=int,
        default=multiprocessing.cpu_count(),
        help=f"Number of CPU cores to use. Default: all available ({multiprocessing.cpu_count()})",
    )
    parser.add_argument(
        "--min_len",
        type=int,
        default=4,
        help="Minimum password length to try. Default: 4",
    )
    parser.add_argument(
        "--max_len",
        type=int,
        default=5,
        help="Maximum password length to try. Default: 5",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=100,
        help="Number of passwords for a worker to check before reporting progress. Default: 100",
    )
    parser.add_argument(
        "--worker_errors",
        action="store_true",
        help="Enable detailed error reporting from worker processes.",
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Enable benchmark mode.",
    )

    # Character set arguments
    parser.add_argument(
        "--charset-numbers",
        action="store_true",
        help="Include numbers (0-9) in the character set.",
    )
    parser.add_argument(
        "--charset-letters",
        action="store_true",
        help="Include letters (a-z, A-Z) in the character set.",
    )
    parser.add_argument(
        "--charset-special",
        action="store_true",
        help="Include common special characters in the character set.",
    )
    parser.add_argument(
        "--charset-custom",
        type=str,
        default="",
        help="Provide a custom character set.",
    )

    return parser
