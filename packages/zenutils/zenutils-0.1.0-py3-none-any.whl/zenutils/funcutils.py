#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
from zenutils.sixutils import *

import time
import functools
import logging
try:
    from inspect import signature
except ImportError:
    from inspect2 import signature # required by python 2.7 and python 3.2

__all__ = [
    "signature",
    "get_default_values",
    "get_inject_params",
    "call_with_inject",
    "mcall_with_inject",
    "classproperty",
    "chain",
    "BunchCallable",
    "try_again_on_error",
    "is_a_class",
    "get_builtins_dict",
    "get_all_builtin_exceptions",
    "get_class_name",
]

logger = logging.getLogger(__name__)

def get_default_values(func):
    """Get function parameters default value.

    In [1]: from zenutils import funcutils

    In [2]: def hi(name, msg="hi, {name}"):
    ...:     print(msg.format(name=name))
    ...:

    In [3]: funcutils.get_default_values(hi)
    Out[3]: {'msg': 'hi, {name}'}
    """
    data = {}
    parameters = signature(func).parameters
    for name, parameter in parameters.items():
        if parameter.default != parameter.empty:
            data[name] = parameter.default
    return data

def get_inject_params(func, data):
    """Get all params that required by calling the func from data.

    In [1]: from zenutils import funcutils

    In [2]: def hi(name, msg="hi, {name}"):
    ...:     print(msg.format(name=name))
    ...:

    In [3]: params = funcutils.get_inject_params(hi, data)

    In [4]: params
    Out[4]: {'name': 'Cissie', 'msg': 'hi, {name}'}

    In [5]: hi(**params)
    hi, Cissie

    """
    from zenutils import typingutils
    params = {}
    parameters = signature(func).parameters
    for name, parameter in parameters.items():
        if parameter.default is parameter.empty: # no default value, this parameter is required
            if not name in data:
                raise KeyError("Missing parameter: {name}".format(name=name))
            value = data[name]
        else:
            value = data.get(name, parameter.default)
        if not parameter.annotation is parameter.empty:
            value = typingutils.smart_cast(parameter.annotation, value, field_name=name)
        params[name] = value
    return params

def call_with_inject(func, data):
    """Call a func with parameters auto inject.
    """
    params = get_inject_params(func, data)
    return func(**params)

def mcall_with_inject(funcs, data):
    if not isinstance(funcs, (list, set, tuple)):
        funcs = [funcs]
    results = []
    for func in funcs:
        params = get_inject_params(func, data)
        result = func(**params)
        results.append(result)
    return results

class ClassPropertyDescriptor(object):

    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self

def classproperty(func):
    """classproperty decorator.

    class Bar(object):

        _bar = 1

        @classproperty
        def bar(cls):
            return cls._bar

        @bar.setter
        def bar(cls, value):
            cls._bar = value


    # test instance instantiation
    foo = Bar()
    assert foo.bar == 1

    baz = Bar()
    assert baz.bar == 1

    # test static variable
    baz.bar = 5
    assert foo.bar == 5

    # test setting variable on the class
    Bar.bar = 50
    assert baz.bar == 50
    assert foo.bar == 50
    """
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)

class chain(object):
    """
    """
    def __init__(self, *args):
        self.funcs = args
    
    def __call__(self, init_result, extra_args=None, extra_kwargs=None):
        extra_args = extra_args or []
        extra_kwargs = extra_kwargs or {}
        result = init_result
        for func in self.funcs:
            if func and callable(func):
                result = func(result, *extra_args, **extra_kwargs)
        return result

class BunchCallable(object):

    def __init__(self, *args, **kwargs):
        """BunchCallable init.

        @Returns:
            (None)
    
        @Parameters:
            args(Any, multiple):
            return_callback_results(bool, optional, default to False):
        """
        return_callback_results = kwargs.get("return_callback_results", False)
        self.return_callback_results = return_callback_results
        self.funcs = []
        for func in args:
            if isinstance(func, self.__class__):
                self.funcs += func.funcs
            else:
                self.funcs.append(func)

    def __call__(self, *args, **kwargs):
        results = []
        for func in self.funcs:
            if func and callable(func):
                result = func(*args, **kwargs)
            else:
                result = None
            results.append(result)
        if self.return_callback_results:
            return results
        else:
            return None

def try_again_on_error(sleep=5, limit=0, callback=None, callback_args=None, callback_kwargs=None):
    def outter_wrapper(func):
        def wrapper(*args, **kwargs):
            counter = 0
            while True:
                counter += 1
                try:
                    return func(*args, **kwargs)
                except InterruptedError:
                    logger.info("exit on got InterruptedError...")
                    break
                except Exception as error:
                    logger.exception("got unknown exception: {0}".format(str(error)))
                    if callback:
                        logger.info("call callback function {0} with params {1} {2}".format(str(callback), str(callback_args), str(callback_kwargs)))
                        local_callback_args = callback_args or []
                        local_callback_kwargs = callback_kwargs or {}
                        callback(*local_callback_args, **local_callback_kwargs)
                    time.sleep(sleep)
                if limit and counter >= limit:
                    break
        return functools.wraps(func)(wrapper)
    return outter_wrapper

def is_a_class(value):
    """Check the value, if it is a class or an instance of a class.

    @Returns:
        (bool): True means the value is a class. False means the value is an instance.
    
    @Parameters:
        value(Any): The value to be checked.
    
    @Example:
        assert is_a_class(uuid.UUID) is True
        assert is_a_class(uuid.uuid4()) is False
    """
    if value is type:
        return False
    return type(value) == type

def get_builtins_dict():
    """Get builtins data as dict typed.

    @Returns:
        (dict): All data in builtins.

    """
    data = {}
    if PY2: # no updates anymore...
        # keys are __builtins__ of python 2.7.18
        keys = ['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BufferError', 'BytesWarning', 'DeprecationWarning', 'EOFError', 'Ellipsis', 'EnvironmentError', 'Exception', 'False', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'NameError', 'None', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'ReferenceError', 'RuntimeError', 'RuntimeWarning', 'StandardError', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'ZeroDivisionError', '__debug__', '__doc__', '__import__', '__name__', '__package__', 'abs', 'all', 'any', 'apply', 'basestring', 'bin', 'bool', 'buffer', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'cmp', 'coerce', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'execfile', 'exit', 'file', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'intern', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'long', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'raw_input', 'reduce', 'reload', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'unichr', 'unicode', 'vars', 'xrange', 'zip']
        for key in keys:
            try:
                data[key] = eval(key)
            except:
                pass
    else:
        import builtins
        for key in dir(builtins):
            data[key] = getattr(builtins, key)
    return data

def get_all_builtin_exceptions():
    """Get all builtin exceptions.
    """
    def get_exceptions(scope):
        klasses = set()
        for key, value in scope.items():
            if key.startswith("_"):
                continue
            try:
                if issubclass(value, BaseException):
                    klasses.add(value)
            except TypeError: # some value can NOT be used in issubclass(xxx), just ignore it...
                pass
        return klasses
    es1 = get_exceptions(get_builtins_dict())
    es2 = get_exceptions(globals())
    es3 = get_exceptions(locals())
    return es1.union(es2).union(es3)

def get_class_name(klass, with_module=False):
    """Get a class's name.

    @Returns:
        (str): The name of the klass.
    
    @Parameters:
        klass(Any): A class or 
    """
    if not is_a_class(klass):
        klass = klass.__class__
    if with_module:
        return klass.__module__ + "." + klass.__name__
    else:
        return klass.__name__
