#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test thu_utils

usage:
    python -m unittest test.py
    python -m unittest test.TestTHU.testuser
"""

import unittest

from context import thu_utils


class TestTHU(unittest.TestCase):
    """Unittest for thu_utils"""

    def test_net(self):
        """test Net"""
        net = thu_utils.Net()
        net.logout()
        self.assertEqual(net.login(), 'Login is successful.')
        self.assertEqual(net.login(), 'IP has been online, please logout.')
        net.show()
        self.assertEqual(net.logout(), 'Logout is successful.')
        self.assertEqual(net.logout(), 'You are not online.')
        net.show()

    def test_learn(self):
        """test Learn"""
        # TODO: test learn
        pass

    def test_usereg(self):
        """test Usereg"""
        # TODO: test Usereg
        usereg = thu_utils.Usereg()
        usereg.show()


if __name__ == "__main__":
    unittest.main()
