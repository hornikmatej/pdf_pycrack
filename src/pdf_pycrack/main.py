import time

from .cli import setup_arg_parser
from .core import crack_pdf_password
from .formatting.output import print_end_info, print_start_info
from .models.cracking_result import CrackingInterrupted, CrackResult, PasswordNotFound


def main() -> None:
    parser = setup_arg_parser()
    args = parser.parse_args()

    # Construct character set
    charset: str = args.charset_custom
    if args.charset_numbers:
        charset += "0123456789"
    if args.charset_letters:
        charset += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if args.charset_special:
        charset += "!@#$%^&*() "

    # Default to numbers if no charset is specified
    if not charset:
        charset = "0123456789"
        print("No charset specified, defaulting to numbers (0-9).")

    # Remove duplicates and sort for consistency
    charset = "".join(sorted(list(set(charset))))

    pdf_document_path: str = args.file
    num_cores_to_use: int = args.cores
    min_pw_len: int = args.min_len
    max_pw_len: int = args.max_len

    if min_pw_len <= 0 or max_pw_len <= 0 or min_pw_len > max_pw_len:
        print("Error: Password lengths must be positive and min_len <= max_len.")
        exit(1)

    start_time: float = time.time()
    print_start_info(
        pdf_document_path,
        min_pw_len,
        max_pw_len,
        charset,
        args.batch_size,
        num_cores_to_use,
        start_time,
    )

    try:
        result: CrackResult = crack_pdf_password(
            pdf_document_path,
            min_len=min_pw_len,
            max_len=max_pw_len,
            charset=charset,
            num_processes=num_cores_to_use,
            batch_size_arg=args.batch_size,
            report_worker_errors_arg=args.worker_errors,
        )
    except KeyboardInterrupt:
        result = CrackingInterrupted(
            passwords_checked=0,  # This will be unknown
            elapsed_time=time.time() - start_time,
        )

    if result:
        # Only print end info if cracking started
        # All concrete CrackResult implementations have a status field
        if getattr(result, "status", "") != "not_encrypted":
            print_end_info(result)
    else:
        # Fallback for unexpected cases where result is None (e.g. file not found)
        end_time: float = time.time()
        print_end_info(
            PasswordNotFound(
                elapsed_time=end_time - start_time,
                passwords_checked=0,
                passwords_per_second=0,
            )
        )


if __name__ == "__main__":
    main()
