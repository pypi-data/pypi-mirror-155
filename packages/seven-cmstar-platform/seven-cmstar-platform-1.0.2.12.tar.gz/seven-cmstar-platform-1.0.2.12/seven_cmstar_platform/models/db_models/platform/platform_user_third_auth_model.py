
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class PlatformUserThirdAuthModel(BaseModel):
    def __init__(self, db_connect_key='db_platform', sub_table=None, db_transaction=None, context=None):
        super(PlatformUserThirdAuthModel, self).__init__(PlatformUserThirdAuth, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class PlatformUserThirdAuth:

    def __init__(self):
        super(PlatformUserThirdAuth, self).__init__()
        self.id = 0  # 自增id
        self.auth_id = 0  # 第三方验证唯一id
        self.channel = 0  # 第三方验证平台标识，0：NoSdk 1：QQ验证，2：微信验证
        self.app_id = ""  # 第三方app_id
        self.open_id = ""  # 第三方用户唯一标识
        self.union_channel = 0  # 开放平台标识，1：QQ互联
        self.union_id = ""  # 开放平台用户唯一标识符
        self.user_nick = ""  # 第三方用户昵称
        self.gender = 0  # 第三方用户性别，0：未知、1：男、2：女
        self.avatar = ""  # 第三方用户头像
        self.access_token = ""  # 第三方获取的access_token,校验使用
        self.app_channel = 0  # 注册时APP渠道标识，0：NoSdk 1：QQ小程序 2：微信小程序
        self.last_app_channel = 0  # 最近登录APP渠道标识，0：NoSdk 1：QQ小程序 2：微信小程序
        self.last_login_time = "1900-01-01 00:00:00"  # 上次登录时间
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间

    @classmethod
    def get_field_list(self):
        return ['id', 'auth_id', 'channel', 'app_id', 'open_id', 'union_channel', 'union_id', 'user_nick', 'gender', 'avatar', 'access_token', 'app_channel', 'last_app_channel', 'last_login_time', 'create_date', 'modify_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "platform_user_third_auth_tb"
    