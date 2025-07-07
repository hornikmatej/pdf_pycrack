import logging
import time

from .core import crack_pdf_password

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def benchmark_cracking(
    pdf_path,
    min_len,
    max_len,
    charset,
    num_processes,
    batch_size_arg,
    report_worker_errors_arg,
    benchmark_mode=False,
):
    if benchmark_mode:
        logging.info("Benchmark mode enabled. Advanced logging is on.")
    else:
        logging.info("Benchmark mode disabled. Standard logging.")

    start_time = time.time()

    logging.info(f"Starting benchmark for '{pdf_path}'")
    logging.info(
        f"Configuration: min_len={min_len}, max_len={max_len}, charset='{charset}', processes={num_processes}"
    )

    result = crack_pdf_password(
        pdf_path,
        min_len=min_len,
        max_len=max_len,
        charset=charset,
        num_processes=num_processes,
        batch_size_arg=batch_size_arg,
        report_worker_errors_arg=report_worker_errors_arg,
    )

    end_time = time.time()
    elapsed_time = end_time - start_time

    if result and result.get("status") == "found":
        passwords_per_second = result.get("passwords_per_second", 0)
        logging.info(f"Password found: {result['password']}")
        logging.info(f"Passwords per second: {passwords_per_second:.2f}")
    elif result and result.get("status") == "interrupted":
        logging.warning("Benchmark interrupted by user.")
    else:
        logging.info("Password not found.")

    logging.info(f"Total benchmark time: {elapsed_time:.2f} seconds")

    return result
