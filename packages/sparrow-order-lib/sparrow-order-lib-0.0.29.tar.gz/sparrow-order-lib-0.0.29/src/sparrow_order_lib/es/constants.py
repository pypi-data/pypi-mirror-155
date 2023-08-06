
from sparrow_order_lib.core.datastructures import ImmutablePropertyClassBase


class DocType(ImmutablePropertyClassBase):
    _TEST_DOC_TYPE = 'test_doc_type'  # 测试数据类型
    ORDER = 'order'  # 订单数据


IndexMapping = {
    DocType._TEST_DOC_TYPE: 'test_doc_type',  # 测试数据类型
    DocType.ORDER: 'order_v2',
}
