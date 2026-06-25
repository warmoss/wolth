"""Tests for the JSON utilities module."""

import json
from datetime import date, datetime
from unittest.mock import patch, mock_open

import pytest

from wolth.util.jsons import (
    ComplexEncoder,
    decode_object_hook,
    dumps,
    loads,
    dump,
    load,
)
from wolth.collections.enhanced.enhanced_dict import EnhancedDict
from wolth.collections.enhanced.enhanced_list import EnhancedList


# ──────────────────────────────────────────────
# ComplexEncoder
# ──────────────────────────────────────────────


class TestComplexEncoder:
    """Tests for ComplexEncoder."""

    def test_encode_datetime(self):
        """datetime is formatted as YYYY-MM-DD HH:MM:SS."""
        dt = datetime(2025, 6, 15, 14, 30, 0)
        result = json.dumps(dt, cls=ComplexEncoder)
        assert result == '"2025-06-15 14:30:00"'

    def test_encode_date(self):
        """date is formatted as YYYY-MM-DD."""
        d = date(2025, 6, 15)
        result = json.dumps(d, cls=ComplexEncoder)
        assert result == '"2025-06-15"'

    def test_encode_dict_becomes_enhanced_dict(self):
        """A plain dict is converted to EnhancedDict in default()."""
        # json.dumps handles dicts natively, so default() won't be called.
        # Instead, verify the encoder's default method directly.
        encoder = ComplexEncoder()
        result = encoder.default({"a": 1})
        assert isinstance(result, EnhancedDict)
        assert result.a == 1

    def test_encode_object_with_dict_method(self):
        """An object with __dict__ method is serialized via that method."""

        class Custom:
            def __dict__(self):
                return {"name": "test", "value": 42}

        obj = Custom()
        result = dumps(obj)
        assert result == '{\n  "name": "test",\n  "value": 42\n}'

    def test_encode_object_without_special_handling(self):
        """An unsupported type raises TypeError."""

        class Unsupported:
            pass

        with pytest.raises(TypeError):
            json.dumps(Unsupported(), cls=ComplexEncoder)

    def test_encode_datetime_midnight(self):
        dt = datetime(2025, 1, 1, 0, 0, 0)
        result = json.dumps(dt, cls=ComplexEncoder)
        assert result == '"2025-01-01 00:00:00"'

    def test_encode_date_epoch(self):
        d = date(1970, 1, 1)
        result = json.dumps(d, cls=ComplexEncoder)
        assert result == '"1970-01-01"'


# ──────────────────────────────────────────────
# decode_object_hook
# ──────────────────────────────────────────────


class TestDecodeObjectHook:
    """Tests for decode_object_hook."""

    def test_plain_dict_becomes_enhanced_dict(self):
        result = decode_object_hook({"a": 1, "b": 2})
        assert isinstance(result, EnhancedDict)
        assert result.a == 1
        assert result.b == 2

    def test_empty_dict(self):
        result = decode_object_hook({})
        assert isinstance(result, EnhancedDict)
        assert len(result) == 0

    def test_nested_dict_not_handled_here(self):
        """decode_object_hook only converts the top-level dict.
        Nested dicts are handled by json.loads calling the hook recursively.
        """
        result = decode_object_hook({"outer": {"inner": 1}})
        assert isinstance(result, EnhancedDict)
        # the inner dict hasn't been processed yet at this level
        assert isinstance(result["outer"], dict)


# ──────────────────────────────────────────────
# dumps
# ──────────────────────────────────────────────


class TestDumps:
    """Tests for dumps."""

    def test_dumps_simple_dict(self):
        result = dumps({"a": 1, "b": 2})
        assert result == '{\n  "a": 1,\n  "b": 2\n}'

    def test_dumps_list(self):
        result = dumps([1, 2, 3])
        assert result == "[\n  1,\n  2,\n  3\n]"

    def test_dumps_string(self):
        result = dumps("hello")
        assert result == '"hello"'

    def test_dumps_number(self):
        result = dumps(42)
        assert result == "42"

    def test_dumps_uses_complex_encoder_for_datetime(self):
        result = dumps(date(2025, 6, 15))
        assert result == '"2025-06-15"'

    def test_dumps_pretty_printed(self):
        """Output should be indented."""
        result = dumps({"x": 1})
        assert "  " in result  # has indentation

    def test_dumps_ensure_ascii_false(self):
        """Non-ASCII characters should be preserved."""
        result = dumps({"name": "café"})
        assert "café" in result

    def test_dumps_none(self):
        result = dumps(None)
        assert result == "null"


# ──────────────────────────────────────────────
# loads
# ──────────────────────────────────────────────


class TestLoads:
    """Tests for loads."""

    def test_loads_simple_dict(self):
        result = loads('{"a": 1, "b": 2}')
        assert isinstance(result, EnhancedDict)
        assert result.a == 1
        assert result.b == 2

    def test_loads_list(self):
        result = loads("[1, 2, 3]")
        assert isinstance(result, list)

    def test_loads_nested_dict(self):
        """Nested dicts are also converted to EnhancedDict."""
        result = loads('{"outer": {"inner": 1}}')
        assert isinstance(result, EnhancedDict)
        assert isinstance(result.outer, EnhancedDict)
        assert result.outer.inner == 1

    def test_loads_dict_with_list(self):
        """Lists inside dicts become EnhancedList."""
        result = loads('{"items": [1, 2, 3]}')
        assert isinstance(result, EnhancedDict)
        assert isinstance(result["items"], EnhancedList)

    def test_loads_string(self):
        result = loads('"hello"')
        assert result == "hello"

    def test_loads_number(self):
        result = loads("42")
        assert result == 42

    def test_loads_empty_dict(self):
        result = loads("{}")
        assert isinstance(result, EnhancedDict)
        assert len(result) == 0

    def test_loads_null(self):
        result = loads("null")
        assert result is None

    def test_loads_invalid_json(self):
        with pytest.raises(json.JSONDecodeError):
            loads("{invalid}")


# ──────────────────────────────────────────────
# dump (file write)
# ──────────────────────────────────────────────


class TestDump:
    """Tests for dump (write JSON to file)."""

    @patch("wolth.util.files.write_all")
    def test_dump_calls_write_all(self, mock_write_all):
        dump("/tmp/test.json", {"a": 1})
        mock_write_all.assert_called_once()
        args, _ = mock_write_all.call_args
        assert args[0] == "/tmp/test.json"
        assert args[1] == '{\n  "a": 1\n}'

    @patch("wolth.util.files.write_all")
    def test_dump_with_datetime(self, mock_write_all):
        dump("/tmp/test.json", date(2025, 6, 15))
        mock_write_all.assert_called_once()
        _, content = mock_write_all.call_args[0]
        assert '"2025-06-15"' in content

    @patch("wolth.util.files.write_all")
    def test_dump_none(self, mock_write_all):
        dump("/tmp/test.json", None)
        mock_write_all.assert_called_once()
        _, content = mock_write_all.call_args[0]
        assert content == "null"

    @patch("wolth.util.files.write_all")
    def test_dump_empty_dict(self, mock_write_all):
        dump("/tmp/test.json", {})
        mock_write_all.assert_called_once()
        _, content = mock_write_all.call_args[0]
        assert content == "{}"


# ──────────────────────────────────────────────
# load (file read)
# ──────────────────────────────────────────────


class TestLoad:
    """Tests for load (read JSON from file)."""

    @patch("wolth.util.files.read_all")
    def test_load_returns_enhanced_dict(self, mock_read_all):
        mock_read_all.return_value = '{"a": 1, "b": 2}'
        result = load("/tmp/test.json")
        assert isinstance(result, EnhancedDict)
        assert result.a == 1
        assert result.b == 2

    @patch("wolth.util.files.read_all")
    def test_load_calls_read_all(self, mock_read_all):
        mock_read_all.return_value = '{"x": 1}'
        load("/tmp/test.json")
        mock_read_all.assert_called_once_with("/tmp/test.json")

    @patch("wolth.util.files.read_all")
    def test_load_nested(self, mock_read_all):
        mock_read_all.return_value = '{"outer": {"inner": [1, 2, 3]}}'
        result = load("/tmp/test.json")
        assert isinstance(result.outer, EnhancedDict)
        assert isinstance(result.outer.inner, EnhancedList)
        assert list(result.outer.inner) == [1, 2, 3]

    @patch("wolth.util.files.read_all")
    def test_load_invalid_json(self, mock_read_all):
        mock_read_all.return_value = "{invalid}"
        with pytest.raises(json.JSONDecodeError):
            load("/tmp/test.json")
