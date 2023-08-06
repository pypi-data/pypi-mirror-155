# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/10/12 15:42
:LastEditTime: 2021/10/12 15:42
:LastEditors: SunYiTan
:Description: 
"""
from seven_framework.base_model import *

from seven_cmstar_platform.models.cache_model import CacheModel
from seven_cmstar_platform.models.db_models.platform.platform_user_follow_model import PlatformUserFollow
from seven_cmstar_platform.models.enum import RedisKeyType


class PlatformUserFollowModelEx(CacheModel):
    __CACHE_KEY = RedisKeyType.PtUserFollowCache.value

    def __init__(self, db_connect_key='db_platform', sub_table=None, db_transaction=None, context=None):
        super(PlatformUserFollowModelEx, self).__init__(PlatformUserFollow, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    @classmethod
    def get_dependency_key(self, user_id):
        return f"{self.__CACHE_KEY}:{user_id}"
