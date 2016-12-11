#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Info
Tool for info.tsinghua.edu.cn

methods:
    login: Login to info.tsinghua.edu.cn
    logout: Logout from info.tsinghua.edu.cn
    show: Show
"""

import requests

from .user import User


class Info(object):
    """Info for info.tsinghua.edu.cn"""

    def __init__(self, user=None):
        """init Info
        :param user: User info
        """
        self._user = user if user is not None else User()
        self._session = requests.session()
        self._base = 'http://info.tsinghua.edu.cn/'
        self._login_url = self._base + 'Login'
        self._logout_url = self._base + 'prelogout.jsp'

    def __del__(self):
        """uninit Info
        close socket session
        """
        self._session.close()

    def login(self, user=None):
        """login info.tsinghua.edu.cn
        :param user: User info
        :return: response text
        """
        if user is None:
            user = self._user
        data = {
            'redirect': 'NO',
            'userName': user.username,
            'password': user.password,
            'x': '31',
            'y': '11'
        }
        req = self._session.post(self._login_url, data)
        return req.text

    def logout(self):
        """logout info.tsinghua.edu.cn
        :return: response text
        """
        req = self._session.get(self._logout_url)
        return req.text
