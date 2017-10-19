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
LWORK = ['* 作业']
LMSG = ['* 公告']
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


def handle_work(work):
    """Handle work"""
    LOG.info('Homework: ' + work.title)
    LWORK.append('** %s：%s ' % (work.course, work.title))
    LWORK.append(datetime.strftime(work.date, TIMEFMT))
    LWORK.append(work.details)

    if work.file is not None:
        LWORK.append('FILE: %s' % work.file.name)
        LOG.info('Homework file: ' + work.file.name)
        if work.course + work.file.name not in DOWNLOADED:
            work.file.save(os.path.join(SAVE, work.course))
            send_file(work.file, '/作业/')
    LWORK.append('\n')
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
    LMSG.append('** %s：%s ' % (message.course, message.title))
    LMSG.append(datetime.strftime(message.date, '%Y-%m-%d'))
    LMSG.append(message.details)
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

    info.write('\n'.join(LWORK))
    info.write('\n\n')
    info.write('\n'.join(LMSG))
    info.close()
    OC.put_file('课程内容/笔记/Info.org', SAVE + '/Info.org')


if __name__ == "__main__":
    atexit.register(exit_handler)
    main()
