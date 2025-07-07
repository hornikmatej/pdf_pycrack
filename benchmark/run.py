import logging
import multiprocessing
import time

from pdf_pycrack.core import crack_pdf_password

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_benchmark():
    """Runs a benchmark to measure password cracking speed."""
    pdf_path = "tests/test_pdfs/numbers/100.pdf"  # An arbitrary PDF for testing
    min_len = 4
    max_len = 8  # A longer password length for a more meaningful benchmark
    charset = "0123456789"
    num_processes = multiprocessing.cpu_count()
    batch_size_arg = 100
    report_worker_errors_arg = False

    logging.info(f"Starting benchmark for '{pdf_path}'")
    logging.info(
        f"Configuration: min_len={min_len}, max_len={max_len}, charset='{charset}', processes={num_processes}"
    )

    start_time = time.time()

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

    if result:
        passwords_per_second = result.get("passwords_per_second", 0)
        logging.info(f"Benchmark finished in {elapsed_time:.2f} seconds.")
        logging.info(f"Average passwords per second: {passwords_per_second:.2f}")
    else:
        logging.warning("Benchmark did not produce a result.")


if __name__ == "__main__":
    run_benchmark()
