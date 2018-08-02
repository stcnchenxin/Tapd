#!/usr/bin/env python
# -*- coding: utf-8 -*-
import handle
import xls as excel
import config as Cfg


def writetask():
    jsonHander = handle.TapdJsonHandler()
    tapdHander = handle.TpadHandler()
    wb = excel.open_xls('test.xls')
    line = {u'甘芳琳;': 2, u'邹祖业;': 2, u'赖增涛;': 2, u'肖兴亮;': 2}
    iter_id = tapdHander.get_iteration_id_by_name(u'2018.08.10维护')
    datas = tapdHander.get_data_by_id('task', iter_id)
    for data in jsonHander.type_task_handle(datas, ['effort', 'name', 'owner']):
        condit = Cfg.CharacterCombination.Q6_QC
        page = data['owner']
        if page in condit:
            row = 2
            for key, value in data.items():
                if key == 'effort':
                    value = float(value)
                excel.write_xls(wb, page, line[page], row, value)
                row += 1
            line[page] += 1
        excel.save_xls('test.xls', wb)


writetask()