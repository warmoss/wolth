"""A minimal integer counter utility.

Provides thread-unsafe increment / get semantics, useful for simple
counting scenarios (e.g. ID generation, iteration tracking).
"""


class Counter(object):
    """A simple, thread-unsafe incrementing counter.

    Args:
        count: Initial value (default ``0``).
    """

    def __init__(self, count=0) -> None:
        self._count_ = count

    def get(self):
        """Return the current counter value."""
        return self._count_

    def incr(self):
        """Increment the counter by 1."""
        self._count_ += 1

    def incr_and_get(self):
        """Increment the counter, then return the new value.

        Equivalent to ``++i`` in C-like languages.
        """
        self._count_ += 1
        return self._count_

    def get_and_incr(self):
        """Return the current value, then increment the counter.

        Equivalent to ``i++`` in C-like languages.
        """
        old_value = self._count_
        self._count_ += 1
        return old_value
