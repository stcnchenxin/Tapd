#!/usr/bin/env python
# -*- coding: utf-8 -*-
import count
import config

if __name__ == '__main__':
    count.write_story_adnormal_data(u'2018.06.29维护', ('id', 'name', 'owner'), 'test.xls', u'甘芳琳;')
    count.write_task(u'2018.05.18维护', config.TapdSearchContent.TASK_FILTER_LIST, config.TapdSearchContent.TASK_OWNER_Q6_QC, 'test.xls', {u'甘芳琳;': 2, u'邹祖业;': 2, u'赖增涛;': 2, u'肖兴亮;': 2})
