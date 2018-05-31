#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os


BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DATABASE = {
    'engine': 'file_storage',  # support mysql, postgresql in the future
    'name': 'account',
    'path': "%s\db" % BASE_DIR
}


LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'transaction': 'transactions.log',
    'access': 'access.log'
}


TRANSACTION_TYPE = {
    'repay': {'action': 'plus', 'interest': 0},
    'withdraw': {'action': 'minus', 'interest': 0.05},
    'transfer': {'action': 'minus', 'interest': 0.05},
    'consume': {'action': 'minus', 'interest': 0},
}
