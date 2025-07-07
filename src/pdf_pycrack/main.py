from .cli import setup_arg_parser
from .core import crack_pdf_password


def main():
    parser = setup_arg_parser()
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
            if (
                "passwords_per_second" in result
                and isinstance(passwords_per_second, (int, float))
                and passwords_per_second > 0
            ):
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
