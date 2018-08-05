#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlwt
from config import XlsFormatConfig
from xlutils.copy import copy
import xlrd
DEFAULT_STYTLE = xlwt.Style.easyxf(XlsFormatConfig.DEFAULT_FORMAT)
ABNORMAL_STYTLE = xlwt.Style.easyxf(XlsFormatConfig.ABNORMAL_FORMAT)


# use open_xls(filepath) to open the file named *.xls, and it will return a excel workbook, you can use it to write data.
# use write_xls(workbook, sheet, row, col, string, style) to write data:
#     The workbook was returned by open_xls(filepath), and the default cell style is: [fontname: YaHei, fontsize: 11, and with border]
# use save_xls(filepath, workbook) to save *.xls. Don't forget call it after you write the data into file.
def open_xls(filepath):
    r""" 通过 excel表路径 打开excel表，返回一个excel工作表对象，用于写入excel数据 """
    rb = xlrd.open_workbook(filepath, formatting_info = True)
    wbk = copy(rb)
    return wbk


def write_xls(wbk, sheet, row, col, str1, styl = DEFAULT_STYTLE):
    r""" 写入excel表， 参数分别为： 工作表对象(通过open_xls()得到、写入的分页名、写入行、写入列、写入格式)， 此函数用默认格式"""
    ws = wbk.get_sheet(sheet)
    ws.write(row, col, str1, styl)


def write_abnromal_xls(wbk, sheet, row, col, str1, styl = ABNORMAL_STYTLE):
    r""" 写入excel表， 参数分别为： 工作表对象(通过open_xls()得到、写入的分页名、写入行、写入列、写入格式)， 此函数用异常格式"""
    ws = wbk.get_sheet(sheet)
    ws.write(row, col, str1, styl)


def save_xls(filepath, wbk):
    r""" 报错excel表， 将 wbk(工作表对象) 保存到给定的路径中"""
    wbk.save(filepath)


if __name__ == '__main__':
    wb = open_xls('test.xls')
    write_abnromal_xls(wb, u'甘芳琳;', 10, 10, u'中文啊啊啊阿萨德吉tetw是点分解fooooo')
    save_xls('test.xls', wb)

