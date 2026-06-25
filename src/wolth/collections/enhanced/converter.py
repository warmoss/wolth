"""Conversion helpers between plain and enhanced collection types.

:func:`enhance` recursively wraps plain ``dict`` / ``list`` objects into
:class:`~wolth.collections.EnhancedDict` / :class:`~wolth.collections.EnhancedList`.

:func:`to_dict` performs the inverse — it unwraps enhanced collections
back into plain built-in types.
"""

def enhance(value):
    """Recursively wrap plain ``dict`` and ``list`` into enhanced types.

    - A plain ``dict`` → :class:`~wolth.collections.EnhancedDict`
    - A plain ``list`` → :class:`~wolth.collections.EnhancedList`
    - Already-enhanced objects are returned unchanged.
    - All other types pass through untouched.

    Args:
        value: Any Python value.

    Returns:
        The (possibly wrapped) value.
    """
    from .enhanced_dict import EnhancedDict
    from .enhanced_list import EnhancedList

    if isinstance(value, dict) and not isinstance(value, EnhancedDict):
        return EnhancedDict(value)
    elif isinstance(value, list) and not isinstance(value, EnhancedList):
        return EnhancedList(value)
    else:
        return value


def to_dict(value):
    """Recursively convert enhanced collections back to plain types.

    - :class:`~wolth.collections.EnhancedDict` → plain ``dict``
    - :class:`~wolth.collections.EnhancedList` → plain ``list``
    - Plain ``dict`` / ``list`` are recursively converted.
    - All other types pass through untouched.

    Args:
        value: Any Python value.

    Returns:
        The converted value.
    """
    from .enhanced_dict import EnhancedDict
    from .enhanced_list import EnhancedList

    if isinstance(value, EnhancedDict):
        return value.to_dict()
    elif isinstance(value, EnhancedList):
        return value.to_dict()
    elif isinstance(value, dict):
        return {k: to_dict(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [to_dict(item) for item in value]
    else:
        return value
