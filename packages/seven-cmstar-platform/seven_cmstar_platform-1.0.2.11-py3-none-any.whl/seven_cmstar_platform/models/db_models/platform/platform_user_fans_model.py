
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class PlatformUserFansModel(BaseModel):
    def __init__(self, db_connect_key='db_platform', sub_table=None, db_transaction=None, context=None):
        super(PlatformUserFansModel, self).__init__(PlatformUserFans, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class PlatformUserFans:

    def __init__(self):
        super(PlatformUserFans, self).__init__()
        self.id = 0  # 自增id
        self.user_id = 0  # 用户id
        self.fans_user_id = 0  # 粉丝用户id
        self.user_type = 0  # 用户类型 1真实用户2随机马甲用户3官方马甲用户4普通马甲用户5特权用户
        self.fans_user_type = 0  # 粉丝用户类型 1真实用户2随机马甲用户3官方马甲用户4普通马甲用户5特权用户
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间
        self.is_new = 0  # 是否是新增关注，1是 0否

    @classmethod
    def get_field_list(self):
        return ['id', 'user_id', 'fans_user_id', 'user_type', 'fans_user_type', 'create_date', 'modify_date', 'is_new']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "platform_user_fans_tb"
    