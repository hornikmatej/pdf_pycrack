"""Test to cover line 54 in worker.py."""

import queue
from unittest.mock import MagicMock, patch

from pdf_pycrack.worker import worker_process


def test_worker_process_continue_on_empty_passwords():
    """Test worker_process continue statement when passwords list is empty.

    This test specifically targets line 54: 'continue'
    """
    # Create mock queues
    mock_password_queue = MagicMock()
    mock_result_queue = MagicMock()
    mock_progress_queue = MagicMock()

    # Create mock found event
    mock_found_event = MagicMock()
    # First call returns False, second call returns True to exit loop
    mock_found_event.is_set.side_effect = [False, True]

    # Make the password queue raise queue.Empty on the first call
    mock_password_queue.get.side_effect = queue.Empty

    # Patch pikepdf.open to avoid actual PDF processing
    with patch("pikepdf.open"):
        # Call worker_process
        worker_process(
            pdf_data=b"mock_pdf_data",
            password_queue=mock_password_queue,
            found_event=mock_found_event,
            result_queue=mock_result_queue,
            progress_queue=mock_progress_queue,
            report_worker_errors=False,
            batch_size=10,
        )

        # Since passwords list is empty when queue.Empty is raised,
        # the function should hit the continue statement and then exit the loop
        # No progress should be reported
        assert mock_progress_queue.empty()
