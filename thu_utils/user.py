#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import pickle
import getpass


class User(object):
    """Contain username and password."""

    def __init__(self, path='.thu'):
        """
        init User

        :path: where to store username and password.

        """
        self._path = path
        home = os.path.expanduser('~')
        self._filename = os.path.join(home, self._path)
        self._data = self._load()

    def _load(self):
        if not os.path.exists(self._filename):
            self.set_user()
        with open(self._filename, 'rb') as file:
            return pickle.load(file)

    def _store(self):
        with open(self._filename, 'wb') as file:
            pickle.dump(self._data, file)
        os.chmod(self._filename, 0o600)

    def set_user(self):
        username = input('Username: ').encode()
        password = getpass.getpass().encode()
        self._data['username'] = username
        self._data['password'] = password
        self._store()

    @property
    def username(self):
        return self._data['username']

    @property
    def password(self):
        return self._data['password']

    def show(self):
        print(self._data['username'].decode())
