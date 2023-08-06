# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/8/11 09:51
:LastEditTime: 2021/8/11 09:51
:LastEditors: SunYiTan
:Description: 微信小游戏帮助类
"""
import base64
import json
import logging
import traceback

from Crypto.Cipher import AES
from seven_framework import HTTPHelper, TimeHelper

from seven_cmstar_platform.models.enum import AppBaseRedisKeyType
from seven_cmstar_platform.utils.json_util import JsonUtil
from seven_cmstar_platform.utils.redis_util import RedisUtil


class WxMiniHelper:

    @classmethod
    def code_to_session(cls, code: str, app_id: str, app_secret: str):
        """
        微信验证
        :param code:
        :param app_id:
        :param app_secret:
        :return:
        {"session_key":"oKR7CraC4X0aR6xxxx","openid":"oHUq14ilDpKbS4NQpxxxx"}

        """
        url = f"https://api.weixin.qq.com/sns/jscode2session?appid={app_id}" \
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
        参考文档：https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/access-token/auth.getAccessToken.html
        :param app_id:
        :param app_secret:
        :return:
        {
            'access_token': '49_XDvBlBxRCMEUmpH_W1BHTSuQf4oxxx',
            'expires_in': 7200
        }
        """
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"

        response = HTTPHelper.get(url)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return {"errcode": -1, "errmsg": "接口请求失败"}

    @classmethod
    def get_access_token_cache(cls, app_id: str, app_secret: str):
        key = AppBaseRedisKeyType.WxAccessToken.value + app_id
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
        lock_key = AppBaseRedisKeyType.WxAccessTokenLock.value + app_id
        redis_util = RedisUtil()
        lock_value = redis_util.acquire_lock_with_timeout(lock_key)
        if lock_value:
            try:
                key = AppBaseRedisKeyType.WxAccessToken.value + app_id
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
                if result.__contains__("errcode") and result["errcode"] != 0:
                    logging.getLogger().error(f"get access token fail from weixin: {result}")
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
    def decrypt_data(self, app_id, session_key, encrypted_data, iv):
        """
        :description:解析加密数据
        :param app_id: 微信小程序标识
        :param session_key: session_key调用登录接口获得
        :param encrypted_data：加密数据,微信返回加密参数
        :param iv：微信返回参数
        :return: 解密后的数据，用户信息或者手机号信息
        :last_editors: HuangJianYi
        """
        data = {}
        try:
            wx_data_crypt = WXBizDataCrypt(app_id, session_key)
            data = wx_data_crypt.decrypt(encrypted_data, iv)  # data中是解密的信息
        except Exception as ex:
            logging.getLogger("log_error").error(str(ex) + "【微信decrypted_data】")
        return data

    @classmethod
    def generate_scheme(cls, access_token, path, query, env_version):
        """
        获取小程序 scheme 码，适用于短信、邮件、外部网页、微信内等拉起小程序的业务场景
        参考文档：https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/url-scheme/urlscheme.generate.html
        :param access_token:
        :param path:
        :param query:
        :param env_version: 要打开的小程序版本。正式版为"release"，体验版为"trial"，开发版为"develop"
        {'errcode': 0, 'errmsg': 'ok', 'openlink': 'weixin://dl/business/?t=yRF6MvAltgb'}
        """
        url = f"https://api.weixin.qq.com/wxa/generatescheme?access_token={access_token}"

        data = {
            "jump_wxa":
                {
                    "path": path,
                    "query": query,
                    "env_version": env_version
                },
            "is_expire": True,
            "expire_time": TimeHelper.get_now_timestamp() + 7 * 24 * 60 * 60
        }
        response = HTTPHelper.post(url, data, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return {"errcode": -1, "errmsg": "接口请求失败"}

    @classmethod
    def generate_url_link(cls, access_token, path, query, env_version):
        """
        获取小程序 URL Link，适用于短信、邮件、网页、微信内等拉起小程序的业务场景
        参考文档：https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/url-link/urllink.generate.html
        :param access_token:
        :param path:
        :param query:
        :param env_version: 要打开的小程序版本。正式版为"release"，体验版为"trial"，开发版为"develop"
        {'errcode': 0, 'errmsg': 'ok', 'url_link': 'https://wxaurl.cn/MMdNDf6qiUt'}
        """
        url = f"https://api.weixin.qq.com/wxa/generate_urllink?access_token={access_token}"

        data = {
            "path": path,
            "query": query,
            "env_version": env_version,
            "is_expire": True,
            "expire_time": TimeHelper.get_now_timestamp() + 7 * 24 * 60 * 60
        }

        response = HTTPHelper.post(url, data, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return {"errcode": -1, "errmsg": "接口请求失败"}

    @classmethod
    def mp_subscribe_message_send(cls, access_token, mp_template_id, app_id, page_path, open_id, content):
        """
        发送公众号订阅消息
        参考文档：https://developers.weixin.qq.com/doc/offiaccount/Subscription_Messages/api.html#send%E5%8F%91%E9%80%81%E8%AE%A2%E9%98%85%E9%80%9A%E7%9F%A5
        :param access_token:
        :param mp_template_id:
        :param app_id:
        :param page_path:
        :param open_id:
        :param content:
        :return:
        """
        url = f"https://api.weixin.qq.com/cgi-bin/message/subscribe/bizsend?access_token={access_token}"

        data = {
            "touser": open_id,
            "template_id": mp_template_id,
            "page": "",
            "miniprogram": {
                "appid": app_id,
                "pagepath": page_path
            },
            "data": content
        }

        response = HTTPHelper.post(url, data, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return {"errcode": -1, "errmsg": "接口请求失败"}

    @classmethod
    def uniform_message_send(cls, access_token, mp_appid, mp_template_id, app_id, page_path, open_id, content):
        """
        下发小程序和公众号统一的服务消息
        参考文档：https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/uniform-message/uniformMessage.send.html
        :param access_token:
        :param mp_appid:
        :param mp_template_id:
        :param app_id:
        :param page_path:
        :param open_id:
        :param content:
        :return:
        """
        url = f"https://api.weixin.qq.com/cgi-bin/message/wxopen/template/uniform_send?access_token={access_token}"

        data = {
            "touser": open_id,
            "mp_template_msg": {
                "appid": mp_appid,
                "template_id": mp_template_id,
                "url": "",
                "miniprogram": {
                    "appid": app_id,
                    "pagepath": page_path
                },
                "data": content
            }
        }

        response = HTTPHelper.post(url, data, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return {"errcode": -1, "errmsg": "接口请求失败"}


class WXBizDataCrypt:
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]
