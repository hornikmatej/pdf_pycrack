import pikepdf
import pypdf  # Added for pypdf usage
from tqdm import tqdm
import multiprocessing
import time
import queue
import argparse  # Added for command-line arguments
from io import BytesIO  # Moved import to top level


def check_password_range(
    # pdf_path, # No longer needed here as pdf_data is passed
    pdf_data,  # Pass pre-read pdf_data
    library_choice,
    start_password,
    end_password,
    password_len,
    found_event,
    result_queue,
    progress_queue,
):
    """
    Checks a range of passwords for a given PDF.
    To be used as a worker function in multiprocessing.
    """
    # Create BytesIO object once per worker process
    pdf_stream = BytesIO(pdf_data)
    local_progress_count = 0
    BATCH_SIZE = 1000  # Report progress in batches of this size

    try:  # Outer try ensures final progress is reported
        for i in range(start_password, end_password + 1):
            if found_event.is_set():
                return  # Exit, outer finally will send pending progress

            password = str(i).zfill(password_len)
            # processed_attempt variable is no longer needed for this progress logic

            try:
                # Reset stream position to the beginning for each attempt
                pdf_stream.seek(0)

                if library_choice == "pikepdf":
                    with pikepdf.open(
                        pdf_stream, password=password
                    ) as pdf_obj:  # Removed allow_overwriting_input=True
                        result_queue.put(password)
                        found_event.set()
                        local_progress_count += 1  # Count this successful attempt
                        return  # Exit, outer finally will send pending progress
                elif library_choice == "pypdf":
                    pdf_stream.seek(
                        0
                    )  # Ensure stream is at the beginning for pypdf too
                    reader = pypdf.PdfReader(pdf_stream)
                    if reader.is_encrypted:
                        if reader.decrypt(password) != 0:
                            result_queue.put(password)
                            found_event.set()
                            local_progress_count += 1  # Count this successful attempt
                            return  # Exit, outer finally will send pending progress
            except pikepdf.PasswordError:
                pass  # Incorrect password for pikepdf
            # No specific pypdf.errors.WrongPasswordError, decrypt handles it by returning 0
            except Exception as e:
                # print(f"Worker error: Password '{password}', Lib: {library_choice}, Error: {e}")
                pass  # Other errors during PDF processing

            # Increment progress count for the attempt (successful, failed, or errored)
            local_progress_count += 1

            if local_progress_count >= BATCH_SIZE:
                try:
                    # Send accumulated batch and reset counter
                    progress_queue.put_nowait(local_progress_count)
                    local_progress_count = 0
                except queue.Full:
                    # If queue is full, count will continue to accumulate
                    # and be sent with the next batch or in the final send.
                    pass
    finally:
        # This outer finally ensures that any remaining progress is sent
        # when the function exits (completes loop, finds password, or event is set).
        if local_progress_count > 0:
            try:
                progress_queue.put(local_progress_count, block=True, timeout=0.01)
            except queue.Full:
                # If still full at the very end, this small portion of progress might be missed.
                pass


def crack_pdf_password_mp(
    pdf_path, library_choice="pikepdf", max_len_for_this_run=5, num_processes=None
):
    """
    Attempts to crack a PDF password for a specific length using multiprocessing.

    Args:
        pdf_path (str): The path to the PDF file.
        library_choice (str): 'pikepdf' or 'pypdf'.
        max_len_for_this_run (int): The specific password length to try in this run.
        num_processes (int): Number of processes to use. Defaults to cpu_count().
    """
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()

    # This print statement is now more specific to the current run
    # print(
    #     f"Attempting to crack '{pdf_path}' using {library_choice} with {num_processes} processes for length {max_len_for_this_run}."
    # )

    try:
        with open(pdf_path, "rb") as f:
            pdf_data_content = f.read()
    except FileNotFoundError:
        print(f"Error: PDF file not found at {pdf_path}")
        return None
    except Exception as e:
        print(f"Error reading PDF file {pdf_path}: {e}")
        return None

    # Initial encryption check (done once before starting workers for this length)
    # This check is important to avoid launching processes if the PDF isn't encrypted
    # or if the library can't handle it.
    initial_check_encrypted = False
    if library_choice == "pikepdf":
        try:
            with pikepdf.open(BytesIO(pdf_data_content)):
                # If open succeeds without password, it's not encrypted with a user password
                print(
                    f"PDF '{pdf_path}' is not user-password encrypted or is empty (checked with pikepdf). Cannot crack."
                )
                return None
        except pikepdf.PasswordError:
            initial_check_encrypted = True
            # This is expected for an encrypted PDF
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
        # If it reaches here and not initial_check_encrypted, something is wrong with the logic or PDF
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
        mininterval=0.1,  # Refresh at most every 0.1 seconds
        unit="pw",  # Set the unit to "pw" (passwords)
        unit_scale=True,  # Automatically scale units (K, M, etc.)
        dynamic_ncols=True,  # Adjust to terminal width changes
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
                ),
            )
            processes.append(process)
            process.start()

        # Progress monitoring loop
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
                    active_processes = False  # All processes have finished
                    # Drain queue one last time
                    while not progress_queue.empty():
                        try:
                            pbar.update(progress_queue.get_nowait())
                        except queue.Empty:
                            break
                    break  # Exit progress loop
            except Exception:  # Should not happen with queue.Empty
                break

        # If password found, ensure tqdm is updated with any remaining items
        if found_event.is_set():
            while not progress_queue.empty():
                try:
                    pbar.update(progress_queue.get_nowait())
                except queue.Empty:
                    break

        for p in processes:
            p.join(timeout=0.2)  # Increased timeout slightly for join
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


from main import main

if __name__ == "__main__":
    main()
