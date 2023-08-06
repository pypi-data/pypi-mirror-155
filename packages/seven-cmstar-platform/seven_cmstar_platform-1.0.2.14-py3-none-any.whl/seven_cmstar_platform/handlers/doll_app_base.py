# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-01-05 17:16:17
@LastEditTime: 2021-04-21 09:33:51
@LastEditors: SunYiTan
@Description: 
"""
from threading import Thread

from jwt import ExpiredSignatureError, DecodeError
from seven_framework.web_tornado.base_handler.base_api_handler import *

from seven_cmstar_platform.models.asset_base_model import AssetBaseModel
from seven_cmstar_platform.models.db_models.platform.platform_doll_info_model import PlatformDollInfoModel
from seven_cmstar_platform.models.db_models.platform.platform_user_address_model import PlatformUserAddressModel
from seven_cmstar_platform.models.db_models.platform.platform_user_info_model import PlatformUserInfoModel
from seven_cmstar_platform.models.db_models.platform.platform_user_third_auth_model import PlatformUserThirdAuthModel
from seven_cmstar_platform.models.db_models_ex.platform.platform_search_statiscs_log_model_ex import \
    SearchStatisticsLogModelEx
from seven_cmstar_platform.models.db_models_ex.platform.platform_user_follow_model_ex import PlatformUserFollowModelEx
from seven_cmstar_platform.models.db_models_ex.platform.platform_user_statistics_log_model_ex import \
    UserStatisticsLogModelEx
from seven_cmstar_platform.models.db_models_ex.platform.platform_user_statistics_model_ex import UserStatisticsModelEx
from seven_cmstar_platform.models.user_base_model import UserTokenParam, UserBaseInfo
from seven_cmstar_platform.models.enum import AppBaseRedisKeyType, StatisticsOrmType, UserStatisticsType, \
    AppChannelType, UserType
from seven_cmstar_platform.utils.json_util import JsonUtil
from seven_cmstar_platform.utils.jwt_util import JwtUtil
from seven_cmstar_platform.utils.redis_util import RedisUtil


class DollAppBaseHandler(BaseApiHandler):
    """
    :description: 客户端基类
    """

    def options_async(self):
        self.reponse_json_success()

    def check_xsrf_cookie(self):
        return

    def set_default_headers(self):
        allow_origin_list = config.get_value("allow_origin_list")
        origin = self.request.headers.get("Origin")
        if origin:
            if "--production" in sys.argv or "--testing" in sys.argv:
                if origin in allow_origin_list:
                    self.set_header("Access-Control-Allow-Origin", origin)
            else:
                # 本地测试，都通过
                self.set_header("Access-Control-Allow-Origin", origin)

        self.set_header("Access-Control-Allow-Headers",
                        "Origin,X-Requested-With,Content-Type,Accept,User-Token,Manage-ProductID,Manage-PageID,PYCKET_ID")
        self.set_header("Access-Control-Allow-Methods", "POST,GET,OPTIONS")
        self.set_header("Access-Control-Allow-Credentials", "true")

    def prepare_ext(self):
        """
        置于任何请求方法前被调用扩展
        :return:
        :last_editors: SunYiTan
        """
        http_log = config.get_value("http_log")
        if http_log and http_log is True:
            if "Content-Type" in self.request.headers and self.request.headers["Content-type"].lower().find(
                    "application/json") >= 0 and self.request.body:
                request_params = json.loads(self.request.body)
            else:
                request_params = self.request.arguments

            self.logging_link_info(
                f"--- request: {self.request.path} ---:\n{JsonUtil.dumps(request_params)}")

    def write_error(self, status_code, **kwargs):
        """
        :Description: 重写全局异常事件捕捉
        :last_editors: ChenXiaolei
        """
        self.logger_error.error(
            traceback.format_exc(),
            extra={"extra": {
                "request_code": self.request_code
            }})

        self.set_status(200)
        return self.reponse_json_error("SystemError", "对不起，系统发生错误")

    def http_reponse(self, content, log_extra_dict=None):
        """
        :description: 将字符串返回给客户端
        :param content: 内容字符串
        :param log_extra_dict:
        :return: 将字符串返回给客户端
        :last_editors: SunYiTan
        """
        http_log = config.get_value("http_log")
        if http_log and http_log is True:
            self.logging_link_info(f"--- response: {self.request.path} ---:\n{content}")

        super().http_reponse(content, log_extra_dict)

    def reponse_json_success(self, data=None, desc='调用成功'):
        """
        :description: 通用成功返回json结构
        :param data: 返回结果对象，即为数组，字典
        :param desc: 字符串，服务端返回的错误信息
        :return: 将dumps后的数据字符串返回给客户端
        :last_editors: HuangJingCan
        """
        self.reponse_common("0", desc, data)

    def reponse_json_error(self, error_code="", error_message="", data=None, log_type=0):
        """
        :description: 通用错误返回json结构
        :param error_code: 字符串，调用失败（success为false）时，服务端返回的错误码
        :param error_message: 字符串，调用失败（success为false）时，服务端返回的错误信息
        :param data: 返回结果对象，即为数组，字典
        :param log_type: 日志记录类型（0-不记录，1-info，2-error）
        :return: 将dumps后的数据字符串返回给客户端
        :last_editors: HuangJianYi
        """
        if log_type == 1:
            self.logging_link_info(f"{error_code}\n{error_message}\n{data}\n{self.request}")
        elif log_type == 2:
            self.logging_link_error(f"{error_code}\n{error_message}\n{data}\n{self.request}")

        self.reponse_common(error_code, error_message, data)

    def reponse_common(self, result, desc, data=None, log_extra_dict=None):
        """
        :Description: 输出公共json模型
        :param result: 返回结果标识
        :param desc: 返回结果描述
        :param data: 返回结果对象，即为数组，字典
        :param log_extra_dict:
        :return: 将dumps后的数据字符串返回给客户端
        :last_editors: SunYiTan
        """
        template_value = {
            'result': result,
            'desc': desc,
            'data': data}

        self.http_reponse(JsonUtil.dumps(template_value), log_extra_dict)

    def get_param(self, param_name, default="", strip=True):
        """
        :Description: 二次封装获取参数
        :param param_name: 参数名
        :param default: 如果无此参数，则返回默认值
        :param strip:
        :return: 参数值
        :last_editors: SunYiTan
        """
        param_ret = ""

        try:
            if "Content-Type" in self.request.headers and \
                    self.request.headers["Content-type"].lower().find("application/json") >= 0 and \
                    self.request.body:
                json_params = json.loads(self.request.body)
                param_ret = json_params.get(param_name, default)
            else:
                param_ret = self.get_argument(param_name, default, strip=strip)

        except Exception as e:
            self.logging_link_error(traceback.format_exc())

        if param_ret == "":
            param_ret = default

        return param_ret

    def get_int_param(self, param_name, default="", strip=True):
        """
        二次封装获取参数，转换成int类型
        :param param_name: 参数名
        :param default: 如果无此参数，则返回默认值
        :param strip:
        :return: 参数值
        :last_editors: SunYiTan
        """
        param_ret = self.get_param(param_name, default, strip)
        try:
            return int(param_ret)
        except ValueError:
            pass

        return 0

    @staticmethod
    def get_condition_by_id_list(primary_key, id_list=None):
        """
        :description: 根据id_list返回查询条件
        :param primary_key：主键
        :param id_list：id：列表
        :return: 查询条件字符串
        :last_editors: HuangJingCan
        """
        if not id_list:
            return ""
        id_list_str = str(id_list).strip('[').strip(']')
        return f"{primary_key} IN({id_list_str})"

    def create_user_token(self, user_token_param: UserTokenParam):
        """
        生成token
        :param user_id:
        :param third_auth_id:
        :return:
        """
        access_token, expire_time = self.__create_access_token(user_token_param)
        return access_token

    def create_user_token_2(self, user_token_param: UserTokenParam):
        """
        创建用户token
        :param user_token_param:
        :return:
        """
        access_token, expire_time = self.__create_access_token(user_token_param)
        refresh_token, _ = self.__create_refresh_token(user_token_param)

        return {"access_token": access_token, "expire_time": expire_time, "refresh_token": refresh_token}

    def refresh_user_token(self, refresh_token):
        """
        刷新用户token
        :param refresh_token:
        :return:
        """
        jwt_secret = config.get_value("jwt_refresh_secret")

        if not refresh_token:
            return None

        try:
            sub_info = JwtUtil.get_sub_info_from_token(refresh_token, jwt_secret)
            user_token_param = UserTokenParam.dict_2_entity(json.loads(sub_info))
            user_id = user_token_param.user_id
            third_auth_id = user_token_param.third_auth_id

            if user_id > 0:
                # 多平台同时登录，iOS应用和安卓应用不能同时登录
                app_channel = user_token_param.app_channel
                if app_channel == AppChannelType.AndroidApp.value:
                    app_channel = AppChannelType.iOSApp.value

                key = AppBaseRedisKeyType.UserRefreshToken.value + str(user_token_param.user_id) + "_" + str(
                    app_channel)
                old_token = RedisUtil().get(key)
            else:
                key = AppBaseRedisKeyType.ThirdRefreshToken.value + str(third_auth_id)
                old_token = RedisUtil().get(key)
            if not old_token:
                # 已过期
                return None

            if old_token != refresh_token:
                # 在别处登录
                return None

            return self.create_user_token_2(user_token_param)

        except:
            return None

    def __create_access_token(self, user_token_param: UserTokenParam):
        """
        access_token，缓存时间：7天
        :param user_token_param:
        :return:
        """
        jwt_secret = config.get_value("jwt_secret")
        jwt_expire = config.get_value("jwt_expire")

        user_token_param.version = 20210909  # QQ和微信版本分开，可以同时登录
        # 生成没有时间限制的token
        token = JwtUtil.create_token(JsonUtil.dumps(user_token_param), jwt_secret, -1)

        # 刷新缓存
        if user_token_param.user_id > 0:
            # 多平台同时登录，iOS应用和安卓应用不能同时登录
            app_channel = user_token_param.app_channel
            if app_channel == AppChannelType.AndroidApp.value:
                app_channel = AppChannelType.iOSApp.value

            key = AppBaseRedisKeyType.UserToken.value + str(user_token_param.user_id) + "_" + str(app_channel)
            # B端用户
            if user_token_param.user_type == UserType.Business.value:
                key = f"{key}_{user_token_param.user_type}"
            RedisUtil().set(key, token, jwt_expire * 24 * 60 * 60)
        else:
            key = AppBaseRedisKeyType.ThirdToken.value + str(user_token_param.third_auth_id)
            RedisUtil().set(key, token, jwt_expire * 24 * 60 * 60)

        return token, jwt_expire * 24 * 60 * 60

    def __create_refresh_token(self, user_token_param: UserTokenParam):
        """
        refresh_token，缓存时间：30天
        :param user_token_param:
        :return:
        """
        jwt_secret = config.get_value("jwt_refresh_secret")
        jwt_expire = config.get_value("jwt_refresh_expire")

        user_token_param.version = 20210909  # QQ和微信版本分开，可以同时登录
        token = JwtUtil.create_token(JsonUtil.dumps(user_token_param), jwt_secret, jwt_expire + 1)

        # 刷新缓存
        if user_token_param.user_id > 0:
            # 多平台同时登录，iOS应用和安卓应用不能同时登录
            app_channel = user_token_param.app_channel
            if app_channel == AppChannelType.AndroidApp.value:
                app_channel = AppChannelType.iOSApp.value

            key = AppBaseRedisKeyType.UserRefreshToken.value + str(user_token_param.user_id) + "_" + str(app_channel)
            # B端用户
            if user_token_param.user_type == UserType.Business.value:
                key = f"{key}_{user_token_param.user_type}"
            RedisUtil().set(key, token, jwt_expire * 24 * 60 * 60)
        else:
            key = AppBaseRedisKeyType.ThirdRefreshToken.value + str(user_token_param.third_auth_id)
            RedisUtil().set(key, token, jwt_expire * 24 * 60 * 60)

        return token, jwt_expire * 24 * 60 * 60

    def request_header_token(self):
        header_token = {}
        if "User-Token" in self.request.headers:
            req_info_list = str.split(self.request.headers["User-Token"], ";")
            for info in req_info_list:
                kv = str.split(info, "=")
                header_token[kv[0]] = kv[1]
        return header_token

    def get_user_token_param(self) -> UserTokenParam:
        """
        获取请求的玩家信息
        :return:
        """
        header_token = self.request_header_token()
        user_token = header_token.get("UserToken", "")
        jwt_secret = config.get_value("jwt_secret")

        if not user_token:
            return UserTokenParam()

        try:
            sub_info = JwtUtil.get_sub_info_from_token(user_token, jwt_secret)
            return UserTokenParam.dict_2_entity(json.loads(sub_info))
        except:
            return UserTokenParam()

    def get_user_id(self):
        return self.get_user_token_param().user_id

    def get_third_auth_id(self):
        return self.get_user_token_param().third_auth_id

    def get_user_base_info(self, user_id, third_auth_id):
        """
        获取用户基础信息
        :param user_id: 用户唯一id
        :return: UserBaseInfo()
        """
        user_dict = PlatformUserInfoModel().get_dict(where="user_id=%s", params=[user_id])
        if not user_dict:
            return None
        third_auth = PlatformUserThirdAuthModel().get_dict(where="auth_id=%s", params=[third_auth_id])
        if not third_auth:
            return None

        user_base_info = UserBaseInfo()
        user_base_info.user_id = user_dict["user_id"]  # 用户唯一id
        user_base_info.channel = third_auth["last_app_channel"]  # 登录APP渠道标识，0：NoSdk 1：QQ小程序 2：微信小程序，3：iOS应用，4：安卓应用
        user_base_info.app_id = third_auth["app_id"]  # 第三方app_id
        user_base_info.open_id = third_auth["open_id"]  # open_id
        user_base_info.user_nick = user_dict["user_nick"]  # 用户昵称
        user_base_info.avatar = user_dict["avatar"]  # 用户头像
        return user_base_info.__dict__

    def get_user_integral(self, user_id):
        """
        获取用户积分
        :param user_id: 用户唯一id
        :return: 用户当前积分
        """
        return AssetBaseModel(self).get_user_integral(user_id)

    def update_user_integral(self, user_id, asset_value,
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
        return AssetBaseModel(self).update_user_integral(
            user_id, asset_value,
            source_type, source_object_id, source_object_name, log_title, module_id, only_id, info_json)

    def get_user_address_info(self, user_id, address_id):
        """
        获取用户收货地址信息
        :param user_id:
        :param address_id
        :return:
        """
        address_dict = PlatformUserAddressModel().get_dict(where="user_id=%s AND address_id=%s AND is_del=0",
                                                           params=[user_id, int(address_id)])
        if not address_dict:
            return None

        temp_dict = {
            "address_id": str(address_dict["address_id"]),  # 地址唯一id
            "user_nick": address_dict["user_nick"],  # 收货人
            "telephone": address_dict["telephone"],  # 手机号
            "province_name": address_dict["province_name"],  # 省份
            "city_name": address_dict["city_name"],  # 城市
            "district_name": address_dict["district_name"],  # 区县
            "address_info": address_dict["address_info"],  # 详细地址
            "is_default": address_dict["is_default"]  # 是否默认，1是 0否
        }

        return temp_dict

    def has_bought_plez(self, user_id):
        """
        判断用户是否过 扑棱蛾子
        :param user_id:
        :return:
        """
        user_dict = PlatformUserInfoModel().get_dict(where="user_id=%s", params=[user_id])
        if not user_dict:
            return False

        total = PlatformDollInfoModel().get_total(
            where="((telephone=%s AND activate_user_id=0) OR user_id=%s) AND goods_code=%s AND get_type=1",
            params=[user_dict["telephone"], user_id, "PLEZ"])
        return True if total and total > 0 else False

    def get_user_follow_status(self, user_id, other_id):
        """
        获取用户关注状态
        :param user_id:  用户平台ID
        :param other_id: 需要查看的其他用户id
        :return: 1关注过 0未关注
        """
        if not user_id or not other_id:
            return 0

        user_id = int(user_id)
        if user_id <= 0:
            return 0

        user_follow_model = PlatformUserFollowModelEx()
        dependency_key = user_follow_model.get_dependency_key(user_id)
        total = user_follow_model.get_cache_total(dependency_key=dependency_key,
                                                  where=f"user_id=%s AND followed_user_id=%s",
                                                  params=[int(user_id), int(other_id)])

        return 1 if total else 0

    def get_followed_user_ids(self, user_id):
        """
        获取关注的用户平台ID列表
        :param user_id: 用户平台ID
        :return:
        """
        user_id = int(user_id)
        if user_id <= 0:
            return []

        user_follow_model = PlatformUserFollowModelEx()
        dependency_key = user_follow_model.get_dependency_key(user_id)
        dict_list = user_follow_model.get_cache_dict_list(dependency_key=dependency_key,
                                                          where=f"user_id=%s",
                                                          field="followed_user_id",
                                                          params=[int(user_id)])

        return [x["followed_user_id"] for x in dict_list]

    def is_mute(self, user_id):
        """
        判断用户是否被禁言
        :param user_id:
        :return:
        """
        if user_id <= 0:
            return False

        user_dict = PlatformUserInfoModel().get_dict(where="user_id=%s", params=[user_id])
        return user_dict and user_dict["status"] == 1 and user_dict["freeze_end_date"] > TimeHelper.get_now_datetime()

    def post_event(self, user_id):
        """
        发帖事件
        :param user_id: 用户平台ID
        :return:
        """
        user_id = int(user_id)
        if user_id <= 0:
            return

        # 数据统计
        UserStatisticsLogModelEx().add_log(user_id, 0, StatisticsOrmType.ClubPost.value, 1)
        UserStatisticsModelEx().add_value(user_id, UserStatisticsType.PostNum.value, 1)

    def comment_post_event(self, user_id, _post_id, reply_id):
        """
        发表评论事件
        :param user_id: 用户平台ID
        :param post_id: 帖子ID
        :param reply_id: 评论ID
        :return:
        """
        user_id = int(user_id)
        if user_id <= 0:
            return

        # 数据统计
        if reply_id <= 0:
            # 不包括评论的评论
            UserStatisticsLogModelEx().add_log(user_id, 0, StatisticsOrmType.ClubComment.value, 1)
        # 包括评论的评论
        UserStatisticsModelEx().add_value(user_id, UserStatisticsType.CommentNum.value, 1)

    def post_dig_event(self, user_id, _post_id, oper_type):
        """
        帖子点赞事件
        :param user_id: 用户平台ID
        :param post_id: 帖子ID
        :param oper_type: 1点赞0取消点赞
        :return:
        """
        user_id = int(user_id)
        if user_id <= 0:
            return

        # 数据统计
        if oper_type == 1:
            UserStatisticsLogModelEx().add_log(user_id, 0, StatisticsOrmType.ClubDig.value, 1)

    def add_search_log(self, search_keyword):
        """
        搜索数据统计
        :param search_keyword:
        :return:
        """
        SearchStatisticsLogModelEx().add_log(search_keyword, 1)


def login_filter(is_check_bind=True):
    """
    :description: 头部过滤装饰器 仅限handler使用
    :param is_check_bind: 是否开启手机号绑定校验
    :last_editors: SunYiTan
    """

    def wrapper(handler):
        def _wrapper(self, **kwargs):
            try:
                header_token = self.request_header_token()
                user_token = header_token.get("UserToken", "")
                jwt_secret = config.get_value("jwt_secret")

                if not user_token:
                    if is_check_bind:
                        self.logging_link_error(f"--- 头部验证信息为空: {self.request.path} : {self.request.headers}")
                        return self.reponse_json_error("TokenEmpty", "非法请求")
                    else:
                        return handler(self, **kwargs)

                sub_info = JwtUtil.get_sub_info_from_token(user_token, jwt_secret)
                user_token_param = UserTokenParam.dict_2_entity(json.loads(sub_info))
                user_id = user_token_param.user_id
                third_auth_id = user_token_param.third_auth_id

                if is_check_bind is True and user_id <= 0:
                    return self.reponse_json_error("UnboundTelephone", "对不起，请先绑定手机号")

                if user_id > 0:
                    # 多平台同时登录，iOS应用和安卓应用不能同时登录
                    app_channel = user_token_param.app_channel
                    if app_channel == AppChannelType.AndroidApp.value:
                        app_channel = AppChannelType.iOSApp.value

                    key = AppBaseRedisKeyType.UserToken.value + str(user_token_param.user_id) + "_" + str(app_channel)
                    # B端用户
                    if user_token_param.user_type == UserType.Business.value:
                        key = f"{key}_{user_token_param.user_type}"
                else:
                    key = AppBaseRedisKeyType.ThirdToken.value + str(third_auth_id)

                redis_util = RedisUtil()
                old_token = redis_util.get(key)
                if not old_token:
                    return self.reponse_json_error("ExpiredSignatureError", "登录已过期，请重新进入小程序")

                if old_token != user_token:
                    return self.reponse_json_error("LoginOther", "对不起，账号在其他地方登录，请重新登录哦~")

                # 延迟时间
                jwt_expire = config.get_value("jwt_expire")
                redis_util.expire(key, jwt_expire * 24 * 60 * 60)

                # 计算停留时间
                if user_id > 0:
                    UserStatisticsLogModelEx().record_remain_time(user_id)

            except ExpiredSignatureError as ex:
                self.logging_link_error(str(ex) + "【登录超时】")
                return self.reponse_json_error("ExpiredSignatureError", "登录已过期，请重新进入小程序")

            except DecodeError as ex:
                self.logging_link_error(str(ex) + "【jwt解码失败】")
                return self.reponse_json_error("DecodeError", "非法请求")

            except Exception as ex:
                self.logging_link_error(traceback.format_exc())
                return self.reponse_json_error("Error", "服务端错误")

            return handler(self, **kwargs)

        return _wrapper

    return wrapper


def add_user_lock(lock_key_head):
    """
    玩家数据加锁，装饰器 仅限handler使用
    :param lock_key_head:
    :return:
    """

    def wrapper(handler):
        def _wrapper(self, **kwargs):

            user_token_param = self.get_user_token_param()
            user_id = user_token_param.user_id

            if user_id <= 0:
                return handler(self, **kwargs)

            lock_key = f"{lock_key_head}:{user_id}"
            redis_util = RedisUtil()
            lock_value = redis_util.acquire_lock_with_timeout(lock_key)
            if lock_value:
                try:

                    ret = handler(self, **kwargs)

                except Exception as e:
                    self.logging_link_error(traceback.format_exc())
                    return self.reponse_json_error("SystemError", "对不起，系统发生错误")

                finally:
                    redis_util.release_lock(lock_key, lock_value)
            else:
                return self.reponse_json_error("LockTimeout", "服务器忙，请稍后再试")

            return ret

        return _wrapper

    return wrapper


def async_func(f):
    """
    异步执行
    :param f:
    :return:
    """

    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper
