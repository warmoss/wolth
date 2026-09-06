"""Identity generation utilities.

Thin convenience wrappers around :mod:`uuid` for common identity
use-cases such as database primary keys, request/session IDs, and
unique filenames:

- :func:`next_uuid` returns a standard hyphenated UUID v4 string.
- :func:`simple_uuid` returns the compact 32-char hex form (no hyphens).
- :func:`parse_uuid` / :func:`is_uuid` validate and normalize UUID input.
"""

import uuid


def next_uuid() -> str:
    """Return a new random (version 4) UUID as a hyphenated string.

    Returns:
        A 36-character UUID string, e.g. ``"123e4567-e89b-12d3-a456-426614174000"``.
    """
    return str(uuid.uuid4())


def simple_uuid() -> str:
    """Return a new random (version 4) UUID in compact hex form.

    Equivalent to :func:`next_uuid` with the hyphens removed, which is
    handy for embedding in URLs or filenames.

    Returns:
        A 32-character lowercase hex string, e.g. ``"123e4567e89b12d3a456426614174000"``.
    """
    return uuid.uuid4().hex


def parse_uuid(value) -> uuid.UUID:
    """Parse a value into a :class:`uuid.UUID`.

    Accepts hyphenated or compact hex strings as well as existing
    :class:`uuid.UUID` objects.

    Args:
        value: The value to parse.

    Returns:
        The parsed :class:`uuid.UUID`.

    Raises:
        ValueError: If *value* cannot be parsed as a UUID.
    """
    if isinstance(value, uuid.UUID):
        return value
    return uuid.UUID(str(value))


def is_uuid(value) -> bool:
    """Check whether *value* represents a valid UUID.

    Args:
        value: Any value; usually a hyphenated or compact hex UUID string.

    Returns:
        ``True`` if *value* can be parsed as a UUID, ``False`` otherwise.
    """
    try:
        parse_uuid(value)
    except (ValueError, TypeError):
        return False
    return True
