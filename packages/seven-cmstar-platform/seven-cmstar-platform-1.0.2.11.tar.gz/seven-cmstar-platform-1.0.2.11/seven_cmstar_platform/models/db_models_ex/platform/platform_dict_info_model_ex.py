# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/11/15 15:38
:LastEditTime: 2021/11/15 15:38
:LastEditors: SunYiTan
:Description: 
"""
from seven_framework import MySQLHelper, config

from seven_cmstar_platform.models.cache_model import CacheModel
from seven_cmstar_platform.models.db_models.platform.platform_dict_info_model import PlatformDictInfo
from seven_cmstar_platform.models.enum import RedisKeyType


class PlatformDictInfoModelEx(CacheModel):
    __CACHE_KEY = RedisKeyType.PtDictInfo.value

    def __init__(self, db_connect_key='db_platform', sub_table=None, db_transaction=None, context=None):
        super(PlatformDictInfoModelEx, self).__init__(PlatformDictInfo, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    @classmethod
    def get_dependency_key(self):
        return f"{self.__CACHE_KEY}"

    def get_dict_value(self, dict_id):
        """
        获取字典的值
        :param dict_id:
        :return:
        """
        dict_info = self.get_cache_dict(dependency_key=self.get_dependency_key(),
                                        where="dict_id=%s", params=[dict_id])
        if dict_info:
            return dict_info["dict_value"]
        else:
            return ""

    def get_dict_text(self, dict_id):
        """
        获取字典的值
        :param dict_id:
        :return:
        """
        dict_info = self.get_cache_dict(dependency_key=self.get_dependency_key(),
                                        where="dict_id=%s", params=[dict_id])
        if dict_info:
            return dict_info["dict_text"]
        else:
            return ""
