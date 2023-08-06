# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/4/26 16:10
:LastEditTime: 2021/4/26 16:10
:LastEditors: SunYiTan
:Description: QQ小游戏帮助类
"""
import json
import logging
import traceback
from io import BytesIO

import requests
from PIL import Image
from seven_framework import HTTPHelper, TimeHelper

from seven_cmstar_platform.models.enum import AppBaseRedisKeyType
from seven_cmstar_platform.utils.json_util import JsonUtil
from seven_cmstar_platform.utils.redis_util import RedisUtil


class QqMiniHelper:

    @classmethod
    def code_to_session(cls, code: str, app_id: str, app_secret: str):
        """
        QQ验证
        :param code:
        :param app_id:
        :param app_secret:
        :return:
        {
            'errcode': 0,
            'errmsg': '',
            'openid': 'E18DE2D9EE0EDA9CF889A8AF2708xxxx',
            'session_key': 'RzFjaXBDZUl6MTJxxxx',
            'uin': '',
            'unionid': 'UID_B98652A7C90F3C342E8FC4xxxx'
        }

        """
        url = f"https://api.q.qq.com/sns/jscode2session?appid={app_id}" \
              f"&secret={app_secret}&js_code={code}&grant_type=authorization_code"

        response = HTTPHelper.get(url)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return {"errcode": -1, "errmsg": "接口请求失败"}

    @classmethod
    def get_access_token(cls, app_id: str, app_secret: str):
        """
        获取AccessToken
        :param app_id:
        :param app_secret:
        :return:
        {
            'errcode': 0,
            'access_token': 'AkAKh4iV0RCi1LyXIhgvlRK8PUDEa_y_yj-fnu1xxxx',
            'expires_in': 7200
        }
        """
        url = f"https://api.q.qq.com/api/getToken?grant_type=client_credential&appid={app_id}&secret={app_secret}"

        response = HTTPHelper.get(url)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return {"errcode": -1, "errmsg": "接口请求失败"}

    @classmethod
    def get_access_token_cache(cls, app_id: str, app_secret: str):
        key = AppBaseRedisKeyType.QqAccessToken.value + app_id
        now = TimeHelper.get_now_timestamp()
        token = ""
        refresh_time = 0
        expires_in = 0

        s = RedisUtil().get(key)
        if s:
            token_info = json.loads(s)
            token = token_info["access_token"]
            refresh_time = token_info["refresh_time"]
            expires_in = token_info["expires_in"]

        if not s or now >= refresh_time + expires_in:
            token = cls.__refresh_access_token(app_id, app_secret)

        return token

    @classmethod
    def __refresh_access_token(cls, app_id: str, app_secret: str):
        lock_key = AppBaseRedisKeyType.QqAccessTokenLock.value + app_id
        redis_util = RedisUtil()
        lock_value = redis_util.acquire_lock_with_timeout(lock_key)
        if lock_value:
            try:
                key = AppBaseRedisKeyType.QqAccessToken.value + app_id
                now = TimeHelper.get_now_timestamp()
                token = ""
                refresh_time = 0
                expires_in = 0

                # 防止重复刷新
                s = RedisUtil().get(key)
                if s:
                    token_info = json.loads(s)
                    token = token_info["access_token"]
                    refresh_time = token_info["refresh_time"]
                    expires_in = token_info["expires_in"]
                if s and now < refresh_time + expires_in and now - refresh_time <= 10:
                    return token

                result = cls.get_access_token(app_id, app_secret)
                if result["errcode"] != 0:
                    logging.getLogger().error(f"get access token fail from qq: {result}")
                    return ""

                token_info = {
                    "access_token": result["access_token"],
                    "expires_in": result["expires_in"],
                    "refresh_time": now
                }

                RedisUtil().set(key, JsonUtil.dumps(token_info))
                return result["access_token"]

            except Exception as e:
                logging.getLogger().error(traceback.format_exc())

            finally:
                redis_util.release_lock(lock_key, lock_value)
        else:
            return ""

    @classmethod
    def msg_sec_check(cls, app_id: str, access_token: str, content: str):
        """
        检查一段文本是否含有违法违规内容
        参考地址：https://q.qq.com/wiki/develop/miniprogram/server/open_port/port_safe.html#security-msgseccheck
        :param app_id:
        :param access_token:
        :param content:
        :return:
        {'errCode': 0, 'errMsg': 'ok'}
        {'errCode': 87014, 'errMsg': 'risky content'}
        """
        url = "https://api.q.qq.com/api/json/security/MsgSecCheck"
        data = {
            "access_token": access_token,
            "appid": app_id,
            "content": content
        }
        headers = {'Content-Type': 'application/json'}

        response = HTTPHelper.post(url, data, headers)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return {"errCode": -1, "errmsg": "接口请求失败"}

    @classmethod
    def img_sec_check(cls, app_id: str, access_token: str, pic_url: str):
        """
        校验一张图片是否含有违法违规内容。（好像只能检查政治人物的图片，检查不了黄色图片）
        :param app_id:
        :param access_token:
        :param pic_url:
        :return:
        {'errCode': 0, 'errMsg': 'ok'}
        {'errCode': 87014, 'errMsg': 'risky content'}
        """
        r = requests.get(pic_url)

        tmpIm = BytesIO(r.content)
        im = Image.open(tmpIm)
        im_format = im.format.lower()
        file_name = f"{TimeHelper.get_now_timestamp(is_ms=True)}.{im_format}"
        file_format = f"image/{im_format}"

        url = f'https://api.q.qq.com/api/json/security/ImgSecCheck'
        data = {
            "access_token": access_token,
            "appid": app_id
        }
        files = {"media": (file_name, r.content, file_format)}

        response = requests.post(url=url, data=data, files=files)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return {"errCode": -1, "errmsg": "接口请求失败"}

    @classmethod
    def subscribe_message_send(cls, access_token, template_id, page_path, open_id, content):
        """
        发送订阅消息
        参考文档：https://q.qq.com/wiki/develop/miniprogram/server/open_port/port_subscribe.html
        :param access_token:
        :param mp_template_id:
        :param app_id:
        :param page_path:
        :param open_id:
        :param content:
        :return:
        """
        url = f"https://api.q.qq.com/api/json/subscribe/SendSubscriptionMessage?access_token={access_token}"

        data = {
            "touser": open_id,
            "template_id": template_id,
            "page": page_path,
            "data": content
        }

        response = HTTPHelper.post(url, data, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return {"errcode": -1, "errmsg": "接口请求失败"}
