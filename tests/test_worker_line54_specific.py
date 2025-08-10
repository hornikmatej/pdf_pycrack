"""Test to specifically cover line 54 in worker.py."""

import queue
from unittest.mock import MagicMock, patch

from pdf_pycrack.worker import worker_process


def test_worker_process_continue_on_empty_passwords_after_fill():
    """Test worker_process continue statement when passwords list is empty after fill loop.

    This test specifically targets line 54: 'continue'
    """
    # Create a real queue for passwords
    password_queue = queue.Queue()
    result_queue = queue.Queue()
    progress_queue = queue.Queue()

    # Create a mock found event
    found_event = MagicMock()
    # First call returns False, second call returns True to exit loop
    found_event.is_set.side_effect = [False, True]

    # Don't add anything to the password queue, so it will timeout during the fill loop

    # Patch pikepdf.open to avoid actual PDF processing
    with patch("pikepdf.open"):
        # Call worker_process
        worker_process(
            pdf_data=b"mock_pdf_data",
            password_queue=password_queue,
            found_event=found_event,
            result_queue=result_queue,
            progress_queue=progress_queue,
            report_worker_errors=False,
            batch_size=10,
        )

        # Since no passwords were added to the queue, the fill loop will timeout,
        # the passwords list will be empty, and the function should hit the continue statement
        # No progress should be reported
        assert progress_queue.empty()
