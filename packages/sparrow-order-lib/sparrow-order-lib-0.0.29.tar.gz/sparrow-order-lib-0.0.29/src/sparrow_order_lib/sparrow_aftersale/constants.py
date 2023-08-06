from ..core.datastructures import ImmutableList


class Aftersale_Number_Refund_Status(object):
    # 退单子退款状态(init初始/doing进行中/done已完成)
    INIT = "init"
    DOING = "doing"
    DONE = "done"
    FAILED = "failed"
    AFTERSALE_NUMBER_REFUND_STATUS_CHOICES = (
        (INIT, '初始'),
        (DOING, '进行中'),
        (DONE, "已完成"),
        (FAILED, "失败"),

    )
    AFTERSALE_NUMBER_REFUND_STATUS_DICT = dict(AFTERSALE_NUMBER_REFUND_STATUS_CHOICES)


class WechatDeliveryReturnStatus:
    """ 用户寄回时的方式 """
    INIT = 0  # 用户未填写退货信息
    APPLY = 1  # 在线预约
    SELF = 2  # 自主填写


class WechatDeliveryReturnOrderStatus:
    """ 退单状态 """
    INIT = 0  # 已下单, 待揽收
    PACKAGED = 1  # 已揽件
    TRANSIT = 2  # 运输中
    DELIVERING = 3  # 派件中
    SELF_SIGNED = 4  # 已签收
    ABNORMAL = 5  # 异常
    PRE_SIGNED = 6  # 代签收
    FAIL_PACKAGED = 7  # 揽件失败
    FAIL_SIGNED = 8  # 签收失败(拒签、超区)
    CANCEL = 11  # 已取消
    RETURNING = 13  # 退件中
    RETURNED = 14  # 已退件
    UNHEARD = 99  # 未知

    # 非终态退单状态
    UNTERMINATE_ORDER_TYPE_LIST = ImmutableList(
        [INIT, PACKAGED, TRANSIT, DELIVERING, RETURNING, UNHEARD]
    )


######### 以下内容来自 constant_event.py ##########
class EventMapKey(object):

    TO_STATUS_KEY = "to_status"
    USER_ROLES_KEY = "user_roles"


class AfsNumberRefundEventConst(object):
    ### 子退单事件 ###
    # 子退单开始申请退
    START = "start"
    # 子退单完成
    SUCCESS = "success"
    # 子退单失败
    FAIL = "fail"

    EVENT_2_BUTTONNAME_MAP = {
        START: "子退单开始申请退",
        SUCCESS: "子退单完成",
        FAIL: "子退单失败"
    }

    FROM_TO_MAP = {
        START: {  # 子退单开始申请退
            Aftersale_Number_Refund_Status.INIT: {
                EventMapKey.TO_STATUS_KEY: Aftersale_Number_Refund_Status.DOING,
                EventMapKey.USER_ROLES_KEY: None
            }
        },
        SUCCESS: {  # 子退单完成
            Aftersale_Number_Refund_Status.DOING: {
                EventMapKey.TO_STATUS_KEY: Aftersale_Number_Refund_Status.DONE,
                EventMapKey.USER_ROLES_KEY: None
            },
            Aftersale_Number_Refund_Status.FAILED: {
                EventMapKey.TO_STATUS_KEY: Aftersale_Number_Refund_Status.DONE,
                EventMapKey.USER_ROLES_KEY: None
            },
        },
        FAIL: {  # 子退单失败
            Aftersale_Number_Refund_Status.DOING: {
                EventMapKey.TO_STATUS_KEY: Aftersale_Number_Refund_Status.FAILED,
                EventMapKey.USER_ROLES_KEY: None
            },
            Aftersale_Number_Refund_Status.FAILED: {
                EventMapKey.TO_STATUS_KEY: Aftersale_Number_Refund_Status.FAILED,
                EventMapKey.USER_ROLES_KEY: None
            }
        }
    }


class AfsLineGenerateFrom:
    SELECT = 'select'  # 创建售后时选中的
    VIRTUAL = 'virtual'  # 虚拟订单数据
    ORIGIN = 'origin'  # 创建售后前的订单(或虚拟订单)数据

    CHOICES = (
        (SELECT, "创建售后时选择的商品"),
        (VIRTUAL, "虚拟订单数据"),
        (ORIGIN, "创建售后前的订单(或虚拟订单)数据"),
    )


class AfsVersionConst:
    V2 = "V2"
    V3 = "V3"
