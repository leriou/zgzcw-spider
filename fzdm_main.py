#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fzdm

if __name__ == "__main__":
    name = input("请输入漫画名字:")
    # name = "进击的巨人"
    f = fzdm.Fzdm(name)
    f.run()
