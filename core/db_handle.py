#!/usr/bin/python
# -*- coding: utf-8 -*-


def file_db_handle(database):
    """
    数据存于文件
    :param database:
    :return: 文件存储路径
    """
    db_path = "%s" % (database['path'])
    return db_path



def sql_db_handle(database):
    """
    数据存于数据库
    :param database:
    :return:
    """
    pass


def handle(database):
    """
    根据数据存储方式判断如何获取数据
    :param database:
    :return:
    """
    if database['engine'] == 'file_storage':
        return file_db_handle(database)
    elif database['engine'] == 'sql':
        return sql_db_handle(database)
    else:
        pass