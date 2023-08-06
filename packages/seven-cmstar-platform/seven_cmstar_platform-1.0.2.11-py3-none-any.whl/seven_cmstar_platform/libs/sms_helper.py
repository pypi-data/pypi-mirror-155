# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/5/14 17:01
:LastEditTime: 2021/5/14 17:01
:LastEditors: SunYiTan
:Description: 发放短信
"""
import logging

import baidubce.services.sms.sms_client as sms
import baidubce.exception as ex
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration


class SmsHelper:

    def __init__(self, ak, sk, host):
        self.ak = ak
        self.sk = sk
        self.host = host

    def send_message(self, telephone: str, sms_sign, template_id, content_var_dict):
        """
        发送端口，百度云短信接口：https://cloud.baidu.com/doc/SMS/s/3kipnj5wy
        :param telephone: 手机号，多个手机号之间以英文逗号分隔，一次请求最多支持200个手机号
        :param code: 验证码
        :return:
        """
        try:
            sms_client = sms.SmsClient(BceClientConfiguration(credentials=BceCredentials(self.ak, self.sk),
                                                              endpoint=self.host))
            response = sms_client.send_message(signature_id=sms_sign,
                                               template_id=template_id,
                                               mobile=telephone,
                                               content_var_dict=content_var_dict)
            # print(JsonUtil.dumps(response))

            if response.code == "1000":
                return True
            else:
                logging.getLogger("log_error").error(f"send sms fail, code: {response.code}, msg: {response.message}")
                return False

        except ex.BceHttpClientError as e:
            if isinstance(e.last_error, ex.BceServerError):
                logging.getLogger("log_error").error('send sms failed. Response %s, code: %s, request_id: %s'
                                                     % (e.last_error.status_code, e.last_error.code,
                                                        e.last_error.request_id))
            else:
                logging.getLogger("log_error").error('send sms failed. Unknown exception: %s' % e)
            return False

        except Exception as e:
            logging.getLogger("log_error").error('send sms failed. Unknown exception: %s' % e)
            return False
