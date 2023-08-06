
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class PlatformUserFollowModel(BaseModel):
    def __init__(self, db_connect_key='db_platform', sub_table=None, db_transaction=None, context=None):
        super(PlatformUserFollowModel, self).__init__(PlatformUserFollow, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class PlatformUserFollow:

    def __init__(self):
        super(PlatformUserFollow, self).__init__()
        self.id = 0  # 自增id
        self.user_id = 0  # 用户id
        self.followed_user_id = 0  # 关注的用户id
        self.user_type = 0  # 用户类型 1真实用户2随机马甲用户3官方马甲用户4普通马甲用户5特权用户
        self.followed_user_type = 0  # 关注的用户类型 1真实用户2随机马甲用户3官方马甲用户4普通马甲用户5特权用户
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间

    @classmethod
    def get_field_list(self):
        return ['id', 'user_id', 'followed_user_id', 'user_type', 'followed_user_type', 'create_date', 'modify_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "platform_user_follow_tb"
    