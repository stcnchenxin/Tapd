#!/usr/bin/env python
# -*- coding: utf-8 -*-
import handle
import config
import xls as excel
import json
DEFAULT_WORKSPACE = {config.TapdRequestArg.REQ_WORKSPACE_ID_FIELD: config.TapdSearchContent.DEFAULT_WORKSPACE_ID}



def write_task(iter_name, task_filter, condits, xlspath, line_dict, row = 2, workspace = DEFAULT_WORKSPACE):
    r""" 筛选相应的迭代内的任务，并写入任务数据
    :param iter_name: string, 迭代名称
    :param task_filter: 需要筛选写入excel表的任务字段，必须包含('owner',)，格式如：('owner', 'effort', 'name', ...)
    :type task_filter: tuple
    :param condits: 筛选的人员名单，同时也会作为excel表的sheet分页，注意：写入的excel表的sheet分页必须与传入的这个参数一致，格式如：(u'甘芳琳;', u'邹祖业;', ...)
    :type condits: tuple
    :param xlspath: string, 写入的excel表的路径
    :param line_dict: 行字典，用于控制各人员的起始行，格式如：{u'甘芳琳;': 2, u'邹祖业;': 2, ...}, 其中2为起始的行
    :type line_dict: dict
    :param row: int, 为起始列，会根据 task_filter 内元素加一行列，默认值为2
    :param workspace: int, tapd默认工作空间id，默认是Q6的工作空间id
    :return: None
    """
    tapdHander = handle.TpadHandler()
    wb = excel.open_xls(xlspath)
    iter_id = tapdHander.get_iterid_by_name(iter_name, workspace)
    for datas in tapdHander.get_data_by_iterid('task', iter_id, workspace):
        for data in tapdHander.task_handle(datas, task_filter):
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


def write_story_adnormal_data(iter_name, story_filter_tuple, xlspath, sheet, line = 2, row = 2, workspace = DEFAULT_WORKSPACE, need_new_date = False):
    r""" 筛选对应迭代内异常的需求，将相应需要的需求数据写入excel表，对于异常的时间会加上红色警示格
    :param iter_name: 迭代名称
    :param story_filter_tuple: 需要写入excel表的需求的字段序列，至少包含('name',)，格式如：('owner', 'effort', 'name', ...)
    :type story_filter_tuple: tuple
    :param xlspath: string, 写入的excel表路径
    :param sheet: string, 写入的excel的sheet分页
    :param line: int, 写入数据的起始行，默认为2
    :param row: int, 写入数据的起始列，默认为2
    :param workspace: int, tapd默认工作空间id，默认是Q6的工作空间id
    :param need_new_date: bool, 是否需要最新的时间， tapd同个状态可能存在多个时间，如多次待测，默认值为False，即只保留第一次待测时间， True则是最近待测的时间
    :return: None
    """
    # 初始化表格相关的字典
    info_story_status_dict = dict(zip(config.TapdSearchContent.CHANGE_STORY_STATUS_KEY_WORD, config.TapdSearchContent.CHANGE_STORY_TIME_LIMIT))
    info_story_status_row_dict = dict(zip(config.TapdSearchContent.CHANGE_STORY_STATUS_KEY_WORD, config.TapdSearchContent.CHANGE_STORY_STATUS_ROW))
    wb = excel.open_xls(xlspath)
    tapdHander = handle.TpadHandler()
    iter_id = tapdHander.get_iterid_by_name(iter_name)
    story_ids = tapdHander.get_storyids_by_iterid(iter_id)
    story_status = tapdHander.get_status_stream('story', workspace)

    start_line = line

    # 遍历迭代内的所有需求id
    for story_id in story_ids:
        # 获取每个需求的所有变更历史，并遍历
        for changes in tapdHander.get_story_change_by_storyid(story_id):
            # is_abnormal_flag = False
            info_story_status_time = dict(zip(config.TapdSearchContent.CHANGE_STORY_STATUS_KEY_WORD, config.TapdSearchContent.CHANGE_STORY_DEFAULT_TIME))

            # 遍历所有变更历史里的单个变更内容
            for change in tapdHander.story_change_handle(changes, ('created', 'changes')):
                change_field = json.loads(change['changes'])
                for status in change_field:
                    # 如果变更内容是状态，则确定是否异常需要找的异常状态，如果是异常则计入数据
                    if status['field'] == 'status':
                        change_time = change['created']
                        if story_status[status['value_after']] in info_story_status_dict.keys():
                            # find the abnormal story(the changed time lower than limit time).
                            status_key = story_status[status['value_after']]
                            # 更新时间
                            update_status_time(info_story_status_time, status_key, change_time, need_new_date)

            # 写入异常需求的时间数据
            story_json = tapdHander.get_story_data_by_storyid(story_id)
            story_datas = tapdHander.story_handle(story_json, story_filter_tuple)
            start_row = row
            for story_data in story_datas:
                for story_v in story_data.values():
                    excel.write_xls(wb, sheet, start_line, start_row, story_v)
                    start_row += 1
            # 写入时间数据
            for k, v in info_story_status_time.items():
                if is_abnormal_time(info_story_status_time[k], info_story_status_dict[k]):
                    excel.write_abnromal_xls(wb, sheet, start_line, info_story_status_row_dict[k], time_to_date(v))
                else:
                    excel.write_xls(wb, sheet, start_line, info_story_status_row_dict[k], time_to_date(v))
            start_line += 1
            excel.save_xls(xlspath, wb)


def is_abnormal_time(changed_time, limit_time):
    # 判断是否异常时间
    if changed_time > limit_time:
        return True
    return False


def time_to_date(times):
    # 拆分tapd的修改时间，返回只有日期的函数
    if times is None:
        return None
    t = times.split(' ')
    d = t[0].split('-')
    return '/'.join(d)


def update_status_time(dictionary, key, new_date, need_new):
    # 更新状态时间字典
    if dictionary[key] is None:
        dictionary[key] = new_date
        return
    if need_new:
        if dictionary[key] < new_date:
            dictionary[key] = new_date
    else:
        if dictionary[key] > new_date:
            dictionary[key] = new_date


if __name__ == '__main__':
    write_task(u'2018.05.18维护', config.TapdSearchContent.TASK_FILTER_LIST, config.TapdSearchContent.TASK_OWNER_Q6_QC, 'test.xls', {u'甘芳琳;': 2, u'邹祖业;': 2, u'赖增涛;': 2, u'肖兴亮;': 2})
    write_story_adnormal_data(u'测试迭代', ('id', 'name', 'owner'), 'test.xls', u'甘芳琳;')

