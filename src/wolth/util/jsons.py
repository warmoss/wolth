"""JSON serialization / deserialization with :class:`~wolth.collections.EnhancedDict` support.

All public functions automatically convert plain ``dict`` and ``list`` objects
into :class:`~wolth.collections.EnhancedDict` and
:class:`~wolth.collections.EnhancedList` respectively, so you can use
attribute-style access on loaded data.

Additionally, :class:`ComplexEncoder` handles :class:`~datetime.date` and
:class:`~datetime.datetime` objects by formatting them as strings.
"""

import json
from wolth.util import files
from datetime import date, datetime
from wolth.collections import EnhancedDict


class ComplexEncoder(json.JSONEncoder):
    """JSON encoder that handles additional types beyond the standard set.

    Supported types:
    - :class:`~datetime.datetime` → formatted as ``"YYYY-MM-DD HH:MM:SS"``
    - :class:`~datetime.date` → formatted as ``"YYYY-MM-DD"``
    - ``dict`` → converted to :class:`~wolth.collections.EnhancedDict`
    - Objects with a ``__dict__()`` method → serialized via that method
    """

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
    """Decode a plain dict into an :class:`~wolth.collections.EnhancedDict`.

    Intended for use as the *object_hook* argument to :func:`json.loads`.
    """
    return EnhancedDict(obj)


def dumps(obj):
    """Serialize *obj* to a pretty-printed JSON string.

    Args:
        obj: Any JSON-serializable object.

    Returns:
        Indented JSON string with non-ASCII characters preserved.
    """
    return json.dumps(obj, cls=ComplexEncoder, ensure_ascii=False, indent=2)


def loads(s: str):
    """Deserialize a JSON string into Python objects.

    All decoded dicts are automatically converted to
    :class:`~wolth.collections.EnhancedDict` so you can use
    attribute-style access.

    Args:
        s: A JSON string.

    Returns:
        The deserialized Python object.
    """
    return json.loads(s, object_hook=decode_object_hook)


def dump(filename: str, obj):
    """Serialize *obj* as JSON and write it to a file.

    Args:
        filename: Path to the output file.
        obj: Any JSON-serializable object.
    """
    content = json.dumps(obj, cls=ComplexEncoder, ensure_ascii=False, indent=2)
    files.write_all(filename, content)


def load(filename: str):
    """Read a JSON file and deserialize its contents.

    All decoded dicts are automatically converted to
    :class:`~wolth.collections.EnhancedDict`.

    Args:
        filename: Path to the JSON file.

    Returns:
        The deserialized Python object.
    """
    content = files.read_all(filename)
    return json.loads(content, object_hook=decode_object_hook)
