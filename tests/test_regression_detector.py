"""Tests for the benchmark regression detector CLI."""

import importlib.util
import json
import sys
from pathlib import Path
from textwrap import dedent
from unittest.mock import patch

import pytest

MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "benchmark" / "regression_detector.py"
)


def load_regression_detector_module():
    """Load the regression detector script as a module for testing."""
    spec = importlib.util.spec_from_file_location(
        "benchmark_regression_detector", MODULE_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_regression_detector_cli_accepts_threshold_help_percent(capsys):
    """The CLI should build successfully on Python 3.14 when threshold help includes %."""
    regression_detector = load_regression_detector_module()

    with (
        patch.object(
            regression_detector.PerformanceRegression,
            "check_regression",
            return_value=(
                False,
                {
                    "status": "ok",
                    "baseline_pw_per_sec": 1500.0,
                    "current_pw_per_sec": 1234.0,
                    "performance_drop_percent": 0.0,
                    "threshold_percent": 15.0,
                    "message": "ok",
                },
            ),
        ),
        patch.object(
            sys,
            "argv",
            [
                "regression_detector.py",
                "--current",
                "1234",
                "--threshold",
                "15.0",
                "--json",
            ],
        ),
    ):
        regression_detector.main()

    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "ok"
    assert output["current_pw_per_sec"] == 1234.0


def test_regression_detector_json_output_stays_valid_when_reading_latest_result(
    capsys, tmp_path, monkeypatch
):
    """JSON mode should keep informational benchmark messages off stdout."""
    regression_detector = load_regression_detector_module()
    history_file = tmp_path / "benchmark_history.csv"
    history_file.write_text(dedent("""\
            c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12
            0,0,0,0,0,0,0,0,0,0,0,0,1234
            """))

    def fake_init(self, results_dir="benchmark/results"):
        self.results_dir = tmp_path
        self.history_file = history_file

    monkeypatch.setattr(
        regression_detector.PerformanceRegression, "__init__", fake_init
    )

    with (
        patch.object(
            regression_detector.PerformanceRegression,
            "check_regression",
            return_value=(
                False,
                {
                    "status": "ok",
                    "baseline_pw_per_sec": 1500.0,
                    "current_pw_per_sec": 1234.0,
                    "performance_drop_percent": 0.0,
                    "threshold_percent": 15.0,
                    "message": "ok",
                },
            ),
        ),
        patch.object(
            sys,
            "argv",
            ["regression_detector.py", "--threshold", "15.0", "--json"],
        ),
    ):
        regression_detector.main()

    captured = capsys.readouterr()
    assert json.loads(captured.out)["current_pw_per_sec"] == pytest.approx(1234.0)
    assert "Using latest benchmark result" in captured.err
