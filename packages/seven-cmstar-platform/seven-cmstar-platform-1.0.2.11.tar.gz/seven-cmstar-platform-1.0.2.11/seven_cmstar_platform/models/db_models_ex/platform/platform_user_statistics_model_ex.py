# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/10/27 09:33
:LastEditTime: 2021/10/27 09:33
:LastEditors: SunYiTan
:Description: 
"""
from seven_framework import TimeHelper

from seven_cmstar_platform.models.db_models.platform.platform_user_statistics_model import PlatformUserStatisticsModel, \
    PlatformUserStatistics
from seven_cmstar_platform.models.enum import UserStatisticsType


class UserStatisticsModelEx(PlatformUserStatisticsModel):

    def add_value(self, user_id: int, statistics_type: UserStatisticsType, add_value):
        """
        增加用户统计信息
        :param user_id:
        :param statistics_type:
        :param add_value:
        :return:
        """
        now_date = TimeHelper.get_now_datetime()

        statistics_info = self.get_dict(where="user_id=%s", params=[user_id])

        if statistics_info:
            if statistics_type == UserStatisticsType.DollNum.value:
                update_sql = "doll_num=doll_num+%s"
            elif statistics_type == UserStatisticsType.ClothNum.value:
                update_sql = "cloth_num=cloth_num+%s"
            elif statistics_type == UserStatisticsType.PostNum.value:
                update_sql = "post_num=post_num+%s"
            elif statistics_type == UserStatisticsType.CommentNum.value:
                update_sql = "comment_num=comment_num+%s"
            elif statistics_type == UserStatisticsType.ApplyNum.value:
                update_sql = "apply_num=apply_num+%s"
            elif statistics_type == UserStatisticsType.QuotationNum.value:
                update_sql = "quotation_num=quotation_num+%s"
            elif statistics_type == UserStatisticsType.OrderNum.value:
                update_sql = "order_num=order_num+%s"
            else:
                return
            self.update_table(update_sql=update_sql, where="user_id=%s",
                              params=[add_value, user_id])

        else:
            statistics_info = PlatformUserStatistics()
            statistics_info.user_id = user_id
            statistics_info.create_date = now_date
            statistics_info.modify_date = now_date

            if statistics_type == UserStatisticsType.DollNum.value:
                statistics_info.doll_num = add_value
            elif statistics_type == UserStatisticsType.ClothNum.value:
                statistics_info.cloth_num = add_value
            elif statistics_type == UserStatisticsType.PostNum.value:
                statistics_info.post_num = add_value
            elif statistics_type == UserStatisticsType.CommentNum.value:
                statistics_info.comment_num = add_value
            elif statistics_type == UserStatisticsType.ApplyNum.value:
                statistics_info.apply_num = add_value
            elif statistics_type == UserStatisticsType.QuotationNum.value:
                statistics_info.quotation_num = add_value
            elif statistics_type == UserStatisticsType.OrderNum.value:
                statistics_info.order_num = add_value
            else:
                return

            self.add_entity(statistics_info)
