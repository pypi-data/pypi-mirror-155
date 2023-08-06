# -*- coding:utf-8 -*-
"""
    规则引擎SDK设备模型模块
    @Author: Ray Wong
    @Create: 2022-02-28
"""

from jy_iiot_ruler_sdk import core


class RulerEngineDevice:
    """
        设备模型访问(物理设备,虚拟设备)
    """

    def __init__(self, ak, sk, host='127.0.0.1', port=8000):
        self._core = core.RulerEngineCore(ak, sk, host, port)
        # 限定只能访问其用户授权的煤矿
        self.company_list = self._core.get_company_list()

    def get_device_info(self, company, biz):
        """
            获取设备列表
        """
        if company not in self.company_list.keys():
            return None, None
        req_url = 'http://%s:%s/api/platform/device/base/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "company": company,
            "biz": biz
        }
        return self._core.api(req_url, req_data)

    def get_tag_info(self, company, biz, device):
        """
            get_device_info方法的扩展,可以直接访问到测点
        """
        if company not in self.company_list.keys():
            return None, None
        req_url = 'http://%s:%s/api/platform/device/tag/base/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "company": company,
            "biz": biz,
            "device": device
        }
        return self._core.api(req_url, req_data)

    def get_vdevice_info(self, company):
        """
            获取虚拟设备点表
        """
        if company not in self.company_list.keys():
            return None, None
        req_url = 'http://%s:%s/api/platform/vDevice/list/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "company": company,
        }
        return self._core.api(req_url, req_data)

    def get_vtag_info(self, company, device):
        """
            get_vdevice_info方法的扩展,可以直接访问到虚拟测点
        """
        if company not in self.company_list.keys():
            return None, None
        req_url = 'http://%s:%s/api/platform/vDevice/vTag/list/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "company": company,
            "device": device
        }
        return self._core.api(req_url, req_data)

    def set_vdevice_info(self, company, device, key, value):
        """
            允许规则引擎重写虚拟设备信息
        """
        if company not in self.company_list.keys():
            return None, None
        req_url = 'http://%s:%s/api/platform/vDevice/device/attr/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "company": company,
            "device": device,
            "key": key,
            "value": value
        }
        return self._core.api(req_url, req_data)

    def set_vtag_info(self, company, device, tag, key, value):
        """
            允许规则引擎重写虚拟测点信息
        """
        if company not in self.company_list.keys():
            return None, None
        req_url = 'http://%s:%s/api/platform/vDevice/tag/attr/' % (self._core.HOST, self._core.PORT)
        req_data = {
            "company": company,
            "device": device,
            "tag": tag,
            "key": key,
            "value": value
        }
        return self._core.api(req_url, req_data)

