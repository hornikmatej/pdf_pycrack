import pikepdf
from tqdm import tqdm
import multiprocessing
import queue
from io import BytesIO
import time
import itertools


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

    manager = multiprocessing.Manager()
    found_event = manager.Event()
    result_queue = manager.Queue()
    progress_queue = manager.Queue()

    pbar = tqdm(total=total_passwords_to_check, desc="Cracking PDF", unit="pw")
    processes = []
    found_password = None
    interrupted = False

    try:
        for length_to_try in range(min_len, max_len + 1):
            if found_event.is_set():
                break

            process = multiprocessing.Process(
                target=check_password_range,
                args=(
                    pdf_path,
                    library_choice,
                    length_to_try,
                    charset,
                    found_event,
                    result_queue,
                    progress_queue,
                    batch_size_arg,
                    report_worker_errors_arg,
                ),
            )
            processes.append(process)
            process.start()

        active_processes = list(processes)
        while active_processes:
            while not progress_queue.empty():
                try:
                    increment = progress_queue.get_nowait()
                    pbar.update(increment)
                except queue.Empty:
                    break

            if not result_queue.empty():
                found_password = result_queue.get()
                found_event.set()
                break

            active_processes = [p for p in active_processes if p.is_alive()]
            time.sleep(progress_interval_arg)

    except KeyboardInterrupt:
        interrupted = True
        print("\n\nCracking interrupted by user (Ctrl+C). Terminating workers...")
        found_event.set()

    finally:
        if found_event.is_set():
            for p in processes:
                if p.is_alive():
                    p.terminate()
                    p.join(timeout=1)

        while not progress_queue.empty():
            try:
                increment = progress_queue.get_nowait()
                pbar.update(increment)
            except queue.Empty:
                break

        for p in processes:
            p.join()

        pbar.close()

        if interrupted:
            duration = time.time() - start_time
            passwords_checked = pbar.n
            rate = passwords_checked / duration if duration > 0 else 0
            return {
                "status": "interrupted",
                "duration": duration,
                "checked": passwords_checked,
                "rate": rate,
            }

    try:
        if not found_password:
            found_password = result_queue.get_nowait()
    except queue.Empty:
        found_password = None

    return found_password


def check_password_range(
    pdf_path,
    library_choice,
    password_len,
    charset,
    found_event,
    result_queue,
    progress_queue,
    batch_size,
    report_worker_errors,
):
    """
    Checks a range of passwords for a given PDF in a worker process.

    Args:
        pdf_path (str): Path to the PDF file.
        library_choice (str): PDF library to use.
        password_len (int): The length of passwords to check.
        charset (str): The character set to use for generating passwords.
        found_event (multiprocessing.Event): Event to signal when the password is found.
        result_queue (multiprocessing.Queue): Queue to store the found password.
        progress_queue (multiprocessing.Queue): Queue to report progress.
        batch_size (int): Number of passwords to check before reporting progress.
        report_worker_errors (bool): Flag to enable or disable worker error reporting.
    """
    local_progress_count = 0
    BATCH_SIZE = batch_size

    try:
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
        pdf_stream = BytesIO(pdf_data)

        for attempt in itertools.product(charset, repeat=password_len):
            if found_event.is_set():
                return

            password = "".join(attempt)
            pdf_stream.seek(0)

            try:
                if library_choice == "pikepdf":
                    with pikepdf.open(pdf_stream, password=password):
                        result_queue.put(password)
                        found_event.set()
                        local_progress_count += 1
                        return
            except pikepdf.PasswordError:
                pass
            except Exception as e:
                if report_worker_errors:
                    print(
                        f"Worker error: Password '{password}', Lib: {library_choice}, Error: {e}"
                    )
                else:
                    pass

            local_progress_count += 1
            if local_progress_count >= BATCH_SIZE:
                try:
                    progress_queue.put_nowait(local_progress_count)
                    local_progress_count = 0
                except queue.Full:
                    pass
    finally:
        if local_progress_count > 0:
            try:
                progress_queue.put(local_progress_count, block=True, timeout=0.01)
            except queue.Full:
                pass


def crack_pdf_password_mp(
    pdf_path,
    library_choice="pikepdf",
    min_len=4,
    max_len=5,
    charset="0123456789",
    num_processes=None,
    batch_size_arg=1000,
    progress_interval_arg=0.1,
    report_worker_errors_arg=False,
):
    """
    Cracks a PDF password using a brute-force attack with multiprocessing.

    This function orchestrates the password cracking process by initializing,
    running, and managing worker processes that check different password lengths
    concurrently.

    Args:
        pdf_path (str): The path to the PDF file to crack.
        library_choice (str): The PDF library to use ('pikepdf').
        min_len (int): The minimum password length to check.
        max_len (int): The maximum password length to check.
        charset (str): The character set to use for generating passwords.
        num_processes (int, optional): The number of CPU cores to use.
            Defaults to all available cores.
        batch_size_arg (int): The number of passwords each worker checks
            before reporting progress.
        progress_interval_arg (float): The interval for updating the
            progress bar.
        report_worker_errors_arg (bool): Whether to report errors from
            worker processes.

    Returns:
        str or dict or None:
        - The found password as a string.
        - A dictionary with cracking statistics if interrupted.
        - None if the password is not found or an error occurs.
    """
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()

    if not _initialize_cracking(pdf_path, library_choice):
        return None

    return _manage_workers(
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
