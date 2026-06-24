"""Tests for EnhancedList."""

from solan.collections.enhanced.enhanced_dict import EnhancedDict
from solan.collections.enhanced.enhanced_list import EnhancedList


class TestEnhancedListInit:
    """Test EnhancedList initialization."""

    def test_empty_init(self):
        """Creating EnhancedList with no arguments."""
        lst = EnhancedList()
        assert len(lst) == 0
        assert isinstance(lst, list)
        assert isinstance(lst, EnhancedList)

    def test_init_with_list(self):
        """Creating EnhancedList with a list."""
        lst = EnhancedList([1, 2, 3])
        assert lst == [1, 2, 3]
        assert len(lst) == 3

    def test_init_with_tuple(self):
        """Creating EnhancedList with a tuple."""
        lst = EnhancedList((10, 20, 30))
        assert lst == [10, 20, 30]

    def test_init_with_generator(self):
        """Creating EnhancedList with a generator."""
        lst = EnhancedList(range(5))
        assert lst == [0, 1, 2, 3, 4]

    def test_init_with_string(self):
        """Creating EnhancedList with a string iterable."""
        lst = EnhancedList("abc")
        assert lst == ["a", "b", "c"]

    def test_init_auto_enhance_dicts(self):
        """Plain dicts in the iterable are auto-converted to EnhancedDict."""
        lst = EnhancedList([{"a": 1}, {"b": 2}])
        assert isinstance(lst[0], EnhancedDict)
        assert isinstance(lst[1], EnhancedDict)

    def test_init_auto_enhance_lists(self):
        """Plain lists in the iterable are auto-converted to EnhancedList."""
        lst = EnhancedList([[1, 2], [3, 4]])
        assert isinstance(lst[0], EnhancedList)
        assert isinstance(lst[1], EnhancedList)

    def test_init_mixed_types(self):
        """Mixed types are handled correctly."""
        lst = EnhancedList([1, "hello", {"key": "val"}, [10, 20]])
        assert lst[0] == 1
        assert lst[1] == "hello"
        assert isinstance(lst[2], EnhancedDict)
        assert isinstance(lst[3], EnhancedList)


class TestEnhancedListGetItem:
    """Test item access."""

    def test_getitem_by_index(self):
        lst = EnhancedList([10, 20, 30])
        assert lst[0] == 10
        assert lst[1] == 20
        assert lst[2] == 30

    def test_getitem_negative_index(self):
        lst = EnhancedList([1, 2, 3])
        assert lst[-1] == 3
        assert lst[-3] == 1

    def test_getitem_slice(self):
        lst = EnhancedList([1, 2, 3, 4, 5])
        assert lst[1:3] == [2, 3]

    def test_getitem_returns_enhanced_for_dicts(self):
        """Accessing a dict item returns EnhancedDict."""
        lst = EnhancedList([{"a": 1}])
        item = lst[0]
        assert isinstance(item, EnhancedDict)

    def test_getitem_index_error(self):
        lst = EnhancedList()
        try:
            _ = lst[0]
            assert False, "Should have raised IndexError"
        except IndexError:
            pass


class TestEnhancedListSetItem:
    """Test item setting."""

    def test_setitem(self):
        lst = EnhancedList([1, 2, 3])
        lst[1] = 99
        assert lst[1] == 99

    def test_setitem_enhances_dict(self):
        lst = EnhancedList([1])
        lst[0] = {"nested": True}
        assert isinstance(lst[0], EnhancedDict)

    def test_setitem_enhances_list(self):
        lst = EnhancedList([1])
        lst[0] = [10, 20]
        assert isinstance(lst[0], EnhancedList)


class TestEnhancedListAppend:
    """Test append method."""

    def test_append_simple(self):
        lst = EnhancedList()
        lst.append(42)
        assert lst == [42]

    def test_append_dict(self):
        lst = EnhancedList()
        lst.append({"key": "value"})
        assert isinstance(lst[0], EnhancedDict)

    def test_append_list(self):
        lst = EnhancedList()
        lst.append([1, 2])
        assert isinstance(lst[0], EnhancedList)

    def test_append_multiple(self):
        lst = EnhancedList([1])
        lst.append(2)
        lst.append(3)
        assert lst == [1, 2, 3]


class TestEnhancedListExtend:
    """Test extend method."""

    def test_extend_with_list(self):
        lst = EnhancedList([1, 2])
        lst.extend([3, 4])
        assert lst == [1, 2, 3, 4]

    def test_extend_enhances_items(self):
        lst = EnhancedList()
        lst.extend([{"a": 1}, [10, 20]])
        assert isinstance(lst[0], EnhancedDict)
        assert isinstance(lst[1], EnhancedList)


class TestEnhancedListInsert:
    """Test insert method."""

    def test_insert_at_beginning(self):
        lst = EnhancedList([2, 3])
        lst.insert(0, 1)
        assert lst == [1, 2, 3]

    def test_insert_at_end(self):
        lst = EnhancedList([1, 2])
        lst.insert(2, 3)
        assert lst == [1, 2, 3]

    def test_insert_enhances_dict(self):
        lst = EnhancedList()
        lst.insert(0, {"x": 1})
        assert isinstance(lst[0], EnhancedDict)


class TestEnhancedListToDict:
    """Test to_dict method."""

    def test_to_dict_plain(self):
        lst = EnhancedList([1, 2, 3])
        result = lst.to_dict()
        assert result == [1, 2, 3]
        assert type(result) is list
        assert not isinstance(result, EnhancedList)

    def test_to_dict_with_enhanced_dict(self):
        lst = EnhancedList([EnhancedDict(a=1)])
        result = lst.to_dict()
        assert result == [{"a": 1}]
        assert type(result[0]) is dict

    def test_to_dict_with_enhanced_list(self):
        lst = EnhancedList([EnhancedList([1, 2])])
        result = lst.to_dict()
        assert result == [[1, 2]]
        assert type(result[0]) is list

    def test_to_dict_deeply_nested(self):
        lst = EnhancedList([
            EnhancedDict(
                items=EnhancedList([1, EnhancedDict(x=2)])
            )
        ])
        result = lst.to_dict()
        assert result == [{"items": [1, {"x": 2}]}]
        assert type(result[0]) is dict
        assert type(result[0]["items"]) is list
        assert type(result[0]["items"][1]) is dict


class TestEnhancedListEdgeCases:
    """Test edge cases."""

    def test_enhanced_list_is_list_subclass(self):
        assert issubclass(EnhancedList, list)

    def test_instance_of_list(self):
        assert isinstance(EnhancedList(), list)

    def test_list_methods_still_work(self):
        lst = EnhancedList([3, 1, 2])
        lst.sort()
        assert lst == [1, 2, 3]

        lst.reverse()
        assert lst == [3, 2, 1]

    def test_pop(self):
        lst = EnhancedList([1, 2, 3])
        assert lst.pop() == 3
        assert lst == [1, 2]

    def test_pop_with_index(self):
        lst = EnhancedList([10, 20, 30])
        assert lst.pop(0) == 10
        assert lst == [20, 30]

    def test_remove(self):
        lst = EnhancedList([1, 2, 3, 2])
        lst.remove(2)
        assert lst == [1, 3, 2]

    def test_count(self):
        lst = EnhancedList([1, 2, 1, 3, 1])
        assert lst.count(1) == 3

    def test_index(self):
        lst = EnhancedList(["a", "b", "c"])
        assert lst.index("b") == 1

    def test_contains(self):
        lst = EnhancedList([1, 2, 3])
        assert 2 in lst
        assert 99 not in lst

    def test_bool_empty(self):
        assert not EnhancedList()

    def test_bool_nonempty(self):
        assert EnhancedList([1])

    def test_iteration(self):
        lst = EnhancedList([10, 20, 30])
        items = []
        for item in lst:
            items.append(item)
        assert items == [10, 20, 30]

    def test_len(self):
        lst = EnhancedList([1, 2, 3])
        assert len(lst) == 3
        lst.append(4)
        assert len(lst) == 4

    def test_equality(self):
        lst1 = EnhancedList([1, 2, 3])
        lst2 = EnhancedList([1, 2, 3])
        assert lst1 == lst2
        assert lst1 == [1, 2, 3]

    def test_concatenation(self):
        lst = EnhancedList([1, 2]) + [3, 4]
        # Concatenation returns a plain list
        assert lst == [1, 2, 3, 4]
        assert type(lst) is list

    def test_repetition(self):
        lst = EnhancedList([1, 2]) * 2
        # Repetition returns a plain list
        assert lst == [1, 2, 1, 2]
        assert type(lst) is list

    def test_copy_returns_plain_list(self):
        """list.copy() returns a plain list, not EnhancedList."""
        lst = EnhancedList([1, 2, 3])
        copied = lst.copy()
        assert copied == [1, 2, 3]
        assert type(copied) is list
