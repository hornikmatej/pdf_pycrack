# Configuration

PDF-PyCrack offers extensive configuration options to optimize performance and customize behavior for different scenarios. This guide covers all configuration aspects, from basic parameter tuning to advanced optimization strategies.

## Configuration Methods

PDF-PyCrack can be configured through:

1. **Command-line arguments** (CLI usage)
2. **Function parameters** (Python library)
3. **Environment variables** (system-wide defaults)
4. **Configuration files** (planned for future versions)

## Core Configuration Parameters

### Password Generation Settings

#### Length Range

Controls the range of password lengths to test:

=== "CLI"
    ```bash
    pdf-pycrack file.pdf --min_len 4 --max_len 8
    ```

=== "Python"
    ```python
    crack_pdf_password("file.pdf", min_len=4, max_len=8)
    ```

**Guidelines:**
- Start with shorter lengths (4-6) for faster results
- Each additional character exponentially increases search time
- Consider the context: corporate passwords vs. personal files

#### Character Set Configuration

Define which characters to include in password generation:

=== "CLI"
    ```bash
    # Individual sets
    pdf-pycrack file.pdf --charset-numbers
    pdf-pycrack file.pdf --charset-letters
    pdf-pycrack file.pdf --charset-special

    # Combined sets
    pdf-pycrack file.pdf --charset-numbers --charset-letters

    # Custom set
    pdf-pycrack file.pdf --charset-custom "abcdef123456"
    ```

=== "Python"
    ```python
    # Predefined character sets
    NUMBERS = "0123456789"
    LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    SPECIAL = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    # Use individual or combined sets
    crack_pdf_password("file.pdf", charset=NUMBERS)
    crack_pdf_password("file.pdf", charset=NUMBERS + LETTERS)
    crack_pdf_password("file.pdf", charset="customcharacters")
    ```

### Performance Configuration

#### CPU Core Usage

Control how many CPU cores to use for parallel processing:

=== "CLI"
    ```bash
    # Use all available cores (default)
    pdf-pycrack file.pdf

    # Use specific number
    pdf-pycrack file.pdf --cores 4

    # Use most cores but leave some for system
    pdf-pycrack file.pdf --cores $(($(nproc) - 2))
    ```

=== "Python"
    ```python
    import multiprocessing

    # Use all cores
    crack_pdf_password("file.pdf")

    # Use specific number
    crack_pdf_password("file.pdf", num_processes=4)

    # Use N-2 cores
    cores = multiprocessing.cpu_count() - 2
    crack_pdf_password("file.pdf", num_processes=cores)
    ```

**Recommendations:**
- **Desktop use**: Leave 1-2 cores for system responsiveness
- **Server use**: Can use all cores if dedicated to cracking
- **Laptop use**: Consider thermal throttling, use 50-75% of cores

#### Batch Size Optimization

Controls how many passwords each worker tests before reporting progress:

=== "CLI"
    ```bash
    # Default (balanced)
    pdf-pycrack file.pdf --batch_size 100

    # More frequent updates (slightly slower)
    pdf-pycrack file.pdf --batch_size 50

    # Less frequent updates (slightly faster)
    pdf-pycrack file.pdf --batch_size 500
    ```

=== "Python"
    ```python
    # Adjust batch size based on your needs
    crack_pdf_password("file.pdf", batch_size_arg=100)
    ```

**Guidelines:**
- **Small batches (10-50)**: More responsive progress, slightly slower
- **Medium batches (100-200)**: Good balance (default)
- **Large batches (500-1000)**: Less responsive, slightly faster

## Environment Variables

Set system-wide defaults using environment variables:

```bash
# Set default number of cores
export PDF_PYCRACK_CORES=6

# Set default batch size
export PDF_PYCRACK_BATCH_SIZE=200

# Set default character set
export PDF_PYCRACK_CHARSET="0123456789abcdef"

# Then use with defaults
pdf-pycrack file.pdf
```

!!! note "Environment Variables"
    Environment variable support is planned for future versions. Currently, configuration is done through command-line arguments or function parameters.

## Optimization Strategies

### Performance Optimization

#### 1. System Resource Optimization

```python
import psutil
import multiprocessing

def get_optimal_config():
    """Calculate optimal configuration based on system resources."""

    # CPU configuration
    cpu_count = multiprocessing.cpu_count()
    available_memory = psutil.virtual_memory().available / (1024**3)  # GB

    # Leave some cores for system
    if cpu_count >= 8:
        optimal_cores = cpu_count - 2
    elif cpu_count >= 4:
        optimal_cores = cpu_count - 1
    else:
        optimal_cores = cpu_count

    # Adjust batch size based on memory
    if available_memory >= 16:
        batch_size = 1000
    elif available_memory >= 8:
        batch_size = 500
    else:
        batch_size = 100

    return {
        "num_processes": optimal_cores,
        "batch_size_arg": batch_size
    }

# Use optimal configuration
config = get_optimal_config()
result = crack_pdf_password("file.pdf", **config)
```

#### 2. Search Space Optimization

```python
def progressive_search(pdf_path: str):
    """Implement a progressive search strategy."""

    strategies = [
        # Quick wins first
        {"charset": "0123456789", "min_len": 4, "max_len": 6},
        {"charset": "abcdefghijklmnopqrstuvwxyz", "min_len": 4, "max_len": 6},

        # Expand character set
        {"charset": "0123456789abcdefghijklmnopqrstuvwxyz", "min_len": 4, "max_len": 6},

        # Expand length range
        {"charset": "0123456789abcdefghijklmnopqrstuvwxyz", "min_len": 7, "max_len": 8},

        # Full search (last resort)
        {
            "charset": "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()",
            "min_len": 4,
            "max_len": 6
        }
    ]

    for i, strategy in enumerate(strategies, 1):
        print(f"Strategy {i}: Testing {len(strategy['charset'])} chars, "
              f"length {strategy['min_len']}-{strategy['max_len']}")

        result = crack_pdf_password(pdf_path, **strategy)

        if hasattr(result, 'password'):  # Password found
            return result

    return None  # All strategies failed
```

### Memory Optimization

#### Monitor and Control Memory Usage

```python
import psutil
import os

class MemoryMonitor:
    def __init__(self, max_memory_gb=4):
        self.max_memory = max_memory_gb * 1024 * 1024 * 1024  # Convert to bytes
        self.process = psutil.Process(os.getpid())

    def check_memory(self):
        """Check if memory usage is within limits."""
        current_memory = self.process.memory_info().rss
        return current_memory < self.max_memory

    def get_memory_usage_mb(self):
        """Get current memory usage in MB."""
        return self.process.memory_info().rss / (1024 * 1024)

def memory_aware_crack(pdf_path: str, max_memory_gb=4):
    """Crack password with memory monitoring."""

    monitor = MemoryMonitor(max_memory_gb)

    # Start with conservative settings
    config = {
        "num_processes": 2,
        "batch_size_arg": 100
    }

    print(f"Starting with {config['num_processes']} processes")

    result = crack_pdf_password(pdf_path, **config)

    print(f"Peak memory usage: {monitor.get_memory_usage_mb():.1f} MB")

    return result
```

## Configuration Profiles

### Pre-defined Profiles for Common Scenarios

#### Desktop Profile (Default)

```python
DESKTOP_PROFILE = {
    "num_processes": multiprocessing.cpu_count() - 1,
    "batch_size_arg": 100,
    "report_worker_errors_arg": False
}
```

#### High-Performance Profile

```python
HIGH_PERFORMANCE_PROFILE = {
    "num_processes": multiprocessing.cpu_count(),
    "batch_size_arg": 500,
    "report_worker_errors_arg": False
}
```

#### Conservative Profile

```python
CONSERVATIVE_PROFILE = {
    "num_processes": max(1, multiprocessing.cpu_count() // 2),
    "batch_size_arg": 50,
    "report_worker_errors_arg": True
}
```

#### Debugging Profile

```python
DEBUG_PROFILE = {
    "num_processes": 1,
    "batch_size_arg": 10,
    "report_worker_errors_arg": True
}
```

### Using Profiles

```python
def crack_with_profile(pdf_path: str, profile_name: str = "desktop"):
    """Crack PDF using predefined profiles."""

    profiles = {
        "desktop": DESKTOP_PROFILE,
        "performance": HIGH_PERFORMANCE_PROFILE,
        "conservative": CONSERVATIVE_PROFILE,
        "debug": DEBUG_PROFILE
    }

    if profile_name not in profiles:
        raise ValueError(f"Unknown profile: {profile_name}")

    config = profiles[profile_name]
    return crack_pdf_password(pdf_path, **config)

# Usage
result = crack_with_profile("file.pdf", "performance")
```

## Platform-Specific Configuration

### Windows Configuration

```python
import platform

def windows_config():
    """Optimized configuration for Windows."""
    if platform.system() == "Windows":
        return {
            "num_processes": multiprocessing.cpu_count() - 1,
            "batch_size_arg": 200,
            # Windows handles process creation differently
        }
    return {}
```

### macOS Configuration

```python
def macos_config():
    """Optimized configuration for macOS."""
    if platform.system() == "Darwin":
        return {
            "num_processes": multiprocessing.cpu_count() - 1,
            "batch_size_arg": 150,
            # Account for macOS process overhead
        }
    return {}
```

### Linux Configuration

```python
def linux_config():
    """Optimized configuration for Linux."""
    if platform.system() == "Linux":
        return {
            "num_processes": multiprocessing.cpu_count(),
            "batch_size_arg": 300,
            # Linux generally has better multiprocessing performance
        }
    return {}
```

## Configuration Validation

### Parameter Validation

```python
def validate_config(**kwargs):
    """Validate configuration parameters."""

    errors = []

    # Validate num_processes
    if "num_processes" in kwargs:
        cores = kwargs["num_processes"]
        max_cores = multiprocessing.cpu_count()
        if cores < 1 or cores > max_cores:
            errors.append(f"num_processes must be 1-{max_cores}, got {cores}")

    # Validate batch_size_arg
    if "batch_size_arg" in kwargs:
        batch_size = kwargs["batch_size_arg"]
        if batch_size < 1 or batch_size > 10000:
            errors.append(f"batch_size_arg must be 1-10000, got {batch_size}")

    # Validate length range
    min_len = kwargs.get("min_len", 1)
    max_len = kwargs.get("max_len", 50)
    if min_len > max_len:
        errors.append(f"min_len ({min_len}) cannot be greater than max_len ({max_len})")

    # Validate charset
    if "charset" in kwargs:
        charset = kwargs["charset"]
        if len(charset) == 0:
            errors.append("charset cannot be empty")
        if len(set(charset)) != len(charset):
            errors.append("charset contains duplicate characters")

    if errors:
        raise ValueError("Configuration errors: " + "; ".join(errors))

    return True

# Usage
try:
    config = {"num_processes": 16, "min_len": 4, "max_len": 8}
    validate_config(**config)
    result = crack_pdf_password("file.pdf", **config)
except ValueError as e:
    print(f"Configuration error: {e}")
```

## Performance Tuning Guide

### Benchmark Your System

```python
import time

def benchmark_configuration(pdf_path: str):
    """Benchmark different configurations to find optimal settings."""

    test_configs = [
        {"num_processes": 1, "batch_size_arg": 100},
        {"num_processes": 2, "batch_size_arg": 100},
        {"num_processes": 4, "batch_size_arg": 100},
        {"num_processes": 4, "batch_size_arg": 50},
        {"num_processes": 4, "batch_size_arg": 200},
    ]

    results = []

    for config in test_configs:
        print(f"Testing: {config}")

        start_time = time.time()
        result = crack_pdf_password(
            pdf_path,
            min_len=4,
            max_len=4,  # Short test
            charset="0123456789",
            **config
        )
        duration = time.time() - start_time

        rate = getattr(result, "rate", 0)
        results.append({
            "config": config,
            "duration": duration,
            "rate": rate
        })

        print(f"  Rate: {rate:,.0f} passwords/second")

    # Find best configuration
    best = max(results, key=lambda x: x["rate"])
    print(f"\nBest configuration: {best['config']}")
    print(f"Best rate: {best['rate']:,.0f} passwords/second")

    return best["config"]
```

## Troubleshooting Configuration Issues

### Common Problems and Solutions

#### Poor Performance

```python
def diagnose_performance():
    """Diagnose and suggest fixes for performance issues."""

    issues = []
    suggestions = []

    # Check CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    if cpu_percent < 80:
        issues.append("Low CPU utilization")
        suggestions.append("Increase number of processes")

    # Check memory usage
    memory = psutil.virtual_memory()
    if memory.percent > 90:
        issues.append("High memory usage")
        suggestions.append("Reduce batch size or number of processes")

    # Check disk I/O
    disk = psutil.disk_usage('/')
    if disk.percent > 90:
        issues.append("Low disk space")
        suggestions.append("Free up disk space")

    return {"issues": issues, "suggestions": suggestions}
```

#### Memory Issues

```python
def memory_safe_config():
    """Generate memory-safe configuration."""

    available_gb = psutil.virtual_memory().available / (1024**3)

    if available_gb < 2:
        return {
            "num_processes": 1,
            "batch_size_arg": 50
        }
    elif available_gb < 4:
        return {
            "num_processes": 2,
            "batch_size_arg": 100
        }
    else:
        return {
            "num_processes": multiprocessing.cpu_count() - 1,
            "batch_size_arg": 200
        }
```

## Best Practices

### 🎯 Configuration Strategy

1. **Start with defaults** and measure performance
2. **Gradually adjust** one parameter at a time
3. **Benchmark** changes to verify improvements
4. **Document** your optimal settings for different scenarios

### 📊 Performance Monitoring

1. **Monitor CPU utilization** - should be 80-95% during cracking
2. **Watch memory usage** - keep under 80% of available RAM
3. **Check thermal throttling** - especially on laptops
4. **Measure actual throughput** - passwords per second

### 🔧 Optimization Tips

1. **Use appropriate character sets** - smaller is faster
2. **Progress systematically** - short lengths first
3. **Leave system resources** - for desktop responsiveness
4. **Test on sample files** - before long runs

## Next Steps

- 📊 **[Performance Guide](../performance/optimization.md)**: Deep dive into performance optimization
- 🛠️ **[Error Handling](error-handling.md)**: Handle configuration and runtime errors
- 📖 **[API Reference](../api/core.md)**: Detailed parameter documentation
- 🐍 **[Python Library](library.md)**: Advanced programmatic usage
