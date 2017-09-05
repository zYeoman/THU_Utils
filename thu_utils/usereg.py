#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Usereg
Info of usereg.tsinghua.edu.cn

methods:
  login: Login to usereg.tsinghua.edu.cn
  logout: Logout from usereg.tsinghua.edu.cn
  show: Show all online ip of usereg
  ipdown: Send logout to ip.
"""

from hashlib import md5
from prettytable import PrettyTable
from bs4 import BeautifulSoup

from .base import THUBase


class Usereg(THUBase):
    """Usereg for usereg.tsinghua.edu.cn"""

    def __init__(self, user=None):
        """init Usereg
        :param user: User info
        """
        super(Usereg, self).__init__(user)
        self._base = 'https://usereg.tsinghua.edu.cn/'
        self._login_url = self._base + 'do.php'

    def login(self):
        """login usereg.tsinghua.edu.cn
        :param user: User info
        :return: response text
        """
        data = {
            'action': 'login',
            'user_login_name': self._user.username,
            'user_password': md5(self._user.password).hexdigest(),
        }
        req = self._session.post(self._login_url, data)
        return req.text

    def logout(self):
        """logout usereg.tsinghua.edu.cn
        :return: response text
        """
        data = {'action': 'logout'}
        req = self._session.post(self._login_url, data)
        return req.text

    @property
    def iplist(self):
        """iplist of online ip
        :return: [] not login or iterator of ip info
        """
        url = self._base + 'online_user_ipv4.php'
        req = self._session.get(url)
        if req.text == '请登录先':
            return []
        tree = BeautifulSoup(req.content, 'html.parser')
        rows = tree.body.table.find_all('table')[1].find_all('tr')
        for row in rows:
            values = [x.string.strip() for x in row.find_all('td') if x.string]
            yield values

    def show(self):
        """show info of online ip
        :return: None
        """
        output = None
        for _, lst in enumerate(self.iplist):
            lst = lst[0:4] + lst[-6:]
            if _ == 0:
                output = PrettyTable(lst)
            else:
                output.add_row(lst)
        if output is None:
            print('请先登录')
        else:
            print(output)

    def ipdown(self, ip_str=None, index=None):
        """send logout request to usereg.tsinghua.edu.cn
        :param ip_str: str ip "127.0.0.1"
        :param index:  index of iplist
        :return: response text
        """
        url = self._base + 'online_user_ipv4.php'

        if index is not None:
            ip_str = list(self.iplist)[index][0]

        values = {'action': 'drop', 'user_ip': ip_str}
        req = self._session.post(url, values)
        return req.text
