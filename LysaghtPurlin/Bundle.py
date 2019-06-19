__author__ = "zanweb <zanweb@163.com>"

# from zBase.base import Integer
from zBase import zbase
from LysaghtPurlin import Part


class Bundle:
    bundle_no = zbase.Integer('bundle_no')

    def __init__(self, bundle_no):
        self.bundle_no = bundle_no
        self.parts = []

    def add_part(self, part):
        if not isinstance(part, Part.Part):
            raise TypeError('You must import a Part type!')
        self.parts.append(part)
