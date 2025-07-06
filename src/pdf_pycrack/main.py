import argparse
import multiprocessing
import time

from .core import crack_pdf_password_mp


def main():
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
        default=1000,
        help="Number of passwords for a worker to check before reporting progress. Default: 1000",
    )
    parser.add_argument(
        "--progress_interval",
        type=float,
        default=0.1,
        help="Minimum interval in seconds for refreshing the progress bar. Default: 0.1",
    )
    parser.add_argument(
        "--worker_errors",
        action="store_true",  # Makes it a boolean flag, default is False
        help="Enable detailed error reporting from worker processes.",
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

    args = parser.parse_args()

    # Construct character set
    charset = args.charset_custom
    if args.charset_numbers:
        charset += "0123456789"
    if args.charset_letters:
        charset += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if args.charset_special:
        charset += "!@#$%^&*()"

    # Default to numbers if no charset is specified
    if not charset:
        charset = "0123456789"
        print("No charset specified, defaulting to numbers (0-9).")

    # Remove duplicates and sort for consistency
    charset = "".join(sorted(list(set(charset))))

    pdf_document_path = args.file
    library_to_use = "pikepdf"
    num_cores_to_use = args.cores
    min_pw_len = args.min_len
    max_pw_len = args.max_len

    if min_pw_len <= 0 or max_pw_len <= 0 or min_pw_len > max_pw_len:
        print("Error: Password lengths must be positive and min_len <= max_len.")
        exit(1)

    start_time_main = time.time()

    print(f"Starting PDF password cracker for '{pdf_document_path}'")
    print(f"Using library: {library_to_use}, Cores: {num_cores_to_use}")
    print(f"Password length range: {min_pw_len} to {max_pw_len} digits.")
    print(f"Using character set: {charset}")

    found_password = crack_pdf_password_mp(
        pdf_document_path,
        library_choice=library_to_use,
        min_len=min_pw_len,
        max_len=max_pw_len,
        charset=charset,
        num_processes=num_cores_to_use,
        batch_size_arg=args.batch_size,
        progress_interval_arg=args.progress_interval,
        report_worker_errors_arg=args.worker_errors,
    )

    end_time_main = time.time()
    duration_main = end_time_main - start_time_main

    if (
        isinstance(found_password, dict)
        and found_password.get("status") == "interrupted"
    ):
        summary = found_password
        print("\n--- Cracking Summary ---")
        print(f"Status: {summary['status'].capitalize()}")
        print(f"Total Time: {summary['duration']:.2f} seconds")
        print(f"Passwords Checked: {summary['checked']}")
        print(f"Average Rate: {summary['rate']:.2f} passwords/sec")
        print("------------------------")
    elif found_password:
        print(f"\nSuccessfully cracked the password: {found_password}")
    else:
        print(
            f"\nFailed to crack the password for lengths {min_pw_len} through {max_pw_len}."
        )

    print(f"Total cracking time: {duration_main:.2f} seconds.")


if __name__ == "__main__":
    main()
