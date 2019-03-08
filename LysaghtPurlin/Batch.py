__author__ = "zanweb <zanweb@163.com>"

from Base.base import Integer
from .Bundle import Bundle


class Batch:
    batch_no = Integer('batch_no')

    def __init__(self, batch_no):
        self.batch_no = batch_no
        self.bundles = []

    def add_bundle(self, bundle):
        if not isinstance(bundle, Bundle):
            raise TypeError('You must import a Part type!')
        self.bundles.append(bundle)
