#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
import base64
from zenutils.sixutils import *

__all__ = [] + base64.__all__

from base64 import *

_globals = globals()

if not "encodebytes" in _globals and "encodestring" in _globals:
    _globals["encodebytes"] = _globals["encodestring"]
    __all__.append("encodebytes")

if not "decodebytes" in _globals and "decodestring" in _globals:
    _globals["decodebytes"] = _globals["decodestring"]
    __all__.append("decodebytes")
