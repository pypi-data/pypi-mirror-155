
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class PlatformUserInfoModel(BaseModel):
    def __init__(self, db_connect_key='db_platform', sub_table=None, db_transaction=None, context=None):
        super(PlatformUserInfoModel, self).__init__(PlatformUserInfo, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class PlatformUserInfo:

    def __init__(self):
        super(PlatformUserInfo, self).__init__()
        self.id = 0  # 自增id
        self.user_id = 0  # 玩家唯一id
        self.telephone = ""  # 绑定的手机号
        self.user_nick = ""  # 用户昵称
        self.gender = 0  # 性别
        self.avatar = ""  # 头像
        self.sign = ""  # 用户签名
        self.inviter_id = 0  # 邀请者Id
        self.tags = ""  # 标签列表，1娃妈 2娃太 3画手
        self.qq = ""  # QQ号
        self.wechat = ""  # 微信号
        self.mail = ""  # 邮箱号
        self.birthday = ""  # 生日
        self.status = 0  # 状态，0正常 1冻结
        self.freeze_reason = ""  # 账号冻结原因
        self.freeze_type = 0  # 冻结类型，1-1天，2-1周，3-一月，4-一年，5-永久
        self.freeze_begin_date = "1900-01-01 00:00:00"  # 冻结开始时间
        self.freeze_end_date = "1900-01-01 00:00:00"  # 冻结结束时间
        self.register_channel = 0  # 注册渠道，第三方平台标识，1QQ小程序（字段废弃）
        self.app_channel = 0  # 注册时APP渠道标识，0：NoSdk 1：QQ小程序 2：微信小程序
        self.last_app_channel = 0  # 最近登录APP渠道标识，0：NoSdk 1：QQ小程序 2：微信小程序
        self.last_login_time = "1900-01-01 00:00:00"  # 上次登录时间
        self.check_fans_date = "1900-01-01 00:00:00"  # 上次查看粉丝时间
        self.del_status = 0  # 注销状态，0正常，1注销中，2已注销
        self.del_begin_at = 0  # 注销开始时间戳
        self.del_end_at = 0  # 注销完成时间戳
        self.im_status = 0  # IM状态，0未注册，1已注册
        self.user_type = 0  # 用户类型，0：普通用户，100：运营人员
        self.create_date = "1900-01-01 00:00:00"  # 创建时间，注册时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间
        self.modify_phone_date = "1900-01-01 00:00:00"  # 修改手机时间

    @classmethod
    def get_field_list(self):
        return ['id', 'user_id', 'telephone', 'user_nick', 'gender', 'avatar', 'sign', 'inviter_id', 'tags', 'qq', 'wechat', 'mail', 'birthday', 'status', 'freeze_reason', 'freeze_type', 'freeze_begin_date', 'freeze_end_date', 'register_channel', 'app_channel', 'last_app_channel', 'last_login_time', 'check_fans_date', 'del_status', 'del_begin_at', 'del_end_at', 'im_status', 'user_type', 'create_date', 'modify_date', 'modify_phone_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "platform_user_info_tb"
    