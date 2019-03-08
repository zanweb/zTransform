__author__ = "zanweb <zanweb@163.com>"

from .Base import _Call


class Material(_Call):
    def __init__(self, action_code='', material_code='', gauge=0, thickness=0.0, width=0.0, color='',
                 material_type='', material_description='', pound_per_foot=0.0, cost_per_pound=0.0,
                 recorder_point=0):
        self.action_code = action_code
        self.material_code = material_code
        self.gauge = gauge
        self.thickness = thickness
        self.width = width
        self.color = color
        self.material_type = material_type
        self.material_description = material_description
        self.pound_per_foot = pound_per_foot
        self.cost_per_pound = cost_per_pound
        self.recorder_point = recorder_point

    @property
    def action_code(self):
        return self._action_code

    @action_code.setter
    def action_code(self, value):
        if not isinstance(value, str):
            raise ValueError('action_code must be a string!')
        if value not in ["A", "C", "D"]:
            raise ValueError('action_code must in list ["A", "C", "D"]!')
        self._action_code = value

    @action_code.deleter
    def action_code(self):
        raise AttributeError("Can't delete attribute")

    @property
    def material_code(self):
        return self._material_code

    @material_code.setter
    def material_code(self, value):
        if not isinstance(value, str):
            raise ValueError('material_code must be a string!')
        if len(value) > 20:
            raise ValueError('material_code must less than 20 characters!')
        self._material_code = value

    @material_code.deleter
    def material_code(self):
        raise AttributeError("Can't delete attribute")

    @property
    def gauge(self):
        return self._gauge

    @gauge.setter
    def gauge(self, value):
        if not isinstance(value, int):
            raise ValueError('gauge must be an int!')
        if value > 99:
            raise ValueError('gauge must less than 99!')
        self._gauge = value

    @gauge.deleter
    def gauge(self):
        raise AttributeError("Can't delete attribute")

    @property
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        if not isinstance(value, float):
            raise ValueError('thickness must be a float!')
        if value > 999999.0:
            raise ValueError('thickness must less than 999999.0!')
        self._thickness = value

    @thickness.deleter
    def thickness(self):
        raise AttributeError("Can't delete attribute")

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if not isinstance(value, float):
            raise ValueError('width must be a float!')
        if value > 999999.0:
            raise ValueError('width must less than 999999.00!')
        self._width = value

    @width.deleter
    def width(self):
        raise AttributeError("Can't delete attribute")

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if not isinstance(value, str):
            raise ValueError('color must be a string!')
        if len(value) > 20:
            raise ValueError('color must less than 20 characters!')
        self._color = value

    @color.deleter
    def color(self):
        raise AttributeError("Can't delete attribute")

    @property
    def material_type(self):
        return self._material_type

    @material_type.setter
    def material_type(self, value):
        if not isinstance(value, str):
            raise ValueError('material_type must be a string!')
        if len(value) > 10:
            raise ValueError('material_type must less than 10 characters!')
        self._material_type = value

    @material_type.deleter
    def material_type(self):
        raise AttributeError("Can't delete attribute")

    @property
    def material_description(self):
        return self._material_description

    @material_description.setter
    def material_description(self, value):
        if not isinstance(value, str):
            raise ValueError('material_description must be a string!')
        if len(value) > 40:
            raise ValueError('material_description must less than 40 characters!')
        self._material_description = value

    @material_description.deleter
    def material_description(self):
        raise AttributeError("Can't delete attribute")

    @property
    def pound_per_foot(self):
        return self._pound_per_foot

    @pound_per_foot.setter
    def pound_per_foot(self, value):
        if not isinstance(value, float):
            raise ValueError('pound_per_foot must be a float!')
        if value > 9999999.0:
            raise ValueError('pound_per_foot must less than 9999999.00!')
        self._pound_per_foot = value

    @pound_per_foot.deleter
    def pound_per_foot(self):
        raise AttributeError("Can't delete attribute")

    @property
    def cost_per_pound(self):
        return self._cost_per_pound

    @cost_per_pound.setter
    def cost_per_pound(self, value):
        if not isinstance(value, float):
            raise ValueError('cost_per_pound must be a float!')
        if value > 9999999.0:
            raise ValueError('cost_per_pound must less than 9999999.00!')
        self._cost_per_pound = value

    @cost_per_pound.deleter
    def cost_per_pound(self):
        raise AttributeError("Can't delete attribute")

    @property
    def recorder_point(self):
        return self._recorder_point

    @recorder_point.setter
    def recorder_point(self, value):
        if not isinstance(value, int):
            raise ValueError('recorder_point must be an int!')
        if value > 999999:
            raise ValueError('recorder_point must less than 999999!')
        self._recorder_point = value

    @recorder_point.deleter
    def recorder_point(self):
        raise AttributeError("Can't delete attribute")

    def __str__(self):
        result = ''
        result += '"' + self.action_code + '",'
        result += '"' + self.material_code + '",'
        if self.gauge:
            result += format(self.gauge, '0.0f') + ','
        else:
            result += ','
        if self.thickness:
            result += format(self.thickness, '0.4f') + ','
        else:
            result += ','
        if self.width:
            result += format(self.width, '0.3f') + ','
        else:
            result += ','
        if self.color:
            result += '"' + self.color + '",'
        else:
            result += '"",'
        if self.material_type:
            result += '"' + self.material_type + '",'
        else:
            result += '"",'
        result += '"",'
        if self.material_description:
            result += '"' + self.material_description + '",'
        else:
            result += '"",'
        if self.pound_per_foot:
            result += format(self.pound_per_foot, '0.2f') + ','
        else:
            result += ','
        if self.cost_per_pound:
            result += format(self.cost_per_pound, '0.2f') + ','
        else:
            result += ','
        result += ','
        if self.recorder_point:
            result += format(self.recorder_point, '0.0f')
        else:
            result += ''
        return result


class Materials:
    def __init__(self):
        self.materials = []

    def __str__(self):
        return '\n'.join(str(x) for x in self.materials)

    def append(self, material):
        self.materials.append(material)

    def save_as(self, file_name):
        self.file_name = file_name
        self.save()

    def save(self):
        test = open(self.file_name, 'w')
        test.write(str(self))
        test.close()
