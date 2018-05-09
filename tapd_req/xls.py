#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlrd
import xlwt
from xlwt import Style
from xlutils.copy import copy


def open_xls(filepath):
    rb = xlrd.open_workbook(filepath, formatting_info=True)
    wb = copy(rb)
    return wb


def write_xls(wb, sheet, row, col, str, styl=Style.default_style):
    ws = wb.get_sheet(sheet)
    ws.write(row, col, str, styl)


def save_xls(filepath, wb):
    wb.save(filepath)

