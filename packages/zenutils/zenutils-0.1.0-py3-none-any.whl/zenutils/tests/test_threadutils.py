#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
from zenutils.sixutils import *



import time
import unittest
import threading
try:
    from queue import Queue
    from queue import Empty
except ImportError:
    from Queue import Queue
    from Queue import Empty


from zenutils import threadutils

class TestThreadUtils(unittest.TestCase):

    def test01(self):
        numbers = []
        meta = {
            "max_number": 10**9,
            "number": 1,
        }
        def get_numbers(ma, ns):
            if ma["number"] <= meta["max_number"]:
                ns.append(meta["number"])
                ma["number"] += 1
        service = threadutils.Service(service_loop=get_numbers, service_loop_kwargs={
            "ma": meta,
            "ns": numbers,
        }, service_loop_interval=0)
        service.start()
        len0 = len(numbers)
        time.sleep(5)
        len1 = len(numbers)
        assert len1 > len0
        service.stop()
        len11 = len(numbers)
        time.sleep(5)
        len12 = len(numbers)
        assert len11 == len12
        service.start()
        time.sleep(5)
        len2 = len(numbers)
        assert len2 > len1
        service.terminate()
        assert service.is_running == False
        assert service.terminated_time
        assert service.service_thread.is_alive() == False
        len3 = len(numbers)
        time.sleep(5)
        len4 = len(numbers)
        assert len4 == len3
        s1 = sum(numbers)
        s2 = (len(numbers)+1)*len(numbers)/2
        assert s1 == s2

    def test02(self):
        number_counter = threadutils.Counter()
        number_queue = Queue()

        class NumberPut(threadutils.SimpleProducer):
            def __init__(self, number_counter, **kwargs):
                self.number_counter = number_counter
                super(NumberPut, self).__init__(**kwargs)
    
            def produce(self):
                return [self.number_counter.incr()]
    
        class NumberGet(threadutils.SimpleConsumer):
            def __init__(self, number_queue, **kwargs):
                self.number_queue = number_queue
                super(NumberGet, self).__init__(**kwargs)
            
            def consume(self, task):
                self.number_queue.put(task)

        server = threadutils.SimpleProducerConsumerServer(
            producer_class=NumberPut,
            consumer_class=NumberGet,
            producer_class_init_kwargs={"number_counter": number_counter, "service_loop_interval": 0},
            consumer_class_init_kwargs={"number_queue": number_queue, "service_loop_interval": 0},
            queue_size=0,
            )
        server.start()
        time.sleep(5)
        server.stop()
        assert number_counter.value == number_queue.qsize()

    def test03(self):
        number_counter = threadutils.Counter()
        number_queue = Queue()
        def NumberPut(number_counter):
            return [number_counter.incr()]
        def NumberGet(task, number_queue):
            number_queue.put(task)
        server = threadutils.SimpleProducerConsumerServer(
            produce=NumberPut,
            produce_kwargs={"number_counter": number_counter},
            consume=NumberGet,
            consume_kwargs={"number_queue": number_queue},
            service_loop_interval=0,
            queue_size=0,
            )
        server.start()
        time.sleep(5)
        server.stop()
        assert number_counter.value == number_queue.qsize()
 
    def test04(self):
        number_counter = threadutils.Counter()
        number_queue = Queue()
        def number_generate(size):
            for i in range(size):
                value = number_counter.incr()
                number_queue.put(value)
        tsnum = 10
        tsize = 10000
        ts = []
        for _ in range(tsnum):
            t = threading.Thread(target=number_generate, args=[tsize])
            t.start()
            ts.append(t)
        for t in ts:
            t.join()
        ns = set()
        while True:
            try:
                ns.add(number_queue.get(block=False))
            except Empty:
                break
        assert len(ns) == tsnum * tsize

    def test05(self):
        c = threadutils.Counter()
        c.incr()
        assert c.value == 1
        c.incr()
        assert c.value == 2
        c.decr()
        assert c.value == 1
        c.decr()
        assert c.value == 0
