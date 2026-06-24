"""Tests for the converter module (enhance / to_dict)."""

from solan.collections.enhanced.converter import enhance, to_dict
from solan.collections.enhanced.enhanced_dict import EnhancedDict
from solan.collections.enhanced.enhanced_list import EnhancedList


class TestEnhance:
    """Tests for the enhance function."""

    def test_enhance_plain_dict(self):
        """A plain dict becomes an EnhancedDict."""
        result = enhance({"a": 1, "b": 2})
        assert isinstance(result, EnhancedDict)
        assert result["a"] == 1
        assert result["b"] == 2

    def test_enhance_plain_list(self):
        """A plain list becomes an EnhancedList."""
        result = enhance([1, 2, 3])
        assert isinstance(result, EnhancedList)
        assert list(result) == [1, 2, 3]

    def test_enhance_already_enhanced_dict(self):
        """An already EnhancedDict stays as-is."""
        original = EnhancedDict(a=1)
        result = enhance(original)
        assert result is original

    def test_enhance_already_enhanced_list(self):
        """An already EnhancedList stays as-is."""
        original = EnhancedList([1, 2])
        result = enhance(original)
        assert result is original

    def test_enhance_int(self):
        """Plain values are returned unchanged."""
        assert enhance(42) == 42

    def test_enhance_string(self):
        assert enhance("hello") == "hello"

    def test_enhance_float(self):
        assert enhance(3.14) == 3.14

    def test_enhance_bool(self):
        assert enhance(True) is True
        assert enhance(False) is False

    def test_enhance_none(self):
        assert enhance(None) is None

    def test_enhance_bytes(self):
        assert enhance(b"data") == b"data"

    def test_enhance_tuple(self):
        """Tuples are not dicts or lists, so returned as-is."""
        t = (1, 2, 3)
        assert enhance(t) is t

    def test_enhance_nested_structure(self):
        """Nested dicts/lists within a dict get enhanced."""
        data = {
            "items": [1, {"x": 10}],
            "config": {"nested": [1, 2]},
        }
        result = enhance(data)
        assert isinstance(result, EnhancedDict)
        assert isinstance(result["items"], EnhancedList)
        assert isinstance(result["config"], EnhancedDict)
        assert isinstance(result["items"][1], EnhancedDict)
        assert isinstance(result["config"]["nested"], EnhancedList)

    def test_enhance_empty_dict(self):
        result = enhance({})
        assert isinstance(result, EnhancedDict)
        assert len(result) == 0

    def test_enhance_empty_list(self):
        result = enhance([])
        assert isinstance(result, EnhancedList)
        assert len(result) == 0

    def test_enhance_custom_object(self):
        """Custom objects that aren't dict/list pass through unchanged."""

        class Custom:
            pass

        obj = Custom()
        assert enhance(obj) is obj

    def test_enhance_ordered_dict(self):
        """OrderedDict is a dict subclass but not EnhancedDict, so it gets enhanced."""
        from collections import OrderedDict

        od = OrderedDict([("a", 1)])
        result = enhance(od)
        assert isinstance(result, EnhancedDict)
        assert result["a"] == 1

    def test_enhance_subclass_of_list(self):
        """A list subclass that isn't EnhancedList gets enhanced."""

        class MyList(list):
            pass

        ml = MyList([1, 2])
        result = enhance(ml)
        assert isinstance(result, EnhancedList)
        assert list(result) == [1, 2]


class TestToDict:
    """Tests for the to_dict function."""

    def test_to_dict_enhanced_dict(self):
        d = EnhancedDict(a=1, b=2)
        result = to_dict(d)
        assert result == {"a": 1, "b": 2}
        assert type(result) is dict
        assert not isinstance(result, EnhancedDict)

    def test_to_dict_enhanced_list(self):
        lst = EnhancedList([1, 2, 3])
        result = to_dict(lst)
        assert result == [1, 2, 3]
        assert type(result) is list
        assert not isinstance(result, EnhancedList)

    def test_to_dict_plain_dict(self):
        d = {"a": 1, "b": {"c": 2}}
        result = to_dict(d)
        assert result == {"a": 1, "b": {"c": 2}}
        assert type(result) is dict
        assert type(result["b"]) is dict

    def test_to_dict_plain_list(self):
        lst = [1, [2, 3]]
        result = to_dict(lst)
        assert result == [1, [2, 3]]
        assert type(result) is list
        assert type(result[1]) is list

    def test_to_dict_plain_values(self):
        assert to_dict(42) == 42
        assert to_dict("hello") == "hello"
        assert to_dict(3.14) == 3.14
        assert to_dict(True) is True
        assert to_dict(None) is None

    def test_to_dict_deeply_nested(self):
        data = EnhancedDict(
            a=1,
            b=EnhancedDict(
                c=EnhancedList([1, EnhancedDict(d=2)]),
            ),
        )
        result = to_dict(data)
        assert result == {"a": 1, "b": {"c": [1, {"d": 2}]}}
        assert type(result["b"]["c"]) is list
        assert type(result["b"]["c"][1]) is dict

    def test_to_dict_with_enhanced_dict_in_list(self):
        data = EnhancedList([EnhancedDict(x=10), EnhancedDict(y=20)])
        result = to_dict(data)
        assert result == [{"x": 10}, {"y": 20}]
        assert type(result[0]) is dict

    def test_to_dict_empty_enhanced_dict(self):
        result = to_dict(EnhancedDict())
        assert result == {}

    def test_to_dict_empty_enhanced_list(self):
        result = to_dict(EnhancedList())
        assert result == []
