__author__ = "zanweb <zanweb@163.com>"

from .Base import _Call


class BundleItemAll(_Call):
    def __init__(self, order_number='', material_code='', product_code='', bundle=0, user1='', user2='', user3='',
                 user4='', user5='', bundle_label='', part_label='', kit_name='', bundle_format='', part_format='',
                 customer_name='', customer_address_line1='', customer_address_line2='', customer_city='',
                 customer_state='', customer_zip='', customer_country='', customer_instructions='', staging_bay='',
                 loading_dock='', work_order='', truck_number='', required_date='', product_code_group='', hold=False):
        self.order_number = order_number
        self.material_code = material_code
        self.product_code = product_code
        self.bundle = bundle
        self.user1 = user1
        self.user2 = user2
        self.user3 = user3
        self.user4 = user4
        self.user5 = user5
        self.bundle_label = bundle_label
        self.part_label = part_label
        self.kit_name = kit_name
        self.bundle_format = bundle_format
        self.part_format = part_format
        self.customer_name = customer_name
        self.customer_address_line1 = customer_address_line1
        self.customer_address_line2 = customer_address_line2
        self.customer_city = customer_city
        self.customer_state = customer_state
        self.customer_zip = customer_zip
        self.customer_country = customer_country
        self.customer_instructions = customer_instructions
        self.staging_bay = staging_bay
        self.loading_dock = loading_dock
        self.work_order = work_order
        self.truck_number = truck_number
        self.required_date = required_date
        self.product_code_group = product_code_group
        self.hold = hold

    @property
    def order_number(self):
        return self._order_number

    @order_number.setter
    def order_number(self, value):
        if not isinstance(value, str):
            raise ValueError('order_number must be a string!')
        if len(value) > 20:
            raise ValueError('order_number must less than 20 characters!')
        self._order_number = value

    @order_number.deleter
    def order_number(self):
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
    def product_code(self):
        return self._product_code

    @product_code.setter
    def product_code(self, value):
        if not isinstance(value, str):
            raise ValueError('product_code must be a string!')
        if len(value) > 20:
            raise ValueError('product_code must less than 20 characters !')
        self._product_code = value

    @product_code.deleter
    def product_code(self):
        raise AttributeError("Can't delete attribute")

    @property
    def bundle(self):
        return self._bundle

    @bundle.setter
    def bundle(self, value):
        if not isinstance(value, int):
            raise ValueError('bundle must be an int!')
        if value > 999:
            raise ValueError('bundle must less than 999!')
        self._bundle = value

    @bundle.deleter
    def bundle(self):
        raise AttributeError("Can't delete attribute")

    @property
    def user1(self):
        return self._user1

    @user1.setter
    def user1(self, value):
        if not isinstance(value, str):
            raise ValueError('user1 must be a string!')
        if len(value) > 254:
            raise ValueError('user1 must less than 254 characters!')
        self._user1 = value

    @user1.deleter
    def user1(self):
        raise AttributeError("Can't delete attribute")

    @property
    def user2(self):
        return self._user2

    @user2.setter
    def user2(self, value):
        if not isinstance(value, str):
            raise ValueError('user2 must be a string!')
        if len(value) > 254:
            raise ValueError('user2 must less than 254 characters!')
        self._user2 = value

    @user2.deleter
    def user2(self):
        raise AttributeError("Can't delete attribute")

    @property
    def user3(self):
        return self._user3

    @user3.setter
    def user3(self, value):
        if not isinstance(value, str):
            raise ValueError('user3 must be a string!')
        if len(value) > 254:
            raise ValueError('user3 must less than 254 characters!')
        self._user3 = value

    @user3.deleter
    def user3(self):
        raise AttributeError("Can't delete attribute")

    @property
    def user4(self):
        return self._user4

    @user4.setter
    def user4(self, value):
        if not isinstance(value, str):
            raise ValueError('user4 must be a string!')
        if len(value) > 254:
            raise ValueError('user4 must less than 254 characters!')
        self._user4 = value

    @user4.deleter
    def user4(self):
        raise AttributeError("Can't delete attribute")

    @property
    def user5(self):
        return self._user5

    @user5.setter
    def user5(self, value):
        if not isinstance(value, str):
            raise ValueError('user5 must be a string!')
        if len(value) > 254:
            raise ValueError('user5 must less than 254 characters!')
        self._user5 = value

    @user5.deleter
    def user5(self):
        raise AttributeError("Can't delete attribute")

    @property
    def bundle_label(self):
        return self._bundle_label

    @bundle_label.setter
    def bundle_label(self, value):
        if not isinstance(value, str):
            raise ValueError('bundle_label must be a string!')
        if len(value) > 254:
            raise ValueError('bundle_label must less than 254 characters !')
        self._bundle_label = value

    @bundle_label.deleter
    def bundle_label(self):
        raise AttributeError("Can't delete attribute")

    @property
    def part_label(self):
        return self._part_label

    @part_label.setter
    def part_label(self, value):
        if not isinstance(value, str):
            raise ValueError('part_label must be a string!')
        if len(value) > 254:
            raise ValueError('part_label must less than 254 characters !')
        self._part_label = value

    @part_label.deleter
    def part_label(self):
        raise AttributeError("Can't delete attribute")

    @property
    def kit_name(self):
        return self._kit_name

    @kit_name.setter
    def kit_name(self, value):
        if not isinstance(value, str):
            raise ValueError('kit_name must be a string!')
        if len(value) > 24:
            raise ValueError('kit_name must less than 24 characters !')
        self._kit_name = value

    @kit_name.deleter
    def kit_name(self):
        raise AttributeError("Can't delete attribute")

    @property
    def bundle_format(self):
        return self._bundle_format

    @bundle_format.setter
    def bundle_format(self, value):
        if not isinstance(value, str):
            raise ValueError('bundle_format must be a string!')
        if len(value) > 12:
            raise ValueError('bundle_format must less than 12 characters!')
        self._bundle_format = value

    @bundle_format.deleter
    def bundle_format(self):
        raise AttributeError("Can't delete attribute")

    @property
    def part_format(self):
        return self._part_format

    @part_format.setter
    def part_format(self, value):
        if not isinstance(value, str):
            raise ValueError('part_format must be a string!')
        if len(value) > 12:
            raise ValueError('part_format must less than 12 characters!')
        self._part_format = value

    @part_format.deleter
    def part_format(self):
        raise AttributeError("Can't delete attribute")

    @property
    def customer_name(self):
        return self._customer_name

    @customer_name.setter
    def customer_name(self, value):
        if not isinstance(value, str):
            raise ValueError('customer_name must be a string!')
        if len(value) > 30:
            raise ValueError('customer_name must less than 30 characters!')
        self._customer_name = value

    @customer_name.deleter
    def customer_name(self):
        raise AttributeError("Can't delete attribute")

    @property
    def customer_address_line1(self):
        return self._customer_address_line1

    @customer_address_line1.setter
    def customer_address_line1(self, value):
        if not isinstance(value, str):
            raise ValueError('customer_address_line1 must be a string!')
        if len(value) > 254:
            raise ValueError('customer_address_line1 must less than 254 characters!')
        self._customer_address_line1 = value

    @customer_address_line1.deleter
    def customer_address_line1(self):
        raise AttributeError("Can't delete attribute")

    @property
    def customer_address_line2(self):
        return self._customer_address_line2

    @customer_address_line2.setter
    def customer_address_line2(self, value):
        if not isinstance(value, str):
            raise ValueError('customer_address_line2 must be a string!')
        if len(value) > 254:
            raise ValueError('customer_address_line2 must less than 254 characters!')
        self._customer_address_line2 = value

    @customer_address_line2.deleter
    def customer_address_line2(self):
        raise AttributeError("Can't delete attribute")

    @property
    def customer_city(self):
        return self._customer_city

    @customer_city.setter
    def customer_city(self, value):
        if not isinstance(value, str):
            raise ValueError('customer_city must be a string!')
        if len(value) > 254:
            raise ValueError('customer_city must less than 254 characters!')
        self._customer_city = value

    @customer_city.deleter
    def customer_city(self):
        raise AttributeError("Can't delete attribute")

    @property
    def customer_state(self):
        return self._customer_state

    @customer_state.setter
    def customer_state(self, value):
        if not isinstance(value, str):
            raise ValueError('customer_state must be a string!')
        if len(value) > 2:
            raise ValueError('customer_state must less than 2 characters!')
        self._customer_state = value

    @customer_state.deleter
    def customer_state(self):
        raise AttributeError("Can't delete attribute")

    @property
    def customer_zip(self):
        return self._customer_zip

    @customer_zip.setter
    def customer_zip(self, value):
        if not isinstance(value, str):
            raise ValueError('customer_zip must be a string!')
        if len(value) > 10:
            raise ValueError('customer_zip must less than 10 characters!')
        self._customer_zip = value

    @customer_zip.deleter
    def customer_zip(self):
        raise AttributeError("Can't delete attribute")

    @property
    def customer_country(self):
        return self._customer_country

    @customer_country.setter
    def customer_country(self, value):
        if not isinstance(value, str):
            raise ValueError('customer_country must be a string!')
        if len(value) > 3:
            raise ValueError('customer_country must less than 3 characters!')
        self._customer_country = value

    @customer_country.deleter
    def customer_country(self):
        raise AttributeError("Can't delete attribute")

    @property
    def customer_instructions(self):
        return self._customer_instructions

    @customer_instructions.setter
    def customer_instructions(self, value):
        if not isinstance(value, str):
            raise ValueError('customer_instructions must be a string!')
        if len(value) > 254:
            raise ValueError('customer_instructions must less than 254 characters!')
        self._customer_instructions = value

    @customer_instructions.deleter
    def customer_instructions(self):
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
    def work_order(self):
        return self._work_order

    @work_order.setter
    def work_order(self, value):
        if not isinstance(value, str):
            raise ValueError('work_order must be a string!')
        if len(value) > 18:
            raise ValueError('work_order must less than 18 characters!')
        self._work_order = value

    @work_order.deleter
    def work_order(self):
        raise AttributeError("Can't delete attribute")

    @property
    def truck_number(self):
        return self._truck_number

    @truck_number.setter
    def truck_number(self, value):
        if not isinstance(value, str):
            raise ValueError('truck_number must be a string!')
        if len(value) > 12:
            raise ValueError('truck_number must less than 12 characters!')
        self._truck_number = value

    @truck_number.deleter
    def truck_number(self):
        raise AttributeError("Can't delete attribute")

    @property
    def required_date(self):
        return self._required_date

    @required_date.setter
    def required_date(self, value):
        if not isinstance(value, str):
            raise ValueError('required_date must be a string!')
        if len(value) > 8:
            raise ValueError('required_date must less than 8 characters!')
        self._required_date = value

    @required_date.deleter
    def required_date(self):
        raise AttributeError("Can't delete attribute")

    @property
    def product_code_group(self):
        return self._product_code_group

    @product_code_group.setter
    def product_code_group(self, value):
        if not isinstance(value, str):
            raise ValueError('product_code_group must be a string!')
        if len(value) > 12:
            raise ValueError('product_code_group must less than 12 characters!')
        self._product_code_group = value

    @product_code_group.deleter
    def product_code_group(self):
        raise AttributeError("Can't delete attribute")

    @property
    def hold(self):
        return self._hold

    @hold.setter
    def hold(self, value):
        if not isinstance(value, bool):
            raise ValueError('hold must be a bool!')
        # if len(value) > 12:
        #     raise ValueError('hold must less than 12 characters!')
        self._hold = value

    @hold.deleter
    def hold(self):
        raise AttributeError("Can't delete attribute")

    def __str__(self):
        result = ''
        result += '"' + self.order_number + '",'
        result += '"' + self.material_code + '",'
        result += '"' + self.product_code + '",'
        if self.bundle >= 0:
            result += format(self.bundle, '0.0f') + ','
        else:
            result += ','
        if self.user1:
            result += '"' + self.user1 + '",'
        else:
            result += '"",'
        if self.user2:
            result += '"' + self.user2 + '",'
        else:
            result += '"",'
        if self.user3:
            result += '"' + self.user3 + '",'
        else:
            result += '"",'
        if self.user4:
            result += '"' + self.user4 + '",'
        else:
            result += '"",'
        if self.user5:
            result += '"' + self.user5 + '",'
        else:
            result += '"",'
        if self.bundle_label:
            result += '"' + self.bundle_label + '",'
        else:
            result += '"",'
        if self.part_label:
            result += '"' + self.part_label + '",'
        else:
            result += '"",'
        if self.kit_name:
            result += '"' + self.kit_name + '",'
        else:
            result += '"",'
        if self.bundle_format:
            result += '"' + self.bundle_format + '",'
        else:
            result += '"",'
        if self.part_format:
            result += '"' + self.part_format + '",'
        else:
            result += '"",'
        if self.customer_name:
            result += '"' + self.customer_name + '",'
        else:
            result += '"",'
        if self.customer_address_line1:
            result += '"' + self.customer_address_line1 + '",'
        else:
            result += '"",'
        if self.customer_address_line2:
            result += '"' + self.customer_address_line2 + '",'
        else:
            result += '"",'
        if self.customer_city:
            result += '"' + self.customer_city + '",'
        else:
            result += '"",'
        if self.customer_state:
            result += '"' + self.customer_state + '",'
        else:
            result += '"",'
        if self.customer_zip:
            result += '"' + self.customer_zip + '",'
        else:
            result += '"",'
        if self.customer_country:
            result += '"' + self.customer_country + '",'
        else:
            result += '"",'
        if self.customer_instructions:
            result += '"' + self.customer_instructions + '",'
        else:
            result += '"",'
        if self.staging_bay:
            result += '"' + self.staging_bay + '",'
        else:
            result += '"",'
        if self.loading_dock:
            result += '"' + self.loading_dock + '",'
        else:
            result += '"",'
        if self.work_order:
            result += '"' + self.work_order + '",'
        else:
            result += '"",'
        if self.truck_number:
            result += '"' + self.truck_number + '",'
        else:
            result += '"",'
        if self.required_date:
            result += '' + self.required_date + ','
        else:
            result += '"",'
        if self.product_code_group:
            result += '"' + self.product_code_group + '",'
        else:
            result += '"",'
        if self.hold:
            if self.hold is True:
                result += '"T"'
            else:
                result += '"F"'
        else:
            result += 'F'

        return result


class BundleItem(BundleItemAll):
    def __init__(self, order_number='', material_code='', product_code='', bundle=0, user1='', user2='', user3='',
                 user4='', user5='', bundle_label='', part_label='', kit_name='', bundle_format='', part_format=''):
        super().__init__()
        self.order_number = order_number
        self.material_code = material_code
        self.product_code = product_code
        self.bundle = bundle
        self.user1 = user1
        self.user2 = user2
        self.user3 = user3
        self.user4 = user4
        self.user5 = user5
        self.bundle_label = bundle_label
        self.part_label = part_label
        self.kit_name = kit_name
        self.bundle_format = bundle_format
        self.part_format = part_format

    def __str__(self):
        result = ''
        result += '"' + self.order_number + '",'
        result += '"' + self.material_code + '",'
        result += '"' + self.product_code + '",'
        if self.bundle >= 0:
            result += format(self.bundle, '0.0f') + ','
        else:
            result += ','
        if self.user1:
            result += '"' + self.user1 + '",'
        else:
            result += '"",'
        if self.user2:
            result += '"' + self.user2 + '",'
        else:
            result += '"",'
        if self.user3:
            result += '"' + self.user3 + '",'
        else:
            result += '"",'
        if self.user4:
            result += '"' + self.user4 + '",'
        else:
            result += '"",'
        if self.user5:
            result += '"' + self.user5 + '",'
        else:
            result += '"",'
        if self.bundle_label:
            result += '"' + self.bundle_label + '",'
        else:
            result += '"",'
        if self.part_label:
            result += '"' + self.part_label + '",'
        else:
            result += '"",'
        if self.kit_name:
            result += '"' + self.kit_name + '",'
        else:
            result += '"",'
        if self.bundle_format:
            result += '"' + self.bundle_format + '",'
        else:
            result += '",'
        if self.part_format:
            result += '"' + self.part_format + '"'
        else:
            result += '""'

        return result


class BundleItems:
    def __init__(self):
        self.bundle_list = []

    def __str__(self):
        return '\n'.join(str(x) for x in self.bundle_list)

    def append(self, bundle_item):
        self.bundle_list.append(bundle_item)

    def save_as(self, file_name):
        self.file_name = file_name
        self.save()

    def save(self):
        test = open(self.file_name, 'w')
        test.write(str(self))
        test.close()
