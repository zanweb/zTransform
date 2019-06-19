__author__ = "zanweb <zanweb@163.com>"

# from zBase.base import Integer
from LysaghtPurlin import Bundle
from zBase import zbase


class Batch:
    batch_no = zbase.Integer('batch_no')

    def __init__(self, batch_no):
        self.batch_no = batch_no
        self.bundles = []

    def add_bundle(self, bundle):
        if not isinstance(bundle, Bundle.Bundle):
            raise TypeError('You must import a Part type!')
        self.bundles.append(bundle)
