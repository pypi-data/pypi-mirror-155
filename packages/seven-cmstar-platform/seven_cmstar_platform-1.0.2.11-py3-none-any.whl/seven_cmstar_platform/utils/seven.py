# -*- coding: utf-8 -*-
"""
:Author: HuangJingCan
:Date: 2020-04-22 14:32:40
:LastEditTime: 2020-07-22 09:59:51
:LastEditors: HuangJingCan
:Description: 常用帮助类
"""
import datetime
import json
import random
import re

from seven_framework import CryptoHelper, config, TimeHelper, HTTPHelper
from seven_framework.base_model import BaseModel
from seven_framework.redis import RedisHelper

from seven_cmstar_platform.models.seven_model import PageInfo

from seven_cmstar_platform.utils.json_util import JsonUtil
from seven_cmstar_platform.utils.redis_util import RedisUtil


class SevenHelper:

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

    @classmethod
    def get_dict_page_info_list(cls, page_index, page_size, p_dict, total=0):
        """
        :description: 获取分页信息
        :param page_index：页索引
        :param page_size：页大小
        :param p_dict：字典列表
        :return:
        :last_editors: HuangJingCan
        """
        page_info = PageInfo()
        page_info.PageIndex = page_index
        page_info.PageSize = page_size
        page_info.RecordCount = total if total > 0 else len(p_dict)
        page_info.Data = p_dict
        page_info = page_info.get_entity_by_page_info(page_info)
        return page_info.__dict__

    @classmethod
    def to_file_size(cls, size):
        """
        :description: 文件大小格式化
        :param size：文件大小
        :return:
        :last_editors: HuangJingCan
        """
        if size < 1000:
            return '%i' % size + 'size'
        elif 1024 <= size < 1048576:
            return '%.2f' % float(size / 1024) + 'KB'
        elif 1048576 <= size < 1073741824:
            return '%.2f' % float(size / 1048576) + 'MB'
        elif 1073741824 <= size < 1000000000000:
            return '%.2f' % float(size / 1073741824) + 'GB'
        elif 1000000000000 <= size:
            return '%.2f' % float(size / 1000000000000) + 'TB'

    @classmethod
    def get_random(cls, num, many):
        """
        :description: 获取随机数
        :param num：位数
        :param many：个数
        :return:
        :last_editors: CaiYouBin
        """
        result = ""
        for x in range(many):
            s = ""
            for i in range(num):
                # n=1 生成数字  n=2 生成字母
                n = random.randint(1, 2)
                if n == 1:
                    numb = random.randint(0, 9)
                    s += str(numb)
                else:
                    nn = random.randint(1, 2)
                    cc = random.randint(1, 26)
                    if nn == 1:
                        numb = chr(64 + cc)
                        s += numb
                    else:
                        numb = chr(96 + cc)
                        s += numb
            result += s
        return result

    @classmethod
    def get_cache_entity(cls, model: BaseModel, dependency_key,
                         where='', group_by='', order_by='', params=None,
                         expire_sec=10 * 60):
        redis_cli = RedisUtil()
        cache_key = f"{where}_{group_by}_{order_by}_{params}_{model.model_obj.get_field_list()}"
        cache_key = CryptoHelper.md5_encrypt(cache_key.lower())
        cache_key = f"entity_{cache_key}"
        s = redis_cli.hget(dependency_key, cache_key)
        if s:
            return model._BaseModel__row_entity(json.loads(s))

        dict_info = model.get_entity(where, group_by, order_by, params)
        if not dict_info:
            return None

        redis_cli.hset(dependency_key, cache_key, JsonUtil.dumps(dict_info))
        redis_cli.expire(dependency_key, expire_sec)
        return dict_info

    @classmethod
    def get_cache_entity_by_id(cls, model: BaseModel, dependency_key,
                               primary_key_id,
                               expire_sec=10 * 60):
        redis_cli = RedisUtil()
        cache_key = f"{primary_key_id}_{model.model_obj.get_field_list()}"
        cache_key = CryptoHelper.md5_encrypt(cache_key.lower())
        cache_key = f"entity_by_id_{cache_key}"
        s = redis_cli.hget(dependency_key, cache_key)
        if s:
            return model._BaseModel__row_entity(json.loads(s))

        dict_info = model.get_entity_by_id(primary_key_id)
        if not dict_info:
            return None

        redis_cli.hset(dependency_key, cache_key, JsonUtil.dumps(dict_info))
        redis_cli.expire(dependency_key, expire_sec)
        return dict_info

    @classmethod
    def get_cache_list(cls, model: BaseModel, dependency_key,
                       where='', group_by='', order_by='', limit='', params=None,
                       expire_sec=10 * 60):
        redis_cli = RedisUtil()
        cache_key = f"{where}_{group_by}_{order_by}_{limit}_{params}_{model.model_obj.get_field_list()}"
        cache_key = CryptoHelper.md5_encrypt(cache_key.lower())
        cache_key = f"list_{cache_key}"
        s = redis_cli.hget(dependency_key, cache_key)
        if s:
            return model._BaseModel__row_entity_list(json.loads(s))

        dict_list = model.get_list(where, group_by, order_by, limit, params)

        redis_cli.hset(dependency_key, cache_key, JsonUtil.dumps(dict_list))
        redis_cli.expire(dependency_key, expire_sec)
        return dict_list

    @classmethod
    def get_cache_page_list(cls, model: BaseModel, dependency_key,
                            field, page_index, page_size, where='', group_by='', order_by='', params=None,
                            expire_sec=10 * 60):
        redis_cli = RedisUtil()
        cache_key = f"{field}_{page_index}_{page_size}_{where}_{group_by}_{order_by}_{params}_{model.model_obj.get_field_list()}"
        cache_key = CryptoHelper.md5_encrypt(cache_key.lower())
        cache_key = f"page_list_{cache_key}"
        s = redis_cli.hget(dependency_key, cache_key)
        if s:
            value = json.loads(s)
            return model._BaseModel__row_entity_list(value["dict_list"]), value["total"]

        dict_list, total = model.get_page_list(field, page_index, page_size, where, group_by, order_by, params)
        value = {"dict_list": dict_list, "total": total}

        redis_cli.hset(dependency_key, cache_key, JsonUtil.dumps(value))
        redis_cli.expire(dependency_key, expire_sec)
        return dict_list, total

    @classmethod
    def get_cache_dict(cls, model: BaseModel, dependency_key,
                       where='', group_by='', order_by='', limit='', field="*", params=None,
                       expire_sec=10 * 60):
        redis_cli = RedisUtil()
        cache_key = f"{where}_{group_by}_{order_by}_{limit}_{field}_{params}_{model.model_obj.get_field_list()}"
        cache_key = CryptoHelper.md5_encrypt(cache_key.lower())
        cache_key = f"dict_{cache_key}"
        s = redis_cli.hget(dependency_key, cache_key)
        if s:
            return json.loads(s)

        dict_info = model.get_dict(where, group_by, order_by, limit, field, params)
        if not dict_info:
            return None

        redis_cli.hset(dependency_key, cache_key, JsonUtil.dumps(dict_info))
        redis_cli.expire(dependency_key, expire_sec)
        return dict_info

    @classmethod
    def get_cache_dict_by_id(cls, model: BaseModel, dependency_key,
                             primary_key_id,
                             expire_sec=10 * 60):
        redis_cli = RedisUtil()
        s = redis_cli.hget(dependency_key, primary_key_id)
        if s:
            return json.loads(s)

        dict_info = model.get_dict_by_id(primary_key_id)
        if not dict_info:
            return None

        redis_cli.hset(dependency_key, primary_key_id, JsonUtil.dumps(dict_info))
        redis_cli.expire(dependency_key, expire_sec)
        return dict_info

    @classmethod
    def get_cache_dict_by_id_new(cls, model: BaseModel, dependency_key,
                                 primary_key_id, field="*",
                                 expire_sec=10 * 60):
        redis_cli = RedisUtil()
        cache_key = f"{primary_key_id}_{field}_{model.model_obj.get_field_list()}"
        cache_key = CryptoHelper.md5_encrypt(cache_key.lower())
        cache_key = f"dict_by_id_{cache_key}"
        s = redis_cli.hget(dependency_key, cache_key)
        if s:
            return json.loads(s)

        dict_info = model.get_dict_by_id(primary_key_id, field)
        if not dict_info:
            return None

        redis_cli.hset(dependency_key, cache_key, JsonUtil.dumps(dict_info))
        redis_cli.expire(dependency_key, expire_sec)
        return dict_info

    @classmethod
    def get_cache_dict_list(cls, model: BaseModel, dependency_key,
                            where='', group_by='', order_by='', limit='', field="*", params=None,
                            expire_sec=10 * 60):
        redis_cli = RedisUtil()
        cache_key = f"{where}_{group_by}_{order_by}_{limit}_{field}_{params}_{model.model_obj.get_field_list()}"
        cache_key = CryptoHelper.md5_encrypt(cache_key.lower())
        cache_key = f"dict_list_{cache_key}"
        s = redis_cli.hget(dependency_key, cache_key)
        if s:
            return json.loads(s)

        dict_list = model.get_dict_list(where, group_by, order_by, limit, field, params)

        redis_cli.hset(dependency_key, cache_key, JsonUtil.dumps(dict_list))
        redis_cli.expire(dependency_key, expire_sec)
        return dict_list

    @classmethod
    def get_cache_dict_page_list(cls, model: BaseModel, dependency_key,
                                 field,
                                 page_index,
                                 page_size,
                                 where='',
                                 group_by='',
                                 order_by='',
                                 params=None,
                                 expire_sec=10 * 60):
        redis_cli = RedisUtil()
        cache_key = f"{field}_{page_index}_{page_size}_{where}_{group_by}_{order_by}_{params}_{model.model_obj.get_field_list()}"
        cache_key = CryptoHelper.md5_encrypt(cache_key.lower())
        cache_key = f"dict_page_list_{cache_key}"
        s = redis_cli.hget(dependency_key, cache_key)
        if s:
            value = json.loads(s)
            return value["dict_list"], value["total"]

        dict_list, total = model.get_dict_page_list(field, page_index, page_size, where, group_by, order_by, params)
        value = {"dict_list": dict_list, "total": total}

        redis_cli.hset(dependency_key, cache_key, JsonUtil.dumps(value))
        redis_cli.expire(dependency_key, expire_sec)
        return dict_list, total

    @classmethod
    def get_cache_total(cls, model: BaseModel, dependency_key,
                        where='', group_by='', field=None, params=None,
                        expire_sec=10 * 60):
        redis_cli = RedisUtil()
        cache_key = f"{where}_{group_by}_{field}_{params}_{model.model_obj.get_field_list()}"
        cache_key = CryptoHelper.md5_encrypt(cache_key.lower())
        cache_key = f"total_{cache_key}"
        s = redis_cli.hget(dependency_key, cache_key)
        if s:
            return int(json.loads(s))

        total = model.get_total(where, group_by, field, params)

        redis_cli.hset(dependency_key, cache_key, total)
        redis_cli.expire(dependency_key, expire_sec)
        return total

    @classmethod
    def delete_cache(cls, dependency_key):
        redis_cli = RedisUtil()
        redis_cli.delete(dependency_key)

    @classmethod
    def delete_cache_by_id(cls, dependency_key, primary_key_id):
        redis_cli = RedisUtil()
        redis_cli.hdel(dependency_key, primary_key_id)

    @classmethod
    def redis_init(self, db=None):
        """
        :description: redis初始化
        :return: redis_cli
        :last_editors: HuangJingCan
        """
        host = config.get_value("redis")["host"]
        port = config.get_value("redis")["port"]
        if not db:
            db = config.get_value("redis")["db"]
        password = config.get_value("redis")["password"]
        redis_cli = RedisHelper.redis_init(host, port, db, password)
        return redis_cli

    @classmethod
    def get_now_int(self, hours=0, fmt='%Y%m%d%H%M%S'):
        """
        :description: 获取整形的时间 格式为yyyyMMddHHmmss，如2009年12月27日9点10分10秒表示为20091227091010
        :param hours: 需要增加的小时数
        :param fmt: 时间格式
        :return:
        :last_editors: HuangJianYi
        """
        now_date = (datetime.datetime.now() + datetime.timedelta(hours=hours))
        return int(now_date.strftime(fmt))

    @classmethod
    def get_now_day_int(self, hours=0):
        """
        :description: 获取整形的天20200506
        :param hours: 需要增加的小时数
        :return: int（20200506）
        :last_editors: HuangJianYi
        """
        return self.get_now_int(fmt='%Y%m%d')

    @classmethod
    def get_now_datetime(self):
        """
        :description: 获取当前时间
        :return: str
        :last_editors: HuangJianYi
        """
        add_hours = config.get_value("add_hours", 0)
        return TimeHelper.add_hours_by_format_time(hour=add_hours)

    @classmethod
    def datetime_to_int(cls, dt, fmt='%Y%m%d%H%M%S'):
        return int(dt.strftime(fmt))

    @classmethod
    def base64_encode(cls, source, encoding="utf-8"):
        """
        :Description: base64加密
        :param source: 需加密的字符串
        :return: 加密后的字符串
        :last_editors: HuangJianYi
        """
        if not source.strip():
            return ""
        import base64
        encode_string = str(base64.b64encode(source.encode(encoding=encoding)), 'utf-8')
        return encode_string

    @classmethod
    def base64_decode(cls, source):
        """
        :Description: base64解密
        :param source: 需加密的字符串
        :return: 解密后的字符串
        :last_editors: HuangJianYi
        """
        if not source.strip():
            return ""
        import base64
        decode_string = str(base64.b64decode(source), 'utf-8')
        return decode_string

    @classmethod
    def emoji_base64_to_emoji(cls, text_string):
        """
        :description: 把加密后的表情还原
        :param text_string: 加密后的字符串
        :return: 解密后的表情字符串
        :last_editors: HuangJianYi
        """
        if not text_string:
            return ""

        results = re.findall('\[em_(.*?)\]', text_string)
        if results:
            for item in results:
                text_string = text_string.replace("[em_{0}]".format(item), cls.base64_decode(item))
        return text_string

    @classmethod
    def emoji_to_emoji_base64(cls, text_string):
        """
        :description: emoji表情转为[em_xxx]形式存于数据库,打包每一个emoji
        :description: 性能遇到问题时重新设计转换程序
        :param text_string: 未加密的字符串
        :return: 解密后的表情字符串
        """
        if not text_string:
            return ""

        try:
            co = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        results = co.findall(text_string)
        if results:
            for item in results:
                emoji_base64 = cls.base64_encode(item)
                text_string = text_string.replace(item, "[em_" + emoji_base64 + "]")
        return text_string

    @classmethod
    def long2short(cls, long_url):
        """
        长链接转短链接，公司接口，灿哥维护，地址中需要存在 gao7.com
        :param access_token:
        :return:
        {'ResultCode': '0', 'ResultMessage': '调用成功', 'Data': [{'ShortUrl': 'http://t.yinews.cn/QniAFv', 'IsNumberUrl': False}]}
        """
        url = f"http://t.yinews.cn/Create"
        params = {
            "url": long_url
        }

        response = HTTPHelper.get(url, params, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return {"ResultCode": '-1', "ResultMessage": "接口请求失败"}
