# PDF Password Cracking Benchmark

A comprehensive benchmarking tool for measuring PDF password cracking performance in passwords per second (pw/s).

## Overview

This benchmark tool is designed to provide consistent, repeatable measurements of the pdf-pycrack tool's performance. It uses controlled test parameters to ensure fair comparisons between different algorithm implementations.

## Quick Start

```bash
# Run the standard benchmark
uv run python benchmark/benchmark.py --standard

# Run a quick test
uv run python benchmark/benchmark.py --min-len 1 --max-len 2 --charset 0123456789

# Run with custom parameters
uv run python benchmark/benchmark.py --pdf tests/test_pdfs/letters/ab.pdf --min-len 1 --max-len 3 --charset abcdefghijklmnopqrstuvwxyz
```

## Standard Benchmark Configuration

The standard benchmark is configured for a 5-10 second runtime at current performance levels:
- **PDF**: `tests/test_pdfs/numbers/100.pdf` (encrypted with password "100")
- **Charset**: Numbers only (`0123456789`)
- **Length range**: 4-5 characters
- **Search space**: 99,999 passwords (9 + 90 + 900 + 9000 + 90000)
- **Expected runtime**: 5-10 seconds at 4k-10k pw/s

This configuration ensures the benchmark completes quickly while providing enough data for accurate measurements.

## Usage

### Command Line Options

```bash
uv run python benchmark/benchmark.py [OPTIONS]

Options:
  --pdf PATH          Path to PDF file (default: tests/test_pdfs/numbers/100.pdf)
  --min-len INT       Minimum password length (default: 4)
  --max-len INT       Maximum password length (default: 5)
  --charset STR       Character set to use (default: 0123456789)
  --processes INT     Number of processes (default: CPU count)
  --batch-size INT    Batch size for workers (default: 100)
  --standard          Run standard benchmark configuration
```

### Examples

```bash
# Standard benchmark
uv run python benchmark/benchmark.py --standard

# Quick test with letters
uv run python benchmark/benchmark.py --pdf tests/test_pdfs/letters/ab.pdf --min-len 1 --max-len 2 --charset abcdefghijklmnopqrstuvwxyz

# Test with mixed charset
uv run python benchmark/benchmark.py --min-len 2 --max-len 3 --charset 0123456789abcdefghijklmnopqrstuvwxyz

# Test with specific process count
uv run python benchmark/benchmark.py --processes 4 --batch-size 1000
```

## Results

Results are automatically saved in the `benchmark/` directory:

- **Individual runs**: `benchmark/benchmark_YYYYMMDD_HHMMSS.json`
- **Historical data**: `benchmark/benchmark_history.csv`

### Sample Output

Results are saved in JSON format to the `benchmark/results/` directory, and a summary is printed to the console:
```
2025-07-14 21:16:41,526 - INFO - ============================================================
2025-07-14 21:16:41,526 - INFO - Starting benchmark
2025-07-14 21:16:41,526 - INFO - ============================================================
2025-07-14 21:16:41,526 - INFO - PDF: tests/test_pdfs/numbers/100.pdf
2025-07-14 21:16:41,526 - INFO - Charset: 0123456789
2025-07-14 21:16:41,526 - INFO - Length range: 4-5
2025-07-14 21:16:41,527 - INFO - Search space: 110,000 passwords
2025-07-14 21:16:41,527 - INFO - Processes: 14
2025-07-14 21:16:41,527 - INFO - Batch size: 100
2025-07-14 21:16:41,527 - INFO - Description: Standard benchmark - numbers 4-5 length
Cracking PDF: 100%|█████████████████████████████████████████████████████████████████████████████████| 110000/110000 [00:20<00:00, 5356.31pw/s]
2025-07-14 21:17:02,151 - INFO - ✓ Benchmark completed (password not found as expected)
2025-07-14 21:17:02,152 - INFO - ------------------------------------------------------------
2025-07-14 21:17:02,152 - INFO - Benchmark Results:
2025-07-14 21:17:02,152 - INFO -   Total passwords checked: 110,000
2025-07-14 21:17:02,152 - INFO -   Elapsed time: 20.62s
2025-07-14 21:17:02,152 - INFO -   CPU time: 0.18s
2025-07-14 21:17:02,152 - INFO -   Passwords per second: 5,333
2025-07-14 21:17:02,152 - INFO -   Efficiency: 100.0%
2025-07-14 21:17:02,152 - INFO - ============================================================
2025-07-14 21:17:02,152 - INFO - Results saved to: pdf_pycrack/benchmark/results/benchmark_20250714_211702.json
2025-07-14 21:17:02,152 - INFO - Results appended to: pdf_pycrack/benchmark/results/benchmark_history.csv
```

## Integration with Development

The benchmark is designed to be run after each change to the core parallel algorithm:

```bash
# Before making changes
uv run python benchmark/benchmark.py --standard

# Make your changes to src/pdf_pycrack/core.py

# After changes
uv run python benchmark/benchmark.py --standard

# Compare results in benchmark_history.csv
```

## Performance Targets

- **Current baseline**: ~4,000 pw/s
- **Target improvement**: 2-5x speedup through algorithm optimization
- **Measurement accuracy**: ±5% due to system variability

## Technical Details

The benchmark uses a PDF encrypted with a known password but searches with incorrect parameters (wrong charset/length) to ensure the entire search space is processed. This provides consistent measurements regardless of when the password is actually found.
