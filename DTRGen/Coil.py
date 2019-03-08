__author__ = "zanweb <zanweb@163.com>"

from .Base import _Call


class CoilItem(_Call):
    def __init__(self, action_code='', coil_number='', description='', date_in='', date_out='', starting_length=0,
                 length_used=0, status='', vendor_name='', material_code='', coil_material_type='', cost_per_pound=0.0,
                 non_exempt_scrap='', exempt_scrap='', other_adjustments='', weight=0, heat_number='', vendor_code='',
                 purchase_order='', storage_location=''):
        self.action_code = action_code
        self.coil_number = coil_number
        self.description = description
        self.date_in = date_in
        self.date_out = date_out
        self.starting_length = starting_length
        self.length_used = length_used
        self.status = status
        self.vendor_name = vendor_name
        self.material_code = material_code
        self.coil_material_type = coil_material_type
        self.cost_per_pound = cost_per_pound
        self.non_exempt_scrap = non_exempt_scrap
        self.exempt_scrap = exempt_scrap
        self.other_adjustments = other_adjustments
        self.weight = weight
        self.heat_number = heat_number
        self.vendor_code = vendor_code
        self.purchase_order = purchase_order
        self.storage_location = storage_location

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
    def coil_number(self):
        return self._coil_number

    @coil_number.setter
    def coil_number(self, value):
        if not isinstance(value, str):
            raise ValueError('coil_number must be a string!')
        if len(value) > 16:
            raise ValueError('coil_number must less than 16 characters!')
        self._coil_number = value

    @coil_number.deleter
    def coil_number(self):
        raise AttributeError("Can't delete attribute")

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise ValueError('description must be a string!')
        if len(value) > 40:
            raise ValueError('description must less than 40 characters!')
        self._description = value

    @description.deleter
    def description(self):
        raise AttributeError("Can't delete attribute")

    @property
    def date_in(self):
        return self._date_in

    @date_in.setter
    def date_in(self, value):
        if not isinstance(value, str):
            raise ValueError('date_in must be a string!')
        if len(value) > 10:
            raise ValueError('date_in must less than 10 characters!')
        self._date_in = value

    @date_in.deleter
    def date_in(self):
        raise AttributeError("Can't delete attribute")

    @property
    def date_out(self):
        return self._date_out

    @date_out.setter
    def date_out(self, value):
        if not isinstance(value, str):
            raise ValueError('date_out must be a string!')
        if len(value) > 10:
            raise ValueError('date_out must less than 10 characters!')
        self._date_out = value

    @date_out.deleter
    def date_out(self):
        raise AttributeError("Can't delete attribute")

    @property
    def starting_length(self):
        return self._starting_length

    @starting_length.setter
    def starting_length(self, value):
        if not isinstance(value, int):
            raise ValueError('starting_length must be an int!')
        if value > 99999999:
            raise ValueError('starting_length must less than 99999999!')
        self._starting_length = value

    @starting_length.deleter
    def starting_length(self):
        raise AttributeError("Can't delete attribute")

    @property
    def length_used(self):
        return self._length_used

    @length_used.setter
    def length_used(self, value):
        if not isinstance(value, int):
            raise ValueError('length_used must be an int!')
        if value > 99999999:
            raise ValueError('length_used must less than 99999999!')
        self._length_used = value

    @length_used.deleter
    def length_used(self):
        raise AttributeError("Can't delete attribute")

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if not isinstance(value, str):
            raise ValueError('status must be a string!')
        if value not in ["I", "C"]:
            raise ValueError('status must in list ["I", "C"]!')
        self._status = value

    @status.deleter
    def status(self):
        raise AttributeError("Can't delete attribute")

    @property
    def vendor_name(self):
        return self._vendor_name

    @vendor_name.setter
    def vendor_name(self, value):
        if not isinstance(value, str):
            raise ValueError('vendor_name must be a string!')
        if len(value) > 30:
            raise ValueError('vendor_name must less than 30 characters!')
        self._vendor_name = value

    @vendor_name.deleter
    def vendor_name(self):
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
    def coil_material_type(self):
        return self._coil_material_type

    @coil_material_type.setter
    def coil_material_type(self, value):
        if not isinstance(value, str):
            raise ValueError('coil_material_type must be a string!')
        if len(value) > 10:
            raise ValueError('coil_material_type must less than 10 characters!')
        self._coil_material_type = value

    @coil_material_type.deleter
    def coil_material_type(self):
        raise AttributeError("Can't delete attribute")

    @property
    def cost_per_pound(self):
        return self._cost_per_pound

    @cost_per_pound.setter
    def cost_per_pound(self, value):
        if not isinstance(value, float):
            raise ValueError('cost_per_pound must be a float!')
        if value > 9999999:
            raise ValueError('cost_per_pound must less than 9999999!')
        self._cost_per_pound = value

    @cost_per_pound.deleter
    def cost_per_pound(self):
        raise AttributeError("Can't delete attribute")

    @property
    def non_exempt_scrap(self):
        return self._non_exempt_scrap

    @non_exempt_scrap.setter
    def non_exempt_scrap(self, value):
        if not isinstance(value, str):
            raise ValueError('non_exempt_scrap must be a string!')
        if len(value) > 9:
            raise ValueError('non_exempt_scrap must less than 9 characters!')
        self._non_exempt_scrap = value

    @non_exempt_scrap.deleter
    def non_exempt_scrap(self):
        raise AttributeError("Can't delete attribute")

    @property
    def exempt_scrap(self):
        return self._exempt_scrap

    @exempt_scrap.setter
    def exempt_scrap(self, value):
        if not isinstance(value, str):
            raise ValueError('exempt_scrap must be a string!')
        if len(value) > 9:
            raise ValueError('exempt_scrap must less than 9 characters!')
        self._exempt_scrap = value

    @exempt_scrap.deleter
    def exempt_scrap(self):
        raise AttributeError("Can't delete attribute")

    @property
    def other_adjustments(self):
        return self._other_adjustments

    @other_adjustments.setter
    def other_adjustments(self, value):
        if not isinstance(value, str):
            raise ValueError('other_adjustments must be a string!')
        if len(value) > 9:
            raise ValueError('other_adjustments must less than 9 characters!')
        self._other_adjustments = value

    @other_adjustments.deleter
    def other_adjustments(self):
        raise AttributeError("Can't delete attribute")

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if not isinstance(value, int):
            raise ValueError('weight must be an int!')
        if value > 9999999999:
            raise ValueError('weight must less than 9999999999!')
        self._weight = value

    @weight.deleter
    def weight(self):
        raise AttributeError("Can't delete attribute")

    @property
    def heat_number(self):
        return self._heat_number

    @heat_number.setter
    def heat_number(self, value):
        if not isinstance(value, str):
            raise ValueError('heat_number must be a string!')
        if len(value) > 20:
            raise ValueError('heat_number must less than 20 characters!')
        self._heat_number = value

    @heat_number.deleter
    def heat_number(self):
        raise AttributeError("Can't delete attribute")

    @property
    def vendor_code(self):
        return self._vendor_code

    @vendor_code.setter
    def vendor_code(self, value):
        if not isinstance(value, str):
            raise ValueError('vendor_code must be a string!')
        if len(value) > 16:
            raise ValueError('vendor_code must less than 16 characters!')
        self._vendor_code = value

    @vendor_code.deleter
    def vendor_code(self):
        raise AttributeError("Can't delete attribute")

    @property
    def purchase_order(self):
        return self._purchase_order

    @purchase_order.setter
    def purchase_order(self, value):
        if not isinstance(value, str):
            raise ValueError('purchase_order must be a string!')
        if len(value) > 10:
            raise ValueError('purchase_order must less than 10 characters!')
        self._purchase_order = value

    @purchase_order.deleter
    def purchase_order(self):
        raise AttributeError("Can't delete attribute")

    @property
    def storage_location(self):
        return self._storage_location

    @storage_location.setter
    def storage_location(self, value):
        if not isinstance(value, str):
            raise ValueError('storage_location must be a string!')
        if len(value) > 20:
            raise ValueError('storage_location must less than 20 characters!')
        self._storage_location = value

    @storage_location.deleter
    def storage_location(self):
        raise AttributeError("Can't delete attribute")

    def __str__(self):
        result = ''
        result += '"' + self.action_code + '",'
        result += '"' + self.coil_number + '",'
        if self.description:
            result += '"' + self.description + '",'
        else:
            result += '"",'
        if self.date_in:
            result += '"' + self.date_in + '",'
        else:
            result += '"",'
        if self.date_out:
            result += '"' + self.date_out + '",'
        else:
            result += '"",'
        if self.starting_length > 0:
            result += '"' + format(self.starting_length, '0.0f') + '",'
        else:
            result += '"",'
        if self.length_used > 0:
            result += '"' + format(self.length_used, '0.0f') + '",'
        else:
            result += '"",'
        if self.status:
            result += '"' + self.status + '",'
        else:
            result += '"",'
        if self.vendor_name:
            result += '"' + self.vendor_name + '",'
        else:
            result += '"",'
        if self.material_code:
            result += '"' + self.material_code + '",'
        else:
            result += '"",'
        if self.coil_material_type:
            result += '"' + self.coil_material_type + '",'
        else:
            result += '"",'
        if self.cost_per_pound >= 0:
            result += '"' + format(self.cost_per_pound, '0.2f') + '",'
        else:
            result += '"",'
        if self.non_exempt_scrap:
            result += '"' + self.non_exempt_scrap + '",'
        else:
            result += '"",'
        if self.exempt_scrap:
            result += '"' + self.exempt_scrap + '",'
        else:
            result += '"",'
        if self.other_adjustments:
            result += '"' + self.other_adjustments + '",'
        else:
            result += '"",'
        if self.weight >= 0:
            result += '"' + format(self.weight, '0.0f') + '",'
        else:
            result += '"",'
        if self.heat_number:
            result += '"' + self.heat_number + '",'
        else:
            result += '"",'
        if self.vendor_code:
            result += '"' + self.vendor_code + '",'
        else:
            result += '"",'
        if self.purchase_order:
            result += '"' + self.purchase_order + '",'
        else:
            result += '"",'
        if self.storage_location:
            result += '"' + self.storage_location + '"'
        else:
            result += '""'

        return result


class CoilItems:
    def __init__(self):
        self.coil_list = []

    def __str__(self):
        return '\n'.join(str(x) for x in self.coil_list)

    def append(self, bundle_item):
        self.coil_list.append(bundle_item)

    def save_as(self, file_name):
        self.file_name = file_name
        self.save()

    def save(self):
        test = open(self.file_name, 'w')
        test.write(str(self))
        test.close()
