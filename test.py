#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import thu_utils

class TestTHU(unittest.TestCase):

    """Unittest for thu_utils"""

    def test_user(self):
        thu_utils.user.input = lambda _:'test'
        thu_utils.user.getpass.getpass = lambda :'test'
        user = thu_utils.User('.test_thu')
        self.assertEqual(user.username, b'test')
        self.assertEqual(user.password, b'test')
        user.del_user()

    def test_net(self):
        net = thu_utils.Net()
        net.logout()
        self.assertEqual(net.login(), 'Login is successful.')
        self.assertEqual(net.login(), 'IP has been online, please logout.')
        net.show()
        self.assertEqual(net.logout(), 'Logout is successful.')
        self.assertEqual(net.logout(), 'You are not online.')
        net.show()

    def test_learn(self):
        pass

    def test_usereg(self):
        usereg = thu_utils.Usereg()
        usereg.show()
