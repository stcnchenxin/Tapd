#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

import search
import config
from config import TapdRespondFiled as Cfg
from config import TapdRequestArg as reqCfg
DEFAULT_WORKSPACE = {reqCfg.REQ_WORKSPACE_ID_FIELD: config.TapdUrlConfig.WORKSPACE_ID_Q6}
DEFAULT_PAGE_LIMIT_AMOUNT = {reqCfg.REQ_LIMIT_FIELD: reqCfg.REQ_LIMIT_FIELD_DEFAULT}


class TapdJsonHandler(object):
    # Handle json data. When the type of data is dictionary, it will convert to a sequence.
    @staticmethod
    def json_to_list(jsons):
        result = jsons
        if isinstance(jsons, dict):
            result = [jsons]
        return result

    @staticmethod
    def count_handle(json):
        return json[Cfg.FIELD_DATA][Cfg.FIELD_COUNT]

    @staticmethod
    def data_filter(data, field_filter):
        result = {}
        for field in field_filter:
            result.update({field: data[field]})
        return result

    def data_handle(self, json):
        return self.json_to_list(json[Cfg.FIELD_DATA])

    def collect_data_after_filter(self, json, data_type, field_filter):
        datas = self.data_handle(json)
        for data in datas:
            data = data[data_type]
            result = self.data_filter(data, field_filter)
            yield result

    def story_handle(self, json, field_filter):
        return self.collect_data_after_filter(json, Cfg.FIELD_STORY, field_filter)

    def story_change_handle(self, json, field_filter):
        return self.collect_data_after_filter(json, Cfg.FIELD_STORY_CHANGE, field_filter)

    def bug_handle(self, json, field_filter):
        return self.collect_data_after_filter(json, Cfg.FIELD_BUG, field_filter)

    def bug_change_handle(self, json, field_filter):
        return self.collect_data_after_filter(json, Cfg.FIELD_BUG_CHANGE, field_filter)

    def task_handle(self, json, field_filter):
        return self.collect_data_after_filter(json, Cfg.FIELD_TASK, field_filter)

    def iteration_handle(self, json, field_filter):
        return self.collect_data_after_filter(json, Cfg.FIELD_ITERATION, field_filter)

    def custom_field_handle(self, json, field_filter):
        return self.collect_data_after_filter(json, Cfg.FIELD_CUSTOM_FIELD, field_filter)


class TpadHandler(TapdJsonHandler):
    def __init__(self):
        self.tapd = search.TapdRequest()

    @staticmethod
    def _get_search_id_query(type_name, tid):
        query = {}
        if type_name == 'iteration':
            query.update({reqCfg.REQ_ID_FIELD: tid})
        else:
            query.update({reqCfg.REQ_ITERATION_ID_FIELD: tid})
        return query

    # Return a list of the ids of the iterations. The parameter must be the name of the iteration of tapd.
    def get_iteration_id_by_name(self, name, work_space = DEFAULT_WORKSPACE):
        r = self.tapd.get_data('iteration', work_space, name = name)
        id_data = self.json_to_list(r.json()[Cfg.FIELD_DATA])
        return id_data[0][Cfg.FIELD_ITERATION][Cfg.FIELD_ID]

    # You can get the data of tapd by using this funciton, and the QUERY condition(parameter iterid) is the id of iteration of tapd.
    # request_data_type: The type of the tapd's data, could be 'story', 'task' or 'bug'.
    # iterid: It must be the id of iteration.
    @staticmethod
    def _pickle_query_with_page_limit():
        query = {}
        query.update({reqCfg.REQ_PAGE_FIELD: 1})
        query.update(DEFAULT_PAGE_LIMIT_AMOUNT)
        return query

    def get_storyids_by_iterid(self, iterid, work_space = DEFAULT_WORKSPACE):
        ids = []
        for datas in self.get_data_by_id('story', iterid, work_space):
            for data in self.story_handle(datas, [reqCfg.REQ_ID_FIELD]):
                ids.append(data[reqCfg.REQ_ID_FIELD])
        return ids

    def get_count_by_id(self, typename, tid, work_space = DEFAULT_WORKSPACE):
        r = self.tapd.get_count(typename, work_space, **self._get_search_id_query(typename, tid))
        count = self.count_handle(r.json())
        return count

    def get_change_count_by_id(self, typename, tid, work_space = DEFAULT_WORKSPACE):
        r = self.tapd.get_change_count(typename, work_space, **self._get_search_id_query(typename, tid))
        count = self.count_handle(r.json())
        return count

    def _yield_data(self, count, typename, method, tid, work_space = DEFAULT_WORKSPACE):
        page = int(count / reqCfg.REQ_LIMIT_FIELD_DEFAULT) + 1
        query = self._get_search_id_query(typename, tid)
        query.update(self._pickle_query_with_page_limit())
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', count, '---', page)
        print(query)
        for i in range(1, page + 1):
            query[reqCfg.REQ_PAGE_FIELD] = i
            if method == 'data':
                r = self.tapd.get_data(typename, work_space, **query)
            elif method == 'change':
                r = self.tapd.get_change(typename, work_space, **query)
            time.sleep(1)  # TAPD请求限制，每秒1条
            yield r.json()

    def get_data_by_id(self, typename, tid, work_space = DEFAULT_WORKSPACE):
        r""" For story, bug, iteration, task, you can select one by typename"""
        count = self.get_count_by_id(typename, tid, work_space)
        return self._yield_data(count, typename, 'data', tid, work_space)

    def get_change_by_id(self, typename, tid, work_space = DEFAULT_WORKSPACE):
        r""" Just for story and bug"""
        count = self.get_change_count_by_id(typename, tid, work_space)
        return self._yield_data(count, typename, 'change', tid, work_space)

