# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/5/21 15:17
:LastEditTime: 2021/5/21 15:17
:LastEditors: SunYiTan
:Description: 
"""
from seven_framework import TimeHelper

from seven_cmstar_platform.models.db_models.ezgame.ezgame_user_action_log_model import EzgameUserActionLogModel, EzgameUserActionLog
from seven_cmstar_platform.models.action_log_model import ActionInfoVO


class UserActionLogModelEx(EzgameUserActionLogModel):

    def __init__(self, db_connect_key='db_platform', sub_table=None, db_transaction=None, context=None):
        super().__init__(db_connect_key, sub_table, db_transaction, context)

    def write_log(self, user_id: int, action_info_vo: ActionInfoVO):
        action_log = EzgameUserActionLog()
        action_log.user_id = user_id
        action_log.action_id = action_info_vo.action_id
        action_log.doll_id = action_info_vo.doll_id
        action_log.parama = action_info_vo.parama
        action_log.paramb = action_info_vo.paramb
        action_log.paramc = action_info_vo.paramc
        action_log.paramd = action_info_vo.paramd
        action_log.create_date = TimeHelper.get_now_datetime()

        self.add_entity(action_log)
