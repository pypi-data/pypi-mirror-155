# -*- coding:utf-8 -*-
"""
    规则引擎SDK核心模块
    @Author: Ray Wong
    @Create: 2022-02-28
"""
import hashlib
import json

import requests
from requests.auth import HTTPBasicAuth


class RulerEngineCore:
    """
        规则引擎SDK核心类
        说明: 这个类应当是一个内部方法类,正常情况下开发规则引擎是不需要调用的
    """

    # 例如：ak:006070021，sk:Jyiot@0021
    def __init__(self, ak, sk, host='127.0.0.1', port=8000):
        self.AK = ak
        self.SK = sk
        self.HOST = host
        self.PORT = port
        self._ak = ''
        if self.AK != '' and self.AK is not None:
            self._ak = self.AK
        self._sk = ''
        if self.SK != '' and self.SK is not None:
            self._sk = hashlib.md5(self.SK.encode(encoding='UTF-8')).hexdigest()

    def api(self, url, body):
        """
            平台接口访问对象
        """
        try:
            data_resp = requests.post(url, json.dumps(body),
                                      auth=HTTPBasicAuth("sad78d0as", "df6bdc4027bf7a2fc8ad51cc1c4a60b6"))
        except BaseException as e:
            return None, e
        if data_resp.status_code != 200:
            return data_resp, BaseException("平台url访问错误")
        try:
            json_res = json.loads(data_resp.text)
        except BaseException as e:
            return None, e
        return json_res["data"], None

    def get_company_list(self):
        """
            根据AK获取可访问授权的煤矿列表(字典 code:name)
        """
        res = dict()
        req_url = 'http://%s:%s/api/platform/user/bind/list/' % (self.HOST, self.PORT)
        req_data = {
            "username": self.AK,
        }
        resp, err = self.api(req_url, req_data)
        if err is not None:
            return dict(), err
        for item in resp:
            res.update({item["username"]: item["company_name"]})
        return res
