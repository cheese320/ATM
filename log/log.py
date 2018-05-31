#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import json
import logging

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(path)  # 这样这个路径会在最后面,每次都要遍历到最后才能找到(如果中途没有同名文件的话)
sys.path.insert(0, path)  # 将该路径插到前面去


from conf import settings


def log(logging_type):
    """
    去掉打印在屏幕上的功能
    :param logging_type:
    :return:
    """
    # 传日志用例, 生成日志对象
    logger = logging.getLogger(logging_type)
    # 设置日志级别
    logger.setLevel(settings.LOG_LEVEL)

    # # 日志打印到屏幕上
    # ch = logging.StreamHandler()
    # ch.setLevel(settings.LOG_LEVEL)

    # 获取文件日志对象及日志文件
    log_file = "%s\log\%s" % (settings.BASE_DIR, settings.LOG_TYPES[logging_type])
    fh = logging.FileHandler(log_file)
    fh.setLevel(settings.LOG_LEVEL)

    # 日志格式
    formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")

    # 输出格式
    # ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # 把日志打印到指定的handler
    # logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

