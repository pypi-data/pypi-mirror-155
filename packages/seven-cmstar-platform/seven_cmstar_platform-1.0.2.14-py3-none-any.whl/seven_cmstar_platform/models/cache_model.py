# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/10/11 09:30
:LastEditTime: 2021/10/11 09:30
:LastEditors: SunYiTan
:Description: 
"""
import datetime

from seven_framework import TimeHelper, config
from seven_framework.base_model import BaseModel

from seven_cmstar_platform.utils.seven import SevenHelper


class CacheModel(BaseModel):

    def __init__(self, model_class, sub_table):
        """
        :Description: 数据缓存业务模型
        :param model_class: 实体对象类
        :param sub_table: 分表标识
        :last_editors: SunYiTan
        """
        super(CacheModel, self).__init__(model_class, sub_table)

    def get_format_time_list(self):
        """
        返回需要转换成日期格式的字段，继承类复写
        :return:
        """
        return ["create_date", "modify_date"]

    def get_cache_entity(self, dependency_key, where='', group_by='', order_by='', params=None, expire_sec=None):
        expire_sec = expire_sec if expire_sec else config.get_value("cache_expire_minute", 60) * 60
        return SevenHelper.get_cache_entity(self, dependency_key,
                                            where, group_by, order_by, params, expire_sec)

    def get_cache_entity_by_id(self, dependency_key, primary_key_id, expire_sec=None):
        expire_sec = expire_sec if expire_sec else config.get_value("cache_expire_minute", 60) * 60
        return SevenHelper.get_cache_entity_by_id(self, dependency_key, primary_key_id, expire_sec)

    def get_cache_list(self, dependency_key, where='', group_by='', order_by='', limit='', params=None,
                       expire_sec=None):
        expire_sec = expire_sec if expire_sec else config.get_value("cache_expire_minute", 60) * 60
        return SevenHelper.get_cache_list(self, dependency_key, where, group_by, order_by, limit, params, expire_sec)

    def get_cache_page_list(self, dependency_key,
                            field, page_index, page_size, where='', group_by='', order_by='', params=None,
                            expire_sec=None):
        expire_sec = expire_sec if expire_sec else config.get_value("cache_expire_minute", 60) * 60
        return SevenHelper.get_cache_page_list(self, dependency_key,
                                               field, page_index, page_size, where, group_by, order_by, params,
                                               expire_sec)

    def get_cache_dict(self, dependency_key, where='', group_by='', order_by='', limit='', field="*", params=None,
                       expire_sec=None):
        expire_sec = expire_sec if expire_sec else config.get_value("cache_expire_minute", 60) * 60
        dict_info = SevenHelper.get_cache_dict(self, dependency_key,
                                               where, group_by, order_by, limit, field, params, expire_sec)
        if dict_info:
            self.__format_time_to_datetime(dict_info)
        return dict_info

    def get_cache_dict_by_id(self, dependency_key, primary_key_id, field="*", expire_sec=None):
        expire_sec = expire_sec if expire_sec else config.get_value("cache_expire_minute", 60) * 60
        dict_info = SevenHelper.get_cache_dict_by_id_new(self, dependency_key, primary_key_id, field, expire_sec)
        if dict_info:
            self.__format_time_to_datetime(dict_info)
        return dict_info

    def get_cache_dict_list(self, dependency_key, where='', group_by='', order_by='', limit='', field="*", params=None,
                            expire_sec=None):
        expire_sec = expire_sec if expire_sec else config.get_value("cache_expire_minute", 60) * 60
        dict_list = SevenHelper.get_cache_dict_list(self, dependency_key,
                                                    where, group_by, order_by, limit, field, params, expire_sec)
        for dict_info in dict_list:
            self.__format_time_to_datetime(dict_info)
        return dict_list

    def get_cache_dict_page_list(self, dependency_key,
                                 field, page_index, page_size, where='', group_by='', order_by='', params=None,
                                 expire_sec=None):
        expire_sec = expire_sec if expire_sec else config.get_value("cache_expire_minute", 60) * 60
        dict_list, total = SevenHelper.get_cache_dict_page_list(
            self, dependency_key,
            field, page_index, page_size, where, group_by, order_by, params, expire_sec)
        for dict_info in dict_list:
            self.__format_time_to_datetime(dict_info)
        return dict_list, total

    def get_cache_total(self, dependency_key, where='', group_by='', field=None, params=None, expire_sec=None):
        expire_sec = expire_sec if expire_sec else config.get_value("cache_expire_minute", 60) * 60
        return SevenHelper.get_cache_total(self, dependency_key, where, group_by, field, params, expire_sec)

    def __format_time_to_datetime(self, dict_info):
        format_time_list = self.get_format_time_list()
        for key in format_time_list:
            if dict_info.__contains__(key) and not isinstance(dict_info[key], datetime.datetime):
                dict_info[key] = TimeHelper.format_time_to_datetime(dict_info[key])

    def delete_cache(self, dependency_key):
        """
        删除缓存
        :return:
        """
        SevenHelper.delete_cache(dependency_key)

    def add_entity_cache(self, model, dependency_key, ignore=False):
        self.delete_cache(dependency_key)
        new_id = super(CacheModel, self).add_entity(model, ignore)
        self.delete_cache(dependency_key)
        return new_id

    def update_entity_cache(self, model, dependency_key, field_list=None, exclude_field_list=None):
        self.delete_cache(dependency_key)
        super(CacheModel, self).update_entity(model, field_list, exclude_field_list)
        self.delete_cache(dependency_key)

    def update_table_cache(self, dependency_key, update_sql, where, params=None):
        self.delete_cache(dependency_key)
        super(CacheModel, self).update_table(update_sql, where, params)
        self.delete_cache(dependency_key)

    def del_entity_cache(self, dependency_key, where, params=None):
        self.delete_cache(dependency_key)
        super(CacheModel, self).del_entity(where, params)
        self.delete_cache(dependency_key)
