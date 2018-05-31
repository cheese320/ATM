#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)  # 这样这个路径会在最后面,每次都要遍历到最后才能找到(如果中途没有同名文件的话)
sys.path.insert(0, path)  # 将该路径插到前面去
from core import tools


def run():
    exit_flag = False
    # 普通用户
    if tools.username != "admin":
        # 能打印帐户信息的都是正常状态的帐户, 所以这里不显示帐户状态
        initial = '''
        ---------- {_name}帐户信息 --------- 
        credit: {_credit}
        balance: {_balance}
        enroll-date: {_enroll}
        expire_date: {_expire}
        pay_day: {_payday}
        ------------ The End ----------- 
        '''.format(_name=tools.username,
                   _credit=tools.info[tools.username]["credit"],
                   _balance=tools.info[tools.username]["balance"],
                   _enroll=tools.info[tools.username]["enroll_date"],
                   _expire=tools.info[tools.username]["expire_date"],
                   _payday=tools.info[tools.username]["pay_day"])
        print(initial)
        while not exit_flag:
            msg = '''
            1. 商城
            2. 还款
            3. 取款
            4. 转帐
            5. 帐单
            6. 退出
            '''
            print("功能列表".center(20, "*"))
            print(msg)
            print("The end".center(23, "*"))
            user_choice = input("请选择功能数字代码: ")
            if user_choice == "quit":
                exit_flag = True
            elif not user_choice.isdigit():
                print("输入有误, 请重输")
                break
            else:
                seq = int(user_choice)
                if seq <= 0 or seq > 6:
                    print("输入有误, 请重输")
                elif seq == 1:
                    tools.shopping_mall()
                elif seq == 2:
                    tools.repay()
                elif seq == 3:
                    tools.withdraw()
                elif seq == 4:
                    tools.transfer()
                elif seq == 5:
                    tools.bill()
                elif seq == 6:
                    exit()

    else:
        while not exit_flag:
            msg2 = '''
            1. 添加帐户
            2. 解锁帐户
            3. 修改用户额度
            4. 冻结帐户
            5. 解冻帐户
            6. 退出
            '''
            print("功能列表".center(20, "*"))
            print(msg2)
            print("The end".center(23, "*"))
            print("\r\n")
            user_choice2 = input("请选择功能数字代码: ")
            if user_choice2 == "quit":
                exit_flag = True
            elif not user_choice2.isdigit():
                print("输入有误, 请重输")
                break
            else:
                seq2 = int(user_choice2)
                if seq2 <= 0 or seq2 > 6:
                    print("输入有误, 请重输")
                elif seq2 == 1:
                    tools.new_account()
                elif seq2 == 2:
                    tools.unlock()
                elif seq2 == 3:
                    tools.adjustment()
                elif seq2 == 4:
                    tools.freeze()
                elif seq2 == 5:
                    tools.unfreeze()
                elif seq2 == 6:
                    exit()


run()