
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class PlatformSearchStatisticsLogModel(BaseModel):
    def __init__(self, db_connect_key='db_platform', sub_table=None, db_transaction=None, context=None):
        super(PlatformSearchStatisticsLogModel, self).__init__(PlatformSearchStatisticsLog, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class PlatformSearchStatisticsLog:

    def __init__(self):
        super(PlatformSearchStatisticsLog, self).__init__()
        self.id = 0  # 自增id
        self.keyword_id = 0  # 搜索词md5加密转int
        self.keyword = ""  # 搜索词
        self.inc_value = 0  # 增加的值
        self.create_day = 0  # 创建日
        self.create_date = "1900-01-01 00:00:00"  # 创建时间

    @classmethod
    def get_field_list(self):
        return ['id', 'keyword_id', 'keyword', 'inc_value', 'create_day', 'create_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "platform_search_statistics_log_tb"
    