import json
from wolth.util.files import files
from datetime import date, datetime
from wolth.collections import EnhancedDict


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, dict):
            return EnhancedDict(obj)
        elif hasattr(obj, "__dict__"):
            return obj.__dict__()
        else:
            return json.JSONEncoder.default(self, obj)


def decode_object_hook(obj):
    return EnhancedDict(obj)


def dumps(obj):
    return json.dumps(obj, cls=ComplexEncoder, ensure_ascii=False, indent=2)


def loads(s: str):
    return json.loads(s, object_hook=decode_object_hook)


def dump(filename: str, obj):
    content = json.dumps(obj, cls=ComplexEncoder, ensure_ascii=False, indent=2)
    files.write_all(filename, content)


def load(filename: str):
    content = files.read_all(filename)
    return json.loads(content, object_hook=decode_object_hook)
