"""Tests for EnhancedDict."""

from wolth.collections.enhanced.enhanced_dict import EnhancedDict
from wolth.collections.enhanced.enhanced_list import EnhancedList


class TestEnhancedDictInit:
    """Test EnhancedDict initialization."""

    def test_empty_init(self):
        """Creating EnhancedDict with no arguments."""
        d = EnhancedDict()
        assert len(d) == 0
        assert isinstance(d, dict)
        assert isinstance(d, EnhancedDict)

    def test_init_with_dict(self):
        """Creating EnhancedDict with a dict."""
        d = EnhancedDict({"a": 1, "b": 2})
        assert d["a"] == 1
        assert d["b"] == 2
        assert len(d) == 2

    def test_init_with_kwargs(self):
        """Creating EnhancedDict with keyword arguments."""
        d = EnhancedDict(a=1, b=2)
        assert d["a"] == 1
        assert d["b"] == 2
        assert len(d) == 2

    def test_init_with_dict_and_kwargs(self):
        """Creating EnhancedDict with both dict and kwargs."""
        d = EnhancedDict({"a": 1}, b=2, c=3)
        assert d["a"] == 1
        assert d["b"] == 2
        assert d["c"] == 3
        assert len(d) == 3

    def test_init_with_iterable(self):
        """Creating EnhancedDict with an iterable of key-value pairs."""
        d = EnhancedDict([("a", 1), ("b", 2)])
        assert d["a"] == 1
        assert d["b"] == 2

    def test_init_auto_enhance_nested_dict(self):
        """Nested plain dicts are auto-converted to EnhancedDict."""
        d = EnhancedDict({"nested": {"x": 1}})
        assert isinstance(d["nested"], EnhancedDict)
        assert d["nested"]["x"] == 1

    def test_init_auto_enhance_nested_list(self):
        """Nested plain lists are auto-converted to EnhancedList."""
        d = EnhancedDict({"items": [1, 2, 3]})
        assert isinstance(d["items"], EnhancedList)
        assert list(d["items"]) == [1, 2, 3]


class TestEnhancedDictGetAttr:
    """Test attribute-style access."""

    def test_getattr_existing_key(self,):
        d = EnhancedDict(a=42)
        assert d.a == 42

    def test_getattr_non_existing_key(self):
        d = EnhancedDict(a=1)
        assert d.b is None

    def test_getattr_after_setitem(self):
        d = EnhancedDict()
        d["name"] = "hello"
        assert d.name == "hello"


class TestEnhancedDictSetAttr:
    """Test attribute-style setting."""

    def test_setattr(self):
        d = EnhancedDict()
        d.foo = "bar"
        assert d["foo"] == "bar"
        assert d.foo == "bar"

    def test_setattr_overwrite(self):
        d = EnhancedDict(a=1)
        d.a = 99
        assert d["a"] == 99

    def test_setattr_with_enhancement(self):
        d = EnhancedDict()
        d.nested = {"x": 1}
        assert isinstance(d["nested"], EnhancedDict)


class TestEnhancedDictDelAttr:
    """Test attribute-style deletion."""

    def test_delattr_existing_key(self):
        d = EnhancedDict(a=1, b=2)
        del d.a
        assert "a" not in d
        assert d.b == 2

    def test_delattr_non_existing_key(self):
        """Deleting a non-existing key should not raise an error."""
        d = EnhancedDict(a=1)
        # Should not raise
        del d.nonexistent
        assert d.a == 1


class TestEnhancedDictSetItem:
    """Test item setting."""

    def test_setitem(self):
        d = EnhancedDict()
        d["key"] = "value"
        assert d["key"] == "value"

    def test_setitem_enhances_dict(self):
        d = EnhancedDict()
        d["child"] = {"nested": True}
        assert isinstance(d["child"], EnhancedDict)

    def test_setitem_enhances_list(self):
        d = EnhancedDict()
        d["nums"] = [1, 2]
        assert isinstance(d["nums"], EnhancedList)

    def test_setitem_overwrite(self):
        d = EnhancedDict(a=1)
        d["a"] = 100
        assert d["a"] == 100


class TestEnhancedDictUpdate:
    """Test update method."""

    def test_update_with_dict(self):
        d = EnhancedDict(a=1)
        d.update({"b": 2, "c": 3})
        assert d["a"] == 1
        assert d["b"] == 2
        assert d["c"] == 3

    def test_update_with_kwargs(self):
        d = EnhancedDict(a=1)
        d.update(b=2, c=3)
        assert d["a"] == 1
        assert d["b"] == 2
        assert d["c"] == 3

    def test_update_with_iterable(self):
        d = EnhancedDict()
        d.update([("x", 10), ("y", 20)])
        assert d["x"] == 10
        assert d["y"] == 20

    def test_update_enhances_values(self):
        d = EnhancedDict()
        d.update({"child": {"deep": True}})
        assert isinstance(d["child"], EnhancedDict)

    def test_update_overwrite(self):
        d = EnhancedDict(a=1)
        d.update({"a": 999})
        assert d["a"] == 999


class TestEnhancedDictToDict:
    """Test to_dict method."""

    def test_to_dict_plain(self):
        d = EnhancedDict(a=1, b=2)
        result = d.to_dict()
        assert result == {"a": 1, "b": 2}
        assert type(result) is dict
        assert not isinstance(result, EnhancedDict)

    def test_to_dict_with_nested_enhanced_dict(self):
        d = EnhancedDict(nested=EnhancedDict(x=1, y=2))
        result = d.to_dict()
        assert result == {"nested": {"x": 1, "y": 2}}
        assert type(result["nested"]) is dict

    def test_to_dict_with_nested_enhanced_list(self):
        d = EnhancedDict(items=EnhancedList([1, 2, {"a": 1}]))
        result = d.to_dict()
        assert result == {"items": [1, 2, {"a": 1}]}
        assert type(result["items"]) is list
        assert type(result["items"][2]) is dict

    def test_to_dict_deeply_nested(self):
        d = EnhancedDict(
            level1=EnhancedDict(
                level2=EnhancedList([EnhancedDict(x=1)])
            )
        )
        result = d.to_dict()
        assert result == {"level1": {"level2": [{"x": 1}]}}
        assert type(result["level1"]) is dict
        assert type(result["level1"]["level2"]) is list
        assert type(result["level1"]["level2"][0]) is dict


class TestEnhancedDictRepr:
    """Test __repr__ method."""

    def test_repr_empty(self):
        d = EnhancedDict()
        assert repr(d) == "EnhancedDict({})"

    def test_repr_with_items(self):
        d = EnhancedDict(a=1)
        rep = repr(d)
        assert rep.startswith("EnhancedDict(")
        assert rep.endswith(")")
        assert "a" in rep


class TestEnhancedDictEdgeCases:
    """Test edge cases."""

    def test_enhanced_dict_is_dict_subclass(self):
        assert issubclass(EnhancedDict, dict)

    def test_instance_of_dict(self):
        assert isinstance(EnhancedDict(), dict)

    def test_dict_methods_still_work(self):
        d = EnhancedDict(a=1, b=2, c=3)
        assert list(d.keys()) == ["a", "b", "c"]
        assert list(d.values()) == [1, 2, 3]
        assert list(d.items()) == [("a", 1), ("b", 2), ("c", 3)]

    def test_len(self):
        d = EnhancedDict(a=1, b=2)
        assert len(d) == 2
        d["c"] = 3
        assert len(d) == 3

    def test_contains(self):
        d = EnhancedDict(a=1)
        assert "a" in d
        assert "b" not in d

    def test_bool_empty(self):
        assert not EnhancedDict()

    def test_bool_nonempty(self):
        assert EnhancedDict(a=1)

    def test_get_method(self):
        d = EnhancedDict(a=1)
        assert d.get("a") == 1
        assert d.get("nonexistent") is None
        assert d.get("nonexistent", 42) == 42

    def test_pop(self):
        d = EnhancedDict(a=1, b=2)
        assert d.pop("a") == 1
        assert "a" not in d

    def test_popitem(self):
        d = EnhancedDict(a=1)
        key, val = d.popitem()
        assert key == "a"
        assert val == 1

    def test_clear(self):
        d = EnhancedDict(a=1, b=2)
        d.clear()
        assert len(d) == 0

    def test_copy_returns_plain_dict(self):
        """dict.copy() returns a plain dict, not EnhancedDict."""
        d = EnhancedDict(a=1, b=EnhancedDict(x=10))
        copied = d.copy()
        assert copied["a"] == 1
        assert type(copied) is dict
