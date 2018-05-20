#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from config import Config as Cfg
from pwdcfg import PWDConfig
DEFAULT_WORKSPACE = {'workspace_id': Cfg.WORKSPACE_ID_Q6}


class BaseTapd(object):
    r"""
    This class will handel the method in the calss :class:`TapdHandler <TapdHandler>`.
    """
    def __init__(self):
        self._auth = (PWDConfig.API_USERNAME, PWDConfig.API_PWD)

    def _callback(self, prefix, name, workspace, **kwargs):
        method = getattr(self, prefix + name)
        if callable(method):
            kwargs.update(workspace)
            return method(**kwargs)

    def _query(self, url, workspace = DEFAULT_WORKSPACE, **kwargs):
        kwargs.update(workspace)
        r = requests.get(url, params = kwargs, auth = self._auth)
        return r

    def get_data(self, typename, workspace = DEFAULT_WORKSPACE, **query):
        return self._callback('_get_', typename, workspace, **query)

    def get_count(self, typename, workspace = DEFAULT_WORKSPACE, **query):
        return self._callback('_get_', typename + '_count', workspace, **query)

    def get_custom_fields(self, typename, workspace = DEFAULT_WORKSPACE, **query):
        return self._callback('_get_', typename + '_custom_fields', workspace, **query)

    def get_group_count(self, typename, workspace = DEFAULT_WORKSPACE, **query):
        return self._callback('_get_', typename + '_group_count', workspace, **query)

    def add_data(self, typename, workspace = DEFAULT_WORKSPACE, **query):
        return self._callback('_add_', typename, workspace, **query)


class TapdHandler(BaseTapd):
    """
    This handel program is used to handel the tapd.

    All of the methods in TapdHandler can be called by the funciton in class :class:`BaseTapd <BaseTapd>` like get_data(), get_count() .etc

    You can call the following funcitons to get the data from api.tapd.cn, and it will be returned the data like json:
    get_data(typename, workspace, **query)
    get_count(typename, workspace, **query)
    get_custom_fields(typename, workspace, **query)
    get_group_count(typename, workspace, **query)
    add_data(typename, workspace, **query)

    :param: typename: The type of tapd, you can use the parameter like: iteration, story, bug, task.
    :type: typename: string
    :param: workspace: The id of tapd's project(workspace), the dafault is {'workspace_id': '20990771'} (the id of workspaces named Q6)
    :type: workspace: dictionary
    :param: query: (optional) you can get the data form this query condition. You can get the query condition form: https://www.tapd.cn/help/view#1120003271001001250
    """

    def __init__(self):
        super(TapdHandler, self).__init__()
        self._url_iteration = Cfg.URL_GET_ITERATION
        self._url_iteration_count = Cfg.URL_GET_ITERATION_COUNT
        self._url_iteration_custom_fields = Cfg.URL_GET_ITERATION_CUSTOM_FIELDS

        self._url_story = Cfg.URL_GET_STORY
        self._url_story_count = Cfg.URL_GET_STORY_COUNT
        self._url_story_custom_fields = Cfg.URL_GET_STORY_CUSTOM_FIELDS

        self._url_bug = Cfg.URL_GET_BUG
        self._url_bug_count = Cfg.URL_GET_BUG_COUNT
        self._url_bug_group_count = Cfg.URL_GET_BUG_GROUP_COUNT
        self._url_bug_custom_fields = Cfg.URL_GET_BUG_CUSTOM_FIELDS
        self._url_add_bug = Cfg.URL_POST_ADD_BUG

        self._url_task = Cfg.URL_GET_TASK
        self._url_task_count = Cfg.URL_GET_TASK_COUNT
        self._url_task_custom_fields = Cfg.URL_GET_TASK_CUSTOM_FIELDS
        self._url_add_task = Cfg.URL_POST_ADD_TASK

    def _get_iteration(self, **query):
        return self._query(self._url_iteration, **query)

    def _get_iteration_count(self, **query):
        return self._query(self._url_iteration_count, **query)

    def _get_iteration_custom_fields(self, **query):
        return self._query(self._url_iteration_custom_fields, **query)

    def _get_story(self, **query):
        return self._query(self._url_story, **query)

    def _get_story_count(self, **query):
        return self._query(self._url_story_count, **query)

    def _get_story_custom_fields(self, **query):
        return self._query(self._url_story_custom_fields, **query)

    def _get_bug(self, **query):
        return self._query(self._url_bug, **query)

    def _get_bug_count(self, **query):
        return self._query(self._url_bug_count, **query)

    def _get_bug_group_count(self, **query):
        return self._query(self._url_bug_group_count, **query)

    def _get_bug_custom_fields(self, **query):
        return self._query(self._url_bug_custom_fields, **query)

    # todo: add tapd bug.
    def _add_bug(self):
        pass

    def _get_task(self, **query):
        return self._query(self._url_task, **query)

    def _get_task_count(self, **query):
        return self._query(self._url_task_count, **query)

    def _get_task_custom_fields(self, **query):
        return self._query(self._url_task_custom_fields, **query)

    # todo: add tapd task.
    def _add_task(self):
        pass