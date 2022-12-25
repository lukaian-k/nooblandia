import json


def read_json(file):
    with open(file, 'r', encoding='utf8') as f:
        return json.load(f)
