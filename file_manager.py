import json


def save(f: str, edited_dict: dict):
    with open(f, 'w') as json_file:
        to_write = json.dumps(edited_dict, indent=4)
        json_file.write(to_write)


def load(f: str):
    json_file = open(f, 'r')
    json_dict = json.loads(json_file.read())
    json_file.close()
    return json_dict
