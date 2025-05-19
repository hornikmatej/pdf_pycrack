import argparse
import multiprocessing
import time
from core import crack_pdf_password_mp


def main():
    parser = argparse.ArgumentParser(
        description="Crack PDF passwords using brute-force."
    )
    parser.add_argument("file", type=str, help="Path to the PDF file to crack.")
    parser.add_argument(
        "--library",
        type=str,
        choices=["pikepdf", "pypdf"],
        default="pikepdf",
        help="PDF library to use (pikepdf or pypdf). Default: pikepdf",
    )
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

    args = parser.parse_args()

    pdf_document_path = args.file
    library_to_use = args.library
    num_cores_to_use = args.cores
    min_pw_len = args.min_len
    max_pw_len = args.max_len

    if min_pw_len <= 0 or max_pw_len <= 0 or min_pw_len > max_pw_len:
        print("Error: Password lengths must be positive and min_len <= max_len.")
        exit(1)

    start_time_main = time.time()
    overall_found_password = None

    print(f"Starting PDF password cracker for '{pdf_document_path}'")
    print(f"Using library: {library_to_use}, Cores: {num_cores_to_use}")
    print(f"Password length range: {min_pw_len} to {max_pw_len} digits.")

    for length_to_try in range(min_pw_len, max_pw_len + 1):
        if overall_found_password:
            break

        if length_to_try > min_pw_len:
            print("-" * 30)

        print(f"Attempting passwords of length {length_to_try}...")
        current_length_password = crack_pdf_password_mp(
            pdf_document_path,
            library_choice=library_to_use,
            max_len_for_this_run=length_to_try,
            num_processes=num_cores_to_use,
            batch_size_arg=args.batch_size,
            progress_interval_arg=args.progress_interval,
            report_worker_errors_arg=args.worker_errors,
        )

        if current_length_password:
            overall_found_password = current_length_password
            print(f"Password found for length {length_to_try}!")
            break
        else:
            pass

    end_time_main = time.time()
    duration_main = end_time_main - start_time_main

    if overall_found_password:
        print(f"\nSuccessfully cracked the password: {overall_found_password}")
    else:
        print(
            f"\nFailed to crack the password for lengths {min_pw_len} through {max_pw_len}."
        )

    print(
        f"Total cracking duration: {duration_main:.2f} seconds using {library_to_use}."
    )


if __name__ == "__main__":
    main()
