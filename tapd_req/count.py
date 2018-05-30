#!/usr/bin/env python
# -*- coding: utf-8 -*-

import search
import time
import json
from xls import open_xls, write_xls, save_xls
import string


iter_query = {'startdate': '>2018-03-18', 'enddate': '<2018-04-23'}


# 获取迭代id，参数为查询条件，字典形式
def get_iteration_ids(**iterquery):
    ids = []
    iteration = search.TapdHandler()
    iterdata = iteration.get_data('iteration', **iterquery)
    for data in iterdata.json()['data']:
        ids.append(data['Iteration']['id'])
    return ids


# 打包id查询条件，参数为字典形式，返回：{'id':'id1, id2, id3'}
def pack_id_query(query):
    try:
        iteration_id = ''
        for value in query['id']:
            iteration_id += (value + ',')
        query['id'] = iteration_id
        iteration_id.rstrip(',')
    except KeyError:
        print '没有对应的键: "id"'
    return query


# 获取需求id，参数为迭代id，列表形式
def get_story_ids(iterids):
    story = search.TapdHandler()
    storyids = []
    for iterid in iterids:
        iter_id_query = {'iteration_id': iterid}
        story_in_iter = story.get_data('story', **iter_id_query)
        for storys in story_in_iter.json()['data']:
            storyids.append(storys['Story']['id'])
    return storyids


def get_change_data_by_storys(storyids):
    list(storyids)
    tpad = search.TapdHandler()
    for storyid in storyids:
        data = []
        data.append(storyids)
        query = {'story_id': storyid}

        name = tapd.get_data('story', **query).json()['data']['Story']['name']
        data.append(name)
        time.sleep(1)

        changes = tpad.get_change('story', **query)
        time.sleep(1)


        yield r.json()
        time.sleep(1)


def get_story_name(storyid):
    tapd = search.TapdHandler()
    query = {'id': storyid}
    time.sleep(1)
    name = tapd.get_data('story', **query).json()['data']['Story']['name']
    return name


def test():
    story1 = search.TapdHandler()
    r = story1.get_custom_fields('story')
    for custom in r.json()['data']:
        print custom['CustomFieldConfig']['name']


# open_xls('test.xls')
# styids = get_story_ids([1120990771001000221])
# time.sleep(1)
# for result in get_change_data_by_storys(styids):
#     print result

tapd = search.TapdHandler()
r = tapd.get_change('story', **{'story_id': 1120990771001008766})
for change in r.json()['data']:
    for data in json.loads(change['WorkitemChange']['changes']):
        print data['value_before']
