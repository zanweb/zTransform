__author__ = "zanweb <zanweb@163.com>"

from Base.base import Integer
from .Part import Part


class Bundle:
    bundle_no = Integer('bundle_no')

    def __init__(self, bundle_no):
        self.bundle_no = bundle_no
        self.parts = []

    def add_part(self, part):
        if not isinstance(part, Part):
            raise TypeError('You must import a Part type!')
        self.parts.append(part)
