from .converter import enhance, to_dict


class EnhancedList(list):
    """A ``list`` subclass that automatically wraps nested plain containers
    into enhanced types when adding or retrieving items.

    Example:
        >>> lst = EnhancedList([{"a": 1}, [2, 3]])
        >>> lst[0]           # automatically an EnhancedDict
        EnhancedDict({'a': 1})
        >>> lst[1]           # automatically an EnhancedList
        EnhancedList([2, 3])
    """

    def __init__(self, iterable=()):
        """Initialize the list, auto-enhancing each element."""
        super().__init__(enhance(item) for item in iterable)

    def __setitem__(self, index, value):
        """Set an item at *index*, auto-enhancing the value."""
        super().__setitem__(index, enhance(value))

    def append(self, value):
        """Append *value*, auto-enhancing it."""
        super().append(enhance(value))

    def extend(self, iterable):
        """Extend the list with items from *iterable*, auto-enhancing each."""
        super().extend(enhance(item) for item in iterable)

    def insert(self, index, value):
        """Insert *value* at *index*, auto-enhancing it."""
        super().insert(index, enhance(value))

    def __getitem__(self, index):
        """Get an item, auto-enhancing the returned value."""
        value = super().__getitem__(index)
        return enhance(value)

    def to_dict(self) -> list:
        """Recursively convert back to a plain ``list``.

        Returns:
            A plain ``list`` with all nested enhanced types unwrapped.
        """
        return [to_dict(item) for item in self]
