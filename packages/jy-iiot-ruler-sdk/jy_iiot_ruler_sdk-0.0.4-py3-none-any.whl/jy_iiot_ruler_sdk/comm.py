# -*- coding:utf-8 -*-
"""
    规则引擎SDK通信模块
    @Author: Ray Wong
    @Create: 2022-02-28
"""

from jy_iiot_ruler_sdk import core


class RulerEngineComm:
    """
        通信模块(对外公共通信模块)
        为用户提供mongo,redis,kafka
    """
    def __init__(self, ak, sk, host='127.0.0.1', port=8000):
        self._core = core.RulerEngineCore(ak, sk, host, port)

    def set_cached(self, key, value):
        # 第20个redis给规则引擎用
        req_url = 'http://%s:%s/api/platform/comm/redis/set/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "key": key,
            "value": value
        }
        return self._core.api(req_url, req_data)

    def get_cached(self, key):
        req_url = 'http://%s:%s/api/platform/comm/redis/get/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "key": key
        }
        return self._core.api(req_url, req_data)

    def set_persist(self, table, value):
        # JY-IIOT的t_engine给规则引擎用
        req_url = 'http://%s:%s/api/platform/comm/mongo/set/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "table": table,
            "value": value
        }
        return self._core.api(req_url, req_data)

    def get_persist(self, table):
        req_url = 'http://%s:%s/api/platform/comm/mongo/get/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "table": table
        }
        return self._core.api(req_url, req_data)

    def pull_local_mq(self, topic, message, key):
        # 自己的kafka
        req_url = 'http://%s:%s/api/platform/comm/localKafka' % (self._core.HOST, self._core.PORT)
        req_data = {
            "topic": topic,
            "message": message,
            "key": key
        }
        return self._core.api(req_url, req_data)

    def pull_remote_mq(self, topic, message, key, host, username, password):
        # 用户的kafka
        req_url = 'http://%s:%s/api/platform/comm/remoteKafka' % (self._core.HOST, self._core.PORT)
        req_data = {
            "topic": topic,
            "message": message,
            "key": key,
            "host": host,
            "username": username,
            "password": password
        }
        return self._core.api(req_url, req_data)
