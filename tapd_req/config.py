#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TapdUrlConfig(object):
    r"""
    The configure of request URL of Tapd.
    """
    URL_GET_STORY = 'https://api.tapd.cn/stories'
    URL_GET_STORY_COUNT = 'https://api.tapd.cn/stories/count'
    URL_GET_STORY_CUSTOM_FIELDS = 'https://api.tapd.cn/stories/custom_fields_settings'
    URL_GET_STORY_CHANGE = 'https://api.tapd.cn/story_changes'
    URL_GET_STORY_CHANGE_COUNT = 'https://api.tapd.cn/story_changes/count'
    URL_GET_BUG = 'https://api.tapd.cn/bugs'
    URL_GET_BUG_COUNT = 'https://api.tapd.cn/bugs/count'
    URL_GET_BUG_GROUP_COUNT = 'https://api.tapd.cn/bugs/group_count'
    URL_GET_BUG_CUSTOM_FIELDS = 'https://api.tapd.cn/bugs/custom_fields_settings'
    URL_GET_BUG_CHANGE = 'https://api.tapd.cn/bug_changes'
    URL_GET_BUG_CHANGE_COUNT = 'https://api.tapd.cn/bug_changes/count'
    URL_POST_ADD_BUG = 'https://api.tapd.cn/bugs'
    URL_GET_TASK = 'https://api.tapd.cn/tasks'
    URL_GET_TASK_COUNT = 'https://api.tapd.cn/tasks/count'
    URL_GET_TASK_CUSTOM_FIELDS = 'https://api.tapd.cn/tasks/custom_fields_settings'
    URL_POST_ADD_TASK = 'https://api.tapd.cn/tasks'
    URL_GET_ITERATION = 'https://api.tapd.cn/iterations'
    URL_GET_ITERATION_COUNT = 'https://api.tapd.cn/iterations/count'
    URL_GET_ITERATION_CUSTOM_FIELDS = 'https://api.tapd.cn/iterations/custom_fields_settings'
    URL_GET_RELATION = 'https://api.tapd.cn/relations'

    WORKSPACE_ID_Q6 = '20990771'


class TapdRequestArg(object):
    REQ_ID_FIELD = 'id'  # id字段
    REQ_WORKSPACE_ID_FIELD = 'workspace_id'  # 迭代id字段
    REQ_ITERATION_ID_FIELD = 'iteration_id'

    REQ_PAGE_FIELD = 'page'
    REQ_LIMIT_FIELD = 'limit'  # 限制条数字段
    REQ_LIMIT_FIELD_DEFAULT = 200  # 默认限制条数数量，tapd官方为30， 这里改成200


class TapdRespondFiled(object):
    r"""
    The configure that is the fields of Tapd's Respond Data.
    """
    # First level field.
    FIELD_DATA = 'data'

    # Second level field.
    # About Story
    FIELD_STORY = 'Story'
    FIELD_STORY_CHANGE = 'WorkitemChange'

    # About bug
    FIELD_BUG = 'Bug'
    FIELD_BUG_CHANGE = 'BugChange'

    # About task
    FIELD_TASK = 'Task'

    # About Iteration
    FIELD_ITERATION = 'Iteration'

    # Common field.
    FIELD_CUSTOM_FIELD = 'CustomFieldConfig'
    FIELD_COUNT = 'count'

    # The lower-level field.
    FIELD_ID = 'id'


class TapdSearchType(object):
    Q6_QC = [u'甘芳琳;', u'邹祖业;', u'赖增涛;', u'肖兴亮;']
    TASK_FILTER_LIST = ['name', 'effort', 'owner']


class XlsFormatConfig(object):
    r"""
    字体：微软雅黑，字号11，加边框
    """
    DEFAULT_FORMAT = u"font: height 0x00DC, name 微软雅黑; borders: left 0x01, right 0x01, top 0x01, bottom 0x01"