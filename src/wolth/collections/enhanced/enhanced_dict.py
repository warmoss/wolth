from .converter import enhance, to_dict


class EnhancedDict(dict):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.update(*args, **kwargs)

    def __getattr__(self, name):
        return self[name] if name in self else None

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]

    def __setitem__(self, key, value):
        return super().__setitem__(key, enhance(value))

    def update(self, *args, **kwargs):
        arg = args[0] if len(args) > 0 else {}
        if isinstance(arg, dict):
            arg = arg.items()

        for k, v in arg:
            self[k] = v

        for k, v in kwargs.items():
            self[k] = v

    def to_dict(self) -> dict:
        return {k: to_dict(v) for k, v in self.items()}

    def __repr__(self):
        return f"EnhancedDict({super().__repr__()})"
