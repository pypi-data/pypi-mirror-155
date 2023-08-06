# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/9/27 14:03
:LastEditTime: 2021/9/27 14:03
:LastEditors: SunYiTan
:Description: 小程序帮助类
"""
import json
import logging
import sys

from seven_framework import config, HTTPHelper

from seven_cmstar_platform.handlers.qqmini_helper import QqMiniHelper
from seven_cmstar_platform.handlers.wxmini_helper import WxMiniHelper


class AppHelper:

    @classmethod
    def get_qq_access_token(cls, app_id):
        """
        获取qq access_token
        :param app_id:
        :return:
        """
        qq_mini_list = config.get_value("qq_mini")
        app_secret = ""
        for qq_info in qq_mini_list:
            if qq_info["app_id"] == app_id:
                app_secret = qq_info["app_secret"]
                break
        if not app_secret:
            logging.getLogger("log_error").error(f"获取QQ小程序信息失败，app_id: {app_id}")
            return True, ""

        access_token = None
        if "--production" in sys.argv:
            # 正式服
            access_token = QqMiniHelper.get_access_token_cache(app_id, app_secret)
        else:
            # 本地或测试服，请求正式服
            url = f"https://dollapps.idspub.com/platform/qq_access_token?app_id={app_id}" \
                  f"&app_secret={app_secret}"

            response = HTTPHelper.get(url)
            if response.status_code == 200:
                result = json.loads(response.text)
                if result["result"] == "0":
                    access_token = result["data"]

        return access_token

    @classmethod
    def get_wx_access_token(cls, app_id):
        """
        获取微信access_token
        :param app_id:
        :return:
        """
        qq_mini_list = config.get_value("wx_mini")
        app_secret = ""
        for qq_info in qq_mini_list:
            if qq_info["app_id"] == app_id:
                app_secret = qq_info["app_secret"]
                break
        if not app_secret:
            logging.getLogger("log_error").error(f"获取微信小程序信息失败，app_id: {app_id}")
            return ""

        access_token = None
        if "--production" in sys.argv:
            # 正式服
            access_token = WxMiniHelper.get_access_token_cache(app_id, app_secret)
        else:
            # 本地或测试服，请求正式服
            url = f"https://dollapps.idspub.com/platform/wx_access_token?app_id={app_id}" \
                  f"&app_secret={app_secret}"

            response = HTTPHelper.get(url)
            if response.status_code == 200:
                result = json.loads(response.text)
                if result["result"] == "0":
                    access_token = result["data"]

        return access_token

    @classmethod
    def get_wx_link_url(cl, app_id, path, query, env_version):
        """
        获取微信链接
        :param app_id:
        :param path:
        :param query:
        :param env_version: 要打开的小程序版本。正式版为"release"，体验版为"trial"，开发版为"develop"
        :return:
        """
        # 获取 access_token
        access_token = AppHelper.get_wx_access_token(app_id)
        if not access_token:
            logging.getLogger("log_error").error(f"get wx access token fail, app_id: {app_id}")
            return ""

        res = WxMiniHelper.generate_url_link(access_token, path, query, env_version)
        if res["errcode"] != 0:
            logging.getLogger("log_error").error(f"get wx url link fail, res: {res}")
            return ""

        return res["url_link"]

        # # 获取 scheme 码
        # res = WxMiniHelper.generate_scheme(access_token, path, query, env_version)
        # if res["errcode"] != 0:
        #     logging.getLogger("log_error").error(f"get wx scheme url fail, res: {res}")
        #     return ""
        #
        # # 长链接转成短链接
        # open_link = res["openlink"]
        # long_link = f"https://dollapps.idspub.com/redirect_scheme?t=gao7.com&scheme={CodingHelper.url_encode(open_link)}"
        # res = SevenHelper.long2short(long_link)
        # if res["ResultCode"] != "0":
        #     logging.getLogger("log_error").error(f"long2short fail, res: {res}")
        #     return ""
        #
        # wx_link_url = ""
        # for temp in res["Data"]:
        #     wx_link_url = temp["ShortUrl"]
        #
        # return wx_link_url

    @classmethod
    def qq_subscribe_message_send(cls, app_id, template_id, page_path, open_id, content):
        """
        发送订阅消息，qq
        :param app_id:
        :param template_id:
        :param page_path:
        :param open_id:
        :param content:
        :return:
        """
        # 获取 access_token
        access_token = cls.get_qq_access_token(app_id)
        if not access_token:
            logging.getLogger("log_error").error(f"get qq access token fail, app_id: {app_id}")
            return {"errcode": -1, "errmsg": "获取 access_token 失败"}

        return QqMiniHelper.subscribe_message_send(access_token, template_id, page_path, open_id, content)

    @classmethod
    def wx_uniform_message_send(cls, mp_appid, mp_template_id, app_id, page_path, open_id, content):
        """
        下发小程序和公众号统一的服务消息，微信
        :param mp_appid:
        :param mp_template_id:
        :param app_id:
        :param page_path:
        :param open_id:
        :param content:
        :return:
        """
        # 获取 access_token
        access_token = AppHelper.get_wx_access_token(app_id)
        if not access_token:
            logging.getLogger("log_error").error(f"get wx access token fail, app_id: {app_id}")
            return {"errcode": -1, "errmsg": "获取 access_token 失败"}

        return WxMiniHelper.uniform_message_send(access_token, mp_appid, mp_template_id, app_id, page_path, open_id,
                                                 content)
