import pikepdf
import pypdf
from tqdm import tqdm
import multiprocessing
import time
import queue
from io import BytesIO


def check_password_range(
    pdf_data,
    library_choice,
    start_password,
    end_password,
    password_len,
    found_event,
    result_queue,
    progress_queue,
    batch_size,  # Added
    report_worker_errors,  # Added
):
    """
    Checks a range of passwords for a given PDF.
    To be used as a worker function in multiprocessing.
    """
    pdf_stream = BytesIO(pdf_data)
    local_progress_count = 0
    BATCH_SIZE = batch_size

    try:
        for i in range(start_password, end_password + 1):
            if found_event.is_set():
                return

            password = str(i).zfill(password_len)
            pdf_stream.seek(0)

            try:
                if library_choice == "pikepdf":
                    with pikepdf.open(pdf_stream, password=password) as pdf_obj:
                        result_queue.put(password)
                        found_event.set()
                        local_progress_count += 1
                        return
                elif library_choice == "pypdf":
                    reader = pypdf.PdfReader(pdf_stream)
                    if reader.is_encrypted:
                        if reader.decrypt(password) != 0:
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
                    pass  # Silently ignore if not reporting

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
    max_len_for_this_run=5,
    num_processes=None,
    batch_size_arg=1000,  # Added with default
    progress_interval_arg=0.1,  # Added with default
    report_worker_errors_arg=False,  # Added with default
):
    """
    Attempts to crack a PDF password for a specific length using multiprocessing.
    """
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()

    try:
        with open(pdf_path, "rb") as f:
            pdf_data_content = f.read()
    except FileNotFoundError:
        print(f"Error: PDF file not found at {pdf_path}")
        return None
    except Exception as e:
        print(f"Error reading PDF file {pdf_path}: {e}")
        return None

    initial_check_encrypted = False
    if library_choice == "pikepdf":
        try:
            with pikepdf.open(BytesIO(pdf_data_content)):
                print(
                    f"PDF '{pdf_path}' is not user-password encrypted or is empty (checked with pikepdf). Cannot crack."
                )
                return None
        except pikepdf.PasswordError:
            initial_check_encrypted = True
        except Exception as e:
            print(f"Pikepdf error during initial check of '{pdf_path}': {e}")
            return None
    elif library_choice == "pypdf":
        try:
            reader = pypdf.PdfReader(BytesIO(pdf_data_content))
            if reader.is_encrypted:
                initial_check_encrypted = True
            else:
                print(
                    f"PDF '{pdf_path}' is not encrypted (checked with pypdf). Cannot crack."
                )
                return None
        except Exception as e:
            print(f"Pypdf error during initial check of '{pdf_path}': {e}")
            return None

    if not initial_check_encrypted:
        print(
            f"Could not confirm PDF '{pdf_path}' is encrypted before starting workers. Aborting for this length."
        )
        return None

    manager = multiprocessing.Manager()
    found_event = manager.Event()
    result_queue = manager.Queue()
    progress_queue = manager.Queue()

    p_len = max_len_for_this_run
    total_passwords = 10**p_len
    passwords_per_process = (total_passwords + num_processes - 1) // num_processes

    processes = []

    with tqdm(
        total=total_passwords,
        desc=f"Cracking {p_len}-digit passwords ({library_choice})",
        mininterval=progress_interval_arg,  # Use argument
        unit="pw",
        unit_scale=True,
        dynamic_ncols=True,
    ) as pbar:
        for i in range(num_processes):
            if found_event.is_set():
                break
            start_num = i * passwords_per_process
            end_num = min((i + 1) * passwords_per_process - 1, total_passwords - 1)
            if start_num >= total_passwords:
                continue
            process = multiprocessing.Process(
                target=check_password_range,
                args=(
                    pdf_data_content,
                    library_choice,
                    start_num,
                    end_num,
                    p_len,
                    found_event,
                    result_queue,
                    progress_queue,
                    batch_size_arg,  # Pass argument
                    report_worker_errors_arg,  # Pass argument
                ),
            )
            processes.append(process)
            process.start()

        active_processes = True
        while (
            pbar.n < total_passwords and not found_event.is_set() and active_processes
        ):
            try:
                increment = progress_queue.get(block=True, timeout=0.05)
                if increment:
                    pbar.update(increment)
            except queue.Empty:
                if not any(p.is_alive() for p in processes):
                    active_processes = False
                    while not progress_queue.empty():
                        try:
                            pbar.update(progress_queue.get_nowait())
                        except queue.Empty:
                            break
                    break
            except Exception:
                break

        if found_event.is_set():
            while not progress_queue.empty():
                try:
                    pbar.update(progress_queue.get_nowait())
                except queue.Empty:
                    break

        for p in processes:
            p.join(timeout=0.2)
            if p.is_alive():
                p.terminate()
                p.join()

    if not result_queue.empty():
        found_password = result_queue.get_nowait()
        while not result_queue.empty():
            result_queue.get_nowait()
        found_event.set()
        for p in processes:
            if p.is_alive():
                p.terminate()
                p.join()
        return found_password

    return None
