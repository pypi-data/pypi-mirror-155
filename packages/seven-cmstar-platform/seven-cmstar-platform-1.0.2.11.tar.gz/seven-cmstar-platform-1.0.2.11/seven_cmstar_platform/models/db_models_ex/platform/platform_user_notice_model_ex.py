# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/10/29 16:35
:LastEditTime: 2021/10/29 16:35
:LastEditors: SunYiTan
:Description: 用户通知模块
"""
from seven_cmstar_platform.models.db_models.platform.platform_user_notice_model import PlatformUserNoticeModel
from seven_cmstar_platform.models.enum import UserNoticeNumType, RedisKeyType
from seven_cmstar_platform.utils.redis_util import RedisUtil


class PlatformUserNoticeModelEx(PlatformUserNoticeModel):

    def add_new_notice_num(self, user_id, notice_num_type: UserNoticeNumType, inc_value):
        """
        增加通知数量，用于小红点显示未读数量
        :param user_id:
        :param notice_num_type:
        :param inc_value:
        :return:
        """
        redis_cli = RedisUtil()
        name = f"{RedisKeyType.PtUserNotifyNum.value}:{user_id}"
        redis_cli.hincrby(name, notice_num_type, inc_value)

    def clear_new_notice_num(self, user_id, notice_num_type: UserNoticeNumType):
        """
        清空通知数量，点击查看后清空
        :param user_id:
        :param notice_num_type:
        :return:
        """
        redis_cli = RedisUtil()
        name = f"{RedisKeyType.PtUserNotifyNum.value}:{user_id}"
        redis_cli.hdel(name, notice_num_type)
