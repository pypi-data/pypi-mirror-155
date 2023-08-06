# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/11/11 18:40
:LastEditTime: 2021/11/11 18:40
:LastEditors: SunYiTan
:Description: 
"""
import decimal

from seven_framework import TimeHelper, CryptoHelper, MySQLHelper, config

from seven_cmstar_platform.models.cache_model import CacheModel
from seven_cmstar_platform.models.db_models.platform.platform_search_statistics_log_model import \
    PlatformSearchStatisticsLog
from seven_cmstar_platform.models.enum import RedisKeyType


class SearchStatisticsLogModelEx(CacheModel):
    __CACHE_KEY = RedisKeyType.PtSearchStatisticsLog.value

    def __init__(self, db_connect_key='db_platform', sub_table=None, db_transaction=None, context=None):
        super(SearchStatisticsLogModelEx, self).__init__(PlatformSearchStatisticsLog, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    @classmethod
    def get_dependency_key(self):
        return f"{self.__CACHE_KEY}"

    def add_log(self, keyword, inc_value):
        """
        添加记录
        :param keyword:
        :param inc_value:
        :return:
        """
        if not keyword:
            return

        keyword_id = CryptoHelper.md5_encrypt_int(keyword)
        now_date = TimeHelper.get_now_datetime()
        now_day = int(TimeHelper.datetime_to_format_time(now_date, "%Y%m%d"))

        statistics_log = self.get_entity(where="keyword_id=%s AND create_day=%s",
                                         params=[keyword_id, now_day])

        if statistics_log:
            self.update_table(update_sql="inc_value=inc_value+%s", where="id=%s",
                              params=[decimal.Decimal(inc_value), statistics_log.id])
        else:
            statistics_log = PlatformSearchStatisticsLog()
            statistics_log.keyword_id = keyword_id
            statistics_log.keyword = keyword
            statistics_log.inc_value = inc_value
            statistics_log.create_day = now_day
            statistics_log.create_date = now_date

            self.add_entity(statistics_log)
