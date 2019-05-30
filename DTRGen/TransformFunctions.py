__author__ = "zanweb <zanweb@163.com>"

import time

from DTRGen.Order import *
from DTRGen.Part import *
from LysaghtPurlin.Batch import Batch
from LysaghtPurlin.Bundle import Bundle
from LysaghtPurlin.Order import Order
# from LysaghtPurlin import Order
from Zfile import zCSV, zFBase


def lysaght_to_dtr(orders, file_path):
    mm_inch = 25.4
    tool_list = get_dtr_tools('./DTRTools.csv')

    order_list = CutList()
    part_list = Parts()
    for batch in orders.batches:
        for bundle in batch.bundles:
            for part in bundle.parts:
                orders.product_code = 'CEES'
                part.material = 'C00000'
                order_item = CutItem(order_number=orders.order_no, bundle=bundle.bundle_no,part_number=part.part_no,
                                     quantity=part.quantity, length=float(part.part_length)/mm_inch, material=part.material,
                                     product_code=orders.product_code, part_option='R', item_id=part.part_no,
                                     action='C')
                order_list.append(order_item)
                # print(part.dtr_holes)
                for dtr_hole in part.dtr_holes:
                    # print('dtr_hole.group_type-->{0}'.format(dtr_hole.group_type))
                    if dtr_hole.group_type == 'double hole':
                        tool_num = get_dtr_tool_id(tool_list, dtr_hole.dia, dtr_hole.gauge)
                        if tool_num > 0:
                            part_item = Part(part_name=part.part_no, tool_number=tool_num,
                                             x_offset=dtr_hole.group_x/mm_inch,
                                             x_reference=dtr_hole.group_x_reference, permanent=True,
                                             y_offset=dtr_hole.group_y/mm_inch,
                                             y_reference=dtr_hole.group_y_reference)
                            part_list.append(part_item)
                        else:
                            print('This type of double tool_id is not defined! dia={0} * gauge={0}'.format(dtr_hole.dia,
                                                                                                           dtr_hole.gauge))
                            return 0
                    else:
                        tool_num = get_dtr_tool_id(tool_list, dtr_hole.dia, dtr_hole.gauge)
                        if tool_num > 0:
                            part_item = Part(part_name=part.part_no, tool_number=tool_num, x_offset=dtr_hole.x/mm_inch,
                                             x_reference=dtr_hole.x_reference, permanent=True,
                                             y_offset=dtr_hole.y/mm_inch,
                                             y_reference=dtr_hole.y_reference)
                            part_list.append(part_item)
                        else:
                            print('This type of single tool_id is not defined! dia={0} * gauge={0}'.format(dtr_hole.dia,
                                                                                                           dtr_hole.gauge))
                            # print(part_list)
                            return 0
    # print(order_list)
    # print(part_list)
    # file_path += 'D' + time.strftime('%y%m%d', time.localtime()) + '0'  # str(random.randint(0, 9))
    file_path += 'D' + '0'*7
    # print(file_path)
    order_list.save_as(file_path + '.ORD')
    part_list.save_as(file_path + '.PRT')


def get_dtr_tools(file_with_path):
    csv_f = zCSV.CsvFile(file_with_path)
    tool_list = csv_f.get_tool_id()
    # print(tool_list)
    return tool_list


def get_dtr_tool_id(tool_list, dia, gauge):
    for tool in tool_list:
        if tool['Dia'] == dia:
            if tool['Gauge'] == gauge:
                return tool['ToolID']
    return -1


def get_lysaght_dias(file_with_path):
    csv_f = zCSV.CsvFile(file_with_path)
    dia_list = csv_f.get_lysaght_dia_no()
    return dia_list


def get_lysaght_real_dia(dia_list, dia_no):
    for dia_item in dia_list:
        if dia_item['DiaNo'] == dia_no:
            return dia_item['Dia']
    return -1


def read_data_from_lysaght_engine(file_path):
    orders = []
    try:
        lysaght_dia_list = get_lysaght_dias('./LysaghtHoleDia.csv')
        order_files = []
        punch_files = []
        order_files_list = zFBase.get_indicate_ext_file(file_path, 'txt')
        punch_files_list = zFBase.get_indicate_ext_file(file_path, 'csv')
        for one_item in order_files_list:
            order_files.append(file_path + one_item + '.txt')
        for one_item in punch_files_list:
            punch_files.append(file_path + one_item + '.csv')
        for order_file in order_files:
            order = Order('', '', '')
            one_order = order.get_order_no_from_lysaght_txt(order_file)
            batch = Batch(176590)
            bundle = Bundle(7)
            for punch_file in punch_files:
                punch = zCSV.CsvFile(punch_file)
                punches = punch.get_lysaght_punch()
                for one_part in punches:
                    one_part.change_dia_no_to_real_dia(lysaght_dia_list)
                    one_part.sort_holes()
                    one_part.group_holes_by_y()
                    one_part.convert_to_dtr_holes()
                    bundle.add_part(one_part)
                batch.add_bundle(bundle)
            order.add_batch(batch)
            orders.append(order)
    except Exception as e:
        print(e)
    finally:
        return orders


if __name__ == '__main__':
    tool_dtr = get_dtr_tools('../DTRTools.csv')
    print(tool_dtr)
    tool_id = get_dtr_tool_id(tool_dtr, 16.0, 230.0)

    print(tool_id)
    # lysaght_orders = Order()
    # lysaght_to_dtr(lysaght_orders, file_path=None)
