"""Enhanced collection types that extend built-in Python containers.

Provides attribute-style access on dicts and automatic recursive conversion
between plain and enhanced types.

Exports:
    EnhancedDict — a ``dict`` subclass with attribute-style access.
    EnhancedList — a ``list`` subclass with automatic item enhancement.
"""

from .enhanced.enhanced_dict import EnhancedDict
from .enhanced.enhanced_list import EnhancedList
