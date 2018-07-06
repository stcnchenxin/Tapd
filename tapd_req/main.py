#!/usr/bin/env python
# -*- coding: utf-8 -*-


import search
import time
import handle
import xls as excel
from config import TapdUrlConfig as Cfg
DEFAULT_WORKSPACE = {'workspace_id': Cfg.WORKSPACE_ID_Q6}


# 获取迭代id，参数为查询条件，字典形式
def get_iteration_ids(**iterquery):
    ids = []
    iteration = search.TapdRequest()
    iterdatas = iteration.get_data('iteration', **iterquery)
    for iterdata in iterdatas.json()['data']:
        ids.append(iterdata['Iteration']['id'])
    return ids


def get_story(iterid):
    tapd = search.TapdRequest()
    r = tapd.get_data('story', {'iteration_id': iterid})
    return r.json()


def get_task(iterid):
    tapd = search.TapdRequest()
    r = tapd.get_data('task', {'iteration_id': iterid})
    return r.json()


def get_story_name(storyid):
    tapd = search.TapdRequest()
    query = {'id': storyid}
    time.sleep(1)
    name = tapd.get_data('story', **query).json()['data']['Story']['name']
    return name


def get_used_story_custom_fields(workspace = DEFAULT_WORKSPACE):
    tapd = search.TapdRequest()
    r = tapd.get_custom_fields('story', workspace)
    result = []
    for customfield in r.json()['data']:
        result.append(customfield['CustomFieldConfig']['custom_field'])
    return result


def get_used_task_custom_fields(workspace = DEFAULT_WORKSPACE):
    tapd = search.TapdRequest()
    r = tapd.get_custom_fields('task', workspace)
    result = []
    for customfield in r.json()['data']:
        result.append(customfield['CustomFieldConfig']['custom_field'])
    return result


def get_task_data_by_query(itername, field):
    iterids = get_iteration_ids(**{'name': itername})
    task = get_task(iterids)
    tapdhendler = handle.TpadDataHandler()
    custom_field = get_used_task_custom_fields(DEFAULT_WORKSPACE)
    custom_field.extend(field)
    for need_data in tapdhendler.task_handler(task, custom_field):
        yield need_data


def task_data_filter(be_filter_dict, filter_content, filter_conditons):
    for condition in filter_conditons:
        if condition == be_filter_dict[filter_content]:
            return be_filter_dict[filter_content]
    return ''


xls = excel.XlsWriter()
wb = xls.open_xls('test.xls')
line = {u'甘芳琳;': 2, u'邹祖业;': 2, u'赖增涛;': 2, u'肖兴亮;': 2}
for data in get_task_data_by_query(u'2018.06.02维护', ['effort', 'name', 'owner']):
    condit = [u'甘芳琳;', u'邹祖业;', u'赖增涛;', u'肖兴亮;']
    page = task_data_filter(data, 'owner', condit)
    if page:
        row = 2
        for key, value in data.items():
            xls.write_xls(wb, page, line[page], row, value)
            row += 1
        line[page] += 1
xls.save_xls('test.xls', wb)
