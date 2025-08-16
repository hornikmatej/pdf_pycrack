#!/usr/bin/env python3
"""
Performance Regression Detection Tool

Automatically detects when performance drops below acceptable thresholds
by comparing current benchmark results with historical baselines.
"""

import csv
import json
import statistics
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Tuple


class PerformanceRegression:
    """Detects performance regressions in benchmark results."""

    def __init__(self, results_dir: str = "benchmark/results"):
        self.results_dir = Path(results_dir)
        self.history_file = self.results_dir / "benchmark_history.csv"

    def get_baseline_performance(self, days_back: int = 30) -> Optional[float]:
        """Get baseline performance from recent successful runs.

        Args:
            days_back: Number of days to look back for baseline

        Returns:
            Median passwords per second from recent runs, or None if no data
        """
        if not self.history_file.exists():
            return None

        cutoff_date = datetime.now() - timedelta(days=days_back)
        recent_results = []

        with open(self.history_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    timestamp = datetime.fromisoformat(row["timestamp"])
                    if timestamp >= cutoff_date:
                        pw_per_sec = float(row["passwords_per_second"])
                        # Only include successful full runs (not interrupted)
                        if (
                            row["result_type"] == "PasswordNotFound"
                            and pw_per_sec > 1000
                        ):
                            recent_results.append(pw_per_sec)
                except (ValueError, KeyError):
                    continue

        if len(recent_results) < 3:
            return None

        return statistics.median(recent_results)

    def check_regression(
        self, current_performance: float, threshold_percent: float = 10.0
    ) -> Tuple[bool, Dict]:
        """Check if current performance represents a regression.

        Args:
            current_performance: Current passwords per second
            threshold_percent: Percentage drop that constitutes regression

        Returns:
            Tuple of (is_regression, details_dict)
        """
        baseline = self.get_baseline_performance()

        if baseline is None:
            return False, {
                "status": "no_baseline",
                "message": "Insufficient historical data for regression detection",
                "current": current_performance,
            }

        performance_drop = ((baseline - current_performance) / baseline) * 100
        is_regression = performance_drop > threshold_percent

        return is_regression, {
            "status": "regression" if is_regression else "ok",
            "baseline_pw_per_sec": baseline,
            "current_pw_per_sec": current_performance,
            "performance_drop_percent": performance_drop,
            "threshold_percent": threshold_percent,
            "message": self._get_regression_message(
                is_regression, baseline, current_performance, performance_drop
            ),
        }

    def _get_regression_message(
        self, is_regression: bool, baseline: float, current: float, drop_percent: float
    ) -> str:
        """Generate human-readable regression message."""
        if not is_regression:
            if drop_percent < 0:  # Performance improved
                return f"✅ Performance improved by {abs(drop_percent):.1f}%"
            else:
                return (
                    f"✅ Performance within acceptable range ({drop_percent:.1f}% drop)"
                )

        return (
            f"⚠️  PERFORMANCE REGRESSION DETECTED!\n"
            f"   Baseline: {baseline:,.0f} pw/s\n"
            f"   Current:  {current:,.0f} pw/s\n"
            f"   Drop:     {drop_percent:.1f}%"
        )


def main():
    """CLI tool for checking performance regression."""
    import argparse

    parser = argparse.ArgumentParser(description="Check for performance regression")
    parser.add_argument(
        "--current",
        type=float,
        help="Current performance (passwords per second). If not provided, reads from latest benchmark result.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=15.0,
        help="Regression threshold percentage (default: 15%)",
    )
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument(
        "--fail-on-regression",
        action="store_true",
        help="Exit with error code if regression detected",
    )

    args = parser.parse_args()

    detector = PerformanceRegression()

    # If no current performance provided, read from latest benchmark
    if args.current is None:
        try:
            with open(detector.history_file, "r") as f:
                lines = f.readlines()
                if len(lines) > 1:  # Skip header
                    last_line = lines[-1].strip()
                    current_perf = float(
                        last_line.split(",")[12]
                    )  # passwords_per_second column
                    print(f"Using latest benchmark result: {current_perf:,.0f} pw/s")
                else:
                    print("No benchmark data found. Run a benchmark first.")
                    exit(1)
        except (FileNotFoundError, IndexError, ValueError) as e:
            print(f"Error reading benchmark data: {e}")
            print("Please provide --current or run a benchmark first.")
            exit(1)
    else:
        current_perf = args.current

    is_regression, details = detector.check_regression(current_perf, args.threshold)

    if args.json:
        print(json.dumps(details, indent=2))
    else:
        print(details["message"])

        if is_regression:
            print(
                "\n⚠️  Consider investigating recent changes that might affect performance:"
            )
            print("   - Added logging or debug code")
            print("   - Inefficient algorithms")
            print("   - Memory allocation issues")
            print("   - Blocking I/O operations")

    if is_regression and args.fail_on_regression:
        exit(1)  # Non-zero exit code for CI/CD


if __name__ == "__main__":
    main()
