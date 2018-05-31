#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import json

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(path)  # 这样这个路径会在最后面,每次都要遍历到最后才能找到(如果中途没有同名文件的话)
sys.path.insert(0, path)  # 将该路径插到前面去

from core import tools # 加完路径再导入就可以了
from conf import settings
from core import db_handle



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
    retry = 0
    acc_dic = load_info("account")
    while retry < 3:

        user_input = input("请输入用户名和密码, 用逗号隔开: ")
        if user_input == "quit":
            exit()
        else:
            user_acc = user_input.strip().split(",")
            if len(user_acc) != 2:
                print("输入有误, 请重输: ")
            elif user_acc[0] not in acc_dic.keys():
                print("帐户不存在, 请重输: ")
            elif user_acc[0] in acc_dic.keys() and user_acc[1] != acc_dic[user_acc[0]]["password"]:
                print("密码错误, 请重输")
                retry += 1
                if retry == 2:
                    # 将用户帐户状态修改为 1 -- blocked
                    acc_dic[user_acc[0]]["status"] = 1
                    # 将修改后的帐户信息写回json文件
                    dump_info("account", acc_dic)

            else:
                return {user_acc[0]: acc_dic[user_acc[0]]}
    else:
        print("错误次数太多, 帐户被锁定, 请联系管理员")


def shopping_mall():
    """
    商城购买
    :return:
    """
    acc_dic = load_info("account")
    goods_dic = load_info("repository")
    temp = list(login().keys())
    username = temp[0]
    print(type(username))
    print(username)
    print(acc_dic[username])
    credit = acc_dic[username]["credit"]
    shopping_list = load_info("shopping_list")
    print("商品列表".center(50, "*"))
    for i in goods_dic:
        print(i, goods_dic[i])
    print("The End".center(53, "*"))
    print("\r\n")
    exit_flag = False
    while not exit_flag:
        user_input = input("请选择商品名称及购买数量(例:iphone,2): ").strip()
        if user_input == "quit":
            exit()
        else:
            order = user_input.split(",")
            price = goods_dic[order[0]]["price"]
            remaining = goods_dic[order[0]]["inventory"]
            goods_2buy = order[0]
            order_qty = int(order[1])
            if len(order) !=2 or (goods_2buy not in goods_dic.keys()) or (not order[1].isdigit()):
                print('\033[34;1m%s\033[0m' % "输入有误, 请重输")
            elif order_qty == 0:
                print('\033[34;1m%s\033[0m' % "购买数量不能为0, 请重输")
            elif 0 < order_qty <= remaining:
                # 做成float类型更准确, 但是这里数量和价格不会超出int取值上限, 为了计算方便, 暂取int类型
                sum_rmb = int(price*order_qty)
                if acc_dic[username]["balance"] >= sum_rmb:
                    # 减少库存
                    remaining = remaining - order_qty
                    goods_dic[order[0]]["inventory"] = remaining
                    # 扣减余额
                    credit = credit - sum_rmb
                    acc_dic[username]["credit"] = credit
                    # TODO log
                    print('\033[31;1m%s\033[0m' % "\r\n购买成功")
                    if len(shopping_list[username]) > 0 and order[0] in list(shopping_list[username].keys()):
                        shopping_list[username][order[0]]["buy_qty"] = shopping_list[username][order[0]]["buy_qty"] + order_qty
                        # qty = qty+order_qty
                    else:
                        # qty = shopping_list[username][order[0]]["buy_qty"]
                        shopping_list[username][order[0]] = {}
                        shopping_list[username][order[0]]["buy_qty"] = order_qty
                        shopping_list[username][order[0]]["spent"] = sum_rmb
                    dump_info("shopping_list",shopping_list)
                    print( "已购买商品列表".center(50, "*"))
                    for i in shopping_list[username]:
                        print(i, shopping_list[username][i])
                    print("The End".center(55, "*"))
                    print("\r\n")
                    dump_info("account", acc_dic)
                    dump_info("repository", goods_dic)

                else:
                    print('\033[34;1m%s\033[0m' % "余额不足, 请重输")
            else:
                print('\033[34;1m%s\033[0m' % "库存不足, 请重输")


shopping_mall()