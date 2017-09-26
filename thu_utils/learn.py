#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Learn
Learn.tsinghua.edu.cn

"""

import re
import os
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup, Comment

from .user import User
from .logger import LOG

# global vars
_SESSION = requests.session()
_SESSION_NEW = requests.session()
_URL_BASE = 'http://learn.tsinghua.edu.cn'
_URL_BASE_NEW = 'http://learn.cic.tsinghua.edu.cn'
_URL_LOGIN = 'http://learn.tsinghua.edu.cn/MultiLanguage/'\
    'lesson/teacher/loginteacher.jsp'
_URL_LOGIN_NEW = 'https://id.tsinghua.edu.cn/do/off/' \
    'ui/auth/login/post/fa8077873a7a80b1cd6b185d5a796617/' \
    '0?/j_spring_security_thauth_roaming_entry'

# 学期
_URL_CURRENT_SEMESTER = '/MultiLanguage/lesson/student/MyCourse.jsp?typepage=1'
_URL_PAST_SEMESTER = '/MultiLanguage/lesson/student/MyCourse.jsp?typepage=2'
# 个人信息
_URL_PERSONAL_INFO = '/MultiLanguage/vspace/vspace_userinfo1.jsp'

# 课程不同板块前缀
# 课程公告
_PREF_MSG = '/MultiLanguage/public/bbs/getnoteid_student.jsp?course_id='
# Get 参数：currentPage:1, pageSize:50
_PREF_MSG_NEW = '/b/myCourse/notice/listForStudent/'
# 课程信息
_PREF_INFO = '/MultiLanguage/lesson/student/course_info.jsp?course_id='
# 课程文件
_PREF_FILES = '/MultiLanguage/lesson/student/download.jsp?course_id='
# POST 无参数
_PREF_FILES_NEW = '/b/myCourse/tree/getCoursewareTreeData/'
_PREF_DOWNLOAD = '/b/resource/downloadFileStream/'
# 教学资源
_PREF_LIST = '/MultiLanguage/lesson/student/ware_list.jsp?course_id='
# 课程作业
_PREF_WORK = '/MultiLanguage/lesson/student/hom_wk_brw.jsp?course_id='
# Get
_PREF_WORK_NEW = '/b/myCourse/homework/list4Student/'


def login():
    """
    login to get cookies in _SESSION
    :return:True if succeed
    """
    user = User()
    data = dict(
        userid=user.username,
        userpass=user.password,
    )
    req = _SESSION.post(_URL_LOGIN, data)
    # 即使登录失败也是200所以根据返回内容简单区分了
    LOG.debug(req.text)
    if len(req.content) > 120:
        return False
    data = dict(
        i_user=user.username,
        i_pass=user.password,
    )
    req = _SESSION_NEW.post(_URL_LOGIN_NEW, data)
    LOG.debug(req.text)
    return True


def get_url(url):
    """
    _SESSION.GET the page, handle the encoding and return BeautifulSoup
    :param url: Page url
    :return: BeautifulSoup
    """
    if 'learn.cic' in url:
        req = _SESSION_NEW.get(url)
    else:
        req = _SESSION.get(url)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.content, "html.parser")
    LOG.debug('GET url: ' + url + ' Status: %d' % req.status_code)
    return soup


class LearnBase(dict):

    """ 实现键值与属性同步的基础类 """

    def __init__(self, *args, **kwargs):
        """ 来自https://goo.gl/DTygYW """
        super(LearnBase, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Semester:
    """ Class Semester have all courses in it """

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
        """ 学期名称 """
        if not self._name:
            soup = get_url(self.url)
            self._name = soup.find('td', class_='active_on').text
        return self._name

    @property
    def courses(self):
        """ 所有课程 """
        soup = get_url(self.url)
        for j in soup.find_all('tr', class_=['info_tr', 'info_tr2']):
            i = j.find('a')
            url = i['href']
            num = (int(x.contents[0])
                   for x in j.find_all('span', class_='red_text'))
            name = i.contents[0]
            name = re.sub(r'[\n\r\t ]', '', name)
            name = re.sub(r'\([^\(\)]+\)$', '', name)
            if url.startswith('/Mult'):
                # learn.tsinghua.edu.cn
                url = _URL_BASE + url
                new = False
                id_ = url.split('=')[-1]
            else:
                # learn.cic.tsinghua.edu.cn
                id_ = url.split('/')[-1]
                new = True
            yield Course(name=name,
                         new=new,
                         url=url,
                         id=id_,
                         num=num)


class Course(LearnBase):
    """
    this is the Course class
    """

    @property
    def works(self):
        """ get all the work in course """
        if self.get('new', False):
            return
        else:
            url = _URL_BASE + _PREF_WORK + self.get('id', '')
            soup = get_url(url)
            for i in soup.find_all('tr', class_=['tr1', 'tr2']):
                tds = i.find_all('td')
                if "已经提交" in tds[3].contents[0]:
                    continue
                url = _URL_BASE + '/MultiLanguage/lesson/student/' + \
                    i.find('a')['href']
                id_ = re.search(r'(\d+)', url).group(0)
                title = i.find('a').contents[0].replace(u'\xa0', u' ')
                end_time = tds[2].contents[0] + ' 23:59:59'
                date = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                if date < datetime.now():
                    continue
                yield Work(id=id_,
                           title=title,
                           course=self.get('name', ''),
                           url=url,
                           date=date)

    @property
    def messages(self):
        """ get all messages in course """
        if self.get('new', False):
            return
        url = _URL_BASE + _PREF_MSG + self.get('id', '')
        soup = get_url(url)
        for mes in soup.find_all('tr', class_=['tr1', 'tr2']):
            tds = mes.find_all('td')
            title = tds[1].contents[1].text.replace(u'\xa0', u' ')
            url = _URL_BASE + '/MultiLanguage/public/bbs/' + \
                tds[1].contents[1]['href']
            id_ = re.search(r"id=(\d+)", url).group(1)
            date = datetime.strptime(tds[3].text, '%Y-%m-%d')
            yield Message(title=title,
                          course=self.get('name', ''),
                          url=url,
                          date=date,
                          id=id_)

    @property
    def files(self):
        """ get all files in course """

        def file_size_m(string):
            """ 计算file大小 """
            digitals = string[:-1]
            if string.endswith('K'):
                return float(digitals) / 1024
            elif string.endswith('M'):
                return float(digitals)
            elif string.endswith('G'):
                return 1024 * float(digitals)
            return float(string) / 1024

        if self.get('new', False):
            url = _URL_BASE_NEW + _PREF_FILES_NEW + self.get('id', '') + '/0'
            json = _SESSION_NEW.post(url).json()
            url = _URL_BASE_NEW + \
                "/b/courseFileAccess/markStatusforYiDu/" + self.get('id', '')
            _SESSION_NEW.post(url).json()
            for courseware_tree in json['resultList'].values():
                for second_node in courseware_tree['childMapData'].values():
                    for third_node in second_node['courseCoursewareList']:
                        file_info = third_node['resourcesMappingByFileId']
                        name = re.sub(r'_[^_]+\.', '.', file_info['fileName'])
                        yield File(size=file_size_m(file_info['fileSize']),
                                   name=name,
                                   new=True,
                                   url=_URL_BASE_NEW + _PREF_DOWNLOAD +
                                   file_info['fileId'],
                                   title=third_node['title'],
                                   course=self.get('name', ''))
        else:
            url = _URL_BASE + _PREF_FILES + self.get('id', '')
            soup = get_url(url)
            for j in soup.find_all('tr', class_=['tr1', 'tr2']):
                tds = j.find_all('td')
                name = re.search(
                    r'getfilelink=([^&]+)&',
                    str(j.find(text=lambda text: isinstance(
                        text, Comment)))).group(1)
                # 使下载后可以把新文件标签去掉
                # url = _URL_BASE + '/kejian/data/%s/download/%s' % (
                #     self.get('id', ''), name)
                url = _URL_BASE + tds[-5].a['href']
                name = re.sub(r'_[^_]+\.', '.', name)
                size = file_size_m(tds[-3].text)
                title = tds[-5].a.text.strip() + name[-4:]
                yield File(size=size,
                           name=name,
                           new=False,
                           url=url,
                           title=title,
                           course=self.get('name', ''))


class Work(LearnBase):
    """
    the homework class
    """

    def __init__(self, *args, **kwargs):
        """ Init homework """
        super(Work, self).__init__(*args, **kwargs)
        self._details = None
        self._file = None

    @property
    def details(self):
        """ the description of the work """
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
        """ the file attached to the work """
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
    """
    the file class
    """

    def save(self, path='.'):
        """ Save this file to path """
        filepath = os.path.join(path, self.get('name', ''))
        if os.path.isfile(filepath):
            return False
        if not os.path.exists(path):
            os.makedirs(path)
        if self.get('new', False):
            req = _SESSION_NEW.get(self.get('url', ''), stream=True)
        else:
            req = _SESSION.get(self.get('url', ''), stream=True)
        with open(filepath, 'wb') as handle:
            if not req.ok:
                raise ValueError('failed in saving file',
                                 self.get('name', ''),
                                 self.get('url', ''))
            for block in req.iter_content(1024):
                handle.write(block)
        return filepath


class Message(LearnBase):
    """
    the message class
    """

    def __init__(self, *args, **kwargs):
        """ Init """
        super(Message, self).__init__(*args, **kwargs)
        self._details = None

    @property
    def details(self):
        """ Details of Message """
        if not self._details:
            soup = get_url(self.get('url', ''))
            _details = soup.find_all('td', class_='tr_l2')[
                1].text.replace('\xa0', ' ')
            _details = re.sub('(\\xa0)+', ' ', _details)
            _details = re.sub('\n+', '\n', _details)
            self._details = _details.replace('\r', '')
        return self._details
