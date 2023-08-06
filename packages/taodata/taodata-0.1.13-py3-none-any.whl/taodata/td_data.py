# !/usr/bin/env python
# -*- coding: utf-8 -*-

from taodata.util import auth
from taodata.util import client


def get_api(token='', timeout=30):
    """
    初始化API,第一次可以通过td.set_token('your token')来记录自己的token凭证，临时token可以通过本参数传入
    """
    if token == '' or token is None:
        token = auth.get_token()
    if token is not None and token != '':
        api = client.DataApi(token=token, timeout=timeout)
        return api
    else:
        raise Exception('api init error.')



