#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlrd
import xlwt
from config import XlsFormatConfig
from xlutils.copy import copy
DEFAULT_STYTLE = xlwt.Style.easyxf(XlsFormatConfig.DEFAULT_FORMAT)


# use open_xls(filepath) to open the file named *.xls, and it will return a excel workbook, you can use it to write data.
# use write_xls(workbook, sheet, row, col, string, style) to write data:
#     The workbook was returned by open_xls(filepath), and the default cell style is: [fontname: YaHei, fontsize: 11, and with border]
# use save_xls(filepath, workbook) to save *.xls. Don't forget call it after you write the data into file.
def open_xls(filepath):
    rb = xlrd.open_workbook(filepath, formatting_info = True)
    wbk = copy(rb)
    return wbk


def write_xls(wbk, sheet, row, col, str1, styl = DEFAULT_STYTLE):
    ws = wbk.get_sheet(sheet)
    ws.write(row, col, str1, styl)


def save_xls(filepath, wbk):
    wbk.save(filepath)


if __name__ == '__main__':
    wb = open_xls('test.xls')
    write_xls(wb, 1, 10, 10, u'中文啊啊啊阿萨德吉tetw是点分解fooooo')
    save_xls('test.xls', wb)

