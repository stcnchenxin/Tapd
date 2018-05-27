#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from tapd_req.search import TapdHandler
import time


class TapdTestCase(unittest.TestCase):
    r"""
    This testcase would test the functions in the class TapdTestCase.
    """
    def __init__(self, *args, **kwargs):
        super(TapdTestCase, self).__init__(*args, **kwargs)
        self._tpad = TapdHandler()

    def test_iteration(self):
        _iter_id = {'id': 1120990771001000210}
        r = self._tpad.get_data('iteration', **_iter_id)
        self.assertTrue(int(r.json()['data']['Iteration']['id']) == _iter_id['id'], 'TapdHandler.get_iteration() is not successd, the status_code is ' + str(r.status_code))

        r = self._tpad.get_count('iteration', **_iter_id)
        self.assertTrue(int(r.json()['data']['count']) == 1, 'TapdHandler.get_iteration_count() is not successd, the status_code is ' + str(r.status_code))

        r = self._tpad.get_custom_fields('iteration')
        self.assertTrue(r.status_code == 200, 'TapdHandler.get_iteration_custom_fields() is not successd, the status_code is ' + str(r.status_code))

    def test_story(self):
        _query_id = {'id': 1120990771001016761}
        _story_id = {'story_id': 1120990771001016761}

        r = self._tpad.get_data('story', **_query_id)
        self.assertTrue(int(r.json()['data']['Story']['id']) == _query_id['id'], 'TapdHandler.get_story() is not successd, the status_code is ' + str(r.status_code))

        r = self._tpad.get_count('story', **_query_id)
        self.assertTrue(int(r.json()['data']['count']) == 1, 'TapdHandler.get_story_count() is not successd, the status_code is ' + str(r.status_code))

        r = self._tpad.get_custom_fields('story')
        self.assertTrue(r.json()['data'] != [], 'TapdHandler.get_story_custom_fields() is not successd, the status_code is ' + str(r.status_code))

        r = self._tpad.get_change('story', **_story_id)
        self.assertTrue(int(r.json()['data'][0]['WorkitemChange']['story_id']) == _story_id['story_id'], 'TapdHandler.get_story_change() is not successd, the status_code is ' + str(r.status_code))

        r = self._tpad.get_change_count('story', **_story_id)
        self.assertTrue(r.json()['data'] != [], 'TapdHandler.get_story_change_count() is not successd, the status_code is ' + str(r.status_code))

    def test_bug(self):
        _bug_id = {'id': 1120990771001004288}

        r = self._tpad.get_data('bug', **_bug_id)
        self.assertTrue(int(r.json()['data']['Bug']['id']) == _bug_id['id'], 'TapdHandler.get_bug() is not successd, the status_code is ' + str(r.status_code))

        r = self._tpad.get_count('bug', **_bug_id)
        self.assertTrue(r.json()['data']['count'] != [], 'TapdHandler.get_bug_count() is not successd, the status_code is ' + str(r.status_code))

        r = self._tpad.get_group_count('bug')
        self.assertTrue(r.json()['data'] != [], 'TapdHandler.get_bug_group_count() is not successd, the status_code is ' + str(r.status_code))

        r = self._tpad.get_custom_fields('bug')
        self.assertTrue(r.json()['data'] != [], 'TapdHandler.get_bug_custom_fields() is not successd, the status_code is ' + str(r.status_code))

    def test_task(self):
        # The tapd.api limit the number of requests in a certain period of time, so the sleep() should be added.
        time.sleep(6)
        _task_id = {'id': 1120990771001008719}

        r = self._tpad.get_data('task', **_task_id)
        self.assertTrue(int(r.json()['data']['Task']['id']) == _task_id['id'], 'TapdHandler.get_task() is not successd, the status_code is ' + str(r.status_code))

        r = self._tpad.get_count('task', **_task_id)
        self.assertTrue(r.json()['data'] != [], 'TapdHandler.get_task_count() is not successd, the status_code is ' + str(r.status_code))

        r = self._tpad.get_custom_fields('task')
        self.assertTrue(r.status_code == 200, 'TapdHandler.get_task_custom_fields() is not successd, the status_code is ' + str(r.status_code))


if __name__ == '__main__':
    unittest.main()