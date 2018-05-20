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
        r = self._tpad.get_data('iteration')
        self.assertTrue(r.json()['data'] != [], 'TapdHandler.get_iteration() is not successd, the status_code is ' + str(r.status_code))

        r = self._tpad.get_count('iteration')
        self.assertTrue(r.json()['data'] != [], 'TapdHandler.get_itera_count() is not successd, the status_code is ' + str(r.status_code))

        r = self._tpad.get_custom_fields('iteration')
        self.assertTrue(r.status_code == 200, 'TapdHandler.get_iteration_custom_fields() is not successd, the status_code is ' + str(r.status_code))

    def test_story(self):
        r = self._tpad.get_data('story')
        self.assertTrue(r.json()['data'] != [], 'TapdHandler.get_story() is not successd, the status_code is ' + str(r.status_code))

        r = self._tpad.get_count('story')
        self.assertTrue(r.json()['data'] != [], 'TapdHandler.get_story_count() is not successd, the status_code is ' + str(r.status_code))

        r = self._tpad.get_custom_fields('story')
        self.assertTrue(r.json()['data'] != [], 'TapdHandler.get_story_custom_fields() is not successd, the status_code is ' + str(r.status_code))

    def test_bug(self):
        r = self._tpad.get_data('bug')
        self.assertTrue(r.json()['data'] != [], 'TapdHandler.get_bug() is not successd, the status_code is ' + str(r.status_code))

        r = self._tpad.get_count('bug')
        self.assertTrue(r.json()['data'] != [], 'TapdHandler.get_bug_count() is not successd, the status_code is ' + str(r.status_code))

        r = self._tpad.get_group_count('bug')
        self.assertTrue(r.json()['data'] != [], 'TapdHandler.get_bug_group_count() is not successd, the status_code is ' + str(r.status_code))

        r = self._tpad.get_custom_fields('bug')
        self.assertTrue(r.json()['data'] != [], 'TapdHandler.get_bug_custom_fields() is not successd, the status_code is ' + str(r.status_code))

    def test_task(self):
        r = self._tpad.get_data('task')
        self.assertTrue(r.json()['data'] != [], 'TapdHandler.get_task() is not successd, the status_code is ' + str(r.status_code))

        r = self._tpad.get_count('task')
        self.assertTrue(r.json()['data'] != [], 'TapdHandler.get_task_count() is not successd, the status_code is ' + str(r.status_code))

        # The tapd.api limit the number of requests in a certain period of time, so the sleep() should be added.
        time.sleep(6)
        r = self._tpad.get_custom_fields('task')
        self.assertTrue(r.status_code == 200, 'TapdHandler.get_task_custom_fields() is not successd, the status_code is ' + str(r.status_code))


if __name__ == '__main__':
    unittest.main()