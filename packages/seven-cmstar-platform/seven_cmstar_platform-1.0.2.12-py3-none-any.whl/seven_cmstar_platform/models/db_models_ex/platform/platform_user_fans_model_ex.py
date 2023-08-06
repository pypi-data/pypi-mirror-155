# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/10/12 18:07
:LastEditTime: 2021/10/12 18:07
:LastEditors: SunYiTan
:Description: 
"""
from seven_framework.base_model import *

from seven_cmstar_platform.models.cache_model import CacheModel
from seven_cmstar_platform.models.db_models.platform.platform_user_fans_model import PlatformUserFans
from seven_cmstar_platform.models.enum import RedisKeyType


class PlatformUserFansModelEx(CacheModel):
    __CACHE_KEY = RedisKeyType.PtUserFansCache.value

    def __init__(self, db_connect_key='db_platform', sub_table=None, db_transaction=None, context=None):
        super(PlatformUserFansModelEx, self).__init__(PlatformUserFans, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    @classmethod
    def get_dependency_key(self, user_id):
        return f"{self.__CACHE_KEY}:{user_id}"
