#!/usr/bin/env python3
"""
Streamlitアプリの起動スクリプト
"""

import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    streamlit_app_path = Path(__file__).parent / "streamlit_app.py"
    
    # Streamlitを起動
    subprocess.run([
        sys.executable,
        "-m", "streamlit", "run",
        str(streamlit_app_path),
        "--server.port=8501",
        "--server.address=localhost"
    ])
