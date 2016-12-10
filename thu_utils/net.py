#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hashlib import md5
from collections import namedtuple
import requests

from .user import User


class Net(object):
    """Net for net.tsinghua.edu.cn"""

    def __init__(self, user=None):
        self._user = user if user is not None else User()
        self._session = requests.session()
        self._base = 'http://net.tsinghua.edu.cn/'
        self._login_url = self._base + 'do_login.php'

    def __del__(self):
        self._session.close()

    def show(self):
        req = self._session.post(self._login_url, {'action':'check_online'})
        print(req.text)
        if req.text != 'not_online':
            req = self._session.post(self._base + 'rad_user_info.php')
            info = req.text.split(',')
            traffic = int(info[6])/1000000000
            timelen = int(info[2]) - int(info[1])
            timelen_str = '{}:{}:{}'.format(timelen//3600,timelen//60%60,timelen%60)
            info_str = 'NetUsage(ip={0[8]},user={0[0]},traffic={1:.2f}GB,timelen={2})'
            info_str = info_str.format(info, traffic, timelen_str)
            print(info_str)

    def login(self):
        data = {
            'action': 'login',
            'username': self._user.username,
            'password': '{MD5_HEX}' + md5(self._user.password).hexdigest(),
            'ac_id': 1
        }
        req = self._session.post(self._login_url, data)
        return req.text

    def logout(self):
        data = {'action': 'logout'}
        req = self._session.post(self._login_url, data)
        return req.text

