#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fzdm,sys

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        name = sys.argv[1]
    else:
        name = input("请输入漫画名字:")
    f = fzdm.Fzdm(name)
    f.run()
