# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2020/7/22 16:13
:LastEditTime: 2020/7/22 16:13
:LastEditors: SunYiTan
:Description: 随机帮助类
"""

from bintrees import RBTree
import random


class RollHelp:

    def __init__(self):
        self.sum = 0
        self.rbTree = RBTree()

    def add_weight(self, odds, obj):
        self.sum += odds
        self.rbTree.insert(self.sum, obj)

    def get_roll(self):
        if self.sum > 0:
            rand = random.randint(1, self.sum)
            return self.rbTree.ceiling_item(rand)[1]

        else:
            return None
