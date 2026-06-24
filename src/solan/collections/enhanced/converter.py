def enhance(value):
    from .enhanced_dict import EnhancedDict
    from .enhanced_list import EnhancedList

    if isinstance(value, dict) and not isinstance(value, EnhancedDict):
        return EnhancedDict(value)
    elif isinstance(value, list) and not isinstance(value, EnhancedList):
        return EnhancedList(value)
    else:
        return value


def to_dict(value):
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
