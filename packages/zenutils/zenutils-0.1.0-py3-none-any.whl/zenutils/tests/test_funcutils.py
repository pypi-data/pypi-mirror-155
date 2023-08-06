#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement

from py import builtin
from zenutils.sixutils import *

import uuid
import unittest
from zenutils import funcutils


class TestFuncUtils(unittest.TestCase):
    def test01(self):
        def s(a, b):
            return a + b
        data = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        params = funcutils.get_inject_params(s, data)
        assert params["a"] == 1
        assert params["b"] == 2

        result = funcutils.call_with_inject(s, data)
        assert result == 3

    def test02(self):
        def s(a, b=2):
            return a + b
        data = {
            "a": 1,
            "c": 3,
        }
        params = funcutils.get_inject_params(s, data)
        assert params["a"] == 1
        assert params["b"] == 2

        result = funcutils.call_with_inject(s, data)
        assert result == 3

    def test03(self):
        def s(a, b=2):
            return a + b
        data = {
            "a": 1,
            "c": 2,
        }
        params = funcutils.get_inject_params(s, data)
        assert params["a"] == 1
        assert params["b"] == 2

        result = funcutils.call_with_inject(s, data)
        assert result == 3

    def test04(self):
        def hi(msg="hi"):
            pass
        assert funcutils.get_default_values(hi)["msg"] == "hi"
    
        def add(a=0, b=0):
            pass
        data = funcutils.get_default_values(add)
        assert data["a"] == 0
        assert data["b"] == 0

        def sub(a, b):
            pass
        data = funcutils.get_default_values(sub)
        assert data == {}

        def multi(a, b=1):
            pass
        data = funcutils.get_default_values(multi)
        assert data["b"] == 1
        assert not "a" in data

    def test05(self):
        def incr(value):
            return value + 1
        def decr(value):
            return value - 2
        
        assert funcutils.chain(incr, decr)(3) == 2
        assert funcutils.chain(incr, decr)(0) == -1
    

        def incr(value, *args, **kwargs):
            incr_delta = kwargs.get("incr_delta", 0)
            return value + incr_delta
        def decr(value, *args, **kwargs):
            decr_delta = kwargs.get("decr_delta", 0)
            return value - decr_delta
        extra_kwargs = {
            "incr_delta": 1,
            "decr_delta": 2,
        }
        assert funcutils.chain(incr, decr)(3, extra_kwargs=extra_kwargs) == 2
        assert funcutils.chain(incr, decr)(0, extra_kwargs=extra_kwargs) == -1

    def test06(self):

        class Summer(object):
            def __init__(self):
                self.total = 0
            def add(self):
                self.total += 1
            def add2(self):
                self.total += 2

        summer = Summer()
        add3 = funcutils.BunchCallable(summer.add, summer.add2)
        add3()
        assert summer.total == 3

        add4 = funcutils.BunchCallable(add3, summer.add)
        add4()
        assert summer.total == 7

        add6 = funcutils.BunchCallable(add4, summer.add2)
        add6()
        assert summer.total == 13

    def test07(self):
        class Bar(object):

            _bar = 1

            @funcutils.classproperty
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

    def test08(self):
        assert funcutils.is_a_class(type) is False
        assert funcutils.is_a_class(uuid.UUID) is True
        assert funcutils.is_a_class(uuid.uuid4()) is False
        assert funcutils.is_a_class(str) is True
        assert funcutils.is_a_class(type(str)) is False
        assert funcutils.is_a_class("hello") is False
        assert funcutils.is_a_class(b"hello") is False

        class A(object):
            pass
        assert funcutils.is_a_class(A) is True
        assert funcutils.is_a_class(A()) is False

    def test09(self):
        es = funcutils.get_all_builtin_exceptions()
        assert Exception in es
        assert TypeError in es
        assert RuntimeError in es
        assert BaseException in es

    def test10(self):
        builtins = funcutils.get_builtins_dict()

        assert "True" in builtins
        assert "False" in builtins
        assert "None" in builtins
        assert "int" in builtins
        assert "zip" in builtins

        assert "BaseException" in builtins
        assert "Exception" in builtins
        assert "RuntimeError" in builtins

    def test11(self):
        assert funcutils.get_class_name(Exception) == "Exception"
        assert funcutils.get_class_name(Exception()) == "Exception"
        class A(object):
            pass
        assert funcutils.get_class_name(A) == "A"
        assert funcutils.get_class_name(A()) == "A"
