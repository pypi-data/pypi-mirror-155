import json


def read_json(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        values = json.load(file)

    return values
