# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-06-02 14:32:40
@LastEditTime: 2020-07-07 16:03:23
@LastEditors: HuangJingCan
@Description: 枚举类
"""

from enum import Enum, unique


class AppBaseRedisKeyType(Enum):
    """
    redis用到的key
    """
    QqAccessToken = "qq_access_token:"  # QQ accessToken
    QqAccessTokenLock = "qq_access_token_lock:"  # QQ accessToken
    WxAccessToken = "wx_access_token:"  # QQ accessToken
    WxAccessTokenLock = "wx_access_token_lock:"  # QQ accessToken
    UserToken = "pt_app_user_token:"
    ThirdToken = "pt_app_third_token:"
    UserRefreshToken = "pt_app_user_refresh_token:"
    ThirdRefreshToken = "pt_app_third_refresh_token:"
    InviteUserToken = "pt_invite_user_token"  # 用户邀请码
    InviteTokenUser = "pt_invite_token_user"  # 用户邀请码


class RedisKeyType(Enum):
    """
    redis用到的key
    """
    IdWorkKey = "pt_id_generator"  # ID生成器key值
    TelephoneCode = "pt_app_telephone_code:"  # 手机验证码
    PhoneCode = "pt_app_phone_code:"  # 手机验证码，新版
    TelephoneReq = "pt_app_telephone_req:"  # 手机验证码请求
    TelephoneLimit = "pt_app_telephone_limit:"  # 手机验证码请求限制
    SystemGiveDoll = "pt_system_give_doll"  # 系统赠送娃娃
    PtUserRemainTime = "pt_user_remain_time"  # 用户留存时间
    PtUserNotifyNum = "pt_user_notify_num"  # 用户通知数量

    BaseInfoCache = "pt_base_info_cache"  # 基础信息缓存
    AdConfigCache = "pt_ad_config_cache"  # 广告配置缓存
    PtDollConfigCache = "pt_doll_config_cache"  # 娃娃游戏配置信息缓存
    PtUserFansCache = "pt_user_fans_cache"  # 用户粉丝信息缓存
    PtUserFollowCache = "pt_user_follow_cache"  # 用户关注信息缓存
    PtProductCategory = "pt_product_category"  # 产品分类信息缓存
    PtSearchStatisticsLog = "pt_search_statistics_log"  # 查询统计信息缓存
    PtDictInfo = "pt_dict_info"  # 字典信息表
    PtClientVersion = "pt_client_version"  # 客户端更新信息缓存
    PtDollInfo = "pt_doll_info"  # 娃娃信息缓存

    PtDollIncr = "pt_doll_incr"  # 娃娃领取数量，迁移时需要同步数据
    PtDollClothIncr = "pt_doll_cloth_incr"  # 娃娃服饰领取数量，迁移时需要同步数据


class OperationType(Enum):
    """
    @description: 用户操作日志类型
    """
    add = 1
    update = 2
    delete = 3


class ThirdChannelType(Enum):
    """
    第三方登录类型
    """
    NoSdk = 0  # noSdk登录
    QqMini = 1  # QQ小程序登录
    WxMini = 2  # 微信小程序登录
    Phone = 3  # 手机号登录


class UnionChannelType(Enum):
    """
    开放平台类型
    """
    QqConnect = 1  # QQ互联


class AppChannelType(Enum):
    """
    应用类型
    """
    NoSdk = 0  # noSdk
    QqMini = 1  # QQ小程序
    WxMini = 2  # 微信小程序
    iOSApp = 3  # iOS应用
    AndroidApp = 4  # 安卓应用
    H5 = 5  # H5网页


class UserType(Enum):
    """
    用户类型
    """
    Client = 0  # C端用户
    Business = 1  # B端用户


class UserTagType(Enum):
    """
    玩家身份标签
    """
    DollOwner = 1  # 娃名
    DollSeller = 2  # 娃太
    DollPainter = 3  # 画手


class StatisticsOrmType(Enum):
    """
    数据统计
    """
    RegisterUser = 1  # 注册人数
    BindUser = 2  # 绑定手机人数
    BindUserLogin = 3  # 绑定手机号登录
    DollUserLogin = 4  # 有娃用户登录
    ActivateDoll = 5  # 激活娃娃
    InteractComplete = 6  # 互动完成
    StoryEnter = 7  # 体验剧情
    StoryBarrage = 8  # 剧情弹幕
    Talk = 9  # 吐槽
    GraspDoll = 10  # 提起娃娃
    TransferDoll = 11  # 转赠娃娃
    RemainTime = 12  # 停留时间

    ## 产房 1001开始
    FactoryApply = 1001  # 新增申请单
    FactoryOrder = 1002  # 新增订单

    ## 社区 2001开始
    ClubPost = 2001  # 新增动态
    ClubComment = 2002  # 新增评论
    ClubDig = 2003  # 新增点赞

    ## 游戏 3001开始


class UserStatisticsType(Enum):
    """
    用户统计
    """
    DollNum = 1  # 娃娃数量
    ClothNum = 2  # 娃衣数量
    PostNum = 3  # 帖子数量
    CommentNum = 4  # 评论数量，包括评论的评论
    ApplyNum = 5  # 申请单
    QuotationNum = 6  # 报价单
    OrderNum = 7  # 订单


class ActionLogType(Enum):
    """
    操作日志枚举
    """
    # 娃娃
    ActivateDoll = 10001  # 激活娃娃
    DollModifyNick = 10002  # 娃娃改名
    # DollTransfer = 10003  # 转赠成功

    # 互动
    DollInteractRequest = 20001  # 娃娃发起互动请求
    DollInteractResult = 20002  # 是否成功进行互动

    # 剧情
    StoryEnter = 30001  # 进入剧情详情界面
    StoryPass = 30002  # 剧情结局
    StoryBarrage = 30003  # 剧情留言
    StoryUnlock = 30004  # 剧情解锁

    # 玩家概要信息
    Talk = 40001  # 吐槽
    ChiefGetLevelReward = 40002  # 领取等级奖励

    # 用户
    UserFreeze = 50001  # 封号解封
    ModifyNick = 50002  # 修改昵称
    ModifyUserInfo = 50003  # 修改用户信息
    ModifyTelephone = 50004  # 更换手机号
    UserDelete = 50005  # 注销账号

    # 农场
    FarmUnlockField = 60001  # 解锁地块
    FarmAddBuilding = 60002  # 增加建筑
    FarmAddHarvest = 60003  # 收割作物
    FarmMergeBuilding = 60004  # 合并建筑
    FarmGetOrderReward = 60005  # 领取订单奖励
    FarmDeleteBuilding = 60006  # 删除建筑

    # 服饰
    ClothBuy = 70001  # 购买服饰
    ClothChipDecompose = 70002  # 碎片分解

    # 冒险
    AdventureSpeedUp = 80001  # 冒险加速
    AdventureGetRewards = 80002  # 领取奖励
    AdventureSentLostDoll = 80003  # 送走迷路的娃娃
    AdventureCharge = 80004  # 充能

    # 背包
    BagComposeChip = 90001  # 碎片合成

    # 任务
    TaskGetRewards = 100001  # 领取任务奖励

    # gm指令
    GmAddItem = 1000001  # 增加道具

    ## 游戏模块，从 2000001 开始


class DollGetType(Enum):
    """
    娃娃获得类型
    """
    Buy = 1  # 购买获得
    SystemGive = 2  # 系统赠送
    RankingReward = 3  # 新年副本排名奖励
    Transfer = 4  # 转让获得


class DollType(Enum):
    """
    娃娃类型
    """
    Forever = 1  # 永久
    TimeLimit = 2  # 限时


class NoticeMainType(Enum):
    """
    通知主类型
    """
    SystemNotice = 1  # 系统通知
    GameNotice = 2  # 游戏通知


class NoticeType(Enum):
    """
    通知类型
    """
    # 系统
    SystemNotice = 1  # 系统通知

    # 工厂订单
    FactoryOrderApply = 101  # 下单通知
    FactoryOrderQuote = 102  # 报价通知
    FactoryOrderProgress = 103  # 进度更新

    # 游戏
    PlantSteal = 201  # 偷菜通知


class UserNoticeNumType(Enum):
    """
    用户通知数量类型
    """
    ClubDigNum = 1001  # 社区点赞
    ClubCommentNum = 1002  # 社区评论数量


class AssetType(Enum):
    """
    资产类型
    """
    Count = 1  # 次数
    Integral = 2  # 积分
    Gear = 3  # 档位


class AssetSourceType(Enum):
    """
    来源类型
    """
    Buy = 1  # 商场购买
    Task = 2  # 任务
    GmModify = 3  # 手动配置
    Draw = 4  # 抽奖
    BuyBack = 5  # 回购
    Adventure = 6  # 娃娃冒险
    DollLvUp = 7  # 娃娃升级
    BuyCloth = 8  # 购买服饰
    BuyCancel = 9  # 商城购买取消，或超时

    ## 游戏，从 10001 开始


class DictInfoType(Enum):
    """
    字典信息类型
    """
    # 平台相关 10001 开始
    WorkWechatRobotUrl = 10001  # 企业微信机器人地址
    WorkWechatRobotMembers = 10002  # 通知用户列表，工号列表，逗号分隔
    UserDefaultAvatar = 10003  # 用户默认头像
    SystemNoticeAvatar = 10004  # 系统通知默认头像
    UserBackgroundUrl = 10005  # 用户默认背景图
    SearchKeyword = 10006  # 搜索关键词
    SystemNoticeName = 10007  # 系统通知默认名字

    # platform_api 20001 开始

    # game_api，30001 开始


class UserDeleteStatus(Enum):
    Normal = 1  # 正常
    Deleting = 2  # 注销中
    Deleted = 3  # 已注销
