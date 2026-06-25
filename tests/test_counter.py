"""Tests for the Counter class."""

from wolth.lang.counter import Counter


class TestCounterInit:
    """Test Counter initialization."""

    def test_default_init(self):
        """Counter starts at 0 by default."""
        c = Counter()
        assert c.get() == 0

    def test_init_with_value(self):
        """Counter starts at the given value."""
        c = Counter(42)
        assert c.get() == 42

    def test_init_with_zero(self):
        c = Counter(0)
        assert c.get() == 0

    def test_init_with_negative(self):
        c = Counter(-5)
        assert c.get() == -5


class TestCounterGet:
    """Test the get method."""

    def test_get_after_init(self):
        c = Counter(10)
        assert c.get() == 10

    def test_get_after_incr(self):
        c = Counter()
        c.incr()
        assert c.get() == 1

    def test_get_does_not_modify(self):
        c = Counter(5)
        assert c.get() == 5
        assert c.get() == 5  # still the same


class TestCounterIncr:
    """Test the incr method."""

    def test_incr_once(self):
        c = Counter()
        c.incr()
        assert c.get() == 1

    def test_incr_multiple(self):
        c = Counter()
        for _ in range(10):
            c.incr()
        assert c.get() == 10

    def test_incr_from_non_zero(self):
        c = Counter(100)
        c.incr()
        assert c.get() == 101


class TestCounterIncrAndGet:
    """Test the incr_and_get method (++i semantics)."""

    def test_incr_and_get_returns_new_value(self):
        c = Counter()
        result = c.incr_and_get()
        assert result == 1

    def test_incr_and_get_updates_counter(self):
        c = Counter(5)
        c.incr_and_get()
        assert c.get() == 6

    def test_incr_and_get_chained(self):
        c = Counter()
        val1 = c.incr_and_get()
        val2 = c.incr_and_get()
        assert val1 == 1
        assert val2 == 2


class TestCounterGetAndIncr:
    """Test the get_and_incr method (i++ semantics)."""

    def test_get_and_incr_returns_old_value(self):
        c = Counter(5)
        result = c.get_and_incr()
        assert result == 5

    def test_get_and_incr_updates_counter(self):
        c = Counter(5)
        c.get_and_incr()
        assert c.get() == 6

    def test_get_and_incr_chained(self):
        c = Counter()
        val1 = c.get_and_incr()
        val2 = c.get_and_incr()
        assert val1 == 0
        assert val2 == 1


class TestCounterEdgeCases:
    """Test edge cases for Counter."""

    def test_large_numbers(self):
        c = Counter(10**9)
        c.incr()
        assert c.get() == 10**9 + 1

    def test_incr_overflow_no_error(self):
        """Python integers have arbitrary precision."""
        c = Counter(2**63 - 1)
        c.incr()
        assert c.get() == 2**63

    def test_type_of_count(self):
        """Counter value should be an int."""
        c = Counter()
        assert isinstance(c.get(), int)
        c.incr()
        assert isinstance(c.get(), int)
