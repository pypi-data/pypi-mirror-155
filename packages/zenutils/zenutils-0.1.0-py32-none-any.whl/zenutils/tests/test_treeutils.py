#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
from zenutils.sixutils import *


import unittest
from zenutils import treeutils

class TestTreeUtils(unittest.TestCase):
    def test01(self):
        thelist = [
            {"id": 1, "title": "a"},
            {"id": 2, "title": "b"},
            {"id": 3, "title": "a.a", "parent_id": 1},
            {"id": 4, "title": "b.a", "parent_id": 2},
            {"id": 5, "title": "a.a.a", "parent_id": 3},
            {"id": 6, "title": "a.a.b", "parent_id": 3},
            {"id": 7, "title": "a.a.c", "parent_id": 3},
            {"id": 8, "title": "c"},
            {"id": 9, "title": "a.a.b.a", "parent_id": 6},
            {"id": 10, "title": "b.a.a", "parent_id": 4},
            {"id": 11, "title": "d"},
        ]
        tree = treeutils.build_tree(thelist)
        treeutils.print_tree(tree)
        title = tree[0]["children"][0]["children"][1]["children"][0]["title"]
        assert title  == "a.a.b.a"

    def test02(self):
        ## if the node's parent_id is not in current list, then the node is treated as root node.
        thelist = [
            {"id": 1, "title": "a", "parent_id": 4},
            {"id": 2, "title": "b", "parent_id": 4},
            {"id": 3, "title": "c", "parent_id": 5},
        ]
        tree = treeutils.build_tree(thelist)
        assert tree[0]["title"] == "a"
        assert tree[1]["title"] == "b"
        assert tree[2]["title"] == "c"
