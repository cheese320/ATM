#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)


from bin import main
if __name__ == '__main__':
    main.run()
