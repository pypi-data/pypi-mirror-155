#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
from zenutils.sixutils import *

import time
import random
import string
import unittest
from zenutils import randomutils

class TestRandomUtils(unittest.TestCase):

    def test01(self):
        password = "".join(randomutils.choices(string.ascii_letters, k=random.randint(4, 16)))
        length = random.randint(1, 1024) * 2
        gen1 = randomutils.Random(password)
        gen2 = randomutils.Random(password)
        data1 = gen1.get_bytes(length)
        data2 = gen2.get_bytes(length)
        assert len(data1) == length
        assert data1 == data2
    
    def test02(self):
        password = "".join(randomutils.choices(string.ascii_letters, k=random.randint(4, 16)))
        length = random.randint(1, 1024) * 2
        gen1 = randomutils.Random(password)
        gen2 = randomutils.Random(password)
        data1 = gen1.get_bytes(length)
        data21 = gen2.get_bytes(length//2)
        data22 = gen2.get_bytes(length//2)
        assert data1 == data21 + data22

    def test03(self):
        gen1 = randomutils.Random(5)
        gen2 = randomutils.Random(5)
        length = 10
        data1 = [gen1.random() for _ in range(length)]
        data2 = [gen2.random() for _ in range(length)]
        assert data1 == data2

    def test04(self):
        gen = randomutils.Random(time.time())
        length = 10
        multi = 1000
        values = [0] * length
        for _ in range(length*multi):
            value = gen.randint(length)
            values[value] += 1
        for value in values:
            assert value
        a = min(values)
        b = max(values)
        assert b - a < b * 0.2

    def test05(self):
        gen = randomutils.Random()
        old = set()
        counter = 0
        while counter < 10000 * 100:
            value = gen.random()
            assert value not in old
            old.add(value)
            counter += 1

    def test06(self):
        gen = randomutils.Random()
        data = bytearray(gen.get_bytes(102400))
        for p in range(256):
            assert p in data

    def test07(self):
        gen = randomutils.Random()
        c1 = gen.choice(string.ascii_letters)
        c2 = gen.choice(string.ascii_letters)
        assert c1 in string.ascii_letters

    def test08(self):
        gen = randomutils.Random()
        length = 8
        pwd1 = "".join(gen.choices(string.ascii_letters, k=length))
        pwd2 = "".join(gen.choices(string.ascii_letters, k=length))
        assert len(pwd1) == length
        assert pwd1 != pwd2

    def test09(self):
        gen = randomutils.Random()
        length = gen.randint(1000)
        thelist = list(range(length))
        gen.shuffle(thelist)
        for x in range(length):
            assert x in thelist

    def test10(self):
        length = 10000 * 100
        gen = randomutils.Random()
        seeds = set()
        for x in range(length):
            value = gen.random()
            seeds.add(value)
        assert len(seeds) == length

    def test11(self):
        uuidgen = randomutils.UuidGenerator()
        uuids = set()
        for i in range(10000*10):
            uid = uuidgen.next()
            assert not uid in uuids
            uuids.add(uid)

    def test12(self):
        n = 100000
        uuidgen = randomutils.UuidGenerator()
        uuids = set(uuidgen.next(n))
        assert len(uuids) == n

    def test13(self):
        n1 = 0
        n2 = -1
        n3 = -100000
        uuidgen = randomutils.UuidGenerator()
        uuids1 = set(uuidgen.next(n1))
        uuids2 = set(uuidgen.next(n2))
        uuids3 = set(uuidgen.next(n3))
        assert len(uuids1) == 0
        assert len(uuids2) == 0
        assert len(uuids3) == 0

    def test14(self):
        thelist = ["a"]
        assert randomutils.choices(thelist, k=0) == []
        assert randomutils.choices(thelist, k=1) == ["a"]
        assert randomutils.choices(thelist, k=2) == ["a", "a"]
        assert randomutils.choices(thelist, k=3) == ["a", "a", "a"]


    def test15(self):
        password = "hello"
        value = 8141294968645153005348737041137229874925484556329662733687648891656190967473008484003711490685970494114845896430057820193510284132416327087093833302720579
        assert randomutils.Random.get_seed(password) == value

        password = "world"
        value = 917621815894390898271268045579761300172305340683275565896802420972662387591329011865249652589391928780576967173433776051555728720648442640225828065134318
        assert randomutils.Random.get_seed(password) == value

        password = ""
        value = 10868450558671247443152026947160338505683745266658651051718065983487878962987857602829315249215796444208488632888003673539585986066311769564391053988452926
        assert randomutils.Random.get_seed(password) == value

        password = "a"
        value = 1636897152625920295465748920275349232570945140773800183880278231231037334490840639395121881466231859643176795512242694658460339042012321358445155903773301
        assert randomutils.Random.get_seed(password) == value

    def test16(self):
        seed = randomutils.Random.get_seed(None)
        assert type(seed) == float

        seed = randomutils.Random.get_seed(12345678)
        assert seed == 12345678

        seed = randomutils.Random.get_seed(12345678.981)
        assert seed == 12345678.981
    