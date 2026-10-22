"""
Root forwarder script for convenience.
Executes the main research pipeline in experiments/run_analysis.py.
"""

import sys
from pathlib import Path

# Add project root to sys.path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from experiments.run_analysis import run_pipeline

if __name__ == "__main__":
    run_pipeline()
