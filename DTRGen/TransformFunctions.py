__author__ = "zanweb <zanweb@163.com>"

import time

from DTRGen.Order import *
from DTRGen.Part import *
# from LysaghtPurlin import Order
from Zfile import zCSV


def lysaght_to_dtr(orders, file_path):
    tool_list = get_dtr_tools('./Tool.csv')

    order_list = CutList()
    part_list = Parts()
    for batch in orders.batches:
        for bundle in batch.bundles:
            for part in bundle.parts:
                order_item = CutItem(order_number=orders.order_no, bundle=bundle.bundle_no,
                                     quantity=part.quantity, length=float(part.part_length), material=part.material,
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
                                             x_offset=dtr_hole.group_x,
                                             x_reference=dtr_hole.group_x_reference, permanent=True,
                                             y_offset=dtr_hole.group_y,
                                             y_reference=dtr_hole.group_y_reference)
                            part_list.append(part_item)
                        else:
                            print('This type of double tool_id is not defined! dia={0} * gauge={0}'.format(dtr_hole.dia,
                                                                                                           dtr_hole.gauge))
                            return 0
                    else:
                        tool_num = get_dtr_tool_id(tool_list, dtr_hole.dia, dtr_hole.gauge)
                        if tool_num > 0:
                            part_item = Part(part_name=part.part_no, tool_number=tool_num, x_offset=dtr_hole.x,
                                             x_reference=dtr_hole.x_reference, permanent=True,
                                             y_offset=dtr_hole.y,
                                             y_reference=dtr_hole.y_reference)
                            part_list.append(part_item)
                        else:
                            print('This type of single tool_id is not defined! dia={0} * gauge={0}'.format(dtr_hole.dia,
                                                                                                           dtr_hole.gauge))
                            # print(part_list)
                            return 0
    print(order_list)
    print(part_list)
    file_path += 'D' + time.strftime('%y%m%d', time.localtime()) + '0'  # str(random.randint(0, 9))
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


if __name__ == '__main__':
    tool_dtr = get_dtr_tools('../Tool.csv')
    print(tool_dtr)
    tool_id = get_dtr_tool_id(tool_dtr, 16.0, 230.0)

    print(tool_id)
    # lysaght_orders = Order()
    # lysaght_to_dtr(lysaght_orders, file_path=None)
