
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class PlatformUserNoticeModel(BaseModel):
    def __init__(self, db_connect_key='db_platform', sub_table=None, db_transaction=None, context=None):
        super(PlatformUserNoticeModel, self).__init__(PlatformUserNotice, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class PlatformUserNotice:

    def __init__(self):
        super(PlatformUserNotice, self).__init__()
        self.id = 0  # 自增id
        self.notice_id = 0  # 通知唯一id
        self.user_id = 0  # 玩家唯一id
        self.type = 0  # 类型，1系统通知，2游戏通知
        self.notice_type = 0  # 通知类型，101下单通知 102报价通知 103进度更新
        self.description = ""  # 描述
        self.params = ""  # 自定义参数，订单id
        self.param_key = ""  # 参数key值，偷菜用
        self.param_value = ""  # 参数value值，偷菜用
        self.is_show = 0  # 是否展示过，1是 0否
        self.create_date = "1900-01-01 00:00:00"  # 创建时间，注册时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间

    @classmethod
    def get_field_list(self):
        return ['id', 'notice_id', 'user_id', 'type', 'notice_type', 'description', 'params', 'param_key', 'param_value', 'is_show', 'create_date', 'modify_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "platform_user_notice_tb"
    