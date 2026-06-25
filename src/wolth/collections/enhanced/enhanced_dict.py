from .converter import enhance, to_dict


class EnhancedDict(dict):
    """A ``dict`` subclass that supports attribute-style access and
    automatically wraps nested plain containers into enhanced types.

    Example:
        >>> d = EnhancedDict({"name": "alice", "tags": ["admin"]})
        >>> d.name
        'alice'
        >>> d.tags           # automatically an EnhancedList
        EnhancedList(['admin'])
        >>> d.tags.append("staff")
        >>> d.tags
        EnhancedList(['admin', 'staff'])
    """

    def __init__(self, *args, **kwargs):
        """Initialize the dictionary.

        Accepts the same arguments as the built-in ``dict``:
        a mapping, an iterable of key-value pairs, and/or keyword arguments.
        """
        super().__init__()
        self.update(*args, **kwargs)

    def __getattr__(self, name):
        """Access dict keys as attributes (e.g. ``d.key`` → ``d["key"]``)."""
        return self[name] if name in self else None

    def __setattr__(self, name, value):
        """Set dict keys via attribute assignment (e.g. ``d.key = val``)."""
        self[name] = value

    def __delattr__(self, name):
        """Delete dict keys via ``del d.key``."""
        if name in self:
            del self[name]

    def __setitem__(self, key, value):
        """Set an item, automatically enhancing nested containers."""
        return super().__setitem__(key, enhance(value))

    def update(self, *args, **kwargs):
        """Update the dictionary, auto-enhancing all values."""
        arg = args[0] if len(args) > 0 else {}
        if isinstance(arg, dict):
            arg = arg.items()

        for k, v in arg:
            self[k] = v

        for k, v in kwargs.items():
            self[k] = v

    def to_dict(self) -> dict:
        """Recursively convert back to a plain ``dict``.

        Returns:
            A plain ``dict`` with all nested enhanced types unwrapped.
        """
        return {k: to_dict(v) for k, v in self.items()}

    def __repr__(self):
        return f"EnhancedDict({super().__repr__()})"
