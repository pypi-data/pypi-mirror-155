#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
from zenutils.sixutils import *

__all__ = [
    "register_global_encoder",
    "make_simple_json_encoder",
    "SimpleJsonEncoder",
    "simple_json_dumps",
]

import json
import uuid
import binascii
import datetime
import decimal
from io import BytesIO
from functools import partial

from zenutils.sixutils import BASESTRING_TYPES

default_simple_json_encoder_base = json.encoder.JSONEncoder
default_error_code = 1

class JsonEncodeLibrary(object):

    def __init__(self, base_class=default_simple_json_encoder_base):
        self.base_class = base_class
        self.encoders = {}
        self.__encoder = None

    def get_encoder(self):
        this = self
        if this.__encoder is not None:
            return this.__encoder
        class SimpleJsonEncoderBase(this.base_class):
            def default(self, o):
                for t, encoder in this.encoders.items():
                    try:
                        isinstance_flag = isinstance(o, t)
                    except:
                        isinstance_flag = False
                    if isinstance_flag:
                        return encoder(o)
                    try:
                        issubclass_flag = issubclass(o, t)
                    except:
                        issubclass_flag = False
                    if issubclass_flag:
                        return encoder(o)
                return super(SimpleJsonEncoder, self).default(o)
        if PY2:
            import json
            import json.encoder
            _default_encode_basestring = json.encoder.encode_basestring
            _default_encode_basestring_ascii = json.encoder.encode_basestring_ascii
            def _encode_basestring(s):
                try:
                    s = force_text(s)
                except:
                    s = encode_bytes(s)
                return _default_encode_basestring(s)
            def _encode_basestring_ascii(s):
                try:
                    s = force_text(s)
                except:
                    s = encode_bytes(s)
                return _default_encode_basestring_ascii(s)
            class SimpleJsonEncoder(SimpleJsonEncoderBase):
                def encode(self, o):
                    json.encoder.encode_basestring = _encode_basestring
                    json.encoder.encode_basestring_ascii = _encode_basestring_ascii
                    result = super(SimpleJsonEncoder, self).encode(o)
                    json.encoder.encode_basestring = _default_encode_basestring
                    json.encoder.encode_basestring_ascii = _default_encode_basestring_ascii     
                    return result
        else:
            class SimpleJsonEncoder(SimpleJsonEncoderBase):
                pass
        this.__encoder = SimpleJsonEncoder
        setattr(this.__encoder, "library", this)
        return this.__encoder

    def register(self, type, encode):
        self.encoders[type] = encode

    def unregister(self, type):
        if type in self.encoders:
            del self.encoders[type]

DATETIME_ISO_FORMAT = "isoformat"
DATETIME_FORMAT = DATETIME_ISO_FORMAT

def set_datetime_format(format=DATETIME_ISO_FORMAT):
    global DATETIME_FORMAT
    DATETIME_FORMAT = format

def encode_datetime(value):
    if DATETIME_FORMAT == DATETIME_ISO_FORMAT:
        return value.isoformat()
    else:
        return value.strftime(DATETIME_FORMAT)

def encode_bytes(value):
    return binascii.hexlify(value).decode()

def encode_basestring(value):
    if isinstance(value, BYTES_TYPE):
        return encode_bytes(value)
    else:
        return value

def encode_decimal(value):
    return float(value)

def encode_complex(value):
    return [value.real, value.imag]

def encode_uuid(value):
    return str(value)

def encode_image(image):
    from zenutils import base64utils
    buffer = BytesIO()
    image.save(buffer, format="png")
    return """data:image/{format};base64,{data}""".format(
        format=format,
        data=force_text(base64utils.encodebytes(buffer.getvalue())),
        )

def encode_exception(error):
    from zenutils import strutils
    from zenutils import funcutils
    if error.args:
        try:
            code = strutils.force_int(error.args[0])
            message = " ".join(error.args[1:])
            return {
                "code": code,
                "message": message,
            }
        except:
            message = " ".join(error.args)
            if message:
                return {
                    "code": default_error_code,
                    "message": message
                }
    return {
        "code": default_error_code,
        "message": funcutils.get_class_name(error),
    }

def encode_bizerror(error):
    return error.json

def encode_django_model(django_model):
    from django.core import serializers

    try:
        isinstance_flag = isinstance(django_model, Model)
    except:
        isinstance_flag = False
    try:
        issubclass_flag = issubclass(django_model, Model)
    except:
        issubclass_flag = False
    if issubclass_flag:
        return ".".join([django_model._meta.app_label, django_model._meta.model_name])
    if isinstance_flag:
        pk_name = django_model._meta.pk.name
        text = serializers.serialize("json", [django_model])
        results = json.loads(text)
        obj = results[0]["fields"]
        obj[pk_name] = results[0]["pk"]
        return obj
    return None

def encode_django_queryset(django_queryset):
    from django.core import serializers
    
    pk_name = django_queryset.model._meta.pk.name
    text = serializers.serialize("json", django_queryset)
    results = json.loads(text)
    data = []
    for result in results:
        obj = result["fields"]
        obj[pk_name] = result["pk"]
        data.append(obj)
    return data

def encode_django_query(django_query):
    return str(django_query)

GLOBAL_ENCODERS = {}

def register_global_encoder(type, encoder):
    """Register a new encoder type to the global-encoder-collections.

    @Returns:
        (None): Nothing.
    
    @Paramters:
        type(Any type): The type has a custom encode callback.
        encoder(Callable): A callable object that
                            takes one parameter which is to be json serialized
                            and returns the system serializable value.
    

    @Example:
        class Model(object):
            def __init__(self):
                self.name = ""
                self.age = 0
            
            def json(self):
                return {
                    "name": self.name,
                    "age": self.age,
                }
        
        def model_encoder(o):
            return o.json()
        
        register_global_encoder(Model, model_encoder)
    """
    if isinstance(type, (list, tuple, set)):
        types = type
    else:
        types = [type]
    for type in types:
        GLOBAL_ENCODERS[type] = encoder

def register_simple_encoders(library):
    """Copy the encoders in the global-encoder-collections to a new encoder library instance.

    @Returns:
        (None): Nothing.
    
    @Parameters:
        library(JsonEncodeLibrary): An instance of JsonEncodeLibrary.
    """
    for type, encoder in GLOBAL_ENCODERS.items():
        library.register(type, encoder)

register_global_encoder((datetime.datetime, datetime.date, datetime.time), encode_datetime)
register_global_encoder(decimal.Decimal, encode_decimal)
register_global_encoder(complex, encode_complex)
register_global_encoder(uuid.UUID, encode_uuid)
register_global_encoder(BASESTRING_TYPES, encode_basestring)

try:
    from zenutils import funcutils
    for exception_class in funcutils.get_all_builtin_exceptions():
        register_global_encoder(exception_class, encode_exception)
except Exception:
    pass

try:
    from PIL.Image import Image
    register_global_encoder(Image, encode_image)
except ImportError:
    pass

try:
    from django.db.models import Model
    register_global_encoder(Model, encode_django_model)
except ImportError:
    pass

try:
    from bizerror import BizErrorBase
    register_global_encoder(BizErrorBase, encode_bizerror)
except ImportError:
    pass

try:
    from django.db.models import QuerySet
    register_global_encoder(QuerySet, encode_django_queryset)
except ImportError:
    pass

try:
    from django.db.models.sql.query import Query
    register_global_encoder(Query, encode_django_query)
except ImportError:
    pass


def make_simple_json_encoder(base_class=default_simple_json_encoder_base):
    library = JsonEncodeLibrary(base_class)
    register_simple_encoders(library)
    return library.get_encoder()

SimpleJsonEncoder = make_simple_json_encoder()
simple_json_dumps = partial(json.dumps, cls=SimpleJsonEncoder)

