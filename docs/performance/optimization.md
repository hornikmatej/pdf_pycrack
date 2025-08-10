# Performance Optimization

PDF-PyCrack offers numerous optimization strategies to maximize cracking speed and efficiency. This guide covers advanced techniques to get the best performance from your system.

## Understanding Performance Factors

Performance in PDF password cracking depends on several key factors:

- **CPU cores and threads**
- **Memory bandwidth and size**
- **Search space complexity**
- **Algorithm efficiency**
- **I/O operations**

## Hardware Optimization

### CPU Configuration

#### Core Count and Hyperthreading

```bash
# Check your system capabilities
nproc  # Linux
sysctl -n hw.ncpu  # macOS

# Use all available cores (default behavior)
pdf-pycrack file.pdf

# Manually specify core count
pdf-pycrack file.pdf --cores 8

# Leave cores for other tasks
pdf-pycrack file.pdf --cores $(($(nproc) - 2))
```

**Hyperthreading Considerations:**
- Physical cores usually perform better than logical cores
- For CPU-intensive cracking, use physical core count
- For mixed workloads, logical cores may help

```python
import psutil

def optimal_core_count():
    """Calculate optimal core count for cracking."""
    physical_cores = psutil.cpu_count(logical=False)
    logical_cores = psutil.cpu_count(logical=True)

    # Use physical cores for maximum performance
    # or logical cores if system load is low
    system_load = psutil.cpu_percent(interval=1)

    if system_load < 30:
        return logical_cores - 1  # Leave one for system
    else:
        return physical_cores
```

#### CPU Affinity (Linux)

```bash
# Pin to specific cores for consistent performance
taskset -c 0-7 pdf-pycrack file.pdf --cores 8

# Use only NUMA node 0 cores
numactl --cpunodebind=0 --membind=0 pdf-pycrack file.pdf
```

### Memory Optimization

#### Memory Usage Patterns

```python
def calculate_memory_requirements(min_len: int, max_len: int, charset_size: int,
                                num_processes: int, batch_size: int) -> dict:
    """Estimate memory requirements for cracking job."""

    # Base memory per process (MB)
    base_memory = 50

    # Memory per password in batch (bytes)
    password_memory = max_len * 2  # Unicode strings

    # Batch memory per process
    batch_memory = (batch_size * password_memory) / (1024 * 1024)

    # Total per process
    process_memory = base_memory + batch_memory

    # System total
    total_memory = process_memory * num_processes

    return {
        "per_process_mb": round(process_memory, 1),
        "total_mb": round(total_memory, 1),
        "recommended_batch_size": max(10, min(1000, batch_size)),
        "warnings": []
    }

# Example usage
requirements = calculate_memory_requirements(
    min_len=4, max_len=8, charset_size=62,
    num_processes=8, batch_size=100
)

print(f"Estimated memory usage: {requirements['total_mb']} MB")
```

#### Batch Size Tuning

```bash
# Small batch size - lower memory, more overhead
pdf-pycrack file.pdf --batch-size 50

# Large batch size - higher memory, less overhead
pdf-pycrack file.pdf --batch-size 500

# Adaptive batch sizing based on available memory
pdf-pycrack file.pdf --batch-size auto
```

**Batch Size Guidelines:**
- **Low memory systems:** 10-50 passwords per batch
- **Normal systems:** 100-200 passwords per batch
- **High-end systems:** 500-1000 passwords per batch
- **Memory-rich systems:** 1000+ passwords per batch

### Storage and I/O

#### Temporary File Optimization

```bash
# Use RAM disk for temporary files (Linux)
sudo mount -t tmpfs -o size=1G tmpfs /tmp/pdf-crack
export TMPDIR=/tmp/pdf-crack
pdf-pycrack file.pdf

# Use SSD for better I/O performance
pdf-pycrack file.pdf --temp-dir /path/to/ssd/temp
```

## Algorithm Optimization

### Search Space Reduction

#### Character Set Optimization

```bash
# Most efficient - numbers only
pdf-pycrack file.pdf --charset-numbers --min-len 4 --max-len 6

# Still efficient - lowercase letters
pdf-pycrack file.pdf --charset-lowercase --min-len 4 --max-len 6

# More complex - mixed case
pdf-pycrack file.pdf --charset-letters --min-len 4 --max-len 6

# Least efficient - all characters
pdf-pycrack file.pdf --charset-all --min-len 4 --max-len 6
```

**Character Set Performance Impact:**
- Numbers (10 chars): ~10^6 combinations for 6 chars
- Lowercase (26 chars): ~26^6 = 308M combinations
- Letters (52 chars): ~52^6 = 19.7B combinations
- All chars (94 chars): ~94^6 = 689B combinations

#### Smart Length Progression

```python
def progressive_crack_strategy(pdf_path: str, max_length: int = 8):
    """Try shorter lengths first for faster results."""

    for length in range(4, max_length + 1):
        print(f"Trying length {length}...")

        result = crack_pdf_password(
            pdf_path,
            min_len=length,
            max_len=length,
            charset="0123456789",  # Start with numbers
            num_processes=os.cpu_count()
        )

        if isinstance(result, PasswordFound):
            return result

        # Expand character set if numbers fail
        result = crack_pdf_password(
            pdf_path,
            min_len=length,
            max_len=length,
            charset="0123456789abcdefghijklmnopqrstuvwxyz",
            num_processes=os.cpu_count()
        )

        if isinstance(result, PasswordFound):
            return result

    return None
```

### Dictionary Attacks

#### Common Password Lists

```python
import requests
from pathlib import Path

def download_common_passwords():
    """Download common password lists for dictionary attacks."""

    lists = {
        "rockyou": "https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt",
        "common_passwords": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-100000.txt"
    }

    for name, url in lists.items():
        file_path = Path(f"dictionaries/{name}.txt")
        file_path.parent.mkdir(exist_ok=True)

        if not file_path.exists():
            print(f"Downloading {name}...")
            response = requests.get(url)
            file_path.write_text(response.text)

    return list(Path("dictionaries").glob("*.txt"))

def dictionary_attack(pdf_path: str, dictionary_files: list):
    """Perform dictionary attack before brute force."""

    for dict_file in dictionary_files:
        print(f"Trying dictionary: {dict_file.name}")

        with open(dict_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, password in enumerate(f, 1):
                password = password.strip()

                if not password:
                    continue

                # Test password
                try:
                    with pikepdf.open(pdf_path, password=password):
                        return PasswordFound(password=password, attempts=line_num)
                except pikepdf.PasswordError:
                    continue
                except Exception as e:
                    print(f"Error testing password: {e}")
                    continue

                # Progress every 10,000 passwords
                if line_num % 10000 == 0:
                    print(f"Tested {line_num:,} passwords...")

    return None
```

## Parallel Processing Optimization

### Process vs Thread Comparison

```python
import time
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def performance_comparison(pdf_path: str, password_batch: list):
    """Compare different parallelization strategies."""

    # Single threaded baseline
    start = time.time()
    single_threaded_result = test_passwords_sequential(pdf_path, password_batch)
    single_time = time.time() - start

    # Multi-processing
    start = time.time()
    with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
        mp_result = test_passwords_parallel(executor, pdf_path, password_batch)
    mp_time = time.time() - start

    # Multi-threading (limited by GIL for CPU-bound tasks)
    start = time.time()
    with ThreadPoolExecutor(max_workers=mp.cpu_count()) as executor:
        mt_result = test_passwords_parallel(executor, pdf_path, password_batch)
    mt_time = time.time() - start

    print(f"Single-threaded: {single_time:.2f}s")
    print(f"Multi-processing: {mp_time:.2f}s ({single_time/mp_time:.1f}x speedup)")
    print(f"Multi-threading: {mt_time:.2f}s ({single_time/mt_time:.1f}x speedup)")
```

### NUMA Awareness

```bash
# Check NUMA topology
numactl --hardware

# Bind to specific NUMA node
numactl --cpunodebind=0 --membind=0 pdf-pycrack file.pdf --cores 8

# Interleave memory across nodes
numactl --interleave=all pdf-pycrack file.pdf
```

## System-Level Optimizations

### Priority and Scheduling

```bash
# Increase process priority (Linux)
nice -n -10 pdf-pycrack file.pdf

# Real-time scheduling (use with caution)
sudo chrt -f 50 pdf-pycrack file.pdf

# CPU governor optimization
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

### Power Management

```bash
# Disable power saving during cracking (Linux)
sudo cpupower frequency-set --governor performance

# Disable CPU idle states
sudo cpupower idle-set --disable-by-latency 0

# Re-enable after cracking
sudo cpupower frequency-set --governor powersave
```

## Monitoring and Profiling

### Performance Monitoring

```python
import psutil
import time
from dataclasses import dataclass
from typing import List

@dataclass
class PerformanceMetrics:
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_mb: float
    passwords_per_second: float
    total_tested: int

class PerformanceMonitor:
    def __init__(self):
        self.metrics: List[PerformanceMetrics] = []
        self.start_time = time.time()
        self.last_password_count = 0

    def record_metrics(self, passwords_tested: int):
        """Record current system performance metrics."""
        now = time.time()

        # Calculate passwords per second
        time_delta = now - (self.metrics[-1].timestamp if self.metrics else self.start_time)
        password_delta = passwords_tested - self.last_password_count
        pps = password_delta / time_delta if time_delta > 0 else 0

        # System metrics
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory()

        metric = PerformanceMetrics(
            timestamp=now,
            cpu_percent=cpu,
            memory_percent=memory.percent,
            memory_mb=memory.used / (1024 * 1024),
            passwords_per_second=pps,
            total_tested=passwords_tested
        )

        self.metrics.append(metric)
        self.last_password_count = passwords_tested

    def get_summary(self) -> dict:
        """Get performance summary statistics."""
        if not self.metrics:
            return {}

        pps_values = [m.passwords_per_second for m in self.metrics[1:]]  # Skip first
        cpu_values = [m.cpu_percent for m in self.metrics]
        memory_values = [m.memory_mb for m in self.metrics]

        return {
            "duration_seconds": self.metrics[-1].timestamp - self.start_time,
            "total_passwords_tested": self.metrics[-1].total_tested,
            "avg_passwords_per_second": sum(pps_values) / len(pps_values) if pps_values else 0,
            "max_passwords_per_second": max(pps_values) if pps_values else 0,
            "avg_cpu_percent": sum(cpu_values) / len(cpu_values),
            "max_memory_mb": max(memory_values),
            "efficiency_score": self._calculate_efficiency()
        }

    def _calculate_efficiency(self) -> float:
        """Calculate efficiency score (passwords per second per CPU core)."""
        summary = self.get_summary()
        avg_pps = summary.get("avg_passwords_per_second", 0)
        cpu_cores = psutil.cpu_count()
        return avg_pps / cpu_cores if cpu_cores > 0 else 0
```

### Profiling Code

```python
import cProfile
import pstats
from pstats import SortKey

def profile_cracking_session(pdf_path: str, **kwargs):
    """Profile a cracking session to identify bottlenecks."""

    profiler = cProfile.Profile()
    profiler.enable()

    try:
        result = crack_pdf_password(pdf_path, **kwargs)
    finally:
        profiler.disable()

    # Analyze results
    stats = pstats.Stats(profiler)
    stats.sort_stats(SortKey.CUMULATIVE)

    print("Top 10 time-consuming functions:")
    stats.print_stats(10)

    print("\nCalling relationships:")
    stats.print_callers(5)

    return result
```

## Optimization Strategies by Use Case

### Quick Tests (Development)

```bash
# Fast iteration for testing
pdf-pycrack file.pdf --min-len 3 --max-len 4 --charset-numbers --cores 2
```

### Production Cracking

```bash
# Maximum performance configuration
pdf-pycrack file.pdf \
  --min-len 6 --max-len 8 \
  --charset-letters --charset-numbers \
  --cores $(nproc) \
  --batch-size 200 \
  --worker-errors
```

### Memory-Constrained Systems

```bash
# Low memory configuration
pdf-pycrack file.pdf \
  --cores 2 \
  --batch-size 25 \
  --min-len 4 --max-len 6 \
  --charset-numbers
```

### High-Performance Systems

```bash
# Maximum throughput configuration
pdf-pycrack file.pdf \
  --cores $(nproc) \
  --batch-size 1000 \
  --min-len 4 --max-len 10 \
  --charset-all
```

## Benchmarking Results

### Hardware Performance Scaling

| CPU Cores | Memory | Passwords/Second | Efficiency |
|-----------|--------|------------------|------------|
| 4         | 8GB    | 45,000          | 11,250     |
| 8         | 16GB   | 85,000          | 10,625     |
| 16        | 32GB   | 160,000         | 10,000     |
| 32        | 64GB   | 300,000         | 9,375      |

### Character Set Impact

| Character Set | Size | 6-char Search Space | Est. Time (8 cores) |
|---------------|------|-------------------|---------------------|
| Numbers       | 10   | 1M               | 12 seconds          |
| Lowercase     | 26   | 309M             | 1 hour              |
| Letters       | 52   | 19.7B            | 2.5 days            |
| All chars     | 94   | 689B             | 3 months            |

## Best Practices Summary

### 🚀 Performance Tips

1. **Start with smaller search spaces** and expand gradually
2. **Use dictionary attacks** before brute force
3. **Match core count to physical cores** for CPU-intensive work
4. **Optimize batch size** based on available memory
5. **Monitor system resources** during operation
6. **Use SSD storage** for temporary files
7. **Set CPU governor to performance** mode
8. **Consider NUMA topology** on multi-socket systems

### 📊 Monitoring

1. **Track passwords per second** for performance metrics
2. **Monitor memory usage** to prevent swapping
3. **Watch CPU utilization** for bottleneck identification
4. **Profile periodically** to find optimization opportunities

### ⚡ Hardware Recommendations

1. **High core count CPUs** for better parallel processing
2. **Fast RAM** (DDR4-3200+ or DDR5) for memory-intensive operations
3. **SSD storage** for temporary files and OS
4. **Adequate cooling** to maintain boost clocks
5. **Multiple NUMA nodes** can help with very large systems

Remember: The best optimization strategy depends on your specific hardware, PDF complexity, and time constraints! 🎯
