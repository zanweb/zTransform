__author__ = "zanweb <zanweb@163.com>"

from .Base import _Call, UNITES


class Part(_Call):
    def __init__(self, part_name='', x_reference=0, x_offset=0.0,
                 permanent=False, tool_number=0, macro_name='', length=0.0, y_offset=0.0,
                 y_reference=0, part_option=None):
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
    def tool_number(self):
        return self._tool_number

    @tool_number.setter
    def tool_number(self, value):
        if not isinstance(value, int):
            raise ValueError('tool_number must be an int!')
        if value > 999:
            raise ValueError('tool_number must less than 999!')
        self._tool_number = value

    @tool_number.deleter
    def tool_number(self):
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
        if not isinstance(value, bool):
            raise ValueError('permanent must be an bool!')
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
        if not isinstance(value, float):
            raise ValueError('y_offset must be an float!')
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
        if value not in [0, 1, 2, 3, 4, 5, 6]:
            raise ValueError('y_reference must in list [1,2,3,4,5,6]!')
        self._y_reference = value

    @y_reference.deleter
    def y_reference(self):
        raise AttributeError("Can't delete attribute")

    def __str__(self):
        result = ""
        result += '"' + self.part_name + '",'
        if self.length == 0.0:
            result += ','
        else:
            result += format(self.length, "0.3f") + ','
        result += '"",'
        result += format(self.tool_number, "0.0f") + ','
        result += format(self.x_reference, "0.0f") + ','
        result += format(self.x_offset, "0.3f") + ','
        if self.permanent:
            result += 'T,'
        else:
            result += 'F,'
        result += '"' + self.macro_name + '",'
        if self.y_offset == 0.0:
            result += ','
        else:
            result += format(self.y_offset, "0.3f") + ','
        if self.y_reference == 0:
            result += ''
        else:
            result += format(self.y_reference, "0.0f")
        return result


class Parts:
    def __init__(self):
        # self.parts = [UNITES]
        self.parts = []
        self.file_name = ''

    def __str__(self):
        return '\n'.join(str(x) for x in self.parts)

    def append(self, part):
        self.parts.append(part)

    def extend(self, parts):
        self.parts.extend(parts)

    def save_as(self, file_name):
        self.file_name = file_name
        self.save()

    def save(self):
        test = open(self.file_name, 'w')
        test.write(str(self))
        test.close()


class PartShape(_Call):
    def __init__(self, part_name='', product_group='', sm_mark='', sm_num='', diameter_length=0.0, width=0.0,
                 x_reference=0, x_offset=0.0,
                 y_reference=0, y_offset=0.0, length=0.0, part_option=None):
        self.width = width
        self.diameter_length = diameter_length
        self.sm_num = sm_num
        self.sm_mark = sm_mark
        self.product_group = product_group
        self.y_reference = y_reference
        self.y_offset = y_offset
        self.x_offset = x_offset
        self.x_reference = x_reference
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
    def product_group(self):
        return self._product_group

    @product_group.setter
    def product_group(self, value):
        if not isinstance(value, str):
            raise ValueError('product_group must be a string!')
        if len(value) > 20:
            raise ValueError('product_group must less than 20 characters!')
        self._product_group = value

    @product_group.deleter
    def product_group(self):
        raise AttributeError("Can't delete attribute")

    @property
    def sm_mark(self):
        return self._sm_mark

    @sm_mark.setter
    def sm_mark(self, value):
        if not isinstance(value, str):
            raise ValueError('sm_mark must be a string!')
        if value not in ["S", "M"]:
            raise ValueError('sm_mark must be in list ["S", "M"]!')
        self._sm_mark = value

    @sm_mark.deleter
    def sm_mark(self):
        raise AttributeError("Can't delete attribute")

    @property
    def sm_num(self):
        return self._sm_num

    @sm_num.setter
    def sm_num(self, value):
        if not isinstance(value, str):
            raise ValueError('sm_num must be an string!')
        if len(value) > 20:
            raise ValueError('sm_num must less than 20 characters!')
        self._sm_num = value

    @sm_num.deleter
    def sm_num(self):
        raise AttributeError("Can't delete attribute")

    @property
    def diameter_length(self):
        return self._diameter_length

    @diameter_length.setter
    def diameter_length(self, value):
        if not isinstance(value, float):
            raise ValueError('diameter_length must be a float!')
        if value > 99999999:
            raise ValueError('diameter_length must less than 99999999!')
        self._diameter_length = value

    @diameter_length.deleter
    def diameter_length(self):
        raise AttributeError("Can't delete attribute")

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if not isinstance(value, float):
            raise ValueError('width must be a float!')
        if value > 99999999:
            raise ValueError('width must less than 99999999!')
        self._width = value

    @width.deleter
    def width(self):
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
        if not isinstance(value, str):
            raise ValueError('x_reference must be a string!')
        if value not in ['LE', 'TE', 'LC', 'TC', 'ES', 'SL', 'KA']:
            raise ValueError('x_reference must in the list ["LE","TE","LC","TC","ES","SL","KA"]!')
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
    def y_offset(self):
        return self._y_offset

    @y_offset.setter
    def y_offset(self, value):
        if not isinstance(value, float):
            raise ValueError('y_offset must be an float!')
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
        if value not in ["CP", "CM", "PE", "ME", "MP", "MM"]:
            raise ValueError('y_reference must in list ["CP", "CM", "PE", "ME", "MP", "MM"]!')
        self._y_reference = value

    @y_reference.deleter
    def y_reference(self):
        raise AttributeError("Can't delete attribute")

    def __str__(self):
        result = '"PD"'
        result += '"' + self.part_name + '",'
        result += ','
        result += '"' + self.product_group + '"'
        if self.length == 0.0:
            result += ','
        else:
            result += format(self.length, "0.3f") + ','
        result += '"",'
        result += '"' + self.sm_mark + ','
        result += '"' + self.sm_num + '",'
        result += format(self.diameter_length, "0.3f") + ','
        result += format(self.width, "0.3f") + ','
        if self.x_offset == 0.0:
            result += ','
        else:
            result += format(self.x_offset, "0.3f") + ','
        if self.x_reference == 0:
            result += ''
        else:
            result += format(self.x_reference, "0.0f")
        if self.y_offset == 0.0:
            result += ','
        else:
            result += format(self.y_offset, "0.3f") + ','
        if self.y_reference == 0:
            result += ''
        else:
            result += format(self.y_reference, "0.0f")
        return result
