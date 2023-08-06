
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class PlatformBaseInfoModel(BaseModel):
    def __init__(self, db_connect_key='db_platform', sub_table=None, db_transaction=None, context=None):
        super(PlatformBaseInfoModel, self).__init__(PlatformBaseInfo, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class PlatformBaseInfo:

    def __init__(self):
        super(PlatformBaseInfo, self).__init__()
        self.id = 0  # 自增id
        self.about_us = ""  # 关于我们
        self.customer_qq = ""  # 客服QQ
        self.customer_wechat = ""  # 客服微信
        self.novice_tid = 0  # 新手娃妈必看攻略话题id
        self.apply_course_tid = 0  # "如何提交【有效】咨询单"帖子话题id
        self.apply_course_pid = 0  # "如何提交【有效】咨询单"帖子id
        self.create_date = "1900-01-01 00:00:00"  # 创建时间，注册时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间

    @classmethod
    def get_field_list(self):
        return ['id', 'about_us', 'customer_qq', 'customer_wechat', 'novice_tid', 'apply_course_tid', 'apply_course_pid', 'create_date', 'modify_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "platform_base_info_tb"
    