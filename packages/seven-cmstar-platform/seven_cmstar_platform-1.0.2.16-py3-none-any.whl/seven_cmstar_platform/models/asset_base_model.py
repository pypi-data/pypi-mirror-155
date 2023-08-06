# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2020-05-12 20:11:48
@LastEditTime: 2021-09-06 19:34:41
@LastEditors: HuangJianYi
:description:
"""
import logging
import traceback

from seven_framework import CryptoHelper, DbTransaction, config, TimeHelper

from seven_cmstar_platform.models.db_models.platform.platform_asset_inventory_model import PlatformAssetInventoryModel, \
    PlatformAssetInventory
from seven_cmstar_platform.models.db_models.platform.platform_asset_log_model import PlatformAssetLogModel, \
    PlatformAssetLog
from seven_cmstar_platform.models.db_models.platform.platform_asset_only_model import PlatformAssetOnlyModel, \
    PlatformAssetOnly
from seven_cmstar_platform.models.db_models.platform.platform_asset_warn_notice_model import \
    PlatformAssetWarnNoticeModel
from seven_cmstar_platform.models.db_models.platform.platform_user_asset_model import PlatformUserAssetModel, \
    PlatformUserAsset
from seven_cmstar_platform.models.db_models.platform.platform_user_info_model import PlatformUserInfoModel
from seven_cmstar_platform.models.enum import AssetType
from seven_cmstar_platform.models.seven_model import InvokeResultData
from seven_cmstar_platform.utils.json_util import JsonUtil
from seven_cmstar_platform.utils.redis_util import RedisUtil
from seven_cmstar_platform.utils.seven import SevenHelper


class AssetBaseModel():
    __APPID = "1508258827228050"  # 随机16位数字

    def __init__(self, context=None):
        self.context = context

    def _get_user_asset_id_md5(self, act_id, user_id, asset_type, asset_object_id):
        """
        :description: 生成用户资产唯一标识
        :param act_id：活动标识
        :param user_id：用户标识
        :param asset_type：资产类型(1-次数2-积分3-价格档位)
        :param asset_object_id：对象标识
        :return: 用户资产唯一标识
        :last_editors: HuangJianYi
        """
        if not act_id or not user_id or not asset_type:
            return 0
        return CryptoHelper.md5_encrypt_int(f"{act_id}_{user_id}_{asset_type}_{asset_object_id}")

    def _get_asset_check_code(self, id_md5, asset_value, sign_key):
        """
        :description: 生成用户资产校验码
        :param 用户资产唯一标识
        :param id_md5：id_md5
        :param asset_value：当前资产值
        :param sign_key：签名key,目前使用app_id作为签名key
        :return: 用户资产校验码
        :last_editors: HuangJianYi
        """
        if not id_md5 or not asset_value:
            return ""
        return CryptoHelper.md5_encrypt(f"{id_md5}_{int(asset_value)}", sign_key)

    def _add_onlyid_warn_stat(self, handler_name):
        """
        :description: 添加唯一标识预警拦截计数
        :param handler_name：接口名称
        :return:
        :last_editors: HuangJianYi
        """
        if handler_name:
            handler_name = str(handler_name).lower()
            redis_util = RedisUtil()

            hash_name_1 = f"warn_handler_list_{str(SevenHelper.get_now_int(fmt='%Y%m%d'))}"
            hash_key_1 = f"handlername_{handler_name}"
            if not redis_util.hexists(hash_name_1, hash_key_1):
                redis_util.hset(hash_name_1, hash_key_1,
                                JsonUtil.dumps({"app_id": '', "handler_name": handler_name}))
                redis_util.expire(hash_name_1, 24 * 3600)

            hash_name_2 = f"{hash_name_1}:{hash_key_1}"
            redis_util.hincrby(hash_name_2, str(SevenHelper.get_now_int(fmt='%Y%m%d%H%M')), 1)
            redis_util.expire(hash_name_2, 24 * 3600)

    def update_user_asset(self, app_id, act_id, module_id, user_id, open_id, user_nick, asset_type, asset_value,
                          asset_object_id, source_type, source_object_id, source_object_name, log_title, only_id="",
                          handler_name="", request_code="", info_json=None):
        """
        :description: 变更资产
        :param act_id：活动标识
        :param module_id：模块标识，没有填0
        :param user_id：用户标识
        :param open_id：open_id
        :param user_nick：昵称
        :param asset_type：资产类型(1-次数2-积分3-价格档位)
        :param asset_value：修改资产值
        :param asset_object_id：资产对象标识
        :param source_type：来源类型（1-购买2-任务3-手动配置4-抽奖5-回购）
        :param source_object_id：来源对象标识(比如来源类型是任务则对应任务类型)
        :param source_object_name：来源对象名称(比如来源类型是任务则对应任务名称)
        :param log_title：资产流水标题
        :param only_id:唯一标识(用于并发操作时校验避免重复操作)由业务方定义传入
        :param handler_name:接口名称
        :param request_code:请求唯一标识，从seven_framework框架获取对应request_code
        :param info_json：资产流水详情，用于存放业务方自定义字典
        :return: 返回实体InvokeResultData
        :last_editors: HuangJianYi
        """
        if info_json is None:
            info_json = {}

        invoke_result_data = InvokeResultData()

        if not act_id or not user_id or not asset_type or not asset_value:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "参数不能为空或等于0"
            return invoke_result_data

        if int(asset_type) == 3 and not asset_object_id:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "资产类型为价格档位,参数asset_object_id不能为空或等于0"
            return invoke_result_data

        user_asset_id_md5 = self._get_user_asset_id_md5(act_id, user_id, asset_type, asset_object_id)
        if user_asset_id_md5 == 0:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "修改失败"
            return invoke_result_data

        # 如果only_id已经存在，直接在redis进行拦截,减少数据库的请求，时限1天
        redis_util = RedisUtil()
        only_cache_key = ""
        if only_id:
            only_cache_key = f"asset_only_list:{act_id}_{SevenHelper.get_now_day_int()}"
            if redis_util.hexists(only_cache_key, only_id):
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "only_id已经存在"
                # 添加唯一标识预警拦截计数,用于控制台跑数据进行并发预警
                self._add_onlyid_warn_stat(handler_name)
                return invoke_result_data

        db_transaction = DbTransaction(db_config_dict=config.get_value("db_platform"))
        user_asset_model = PlatformUserAssetModel(db_transaction=db_transaction)
        asset_log_model = PlatformAssetLogModel(db_transaction=db_transaction)
        asset_only_model = PlatformAssetOnlyModel(db_transaction=db_transaction)
        asset_inventory_model = PlatformAssetInventoryModel(db_transaction=db_transaction)

        lock_key = f"userasset:{user_asset_id_md5}"
        lock_value = redis_util.acquire_lock_with_timeout(lock_key)
        if lock_value:
            try:
                now_day_int = SevenHelper.get_now_day_int()
                now_datetime = SevenHelper.get_now_datetime()
                old_user_asset_id = 0
                history_asset_value = 0

                user_asset = user_asset_model.get_entity("id_md5=%s", params=[user_asset_id_md5])
                if user_asset:
                    if user_asset.asset_value + asset_value < 0:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "no_enough"
                        invoke_result_data.error_message = "变更后的资产不能为负数"
                        return invoke_result_data

                    old_user_asset_id = user_asset.id
                    history_asset_value = user_asset.asset_value
                else:
                    user_asset = PlatformUserAsset()
                    user_asset.id_md5 = user_asset_id_md5
                    user_asset.app_id = app_id
                    user_asset.act_id = act_id
                    user_asset.user_id = user_id
                    user_asset.open_id = open_id
                    user_asset.user_nick = user_nick
                    user_asset.asset_type = asset_type
                    user_asset.asset_object_id = asset_object_id
                    user_asset.create_date = now_datetime

                user_asset.asset_value += asset_value
                user_asset.asset_check_code = self._get_asset_check_code(user_asset_id_md5, user_asset.asset_value,
                                                                         app_id)
                user_asset.modify_date = now_datetime

                old_asset_inventory_id = 0
                asset_inventory_id_md5 = CryptoHelper.md5_encrypt_int(
                    f"{act_id}_{user_id}_{asset_type}_{asset_object_id}_{now_day_int}")
                asset_inventory = asset_inventory_model.get_entity("id_md5=%s", params=[asset_inventory_id_md5])
                asset_inventory_update_sql = f"process_count=0,now_value={user_asset.asset_value}"
                if asset_inventory:
                    old_asset_inventory_id = asset_inventory.id
                    if asset_value > 0:
                        asset_inventory_update_sql += f",inc_value=inc_value+{asset_value}"
                    else:
                        asset_inventory_update_sql += f",dec_value=dec_value+{asset_value}"
                else:
                    asset_inventory = PlatformAssetInventory()
                    asset_inventory.id_md5 = asset_inventory_id_md5
                    asset_inventory.app_id = app_id
                    asset_inventory.act_id = act_id
                    asset_inventory.user_id = user_id
                    asset_inventory.open_id = open_id
                    asset_inventory.user_nick = user_nick
                    asset_inventory.asset_type = asset_type
                    asset_inventory.asset_object_id = asset_object_id
                    if asset_value > 0:
                        asset_inventory.inc_value += asset_value
                    else:
                        asset_inventory.dec_value += asset_value
                    asset_inventory.history_value = history_asset_value
                    asset_inventory.now_value = user_asset.asset_value
                    asset_inventory.create_date = now_datetime
                    asset_inventory.create_day = now_day_int

                asset_log = PlatformAssetLog()
                asset_log.app_id = app_id
                asset_log.act_id = act_id
                asset_log.module_id = module_id
                asset_log.user_id = user_id
                asset_log.open_id = open_id
                asset_log.user_nick = user_nick
                asset_log.log_title = log_title
                asset_log.info_json = info_json if not info_json else {}
                asset_log.asset_type = asset_type
                asset_log.asset_object_id = asset_object_id
                asset_log.source_type = source_type
                asset_log.source_object_id = source_object_id
                asset_log.source_object_name = source_object_name
                asset_log.only_id = only_id
                asset_log.operate_type = 0 if asset_value > 0 else 1
                asset_log.operate_value = asset_value
                asset_log.history_value = history_asset_value
                asset_log.now_value = user_asset.asset_value
                asset_log.handler_name = handler_name
                asset_log.request_code = request_code
                asset_log.create_date = now_datetime
                asset_log.create_day = now_day_int

                if only_id:
                    asset_only = PlatformAssetOnly()
                    asset_only.id_md5 = CryptoHelper.md5_encrypt_int(f"{act_id}_{user_id}_{only_id}")
                    asset_only.app_id = app_id
                    asset_only.act_id = act_id
                    asset_only.user_id = user_id
                    asset_only.open_id = open_id
                    asset_only.only_id = only_id
                    asset_only.create_date = now_datetime

                # 数据库，事务开始
                db_transaction.begin_transaction()

                if old_user_asset_id != 0:
                    user_asset_model.update_entity(user_asset, "asset_value,asset_check_code,modify_date")
                else:
                    user_asset_model.add_entity(user_asset)
                if old_asset_inventory_id != 0:
                    asset_inventory_model.update_table(asset_inventory_update_sql, "id=%s",
                                                       params=[old_asset_inventory_id])
                else:
                    asset_inventory_model.add_entity(asset_inventory)
                if only_id:
                    asset_only_model.add_entity(asset_only)

                asset_log_model.add_entity(asset_log)

                # 数据库，事务提交
                result = db_transaction.commit_transaction()
                if not result:
                    if only_id:
                        # 添加唯一标识预警拦截计数,用于控制台跑数据进行并发预警
                        self._add_onlyid_warn_stat(handler_name)

                    invoke_result_data.success = False
                    invoke_result_data.error_code = "fail"
                    invoke_result_data.error_message = "系统繁忙,请稍后再试"
                    return invoke_result_data

                if only_id:
                    redis_util.hset(only_cache_key, only_id, 1)
                    redis_util.expire(only_cache_key, 24 * 3600)

                invoke_result_data.data = user_asset.asset_value

            except Exception as ex:
                if self.context:
                    self.context.logging_link_error("【变更资产】" + str(ex))
                else:
                    logging.getLogger("log_error").error("【变更资产】" + str(ex))

                if db_transaction.is_transaction == True:
                    # 数据库，事务回滚
                    db_transaction.rollback_transaction()

                invoke_result_data.success = False
                invoke_result_data.error_code = "exception"
                invoke_result_data.error_message = "系统繁忙,请稍后再试"
                return invoke_result_data
            finally:
                redis_util.release_lock(lock_key, lock_value)
        else:
            invoke_result_data.success = False
            invoke_result_data.error_code = "acquire_lock"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
            return invoke_result_data

        return invoke_result_data

    def get_user_asset_list(self, app_id, act_id, user_ids, asset_type=0):
        """
        :description: 获取用户资产列表
        :param app_id：应用标识
        :param act_id：活动标识
        :param user_ids：用户标识 多个逗号,分隔
        :param asset_type：资产类型(1-次数2-积分3-价格档位)
        :return: 返回list
        :last_editors: HuangJianYi
        """
        if not act_id or not user_ids:
            return []
        condition = "act_id=%s"
        params = [act_id]
        if asset_type > 0:
            condition += " AND asset_type=%s"
            params.append(asset_type)
        if user_ids:
            if ',' in str(user_ids):
                condition += f" AND user_id in ({user_ids})"
            elif isinstance(user_ids, list):
                condition += " AND" + SevenHelper.get_condition_by_id_list("user_id", user_ids)
            else:
                condition += " AND user_id=%s"
                params.append(user_ids)
        user_asset_model = PlatformUserAssetModel()
        user_asset_dict_list = user_asset_model.get_dict_list(condition, params=params)
        if len(user_asset_dict_list) > 0:
            for user_asset_dict in user_asset_dict_list:
                if user_asset_dict["app_id"] != str(app_id):
                    user_asset_dict["asset_value"] = 0
                if self._get_asset_check_code(user_asset_dict["id_md5"], user_asset_dict["asset_value"], app_id) != \
                        user_asset_dict["asset_check_code"]:
                    user_asset_dict["asset_value"] = 0
        return user_asset_dict_list

    def get_user_asset(self, app_id, act_id, user_id, asset_type, asset_object_id):
        """
        :description: 获取具体的用户资产
        :param app_id：应用标识
        :param act_id：活动标识
        :param user_id：用户标识
        :param asset_type：资产类型(1-次数2-积分3-价格档位)
        :param asset_object_id：资产对象标识,没有传空
        :return: 返回list
        :last_editors: HuangJianYi
        """
        if not act_id or not user_id or not asset_type:
            return None
        user_asset_model = PlatformUserAssetModel()
        user_asset_id_md5 = self._get_user_asset_id_md5(act_id, user_id, asset_type, asset_object_id)
        user_asset_dict = user_asset_model.get_dict("id_md5=%s", params=[user_asset_id_md5])
        if user_asset_dict:
            if user_asset_dict["app_id"] != str(app_id):
                user_asset_dict["asset_value"] = 0
            if self._get_asset_check_code(user_asset_dict["id_md5"], user_asset_dict["asset_value"], app_id) != \
                    user_asset_dict["asset_check_code"]:
                user_asset_dict["asset_value"] = 0
        return user_asset_dict

    def get_asset_log_list(self, app_id, act_id, asset_type, page_size=20, page_index=0, user_id=0, asset_object_id="",
                           start_date="", end_date="", user_nick="", open_id="", source_type=0, source_object_id="",
                           field="*"):
        """
        :description: 获取用户资产流水记录
        :param app_id：应用标识
        :param act_id：活动标识
        :param asset_type：资产类型(1-次数2-积分3-价格档位)
        :param page_size：条数
        :param page_index：页数
        :param user_id：用户标识
        :param asset_object_id：资产对象标识
        :param start_date：开始时间
        :param end_date：结束时间
        :param user_nick：昵称
        :param open_id：open_id
        :param source_type：来源类型（1-购买2-任务3-手动配置4-抽奖5-回购）
        :param source_object_id：来源对象标识(比如来源类型是任务则对应任务类型)
        :param field：查询字段
        :return: 返回PageInfo
        :last_editors: HuangJianYi
        """
        page_info = SevenHelper.get_dict_page_info_list(page_index, page_size, 0, [])
        if not act_id or asset_type <= 0:
            return page_info

        condition = "act_id=%s AND asset_type=%s"
        params = [act_id, asset_type]

        if app_id:
            condition += " AND app_id=%s"
            params.append(app_id)
        if user_id != 0:
            condition += " AND user_id=%s"
            params.append(user_id)
        if open_id:
            condition += " AND open_id=%s"
            params.append(open_id)
        if user_nick:
            condition += " AND user_nick=%s"
            params.append(user_nick)
        if asset_object_id:
            condition += " AND asset_object_id=%s"
            params.append(asset_object_id)
        if start_date:
            condition += " AND create_date>=%s"
            params.append(start_date)
        if end_date:
            condition += " AND create_date<=%s"
            params.append(end_date)
        if source_type != 0:
            condition += " AND source_type=%s"
            params.append(source_type)
        if source_object_id:
            condition += " AND source_object_id=%s"
            params.append(source_object_id)
        page_list, total = PlatformAssetLogModel().get_dict_page_list(field,
                                                                      page_index,
                                                                      page_size,
                                                                      condition,
                                                                      order_by="create_date desc",
                                                                      params=params)
        if len(page_list) > 0:
            for item in page_list:
                item["create_day"] = item["create_date"].strftime('%Y-%m-%d')
        page_info = SevenHelper.get_dict_page_info_list(page_index, page_size, total, page_list)
        return page_info

    def get_asset_warn_list(self, app_id, act_id, asset_type, page_size=20, page_index=0, user_id=0, asset_object_id="",
                            start_date="", end_date="", user_nick="", open_id="", field="*"):
        """
        :description: 获取资产预警记录
        :param app_id：应用标识
        :param act_id：活动标识
        :param asset_type：资产类型(1-次数2-积分3-价格档位)
        :param page_size：条数
        :param page_index：页数
        :param user_id：用户标识
        :param asset_object_id：资产对象标识
        :param start_date：开始时间
        :param end_date：结束时间
        :param user_nick：昵称
        :param open_id：open_id
        :param field：查询字段
        :return: 返回PageInfo
        :last_editors: HuangJianYi
        """
        page_info = SevenHelper.get_dict_page_info_list(page_index, page_size, 0, [])
        if not act_id:
            return page_info

        condition = "act_id=%s and asset_type=%s"
        params = [act_id, asset_type]
        if app_id:
            condition += " AND app_id=%s"
            params.append(app_id)
        if asset_type != 0:
            condition += " AND asset_type=%s"
            params.append(asset_type)
        if asset_object_id:
            condition += " AND asset_object_id=%s"
            params.append(asset_object_id)
        if user_id != 0:
            condition += " AND user_id=%s"
            params.append(user_id)
        if open_id:
            condition += " AND open_id=%s"
            params.append(open_id)
        if user_nick:
            condition += " AND user_nick=%s"
            params.append(user_nick)
        if start_date:
            condition += " AND create_date>=%s"
            params.append(start_date)
        if end_date:
            condition += " AND create_date<=%s"
            params.append(end_date)

        page_list, total = PlatformAssetWarnNoticeModel().get_dict_page_list(field, page_index, page_size,
                                                                             condition, order_by="id desc",
                                                                             params=params)
        page_info = SevenHelper.get_dict_page_info_list(page_index, page_size, total, page_list)
        return page_info

    def get_user_integral(self, user_id):
        """
        :description: 获取用户积分
        :param user_id：用户标识
        :return: 返回list
        :last_editors: SunYiTan
        """
        if not user_id:
            return 0

        app_id = self.__APPID
        asset_type = AssetType.Integral.value
        asset_object_id = 0

        now_date = TimeHelper.get_now_datetime()
        act_id = SevenHelper.datetime_to_int(now_date, "%Y")
        last_act_id = act_id - 1

        user_asset_model = PlatformUserAssetModel()
        id_md5 = self._get_user_asset_id_md5(act_id, user_id, asset_type, asset_object_id)
        last_id_md5 = self._get_user_asset_id_md5(last_act_id, user_id, asset_type, asset_object_id)
        user_asset_dict_list = user_asset_model.get_dict_list(f"id_md5 IN({id_md5},{last_id_md5})")
        integral = 0
        for user_asset_dict in user_asset_dict_list:
            if user_asset_dict["app_id"] != str(app_id):
                user_asset_dict["asset_value"] = 0
            if self._get_asset_check_code(user_asset_dict["id_md5"], user_asset_dict["asset_value"], app_id) != \
                    user_asset_dict["asset_check_code"]:
                user_asset_dict["asset_value"] = 0

            integral += user_asset_dict["asset_value"]

        return integral

    def update_user_integral(self, user_id, asset_value,
                             source_type, source_object_id, source_object_name, log_title,
                             module_id=0, only_id="",
                             info_json=None):
        """
        :description: 变更积分
        :param user_id：用户标识
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
        if info_json is None:
            info_json = {}

        invoke_result_data = InvokeResultData()

        app_id = self.__APPID
        asset_type = AssetType.Integral.value
        asset_object_id = 0
        asset_value = int(asset_value)

        now_day_int = SevenHelper.get_now_day_int()
        now_datetime = SevenHelper.get_now_datetime()
        now_date = TimeHelper.get_now_datetime()
        cur_act_id = SevenHelper.datetime_to_int(now_date, "%Y")
        last_act_id = cur_act_id - 1

        if not user_id or not asset_type or not asset_value:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "参数不能为空或等于0"
            return invoke_result_data

        user_dict = PlatformUserInfoModel().get_dict(where="user_id=%s", field="user_nick", params=[user_id])
        if not user_dict:
            invoke_result_data.success = False
            invoke_result_data.error_code = "user_not_exist"
            invoke_result_data.error_message = "用户信息不存在"
            return invoke_result_data

        user_nick = user_dict["user_nick"]
        handler_name = self.context.__class__.__name__ if self.context else ""
        request_code = self.context.request_code if self.context else ""

        db_transaction = DbTransaction(db_config_dict=config.get_value("db_platform"))
        user_asset_model = PlatformUserAssetModel(db_transaction=db_transaction)
        asset_log_model = PlatformAssetLogModel(db_transaction=db_transaction)
        asset_only_model = PlatformAssetOnlyModel(db_transaction=db_transaction)
        asset_inventory_model = PlatformAssetInventoryModel(db_transaction=db_transaction)

        try:
            # 数据库，事务开始
            db_transaction.begin_transaction()
            redis_util = RedisUtil()
            only_cache_key_list = []

            # 增加时，增加今年的积分
            act_id_list = [cur_act_id]
            if asset_value < 0:
                # 扣除时，先扣除前年的积分，再扣除今年的积分
                act_id_list = [last_act_id, cur_act_id]

            for act_id in act_id_list:
                if asset_value == 0:
                    break

                user_asset_id_md5 = self._get_user_asset_id_md5(act_id, user_id, asset_type, asset_object_id)
                if user_asset_id_md5 == 0:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "修改失败"
                    return invoke_result_data

                # 如果only_id已经存在，直接在redis进行拦截,减少数据库的请求，时限1天
                if only_id:
                    only_cache_key = f"asset_only_list:{act_id}_{now_day_int}"
                    only_cache_key_list.append(only_cache_key)
                    if redis_util.hexists(only_cache_key, only_id):
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = "only_id已经存在"
                        # 添加唯一标识预警拦截计数,用于控制台跑数据进行并发预警
                        self._add_onlyid_warn_stat(handler_name)
                        return invoke_result_data

                # 修改用户积分
                old_user_asset_id = 0
                user_asset = user_asset_model.get_entity("id_md5=%s", params=[user_asset_id_md5])
                if user_asset:
                    old_user_asset_id = user_asset.id
                else:
                    user_asset = PlatformUserAsset()
                    user_asset.id_md5 = user_asset_id_md5
                    user_asset.app_id = app_id
                    user_asset.act_id = act_id
                    user_asset.user_id = user_id
                    user_asset.open_id = ""
                    user_asset.user_nick = user_dict["user_nick"]
                    user_asset.asset_type = asset_type
                    user_asset.asset_object_id = asset_object_id
                    user_asset.create_date = now_datetime

                if asset_value < 0 and user_asset.asset_value <= 0:
                    # 跳过没有积分的年份
                    continue

                history_asset_value = user_asset.asset_value
                if asset_value < 0:
                    # 扣除积分
                    if user_asset.asset_value + asset_value < 0:
                        # 剩余积分不足
                        change_value = -user_asset.asset_value
                        asset_value += user_asset.asset_value
                        user_asset.asset_value = 0
                    else:
                        # 剩余积分足够
                        change_value = asset_value
                        user_asset.asset_value += asset_value
                        asset_value = 0
                else:
                    # 增加积分
                    change_value = asset_value
                    user_asset.asset_value += asset_value
                    asset_value = 0

                user_asset.asset_check_code = self._get_asset_check_code(user_asset_id_md5, user_asset.asset_value,
                                                                         app_id)
                user_asset.modify_date = now_datetime
                if old_user_asset_id != 0:
                    user_asset_model.update_entity(user_asset, "asset_value,asset_check_code,modify_date")
                else:
                    user_asset_model.add_entity(user_asset)

                # 更新玩家资产进销表
                self.update_asset_inventory(asset_inventory_model, app_id, act_id, user_id, user_nick, asset_type,
                                            asset_object_id, change_value, user_asset.asset_value, history_asset_value,
                                            now_day_int, now_datetime)

                # 新增流水表
                self.add_asset_log(asset_log_model, app_id, act_id, module_id, user_id, user_nick, asset_type,
                                   asset_object_id,
                                   change_value, user_asset.asset_value, history_asset_value,
                                   source_type, source_object_id, source_object_name,
                                   log_title, only_id, info_json,
                                   now_day_int, now_datetime, handler_name, request_code)

                if only_id:
                    self.add_asset_only(asset_only_model, app_id, act_id, user_id, only_id, now_datetime)

            if asset_value < 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = "no_enough"
                invoke_result_data.error_message = "星币不足"
                return invoke_result_data

            # 数据库，事务提交
            result = db_transaction.commit_transaction()
            if not result:
                if only_id:
                    # 添加唯一标识预警拦截计数,用于控制台跑数据进行并发预警
                    self._add_onlyid_warn_stat(handler_name)

                invoke_result_data.success = False
                invoke_result_data.error_code = "fail"
                invoke_result_data.error_message = "系统繁忙,请稍后再试"
                return invoke_result_data

            if only_id:
                for only_cache_key in only_cache_key_list:
                    redis_util.hset(only_cache_key, only_id, 1)
                    redis_util.expire(only_cache_key, 24 * 3600)

            invoke_result_data.data = self.get_user_integral(user_id)

        except Exception as ex:
            if self.context:
                self.context.logging_link_error(f"【变更资产】：{traceback.format_exc()}")
            else:
                logging.getLogger("log_error").error(f"【变更资产】：{traceback.format_exc()}")

            if db_transaction.is_transaction == True:
                # 数据库，事务回滚
                db_transaction.rollback_transaction()

            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
            return invoke_result_data

        return invoke_result_data

    def update_asset_inventory(self, asset_inventory_model, app_id, act_id, user_id, user_nick, asset_type,
                               asset_object_id,
                               asset_value, now_asset_value, history_asset_value,
                               now_day_int, now_datetime):
        """
        更新玩家资产进销表
        """
        asset_inventory_id_md5 = CryptoHelper.md5_encrypt_int(
            f"{act_id}_{user_id}_{asset_type}_{asset_object_id}_{now_day_int}")
        asset_inventory = asset_inventory_model.get_entity("id_md5=%s", params=[asset_inventory_id_md5])
        asset_inventory_update_sql = f"process_count=0,now_value={now_asset_value}"
        if asset_inventory:
            old_asset_inventory_id = asset_inventory.id
            if asset_value > 0:
                asset_inventory_update_sql += f",inc_value=inc_value+{asset_value}"
            else:
                asset_inventory_update_sql += f",dec_value=dec_value+{asset_value}"

            asset_inventory_model.update_table(asset_inventory_update_sql, "id=%s",
                                               params=[old_asset_inventory_id])
        else:
            asset_inventory = PlatformAssetInventory()
            asset_inventory.id_md5 = asset_inventory_id_md5
            asset_inventory.app_id = app_id
            asset_inventory.act_id = act_id
            asset_inventory.user_id = user_id
            asset_inventory.open_id = ""
            asset_inventory.user_nick = user_nick
            asset_inventory.asset_type = asset_type
            asset_inventory.asset_object_id = asset_object_id
            if asset_value > 0:
                asset_inventory.inc_value += asset_value
            else:
                asset_inventory.dec_value += asset_value
            asset_inventory.history_value = history_asset_value
            asset_inventory.now_value = now_asset_value
            asset_inventory.create_date = now_datetime
            asset_inventory.create_day = now_day_int
            asset_inventory_model.add_entity(asset_inventory)

    def add_asset_log(self, asset_log_model, app_id, act_id, module_id, user_id, user_nick, asset_type,
                      asset_object_id,
                      asset_value, now_asset_value, history_asset_value,
                      source_type, source_object_id, source_object_name,
                      log_title, only_id, info_json,
                      now_day_int, now_datetime, handler_name, request_code):
        """
        新增流水表
        """
        asset_log = PlatformAssetLog()
        asset_log.app_id = app_id
        asset_log.act_id = act_id
        asset_log.module_id = module_id
        asset_log.user_id = user_id
        asset_log.open_id = ""
        asset_log.user_nick = user_nick
        asset_log.log_title = log_title
        asset_log.info_json = info_json if not info_json else {}
        asset_log.asset_type = asset_type
        asset_log.asset_object_id = asset_object_id
        asset_log.source_type = source_type
        asset_log.source_object_id = source_object_id
        asset_log.source_object_name = source_object_name
        asset_log.only_id = only_id
        asset_log.operate_type = 0 if asset_value > 0 else 1
        asset_log.operate_value = asset_value
        asset_log.history_value = history_asset_value
        asset_log.now_value = now_asset_value
        asset_log.handler_name = handler_name
        asset_log.request_code = request_code
        asset_log.create_date = now_datetime
        asset_log.create_day = now_day_int
        asset_log_model.add_entity(asset_log)

    def add_asset_only(self, asset_only_model, app_id, act_id, user_id, only_id, now_datetime):
        """
        新增资产唯一表
        """
        asset_only = PlatformAssetOnly()
        asset_only.id_md5 = CryptoHelper.md5_encrypt_int(f"{act_id}_{user_id}_{only_id}")
        asset_only.app_id = app_id
        asset_only.act_id = act_id
        asset_only.user_id = user_id
        asset_only.open_id = ""
        asset_only.only_id = only_id
        asset_only.create_date = now_datetime
        asset_only_model.add_entity(asset_only)
