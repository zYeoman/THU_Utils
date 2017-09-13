#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Its
Tool for its.tsinghua.edu.cn

methods:
    login: Login to its.tsinghua.edu.cn
    logout: Logout from its.tsinghua.edu.cn
    show: Show
"""

from .base import THUBase
from .logger import LOG


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

    def login(self):
        """login its.tsinghua.edu.cn
        :return: response text
        """
        data = {
            'username': self._user.username,
            'password': self._user.password
        }
        req = self._session.post(self._login_url, data)
        LOG.info(req.text)
        return req.text

    def logout(self):
        """logout its.tsinghua.edu.cn
        :return: response text
        """
        req = self._session.get(self._logout_url)
        LOG.info(req.text)
        return req.text
