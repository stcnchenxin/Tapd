#!/usr/bin/env python
# -*- coding: utf-8 -*-

import search
import config
from config import TapdRespondFiled as Cfg
from config import TapdRequestArg as reqCfg
DEFAULT_WORKSPACE = {reqCfg.REQ_WORKSPACE_ID_FIELD: config.TapdSearchContent.DEFAULT_WORKSPACE_ID}
DEFAULT_PAGE_LIMIT_AMOUNT = {reqCfg.REQ_LIMIT_FIELD: reqCfg.REQ_LIMIT_FIELD_DEFAULT}


class TapdJsonHandler(object):
    # Handle json data. When the type of data is dictionary, it will convert to a sequence.
    @staticmethod
    def _json_to_list(tapdjson):
        result = tapdjson
        if isinstance(tapdjson, dict):
            result = [tapdjson]
        return result

    @staticmethod
    def _data_filter(data, field_filter):
        result = {}
        for field in field_filter:
            result.update({field: data[field]})
        return result

    def _data_handle(self, tapdjson):
        return self._json_to_list(tapdjson[Cfg.FIELD_DATA])

    def _collect_data_after_filter(self, tapdjson, data_type, field_filter):
        datas = self._data_handle(tapdjson)
        for data in datas:
            data = data[data_type]
            result = self._data_filter(data, field_filter)
            yield result

    # 返回各种统计json的计数
    @staticmethod
    def count_handle(tapdjson):
        return tapdjson[Cfg.FIELD_DATA][Cfg.FIELD_COUNT]

    # 以下所有的函数都返回json列表中所有符合过滤器元组的生成器，每次生成一个字典，内容包含{{字段: 字段内容}...}模式
    def story_handle(self, tapdjson, field_filter):
        return self._collect_data_after_filter(tapdjson, Cfg.FIELD_STORY, field_filter)

    def story_change_handle(self, tapdjson, field_filter):
        return self._collect_data_after_filter(tapdjson, Cfg.FIELD_STORY_CHANGE, field_filter)

    def bug_handle(self, tapdjson, field_filter):
        return self._collect_data_after_filter(tapdjson, Cfg.FIELD_BUG, field_filter)

    def bug_change_handle(self, tapdjson, field_filter):
        return self._collect_data_after_filter(tapdjson, Cfg.FIELD_BUG_CHANGE, field_filter)

    def task_handle(self, tapdjson, field_filter):
        return self._collect_data_after_filter(tapdjson, Cfg.FIELD_TASK, field_filter)

    def iteration_handle(self, tapdjson, field_filter):
        return self._collect_data_after_filter(tapdjson, Cfg.FIELD_ITERATION, field_filter)

    def custom_field_handle(self, tapdjson, field_filter):
        return self._collect_data_after_filter(tapdjson, Cfg.FIELD_CUSTOM_FIELD, field_filter)


class TpadHandler(TapdJsonHandler):
    def __init__(self):
        self.tapd = search.TapdRequest()

    # 根据传入的id生成各种id查询条件
    @staticmethod
    def _pickle_iterid_query(tid):
        # 返回 迭代字段: 迭代id 的查询条件
        query = {}
        query.update({reqCfg.REQ_ITERATION_ID_FIELD: tid})
        return query

    @staticmethod
    def _pickle_id_query(tid, typename = ''):
        # 根据传入条件不同生成不同的查询id条件
        query = {}
        key = reqCfg.REQ_ID_FIELD
        if typename == 'story':
            key = reqCfg.REQ_STORY_ID_FIELD
        elif typename == 'bug':
            key = reqCfg.REQ_BUG_ID_FIELD
        elif typename == 'task':
            key = reqCfg.REQ_TASK_ID_FIELD
        query.update({key: tid})
        return query

    @staticmethod
    def _pickle_status_stream_query(typename):
        # 状态查询条件跟id有所不同，特写
        query = {}
        query.update({reqCfg.REQ_STATUS_STREAM_SYSTEM: typename})
        return query

    @staticmethod
    def _pickle_query_with_page_limit():
        # 用于生成查询返回较多内容的查询提交（如根据迭代id查询当次迭代内容所有任务，会超过30条的限制，需要此条件进行分块查询）
        query = {}
        query.update({reqCfg.REQ_PAGE_FIELD: 1})
        query.update(DEFAULT_PAGE_LIMIT_AMOUNT)
        return query

    def _yield_data(self, page, typename, query, work_space = DEFAULT_WORKSPACE):
        # 一般用于会返回较多内容的查询（如根据迭代id查询当次迭代内容所有任务），每次返回一页的内容
        # 跟_yield_change_data()类似，调用的 tapd实例 方法有所不同
        for i in range(1, page + 1):
            query[reqCfg.REQ_PAGE_FIELD] = i
            r = self.tapd.get_data(typename, work_space, **query)
            yield r.json()

    def _yield_change_data(self, page, typename, query, work_space = DEFAULT_WORKSPACE):
        # 见_yield_data()
        for i in range(1, page + 1):
            query[reqCfg.REQ_PAGE_FIELD] = i
            r = self.tapd.get_change(typename, work_space, **query)
            yield r.json()

    def get_iterid_by_name(self, name, work_space = DEFAULT_WORKSPACE):
        """ 根据(迭代名字， workspace)获取迭代id """
        r = self.tapd.get_data('iteration', work_space, name = name)
        id_data = r.json()[Cfg.FIELD_DATA]
        try:
            return id_data[0][Cfg.FIELD_ITERATION][Cfg.FIELD_ID]
        except IndexError:
            raise IndexError('has not key, is the iteration name exist?', name)

    def get_storyname_by_storyid(self, sid, work_space = DEFAULT_WORKSPACE):
        """ 根据需求id、工作空间 获取需求标题 """
        r = self.tapd.get_data('story', work_space, id = sid)
        name_data = r.json()[Cfg.FIELD_DATA]
        try:
            return name_data[Cfg.FIELD_STORY][Cfg.FIELD_NAME]
        except IndexError:
            raise IndexError('has not key, is the story id is exist?', sid)

    def get_storyids_by_iterid(self, iterid, work_space = DEFAULT_WORKSPACE):
        """ 根据迭代id、工作空间获取 迭代内所有的需求id， 返回一个列表 """
        ids = []
        for datas in self.get_data_by_iterid('story', iterid, work_space):
            for data in self.story_handle(datas, [reqCfg.REQ_ID_FIELD]):
                ids.append(data[reqCfg.REQ_ID_FIELD])
        return ids

    def get_count_by_iterid(self, typename, tid, work_space = DEFAULT_WORKSPACE):
        """ 根据需要查找的类型名('story', 'bug', 'task')、迭代id、工作空间 获取迭代内的类型数量计数，返回一个 整数 """
        r = self.tapd.get_count(typename, work_space, **self._pickle_iterid_query(tid))
        count = self.count_handle(r.json())
        return count

    def get_data_by_iterid(self, typename, tid, work_space = DEFAULT_WORKSPACE):
        """ 根据需要查找的类型名('story', 'bug', 'task')、迭代id、工作空间 获取迭代内的类型所有内容， 返回一个生成器，每次生成一页的 json（可能有多页，一页包含200个类型的内容）"""
        count = self.get_count_by_iterid(typename, tid, work_space)
        page = int(count / reqCfg.REQ_LIMIT_FIELD_DEFAULT) + 1
        query = self._pickle_iterid_query(tid)
        query.update(self._pickle_query_with_page_limit())
        return self._yield_data(page, typename, query, work_space)

    def get_story_data_by_storyid(self, sid, work_space = DEFAULT_WORKSPACE):
        """ 根据 需求id、工作空间 获取需求内的所有内容，一般用来获取各种数据， 返回一个 json"""
        query = self._pickle_id_query(sid)
        r = self.tapd.get_data('story', work_space, **query)
        return r.json()

    def get_story_change_count_by_storyid(self, tid, work_space = DEFAULT_WORKSPACE):
        """ 根据需求id、工作空间 回去一个需求的变更记录计数，返回一个 整数"""
        query = self._pickle_id_query(tid, 'story')
        r = self.tapd.get_change_count('story', work_space, **query)
        count = self.count_handle(r.json())
        return count

    def get_story_change_by_storyid(self, tid, work_space = DEFAULT_WORKSPACE):
        """ 根据需求id、工作空间 获取需求的所有变更历史， 返回一个生成器，每次生成一页的 json（可能有多页，一页包含200个变更记录）"""
        count = self.get_story_change_count_by_storyid(tid, work_space)
        page = int(count / reqCfg.REQ_LIMIT_FIELD_DEFAULT) + 1
        query = self._pickle_id_query(tid, 'story')
        query.update(self._pickle_query_with_page_limit())
        return self._yield_change_data(page, 'story', query, work_space)

    def get_used_custom_fields(self, typename, work_space = DEFAULT_WORKSPACE):
        """ 根据类型名('story', 'bug', 'iteration')、工作空间，获取相应类型的正在使用中的 自定义字段， 返回一个字典，内容为：{{字段id: 字段自定义名字} ... }"""
        r = self.tapd.get_custom_fields(typename, work_space)
        custom_fields = self._json_to_list(r.json()[Cfg.FIELD_DATA])
        result = {}
        for custom_field in custom_fields:
            field = custom_field[Cfg.FIELD_CUSTOM_FIELDS]
            if field[Cfg.FIELD_CUSTOM_ENABLED] == '1':
                result.update({field[Cfg.FIELD_CUSTOM_FIELD]: field[Cfg.FIELD_CUSTOM_NAME]})
        return result

    def get_status_stream(self, typename, work_space = DEFAULT_WORKSPACE):
        """ 根据 类型名('story', 'bug')、工作空间，获取相应类型的 状态流极其对应名字 ，返回一个字典， 内容为： {{状态流id: 自定义状态流名字} ... } """
        query = self._pickle_status_stream_query(typename)
        r = self.tapd.get_status_stream(typename, work_space, **query)
        return r.json()[Cfg.FIELD_DATA]


if __name__ == '__main__':
    # for test
    tapdhandler = TpadHandler()
    a = tapdhandler.get_used_custom_fields('story')
    for k, v in a.items():
        print(k)
        print(v)
