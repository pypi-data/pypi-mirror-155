#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 fx-kirin <fx.kirin@gmail.com>
#

import logging
import os

import kanilog
import numpy as np
import pytest
import stdlogging
from add_parent_path import add_parent_path

with add_parent_path():
    import ktools.numpy


def setup_module(module):
    pass


def teardown_module(module):
    pass


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_func():
    choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, np.nan]
    a = np.random.choice(choices, size=(1000, 10, 10))
    ktools.numpy.ffill(a)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    kanilog.setup_logger(logfile='/tmp/%s.log' % (os.path.basename(__file__)), level=logging.INFO)
    stdlogging.enable()

    pytest.main([__file__, '-k test_', '-s'])
# Sample Test passing with nose and pytest
