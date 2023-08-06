import json

def parse(json_string):
    if not json_string or json_string is None:
        raise Exception("json_string is required.")
    return json.loads(json_string)

def get_by_key(data, key):
    if key in data:
        return data[key]
    else:
        raise Exception(key + " does not exists.")

def parse_from_file(path):
    if not path or path is None:
        raise Exception("File path is required.")
    jsonFile = open(path, "r")
    result = json.loads(jsonFile.read())
    jsonFile.close()
    return result

def serialize(obj):
    return json.dumps(obj)