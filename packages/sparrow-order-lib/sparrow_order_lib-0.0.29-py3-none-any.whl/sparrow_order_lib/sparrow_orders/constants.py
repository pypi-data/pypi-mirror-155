# 这些常量会在其他地方被用到，用作某些判断


class ReversedStockStatus(object):
    # 默认状态
    INIT = "init"
    # 缺货
    SHORTAGE = "shortage"
    # 无货需要下架
    OFF = "off"
    # 备好货
    PREPARED = "prepared"


class ReversedStockType(object):
    PRODUCT = "product"
    GIFT = "gift"


class ReversedStockActions(object):
    # 导购标记货品
    GUIDE_MARK = "guide_mark"
    # 客服取货
    PICK_UP = "pick_up"
    # 客服还货
    RETURN = "return"


class ReversedStockNoteMessage(object):
    GUIDE_MARK = '标记货品状态为{0}'
    PICK_UP = '客服提货'
    RETURN = '客服还货'


class RequiredCountStock(object):
    IS_STOCK = "is_stock"
    IS_REQUIRED_COUNT = "is_required_count"
    IS_ANY = "is_any"


class AftersaleActions(object):
    # 创建售后单
    CREATE = "create"
    # 修改售后单
    UPDATE = "update"
    # 关闭售后单
    REMOVE = "remove"
    # 完成售后单
    COMPLETE = "complete"
    # 客服审核通过
    OPERATOR_APPROVE = "operator_approve"
    # 财务审核通过
    FINANCE_APPROVE_1ST = "finance_approve_1st"
    # 财务审核通过
    FINANCE_APPROVE = "finance_approve"
    # 财务驳回
    FINANCE_REJECT = "finance_reject"
    # 店内系统驳回
    INSTORE_REJECT = "instore_reject"
    # 店内通过
    ALL_APPROVE = "all_approve"
    # 退款失败
    REFUND_FAIL = "refund_fail"
    # 开始退款
    START_REFUND = "start_refund"
    # 退款成功
    REFUND_SUCCEED = "refund_succeed"
    # 待退货
    PENDING_RETURN = "pending_return"
    # 待退款
    PENDING_REFUND = "pending_refund"
    # 直接退款
    REFUND_DIRECTLY = "pending_directly"
    # 自动
    AUTO = "auto"
    # 确认已经退货
    CONFIRM_RETURNED = "confirm_returned"
    # 客户回填运单信息
    CUSTOMER_WRITEBACK_EXPRESS = "customer_writeback_express"
    # 拦截失败
    BLOCK_FAILED = "block_failed"
    # 客服修改运单信息
    CUSSERVICE_MODIFY_EXPRESS = "cusservice_modify_express"


class AssignmentActions(object):
    # 创建配货
    CREATE = "create"
    # 关闭配货
    REMOVE = "remove"
    # 完成配货
    COMPLETE = "complete"
    # 已打印
    PRINTED = "printed"


class OrderActions(object):
    # 售后单独有一个Note表
    # 负库存相关单独有一个Note表
    # 修改
    MODIFY_ADDRESS = "modify_address"
    # 修改客服备注
    MODIFY_OPERATOR_NOTE = "modify_operator_note"
    # 关闭订单
    CLOSE = "close"
    # 发起支付
    PAY = "pay"
    # 完成支付订单
    COMPLETE_PAYMENT = "complete_payment"
    # 发货
    SEND = "send"
    # 用户提货
    TAKE = "take"
    # 其他
    OTHERS = "others"
    # 创建订单
    CREATE = "create"
    # 生成发货单
    GENERATE_DISTRIBUTE = "generate_distribute"
    # 给客户发短信
    SEND_SMS_MESSAGE = "send_sms_message"


class OrderTypes(object):
    # 线上订单
    ONLINE = "online"
    # 闪购
    FLASHSALE = "flashsale"
    # 贩卖机类型，现场直接出货
    VENDING = "vending"
    # 贩卖机类型，现场直接出货： 样机种草
    VENDING_MACHINE_HR = "vending_machine_hr"
    # 互动触摸屏类型，提货需要到专柜
    SCREEN = "screen"
    # rfid 订单类型
    RFID = "rfid"
    # 拼团订单
    GROUP = "group"
    # 积分商城
    POINTS_MALL = "points_mall"
    # 汉光贩售机
    HGVENDING = "hgvending"
    # 海淘
    HAITAO = "haitao"

    ORDER_TYPES_CHOICES = (
        (ONLINE, "线上订单"),
        (FLASHSALE, "闪购订单"),
        (VENDING, "售货机自提"),
        (VENDING_MACHINE_HR, "样机种草"),
        (SCREEN, "互动触摸屏"),
        (RFID, "RFID"),
        (GROUP, "拼团订单"),
        (HGVENDING, "汉光贩售机"),
        (HAITAO, "海淘"),
    )


class OrderShippingMethods(object):

    SELF_SERVICE = "self_service"
    EXPRESS = "express"


class OrderStatus(object):
    """订单对外展示状态"""
    # 2018-02-08 确定新的四个统一订单对外状态
    # 待付款
    UNPAID = "unpaid"
    # 准备中
    PREPARING = "preparing"
    # 可提货，待发货
    TO_DELIVER = "to_deliver"
    # 已发货，已完成
    COMPLETED = "completed"
    # 已关闭/取消
    CLOSED = "closed"
    # 订单不再筛选售后状态！

    # 售后
    AFTERSALE = "after_sale"
    # 待发货
    TO_SHIP = "to_ship"
    # 可自提
    TO_PICKUP = "to_pickup"

    # 待付款
    # UNPAID = "unpaid"
    # # 备货中
    # IN_PREPARING = "in_preparing"
    # # 待发货
    # TO_SEND = "to_send"
    # # 待提货
    # TO_TAKE = "to_take"
    # # 部分发货
    # PARTIALLY_SENT = "partially_sent"
    # # 已发货
    # SENT = "sent"
    # # 部分提货
    # PARTIALLY_TAKEN = "partially_taken"
    # # 已提货
    # TAKEN = "taken"
    # # 退换/售后
    # IN_AFTERSALE = "in_aftersale"
    # # 已关闭/取消
    # CLOSED = "closed"


class OrderPayStatus(object):
    # 订单支付状态
    UNPAID = "unpaid"
    PAY_FINISHED = "pay_finished"
    CLOSED = "closed"
    # ------------- 分阶段支付 --------------
    # 定金待支付
    TO_DEPOSITPAY = "to_depositpay"
    # 尾款待支付
    TO_TAILPAY = "to_tailpay"
    # 尾款超时
    TAILPAY_OVERTIME = "tailpay_overtime"

    ORDER_PAY_STATUS_CHOICE = (
        (UNPAID, "未支付"),
        (PAY_FINISHED, "支付完成"),
        (CLOSED, "已关闭"),
        (TO_DEPOSITPAY, "待支付定金"),
        (TO_TAILPAY, "待支付尾款"),
        (TAILPAY_OVERTIME, "尾款超时"),
    )
    ORDER_PAY_STATUS_DICT = dict(ORDER_PAY_STATUS_CHOICE)


class OrderGroupStatus(object):
    # 拼团中
    PROGRESS = "progress"
    # 已成团
    SUCCESS = "success"
    # 拼团失败
    FAIL = "fail"


class OrderAssignStatus(object):
    '''订单配货状态'''
    # 无配货 - 没有ready或completed的发货单，或者说没有发货单或发货单只有closed的
    INIT = "init"
    # 部分配货 - 有ready的发货单，但是ready的发货单里的line的总数总量不全
    PARTIAL = "partial"
    # 全部配货 - 有不是closed的发货单，全部发货单里全部line数量总量和订单一致
    COMPLETED = "completed"


class OrderShippingStatus(object):
    '''订单发货状态'''
    # 未发货 - 没有completed的发货单
    INIT = "init"
    # 部分发货 - 有completed的发货单，里面的line总量不全
    PARTIAL = "partial"
    # 全部发货 - completed的发货单里面的line总量和订单一致
    COMPLETED = "completed"


class OrderAftersaleStatus(object):
    # 订单售后状态
    # 有待处理售后
    OPEN = "open"
    # 无售后
    NONE = "none"
    # 售后都完成（因为同时open的售后单只会有一单）
    DONE = "done"


class OrderExchangeStatus(object):
    '''### 订单换货状态###'''
    # 有待处理售后
    OPEN = "open"
    # 无售后
    NONE = "none"
    # 换货都完成（因为同时open的换货单只会有一单）
    DONE = "done"
    # 配货状态
    EXCHANGE_STATUS = (
        (OPEN, "有在进行的换货"),
        (NONE, "无换货"),
        (DONE, "换货已完成"),
    )


class AftersaleStatus(object):

    # 财务待审
    IN_FINANCE = "in_finance"
    # 财务一审通过，待二审
    IN_FINANCE_2ND = "in_finance_2nd"
    # 财务驳回
    REJECTED = "rejected"
    # 店内通过的售后单状态们
    # AFTER_APPROVES = [ALL_APPROVED, REFUND_FAILED, COMPLETED]
    # IN_OPENS = [OPEN, IN_FINANCE, IN_FINANCE_2ND, REJECTED, INSTORE_REJECTED]
    ######  以上为需求v190611之前的状态，现在不用了,但必须保留做兼容#########

    # 待审核/审核中
    OPEN = "open"
    # 待退货
    PENDING_RETURN = "pending_return"
    PENDING_RETURN_0 = "pending_return_0"  # For C端， 待客服退货，此状态，在数据库中并不存在
    PENDING_RETURN_1 = "pending_return_1"  # For C端， 待客人退货，此状态，在数据库中并不存在
    PENDING_RETURN_2 = "pending_return_2"  # For C端， 待外仓退货，此状态，在数据库中并不存在
    # 待退款
    PENDING_REFUND = "pending_refund"
    # 店内系统通过
    INSTORE_APPROVED = "instore_approved"
    # 店内系统驳回
    INSTORE_REJECTED = "instore_rejected"
    # 已完成主流程，不涉及退款 —— 这是一个中间状态，退款的时候用来校验
    # 这里店内系统也已经记录了，绝对不能改了。如果退款失败了只能单独和用户沟通或者店内系统也得改
    # 只有是这个状态才能发起退款
    ALL_APPROVED = "all_approved"

    # 退款失败
    REFUND_FAILED = "refund_failed"
    # 已完成
    COMPLETED = "completed"
    # 已取消，已关闭
    CLOSED = "closed"

    AFTERSALE_STATUS_CHOICES = (
        (OPEN, "待审核"),
        # (IN_FINANCE, "财务待审"),
        # (IN_FINANCE_2ND, "财务一审通过"),
        # (REJECTED, "财务驳回"),
        (PENDING_RETURN, "待退货"),
        (PENDING_REFUND, "待退款"),
        (INSTORE_APPROVED, "店内系统通过"),
        (INSTORE_REJECTED, "店内系统驳回"),
        (ALL_APPROVED, "店内系统通过"),
        (REFUND_FAILED, "退款失败"),
        (COMPLETED, "已完成"),
        (CLOSED, "已取消"),
    )
    AFTERSALE_STATUS_CHOICES_FOR_C = (
        (OPEN, "待审核"),
        (PENDING_RETURN_0, "待审核"),  # 待客服退货
        (PENDING_RETURN_1, "待退货"),  # 待客人退货
        (PENDING_RETURN_2, "待退货"),  # 发货拦截中
        (PENDING_REFUND, "待退款"),
        (INSTORE_APPROVED, "待退款"),
        (INSTORE_REJECTED, "待退款"),
        (ALL_APPROVED, "待退款"),
        (REFUND_FAILED, "待退款"),
        (COMPLETED, "已完成"),
        (CLOSED, "已关闭"),
    )
    AFTERSALE_MESSAGE_DICT_FOR_C = {
        # OPEN: ["您的退换货申请已提交，等待客服审核，请保持电话畅通。"],
        OPEN: ["您的售后已申请成功，待售后审核中"],
        # PENDING_RETURN_0: ["您的售后正在审核中，请耐心等待。"],
        PENDING_RETURN_0: ["您的售后审核已通过，待售后中心收退货"],
        # PENDING_RETURN_1: ["您的售后已审核通过，请将售后商品邮寄到指定地址并填写物流单号，查看退货地址"],
        PENDING_RETURN_1: ["您的售后审核已通过，待售后中心收退货"],
        # PENDING_RETURN_2: ["正在为您尝试拦截中，请耐心等待。"],
        PENDING_RETURN_2: ["您的售后审核已通过，待售后中心收退货"],
        # PENDING_REFUND: ["客服正在为您处理退款。"],
        PENDING_REFUND: ["您的售后待客服处理退款"],
        # INSTORE_APPROVED: ["客服正在为您处理退款。"],
        INSTORE_APPROVED: ["您的售后待客服处理退款"],
        # INSTORE_REJECTED: ["客服正在为您处理退款。"],
        INSTORE_REJECTED: ["您的售后待客服处理退款"],
        # ALL_APPROVED: ["客服正在为您处理退款。"],
        ALL_APPROVED: ["您的售后待客服处理退款"],
        # REFUND_FAILED: ["客服正在为您处理退款。"],
        REFUND_FAILED: ["您的售后待客服处理退款"],
        # COMPLETED: ["售后已完成，退款金额将原路返回到您的帐户，预计最晚到账1-7个工作日，请您注意查收。"],
        COMPLETED: ["售后服务已完成，感谢您对汉光的支持"],
        CLOSED: ["售后已关闭。"],
    }


class AftersaleFinanceStatus(object):
    # 未审核
    INIT = "init"
    # 一审通过
    APPROVED_1ST = "approved_1st"
    # 二审通过
    APPROVED = "approved"
    # 财务驳回
    REJECTED = "rejected"


class AftersaleFinanceType(object):
    '''一期有一些需要财务手动调账的'''
    # 普普通通的售后单
    AUTO = "auto"
    # 需要财务手动调账的售后单，微信不能自动退款
    MANUAL = "manual"


class CancelSource(object):
    """
    售后取消来源
    """
    # 客人取消
    GUEST_CANCEL = "guest_cancel"
    # 客服取消
    SERVICE_CANCEL = "service_cancel"
    # 高级客服取消
    SUPER_SERVICE_CANCEL = "super_service_cancel"
    # 超时自动取消
    TIMEOUT_CANCEL = "timeout_cancel"


class RefundStatus(object):
    # 未退款，初始状态
    INIT = "init"
    # 退款成功
    SUCCEEDED = "succeeded"
    # 退款失败
    FAILED = "failed"


class CouponSource(object):
    # 线上发的券
    ONLINE = "online"
    # 店内发的券
    IN_STORE = "store"


class ProductSaleType(object):
    # 实物类型
    REAL = "REAL"

    # 虚拟商品
    VIRTUAL = "VIRTUAL"


class SettingsLabel(object):
    """
    系统配置
    """
    # 客服主管拦截
    SUPERVISOR_INTERCEPTION = "supervisor_interception"


class InnerApiUri(object):
    ALIPAY = "/api/sparrow_alipay/i/alipay_aftersale_returned/"
    REFUND_QUERY = "/api/sparrow_alipay/i/alipay_aftersale_returned_query/"
    PRODUCT = "/api/sparrow_products_i/pure_products/{}/"


class ErrorCode(object):
    SUCCESS = 0  # 成功
    FLASH_HAS_PICKUP = 201001  # 闪购订单已提货，不能发起退单。
    HAS_VALID_AFTERSALE = 201002  # 此订单已发起售后
    HAS_VALID_ASSIGNMENT = 201003  # 此订单已配货，请点击申请售后
    REFUND_ERROR = 201004  # 退款失败


class BatchAssignType(object):
    '''订单配货类型'''
    # 全部配货
    WHOLE = "whole"
    # 部分配货
    PARTIAL = "partial"
    # 按商品部分配货
    PRODUCT = "product"
    # 按专柜部分配货
    SHOP = "shop"


class BatchAssignTaskStatus(object):
    '''订单配货任务执行状态'''
    # 正在进行中
    IN_PROGRESS = "in_progress"
    # 已经完成
    COMPLETED = "completed"
    # 执行出错
    ERROR = "error"


class AfterSaleType(object):
    # 正常售后单
    NORMAL = "normal"
    # 换货
    EXCHANGE = "exchange"
    # 投诉
    COMPLAINT = "complaint"
    # 催货
    REMINDER = "reminder"
    # 仅退运费
    ONLY_REFUND_POSTAGE = "only_refund_postage"
    # 其他
    OTHER = "other"


class AfterSaleReasons(object):
    # 催单
    REMINDER = "reminder"
    # 退运费
    RETURN_POST = "return_post"
    # 不喜欢/不想要了
    NOT_LIKE_OR_NOT_WANT = "not_like_or_not_want"
    # 快递太慢了不想等了
    SHIPPING_TOO_SLOW_AND_NO_WAIT = "shipping_too_slow_and_no_wait"
    # 快递太慢，帮我催一下
    SHIPPING_TOO_SLOW_AND_REMINDER = "shipping_too_slow_reminder"
    # 换货：质量问题
    EXCHANGE_PRODUCT_QUALITY_ISSUE = "exchange_product_quality_issue"
    # 退货：质量问题
    RETURN_PRODUCT_QUALITY_ISSUE = "return_product_quality_issue"
    # 退货：不喜欢，不想要了
    RETURN_PRODUCT_NOT_LIKE_OR_NOT_WANT = "return_product_not_like_or_not_want"
    # 退货：穿着不合适需退货
    RETURN_PRODUCT_INAPPROPRIATE = "return_product_inappropriate"
    # 换货：大小/款式不合适
    EXCHANGE_PRODUCT_INAPPROPRIATE = "exchange_inappropriate"
    # 退货：商品与描述不符
    RETURN_PRODUCT_DESCRIPTION_MISMATCH = "return_product_description_mismatch"
    # 其他
    OTHER = "other"
    ##  其他前缀，用来做过滤查询
    OTHER_PREFIX = "其他-"
    ###############
    # '客人不想要了',
    CUSTOMER_NOT_WANT = "customer_not_want"
    # '商品缺货，不想等了',
    PRODUCT_LACK_NO_WAIT = "product_lack_no_wait"
    # '订单不能按预计时间送达',
    ORDER_CANNOT_SHIPPING_ONTIME = "order_cannot_shipping_ontime"
    # '操作有误（商品、地址等选错）',
    OPERATE_ERROR = "operate_error"
    # '重复下单/误下单',
    ORDER_DUPLICATE = "order_duplicate"
    # '其他渠道价格更低',
    CHIPPER_ON_OTHER_CHANNEL = "chipper_on_other_channel"
    # '该商品降价了',
    CHIPPER_NOW = "chipper_now"
    # 重新下单买（商品/数量拍错了）
    ORDER_DUPLICATE2 = "order_duplicate2"
    # 不想买了
    NOT_WANT_ANYMORE = "not_want_anymore"
    # 用户整单退
    USER_ENTIRE_RETURN = "user_entire_return"
    # 整单退
    ENTIRE_RETURN = "entire_return"


AFTERSALE_USER_REASON_DICT = {
    AfterSaleReasons.REMINDER: "提醒发货",
    AfterSaleReasons.RETURN_POST: "退运费",
    AfterSaleReasons.NOT_LIKE_OR_NOT_WANT: "不喜欢/不想要了",
    AfterSaleReasons.SHIPPING_TOO_SLOW_AND_NO_WAIT: "快递太慢了不想等了",
    AfterSaleReasons.SHIPPING_TOO_SLOW_AND_REMINDER: '快递太慢，帮我催一下',
    # AfterSaleReasons.EXCHANGE_PRODUCT_INAPPROPRIATE: '换货：大小/款式不合适',
    # AfterSaleReasons.EXCHANGE_PRODUCT_QUALITY_ISSUE:'换货：质量问题',
    AfterSaleReasons.RETURN_PRODUCT_QUALITY_ISSUE: '退货：质量问题',
    AfterSaleReasons.RETURN_PRODUCT_INAPPROPRIATE: '退货：穿着不合适需退货',
    AfterSaleReasons.RETURN_PRODUCT_NOT_LIKE_OR_NOT_WANT: '退货：不喜欢，不想要了',
    AfterSaleReasons.RETURN_PRODUCT_DESCRIPTION_MISMATCH: '退货：商品与描述不符',
    AfterSaleReasons.OTHER: "其他",

}

AFTERSALE_ALL_REASON_DICT = {
    AfterSaleReasons.REMINDER: "提醒发货",
    AfterSaleReasons.RETURN_POST: "退运费",
    AfterSaleReasons.NOT_LIKE_OR_NOT_WANT: "不喜欢/不想要了",
    AfterSaleReasons.SHIPPING_TOO_SLOW_AND_NO_WAIT: "快递太慢了不想等了",
    AfterSaleReasons.SHIPPING_TOO_SLOW_AND_REMINDER: '快递太慢，帮我催一下',
    AfterSaleReasons.EXCHANGE_PRODUCT_INAPPROPRIATE: '换货：大小/款式不合适',
    AfterSaleReasons.EXCHANGE_PRODUCT_QUALITY_ISSUE: '换货：质量问题',
    AfterSaleReasons.RETURN_PRODUCT_QUALITY_ISSUE: '退货：质量问题',
    AfterSaleReasons.RETURN_PRODUCT_INAPPROPRIATE: '退货：穿着不合适需退货',
    AfterSaleReasons.RETURN_PRODUCT_NOT_LIKE_OR_NOT_WANT: '退货：不喜欢，不想要了',
    AfterSaleReasons.RETURN_PRODUCT_DESCRIPTION_MISMATCH: '退货：商品与描述不符',
    AfterSaleReasons.CUSTOMER_NOT_WANT: "客人不想要了",
    AfterSaleReasons.PRODUCT_LACK_NO_WAIT: "商品缺货，不想等了",
    AfterSaleReasons.ORDER_CANNOT_SHIPPING_ONTIME: "订单不能按预计时间送达",
    AfterSaleReasons.OPERATE_ERROR: "操作有误（商品、地址等选错）",
    AfterSaleReasons.ORDER_DUPLICATE: "重复下单/误下单",
    AfterSaleReasons.CHIPPER_ON_OTHER_CHANNEL: "其他渠道价格更低",
    AfterSaleReasons.CHIPPER_NOW: "该商品降价了",
    AfterSaleReasons.ORDER_DUPLICATE2: "重新下单买（商品/数量拍错了）",
    AfterSaleReasons.NOT_WANT_ANYMORE: "不想买了",
    AfterSaleReasons.USER_ENTIRE_RETURN: "用户整单退",
    AfterSaleReasons.ENTIRE_RETURN: "整单退",
    AfterSaleReasons.OTHER: "其他"

}


class HGVendingStatus(object):
    # 初始态
    INIT = "init"
    # 已取货
    PICKED_UP = "picked_up"
    # 已售后
    REFUND = "refund"
    # 超时未支付关闭
    CLOSED = "closed"

    HGVENDING_STATUS_CHOICES = (
        (INIT, "初始态"),
        (PICKED_UP, "已取货"),
        (REFUND, "已售后"),
        (CLOSED, "已关闭")
    )


# 贩售机取货码过期检测定时任务运行间隔
HGVENDING_BULK_TASK_INTERVAL = 15 * 60


class DeliverTimeType(object):
    '''
    发货时间类型(fixed_time 固定时间/pay_relative_time 支付相对时间)
    '''
    FIXED_TIME = "fixed_time"
    PAY_RELATIVE_TIME = "pay_relative_time"
    DELIVERTIME_TYPE_CHOICES = (
        (FIXED_TIME, "固定时间"),
        (PAY_RELATIVE_TIME, "支付相对时间")
    )


class PayMethod(object):
    '''支付方法（once 一次支付/twice两次支付）'''
    ONCE = "once"
    TWICE = "twice"
    PAY_METHOD_CHOICES = (
        (ONCE, "一次支付"),
        (TWICE, "两次支付")
    )


class DeliverTimeStatus(object):
    '''发货时间配置状态(none无需配置/to_configure待配置/configured已配置)'''
    NONE = "none"
    TO_CONFIGURE = "to_configure"
    CONFIGURED = "configured"
    DELIVERTIME_STATUS_CHOICES = (
        (NONE, "无需配置"),
        (TO_CONFIGURE, "待配置"),
        (CONFIGURED, "已配置")
    )


class PayStepType(object):
    '''支付阶段类型(all全款/deposit定金/tailpay尾款)'''
    ONCE = "once"
    DEPOSIT = "deposit"
    TAIL = "tail"
    PAY_STEP_TYPE_CHOICES = (
        (ONCE, "全款"),
        (DEPOSIT, "定金"),
        (TAIL, "尾款")
    )


STEP_CHAR = "&"


class AssignmentStatus(object):
    '''发货单邮寄状态'''
    # 只要创建了发货单就认为是配货了
    # 已配货，待发货（无快递单号）或待提货
    READY = "ready"
    # 已完成-有快递单号了，或者用户来自提了
    COMPLETED = "completed"
    # 已取消
    # 发货单不能删除，只能关闭取消
    CLOSED = "closed"


class AftersaleSource(object):
    """
    售后来源
    """
    # 客人发起
    GUEST_INITIATED = "guest_initiated"
    # 客服发起
    SERVICE_INITIATED = "service_initiated"


AFTERSALE_USER_REASON_DICT = {
    AfterSaleReasons.REMINDER: "提醒发货",
    AfterSaleReasons.RETURN_POST: "退运费",
    AfterSaleReasons.NOT_LIKE_OR_NOT_WANT: "不喜欢/不想要了",
    AfterSaleReasons.SHIPPING_TOO_SLOW_AND_NO_WAIT: "快递太慢了不想等了",
    AfterSaleReasons.SHIPPING_TOO_SLOW_AND_REMINDER: '快递太慢，帮我催一下',
    # AfterSaleReasons.EXCHANGE_PRODUCT_INAPPROPRIATE: '换货：大小/款式不合适',
    # AfterSaleReasons.EXCHANGE_PRODUCT_QUALITY_ISSUE:'换货：质量问题',
    AfterSaleReasons.RETURN_PRODUCT_QUALITY_ISSUE: '退货：质量问题',
    AfterSaleReasons.RETURN_PRODUCT_INAPPROPRIATE: '退货：穿着不合适需退货',
    AfterSaleReasons.RETURN_PRODUCT_NOT_LIKE_OR_NOT_WANT: '退货：不喜欢，不想要了',
    AfterSaleReasons.RETURN_PRODUCT_DESCRIPTION_MISMATCH: '退货：商品与描述不符',
    AfterSaleReasons.OTHER: "其他",
}

AFTERSALE_ALL_REASON_DICT = {
    AfterSaleReasons.REMINDER: "提醒发货",
    AfterSaleReasons.RETURN_POST: "退运费",
    AfterSaleReasons.NOT_LIKE_OR_NOT_WANT: "不喜欢/不想要了",
    AfterSaleReasons.SHIPPING_TOO_SLOW_AND_NO_WAIT: "快递太慢了不想等了",
    AfterSaleReasons.SHIPPING_TOO_SLOW_AND_REMINDER: '快递太慢，帮我催一下',
    AfterSaleReasons.EXCHANGE_PRODUCT_INAPPROPRIATE: '换货：大小/款式不合适',
    AfterSaleReasons.EXCHANGE_PRODUCT_QUALITY_ISSUE: '换货：质量问题',
    AfterSaleReasons.RETURN_PRODUCT_QUALITY_ISSUE: '退货：质量问题',
    AfterSaleReasons.RETURN_PRODUCT_INAPPROPRIATE: '退货：穿着不合适需退货',
    AfterSaleReasons.RETURN_PRODUCT_NOT_LIKE_OR_NOT_WANT: '退货：不喜欢，不想要了',
    AfterSaleReasons.RETURN_PRODUCT_DESCRIPTION_MISMATCH: '退货：商品与描述不符',
    AfterSaleReasons.CUSTOMER_NOT_WANT: "客人不想要了",
    AfterSaleReasons.PRODUCT_LACK_NO_WAIT: "商品缺货，不想等了",
    AfterSaleReasons.ORDER_CANNOT_SHIPPING_ONTIME: "订单不能按预计时间送达",
    AfterSaleReasons.OPERATE_ERROR: "操作有误（商品、地址等选错）",
    AfterSaleReasons.ORDER_DUPLICATE: "重复下单/误下单",
    AfterSaleReasons.CHIPPER_ON_OTHER_CHANNEL: "其他渠道价格更低",
    AfterSaleReasons.CHIPPER_NOW: "该商品降价了",
    AfterSaleReasons.ORDER_DUPLICATE2: "重新下单买（商品/数量拍错了）",
    AfterSaleReasons.NOT_WANT_ANYMORE: "不想买了",
    AfterSaleReasons.USER_ENTIRE_RETURN: "用户整单退",
    AfterSaleReasons.ENTIRE_RETURN: "整单退",
    AfterSaleReasons.OTHER: "其他",
}


class Order_Number_Pay_Status(object):
    # 子支付单状态(init初始/doing进行中/done已完成)
    INIT = "init"
    DOING = "doing"
    DONE = "done"
    FAILED = "failed"
    ORDER_NUMBER_PAY_STATUS_CHOICES = (
        (INIT, '初始'),
        (DOING, '进行中'),
        (DONE, "已完成"),
        (FAILED, "失败"),

    )
    ORDER_NUMBER_PAY_STATUS_DICT = dict(ORDER_NUMBER_PAY_STATUS_CHOICES)
