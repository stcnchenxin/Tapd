#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from tapd_req.search import Iteration, Story, Bug, Task
import time


class TapdTestCase(unittest.TestCase):
    def test_iteration(self):
        iterObj = Iteration()
        r = iterObj.get_iteration()
        self.assertTrue(r.json()['data'] != [], 'Iteration.get_iteration() is not successd, the status_code is ' + str(r.status_code))

        r = iterObj.get_iteration_count()
        self.assertTrue(r.json()['data'] != [], 'Iteration.get_itera_count() is not successd, the status_code is ' + str(r.status_code))

        r = iterObj.get_iteration_custom_fields()
        self.assertTrue(r.status_code == 200, 'Iteration.get_iteration_custom_fields() is not successd, the status_code is ' + str(r.status_code))

    def test_story(self):
        storyObj = Story()
        r = storyObj.get_story()
        self.assertTrue(r.json()['data'] != [], 'Story.get_story() is not successd, the status_code is ' + str(r.status_code))

        r = storyObj.get_story_count()
        self.assertTrue(r.json()['data'] != [], 'Story.get_story_count() is not successd, the status_code is ' + str(r.status_code))

        r = storyObj.get_story_custom_fields()
        self.assertTrue(r.json()['data'] != [], 'Story.get_story_custom_fields() is not successd, the status_code is ' + str(r.status_code))

    def test_bug(self):
        bugObj = Bug()
        r = bugObj.get_bug()
        self.assertTrue(r.json()['data'] != [], 'Bug.get_bug() is not successd, the status_code is ' + str(r.status_code))

        r = bugObj.get_bug_count()
        self.assertTrue(r.json()['data'] != [], 'Bug.get_bug_count() is not successd, the status_code is ' + str(r.status_code))

        r = bugObj.get_bug_group_count()
        self.assertTrue(r.json()['data'] != [], 'Bug.get_bug_group_count() is not successd, the status_code is ' + str(r.status_code))

        r = bugObj.get_bug_custom_fields()
        self.assertTrue(r.json()['data'] != [], 'Bug.get_bug_custom_fields() is not successd, the status_code is ' + str(r.status_code))

    def test_task(self):
        taskObj = Task()
        r = taskObj.get_task()
        self.assertTrue(r.json()['data'] != [], 'Task.get_task() is not successd, the status_code is ' + str(r.status_code))

        r = taskObj.get_task_count()
        self.assertTrue(r.json()['data'] != [], 'Task.get_task_count() is not successd, the status_code is ' + str(r.status_code))

        # 因为tapd限制一定时间的请求次数，这里需要加下延时
        time.sleep(5)
        r = taskObj.get_task_custom_fields()
        self.assertTrue(r.status_code == 200, 'Task.get_task_custom_fields() is not successd, the status_code is ' + str(r.status_code))


if __name__ == '__main__':
    unittest.main()