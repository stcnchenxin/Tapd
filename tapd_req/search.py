#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from config import Config as Cfg
from pwdcfg import PWDConfig
DEFAULT_WORKSPACE = {'workspace_id':Cfg.WORKSPACE_ID_Q6}


class BaseTapd(object):
    def __init__(self):
        self._auth = (PWDConfig.API_USERNAME, PWDConfig.API_PWD)

    def __call__(self, url, **kwargs):
        r = requests.get(url, params = kwargs, auth = self._auth)
        return r

    def get_data(self, url, **kwargs):
        r = requests.get(url, params = kwargs, auth = self._auth)
        return r

    def get_query(self, workspace, **query):
        query.update(workspace)
        return query


class Iteration(BaseTapd):
    def __init__(self):
        super(Iteration, self).__init__()
        self._url_iteration = Cfg.URL_GET_ITERATION
        self._url_iteration_count = Cfg.URL_GET_ITERATION_COUNT
        self._url_iteration_custom_fields = Cfg.URL_GET_ITERATION_CUSTOM_FIELDS

    def get_iteration(self, workspace = DEFAULT_WORKSPACE, **query):
        query.update(workspace)
        return self.get_data(self._url_iteration, **query)

    def get_iteration_count(self, workspace = DEFAULT_WORKSPACE, **query):
        query.update(workspace)
        return self.get_data(self._url_iteration_count, **query)

    def get_iteration_custom_fields(self, workspace = DEFAULT_WORKSPACE):
        return self.get_data(self._url_iteration_custom_fields, **workspace)


class Story(BaseTapd):
    def __init__(self):
        super(Story, self).__init__()
        self._url_story = Cfg.URL_GET_STORY
        self._url_story_count = Cfg.URL_GET_STORY_COUNT
        self._url_story_custom_fields = Cfg.URL_GET_STORY_CUSTOM_FIELDS

    def get_story(self, workspace = DEFAULT_WORKSPACE, **query):
        query.update(workspace)
        return self.get_data(self._url_story, **query)

    def get_story_count(self, workspace = DEFAULT_WORKSPACE, **query):
        query.update(workspace)
        return self.get_data(self._url_story_count, **query)

    def get_story_custom_fields(self, workspace = DEFAULT_WORKSPACE):
        return self.get_data(self._url_story_custom_fields, **workspace)


class Bug(BaseTapd):
    def __init__(self):
        super(Bug, self).__init__()
        self._url_bug = Cfg.URL_GET_BUG
        self._url_bug_count = Cfg.URL_GET_BUG_COUNT
        self._url_bug_group_count = Cfg.URL_GET_BUG_GROUP_COUNT
        self._url_bug_custom_fields = Cfg.URL_GET_BUG_CUSTOM_FIELDS

    def get_bug(self, workspace = DEFAULT_WORKSPACE, **query):
        query.update(workspace)
        return self.get_data(self._url_bug, **query)

    def get_bug_count(self, workspace = DEFAULT_WORKSPACE, **query):
        query.update(workspace)
        return self.get_data(self._url_bug_count, **query)

    def get_bug_group_count(self, workspace = DEFAULT_WORKSPACE, **query):
        query.update(workspace)
        return self.get_data(self._url_bug_group_count, **query)

    def get_bug_custom_fields(self, workspace = DEFAULT_WORKSPACE):
        return self.get_data(self._url_bug_custom_fields, **workspace)

    # 新建缺陷，暂时先不写
    def add_bug(self):
        pass


class Task(BaseTapd):
    def __init__(self):
        super(Task, self).__init__()
        self._url_task = Cfg.URL_GET_TASK
        self._url_task_count = Cfg.URL_GET_TASK_COUNT
        self._url_task_custom_fields = Cfg.URL_GET_TASK_CUSTOM_FIELDS

    def get_task(self, workspace = DEFAULT_WORKSPACE, **query):
        query.update(workspace)
        return self.get_data(self._url_task, **query)

    def get_task_count(self, workspace = DEFAULT_WORKSPACE, **query):
        query.update(workspace)
        return self.get_data(self._url_task_count, **query)

    def get_task_custom_fields(self, workspace = DEFAULT_WORKSPACE):
        return self.get_data(self._url_task_custom_fields, **workspace)

    # 新建任务，暂时先不写
    def add_task(self):
        pass





