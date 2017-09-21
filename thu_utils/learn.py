#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup, Comment

from .user import User
from .logger import LOG

# global vars
_session = requests.session()
_URL_BASE_ = 'http://learn.tsinghua.edu.cn'
_URL_BASE = 'http://learn.tsinghua.edu.cn/MultiLanguage'
_URL_LOGIN = '/lesson/teacher/loginteacher.jsp'

# 学期
_URL_CURRENT_SEMESTER = '/lesson/student/MyCourse.jsp?typepage=1'
_URL_PAST_SEMESTER = '/lesson/student/MyCourse.jsp?typepage=2'
# 个人信息
_URL_PERSONAL_INFO = '/vspace/vspace_userinfo1.jsp'

# 课程不同板块前缀
# 课程公告
_PREF_MSG = '/public/bbs/getnoteid_student.jsp?course_id='
# 课程信息
_PREF_INFO = '/lesson/student/course_info.jsp?course_id='
# 课程文件
_PREF_FILES = '/lesson/student/download.jsp?course_id='
# 教学资源
_PREF_LIST = '/lesson/student/ware_list.jsp?course_id='
# 课程作业
_PREF_WORK = '/lesson/student/hom_wk_brw.jsp?course_id='


def login():
    """
    login to get cookies in _session
    :return:True if succeed
    """
    user = User()
    data = dict(
        userid=user.username,
        userpass=user.password,
    )
    r = _session.post(_URL_BASE + _URL_LOGIN, data)
    # 即使登录失败也是200所以根据返回内容简单区分了
    LOG.debug(r.text)
    if len(r.content) > 120:
        return False
    return True


def get_url(url):
    """
    _session.GET the page, handle the encoding and return BeautifulSoup
    :param url: Page url
    :return: BeautifulSoup
    """
    r = _session.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.content, "html.parser")
    LOG.debug('GET url: ' + url + ' Status: %d' % r.status_code)
    return soup


class LearnBase(dict):

    """ 实现键值与属性同步的基础类 """

    def __init__(self, *args, **kwargs):
        """ 来自https://goo.gl/DTygYW """
        super(LearnBase, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Semester:
    """
    Class Semester have all courses in it
    """

    def __init__(self, current=True):
        """
        set the current flag to get current/past Semester
        :param current: Boolean True/False for Current/Past semester
        :return: None
        """
        login()
        if current:
            self.url = _URL_BASE + _URL_CURRENT_SEMESTER
        else:
            self.url = _URL_BASE + _URL_PAST_SEMESTER
        self._name = None

    @property
    def name(self):
        if not self._name:
            soup = get_url(self.url)
            self._name = soup.find('td', class_='active_on').text
        return self._name

    @property
    def courses(self):
        """
        return all the courses under the semester
        :return: Courses generator
        """
        soup = get_url(self.url)
        for j in soup.find_all('tr', class_=['info_tr', 'info_tr2']):
            i = j.find('a')
            url = i['href']
            if url.startswith('/Mult'):
                url = _URL_BASE_ + url
            else:
                # !!important!! ignore the new
                # WebLearning Courses At This moment
                # TODO: new learn.cic.tsinghua.edu.cn
                continue
            num = (int(x.contents[0])
                   for x in j.find_all('span', class_='red_text'))
            name = i.contents[0]
            name = re.sub(r'[\n\r\t ]', '', name)
            name = re.sub(r'\([^\(\)]+\)$', '', name)
            id = url[-6:]
            yield Course(name=name,
                         url=url,
                         id=id,
                         num=num)


class Course(LearnBase):
    """
    this is the Course class
    """

    @property
    def works(self):
        """
        get all the work in course
        :return: Work generator
        """
        url = _URL_BASE + _PREF_WORK + self.get('id', '')
        soup = get_url(url)
        for i in soup.find_all('tr', class_=['tr1', 'tr2']):
            tds = i.find_all('td')
            if "已经提交" in tds[3].contents[0]:
                continue
            url = _URL_BASE + '/lesson/student/' + \
                i.find('a')['href']
            id = re.search(r'(\d+)', url).group(0)
            title = i.find('a').contents[0].replace(u'\xa0', u' ')
            end_time = tds[2].contents[0] + ' 23:59:59'
            date = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            if date < datetime.now():
                continue
            yield Work(id=id,
                       title=title,
                       course=self.get('name', ''),
                       url=url,
                       date=date)

    @property
    def messages(self):
        """
        get all messages in course
        :return: Message generator
        """
        url = _URL_BASE + _PREF_MSG + self.get('id', '')
        soup = get_url(url)
        for m in soup.find_all('tr', class_=['tr1', 'tr2']):
            tds = m.find_all('td')
            title = tds[1].contents[1].text.replace(u'\xa0', u' ')
            url = _URL_BASE + '/public/bbs/' + \
                tds[1].contents[1]['href']
            id = re.search(r"id=(\d+)", url).group(1)
            date = datetime.strptime(tds[3].text, '%Y-%m-%d')
            yield Message(title=title,
                          course=self.get('name', ''),
                          url=url,
                          date=date,
                          id=id)

    @property
    def files(self):
        """
        get all files in course
        :return: File generator
        """

        def file_size_M(s):
            digitals = s[:-1]
            if s.endswith('K'):
                return float(digitals) / 1024
            elif s.endswith('M'):
                return float(digitals)
            return 1024 * float(digitals)

        url = _URL_BASE + _PREF_FILES + self.get('id', '')
        soup = get_url(url)
        for j in soup.find_all('tr', class_=['tr1', 'tr2']):
            tds = j.find_all('td')
            name = re.search(
                r'getfilelink=([^&]+)&',
                str(j.find(text=lambda text: isinstance(text,
                                                        Comment)))).group(1)
            url = 'http://learn.tsinghua.edu.cn/kejian/data/%s/download/%s' % (
                self.get('id', ''), name)
            name = re.sub(r'_[^_]+\.', '.', name)
            size = file_size_M(tds[-3].text)
            title = tds[-5].a.text.strip() + name[-4:]
            yield File(size=size,
                       name=name,
                       url=url,
                       title=title,
                       course=self.get('name', ''))


class Work(LearnBase):
    """
    the homework class
    """

    def __init__(self, *args, **kwargs):
        super(Work, self).__init__(*args, **kwargs)
        self._details = None
        self._file = None

    @property
    def details(self):
        """
        the description of the work
        :return:str details /None if not exists
        """
        if not self._details:
            soup = get_url(self.get('url', ''))
            try:
                _details = soup.find_all('td', class_='tr_2')[
                    1].textarea.contents[0]
            except:
                _details = ""
            self._details = _details.replace('\r', '')
        return self._details

    @property
    def file(self):
        """
        the file attached to the work
        :return: Instance of File/None if not exists
        """
        if not self.get('_file', ''):
            soup = get_url(self.get('url', ''))
            try:
                fname = soup.find_all('td', class_='tr_2')[2].a.contents[0]
                furl = 'http://learn.tsinghua.edu.cn' + \
                    soup.find_all('td', class_='tr_2')[2].a['href']
                _file = File(url=furl,
                             name=fname,
                             course=self.get('course', ''))
            except AttributeError:
                _file = None
            self._file = _file
        return self._file


class File(LearnBase):

    def save(self, path='.'):
        filepath = os.path.join(path, self.get('name', ''))
        if os.path.isfile(filepath):
            return filepath
        if not os.path.exists(path):
            os.makedirs(path)
        r = _session.get(self.get('url', ''), stream=True)
        with open(filepath, 'wb') as handle:
            if not r.ok:
                raise ValueError('failed in saving file',
                                 self.get('name', ''),
                                 self.get('url', ''))
            for block in r.iter_content(1024):
                handle.write(block)
        return filepath


class Message(LearnBase):

    def __init__(self, *args, **kwargs):
        super(Message, self).__init__(*args, **kwargs)
        self._details = None

    @property
    def details(self):
        if not self._details:
            soup = get_url(self.get('url', ''))
            _details = soup.find_all('td', class_='tr_l2')[
                1].text.replace('\xa0', ' ')
            _details = re.sub('(\\xa0)+', ' ', _details)
            _details = re.sub('\n+', '\n', _details)
            self._details = _details.replace('\r', '')
        return self._details
