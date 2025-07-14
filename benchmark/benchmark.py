#!/usr/bin/env python3
"""
PDF Password Cracking Benchmark Tool

This script provides comprehensive benchmarking for the pdf-pycrack tool,
measuring password cracking speed in passwords per second (pw/s).
"""

import argparse
import csv
import json
import logging
import multiprocessing
import os
import time
from datetime import datetime
from typing import Any, Dict, Optional

from pdf_pycrack.core import crack_pdf_password
from pdf_pycrack.models.cracking_result import PasswordNotFound

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


class BenchmarkRunner:
    """Handles running and measuring password cracking benchmarks."""

    def __init__(self):
        # Save results in benchmark/results folder
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.output_dir = os.path.join(project_root, "benchmark", "results")
        os.makedirs(self.output_dir, exist_ok=True)

    def calculate_search_space(self, min_len: int, max_len: int, charset: str) -> int:
        """Calculate total number of passwords to check."""
        return sum(len(charset) ** length for length in range(min_len, max_len + 1))

    def run_benchmark(
        self,
        pdf_path: str,
        min_len: int,
        max_len: int,
        charset: str,
        num_processes: Optional[int] = None,
        batch_size: int = 100,
        description: str = "",
    ) -> Dict[str, Any]:
        """
        Run a single benchmark test.

        Args:
            pdf_path: Path to the PDF file
            min_len: Minimum password length
            max_len: Maximum password length
            charset: Character set to use
            num_processes: Number of CPU cores to use (default: all)
            batch_size: Batch size for worker processes
            description: Optional description for this benchmark

        Returns:
            Dictionary with benchmark results
        """
        if num_processes is None:
            num_processes = multiprocessing.cpu_count()

        search_space = self.calculate_search_space(min_len, max_len, charset)

        logging.info("=" * 60)
        logging.info("Starting benchmark")
        logging.info("=" * 60)
        logging.info(f"PDF: {pdf_path}")
        logging.info(f"Charset: {charset}")
        logging.info(f"Length range: {min_len}-{max_len}")
        logging.info(f"Search space: {search_space:,} passwords")
        logging.info(f"Processes: {num_processes}")
        logging.info(f"Batch size: {batch_size}")
        if description:
            logging.info(f"Description: {description}")

        start_time = time.time()
        start_cpu = time.process_time()

        result = crack_pdf_password(
            pdf_path,
            min_len=min_len,
            max_len=max_len,
            charset=charset,
            num_processes=num_processes,
            batch_size_arg=batch_size,
            report_worker_errors_arg=False,
        )

        end_time = time.time()
        end_cpu = time.process_time()

        elapsed_time = end_time - start_time
        cpu_time = end_cpu - start_cpu

        # Calculate performance metrics
        passwords_checked = getattr(result, "passwords_checked", 0)
        passwords_per_second = (
            passwords_checked / elapsed_time if elapsed_time > 0 else 0
        )

        # We expect PasswordNotFound since we're using wrong charset/length
        if isinstance(result, PasswordNotFound):
            logging.info("✓ Benchmark completed (password not found as expected)")
        else:
            logging.warning(f"⚠ Unexpected result: {type(result).__name__}")

        results = {
            "timestamp": datetime.now().isoformat(),
            "pdf_path": pdf_path,
            "min_len": min_len,
            "max_len": max_len,
            "charset": charset,
            "charset_length": len(charset),
            "search_space": search_space,
            "num_processes": num_processes,
            "batch_size": batch_size,
            "elapsed_time": elapsed_time,
            "cpu_time": cpu_time,
            "passwords_checked": passwords_checked,
            "passwords_per_second": passwords_per_second,
            "description": description,
            "result_type": type(result).__name__,
        }

        logging.info("-" * 60)
        logging.info("Benchmark Results:")
        logging.info(f"  Total passwords checked: {passwords_checked:,}")
        logging.info(f"  Elapsed time: {elapsed_time:.2f}s")
        logging.info(f"  CPU time: {cpu_time:.2f}s")
        logging.info(f"  Passwords per second: {passwords_per_second:,.0f}")
        logging.info(f"  Efficiency: {(passwords_checked/search_space)*100:.1f}%")
        logging.info("=" * 60)

        return results

    def save_results(self, results: Dict[str, Any], filename: Optional[str] = None):
        """Save benchmark results to JSON and CSV files."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_{timestamp}"

        # Save as JSON
        json_path = os.path.join(self.output_dir, f"{filename}.json")
        with open(json_path, "w") as f:
            json.dump(results, f, indent=2)
        logging.info(f"Results saved to: {json_path}")

        # Save as CSV (append mode for tracking)
        csv_path = os.path.join(self.output_dir, "benchmark_history.csv")
        file_exists = os.path.exists(csv_path)

        with open(csv_path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(results)
        logging.info(f"Results appended to: {csv_path}")

    def run_standard_benchmark(self) -> Dict[str, Any]:
        """Run the standard benchmark configuration."""
        # Use a PDF with known encryption but wrong search parameters
        pdf_path = "tests/test_pdfs/numbers/100.pdf"

        # Configure for ~15-30 second runtime at 4k/s
        # Numbers 4-5: 9 + 90 + 900 + 9000 + 90000 = 99,999 passwords
        min_len = 4
        max_len = 5
        charset = "0123456789"

        results = self.run_benchmark(
            pdf_path=pdf_path,
            min_len=min_len,
            max_len=max_len,
            charset=charset,
            description="Standard benchmark - numbers 4-5 length",
        )

        return results


def main():
    """Main entry point for the benchmark tool."""
    parser = argparse.ArgumentParser(description="PDF Password Cracking Benchmark")
    parser.add_argument(
        "--pdf",
        type=str,
        default="tests/test_pdfs/numbers/100.pdf",
        help="Path to PDF file for benchmarking",
    )
    parser.add_argument(
        "--min-len", type=int, default=4, help="Minimum password length"
    )
    parser.add_argument(
        "--max-len", type=int, default=5, help="Maximum password length"
    )
    parser.add_argument(
        "--charset", type=str, default="0123456789", help="Character set to use"
    )
    parser.add_argument(
        "--processes",
        type=int,
        default=None,
        help="Number of processes (default: CPU count)",
    )
    parser.add_argument(
        "--batch-size", type=int, default=100, help="Batch size for workers"
    )
    parser.add_argument(
        "--standard", action="store_true", help="Run standard benchmark configuration"
    )

    args = parser.parse_args()

    runner = BenchmarkRunner()

    if args.standard:
        results = runner.run_standard_benchmark()
    else:
        results = runner.run_benchmark(
            pdf_path=args.pdf,
            min_len=args.min_len,
            max_len=args.max_len,
            charset=args.charset,
            num_processes=args.processes,
            batch_size=args.batch_size,
        )

    runner.save_results(results)


if __name__ == "__main__":
    main()
