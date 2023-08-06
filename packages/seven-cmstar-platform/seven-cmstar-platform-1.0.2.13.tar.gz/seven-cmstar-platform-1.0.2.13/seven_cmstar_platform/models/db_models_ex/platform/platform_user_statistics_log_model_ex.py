# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/5/21 15:17
:LastEditTime: 2021/5/21 15:17
:LastEditors: SunYiTan
:Description: 用户统计日志表
"""
import decimal
import json

from seven_framework import TimeHelper

from seven_cmstar_platform.models.db_models.platform.platform_user_statistics_log_model import \
    PlatformUserStatisticsLogModel, PlatformUserStatisticsLog
from seven_cmstar_platform.models.enum import StatisticsOrmType, RedisKeyType
from seven_cmstar_platform.utils.json_util import JsonUtil
from seven_cmstar_platform.utils.redis_util import RedisUtil


class UserStatisticsLogModelEx(PlatformUserStatisticsLogModel):

    def __init__(self, db_connect_key='db_platform', sub_table=None, db_transaction=None, context=None):
        super().__init__(db_connect_key, sub_table, db_transaction, context)

    def add_log(self, user_id: int, third_auth_id: int, orm_id: int, inc_value):
        """
        添加记录
        :param user_id:
        :param third_auth_id
        :param orm_id:
        :param inc_value:
        :return:
        """
        now_date = TimeHelper.get_now_datetime()
        now_day = int(TimeHelper.datetime_to_format_time(now_date, "%Y%m%d"))
        now_hour = int(TimeHelper.datetime_to_format_time(now_date, "%Y%m%d%H"))

        statistics_log = self.get_entity(where="user_id=%s AND auth_id=%s AND orm_id=%s AND create_hour=%s",
                                         params=[user_id, third_auth_id, orm_id, now_hour])

        if statistics_log:
            self.update_table(update_sql="inc_value=inc_value+%s", where="id=%s",
                              params=[decimal.Decimal(inc_value), statistics_log.id])
        else:
            statistics_log = PlatformUserStatisticsLog()
            statistics_log.user_id = user_id
            statistics_log.auth_id = third_auth_id
            statistics_log.orm_id = orm_id
            statistics_log.inc_value = inc_value
            statistics_log.create_hour = now_hour
            statistics_log.create_day = now_day
            statistics_log.create_date = now_date

            self.add_entity(statistics_log)

    def record_remain_time(self, user_id):
        """
        统计用户留存时间
        :param user_id:
        :return:
        """
        now_time = TimeHelper.get_now_timestamp()
        key = f"{RedisKeyType.PtUserRemainTime.value}:{user_id}"

        result = RedisUtil().get(key)
        if not result:
            record_dict = {
                "record_time": now_time,
                "remain_time": 0
            }
            RedisUtil().set(key, JsonUtil.dumps(record_dict), 24 * 60 * 60)
            return

        record_dict = json.loads(result)
        if now_time - record_dict["record_time"] > 60:
            # 两协议间请求时间超过1分钟，重新开始统计
            remain_time = record_dict["remain_time"]
            record_dict = {
                "record_time": now_time,
                "remain_time": 0
            }
            RedisUtil().set(key, JsonUtil.dumps(record_dict), 24 * 60 * 60)

            if remain_time > 0:
                # 统计数据，记录之前累计的时间
                self.add_log(user_id, 0, StatisticsOrmType.RemainTime.value, remain_time)
        else:
            # 两协议间请求时间不超过1分钟，累计停留时间
            record_dict["remain_time"] += now_time - record_dict["record_time"]
            record_dict["record_time"] = now_time

            remain_time = record_dict["remain_time"]
            if remain_time >= 60:
                # 累计时间超过1分钟，记录时间，重新开始统计
                record_dict = {
                    "record_time": now_time,
                    "remain_time": 0
                }

                # 统计数据
                self.add_log(user_id, 0, StatisticsOrmType.RemainTime.value, remain_time)

            RedisUtil().set(key, JsonUtil.dumps(record_dict), 24 * 60 * 60)
