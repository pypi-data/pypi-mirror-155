
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class PlatformDollInfoModel(BaseModel):
    def __init__(self, db_connect_key='db_platform', sub_table=None, db_transaction=None, context=None):
        super(PlatformDollInfoModel, self).__init__(PlatformDollInfo, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class PlatformDollInfo:

    def __init__(self):
        super(PlatformDollInfo, self).__init__()
        self.id = 0  # 自增id
        self.doll_id = 0  # 娃娃唯一id
        self.doll_code = ""  # 娃娃编号
        self.cdk = ""  # 对应的激活码
        self.order_id = 0  # 订单唯一id
        self.market_order_id = 0  # 商城订单id
        self.market_order_goods_id = 0  # 商城订单商品id
        self.goods_id = 0  # 娃类唯一id
        self.goods_code = ""  # 娃类编码
        self.seller_id = 0  # 卖家唯一id
        self.doll_nick = ""  # 娃娃昵称
        self.gender = 0  # 性别
        self.height = ""  # 娃娃身高
        self.telephone = ""  # 绑定的手机号
        self.qq = ""  # 绑定的QQ号
        self.birth_date = "1900-01-01 00:00:00"  # 出生时间
        self.activate_date = "1900-01-01 00:00:00"  # 激活时间
        self.activate_user_id = 0  # 激活的玩家id
        self.user_id = 0  # 拥有的玩家id，娃妈id
        self.get_type = 0  # 获得类型，1购买获得，2系统赠送，3奖励获得，4转让获得
        self.got_cloth = 0  # 是否已经领取过服饰
        self.activate_sort = 0  # 激活序号
        self.doll_type = 0  # 娃娃类型，1永久，2限时
        self.is_equipped_cloth = 0  # 是否穿戴衣服
        self.cms_user_id = ""  # 操作用户id
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间
        self.expire_date = "1900-01-01 00:00:00"  # 过期时间

    @classmethod
    def get_field_list(self):
        return ['id', 'doll_id', 'doll_code', 'cdk', 'order_id', 'market_order_id', 'market_order_goods_id', 'goods_id', 'goods_code', 'seller_id', 'doll_nick', 'gender', 'height', 'telephone', 'qq', 'birth_date', 'activate_date', 'activate_user_id', 'user_id', 'get_type', 'got_cloth', 'activate_sort', 'doll_type', 'is_equipped_cloth', 'cms_user_id', 'create_date', 'modify_date', 'expire_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "platform_doll_info_tb"
    