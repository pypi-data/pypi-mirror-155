import json


def json_to_bytes(data) -> bytes:
    return bytes(json.dumps(data), 'utf-8')
