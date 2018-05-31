Module2-atm/
├── README
├── atm #ATM主程目录
│   ├── __init__.py
│   ├── bin #ATM 执行文件 目录
│   │   ├── __init__.py
│   │   ├── main.py  #ATM 主程序
│   │   └── path_define.py  # 直接执行主程序
│   ├── conf #配置文件
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── core #主要程序逻辑都 在这个目录 里
│   │   ├── __init__.py
│   │   ├── db_handle.py   #数据库连接引擎
│   │   └── tools.py  #所有子程序都在这儿,a包括商城程序.
│   ├── db  #用户数据存储的地方
│   │   ├── __init__.py
│   │   ├── account.py #便于迅速恢复同名json文件数据初始化状态.
│   │   ├── account.json #用户帐户信息.
│   │   ├── repository.py #便于迅速恢复同名json文件数据初始化状态.
│   │   ├── repository.json #商品库存信息
│   │   └── shopping_list.json #存各个用户的商城购买清单
│   │
│   │── doc #文档
│   │   ├── __init__.py
│   │   ├── idea.txt #代码思路
│   │   └── flowchart.jpg #流程图
│   └── log #日志目录
│       ├── __init__.py
│       ├── access.log #用户访问和操作的相关日志
└──     └── transactions.log    #所有的交易日志

注:程序执行环境 1. python 3.0; 2. windows 10; 3. IDE: pycharm 2.7
