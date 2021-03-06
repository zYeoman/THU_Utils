#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Net
Tool for net.tsinghua.edu.cn

methods:
  login: Login to net.tsinghua.edu.cn
  logout: Logout from net.tsinghua.edu.cn
  show: Show current state
"""

from hashlib import md5

from .base import THUBase
from .logger import LOG


class Net(THUBase):
    """Net for net.tsinghua.edu.cn"""

    def __init__(self, user=None):
        """init Net
        :param user: User info
        """
        super(Net, self).__init__(user)
        self._base = 'https://net.tsinghua.edu.cn/'
        self._login_url = self._base + 'do_login.php'

    def show(self):
        """show net.tsinghua.edu.cn info
        :return: None
        """
        req = self._session.post(self._login_url, {'action': 'check_online'})
        print(req.text)
        if req.text != 'not_online':
            req = self._session.post(self._base + 'rad_user_info.php')
            info = req.text.split(',')
            traffic = int(info[6]) / 1000000000
            timelen = int(info[2]) - int(info[1])
            timelen_str = '{}:{}:{}'.format(timelen // 3600, timelen // 60 %
                                            60, timelen % 60)
            info_str = 'ip={0[8]},user={0[0]},traffic={1:.2f}GB,timelen={2}'
            info_str = info_str.format(info, traffic, timelen_str)
            print(info_str)

    def login(self):
        """login net.tsinghua.edu.cn
        :param user: User info
        :return: response text
        """
        data = {
            'action': 'login',
            'username': self._user.username,
            'password': '{MD5_HEX}' + md5(self._user.password).hexdigest(),
            'ac_id': 1
        }
        req = self._session.post(self._login_url, data)
        LOG.info(req.text)
        return req.text

    def logout(self):
        """logout net.tsinghua.edu.cn
        :return: response text
        """
        data = {'action': 'logout'}
        req = self._session.post(self._login_url, data)
        LOG.info(req.text)
        return req.text
