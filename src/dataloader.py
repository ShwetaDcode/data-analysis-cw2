import os
import json

def load_data(filepath):
    # get absolute path to project root (folder above src)
    base_dir = os.path.dirname(os.path.dirname(__file__))
    full_path = os.path.join(base_dir, filepath.replace("./", "").replace(".\\", ""))

    with open(full_path, "r") as file:
        for line in file:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue
