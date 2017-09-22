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
from datetime import datetime
import owncloud
from thu_utils import User
from thu_utils import Semester
from thu_utils import LOG


USER = User('.ownuser', 'Input owncloud user')
OC = owncloud.Client('https://cloud.mickir.me')
OC.login(USER.username, USER.password)

FILE = open("tmp/Info.org", "w")


def handle_work(work):
    """Handle work"""
    LOG.info(work.course + ' Homework: ' + work.title)
    FILE.write('** 作业：%s at ' % work.title)
    FILE.write(datetime.strftime(work.date, '%Y-%m-%d\n'))
    FILE.write(work.details)
    FILE.write('\n\n')

    if work.file is not None:
        work.file.save(os.path.join('tmp', work.course))
        send_file(work.file, '/作业/')
    google_upload(work)


def handle_file(file):
    """Handle file"""
    LOG.info('File: ' + file.name)
    file.save(os.path.join('tmp', file.course))
    send_file(file)


def handle_message(message):
    """Handle message"""
    LOG.info('Message: ' + message.title)
    FILE.write('** 公告：%s at ' % message.title)
    FILE.write(datetime.strftime(message.date, '%Y-%m-%d\n'))
    FILE.write(message.details)
    FILE.write('\n\n')
    google_upload(message)


def google_upload(message):
    """ Send message to GoogleCalendar"""
    pass


def send_file(file, path='/'):
    """ Send file to GoogleDrive or NextCloud """
    target_path = '课程内容/' + file.course + path
    local_path = 'tmp/' + file.course + '/' + file.name
    try:
        OC.mkdir('课程内容/' + file.course + '/')
    except owncloud.HTTPResponseError:
        pass
    try:
        OC.mkdir(target_path)
    except owncloud.HTTPResponseError:
        pass

    OC.put_file(target_path + file.name, local_path)
    LOG.info('Upload ' + file.course + ' ' + file.name)


def main():
    """main function"""
    semester = Semester()
    try:
        OC.mkdir('课程内容')
    except owncloud.HTTPResponseError:
        pass
    for course in semester.courses:
        LOG.info('Get course: ' + course.name)
        FILE.write('* %s\n\n' % course.name)

        for work in course.works:
            handle_work(work)

        for message in course.messages:
            handle_message(message)

        for file in course.files:
            handle_file(file)

    FILE.close()
    OC.put_file('课程内容/Info.org', 'tmp/Info.org')


if __name__ == "__main__":
    main()
