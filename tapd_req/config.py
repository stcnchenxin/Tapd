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

    URL_GET_STATUS_STREAM = 'https://api.tapd.cn/workflows/status_map'


class TapdRequestArg(object):
    r""" The request argument(field) of tapd
    """
    REQ_ID_FIELD = 'id'  # id字段
    REQ_WORKSPACE_ID_FIELD = 'workspace_id'  # 迭代id字段
    REQ_ITERATION_ID_FIELD = 'iteration_id'
    REQ_STORY_ID_FIELD = 'story_id'
    REQ_TASK_ID_FIELD = 'task_id'
    REQ_BUG_ID_FIELD = 'bug_id'

    # 以下3个内容用于会返回大量内容的tapd请求（如请求迭代内容所有的任务，可能超过30条）
    REQ_PAGE_FIELD = 'page'
    REQ_LIMIT_FIELD = 'limit'  # 限制条数字段
    REQ_LIMIT_FIELD_DEFAULT = 200  # 默认限制条数数量，tapd官方为30， 这里改成200

    # 状态流相关字段
    REQ_STATUS_STREAM_SYSTEM = 'system'


class TapdRespondFiled(object):
    r"""
    The configure that is the fields of Tapd's Respond Data.
    """
    # Top level field.
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

    # Common custome field.
    FIELD_CUSTOM_FIELDS = 'CustomFieldConfig'
    FIELD_COUNT = 'count'

    # The lower-level field.
    # About Story

    # About bug

    # About task

    # About Iteration

    # Common custome field.
    FIELD_CUSTOM_FIELD = 'custom_field'
    FIELD_CUSTOM_NAME = 'name'
    FIELD_CUSTOM_ENABLED = 'enabled'

    # Common fields.
    FIELD_ID = 'id'
    FIELD_NAME = 'name'


class TapdSearchContent(object):
    r"""用来设置各种请求id及需要过滤保留到excel表中的数据"""
    # 默认的tapd工作空间id
    DEFAULT_WORKSPACE_ID = '20990771'
    WORKSPACE_ID_Q6 = '20897871'

    # 需要记录任务的人员名单
    TASK_OWNER_Q6_QC = (u'甘芳琳;', u'邹祖业;', u'赖增涛;', u'肖兴亮;')
    # 需要筛选的任务字段名
    TASK_FILTER_LIST = ('name', 'effort', 'owner')

    # 需要记录的状态名单，根据实际自己的项目定义填，需要注意的是，下面4个常量的元素数量需要有对应关系，以第一个状态名为准，如状态名单共有3个元素，则下面的3个参数需要跟着修改为3个元素
    CHANGE_STORY_STATUS_KEY_WORD = (u'完成待测试', u'待提交', u'测试关闭')
    # 记录到表中的状态的行数，按下面的写法：完成待测试的数据会写在第 10 列，以此类推
    CHANGE_STORY_STATUS_ROW = (10, 11, 12)
    # 用于判断时间是否异常的临界时间，按下面的写法：完成待测试的时间 超过 2018-04-25 15:37:26，则会被认为异常，以此类推
    CHANGE_STORY_TIME_LIMIT = (u'2018-08-05 15:37:26', u'2018-04-25 15:37:26', u'2018-04-25 15:37:26')
    # 用于生成需求状态实际发生变更的真实时间的初始数据，无需关注，只有在 状态名单 的元素数量发生变化时才需要修改，如状态名单元素数量变为 4 个，则需要改成 (None, None, None, None)
    CHANGE_STORY_DEFAULT_TIME = (None, None, None)

    # CHANGE_STORY_STATUS_KEY_WORD = (u'测试中', u'验收中', u'已实现')  # for test



class XlsFormatConfig(object):
    r"""
    excel表的写入格式
    """
    # 字体：微软雅黑，字号11，加边框
    DEFAULT_FORMAT = u"font: height 0x00DC, name 微软雅黑; borders: left 0x01, right 0x01, top 0x01, bottom 0x01"
    # 字体：微软雅黑，字号11，加边框，加红色底框
    ABNORMAL_FORMAT = u"font: height 0x00DC, name 微软雅黑; borders: left 0x01, right 0x01, top 0x01, bottom 0x01; pattern: pattern solid, fore_colour red"
