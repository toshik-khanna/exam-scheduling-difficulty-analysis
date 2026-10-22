"""
Test runner script.
Executes the complete test suite (21 tests) across all 6 test modules.

Usage:
    python run_tests.py
"""

import sys
from pathlib import Path

# Ensure src/ is on sys.path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

import pytest

if __name__ == "__main__":
    exit_code = pytest.main(["-v", str(ROOT / "tests")])
    sys.exit(exit_code)
