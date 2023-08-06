# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2020/7/23 16:33
:LastEditTime: 2020/7/23 16:33
:LastEditors: SunYiTan
:Description: Json帮助类
"""
import datetime
import decimal
import json


class JsonUtil:

    @staticmethod
    def dumps(obj):
        """
        :description: 对象 -> 字符串
        :param obj: 对象
        :return: 字符串
        :last_editors: SunYiTan
        """
        return json.dumps(obj, ensure_ascii=False, separators=(',', ':'), cls=MyJsonEncoder)


class MyJsonEncoder(json.JSONEncoder):
    """
    继承json.JSONEncoder

    使用方法:json.dumps(json_obj, ensure_ascii=False, cls=JsonEncoder)
    """

    def default(self, obj):  # pylint: disable=E0202
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, bytes):
            return obj.decode()
        elif isinstance(obj, decimal.Decimal):
            return str(decimal.Decimal(obj).quantize(decimal.Decimal('0.00')))
        else:
            # return json.JSONEncoder.default(self, obj)
            return obj.__dict__
