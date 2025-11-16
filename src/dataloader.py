import json

def load_data(filepath):
    with open(filepath, "r") as file:
        for line in file:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue
