#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Learn_Download
# 下载网络学堂上的公告、作业文件、课程文件等内容并存储与NextCloud或GoogleDrive上。
#
# Copyright © 2017 Yongwen Zhuang <zeoman@163.com>
#
# Distributed under terms of the MIT license.

"""
Learn_Download
下载网络学堂上的公告、作业文件、课程文件等内容并存储与NextCloud或GoogleDrive上。

Author: Yongwen Zhuang
Create: 2017-09-17
"""

import os
import functools
import atexit
import pickle
from datetime import datetime
import owncloud
from thu_utils import User
from thu_utils import Semester
from thu_utils import LOG


USER = User('.ownuser', 'Input owncloud user')
OC = owncloud.Client('https://cloud.mickir.me')
OC.login(USER.username, USER.password)

SAVE = 'tmp'

TIMEFMT = 'DEADLINE: <%Y-%m-%d %a %H:%M>'
LWORK = []
LMSG = []
DOWNFILE = 'log/download.log'
if os.path.exists(DOWNFILE):
    with open(DOWNFILE, 'rb') as down_r:
        DOWNLOADED = pickle.load(down_r)
else:
    DOWNLOADED = []


def exit_handler():
    """退出前保存已下载文件 """
    with open(DOWNFILE, 'wb') as down_w:
        pickle.dump(DOWNLOADED, down_w)


def cmp(item1, item2):
    """按时间正序排序"""
    if item1.date < item2.date:
        return -1
    return 1


def works_to_str(works):
    """作业内容排序变成字符串"""
    works.sort(key=functools.cmp_to_key(cmp))
    string = ['* 作业']
    for work in works:
        string.append('** %s：%s ' % (work.course, work.title))
        string.append(datetime.strftime(work.date, TIMEFMT))
        string.append(work.details if work.details is not None else '')
        if work.file is not None:
            string.append('FILE: %s' % work.file.name)
        string.append('\n')
    return '\n'.join(string)


def msgs_to_str(msgs):
    """通知内容排序变成字符串"""
    msgs.sort(key=functools.cmp_to_key(cmp), reverse=True)
    string = ['* 通知']
    for message in msgs:
        string.append('** %s：%s ' % (message.course, message.title))
        string.append(datetime.strftime(message.date, '%Y-%m-%d'))
        string.append(message.details)
    return '\n'.join(string)


def handle_work(work):
    """Handle work"""
    LOG.info('Homework: ' + work.title)
    LWORK.append(work)

    if work.file is not None:
        LOG.info('Homework file: ' + work.file.name)
        if work.course + work.file.name not in DOWNLOADED:
            work.file.save(os.path.join(SAVE, work.course))
            send_file(work.file, '/作业/')
    google_upload(work)


def handle_file(file):
    """Handle file"""
    LOG.info('File: ' + file.name)
    if file.course + file.name not in DOWNLOADED:
        file.save(os.path.join(SAVE, file.course))
        send_file(file)


def handle_message(message):
    """Handle message"""
    LOG.info('Message: ' + message.title)
    LMSG.append(message)
    google_upload(message)


def google_upload(message):
    """ Send message to GoogleCalendar"""
    pass


def send_file(file, path='/'):
    """ Send file to GoogleDrive or NextCloud """
    LOG.info('Upload ' + file.course + ' ' + file.name)
    target_path = '课程内容/' + file.course + path
    local_path = SAVE + '/' + file.course + '/' + file.name
    try:
        OC.mkdir('课程内容/' + file.course + '/')
    except owncloud.HTTPResponseError:
        pass
    try:
        OC.mkdir(target_path)
    except owncloud.HTTPResponseError:
        pass

    OC.put_file(target_path + file.name, local_path)
    os.remove(local_path)
    DOWNLOADED.append(file.course + file.name)


def main():
    """main function"""
    semester = Semester()
    try:
        OC.mkdir('课程内容')
    except owncloud.HTTPResponseError:
        pass
    info = open(SAVE + "/Info.org", "w")
    for course in semester.courses:
        LOG.info('Course: ' + course.name)

        for work in course.works:
            if work.date < datetime.now():
                continue
            handle_work(work)

        for message in course.messages:
            handle_message(message)

        for file in course.files:
            handle_file(file)

    info.write(works_to_str(LWORK))
    info.write('\n\n')
    info.write(msgs_to_str(LMSG))
    info.close()
    OC.put_file('课程内容/笔记/Info.org', SAVE + '/Info.org')


if __name__ == "__main__":
    atexit.register(exit_handler)
    try:
        main()
    except Exception as e:
        info = open(SAVE + "/Info.org", "w")
        info.write(str(e))
        info.close()
        OC.put_file('课程内容/笔记/Info.org', SAVE + '/Info.org')
