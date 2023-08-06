# -*- coding:utf-8 -*-
"""
    规则引擎SDK引擎探针模块
    @Author: Ray Wong
    @Create: 2022-02-28
"""

from jy_iiot_ruler_sdk import core


class RulerEngineProbe:
    """
        规则引擎探针
        规则在编写时应当符合规定要求,不然无法监测规则执行情况
    """

    def __init__(self, ak, sk, host='127.0.0.1', port=8888):
        self._core = core.RulerEngineCore(ak, sk, host, port)
        # 限定只能访问其用户授权的煤矿
        self.company_list = self._core.get_company_list()

    def set_ruler_stat(self, code, stat):
        """
            设置探针状态:
                主要是反馈脚本执行过程中是否异常,当执行完成后反馈脚本执行是否成功
        """
        req_url = 'http://%s:%s/api/platform/probe/stat/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "code": code,
            "stat": stat
        }
        return self._core.api(req_url, req_data)

    def ruler_log(self, code, level, message):
        """
            执行过程的日志
            level: panic,fatal,error,warning,info,debug,trace
        """
        req_url = 'http://%s:%s/api/platform/probe/log/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "code": code,
            "level": level,
            "stat": message
        }
        return self._core.api(req_url, req_data)
