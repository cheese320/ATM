#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
from.import db_handle
from conf import settings
from log import log


def load_info(filename):
    """
    将用户信息.json转换成字典
    :param
    :return: 字典
    """
    db_path = db_handle.handle(settings.DATABASE)
    doc = "%s%s%s.json" % (db_path, "\\", filename)
    if os.path.isfile(doc):
        with open(doc, "r", encoding='utf-8') as f:
            account_data = json.load(f)
            return account_data


def dump_info(filename, acc_dic):
    """
    将更改的用户信息写回json文件
    :return:
    """
    db_path = db_handle.handle(settings.DATABASE)
    doc = "%s%s%s.json" % (db_path, "\\", filename)
    if os.path.isfile(doc):
        with open(doc, "w", encoding='utf-8') as f:
            json.dump(acc_dic, f)


def login():
    """
    登录.
    帐户状态: 0 - normal; 1 - locked; 2 - freeze
    :return:
    """
    access_log = log.log("access")
    retry = 0
    acc_dic = load_info("account")
    while retry < 3:

        user_input = input("请输入用户名和密码, 用逗号隔开: ")
        if user_input == "quit":
            exit()
        else:
            user_acc = user_input.strip().split(",")
            if len(user_acc) != 2:
                print('\033[34;1m%s\033[0m' % "输入有误, 请重输")
            elif user_acc[0] not in acc_dic.keys():
                print('\033[34;1m%s\033[0m' % "帐户不存在, 请重输")
            elif acc_dic[user_acc[0]]["status"] != 0:
                print('\033[34;1m%s\033[0m' % "帐户不可用, 请联系管理员")
            elif user_acc[0] in acc_dic.keys() and user_acc[1] != acc_dic[user_acc[0]]["password"]:
                print('\033[34;1m%s\033[0m' % "密码错误, 请重输")
                retry += 1
                if retry == 2:
                    # 将用户帐户状态修改为 1 -- blocked
                    acc_dic[user_acc[0]]["status"] = 1
                    # 将修改后的帐户信息写回json文件
                    dump_info("account", acc_dic)
            else:
                access_log.info('用户%s登录' % user_acc[0])
                print('\033[31;1m%s\033[0m' % "\r\n登录成功")
                return {user_acc[0]: acc_dic[user_acc[0]]}
    else:
        print('\033[34;1m%s\033[0m' % "错误次数太多, 帐户被锁定, 请联系管理员")
        exit()


info = login()
usercenter = list(info.keys())
username = usercenter[0]


def shopping_mall():
    """
    商城购买
    :return:
    """
    transactions_log = log.log("transaction")
    acc_dic = load_info("account")
    goods_dic = load_info("repository")
    '''
    若是直接username = login().keys(), 返回的是class dict_keys, 即使强转, 得到的str也是dict_keys(['Alex]), 
    而需要的返回结果是'Alex'. 这样是没法直接用acc_dic[username]取值的.
    所以只能把login().keys()转成list,再取值, 就可以把dict_keys字样去掉了.
    '''
    balance = acc_dic[username]["balance"]
    shopping_dic = load_info("shopping_list")
    exit_flag = False
    while not exit_flag:
        print("商品列表".center(50, "*"))
        for i in goods_dic:
            print(i, goods_dic[i])
        print("The End".center(53, "*"))
        print("\r\n")
        user_input = input("请选择商品名称及购买数量(例:'iphone,2'): ").strip()
        if user_input == "quit":
            exit_flag = True
        elif acc_dic[username]["status"] != 0:
            print('\033[34;1m%s\033[0m' % "帐户不可用, 请联系管理员.")
            exit_flag = True
        elif user_input.split(",")[0] not in goods_dic.keys():
            print('\033[34;1m%s\033[0m' % "商品不存在, 请重输")
        else:
            order = user_input.split(",")
            price = goods_dic[order[0]]["price"]
            remaining = goods_dic[order[0]]["inventory"]
            goods_2buy = order[0]
            order_qty = int(order[1])
            if len(order) != 2 or (goods_2buy not in goods_dic.keys()) or (not order[1].isdigit()):
                print('\033[34;1m%s\033[0m' % "输入有误, 请重输")
            elif order_qty == 0:
                print('\033[34;1m%s\033[0m' % "购买数量不能为0, 请重输")
            elif 0 < order_qty <= remaining:
                # 做成float类型更准确, 但是这里数量和价格不会超出int取值上限, 为了计算方便, 暂取int类型
                sum_rmb = int(price * order_qty)
                if acc_dic[username]["balance"] >= sum_rmb:
                    # 减少库存
                    remaining = remaining - order_qty
                    goods_dic[order[0]]["inventory"] = remaining
                    # 扣减余额
                    balance = balance - sum_rmb
                    acc_dic[username]["balance"] = balance
                    transactions_log.info('用户%s花费%s购买商品%s' % (username, balance, order[0]))
                    print('\033[31;1m%s\033[0m' % "\r\n购买成功")
                    if len(shopping_dic[username]) > 0 and order[0] in list(shopping_dic[username].keys()):
                        shopping_dic[username][order[0]]["buy_qty"] = shopping_dic[username][order[0]]["buy_qty"] + \
                                                                      order_qty
                        # qty = qty+order_qty
                    else:
                        # qty = shopping_list[username][order[0]]["buy_qty"]
                        shopping_dic[username][order[0]] = {}
                        shopping_dic[username][order[0]]["buy_qty"] = order_qty
                        shopping_dic[username][order[0]]["spent"] = sum_rmb
                    dump_info("shopping_list", shopping_dic)
                    print("已购买商品列表".center(50, "*"))
                    for i in shopping_dic[username]:
                        print(i, shopping_dic[username][i])
                    print("The End".center(55, "*"))
                    print("\r\n")
                    dump_info("account", acc_dic)
                    dump_info("repository", goods_dic)

                else:
                    print('\033[34;1m%s\033[0m' % "余额不足, 请重输")
            else:
                print('\033[34;1m%s\033[0m' % "库存不足, 请重输")


def repay():
    """
    :return: 
    """
    transactions_log = log.log("transaction")
    acc_dic = load_info("account")
    debt = 15000 - float(acc_dic[username]["balance"])
    print('用户\033[31;1m%s\033[0m当前欠款\033[31;1m%s\033[0m元整' % (username, debt))
    exit_flag = False
    while not exit_flag:
        user_input = input("请输入还款金额: ").strip()
        if user_input == "quit":
            exit_flag = True
        elif acc_dic[username]["status"] != 0:
            # 打款方帐户不能被锁定或冻结, 但是收款方帐户没有这个要求.
            print('\033[34;1m%s\033[0m' % "帐户不可用, 请联系管理员.")
            exit_flag = True
        elif not user_input.isdigit():
            print('\033[34;1m%s\033[0m' % "输入有误, 请重输")
        elif int(user_input) <= 0:
            print('\033[34;1m%s\033[0m' % "输入有误, 请重输")
        else:
            print('\033[31;1m%s\033[0m' % "还款成功")
            curr_balance = float(acc_dic[username]["balance"]) + float(user_input)
            acc_dic[username]["balance"] = curr_balance
            print('用户\033[31;1m%s\033[0m当前额度\033[31;1m%s\033[0m元整' % (username, curr_balance))
            transactions_log.info('用户%s还款%s元整' % int(username, user_input))
            dump_info("account", acc_dic)


def withdraw():
    transactions_log = log.log("transaction")
    acc_dic = load_info("account")
    balance = float(acc_dic[username]["balance"])
    exit_flag = False
    while not exit_flag:
        user_input = input("请输入借款金额: ").strip()
        if user_input == "quit":
            exit_flag = True
        elif acc_dic[username]["status"] != 0:
            # 打款方帐户不能被锁定或冻结, 但是收款方帐户没有这个要求.
            print('\033[34;1m%s\033[0m' % "帐户不可用, 请联系管理员.")
            exit_flag = True
        elif not user_input.isdigit():
            print('\033[34;1m%s\033[0m' % "输入有误, 请重输")
        elif int(user_input) == 0 or int(user_input) < 0 or int(user_input) > balance:
            print('\033[34;1m%s\033[0m' % "输入有误, 请重输")
        else:
            print('\033[31;1m%s\033[0m' % "取款成功")
            interest = float(settings.TRANSACTION_TYPE['withdraw']['interest'])
            curr_balance = float(acc_dic[username]["balance"]) - float(user_input) * (1 + interest)
            print('用户\033[31;1m%s\033[0m取款\033[31;1m%s\033[0m元, 利息\033[31;1m%s\033[0m元, '
                  '用户当前额度\033[31;1m%s\033[0m元整' % (username, user_input, float(user_input) * interest,
                                                   curr_balance))
            transactions_log.info('用户%s取款%s元, 利息%s元' % (username, user_input, (float(user_input) * interest)))
            dump_info("account", acc_dic)


def transfer():
    transactions_log = log.log("transaction")
    acc_dic = load_info("account")
    balance = float(acc_dic[username]["balance"])
    exit_flag = False
    while not exit_flag:
        receiver = input("请输入收款方: ").strip()
        user_input = input("请输入转帐金额: ").strip()
        if user_input == "quit" or receiver == "quit":
            exit_flag = True
        elif not user_input.isdigit():
            print('\033[34;1m%s\033[0m' % "输入有误, 请重输")
        elif int(user_input) == 0 or int(user_input) < 0 or int(user_input) > balance:
            print('\033[34;1m%s\033[0m' % "输入有误, 请重输")
        else:
            print('\033[31;1m%s\033[0m' % "转帐成功")
            interest = settings.TRANSACTION_TYPE['withdraw']['interest']
            curr_balance = float(acc_dic[username]["balance"]) - float(user_input) * (1 + interest)
            print('用户完成\033[31;1m%s\033[0m转帐\033[31;1m%s\033[0m, 手续费\033[31;1m%s\033[0m, '
                  '用户当前额度\033[31;1m%s\033[0m元整' % (username, user_input, float(user_input) * interest,
                                                   curr_balance))
            transactions_log.info('用户%s转帐%s元, 利息%s元' % (username, user_input, float(user_input) * interest))
            dump_info("account", acc_dic)


def bill():
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path = '%s\log' % path
    doc = "%s%s%s.log" % (log_path, "\\", "transactions")
    exit_flag = False
    while not exit_flag:
        duration = input("请输入查询帐单周期, 例'201803,201805': ").strip()
        if duration == "quit":
            exit_flag = True
        elif len(duration.split(",")) == 2:
            temp = []
            dur = duration.split(",")
            if not dur[0].isdigit() or not dur[1].isdigit():
                print('\033[34;1m%s\033[0m' % "输入有误, 请重输")
            elif dur[1] < dur[0]:
                print('\033[34;1m%s\033[0m' % "结束年月不能比起始年月小 请重输")
            else:
                with open(doc, "r", encoding='GBK') as f:
                    for line in f:
                        if (dur[0] <= line[:7].replace("-", "") <= dur[1]) and username in line:
                            temp.append(line)
                    print("帐单详情".center(50, "*"))
                    for i in temp:
                        print(i)
                    print("The End".center(50, "*"))
        else:
            print('\033[34;1m%s\033[0m' % "输入有误, 请重输")


def new_account():
    acc_dic = load_info("account")
    exit_flag = False
    while not exit_flag:
        acc_name = input("请输入用户名: ").strip()
        pw = input("请输入密码: ").strip()
        if acc_name == "quit" or pw == "quit":
            exit_flag = True
        elif len(acc_name.split(",")) > 1:
            print('\033[34;1m%s\033[0m' % "输入有误, 请重输: ")
        elif acc_name in acc_dic.keys():
            print('\033[34;1m%s\033[0m' % "用户已存在, 请重输: ")
        else:
            print('\033[31;1m%s\033[0m' % "添加成功")
            acc_dic[acc_name] = {"password": pw, "credit": 150000,
                                 "balance": 15000,
                                 "enroll_date": "2017-01-01",
                                 "expire_date": "2021-01-01",
                                 "pay_day": 22, "status": 0}
            dump_info("account", acc_dic)


def unlock():
    acc_dic = load_info("account")
    exit_flag = False
    while not exit_flag:
        acc_name = input("请输入要解锁的用户名: ").strip()
        if acc_name == "quit":
            exit_flag = True
        elif acc_name not in acc_dic.keys():
            print('\033[34;1m%s\033[0m' % "用户不存在, 请重输: ")
        else:
            # 此处即使用户的状态原本就是0, 再改成0也没什么害处, 所以此处就不判断状态了.
            acc_dic[acc_name]["status"] = 0
            print('\033[31;1m%s\033[0m' % "解锁成功")
            dump_info("account", acc_dic)


def adjustment():
    acc_dic = load_info("account")
    exit_flag = False
    while not exit_flag:
        acc_name = input("请输入要调整额度的用户名: ").strip()
        if acc_name == "quit":
            exit_flag = True
        elif acc_name not in acc_dic.keys():
            print('\033[34;1m%s\033[0m' % "用户不存在, 请重输: ")
        else:
            new_credit = input("请输入新的额度(仅限正整数, 例: 20000): ").strip()
            if not new_credit.isdigit():
                print('\033[34;1m%s\033[0m' % "输入有误, 请重输: ")
            elif int(new_credit) <= 0 or int(new_credit) > 10000000:
                print('\033[34;1m%s\033[0m' % "输入有误, 请重输: ")
            else:
                # 不论帐户状态是被锁定还是被冻结, 修改额度并不影响, 所以这里不判断状态
                acc_dic[acc_name]["credit"] = int(new_credit)
                print('\033[31;1m%s\033[0m' % "额度修改成功")
                print('用户\033[31;1m%s\033[0m当前额度\033[31;1m%s\033[0m元整' % (acc_name, new_credit))
                dump_info("account", acc_dic)


def freeze():
    acc_dic = load_info("account")
    exit_flag = False
    while not exit_flag:
        acc_name = input("请输入要冻结的用户名: ").strip()
        if acc_name == "quit":
            exit_flag = True
        elif acc_name not in acc_dic.keys():
            print('\033[34;1m%s\033[0m' % "用户不存在, 请重输: ")
        else:
            # 此处即使用户的状态原本就是0, 再改成0也没什么害处, 所以此处就不判断状态了.
            acc_dic[acc_name]["status"] = 2
            print('\033[31;1m%s\033[0m' % "冻结成功")
            dump_info("account", acc_dic)


def unfreeze():
    acc_dic = load_info("account")
    exit_flag = False
    while not exit_flag:
        acc_name = input("请输入要解冻的用户名: ").strip()
        if acc_name == "quit":
            exit_flag = True
        elif acc_name not in acc_dic.keys():
            print('\033[34;1m%s\033[0m' % "用户不存在, 请重输: ")
        else:
            # 此处即使用户的状态原本就是0, 再改成0也没什么害处, 所以此处就不判断状态了.
            acc_dic[acc_name]["status"] = 0
            print('\033[31;1m%s\033[0m' % "解冻成功")
            dump_info("account", acc_dic)
