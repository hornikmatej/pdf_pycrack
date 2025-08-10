# Benchmarking

PDF-PyCrack includes a comprehensive benchmarking system to measure and optimize performance. This guide covers how to use the benchmarking tools, interpret results, and improve your cracking performance.

## Overview

The benchmarking system provides:

- **Consistent measurements** across different runs
- **Performance tracking** over time
- **Optimization guidance** for different scenarios
- **System comparison** capabilities

## Quick Start

### Running the Standard Benchmark

The easiest way to measure performance is using the standard benchmark:

```bash
# Run the default benchmark
uv run python benchmark/benchmark.py --standard
```

This runs a standardized test that:
- Uses a known test PDF
- Tests a controlled search space (110,000 passwords)
- Completes in 5-20 seconds
- Provides consistent results for comparison

### Custom Benchmarks

You can also run custom benchmarks with specific parameters:

```bash
# Quick test with numbers only
uv run python benchmark/benchmark.py --min-len 1 --max-len 3 --charset 0123456789

# Test with letters
uv run python benchmark/benchmark.py --pdf tests/test_pdfs/letters/ab.pdf --min-len 1 --max-len 2 --charset abcdefghijklmnopqrstuvwxyz

# Test with custom configuration
uv run python benchmark/benchmark.py --processes 4 --batch-size 200
```

## Understanding Benchmark Results

### Sample Output

When you run a benchmark, you'll see output like this:

```
============================================================
Starting benchmark
============================================================
PDF: tests/test_pdfs/numbers/100.pdf
Charset: 0123456789
Length range: 4-5
Search space: 110,000 passwords
Processes: 8
Batch size: 100
Description: Standard benchmark - numbers 4-5 length

Cracking PDF: 100%|████████████████| 110000/110000 [00:15<00:00, 7234.56pw/s]

✓ Benchmark completed (password not found as expected)
------------------------------------------------------------
Benchmark Results:
  Total passwords checked: 110,000
  Elapsed time: 15.21s
  CPU time: 0.15s
  Passwords per second: 7,235
  Efficiency: 98.5%
============================================================
Results saved to: benchmark/results/benchmark_20250810_142305.json
Results appended to: benchmark/results/benchmark_history.csv
```

### Key Metrics Explained

#### Passwords per Second (pw/s)
This is the primary performance metric:
- **Higher is better**
- Typical ranges:
  - **2,000-5,000 pw/s**: Laptop/older hardware
  - **5,000-15,000 pw/s**: Modern desktop
  - **15,000+ pw/s**: High-end workstation

#### Efficiency
Percentage of CPU time actually spent on cracking vs. overhead:
- **95-100%**: Excellent (minimal overhead)
- **85-95%**: Good (some overhead but acceptable)
- **<85%**: Poor (too much overhead, tune parameters)

#### CPU Time vs Elapsed Time
- **CPU time**: Actual processing time
- **Elapsed time**: Wall-clock time
- **Efficiency = (CPU time / Elapsed time) × 100**

## Benchmark Configuration

### Command Line Options

```bash
uv run python benchmark/benchmark.py [OPTIONS]

Options:
  --pdf PATH          Path to PDF file
  --min-len INT       Minimum password length
  --max-len INT       Maximum password length
  --charset STR       Character set to use
  --processes INT     Number of processes
  --batch-size INT    Batch size for workers
  --standard          Run standard benchmark configuration
```

### Standard Configuration

The standard benchmark uses:
- **PDF**: `tests/test_pdfs/numbers/100.pdf` (password: "100")
- **Charset**: Numbers only (`0123456789`)
- **Length**: 4-5 characters
- **Search space**: 110,000 passwords
- **Runtime**: 5-20 seconds (depending on hardware)

This configuration ensures:
✅ **Quick completion** for regular testing
✅ **Consistent results** across runs
✅ **Meaningful data** for optimization

## Performance Analysis

### Historical Tracking

All benchmark results are saved and can be tracked over time:

```bash
# View historical results
cat benchmark/results/benchmark_history.csv

# Plot performance trends (if you have plotting tools)
python -c "
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('benchmark/results/benchmark_history.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
plt.plot(df['timestamp'], df['passwords_per_second'])
plt.title('Performance Over Time')
plt.ylabel('Passwords per Second')
plt.show()
"
```

### Comparing Configurations

You can benchmark different configurations to find optimal settings:

```bash
# Test different process counts
for processes in 2 4 6 8; do
    echo "Testing $processes processes..."
    uv run python benchmark/benchmark.py --processes $processes --standard
done

# Test different batch sizes
for batch in 50 100 200 500; do
    echo "Testing batch size $batch..."
    uv run python benchmark/benchmark.py --batch-size $batch --standard
done
```

### System Comparison

Compare performance across different systems:

```bash
# Generate system fingerprint
echo "System: $(uname -a)" > system_benchmark.txt
echo "CPU: $(lscpu | grep 'Model name')" >> system_benchmark.txt
echo "Memory: $(free -h | grep Mem)" >> system_benchmark.txt

# Run benchmark
uv run python benchmark/benchmark.py --standard >> system_benchmark.txt
```

## Optimization Guide

### Finding Optimal Process Count

Too few processes underutilize CPU, too many create overhead:

```python
#!/usr/bin/env python3
"""Find optimal process count for your system."""

import subprocess
import json
import multiprocessing

def benchmark_processes():
    max_processes = multiprocessing.cpu_count()
    results = {}

    for processes in range(1, max_processes + 1):
        print(f"Testing {processes} processes...")

        cmd = [
            "uv", "run", "python", "benchmark/benchmark.py",
            "--processes", str(processes),
            "--min-len", "4", "--max-len", "4",  # Quick test
            "--charset", "0123456789"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        # Parse results (simplified - you'd want better parsing)
        if "Passwords per second:" in result.stdout:
            lines = result.stdout.split('\n')
            for line in lines:
                if "Passwords per second:" in line:
                    rate = int(line.split(':')[1].strip().replace(',', ''))
                    results[processes] = rate
                    break

    # Find optimal
    optimal = max(results.items(), key=lambda x: x[1])
    print(f"\nOptimal configuration: {optimal[0]} processes")
    print(f"Performance: {optimal[1]:,} passwords/second")

    return results

if __name__ == "__main__":
    results = benchmark_processes()
```

### Batch Size Optimization

Find the optimal batch size for your workload:

```python
def benchmark_batch_sizes():
    batch_sizes = [10, 25, 50, 100, 200, 500, 1000]
    results = {}

    for batch_size in batch_sizes:
        print(f"Testing batch size {batch_size}...")

        cmd = [
            "uv", "run", "python", "benchmark/benchmark.py",
            "--batch-size", str(batch_size),
            "--standard"
        ]

        # Run and parse results
        # (Implementation details omitted for brevity)

    return results
```

## Advanced Benchmarking

### Memory Usage Profiling

Monitor memory usage during benchmarks:

```python
import psutil
import time
import subprocess
import threading

class MemoryProfiler:
    def __init__(self):
        self.max_memory = 0
        self.monitoring = False

    def start_monitoring(self):
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor)
        self.monitor_thread.start()

    def stop_monitoring(self):
        self.monitoring = False
        self.monitor_thread.join()
        return self.max_memory

    def _monitor(self):
        while self.monitoring:
            memory = psutil.virtual_memory().used / (1024**3)  # GB
            self.max_memory = max(self.max_memory, memory)
            time.sleep(0.1)

def profile_memory_usage():
    profiler = MemoryProfiler()

    profiler.start_monitoring()

    # Run benchmark
    subprocess.run([
        "uv", "run", "python", "benchmark/benchmark.py", "--standard"
    ])

    max_memory = profiler.stop_monitoring()
    print(f"Peak memory usage: {max_memory:.2f} GB")
```

### CPU Utilization Analysis

Monitor CPU usage patterns:

```python
import psutil
import time
import matplotlib.pyplot as plt

def monitor_cpu_usage(duration=30):
    cpu_percentages = []
    timestamps = []

    start_time = time.time()
    while time.time() - start_time < duration:
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        cpu_percentages.append(cpu_percent)
        timestamps.append(time.time() - start_time)

    # Plot results
    plt.figure(figsize=(12, 6))
    for i, core_data in enumerate(zip(*cpu_percentages)):
        plt.plot(timestamps, core_data, label=f'Core {i}')

    plt.xlabel('Time (seconds)')
    plt.ylabel('CPU Usage (%)')
    plt.title('CPU Usage During Benchmark')
    plt.legend()
    plt.grid(True)
    plt.show()
```

## Performance Targets and Expectations

### Hardware Performance Guide

| Hardware Type | Expected Performance | Notes |
|---------------|---------------------|-------|
| **High-end Desktop** | 15,000-25,000 pw/s | 8+ cores, fast RAM |
| **Modern Laptop** | 8,000-15,000 pw/s | 4-8 cores, good cooling |
| **Older Desktop** | 3,000-8,000 pw/s | 2-4 cores, slower RAM |
| **Budget Laptop** | 1,000-3,000 pw/s | 2-4 cores, thermal limits |

### Optimization Targets

When optimizing, aim for:

1. **CPU Utilization**: 85-95% across all cores
2. **Memory Usage**: <50% of available RAM
3. **Efficiency**: >90% (minimal overhead)
4. **Scalability**: Near-linear improvement with core count

### Warning Signs

Watch out for these performance issues:

❌ **Low CPU utilization** (<70%)
- **Cause**: Too few processes or I/O bottleneck
- **Fix**: Increase process count, check disk speed

❌ **Poor efficiency** (<80%)
- **Cause**: Too many processes or small batch sizes
- **Fix**: Reduce processes, increase batch size

❌ **Memory pressure** (>90% RAM usage)
- **Cause**: Too many processes or large batches
- **Fix**: Reduce processes, smaller batches

❌ **Thermal throttling** (performance drops over time)
- **Cause**: CPU overheating
- **Fix**: Improve cooling, reduce processes

## Integration with Development

### Continuous Performance Monitoring

Set up automated benchmarking for development:

```bash
#!/bin/bash
# run_benchmark.sh - Run after code changes

echo "Running benchmark after changes..."
uv run python benchmark/benchmark.py --standard

# Check if performance regression occurred
LATEST_RESULT=$(tail -n 1 benchmark/results/benchmark_history.csv | cut -d',' -f6)
BASELINE=5000  # Your baseline performance

if (( $(echo "$LATEST_RESULT < $BASELINE" | bc -l) )); then
    echo "⚠️  Performance regression detected!"
    echo "Current: $LATEST_RESULT pw/s"
    echo "Baseline: $BASELINE pw/s"
    exit 1
else
    echo "✅ Performance maintained or improved"
    echo "Current: $LATEST_RESULT pw/s"
fi
```

### Pre-commit Hooks

Add benchmarking to your development workflow:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: performance-check
        name: Performance benchmark
        entry: ./run_benchmark.sh
        language: script
        pass_filenames: false
        stages: [manual]  # Only run when explicitly requested
```

## Benchmark Result Format

### JSON Output

Each benchmark run produces a JSON file with detailed results:

```json
{
  "timestamp": "2025-08-10T14:23:05.123456",
  "pdf_file": "tests/test_pdfs/numbers/100.pdf",
  "charset": "0123456789",
  "min_length": 4,
  "max_length": 5,
  "search_space": 110000,
  "processes": 8,
  "batch_size": 100,
  "total_passwords_checked": 110000,
  "elapsed_time": 15.21,
  "cpu_time": 0.15,
  "passwords_per_second": 7235,
  "efficiency": 98.5,
  "system_info": {
    "cpu_count": 8,
    "memory_gb": 16,
    "platform": "Linux-5.4.0-80-generic-x86_64"
  },
  "result_type": "PasswordNotFound",
  "description": "Standard benchmark - numbers 4-5 length"
}
```

### CSV Output

Historical data is maintained in CSV format for easy analysis:

```csv
timestamp,pdf_file,charset,min_length,max_length,passwords_per_second,efficiency,processes,batch_size
2025-08-10T14:23:05,tests/test_pdfs/numbers/100.pdf,0123456789,4,5,7235,98.5,8,100
2025-08-10T14:25:12,tests/test_pdfs/numbers/100.pdf,0123456789,4,5,7180,97.8,8,200
...
```

## Next Steps

- 🔧 **[Optimization Guide](optimization.md)**: Detailed performance optimization techniques
- ⚙️ **[Configuration](../user-guide/configuration.md)**: Configure for maximum performance
- 🛠️ **[Development](../development/contributing.md)**: Contribute performance improvements
- 📊 **Analyze Results**: Use the data to optimize your specific use case
