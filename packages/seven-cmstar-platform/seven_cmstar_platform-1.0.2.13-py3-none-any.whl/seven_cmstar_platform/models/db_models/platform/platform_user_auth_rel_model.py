
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class PlatformUserAuthRelModel(BaseModel):
    def __init__(self, db_connect_key='db_platform', sub_table=None, db_transaction=None, context=None):
        super(PlatformUserAuthRelModel, self).__init__(PlatformUserAuthRel, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class PlatformUserAuthRel:

    def __init__(self):
        super(PlatformUserAuthRel, self).__init__()
        self.id = 0  # 自增id
        self.auth_id = 0  # 第三方验证唯一id
        self.channel = 0  # 第三方平台标识，0NoSdk 1QQ小程序
        self.app_id = ""  # 第三方app_id
        self.user_id = 0  # 关联的玩家id
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间

    @classmethod
    def get_field_list(self):
        return ['id', 'auth_id', 'channel', 'app_id', 'user_id', 'create_date', 'modify_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "platform_user_auth_rel_tb"
    