#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from duckiebot.skeleton import fib

__author__ = "gregoryjhansell97"
__copyright__ = "gregoryjhansell97"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
