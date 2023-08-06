
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class PlatformUserAddressModel(BaseModel):
    def __init__(self, db_connect_key='db_platform', sub_table=None, db_transaction=None, context=None):
        super(PlatformUserAddressModel, self).__init__(PlatformUserAddress, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class PlatformUserAddress:

    def __init__(self):
        super(PlatformUserAddress, self).__init__()
        self.id = 0  # 自增id
        self.address_id = 0  # 地址唯一id
        self.user_id = 0  # 玩家唯一id
        self.user_nick = ""  # 收货人
        self.telephone = ""  # 手机号
        self.province_name = ""  # 省份
        self.city_name = ""  # 城市
        self.district_name = ""  # 区县
        self.address_info = ""  # 详细地址
        self.is_default = 0  # 是否默认，1是 0否
        self.is_del = 0  # 是否删除，1是 0否
        self.create_date = "1900-01-01 00:00:00"  # 创建时间，注册时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间

    @classmethod
    def get_field_list(self):
        return ['id', 'address_id', 'user_id', 'user_nick', 'telephone', 'province_name', 'city_name', 'district_name', 'address_info', 'is_default', 'is_del', 'create_date', 'modify_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "platform_user_address_tb"
    