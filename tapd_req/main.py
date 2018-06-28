#!/usr/bin/env python
# -*- coding: utf-8 -*-


import search
import time
import handle
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


iterids = get_iteration_ids(**{'name': u'2018.06.14版本'})
storys = get_task(iterids)
tapdhendler = handle.TpadDataHandler()
custom_field = get_used_task_custom_fields(DEFAULT_WORKSPACE)
custom_field.extend([u'id', u'name', u'effort'])
print custom_field
for need_data in tapdhendler.task_handler(storys, custom_field):
    for data in need_data:
        print(data)
    print('----------------------------------------')