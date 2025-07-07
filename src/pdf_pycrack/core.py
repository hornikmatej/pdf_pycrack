import multiprocessing
import queue
import time
from io import BytesIO

import pikepdf
from tqdm import tqdm

from .password_generator import generate_passwords


def crack_pdf_password(
    pdf_path,
    min_len=4,
    max_len=5,
    charset="0123456789",
    num_processes=multiprocessing.cpu_count(),
    batch_size_arg=5000,
    report_worker_errors_arg=True,
):
    """
    Crack a PDF password using multiple processes.

    Args:
        pdf_path (str): The path to the PDF file.
        min_len (int): Minimum password length.
        max_len (int): Maximum password length.
        charset (str): Character set for passwords.
        num_processes (int): Number of CPU cores to use.
        batch_size_arg (int): Password batch size for workers.
        report_worker_errors_arg (bool): Whether to report worker errors.

    Returns:
        dict or None: A dictionary with results or None if no password is found.
    """
    if not _initialize_cracking(pdf_path):
        return None

    result = _manage_workers(
        pdf_path,
        min_len,
        max_len,
        charset,
        num_processes,
        batch_size_arg,
        report_worker_errors_arg,
    )

    if isinstance(result, dict) and result.get("status") == "interrupted":
        return result

    return result


def _initialize_cracking(pdf_path):
    """
    Checks if the PDF is encrypted and ready for cracking.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        bool: True if the PDF is encrypted, False otherwise.
    """
    try:
        with pikepdf.open(pdf_path):
            print(
                f"PDF '{pdf_path}' is not user-password encrypted or is empty (checked with pikepdf). Cannot crack."
            )
            return False
    except pikepdf.PasswordError:
        return True  # PDF is encrypted
    except Exception as e:
        print(f"Error during initial check with pikepdf on '{pdf_path}': {e}")
        return False


def _password_generator_process(
    password_queue,
    min_len,
    max_len,
    charset,
    stop_generating_event,
    num_processes,
):
    """
    A separate process to generate and queue passwords.

    Args:
        password_queue (multiprocessing.Queue): Queue to put passwords into.
        min_len (int): Minimum password length.
        max_len (int): Maximum password length.
        charset (str): Character set for passwords.
        stop_generating_event (multiprocessing.Event): Event to signal when to stop.
        num_processes (int): Number of worker processes.
    """
    password_generator = generate_passwords(min_len, max_len, charset)

    while not stop_generating_event.is_set():
        try:
            password = next(password_generator)
            password_queue.put(password)
        except StopIteration:
            break

    # Signal workers to exit
    for _ in range(num_processes):
        password_queue.put(None)


def _manage_workers(
    pdf_path,
    min_len,
    max_len,
    charset,
    num_processes,
    batch_size_arg,
    report_worker_errors_arg,
):
    """
    Manages worker processes for password cracking.

    Args:
        pdf_path (str): Path to the PDF file.
        min_len (int): Minimum password length.
        max_len (int): Maximum password length.
        charset (str): Character set for passwords.
        num_processes (int): Number of CPU cores to use.
        batch_size_arg (int): Password batch size for workers.
        report_worker_errors_arg (bool): Whether to report worker errors.

    Returns:
        str or dict or None: The found password, an interruption summary, or None.
    """
    start_time = time.time()
    total_passwords_to_check = sum(
        len(charset) ** length for length in range(min_len, max_len + 1)
    )

    try:
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
    except IOError as e:
        print(f"Error reading PDF file: {e}")
        return None

    manager = multiprocessing.Manager()
    found_event = manager.Event()
    result_queue = manager.Queue()
    password_queue = manager.Queue(maxsize=num_processes * 2)  # Smaller queue size
    progress_queue = manager.Queue()
    stop_generating_event = manager.Event()

    pbar = tqdm(total=total_passwords_to_check, desc="Cracking PDF", unit="pw")

    # Start the password generator process
    generator_process = multiprocessing.Process(
        target=_password_generator_process,
        args=(
            password_queue,
            min_len,
            max_len,
            charset,
            stop_generating_event,
            num_processes,
        ),
    )
    generator_process.start()

    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(
            target=worker,
            args=(
                pdf_data,
                password_queue,
                found_event,
                result_queue,
                progress_queue,
                report_worker_errors_arg,
                batch_size_arg,  # Pass batch_size to worker
            ),
        )
        processes.append(p)
        p.start()

    found_password = None
    interrupted = False
    passwords_processed = 0

    try:
        while (
            passwords_processed < total_passwords_to_check and not found_event.is_set()
        ):
            try:
                progress = progress_queue.get(timeout=0.1)
                pbar.update(progress)
                passwords_processed += progress
            except queue.Empty:
                # Check if the generator is done and the queue is empty
                if (
                    not generator_process.is_alive()
                    and password_queue.empty()
                    and not any(p.is_alive() for p in processes)
                ):
                    break
                continue

            if not result_queue.empty():
                found_password = result_queue.get_nowait()
                if found_password:
                    found_event.set()
                    stop_generating_event.set()

    except KeyboardInterrupt:
        interrupted = True
        print("\nCracking interrupted by user.")
        stop_generating_event.set()

    # Wait for all worker processes to finish
    for p in processes:
        p.join()

    generator_process.join()

    # Final progress update
    while not progress_queue.empty():
        passwords_processed += progress_queue.get_nowait()
    pbar.update(total_passwords_to_check - pbar.n)

    # Collect the final result if found
    if not found_password:
        while not result_queue.empty():
            found_password = result_queue.get_nowait()

    pbar.close()

    end_time = time.time()
    elapsed_time = end_time - start_time
    passwords_per_second = (
        (passwords_processed / elapsed_time) if elapsed_time > 0 else 0
    )

    if interrupted:
        return {
            "status": "interrupted",
            "passwords_checked": passwords_processed,
            "elapsed_time": elapsed_time,
        }

    if found_password:
        return {
            "status": "found",
            "password": found_password,
            "passwords_checked": passwords_processed,
            "elapsed_time": elapsed_time,
            "passwords_per_second": passwords_per_second,
        }

    return None


def worker(
    pdf_data,
    password_queue,
    found_event,
    result_queue,
    progress_queue,
    report_worker_errors,
    batch_size,
):
    """
    Worker process for cracking PDF passwords.

    Args:
        pdf_data (bytes): The in-memory PDF file data.
        password_queue (multiprocessing.Queue): Queue to get passwords from.
        found_event (multiprocessing.Event): Event to signal when a password is found.
        result_queue (multiprocessing.Queue): Queue to put the found password in.
        progress_queue (multiprocessing.Queue): Queue to report progress.
        report_worker_errors (bool): Whether to report worker errors.
        batch_size (int): The number of passwords to process in a batch.
    """
    passwords = []
    try:
        while not found_event.is_set():
            # Fill the batch
            while len(passwords) < batch_size:
                try:
                    password = password_queue.get(timeout=1.0)  # Longer timeout
                    if password is None:  # End of queue
                        if not passwords:  # No more passwords to process
                            return
                        break
                    passwords.append(password)
                except queue.Empty:
                    if not passwords:  # No work to do, exit
                        return
                    break  # Process the current batch

            if not passwords:
                continue

            for password in passwords:
                if found_event.is_set():
                    break
                try:
                    with pikepdf.open(BytesIO(pdf_data), password=password):
                        if not found_event.is_set():
                            found_event.set()
                            result_queue.put(password)
                        break  # Exit after finding the password
                except pikepdf.PasswordError:
                    continue
                except Exception as e:
                    if report_worker_errors:
                        print(f"Worker error during PDF processing: {e}")

            progress_queue.put(len(passwords))
            passwords = []

    except KeyboardInterrupt:
        pass
    finally:
        # Ensure any remaining progress is reported
        if passwords:
            progress_queue.put(len(passwords))
