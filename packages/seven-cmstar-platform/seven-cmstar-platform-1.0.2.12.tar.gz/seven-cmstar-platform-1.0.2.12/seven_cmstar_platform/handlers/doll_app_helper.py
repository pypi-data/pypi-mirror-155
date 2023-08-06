# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/10/29 17:22
:LastEditTime: 2021/10/29 17:22
:LastEditors: SunYiTan
:Description: 娃娃平台帮助类
"""
from seven_cmstar_platform.models.db_models_ex.platform.platform_user_notice_model_ex import PlatformUserNoticeModelEx
from seven_cmstar_platform.models.enum import UserNoticeNumType


class DollAppHelper:

    @staticmethod
    def add_new_notice_num(user_id, notice_num_type: UserNoticeNumType, inc_value):
        """
        增加通知数量，用于小红点显示未读数量
        :param user_id:
        :param notice_num_type:
        :param inc_value:
        :return:
        """
        PlatformUserNoticeModelEx().add_new_notice_num(user_id, notice_num_type, inc_value)

    @staticmethod
    def clear_new_notice_num(user_id, notice_num_type: UserNoticeNumType):
        """
        清空通知数量，点击查看后清空
        :param user_id:
        :param notice_num_type:
        :return:
        """
        PlatformUserNoticeModelEx().clear_new_notice_num(user_id, notice_num_type)
