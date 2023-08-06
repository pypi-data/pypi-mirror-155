
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class PlatformUserStatisticsModel(BaseModel):
    def __init__(self, db_connect_key='db_platform', sub_table=None, db_transaction=None, context=None):
        super(PlatformUserStatisticsModel, self).__init__(PlatformUserStatistics, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class PlatformUserStatistics:

    def __init__(self):
        super(PlatformUserStatistics, self).__init__()
        self.id = 0  # 自增id
        self.user_id = 0  # 玩家唯一id
        self.doll_num = 0  # 娃娃数
        self.cloth_num = 0  # 娃衣数
        self.post_num = 0  # 动态数
        self.comment_num = 0  # 评论数
        self.apply_num = 0  # 申请单
        self.quotation_num = 0  # 报价单
        self.order_num = 0  # 订单
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间

    @classmethod
    def get_field_list(self):
        return ['id', 'user_id', 'doll_num', 'cloth_num', 'post_num', 'comment_num', 'apply_num', 'quotation_num', 'order_num', 'create_date', 'modify_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "platform_user_statistics_tb"
    