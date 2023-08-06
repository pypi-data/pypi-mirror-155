#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 fx-kirin <fx.kirin@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""


def get_nehaba_limit(last_execution):
    if last_execution < 200:
        return 5
    if last_execution < 500:
        return 8
    if last_execution < 700:
        return 10
    if last_execution < 1000:
        return 15
    if last_execution < 1500:
        return 30
    if last_execution < 2000:
        return 40
    if last_execution < 3000:
        return 50
    if last_execution < 5000:
        return 70
    if last_execution < 7000:
        return 100
    if last_execution < 10000:
        return 150
    if last_execution < 15000:
        return 300
    if last_execution < 20000:
        return 400
    if last_execution < 30000:
        return 500
    if last_execution < 50000:
        return 700
    if last_execution < 70000:
        return 1000
    if last_execution < 100000:
        return 1500
    if last_execution < 150000:
        return 3000
    if last_execution < 200000:
        return 4000
    if last_execution < 300000:
        return 5000
    if last_execution < 500000:
        return 7000
    if last_execution < 700000:
        return 10000
    if last_execution < 1000000:
        return 15000
    if last_execution < 1500000:
        return 30000
    if last_execution < 2000000:
        return 40000
    if last_execution < 3000000:
        return 50000
    if last_execution < 5000000:
        return 70000
    if last_execution < 7000000:
        return 100000
    if last_execution < 10000000:
        return 150000
    if last_execution < 15000000:
        return 300000
    if last_execution < 20000000:
        return 400000
    if last_execution < 30000000:
        return 500000
    if last_execution < 50000000:
        return 700000
    return 1000000


def get_price_limit(last_execution):
    if last_execution < 100:
        return 30
    if last_execution < 200:
        return 50
    if last_execution < 500:
        return 80
    if last_execution < 700:
        return 100
    if last_execution < 1000:
        return 150
    if last_execution < 1500:
        return 300
    if last_execution < 2000:
        return 400
    if last_execution < 3000:
        return 500
    if last_execution < 5000:
        return 700
    if last_execution < 7000:
        return 1000
    if last_execution < 10000:
        return 1500
    if last_execution < 15000:
        return 3000
    if last_execution < 20000:
        return 4000
    if last_execution < 30000:
        return 5000
    if last_execution < 50000:
        return 7000
    if last_execution < 70000:
        return 10000
    if last_execution < 100000:
        return 15000
    if last_execution < 150000:
        return 30000
    if last_execution < 200000:
        return 40000
    if last_execution < 300000:
        return 50000
    if last_execution < 500000:
        return 70000
    if last_execution < 700000:
        return 100000
    if last_execution < 1000000:
        return 150000
    if last_execution < 1500000:
        return 300000
    if last_execution < 2000000:
        return 400000
    if last_execution < 3000000:
        return 500000
    if last_execution < 5000000:
        return 700000
    if last_execution < 7000000:
        return 1000000
    if last_execution < 10000000:
        return 1500000
    if last_execution < 15000000:
        return 3000000
    if last_execution < 20000000:
        return 4000000
    if last_execution < 30000000:
        return 5000000
    if last_execution < 50000000:
        return 7000000
    return 10000000
