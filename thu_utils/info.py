#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Info
Tool for info.tsinghua.edu.cn

methods:
    login: Login to info.tsinghua.edu.cn
    logout: Logout from info.tsinghua.edu.cn
    show: Show
"""

from .base import THUBase
from .logger import LOG


class Info(THUBase):
    """Info for info.tsinghua.edu.cn"""

    def __init__(self, user=None):
        """init Info
        :param user: User info
        """
        super(Info, self).__init__(user)
        self._base = 'http://info.tsinghua.edu.cn/'
        self._login_url = self._base + 'Login'
        self._logout_url = self._base + 'prelogout.jsp'

    def login(self):
        """login info.tsinghua.edu.cn
        :param user: User info
        :return: response text
        """
        data = {
            'redirect': 'NO',
            'userName': self._user.username,
            'password': self._user.password,
            'x': '31',
            'y': '11'
        }
        req = self._session.post(self._login_url, data)
        LOG.info(req.text)
        return req.text

    def logout(self):
        """logout info.tsinghua.edu.cn
        :return: response text
        """
        req = self._session.get(self._logout_url)
        LOG.info(req.text)
        return req.text
