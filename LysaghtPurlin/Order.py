__author__ = "zanweb <zanweb@163.com>"

from Base.base import String
from .Batch import Batch
from Zfile.zText import TextFile


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

    def get_order_no_from_lysaght_txt(self, file_with_path):
        try:
            f = TextFile(file_with_path)
            order_info = f.get_lysaght_order()
            self.order_no = order_info['ORDER_NO']
        except Exception as e:
            print(e)
        finally:
            return self.order_no
