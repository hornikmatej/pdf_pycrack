"""Test to specifically cover line 51 in worker.py."""

import queue
from unittest.mock import MagicMock, patch

from pdf_pycrack.worker import worker_process


def test_worker_process_return_on_empty_passwords():
    """Test worker_process return when passwords list is empty after queue.Empty.

    This test specifically targets line 51: 'if not passwords: return'
    """
    # Create a real queue for passwords
    password_queue = queue.Queue()
    result_queue = queue.Queue()
    progress_queue = queue.Queue()

    # Create a mock found event
    found_event = MagicMock()
    found_event.is_set.return_value = False  # Keep looping initially

    # Don't add anything to the password queue, so it will timeout

    # Patch pikepdf.open to avoid actual PDF processing
    with patch("pikepdf.open"):
        # Patch time.sleep to avoid delays
        with patch("time.sleep"):
            # Call worker_process with a very short timeout
            worker_process(
                pdf_data=b"mock_pdf_data",
                password_queue=password_queue,
                found_event=found_event,
                result_queue=result_queue,
                progress_queue=progress_queue,
                report_worker_errors=False,
                batch_size=10,
            )

        # Since no passwords were added to the queue, and the queue times out,
        # the passwords list should be empty, and the function should return
        # without processing anything
        assert progress_queue.empty()
