__author__ = "zanweb <zanweb@163.com>"

from Base.base import String
from .Batch import Batch


class Order(object):
    order_no = String('order_no')
    org = String('org')
    product_code = String('product_code')

    def __init__(self, order_no, org, product_code):
        self.product_code = product_code
        self.org = org
        self.order_no = order_no
        self.batches = []

    def add_batch(self, batch):
        if not isinstance(batch, Batch):
            raise TypeError('You must import a Batch type!')
        self.batches.append(batch)
