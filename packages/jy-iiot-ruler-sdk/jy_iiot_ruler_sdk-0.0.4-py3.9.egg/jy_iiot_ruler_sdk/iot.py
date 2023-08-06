# -*- coding:utf-8 -*-
"""
    规则引擎SDK动态数据模块
    @Author: Ray Wong
    @Create: 2022-02-28
"""

from jy_iiot_ruler_sdk import core


class RulerEngineIOT:
    """
        动态数据访问
    """

    def __init__(self, ak, sk, host='127.0.0.1', port=8000):
        self._core = core.RulerEngineCore(ak, sk, host, port)
        # 限定只能访问其用户授权的煤矿
        self.company_list = self._core.get_company_list()

    def get_tag_real(self, company, biz, device):
        """
            获取测点实时数据
        """
        if company not in self.company_list.keys():
            return None, None
        req_url = 'http://%s:%s/api/platform/device/tag/real/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "company": company,
            "device": device,
            "biz": biz
        }
        return self._core.api(req_url, req_data)

    def get_tag_history(self, company, biz, year, device, tag, start_time, end_time):
        """
            获取测点历史数据列表
        """
        if company not in self.company_list.keys():
            return None, None
        req_url = 'http://%s:%s/api/platform/device/history/tend/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "company": company,
            "biz": biz,
            "year": year,
            "device": device,
            "tag": tag,
            "start_time": start_time,
            "end_time": end_time
        }
        return self._core.api(req_url, req_data)

    def get_channel_data(self, company, biz, year, channel_type, start_time, end_time):
        """
            获取非标通道数据(平台内的)
        """
        if company not in self.company_list.keys():
            return None, None
        req_url = 'http://%s:%s/api/platform/channel/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "company": company,
            "biz": biz,
            "year": year,
            "channel_type": channel_type,
            "start_time": start_time,
            "end_time": end_time
        }
        return self._core.api(req_url, req_data)

    def get_platform_alarm_real(self, company, biz):
        """
            获取平台实时报警
        """
        if company not in self.company_list.keys():
            return None, None
        req_url = 'http://%s:%s/api/platform/alarm/real/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "company": company,
            "biz": biz,
        }
        return self._core.api(req_url, req_data)

    def get_platform_alarm_history(self, company, biz, year, device, tag, start_time, end_time):
        """
            获取平台历史报警
        """
        if company not in self.company_list.keys():
            return None, None
        req_url = 'http://%s:%s/api/platform/alarm/his/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "company": company,
            "biz": biz,
            "year": year,
            "device": device,
            "tag": tag,
            "start_time": start_time,
            "end_time": end_time
        }
        return self._core.api(req_url, req_data)

    def get_raw_alarm_history(self, company, biz, year, device, tag, start_time, end_time):
        """
            获取原始历史报警
        """
        if company not in self.company_list.keys():
            return None, None
        req_url = 'http://%s:%s/api/platform/alarm/raw' % (self._core.HOST, self._core.PORT)
        req_data = {
            "company": company,
            "biz": biz,
            "year": year,
            "device": device,
            "tag": tag,
            "start_time": start_time,
            "end_time": end_time
        }
        return self._core.api(req_url, req_data)

    def get_link_alarm(self, company, biz, year, start_time, end_time):
        """
            获取断线报警
        """
        if company not in self.company_list.keys():
            return None, None
        req_url = 'http://%s:%s/api/platform/alarm/link' % (self._core.HOST, self._core.PORT)
        req_data = {
            "company": company,
            "biz": biz,
            "year": year,
            "start_time": start_time,
            "end_time": end_time
        }
        return self._core.api(req_url, req_data)

    def set_vtag_value(self, company, device, tag, value):
        """
            虚拟测点赋值
            同时写入mongo,tsdb
        """
        if company not in self.company_list.keys():
            return None, None
        req_url = 'http://%s:%s/api/platform/vDevice/tag/value/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "company": company,
            "device": device,
            "tag": tag,
            "value": value
        }
        return self._core.api(req_url, req_data)

    def get_vtag_real(self, company, device, tag):
        """
            虚拟测点实时数据
        """
        if company not in self.company_list.keys():
            return None, None
        req_url = 'http://%s:%s/api/platform/vDevice/vTag/list/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "company": company,
            "device": device,
            "search_query": tag
        }
        return self._core.api(req_url, req_data)

    def get_vtag_history(self, company, year, device, tag, start_time, end_time):
        """
            虚拟测点历史数据
        """
        if company not in self.company_list.keys():
            return None, None
        req_url = 'http://%s:%s/api/platform/device/history/tend/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "company": company,
            "biz": "virtual",
            "year": year,
            "device": device,
            "tag": tag,
            "start_time": start_time,
            "end_time": end_time
        }
        return self._core.api(req_url, req_data)
