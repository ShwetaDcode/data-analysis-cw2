import os
import sys
import json

def get_base_path():
    # If running as EXE (PyInstaller)
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS

    # If running as normal Python
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def load_data(filepath):
    filepath = filepath.replace("./", "").replace(".\\", "")

    base_path = get_base_path()
    full_path = os.path.join(base_path, filepath)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Data file not found at: {full_path}")

    with open(full_path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue
