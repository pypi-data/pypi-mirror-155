# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/12/27 09:58
:LastEditTime: 2021/12/27 09:58
:LastEditors: SunYiTan
:Description: 
"""
from seven_cmstar_platform.models.enum import AppBaseRedisKeyType
from seven_cmstar_platform.utils.redis_util import RedisUtil
from seven_framework import UUIDHelper


class InviteModel():
    __USER_TOKEN_KEY = AppBaseRedisKeyType.InviteUserToken.value
    __TOKEN_USER_KEY = AppBaseRedisKeyType.InviteTokenUser.value

    @classmethod
    def __get_user_token(cls, user_id: int) -> str:
        """
        获取玩家token信息
        :param user_id:
        :return:
        """
        key1 = f"{cls.__USER_TOKEN_KEY}:{user_id}"
        return RedisUtil().get(key1)

    @classmethod
    def __update_user_token(cls, user_id: int, token: str):
        """
        更新玩家token信息
        :param user_id:
        :param token:
        :return:
        """
        key1 = f"{cls.__USER_TOKEN_KEY}:{user_id}"
        key2 = f"{cls.__TOKEN_USER_KEY}:{token}"
        RedisUtil().set(key1, token, 604800)  # 7天
        RedisUtil().set(key2, str(user_id), 604800)

    @classmethod
    def __get_user_id_by_token(cls, token: str):
        key2 = f"{cls.__TOKEN_USER_KEY}:{token}"
        s = RedisUtil().get(key2)
        if s:
            return int(s)
        else:
            return None

    @classmethod
    def get_invite_token(cls, user_id):
        """
        获取玩家邀请码
        :param user_id:
        :return:
        """
        token = cls.__get_user_token(user_id)
        if not token:
            token = UUIDHelper.get_uuid()

        cls.__update_user_token(user_id, token)
        return token

    @classmethod
    def get_user_id_by_token(cls, invite_token: str):
        """
        通过邀请码获取玩家id
        :param invite_token:
        :return:
        """
        if not invite_token:
            return None

        user_id = cls.__get_user_id_by_token(invite_token)
        return user_id
