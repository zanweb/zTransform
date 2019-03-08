__author__ = "zanweb <zanweb@163.com>"

import copy
UNITES = "UNITS=.39370078"


class _Call:
    """Makes a callable class."""

    def copy(self):
        """Returns a copy."""
        return copy.deepcopy(self)

    def __call__(self, **attrs):
        """Returns a copy with modified attributes."""
        copied = self.copy()
        for attr in attrs:
            setattr(copied, attr, attrs[attr])
        return copied
