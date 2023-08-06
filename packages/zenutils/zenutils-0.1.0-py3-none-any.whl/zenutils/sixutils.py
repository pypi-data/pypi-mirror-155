#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement

__all__ = [
    "PY2",
    "PY3",
    "STR_TYPE",
    "BYTES_TYPE",
    "BASESTRING_TYPES",
    "TEXT",
    "BYTES",
    "INT_TO_BYTES",
    "force_bytes",
    "force_text",
    "bytes_to_array",
    "bstr_to_array",
    "bchar",
    "default_encodings",
    "default_encoding",
    "NUMERIC_TYPES",
]

import sys

default_encodings = ["utf-8", "gb18030"]
default_encoding = "utf-8"

INT_TO_BYTES = {}
if sys.version_info.major == 2:
    PY2 = True
    PY3 = False
    BASESTRING_TYPES = (basestring,str,unicode)
    STR_TYPE = unicode
    BYTES_TYPE = str
    for i in range(256):
        INT_TO_BYTES[i] = chr(i)
    NUMERIC_TYPES = (int, long, float)
else:
    PY2 = False
    PY3 = True
    BASESTRING_TYPES = (str, bytes)
    STR_TYPE = str
    BYTES_TYPE = bytes
    for i in range(256):
        INT_TO_BYTES[i] = bytes([i])
    NUMERIC_TYPES = (int, float)

def force_bytes(value, encoding=None):
    if callable(value):
        value = value()
    if value is None:
        return None
    if isinstance(value, BYTES_TYPE):
        return value
    encoding = encoding or default_encoding
    if isinstance(value, STR_TYPE):
        return value.encode(encoding)
    else:
        return STR_TYPE(value).encode(encoding)

def force_text(value, encoding=None):
    if callable(value):
        value = value()
    if value is None:
        return None
    if isinstance(value, STR_TYPE):
        return value
    if not isinstance(value, BYTES_TYPE):
        return str(value)
    if not encoding:
        encodings = default_encodings
    elif isinstance(encoding, (set, list, tuple)):
        encodings = encoding
    else:
        encodings = [encoding]
    last_error = None
    for encoding in encodings:
        try:
            return value.decode(encoding)
        except UnicodeDecodeError as error:
            last_error = error
    if last_error:
        last_error.encoding = " or ".join(encodings)
        raise last_error

def bytes_to_array(data):
    """Turn bytes into list of bytes char.

    @Returns:
        (list of bytes char): Returns the list of the bytes char.
    
    @Parameters:
        data(str or bytes): The data to be splitted.
    
    @Example:
        sixutils.bytes_to_array(b"hello") == [b"h", b"e", b"l", b"l", b"o"]
    """
    data = force_bytes(data)
    if PY2:
        return list(data)
    else:
        return [data[idx:idx+1] for idx in range(len(data))]

def bstr_to_array(data):
    """Get char array of the given data.

    Returns:
        (list of char): The char array of the given daa.
    
    @Parameters:
        data(str or bytes): The data will be split into chars.
    
    @Examples:
        assert sixutils.bstr_to_array("hello") == ["h", "e", "l", "l", "o"]
        assert sixutils.bstr_to_array(b"hello") == [b"h", b"e", b"l", b"l", b"o"]
    """
    if isinstance(data, BYTES_TYPE):
        return bytes_to_array(data)
    else:
        return list(data)

def bchar(value):
    """Similar as chr(value) by returns bytes char. The value is in [0, 255].

    @Returns:
        (bytes char): One length bytes.
    
    @Parameters:
        value(int): The int value between [0, 255].
    
    @Example:
        assert bchar(0) == b'\\x00';
        assert bchar(1) == b'\\x01';
        assert bchar(255) == b'\\xff'.
    """
    return INT_TO_BYTES[value]

def TEXT(value):
    return force_text(value)

def BYTES(value):
    return force_bytes(value)
