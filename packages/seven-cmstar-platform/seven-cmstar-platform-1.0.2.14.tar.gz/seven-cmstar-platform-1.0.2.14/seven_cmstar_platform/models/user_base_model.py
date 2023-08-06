# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/6/18 12:33
:LastEditTime: 2021/6/18 12:33
:LastEditors: SunYiTan
:Description: 
"""


class UserTokenParam:
    """
    user_token参数
    """

    def __init__(self):
        self.user_id = 0  # 平台用户ID
        self.third_auth_id = 0  # 第三方验证唯一id
        self.app_channel = 0  # 登录APP渠道标识，0：NoSdk 1：QQ小程序 2：微信小程序，3：iOS应用，4：安卓应用
        self.user_type = 0  # 用户类型，0：C端用户，1：B端用户
        self.version = 0  # 版本号

    @classmethod
    def dict_2_entity(cls, dict_info):
        obj = cls()
        for (k, v) in dict_info.items():
            if getattr(obj, k, None) is not None:
                setattr(obj, k, v)
        return obj


class UserBaseInfo:
    """
    用户基本信息
    """

    def __init__(self):
        self.user_id = 0  # 用户唯一id
        self.user_nick = ""  # 用户昵称
        self.avatar = ""  # 用户头像
        self.channel = 0  # 登录APP渠道标识，0：NoSdk 1：QQ小程序 2：微信小程序，3：iOS应用，4：安卓应用
        self.app_id = ""  # 第三方app_id
        self.open_id = ""  # open_id
