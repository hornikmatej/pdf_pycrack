"""Test to cover line 51 in worker.py."""

import queue
from unittest.mock import MagicMock, patch

from pdf_pycrack.worker import worker_process


def test_worker_process_empty_passwords_on_queue_empty():
    """Test worker_process when queue.Empty is raised and passwords list is empty.

    This test specifically targets line 51: 'if not passwords: return'
    """
    # Create mock queues
    mock_password_queue = MagicMock()
    mock_result_queue = MagicMock()
    mock_progress_queue = MagicMock()

    # Create mock found event
    mock_found_event = MagicMock()
    mock_found_event.is_set.return_value = False  # Keep looping

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
        # the function should return immediately without processing
        # and without reporting any progress
        assert mock_progress_queue.empty()
