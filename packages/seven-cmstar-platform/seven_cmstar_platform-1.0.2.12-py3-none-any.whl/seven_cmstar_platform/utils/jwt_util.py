# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2020/7/22 13:49
:LastEditTime: 2020/7/22 13:49
:LastEditors: SunYiTan
:Description: jwt认证工具类
"""
import jwt
import time


class JwtUtil:

    @staticmethod
    def create_token(sub_info: str, secret: str, expire: int):
        """
        生成token
        :param user_info:
        :param secret:
        :param expire: 过期时间，天
        :return:
        """
        if expire > 0:
            payload = {
                "iat": int(time.time()),
                "exp": int(time.time()) + 86400 * expire,
                "sub": sub_info
            }
        else:
            payload = {
                "iat": int(time.time()),
                "sub": sub_info
            }

        return jwt.encode(payload, secret, algorithm='HS256').decode()

    @staticmethod
    def get_sub_info_from_token(token, secret: str):
        """
        获取玩家Id
        :param token:
        :param secret:
        :return:
        """
        payload = jwt.decode(token, secret, algorithms='HS256')
        if payload:
            return payload.get("sub")
        else:
            return None
