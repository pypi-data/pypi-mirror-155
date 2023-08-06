
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class EzgameUserStatisticsLogModel(BaseModel):
    def __init__(self, db_connect_key='db_platform', sub_table=None, db_transaction=None, context=None):
        super(EzgameUserStatisticsLogModel, self).__init__(EzgameUserStatisticsLog, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class EzgameUserStatisticsLog:

    def __init__(self):
        super(EzgameUserStatisticsLog, self).__init__()
        self.id = 0  # 自增id
        self.user_id = 0  # 玩家id
        self.auth_id = 0  # 第三方验证唯一id
        self.orm_id = 0  # 统计映射表id
        self.inc_value = 0  # 增加的值
        self.create_day = 0  # 创建日
        self.create_date = "1900-01-01 00:00:00"  # 创建时间

    @classmethod
    def get_field_list(self):
        return ['id', 'user_id', 'auth_id', 'orm_id', 'inc_value', 'create_day', 'create_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "ezgame_user_statistics_log_tb"
    