# -*- coding:utf-8 -*-
"""
    规则引擎SDK引擎探针模块
    @Author: Ray Wong
    @Create: 2022-02-28
"""

from jy_iiot_ruler_sdk import core


class RulerEngineBase:
    """
        基础数据访问(煤矿列表，子系统列表)
    """

    def __init__(self, ak, sk, host='127.0.0.1', port=8888):
        self._core = core.RulerEngineCore(ak, sk, host, port)
        # 限定只能访问其用户授权的煤矿
        self.company_list = self._core.get_company_list()

    def get_company_list(self):
        req_url = 'http://%s:%s/api/platform/user/bind/list/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "username": self._core.AK,
        }
        return self._core.api(req_url, req_data)

    def get_biz_list(self):
        req_url = 'http://%s:%s/api/platform/biz/list/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "username": self._core.AK,
        }
        return self._core.api(req_url, req_data)
