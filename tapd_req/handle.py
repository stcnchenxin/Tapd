#!/usr/bin/env python
# -*- coding: utf-8 -*-
import search
import config
from config import TapdRespondFiled as Cfg
DEFAULT_WORKSPACE = {'workspace_id': config.TapdUrlConfig.WORKSPACE_ID_Q6}


class TapdJsonHandler(object):
    # Handle json data. When the type of data is dictionary, it will convert to a sequence.
    @staticmethod
    def json_to_list(jsons):
        result = jsons
        if isinstance(jsons, dict):
            result = [jsons]
        return result

    @staticmethod
    def type_count_handle(json):
        return json(json[Cfg.FIELD_DATA][Cfg.FIELD_COUNT])

    @staticmethod
    def data_filter(data, field_filter):
        result = {}
        try:
            for field in field_filter:
                result.update({field: data[field]})
        except KeyError:
            print("The data has not key: " + field)
        return result

    def type_data_handle(self, json):
        return self.json_to_list(json[Cfg.FIELD_DATA])

    def collect_data_after_filter(self, json, data_type, field_filter):
        datas = self.type_data_handle(json)
        for data in datas:
            data = data[data_type]
            result = self.data_filter(data, field_filter)
            yield result

    def type_story_handle(self, json, field_filter):
        return self.collect_data_after_filter(json, Cfg.FIELD_STORY, field_filter)

    def type_story_change_handle(self, json, field_filter):
        return self.collect_data_after_filter(json, Cfg.FIELD_STORY_CHANGE, field_filter)

    def type_bug_handle(self, json, field_filter):
        return self.collect_data_after_filter(json, Cfg.FIELD_BUG, field_filter)

    def type_bug_change_handle(self, json, field_filter):
        return self.collect_data_after_filter(json, Cfg.FIELD_BUG_CHANGE, field_filter)

    def type_task_handle(self, json, field_filter):
        return self.collect_data_after_filter(json, Cfg.FIELD_TASK, field_filter)

    def type_iteration_handle(self, json, field_filter):
        return self.collect_data_after_filter(json, Cfg.FIELD_ITERATION, field_filter)

    def type_custom_field_handle(self, json, field_filter):
        return self.collect_data_after_filter(json, Cfg.FIELD_CUSTOM_FIELD, field_filter)


class TpadHandler(TapdJsonHandler):
    def __init__(self):
        self.tapd = search.TapdRequest()

    # Return a list of the ids of the iterations. The parameter must be the name of the iteration of tapd.
    def get_iteration_id_by_name(self, name, wsp = DEFAULT_WORKSPACE):
        r = self.tapd.get_data('iteration', wsp, name = name)
        id_data = self.json_to_list(r.json()['data'])
        return id_data[0]['Iteration']['id']

    # You can get the data of tapd by using this funciton, and the QUERY condition(parameter iterid) is the id of iteration of tapd.
    # request_data_type: The type of the tapd's data, could be 'story', 'task' or 'bug'.
    # iterid: It must be the id of iteration.
    def get_data_by_id(self, typename, tid, wsp = DEFAULT_WORKSPACE):
        if typename == 'iteration':
            r = self.tapd.get_data(typename, wsp, id = tid)
        else:
            r = self.tapd.get_data(typename, wsp, iteration_id = tid)
        return r.json()


#
# if __name__ == '__main__':
#     sto = search.TapdRequest()
#     r0 = sto.get_data('story', **{'id': 1120990771001016761})
#     r1 = sto.get_data('story', **{'id': '1120990771001016761,1120990771001022165'})
#
#     # print(r0.json())
#     jsonh = TapdJsonHandler()
#     a = jsonh.type_story_handle(r1.json(), ['id', 'modified'])
#     for b in a:
#         print(b)