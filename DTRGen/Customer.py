__author__ = "zanweb <zanweb@163.com>"

from .Base import _Call


class Customer(_Call):
    def __init__(self, action_code='', customer_code=0, customer_name='', customer_address_line1='',
                 customer_address_line2='', customer_city='', customer_state='', customer_zip='', customer_country='',
                 customer_instructions='', max_bundle_weight=0, delivery_phone='', e_mail_address=''):
        self.action_code = action_code
        self.customer_code = customer_code
        self.customer_name = customer_name
        self.customer_address_line1 = customer_address_line1
        self.customer_address_line2 = customer_address_line2
        self.customer_city = customer_city
        self.customer_state = customer_state
        self.customer_zip = customer_zip
        self.customer_country = customer_country
        self.customer_instructions = customer_instructions
        self.max_bundle_weight = max_bundle_weight
        self.delivery_phone = delivery_phone
        self.e_mail_address = e_mail_address

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
    def customer_code(self):
        return self._customer_code

    @customer_code.setter
    def customer_code(self, value):
        if not isinstance(value, int):
            raise ValueError('customer_code must be an int!')
        if value > 99999999999:
            raise ValueError('customer_code must less than 999999999999!')
        self._customer_code = value

    @customer_code.deleter
    def customer_code(self):
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
        if len(value) > 30:
            raise ValueError('customer_address_line1 must less than 30 characters!')
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
        if len(value) > 30:
            raise ValueError('customer_address_line2 must less than 30 characters!')
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
        if len(value) > 30:
            raise ValueError('customer_city must less than 30 characters!')
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
        if len(value) > 30:
            raise ValueError('customer_instructions must less than 30 characters!')
        self._customer_instructions = value

    @customer_instructions.deleter
    def customer_instructions(self):
        raise AttributeError("Can't delete attribute")

    @property
    def max_bundle_weight(self):
        return self._max_bundle_weight

    @max_bundle_weight.setter
    def max_bundle_weight(self, value):
        if not isinstance(value, int):
            raise ValueError('max_bundle_weight must be an int!')
        if value > 9999:
            raise ValueError('max_bundle_weight must less than 9999!')
        self._max_bundle_weight = value

    @max_bundle_weight.deleter
    def max_bundle_weight(self):
        raise AttributeError("Can't delete attribute")

    @property
    def delivery_phone(self):
        return self._delivery_phone

    @delivery_phone.setter
    def delivery_phone(self, value):
        if not isinstance(value, str):
            raise ValueError('delivery_phone must be a string!')
        if len(value) > 30:
            raise ValueError('delivery_phone must less than 30 characters!')
        self._delivery_phone = value

    @delivery_phone.deleter
    def delivery_phone(self):
        raise AttributeError("Can't delete attribute")

    @property
    def e_mail_address(self):
        return self._e_mail_address

    @e_mail_address.setter
    def e_mail_address(self, value):
        if not isinstance(value, str):
            raise ValueError('e_mail_address must be a string!')
        if len(value) > 100:
            raise ValueError('e_mail_address must less than 100 characters!')
        self._e_mail_address = value

    @e_mail_address.deleter
    def e_mail_address(self):
        raise AttributeError("Can't delete attribute")

    def __str__(self):
        result = ''
        result += '"' + self.action_code + '",'
        result += format(self.customer_code,'0.0f') + ','
        result += '"' + self.customer_name + '",'
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
        if self.max_bundle_weight:
            result += format(self.max_bundle_weight, '0.0f') + ','
        else:
            result += ','
        if self.delivery_phone:
            result += '"' + self.delivery_phone + '",'
        else:
            result += '"",'
        if self.e_mail_address:
            result += '"' + self.e_mail_address + '"'
        else:
            result += '""'

        return result


class Customers:
    def __init__(self):
        self.customer_list = []

    def __str__(self):
        return '\n'.join(str(x) for x in self.customer_list)

    def append(self, customer):
        self.customer_list.append(customer)

    def save_as(self, file_name):
        self.file_name = file_name
        self.save()

    def save(self):
        test = open(self.file_name, 'w')
        test.write(str(self))
        test.close()
