

class MemberLevel(object):
    '''会员级别'''
    MEMBER_ALL = "ALL"
    MEMBER_L1 = 'MEMBER_L1'  # 银卡会员
    MEMBER_L2 = "MEMBER_L2"  # 金卡会员
    MEMBER_L0 = "MEMBER_L0"  # 普卡会员


class PayType(object):
    '''支付类型'''
    CASH = "1"
    CHECK = "2"
    HG_DISCOUNT = "4"
    WECHAT = "17"
    ALIPAY = "18"
    C_COUPON = "13"
    A_COUPON = "10"
    D_COUPON = "15"
    GIFT_COUPON = "16"
    # 待拆分的
    TO_SPLIT = "888"
    # 待被决定的
    TO_PAY = "999"
    # 现金类支付方式
    CASH_PAY_TYPE_VALUE = ("1", "17", "18", "2")
    # 现金类支付choise
    CASH_PAY_TYPE_CHOICE = (
        (WECHAT, "微信支付"),
        (ALIPAY, "支付宝支付"),
    )
    PAYMENT_TYPE_CHOICES = (
        (CASH, "现金"),
        (WECHAT, "微信支付"),
        (ALIPAY, "支付宝支付"),
        (A_COUPON, "A券"),
        (C_COUPON, "C券"),
        (D_COUPON, "钱包"),
        (GIFT_COUPON, "礼券"),
        (TO_SPLIT, "待拆分"),
        (TO_PAY, "待支付"),
    )


class PaymentPayer(object):
    '''费用承担方'''
    HG = "HG"  # 汉光
    SHOP = "SHOP"  # 专柜
    BAISHI = "baishi"  # 百世

    PAYER_CHOICES = (
        (HG, "汉光"),
        (SHOP, "专柜"),
        (BAISHI, "百世"),
    )


class LogLevel(object):
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    SYSTEM = 'system'


class ShippingPartnerCodes(object):
    '''ExpressPartner里面要用到的code'''
    # 顺丰
    SF = "sf"
    # 顺丰同城急送
    SFTCJS = "sftcjs"
    # 圆通
    YTO = "yto"
    # 中通
    ZTO = "zto"
    # 申通
    STO = "sto"
    # EMS
    EMS = "ems"
    # 邮政
    YZPY = "yzpy"
    # 韵达
    YD = "yd"
    # 宅急送
    ZJS = "zjs"
    # 京东
    JD = "jd"
    # 德邦
    DBL = "dbl"
    # 百世快递
    HTKY = "htky"
    # 天天
    HHTT = "hhtt"
    # 其它
    OTHERS = "others"
    # 专柜代发
    SHOP = "shop"
    # 闪送
    SS = "ss"


# 快递公司代号与中文对照
ShippingPartnerCodes_DICT = {
    ShippingPartnerCodes.SF: "顺丰",
    ShippingPartnerCodes.SFTCJS: "顺丰同城急送",
    ShippingPartnerCodes.YTO: "圆通",
    ShippingPartnerCodes.ZTO: "中通",
    ShippingPartnerCodes.STO: "申通",
    ShippingPartnerCodes.EMS: "EMS",
    ShippingPartnerCodes.YZPY: "邮政",
    ShippingPartnerCodes.YD: "韵达",
    ShippingPartnerCodes.ZJS: "宅急送",
    ShippingPartnerCodes.JD: "京东",
    ShippingPartnerCodes.DBL: "德邦",
    ShippingPartnerCodes.HTKY: "百世快递",
    ShippingPartnerCodes.HHTT: "天天",
    ShippingPartnerCodes.OTHERS: "其它",
    ShippingPartnerCodes.SHOP: "专柜代发",
    ShippingPartnerCodes.SS: "闪送",
}


class UserRole(object):
    '''
    ### 用户角色 ###
    '''
    # 客户
    CUSTOMER = "customer"
    # 客服
    CUSSERVICE = "cusservice"
    # 导购
    GUIDE = "guide"
    # 麻雀自动
    AUTO = "auto"
    # 高级客服
    SUPER_CUSSERVICE = "supercusservice"
    # 楼层
    LOUCENG = "louceng"
    # 开发
    DEV = "dev"

    USERROLE_CHOICES = (
        (CUSTOMER, "客户"),
        (CUSSERVICE, "客服"),
        (GUIDE, "导购"),
        (AUTO, "麻雀自动"),
        (SUPER_CUSSERVICE, "高级客服"),
        (LOUCENG, "楼层"),
        (DEV, "开发"),
    )
    USERROLE_DICT = dict(USERROLE_CHOICES)

    # 扶摇上权限管理角色 role_code 和 常量 role 的对应关系
    ROLE_CODE_2_ROLE = {
        'dev': DEV,
        's_customer': SUPER_CUSSERVICE,
        'j_customer': CUSSERVICE,
        'louceng': LOUCENG,
        'guide': GUIDE
    }
    # 扶摇上权限管理角色的权重顺序, 从高到低
    ROLE_WEIGHT = ['dev', 's_customer', 'j_customer', 'louceng', 'guide']
