#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Its
Tool for its.tsinghua.edu.cn

methods:
    login: Login to its.tsinghua.edu.cn
    logout: Logout from its.tsinghua.edu.cn
    show: Show
"""

import requests

from .user import User
from .base import THUBase


class Its(THUBase):
    """Its for its.tsinghua.edu.cn"""

    def __init__(self, user=None):
        """init Its
        :param user: User info
        """
        super(Its, self).__init__(user)
        self._base = 'http://its.tsinghua.edu.cn/'
        self._login_url = self._base + 'loginAjax'
        self._logout_url = self._base + 'logout'
        self._columns = ['czxt', 'fbdrj', 'kfrj', 'bgrj', 'jsrj']

    def login(self, user=None):
        """login its.tsinghua.edu.cn
        :param user: User info
        :return: response text
        """
        if user is None:
            user = self._user
        data = {
            'username': user.username,
            'password': user.password
        }
        req = self._session.post(self._login_url, data)
        return req.text

    def logout(self):
        """logout its.tsinghua.edu.cn
        :return: response text
        """
        req = self._session.get(self._logout_url)
        return req.text
