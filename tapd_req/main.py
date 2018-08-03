#!/usr/bin/env python
# -*- coding: utf-8 -*-
import handle
import config
import xls as excel
from config import TapdSearchType as Cfg
DEFAULT_WORKSPACE = {'workspace_id': config.TapdUrlConfig.WORKSPACE_ID_Q6}


def write_task(iter_name, filter_list, condits, xlspath, line_dict, row = 2, workspace = DEFAULT_WORKSPACE):
    jsonHander = handle.TapdJsonHandler()
    tapdHander = handle.TpadHandler()
    wb = excel.open_xls(xlspath)
    iter_id = tapdHander.get_iteration_id_by_name(iter_name, workspace)
    for datas in tapdHander.get_data_by_id('task', iter_id, workspace):
        for data in jsonHander.task_handle(datas, filter_list):
            page = data['owner']
            for condit in condits:
                if condit in page:
                    start_row = row
                    for key, value in data.items():
                        if key == 'effort':
                            value = float(value)
                        excel.write_xls(wb, condit, line_dict[condit], start_row, value)
                        start_row += 1
                    line_dict[condit] += 1
            excel.save_xls(xlspath, wb)


def test():
    tapdHander = handle.TpadHandler()
    iter_id = tapdHander.get_iteration_id_by_name(u'2018.05.04维护')
    story_ids = tapdHander.get_storyids_by_iterid(iter_id)
    print(story_ids)
    for story_id in story_ids:
        for change in tapdHander.get_change_by_id('story', story_id):
            print(story_id, 'ffffffffffffffffffffffffffff')
            # print(change)


# write_task(u'2018.05.18维护', Cfg.TASK_FILTER_LIST, Cfg.Q6_QC, 'test.xls', {u'甘芳琳;': 2, u'邹祖业;': 2, u'赖增涛;': 2, u'肖兴亮;': 2})
test()