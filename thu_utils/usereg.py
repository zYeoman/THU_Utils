#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from hashlib import md5
from prettytable import PrettyTable
from bs4 import BeautifulSoup
from .user import User


class Usereg(object):
    """Usereg for usereg.tsinghua.edu.cn"""

    def __init__(self, user=None):
        self._user = user if user is not None else User()
        self._session = requests.session()
        self._base = 'https://usereg.tsinghua.edu.cn/'
        self._login_url = self._base + 'do.php'

    def __del__(self):
        self._session.close()

    def login(self, user=None):
        if user is None:
            user = self._user
        data = {
            'action': 'login',
            'user_login_name': self._user.username,
            'user_password': md5(self._user.password).hexdigest(),
        }
        req = self._session.post(self._login_url, data)
        return req.text

    def logout(self):
        data = {
            'action': 'logout'
        }
        req = self._session.post(self._login_url, data)
        return req.text

    @property
    def iplist(self):
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
        output = '请登录先'
        for _, lst in enumerate(self.iplist):
            lst = lst[0:4] + lst[-6:]
            if _ == 0:
                output = PrettyTable(lst)
            else:
                output.add_row(lst)
        print(output)


    def ipdown(self, ip):
        url = self._base + 'online_user_ipv4.php'
        index = None

        if ip.isdigit():
            index = int(ip)
            ipr = list(self.iplist)[index]
            ip = ipr[0]

        values = {
            'action': 'drop',
            'user_ip': ip
        }
        req = self._session.post(url, values)
        return req.text

