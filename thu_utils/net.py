#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hashlib import md5
from collections import namedtuple
from urllib.request import urlopen, Request
from urllib.parse import urlencode

from .user import User


class Net(object):
    """Net for net.tsinghua.edu.cn"""

    def __init__(self, user=None):
        self._user = user if user is not None else User()
        self._base = 'http://net.tsinghua.edu.cn/'
        self._login_url = self._base + 'do_login.php'
        self._net_usage = namedtuple('NetUsage', 'ip user traffic timelen')

    def show(self):
        req = Request(self._login_url, b'action=check_online')
        resp = urlopen(req).read().decode()
        print(resp)
        if resp != 'not_online':
            req = Request(self._base + 'rad_user_info.php', b'')
            resp = urlopen(req).read().decode()
            info = resp.split(',')
            info = self._net_usage(*[
                info[8], info[0], int(info[6]) / 1000000000,
                int(info[2]) - int(info[1])
            ])
            print(info)

    def login(self):
        data = urlencode({
            'action': 'login',
            'username': self._user.username,
            'password': '{MD5_HEX}' + md5(self._user.password).hexdigest(),
            'ac_id': 1
        })
        req = Request(self._login_url, data.encode())
        return urlopen(req).read().decode()

    def logout(self):
        date = urlencode({'action': 'logout'})
        req = Request(self._login_url, date.encode())
        return urlopen(req).read().decode()
