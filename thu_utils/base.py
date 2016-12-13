#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""THUBase
Base class for other

methods:
    login: Login
    logout: Logout
    show: Show
"""

import requests

from .user import User


class THUBase(object):
    """Base class for other class"""

    def __init__(self, user=None):
        """init Base
        :param user: User info
        """
        self._user = user if user is not None else User()
        self._session = requests.session()

    def __del__(self):
        """uninit Base
        close socket session
        """
        self._session.close()
