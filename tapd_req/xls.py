#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlrd
import xlwt
from config import XlsFormatConfig
from xlutils.copy import copy
DEFAULT_STYTLE = xlwt.Style.easyxf(XlsFormatConfig.DEFAULT_FORMAT)


class XlsWriter(object):
    r"""
    This class is using to write the data in Excel file.

    use open_xls(filepath) to open the file named *.xls, and it will return a excel workbook, you can use it to write data.
    use write_xls(workbook, sheet, row, col, string, style) to write data:
        The workbook was returned by open_xls(filepath), and the default cell style is: [fontname: YaHei, fontsize: 11, and with border]
    use save_xls(filepath, workbook) to save *.xls. Don't forget call it after you write the data into file.
    """
    def open_xls(self, filepath):
        rb = xlrd.open_workbook(filepath, formatting_info=True)
        wbk = copy(rb)
        return wbk

    def write_xls(self, wbk, sheet, row, col, str1, styl = DEFAULT_STYTLE):
        ws = wbk.get_sheet(sheet)
        ws.write(row, col, str1, styl)

    def save_xls(self, filepath, wbk):
        wbk.save(filepath)


class XlsReader(object):
    pass


if __name__ == '__main__':
    xls = XlsWriter()
    wb = xls.open_xls('test.xls')
    xls.write_xls(wb, 1, 10, 10, u'中文啊啊啊阿萨德吉tetw是点分解fooooo')
    xls.save_xls('test.xls', wb)

