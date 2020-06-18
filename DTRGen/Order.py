__author__ = "zanweb <zanweb@163.com>"

from itertools import groupby
from operator import attrgetter

from .Base import _Call


class CutItem(_Call):
    def __init__(self, order_number='', bundle=0, quantity=0, length=0.0, material='', product_code='', part_option='R',
                 item_id='', action='', bundle_label='', part_label='', kit_name='',
                 part_number='', message='', schedule_date='', machine=0, items_user1='', items_user2='',
                 hole_offset=0.0, hole_count=0, stagger='', part_format_name='', bundle_format_name='', items_user3='',
                 items_user4='', items_user5='', bundle_code='', sku=''):
        self.bundle_label = bundle_label
        self.part_label = part_label
        self.kit_name = kit_name
        self.item_id = item_id
        self.action = action
        self.order_number = order_number
        self.bundle = bundle
        self.quantity = quantity
        self.length = length
        self.material = material
        self.product_code = product_code
        self.part_option = part_option
        self.part_number = part_number
        self.message = message
        self.schedule_date = schedule_date
        self.machine = machine
        self.items_user1 = items_user1
        self.items_user2 = items_user2
        self.hole_offset = hole_offset
        self.hole_count = hole_count
        self.stagger = stagger
        self.part_format_name = part_format_name
        self.bundle_format_name = bundle_format_name
        self.items_user3 = items_user3
        self.items_user4 = items_user4
        self.items_user5 = items_user5
        self.bundle_code = bundle_code
        self.sku = sku

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
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if not isinstance(value, int):
            raise ValueError('quantity must be an int!')
        if value > 9999:
            raise ValueError('quantity must less than 999!')
        self._quantity = value

    @quantity.deleter
    def quantity(self):
        raise AttributeError("Can't delete attribute")

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        if not isinstance(value, float):
            raise ValueError('length must be a float!')
        if value > 999999999:
            raise ValueError('length must less than 999999999!')
        self._length = value

    @length.deleter
    def length(self):
        raise AttributeError("Can't delete attribute")

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, value):
        if not isinstance(value, str):
            raise ValueError('material must be a string!')
        if len(value) > 20:
            raise ValueError('material must less than 20 characters !')
        self._material = value

    @material.deleter
    def material(self):
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
    def part_option(self):
        return self._part_option

    @part_option.setter
    def part_option(self, value):
        if not isinstance(value, str):
            raise ValueError('part_option must be a string!')
        if value not in ["R", "L", "A", "M"]:
            raise ValueError('part_option must in list ["R", "L", "A", "M"]!')
        self._part_option = value

    @part_option.deleter
    def part_option(self):
        raise AttributeError("Can't delete attribute")

    @property
    def part_number(self):
        return self._part_number

    @part_number.setter
    def part_number(self, value):
        if not isinstance(value, str):
            raise ValueError('part_number must be a string!')
        if len(value) > 30:
            raise ValueError('part_number must less than 30 characters !')
        self._part_number = value

    @part_number.deleter
    def part_number(self):
        raise AttributeError("Can't delete attribute")

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        if not isinstance(value, str):
            raise ValueError('message must be a string!')
        if len(value) > 40:
            raise ValueError('message must less than 40 characters !')
        self._message = value

    @message.deleter
    def message(self):
        raise AttributeError("Can't delete attribute")

    @property
    def schedule_date(self):
        return self._schedule_date

    @schedule_date.setter
    def schedule_date(self, value):
        if not isinstance(value, str):
            raise ValueError('schedule_date must be a string!')
        if len(value) > 8:
            raise ValueError('schedule_date must less than 8 characters !')
        self._schedule_date = value

    @schedule_date.deleter
    def schedule_date(self):
        raise AttributeError("Can't delete attribute")

    @property
    def item_id(self):
        return self._item_id

    @item_id.setter
    def item_id(self, value):
        if not isinstance(value, str):
            raise ValueError('item_id must be a string!')
        if len(value) > 20:
            raise ValueError('item_id must less than 20 characters !')
        self._item_id = value

    @item_id.deleter
    def item_id(self):
        raise AttributeError("Can't delete attribute")

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        if not isinstance(value, str):
            raise ValueError('action must be a string!')
        if value not in ["C", "Q", "R"]:
            raise ValueError('action must in list ["C", "Q", "R"]!')
        self._action = value

    @action.deleter
    def action(self):
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
    def machine(self):
        return self._machine

    @machine.setter
    def machine(self, value):
        if not isinstance(value, int):
            raise ValueError('machine must be an int!')
        if value > 99:
            raise ValueError('machine must less than 99!')
        self._machine = value

    @machine.deleter
    def machine(self):
        raise AttributeError("Can't delete attribute")

    @property
    def items_user1(self):
        return self._items_user1

    @items_user1.setter
    def items_user1(self, value):
        if not isinstance(value, str):
            raise ValueError('items_user1 must be a string!')
        if len(value) > 254:
            raise ValueError('items_user1 must less than 254 characters!')
        self._items_user1 = value

    @items_user1.deleter
    def items_user1(self):
        raise AttributeError("Can't delete attribute")

    @property
    def items_user2(self):
        return self._items_user2

    @items_user2.setter
    def items_user2(self, value):
        if not isinstance(value, str):
            raise ValueError('items_user2 must be a string!')
        if len(value) > 254:
            raise ValueError('items_user2 must less than 254 characters!')
        self._items_user2 = value

    @items_user2.deleter
    def items_user2(self):
        raise AttributeError("Can't delete attribute")

    @property
    def items_user3(self):
        return self._items_user3

    @items_user3.setter
    def items_user3(self, value):
        if not isinstance(value, str):
            raise ValueError('items_user3 must be a string!')
        if len(value) > 254:
            raise ValueError('items_user3 must less than 254 characters!')
        self._items_user3 = value

    @items_user3.deleter
    def items_user3(self):
        raise AttributeError("Can't delete attribute")

    @property
    def items_user4(self):
        return self._items_user4

    @items_user4.setter
    def items_user4(self, value):
        if not isinstance(value, str):
            raise ValueError('items_user4 must be a string!')
        if len(value) > 254:
            raise ValueError('items_user4 must less than 254 characters!')
        self._items_user4 = value

    @items_user4.deleter
    def items_user4(self):
        raise AttributeError("Can't delete attribute")

    @property
    def items_user5(self):
        return self._items_user5

    @items_user5.setter
    def items_user5(self, value):
        if not isinstance(value, str):
            raise ValueError('items_user5 must be a string!')
        if len(value) > 254:
            raise ValueError('items_user5 must less than 254 characters!')
        self._items_user5 = value

    @items_user5.deleter
    def items_user5(self):
        raise AttributeError("Can't delete attribute")

    @property
    def hole_offset(self):
        return self._hole_offset

    @hole_offset.setter
    def hole_offset(self, value):
        if not isinstance(value, float):
            raise ValueError('hole_offset must be a float!')
        if value > 99999999:
            raise ValueError('hole_offset must less than 99999999!')
        self._hole_offset = value

    @hole_offset.deleter
    def hole_offset(self):
        raise AttributeError("Can't delete attribute")

    @property
    def hole_count(self):
        return self._hole_count

    @hole_count.setter
    def hole_count(self, value):
        if not isinstance(value, int):
            raise ValueError('hole_count must be an int !')
        if value > 9999:
            raise ValueError('hole_count must less than 9999!')
        self._hole_count = value

    @hole_count.deleter
    def hole_count(self):
        raise AttributeError("Can't delete attribute")

    @property
    def stagger(self):
        return self._stagger

    @stagger.setter
    def stagger(self, value):
        if not isinstance(value, str):
            raise ValueError('stagger must be a string!')
        if value not in ["S", ""]:
            raise ValueError('stagger must in list ["S", ""]!')
        self._stagger = value

    @stagger.deleter
    def stagger(self):
        raise AttributeError("Can't delete attribute")

    @property
    def part_format_name(self):
        return self._part_format_name

    @part_format_name.setter
    def part_format_name(self, value):
        if not isinstance(value, str):
            raise ValueError('part_format_name must be a string!')
        if len(value) > 12:
            raise ValueError('part_format_name must less than 12 characters!')
        self._part_format_name = value

    @part_format_name.deleter
    def part_format_name(self):
        raise AttributeError("Can't delete attribute")

    @property
    def bundle_format_name(self):
        return self._bundle_format_name

    @bundle_format_name.setter
    def bundle_format_name(self, value):
        if not isinstance(value, str):
            raise ValueError('bundle_format_name must be a string!')
        if len(value) > 12:
            raise ValueError('bundle_format_name must less than 12 characters!')
        self._bundle_format_name = value

    @bundle_format_name.deleter
    def bundle_format_name(self):
        raise AttributeError("Can't delete attribute")

    @property
    def bundle_code(self):
        return self._bundle_code

    @bundle_code.setter
    def bundle_code(self, value):
        if not isinstance(value, str):
            raise ValueError('bundle_code must be a string!')
        if len(value) > 15:
            raise ValueError('bundle_code must less than 15 characters!')
        self._bundle_code = value

    @bundle_code.deleter
    def bundle_code(self):
        raise AttributeError("Can't delete attribute")

    @property
    def sku(self):
        return self._sku

    @sku.setter
    def sku(self, value):
        if not isinstance(value, str):
            raise ValueError('sku must be a string!')
        if len(value) > 50:
            raise ValueError('sku must less than 50 characters!')
        self._sku = value

    @sku.deleter
    def sku(self):
        raise AttributeError("Can't delete attribute")

    def __str__(self):
        result = ""
        result += '"' + self.order_number + '",'
        result += format(self.bundle, "0.0f") + ','
        result += format(self.quantity, "0.0f") + ','
        result += format(self.length, "0.3f") + ','
        result += '"' + self.material + '",'
        if self.message:
            result += '"' + self.message + '",'
        else:
            result += '"",'
        result += '"' + self.product_code + '",'
        if self.part_number:
            result += '"' + self.part_number + '",'
        else:
            result += '"",'
        result += '"' + self.part_option + '",'
        if self._bundle_label:
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
        result += '"' + self.item_id + '",'
        result += '"' + self.action + '",'
        if self.schedule_date:
            result += '"' + self.schedule_date + '",'
        else:
            result += '"",'
        if self.machine:
            result += format(self.machine, "0.0f") + ','
        else:
            result += ','
        if self.items_user1:
            result += '"' + self.items_user1 + '",'
        else:
            result += '"",'
        if self.items_user2:
            result += '"' + self.items_user2 + '",'
        else:
            result += '"",'
        if self.hole_offset:
            result += format(self.hole_offset, '0.3f') + ','
        else:
            result += ','
        if self.hole_count:
            result += format(self.hole_count, '0.0f') + ','
        else:
            result += ','
        if self.stagger:
            result += '"' + self.stagger + '",'
        else:
            result += '"",'
        if self.part_format_name:
            result += '"' + self.part_format_name + '",'
        else:
            result += '"",'
        if self.bundle_format_name:
            result += '"' + self.bundle_format_name + '",'
        else:
            result += '"",'
        if self.items_user3:
            result += '"' + self.items_user3 + '",'
        else:
            result += '"",'
        if self.items_user4:
            result += '"' + self.items_user4 + '",'
        else:
            result += '"",'
        if self.items_user5:
            result += '"' + self.items_user5 + '",'
        else:
            result += '"",'
        if self.bundle_code:
            result += '"' + self.bundle_code + '"'
        else:
            result += '""'
        # result += '"","",'
        # if self.sku:
        #     result += '"' + self.sku + '"'
        # else:
        #     result += '""'
        return result


class CutList:
    def __init__(self):
        # self.cut_list = [UNITES]
        self.cut_list = []
        self.file_name = ''

    def __str__(self):
        return '\n'.join(str(x) for x in self.cut_list)

    def append(self, cut_item):
        self.cut_list.append(cut_item)

    def extend(self, cut_list):
        self.cut_list.extend(cut_list)

    def save_as(self, file_name):
        self.file_name = file_name
        self.save()

    def save(self):
        test = open(self.file_name, 'w')
        test.write(str(self))
        test.close()

    def save_list(self, file_name):
        list_context = '     Batch,       Raw,    Bundle,                        PartNo,    Length,       Qty,       Cat, User1'
        for material_index, material_group in groupby(self.cut_list, key=attrgetter('material')):
            list_context += '\n' + str(self.cut_list[0].order_number).rjust(10) + str(material_index).rjust(10)
            list_context += '\n' + '-' * 122
            for bundle_index, bundle_group in groupby(material_group, key=attrgetter('bundle')):
                for bundle_one in bundle_group:
                    list_context += '\n' + ' ' * 22 + str(bundle_one.bundle).rjust(10) + ',' + str(
                        bundle_one.part_number).rjust(30) + ',' + str(int(bundle_one.length * 25.4)).rjust(
                        10) + ',' + str(
                        bundle_one.quantity).rjust(10) + ',' + str(bundle_one.product_code).rjust(10) + ',' + bundle_one.items_user1
        list_file = open(file_name, 'w')
        list_file.write(list_context)
        list_file.close()
