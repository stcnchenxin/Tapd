#!/usr/bin/env python
# -*- coding: utf-8 -*-
import search
from config import TapdRespondFiled as Cfg


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

    # Return a list of the ids of the iterations. The parameter is the QUERY dictionary, just like: {'name': 'iteration_name'}
    def get_iteration_ids(self, **iterquery):
        ids = []
        iterdatas = self.tapd.get_data('iteration', **iterquery)
        for iterdata in self.json_to_list(iterdatas.json()['data']):
            ids.extend(iterdata['Iteration']['id'])
        return ids

    # Return a list of the ids of the iterations. The parameter must be the name of the iteration of tapd.
    def get_iteration_ids_by_name(self, name):
        query = {'name': name}
        ids = self.get_iteration_ids(**query)
        return ids

    # You can get the data of tapd by using this funciton, and the QUERY condition(parameter iterid) is the id of iteration of tapd.
    # request_data_type: The type of the tapd's data, could be 'story', 'task' or 'bug'.
    # iterid: It must be the id of iteration.
    def get_data_by_iterid(self, data_type, iterid):
        r = self.tapd.get_data(data_type, {'iteration_id': iterid})
        return r.json()['data']




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