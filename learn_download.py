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
import owncloud
from thu_utils import User
from thu_utils import Semester
from thu_utils import LOG


USER = User('.ownuser', 'Input owncloud user')
OC = owncloud.Client('https://cloud.mickir.me')
OC.login(USER.username, USER.password)


def handle_work(work, course):
    """Handle work"""
    LOG.info(course + ' Homework: ' + work.title)
    # TODO: 下载作业文件
    # TODO: 作业内容集合到一个文件内
    # TODO: 内容上传到GoogleCalendar


def handle_file(file, course):
    """Handle file"""
    LOG.info('File: ' + file.name)
    file.save(os.path.join('tmp', course))
    send_file(file.name, course)


def handle_message(message, course):
    """Handle message"""
    LOG.info('Message: ' + message.title)
    msg = {
        'title': course + ' ' + message.title,
        'date': message.date,
        'details': message.details
    }
    send_msg(msg)
    # TODO: 集合信息为一个文件，可访问
    # TODO: 上传到GoogleCalendar


def send_msg(msg):
    """ Send message to GoogleCalendar or print"""
    print(msg)


def send_file(filename, coursename):
    """ Send file to GoogleDrive or NextCloud """
    target_path = '课程内容/' + coursename + '/'
    local_path = 'tmp/' + coursename + '/' + filename
    try:
        OC.mkdir('课程内容')
    except owncloud.HTTPResponseError:
        pass
    try:
        OC.mkdir(target_path)
    except owncloud.HTTPResponseError:
        pass

    LOG.info('Upload ' + coursename + ' ' + filename)
    OC.put_file(target_path + filename, local_path)


def main():
    """main function"""
    semester = Semester()
    for course in semester.courses:
        LOG.info('Get course: ' + course.name)

        for work in course.works:
            handle_work(work, course.name)

        for message in course.messages:
            handle_message(message, course.name)

        for file in course.files:
            handle_file(file, course.name)


if __name__ == "__main__":
    main()
