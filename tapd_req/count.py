#!/usr/bin/env python
# -*- coding: utf-8 -*-

import search
from xls import open_xls, write_xls, save_xls
import string


iter_query = {'startdate':'>2018-03-18', 'enddate':'<2018-04-23'}


# 获取迭代id，参数为查询条件，字典形式
def get_iteration_ids(**iterquery):
    ids = []
    iteration = search.Iteration()
    iterdata = iteration.get_iteration(**iterquery)
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
    story = search.Story()
    storyids = []
    for iterid in iterids:
        iter_id_query = {'iteration_id':iterid}
        story_in_iter = story.get_story(**iter_id_query)
        for storys in story_in_iter.json()['data']:
            storyids.append(storys['Story']['id'])
    return storyids


iterate = search.Story()
r = iterate.get_story_custom_fields()
for custom in r.json()['data']:
    print custom['CustomFieldConfig']['custom_field']


# story = search.Story()
# sty = story.get_story(**{'id':'1120990771001012467'})
# print sty.url
# print sty.json()
# print sty.json()['data']['Story']['custom_field_98']

# iterids = get_iteration_ids(**iterquery)
# storyids = get_story_ids(iterids)
#
# print storyids

# tapd = search.BaseTapd()
# abc = tapd('https://api.tapd.cn/stories/custom_field_url', **{'workspace_id':'20990771'})
# print abc.url
