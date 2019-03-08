__author__ = "zanweb <zanweb@163.com>"

from .Base import _Call


class Part(_Call):
    def __init__(self, part_name='', x_reference=0, x_offset=0.0,
                 permanent=False, tool_number=0, macro_name='', length=None, y_offset=0.0,
                 y_reference=1, part_option=None):
        self.y_reference = y_reference
        self.y_offset = y_offset
        self.macro_name = macro_name
        self.permanent = permanent
        self.x_offset = x_offset
        self.x_reference = x_reference
        self.tool_number = tool_number
        self.part_option = part_option
        self.length = length
        self.part_name = part_name

    @property
    def part_name(self):
        return self._part_name

    @part_name.setter
    def part_name(self, value):
        if not isinstance(value, str):
            raise ValueError('score must be an string!')
        if len(value) > 30:
            raise ValueError('part_name must less than 30!')
        self._part_name = value

    @part_name.deleter
    def part_name(self):
        raise AttributeError("Can't delete attribute")

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        if not isinstance(value, float):
            raise ValueError('length must be an float!')
        if value > 99999999:
            raise ValueError('length must less than 99999999!')
        self._length = value

    @length.deleter
    def length(self):
        raise AttributeError("Can't delete attribute")

    @property
    def x_reference(self):
        return self._x_reference

    @x_reference.setter
    def x_reference(self, value):
        if not isinstance(value, int):
            raise ValueError('x_reference must be an int!')
        if value not in [0, 1, 2, 3, 4, 5, 8]:
            raise ValueError('x_reference must in the list [0, 1, 2, 3, 4, 5, 8]!')
        self._x_reference = value

    @x_reference.deleter
    def x_reference(self):
        raise AttributeError("Can't delete attribute")

    @property
    def x_offset(self):
        return self._x_offset

    @x_offset.setter
    def x_offset(self, value):
        if not isinstance(value, float):
            raise ValueError('x_offset must be an float!')
        if value > 9999999999:
            raise ValueError('x_offset must less than 9999999999!')
        self._x_offset = value

    @x_offset.deleter
    def x_offset(self):
        raise AttributeError("Can't delete attribute")

    @property
    def permanent(self):
        return self._permanent

    @permanent.setter
    def permanent(self, value):
        if not isinstance(value, str):
            raise ValueError('permanent must be an string!')
        if value not in ["T", "F"]:
            raise ValueError('permanent must in list ["T", "F"]!')
        self._permanent = value

    @permanent.deleter
    def permanent(self):
        raise AttributeError("Can't delete attribute")

    @property
    def macro_name(self):
        return self._macro_name

    @macro_name.setter
    def macro_name(self, value):
        if not isinstance(value, str):
            raise ValueError('macro_name must be an string!')
        if len(value) > 30:
            raise ValueError('macro_name must less than 30!')
        self._macro_name = value

    @macro_name.deleter
    def macro_name(self):
        raise AttributeError("Can't delete attribute")

    @property
    def y_offset(self):
        return self._y_offset

    @y_offset.setter
    def y_offset(self, value):
        if not isinstance(value, int):
            raise ValueError('y_offset must be an int!')
        if value > 99999999:
            raise ValueError('y_offset must less than 99999999!')
        self._y_offset = value

    @y_offset.deleter
    def y_offset(self):
        raise AttributeError("Can't delete attribute")

    @property
    def y_reference(self):
        return self._y_reference

    @y_reference.setter
    def y_reference(self, value):
        if not isinstance(value, int):
            raise ValueError('y_reference must be an int!')
        if value not in [1, 2, 3, 4, 5, 6]:
            raise ValueError('y_reference must in list [1,2,3,4,5,6]!')
        self._y_reference = value

    @y_reference.deleter
    def y_reference(self):
        raise AttributeError("Can't delete attribute")

    def __str__(self):
        result = ""
        result += '"' + self.part_name + '",'
        result += format(self.length, "0.3f") + ','
        result += '"' + self.part_option + '",'
        result += format(self.tool_number, "3f") + ','
        result += format(self.x_reference, "1f") + ','
        result += format(self.x_offset, "10.3f") + ','
        result += self.permanent + ','
        result += '"' + self.macro_name + '",'
        result += format(self.y_offset, "8.3f") + ','
        result += format(self.y_reference, "1f")
        return result


class Parts:
    def __init__(self):
        self.parts = []

    def __str__(self):
        return '\n'.join(str(x) for x in self.parts)
