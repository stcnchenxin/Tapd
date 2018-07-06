#!/usr/bin/env python
# -*- coding: utf-8 -*-
import search


class TpadDataHandler(object):
    def story_handler(self, storyjson, fieldlist):
        jsons = self._json_to_list(storyjson['data'])
        for storydata in jsons:
            story = storydata['Story']
            result = []
            for field in fieldlist:
                result.append({field: story[field]})
            yield result

    def task_handler(self, taskjson, fieldlist):
        jsons = self._json_to_list(taskjson['data'])
        for taskjson in jsons:
            task = taskjson['Task']
            midresult = {}
            for field in fieldlist:
                midresult.update({field: task[field]})
            yield midresult

    def _json_to_list(self, jsons):
        result = []
        if isinstance(jsons, dict):
            result = [jsons]
        elif isinstance(jsons, list):
            result = jsons
        return result


if __name__ == '__main__':
    test = TpadDataHandler()
    sto = search.TapdRequest()
    r = sto.get_data('story', **{'id': 1120990771001016761})
    r1 = sto.get_data('story', **{'id': '1120990771001016761,1120990771001022165'})

    aaa = test.story_handler(r1.json(), ['children_id', 'category_id'])
    print aaa