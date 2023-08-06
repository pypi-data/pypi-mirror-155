# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/12/15 18:31
:LastEditTime: 2021/12/15 18:31
:LastEditors: SunYiTan
:Description: 
"""
from seven_cmstar_platform.models.asset_base_model import AssetBaseModel


class PlatformHelper:

    @classmethod
    def get_user_integral(cls, user_id):
        """
        获取用户积分
        :param user_id: 用户唯一id
        :return: 用户当前积分
        """
        return AssetBaseModel().get_user_integral(user_id)

    @classmethod
    def update_user_integral(cls, user_id, asset_value,
                             source_type, source_object_id, source_object_name, log_title,
                             module_id=0, only_id="",
                             info_json=None):
        """
        :description: 变更用户积分
        :param user_id：用户唯一id
        :param asset_value：修改资产值
        :param source_type：来源类型（1-购买2-任务3-手动配置4-抽奖5-回购）
        :param source_object_id：来源对象标识(比如来源类型是任务则对应任务类型)
        :param source_object_name：来源对象名称(比如来源类型是任务则对应任务名称)
        :param log_title：资产流水标题
        :param module_id：模块标识，没有填0
        :param only_id:唯一标识(用于并发操作时校验避免重复操作)由业务方定义传入
        :param info_json：资产流水详情，用于存放业务方自定义字典
        :return: 返回实体InvokeResultData
        :last_editors: SunYiTan
        """
        return AssetBaseModel().update_user_integral(
            user_id, asset_value,
            source_type, source_object_id, source_object_name, log_title, module_id, only_id, info_json)