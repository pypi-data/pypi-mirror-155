# !/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from functools import partial
from taodata.util.dsl import BodyHelper
import json
import requests


class DataApi:

    __token = ''
    __http_url = 'http://210.22.185.58:7788/route'
    #__http_url = 'http://localhost:5000/route'

    def __init__(self, token, timeout=30):
        """
        Parameters
        ----------
        token: str
            API接口TOKEN，用于用户认证
        """
        self.__token = token
        self.__timeout = timeout

    # 得到专题列表
    # 参数
    def get_topics(self, **kwargs):
        req_params = {
            'action': 'get_topics',
            'token': self.__token,
            'params': kwargs,
        }
        res = requests.post(self.__http_url, json=req_params, timeout=self.__timeout)
        if res:
            result = json.loads(res.text)
            if result['code'] != 0:
                raise Exception(result['msg'])
            data = result['data']
            return data
        else:
            return None

    # 获取专题下采集任务列表
    # 参数
    # topic_id
    def get_tasks(self, **kwargs):
        req_params = {
            'action': 'get_tasks',
            'token': self.__token,
            'params': kwargs,
        }
        res = requests.post(self.__http_url, json=req_params, timeout=self.__timeout)
        if res:
            result = json.loads(res.text)
            if result['code'] != 0:
                raise Exception(result['msg'])
            data = result['data']
            return data
        else:
            return None

    # 获取专题数据字段
    # 参数
    # topic_id
    def get_topic_fields(self, **kwargs):
        req_params = {
            'action': 'get_topic_fields',
            'token': self.__token,
            'params': kwargs,
        }
        res = requests.post(self.__http_url, json=req_params, timeout=self.__timeout)
        if res:
            result = json.loads(res.text)
            if result['code'] != 0:
                raise Exception(result['msg'])
            data = result['data']
            return data
        else:
            return None

    # 获取专题数据
    # 参数
    # topic_id  专题标识 不能为空
    # fields 专题字段ID列表，可以为空
    # scroll 使用游标 True,False 可以为空
    # scroll_id 游标获取数据标记
    # size 每次返回数据数，默认1000, 不能超过10000
    def get_topic_data(self, **kwargs):
        req_params = {
            'action': 'get_topic_data',
            'token': self.__token,
            'params': kwargs,
        }
        res = requests.post(self.__http_url, json=req_params, timeout=self.__timeout)
        if res:
            result = json.loads(res.text)
            if result['code'] != 0:
                raise Exception(result['msg'])
            data = result['data']
            return data
        else:
            return None

    # 获取采集任务数据
    # 参数
    # task_id  采集任务标识 不能为空
    # fields 专题字段ID列表，可以为空
    # scroll 使用游标 True,False 可以为空
    # scroll_id 游标获取数据标记
    # size 每次返回数据数，默认1000, 不能超过10000
    def get_task_data(self, **kwargs):
        req_params = {
            'action': 'get_task_data',
            'token': self.__token,
            'params': kwargs,
        }
        res = requests.post(self.__http_url, json=req_params, timeout=self.__timeout)
        if res:
            result = json.loads(res.text)
            if result['code'] != 0:
                raise Exception(result['msg'])
            data = result['data']
            return data
        else:
            return None

