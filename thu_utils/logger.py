#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Logger
Logging for THU_Utils

LOG : object
"""

import os
import logging
import logging.handlers

# 日志文件的路径，FileHandler不能创建目录，这里先检查目录是否存在，不存在创建他
# 当然也可以继承之后重写FileHandler的构造函数
LOG_FILE_PATH = "log/Execution.log"
dir = os.path.dirname(LOG_FILE_PATH)
if not os.path.isdir(dir):
    os.mkdir(dir)
# 写入文件的日志等级，由于是详细信息，推荐设为debug
FILE_LOG_LEVEL = "DEBUG"
# 控制台的日照等级，info和warning都可以，可以按实际要求定制
CONSOLE_LOG_LEVEL = "INFO"

MAPPING = {"CRITICAL": logging.CRITICAL,
           "ERROR": logging.ERROR,
           "WARNING": logging.WARNING,
           "INFO": logging.INFO,
           "DEBUG": logging.DEBUG,
           "NOTSET": logging.NOTSET,
           }


class Logger():
    """Logging for THU_Utils"""

    def __init__(self, log_file, file_level, console_level):
        self.config(log_file, file_level, console_level)

    def config(self, log_file, file_level, console_level):
        self.logger = logging.getLogger("thu_utils")
        self.logger.setLevel(MAPPING[file_level])
        # 生成RotatingFileHandler，设置文件大小为10M,编码为utf-8，最大文件个数为100个，如果日志文件超过100，则会覆盖最早的日志
        self.fh = logging.handlers.RotatingFileHandler(
            log_file,
            mode='a',
            maxBytes=1024 * 1024 * 10,
            backupCount=100,
            encoding="utf-8")
        self.fh.setLevel(MAPPING[file_level])
        # 生成StreamHandler
        self.ch = logging.StreamHandler()
        self.ch.setLevel(MAPPING[console_level])
        # 设置格式
        formatter = logging.Formatter(
            "%(asctime)s *%(levelname)s* : %(message)s", '%Y-%m-%d %H:%M:%S')
        self.ch.setFormatter(formatter)
        self.fh.setFormatter(formatter)
        # 把所有的handler添加到root logger中
        self.logger.addHandler(self.ch)
        self.logger.addHandler(self.fh)

    def debug(self, msg):
        if msg is not None:
            self.logger.debug(msg)

    def info(self, msg):
        if msg is not None:
            self.logger.info(msg)

    def warning(self, msg):
        if msg is not None:
            self.logger.warning(msg)

    def error(self, msg):
        if msg is not None:
            self.logger.error(msg)

    def critical(self, msg):
        if msg is not None:
            self.logger.critical(msg)

LOG = Logger(LOG_FILE_PATH, FILE_LOG_LEVEL, CONSOLE_LOG_LEVEL)

if __name__ == "__main__":
    # 测试代码
    for i in range(50):
        LOG.error(i)
        LOG.debug(i)
    LOG.critical("Database has gone away")
