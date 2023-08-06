#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
from zenutils.sixutils import *

import os
import uuid
import random
import unittest
from zenutils import hashutils


class TestHashUtils(unittest.TestCase):

    def test01(self):
        text = hashutils.get_md5()
        assert text == "d41d8cd98f00b204e9800998ecf8427e"

    def test02(self):
        text = hashutils.get_md5(b"a")
        assert text == "0cc175b9c0f1b6a831c399e269772661"

    def test03(self):
        text = hashutils.get_md5("a", b"b")
        assert text == "187ef4436122d1cc2f40dc2b92f0eba0"

    def test04(self):
        text = hashutils.get_md5("a", "b", 1)
        assert text == "68b6a776378decbb4a79cda89087c4ce"

    def test05(self):
        text = hashutils.get_sha1("a", 1, True)
        assert text == "3251aeb0f68984b60d7cb2ed7f2505bee819a7c7"
    
    def test06(self):
        text = hashutils.get_sha1_base64("a", 1, True, 0.01)
        assert text == "yrZxIUBkyZ03qTIMbYORcBdnFRc="

    def test07(self):
        text = hashutils.get_pbkdf2_hmac("testpassword", salt="bPBMORgAZP53", iterations=150000, hash_name="sha256")
        assert text == "pbkdf2_sha256$150000$bPBMORgAZP53$yPCstMcQYC9Rgn0h2mT0egPjUdW5T7WUiViib9Sn0dM="

    def test08(self):
        text = hashutils.get_pbkdf2_sha256("testpassword", salt="bPBMORgAZP53", iterations=150000)
        assert text == "pbkdf2_sha256$150000$bPBMORgAZP53$yPCstMcQYC9Rgn0h2mT0egPjUdW5T7WUiViib9Sn0dM="
  
    def test09(self):
        text = hashutils.get_pbkdf2_sha256("just a test")
        assert hashutils.validate_pbkdf2_sha256("just a test", text)

    def test10(self):
        text = hashutils.get_pbkdf2_md5("just a test")
        assert hashutils.validate_pbkdf2_md5("just a test", text)

        text = hashutils.get_pbkdf2_md5(b"just a test")
        assert hashutils.validate_pbkdf2_md5(b"just a test", text)

        text = hashutils.get_pbkdf2_md5(b"just a test")
        assert hashutils.validate_pbkdf2_md5("just a test", text)

        text = hashutils.get_pbkdf2_md5("just a test")
        assert hashutils.validate_pbkdf2_md5(b"just a test", text)

    def test11(self):
        assert "5vNnRsy6QsKIrPkG5ja7J46ut+g=" == hashutils.get_sha1_base64(b"just a test")
        assert "5vNnRsy6QsKIrPkG5ja7J46ut+g=" == hashutils.get_sha1_base64("just a test")

    def test12(self):
        filename = "{0}.txt".format(str(uuid.uuid4()))
        try:
            length = random.randint(0, 1024*1024*16)
            stream = os.urandom(length)
            with open(filename, "wb") as fobj:
                fobj.write(stream)
            code1 = hashutils.get_file_md5(filename)
            code2 = hashutils.get_md5(stream)
            assert code1 == code2

            code3 = hashutils.get_file_sha(filename)
            code4 = hashutils.get_sha1(stream)
            assert code3 == code4
        finally:
            if os.path.exists(filename):
                os.unlink(filename)

    def test13(self):
        assert hashutils.method_load("md5") == hashutils.method_load(b"md5")
        assert hashutils.method_load("sha1") == hashutils.method_load(b"sha1")
        assert hashutils.method_load("sha256") == hashutils.method_load(b"sha256")
