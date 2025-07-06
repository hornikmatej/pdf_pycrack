import itertools
import multiprocessing
import queue
import time
from io import BytesIO

import pikepdf
from tqdm import tqdm


def crack_pdf_password(
    pdf_path,
    library_choice="pikepdf",
    min_len=4,
    max_len=5,
    charset="0123456789",
    num_processes=multiprocessing.cpu_count(),
    batch_size_arg=1000,
    progress_interval_arg=0.1,
    report_worker_errors_arg=False,
):
    """
    Crack a PDF password using multiple processes.

    Args:
        pdf_path (str): The path to the PDF file.
        library_choice (str): The library to use for PDF operations.
        min_len (int): Minimum password length.
        max_len (int): Maximum password length.
        charset (str): Character set for passwords.
        num_processes (int): Number of CPU cores to use.
        batch_size_arg (int): Password batch size for workers.
        progress_interval_arg (float): Progress bar refresh interval.
        report_worker_errors_arg (bool): Whether to report worker errors.

    Returns:
        dict or None: A dictionary with results or None if no password is found.
    """
    if not _initialize_cracking(pdf_path, library_choice):
        return None

    result = _manage_workers(
        pdf_path,
        library_choice,
        min_len,
        max_len,
        charset,
        num_processes,
        batch_size_arg,
        progress_interval_arg,
        report_worker_errors_arg,
    )

    if isinstance(result, dict) and result.get("status") == "interrupted":
        return result

    return result


def _initialize_cracking(pdf_path, library_choice):
    """
    Checks if the PDF is encrypted and ready for cracking.

    Args:
        pdf_path (str): The path to the PDF file.
        library_choice (str): The library to use for PDF operations.

    Returns:
        bool: True if the PDF is encrypted, False otherwise.
    """
    if library_choice == "pikepdf":
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
    return False


def _manage_workers(
    pdf_path,
    library_choice,
    min_len,
    max_len,
    charset,
    num_processes,
    batch_size_arg,
    progress_interval_arg,
    report_worker_errors_arg,
):
    """
    Manages worker processes for password cracking.

    Args:
        pdf_path (str): Path to the PDF file.
        library_choice (str): PDF library to use.
        min_len (int): Minimum password length.
        max_len (int): Maximum password length.
        charset (str): Character set for passwords.
        num_processes (int): Number of CPU cores to use.
        batch_size_arg (int): Password batch size for workers.
        progress_interval_arg (float): Progress bar refresh interval.
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
    password_queue = manager.Queue(maxsize=num_processes * batch_size_arg)
    progress_queue = manager.Queue()

    pbar = tqdm(total=total_passwords_to_check, desc="Cracking PDF", unit="pw")

    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(
            target=worker,
            args=(
                pdf_data,
                library_choice,
                password_queue,
                found_event,
                result_queue,
                progress_queue,
                report_worker_errors_arg,
            ),
        )
        processes.append(p)
        p.start()

    found_password = None
    interrupted = False
    passwords_checked = 0

    try:
        # Password generation and queueing
        password_generator = (
            "".join(p_tuple)
            for length in range(min_len, max_len + 1)
            for p_tuple in itertools.product(charset, repeat=length)
        )

        while not found_event.is_set():
            try:
                # Check for progress updates
                while True:
                    try:
                        pbar.update(progress_queue.get_nowait())
                        passwords_checked += 1
                    except queue.Empty:
                        break

                # Check if password is found
                if not result_queue.empty():
                    found_password = result_queue.get()
                    if found_password:
                        found_event.set()
                        break

                # Feed passwords to workers
                for _ in range(num_processes * 10):
                    password = next(password_generator)
                    password_queue.put(password)

            except StopIteration:
                break  # All passwords generated

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        interrupted = True
        found_event.set()

    finally:
        # Signal workers to exit
        for _ in range(num_processes):
            password_queue.put(None)

        for p in processes:
            p.join()

        # Final progress update
        while not progress_queue.empty():
            pbar.update(progress_queue.get_nowait())
            passwords_checked += 1

        pbar.close()

        end_time = time.time()
        elapsed_time = end_time - start_time
        passwords_per_second = (
            (passwords_checked / elapsed_time) if elapsed_time > 0 else 0
        )

        if interrupted:
            return {
                "status": "interrupted",
                "passwords_checked": passwords_checked,
                "elapsed_time": elapsed_time,
                "passwords_per_second": passwords_per_second,
            }

        if found_password:
            return {
                "status": "found",
                "password": found_password,
                "passwords_checked": passwords_checked,
                "elapsed_time": elapsed_time,
                "passwords_per_second": passwords_per_second,
            }

        return {
            "status": "not_found",
            "passwords_checked": passwords_checked,
            "elapsed_time": elapsed_time,
            "passwords_per_second": passwords_per_second,
        }


def worker(
    pdf_data,
    library_choice,
    password_queue,
    found_event,
    result_queue,
    progress_queue,
    report_worker_errors,
):
    """
    Worker process for cracking PDF passwords.

    Args:
        pdf_data (bytes): The in-memory PDF file data.
        library_choice (str): PDF library to use.
        password_queue (multiprocessing.Queue): Queue to get passwords from.
        found_event (multiprocessing.Event): Event to signal when a password is found.
        result_queue (multiprocessing.Queue): Queue to put the found password in.
        progress_queue (multiprocessing.Queue): Queue to report progress.
        report_worker_errors (bool): Whether to report worker errors.
    """
    try:
        while not found_event.is_set():
            try:
                password = password_queue.get(timeout=0.1)
                if password is None:
                    break

                try:
                    with pikepdf.open(BytesIO(pdf_data), password=password):
                        found_event.set()
                        result_queue.put(password)
                        progress_queue.put(1)
                        break
                except pikepdf.PasswordError:
                    progress_queue.put(1)
                except Exception as e:
                    if report_worker_errors:
                        print(f"Worker error during PDF processing: {e}")
            except queue.Empty:
                if all(not p.is_alive() for p in multiprocessing.active_children()):
                    break
                continue
            except Exception as e:
                if report_worker_errors:
                    print(f"Worker error: {e}")
                break
    except KeyboardInterrupt:
        pass
