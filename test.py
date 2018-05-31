#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
acc_dic = {
    'Alex': {
        'id': 101,
        'password': 'aaa',
        'credit': 15000,
        'balance': 15000,
        'enroll_date': '2017-01-01',
        'expire_date': '2021-01-01',
        'pay_day': 22,
        'status': 0 # 0 = normal, 1 = locked, 2 = disabled
    },
    'Lucy': {
        'id': 102,
        'password': 'bbb',
        'credit': 15000,
        'balance': 15000,
        'enroll_date': '2017-02-02',
        'expire_date': '2022-02-02',
        'pay_day': 22,
        'status': 0  # 0 = normal, 1 = locked, 2 = disabled
    },
    'Jack': {
        'id': 103,
        'password': 'ccc',
        'credit': 15000,
        'balance': 15000,
        'enroll_date': '2017-03-03',
        'expire_date': '2023-03-03',
        'pay_day': 22,
        'status': 0  # 0 = normal, 1 = locked, 2 = disabled
    },
    'admin': {
        'id': 100,
        'password': 'root',
        'status': 0  # 0 = normal, 1 = locked, 2 = disabled
    }
}

print(json.dumps(acc_dic))

