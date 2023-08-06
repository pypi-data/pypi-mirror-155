# -*- coding:utf-8 -*-
"""
    精英物联网数据服务平台规则引擎轻代码开发SDK
    @Author: Ray Wong
    @Create: 2022-02-28
    @CopyRight: 精英数智科技股份有限公司
"""
# 适配平台版本
__platform_version__ = '1.2.0'
# SDK版本
__version__ = '0.0.3'

def descript():
    return '''
        精英物联网数据服务平台规则引擎轻代码开发SDK
    '''

# 获取版本信息
def get_version():
    return dict(name="jy_iiot_ruler_sdk", runtime="python 3.9", version=__version__,
                platform_version=__platform_version__)
