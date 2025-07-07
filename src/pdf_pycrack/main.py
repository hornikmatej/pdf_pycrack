import time

from .cli import setup_arg_parser
from .core import crack_pdf_password
from .formatting.output import print_end_info, print_start_info


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

    start_time = time.time()
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
        result = {
            "status": "interrupted",
            "elapsed_time": time.time() - start_time,
        }

    if result:
        # Only print end info if cracking started
        if result.get("status") != "not_encrypted":
            print_end_info(result)
    else:
        # Fallback for unexpected cases where result is None (e.g. file not found)
        end_time = time.time()
        print_end_info({"status": "not_found", "elapsed_time": end_time - start_time})


if __name__ == "__main__":
    main()
