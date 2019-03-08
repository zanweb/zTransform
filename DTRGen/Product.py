__author__ = "zanweb <zanweb@163.com>"

from .Base import _Call, UNITES

class Product(_Call):
    def __init__(self, action_code= '', machine= 0, product_code= '', description= '', finished_width= 0.0, staging_bay= '', loading_dock= '', hole_spacing= 0.0, calculate_length= False, hole_count= False, leg_height= 0.0, product_code_group= '', coil_change_minutes= 0.0, tooling_change_minutes= 0.0, feet_per_minute= 0):
        self.action_code = action_code
        self.machine = machine
        self.product_code = product_code
        self.description = description
        self.finished_width = finished_width
        self.staging_bay = staging_bay
        self.loading_dock = loading_dock
        self.hole_spacing = hole_spacing
        self.calculate_length = calculate_length
        self.hole_count = hole_count
        self.leg_height = leg_height
        self.product_code_group = product_code_group
        self.coil_change_minutes = coil_change_minutes
        self.tooling_change_minutes = tooling_change_minutes
        self.feet_per_minute = feet_per_minute

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
    def machine(self):
        return self._machine

    @machine.setter
    def machine(self, value):
        if not isinstance(value, int):
            raise ValueError('machine must be an int!')
        if value > 999:
            raise ValueError('machine must less than 999!')
        self._machine = value

    @machine.deleter
    def machine(self):
        raise AttributeError("Can't delete attribute")


    @property
    def product_code(self):
        return self._product_code

    @product_code.setter
    def product_code(self, value):
        if not isinstance(value, str):
            raise ValueError('product_code must be a string!')
        if len(value) > 20:
            raise ValueError('product_code must less than 20 characters!')
        self._product_code = value

    @product_code.deleter
    def product_code(self):
        raise AttributeError("Can't delete attribute")


    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise ValueError('description must be a string!')
        if len(value) > 30:
            raise ValueError('description must less than 30 characters!')
        self._description = value

    @description.deleter
    def description(self):
        raise AttributeError("Can't delete attribute")


    @property
    def finished_width(self):
        return self._finished_width

    @finished_width.setter
    def finished_width(self, value):
        if not isinstance(value, float):
            raise ValueError('finished_width must be a float!')
        if value > 99999999.0:
            raise ValueError('finished_width must less than 99999999.00!')
        self._finished_width = value

    @finished_width.deleter
    def finished_width(self):
        raise AttributeError("Can't delete attribute")


    @property
    def staging_bay(self):
        return self._staging_bay

    @staging_bay.setter
    def staging_bay(self, value):
        if not isinstance(value, str):
            raise ValueError('staging_bay must be a string!')
        if len(value) > 10:
            raise ValueError('staging_bay must less than 10 characters!')
        self._staging_bay = value

    @staging_bay.deleter
    def staging_bay(self):
        raise AttributeError("Can't delete attribute")


    @property
    def loading_dock(self):
        return self._loading_dock

    @loading_dock.setter
    def loading_dock(self, value):
        if not isinstance(value, str):
            raise ValueError('loading_dock must be a string!')
        if len(value) > 10:
            raise ValueError('loading_dock must less than 10 characters!')
        self._loading_dock = value

    @loading_dock.deleter
    def loading_dock(self):
        raise AttributeError("Can't delete attribute")


    @property
    def hole_spacing(self):
        return self._hole_spacing

    @hole_spacing.setter
    def hole_spacing(self, value):
        if not isinstance(value, float):
            raise ValueError('hole_spacing must be a float!')
        if value > 99999999.0:
            raise ValueError('hole_spacing must less than 999999999.00!')
        self._hole_spacing = value

    @hole_spacing.deleter
    def hole_spacing(self):
        raise AttributeError("Can't delete attribute")


    @property
    def calculate_length(self):
        return self._calculate_length

    @calculate_length.setter
    def calculate_length(self, value):
        if not isinstance(value, bool):
            raise ValueError('calculate_length must be a bool!')
        # if len(value) > 20:
        #     raise ValueError('calculate_length must less than 20 characters!')
        self._calculate_length = value

    @calculate_length.deleter
    def calculate_length(self):
        raise AttributeError("Can't delete attribute")


    @property
    def hole_count(self):
        return self._hole_count

    @hole_count.setter
    def hole_count(self, value):
        if not isinstance(value, bool):
            raise ValueError('hole_count must be a bool!')
        # if len(value) > 20:
        #     raise ValueError('hole_count must less than 20 characters!')
        self._hole_count = value

    @hole_count.deleter
    def hole_count(self):
        raise AttributeError("Can't delete attribute")


    @property
    def leg_height(self):
        return self._leg_height

    @leg_height.setter
    def leg_height(self, value):
        if not isinstance(value, float):
            raise ValueError('leg_height must be a float!')
        if value > 99999999.0:
            raise ValueError('leg_height must less than 99999999.00!')
        self._leg_height = value

    @leg_height.deleter
    def leg_height(self):
        raise AttributeError("Can't delete attribute")


    @property
    def product_code_group(self):
        return self._product_code_group

    @product_code_group.setter
    def product_code_group(self, value):
        if not isinstance(value, str):
            raise ValueError('product_code_group must be a string!')
        if len(value) > 20:
            raise ValueError('product_code_group must less than 20 characters!')
        self._product_code_group = value

    @product_code_group.deleter
    def product_code_group(self):
        raise AttributeError("Can't delete attribute")


    @property
    def coil_change_minutes(self):
        return self._coil_change_minutes

    @coil_change_minutes.setter
    def coil_change_minutes(self, value):
        if not isinstance(value, float):
            raise ValueError('coil_change_minutes must be a float!')
        if value > 999999.0:
            raise ValueError('coil_change_minutes must less than 999999.00!')
        self._coil_change_minutes = value

    @coil_change_minutes.deleter
    def coil_change_minutes(self):
        raise AttributeError("Can't delete attribute")


    @property
    def tooling_change_minutes(self):
        return self._tooling_change_minutes

    @tooling_change_minutes.setter
    def tooling_change_minutes(self, value):
        if not isinstance(value, float):
            raise ValueError('tooling_change_minutes must be a float!')
        if value > 999999.0:
            raise ValueError('tooling_change_minutes must less than 999999.00!')
        self._tooling_change_minutes = value

    @tooling_change_minutes.deleter
    def tooling_change_minutes(self):
        raise AttributeError("Can't delete attribute")


    @property
    def feet_per_minute(self):
        return self._feet_per_minute

    @feet_per_minute.setter
    def feet_per_minute(self, value):
        if not isinstance(value, int):
            raise ValueError('feet_per_minute must be an int!')
        if value > 9999:
            raise ValueError('feet_per_minute must less than 9999!')
        self._feet_per_minute = value

    @feet_per_minute.deleter
    def feet_per_minute(self):
        raise AttributeError("Can't delete attribute")

    def __str__(self):
        result = ''
        result += '"' + self.action_code + '",'
        result += format(self.machine, '0.0f') + ','
        result += '"' + self.product_code + '",'
        if self.description:
            result += '"' + self.description + '",'
        else:
            result += '"",'
        if self.finished_width:
            result += format(self.finished_width, '0.3f') + ','
        else:
            result += ','
        if self.staging_bay:
            result += '"' + self.staging_bay + '",'
        else:
            result += '"",'
        if self.loading_dock:
            result += '"' + self.loading_dock + '",'
        else:
            result += '"",'
        if self.hole_spacing:
            result += format(self.hole_spacing, '0.3f') + ','
        else:
            result += ','
        if self.calculate_length:
            result += 'T,'
        else:
            result += 'F,'
        if self.hole_count:
            result += 'T,'
        else:
            result +='F,'
        if self.leg_height:
            result += format(self.leg_height, '0.3f') + ','
        else:
            result += ','
        if self.product_code_group:
            result += '"' + self.product_code_group + '",'
        else:
            result += '"",'
        if self.coil_change_minutes:
            result += format(self.coil_change_minutes, '0.0f') + ','
        else:
            result += ','
        if self.tooling_change_minutes:
            result += format(self.tooling_change_minutes, '0.0f') + ','
        else:
            result += ','
        if self.feet_per_minute:
            result += format(self.feet_per_minute, '0.0f') + ''
        else:
            result += ''

        return result


class Products:
    def __init__(self):
        self.products = []

    def __str__(self):
        return '\n'.join(str(x) for x in self.products)

    def append(self, product):
        self.products.append(product)

    def save_as(self, file_name):
        self.file_name = file_name
        self.save()

    def save(self):
        test = open(self.file_name, 'w')
        test.write(str(self))
        test.close()
