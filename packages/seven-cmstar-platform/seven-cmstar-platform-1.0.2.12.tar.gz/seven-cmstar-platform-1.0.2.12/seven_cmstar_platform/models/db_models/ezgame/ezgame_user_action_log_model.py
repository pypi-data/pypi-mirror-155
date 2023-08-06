
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class EzgameUserActionLogModel(BaseModel):
    def __init__(self, db_connect_key='db_platform', sub_table=None, db_transaction=None, context=None):
        super(EzgameUserActionLogModel, self).__init__(EzgameUserActionLog, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class EzgameUserActionLog:

    def __init__(self):
        super(EzgameUserActionLog, self).__init__()
        self.id = 0  # 自增id
        self.user_id = 0  # 玩家id
        self.action_id = 0  # 操作id
        self.doll_id = 0  # 玩家id
        self.parama = ""  # parama
        self.paramb = ""  # paramb
        self.paramc = ""  # paramc
        self.paramd = ""  # paramd
        self.create_date = "1900-01-01 00:00:00"  # 创建时间

    @classmethod
    def get_field_list(self):
        return ['id', 'user_id', 'action_id', 'doll_id', 'parama', 'paramb', 'paramc', 'paramd', 'create_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "ezgame_user_action_log_tb"
    