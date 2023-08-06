
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class PlatformDictInfoModel(BaseModel):
    def __init__(self, db_connect_key='db_platform', sub_table=None, db_transaction=None, context=None):
        super(PlatformDictInfoModel, self).__init__(PlatformDictInfo, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class PlatformDictInfo:

    def __init__(self):
        super(PlatformDictInfo, self).__init__()
        self.id = 0  # 自增id
        self.dict_id = 0  # 字典唯一id
        self.dict_name = ""  # 字典名称
        self.dict_value = ""  # 字典值
        self.dict_text = ""  # 字典文本
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间

    @classmethod
    def get_field_list(self):
        return ['id', 'dict_id', 'dict_name', 'dict_value', 'dict_text', 'create_date', 'modify_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "platform_dict_info_tb"
    