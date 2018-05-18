#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlrd
import xlwt
from xlutils.copy import copy


DEFAULT_STYTLE = xlwt.Style.easyxf(u"font: height 0x00DC, name 微软雅黑; borders: left 0x01, right 0x01, top 0x01, bottom 0x01")


def open_xls(filepath):
    rb = xlrd.open_workbook(filepath, formatting_info=True)
    wbk = copy(rb)
    return wbk


def write_xls(wbk, sheet, row, col, str1, styl=DEFAULT_STYTLE):
    ws = wbk.get_sheet(sheet)
    ws.write(row, col, str1, styl)


def save_xls(filepath, wbk):
    wbk.save(filepath)


wb = open_xls('test.xls')
write_xls(wb, 1, 10, 10, u'中文啊啊啊阿萨德吉tetw是点分解fooooo')
write_xls(wb, 1, 11, 10, 04.22)
save_xls('test.xls', wb)

