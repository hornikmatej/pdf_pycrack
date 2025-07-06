import argparse
import multiprocessing

from .core import crack_pdf_password


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
    num_cores_to_use = args.cores
    min_pw_len = args.min_len
    max_pw_len = args.max_len

    if min_pw_len <= 0 or max_pw_len <= 0 or min_pw_len > max_pw_len:
        print("Error: Password lengths must be positive and min_len <= max_len.")
        exit(1)

    print(f"Starting PDF password cracker for '{pdf_document_path}'")
    print(f"Password length range: {min_pw_len} to {max_pw_len} digits.")
    print(f"Using character set: {charset}")

    try:
        result = crack_pdf_password(
            pdf_document_path,
            min_len=min_pw_len,
            max_len=max_pw_len,
            charset=charset,
            num_processes=num_cores_to_use,
            batch_size_arg=args.batch_size,
            report_worker_errors_arg=args.worker_errors,
        )
    except KeyboardInterrupt:
        print("\nCracking process interrupted by user.")
        # Create a dummy result for reporting
        result = {"status": "interrupted"}

    if result:
        status = result.get("status")
        elapsed_time = result.get("elapsed_time", 0)
        passwords_checked = result.get("passwords_checked", 0)
        passwords_per_second = result.get("passwords_per_second", 0)

        if status == "found":
            print(f"\nSuccessfully cracked the password: {result['password']}")
            print(f"Cracking took {elapsed_time:.2f} seconds.")
            print(f"Passwords checked: {passwords_checked}")
            print(f"Average rate: {passwords_per_second:.2f} passwords/sec")
        elif status == "interrupted":
            print("\nCracking process interrupted by user.")
            if "elapsed_time" in result:
                print(f"Elapsed time: {elapsed_time:.2f} seconds.")
            if "passwords_checked" in result:
                print(f"Passwords checked: {passwords_checked}")
            if "passwords_per_second" in result and passwords_per_second > 0:
                print(f"Average rate: {passwords_per_second:.2f} passwords/sec")
        elif status == "not_found":
            print(
                f"\nFailed to crack the password for lengths {min_pw_len} through {max_pw_len}."
            )
            print(f"Elapsed time: {elapsed_time:.2f} seconds.")
            print(f"Passwords checked: {passwords_checked}")
            print(f"Average rate: {passwords_per_second:.2f} passwords/sec")
    else:
        print(
            f"\nFailed to crack the password for lengths {min_pw_len} through {max_pw_len}."
        )


if __name__ == "__main__":
    main()
