from functools import reduce

__author__ = "zanweb <zanweb@163.com>"

# import os
# from LysaghtPurlin.Batch import Batch
# from LysaghtPurlin.Bundle import Bundle
# from LysaghtPurlin.Order import Order
# from LysaghtPurlin import Order
# from LysaghtPurlin import Part
# from DBbase import dbunit, genSQL

import LysaghtPurlin.Part as lpart
from CamGen.NCBase import *
from DTRGen.Order import *
from DTRGen.Part import *
from LysaghtPurlin import Batch
from LysaghtPurlin import Bundle
from LysaghtPurlin import Order
from Zfile import zCSV, zFBase
from zBase.constant import MM_INCH, CENTER_N, CENTER_P


# from pprint import pprint

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
                order_item = CutItem(order_number=orders.order_no, bundle=bundle.bundle_no, part_number=part.part_no,
                                     quantity=part.quantity, length=float(part.part_length) / mm_inch,
                                     material=part.material,
                                     product_code=orders.product_code, part_option='R', item_id=part.part_no,
                                     action='C')
                order_list.append(order_item)
                # print(part.dtr_holes)
                for dtr_hole in part.dtr_holes:
                    # print('dtr_hole.group_type-->{0}'.format(dtr_hole.group_type))
                    if dtr_hole.group_type == 'double hole':
                        tool_num = get_dtr_tool_id(tool_list, dtr_hole.dia, dtr_hole.gauge, dtr_hole.group_y)
                        if tool_num > 0:
                            part_item = Part(part_name=part.part_no, tool_number=tool_num,
                                             x_offset=dtr_hole.group_x / mm_inch,
                                             x_reference=dtr_hole.group_x_reference, permanent=True,
                                             y_offset=dtr_hole.group_y / mm_inch,
                                             y_reference=dtr_hole.group_y_reference)
                            part_list.append(part_item)
                        else:
                            print('This type of double tool_id is not defined! dia={0} * gauge={0}'.format(
                                dtr_hole.dia,
                                dtr_hole.gauge))
                            return 0
                    else:
                        tool_num = get_dtr_tool_id(tool_list, dtr_hole.dia, dtr_hole.gauge, dtr_hole.group_y)
                        if tool_num > 0:
                            part_item = Part(part_name=part.part_no, tool_number=tool_num,
                                             x_offset=dtr_hole.x / mm_inch,
                                             x_reference=dtr_hole.x_reference, permanent=True,
                                             y_offset=dtr_hole.y / mm_inch,
                                             y_reference=dtr_hole.y_reference)
                            part_list.append(part_item)
                        else:
                            print('This type of single tool_id is not defined! dia={0} * gauge={0}'.format(
                                dtr_hole.dia,
                                dtr_hole.gauge))
                            # print(part_list)
                            return 0
    # print(order_list)
    # print(part_list)
    # file_path += 'D' + time.strftime('%y%m%d', time.localtime()) + '0'  # str(random.randint(0, 9))
    file_path += 'D' + '0' * 7
    # print(file_path)
    order_list.save_as(file_path + '.ORD')
    part_list.save_as(file_path + '.PRT')


def get_dtr_tools(file_with_path):
    csv_f = zCSV.CsvFile(file_with_path)
    tool_list = csv_f.get_tool_id()
    # print(tool_list)
    return tool_list


def get_dtr_tool_id(tool_list, dia, gauge, diff):
    for tool in tool_list:
        if tool['Dia'] == dia:
            if tool['Gauge'] == gauge:
                if tool['Diff'] == diff:
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
            order = Order.Order('', '', '')
            one_order = order.get_order_no_from_lysaght_txt(order_file)
            print(one_order)
            batch = Batch.Batch(176590)
            # bundle = Bundle(7)
            for punch_file in punch_files:
                punch = zCSV.CsvFile(punch_file)
                punches = punch.get_lysaght_punch()
                bundle_info = punch.get_lysaght_bundle_cz_info()
                bundle = Bundle.Bundle(bundle_info[0])
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


def gen_butler_order_cut_list(cut_list, nc_folder):
    mm_inch = 25.4
    tool_list = get_dtr_tools('./DTRTools.csv')

    return_list = CutList()
    part_list = Parts()
    # part_list = []
    no_pattern_list = []
    for cut_part in cut_list:
        order_number = str(cut_part['Order Num'])
        batch_number = str(cut_part['Batch Id'])
        bundle = int(re.sub(r'\D', '', cut_part['Bundle']))
        quantity = cut_part['Fa Qty']
        length = cut_part['Unit Length']
        material = cut_part['Raw Material'].strip()
        product_code = cut_part['Item Cat'].strip()
        part_number = cut_part['Fa Item'][0:7]
        part_option = 'R'
        item_id = part_number
        action = 'C'
        cut_item = CutItem(order_number=batch_number, bundle=bundle, part_number=part_number,
                           quantity=quantity, length=length / MM_INCH,
                           material=material,
                           product_code=product_code, part_option=part_option, item_id=item_id,
                           action=action)
        return_list.append(cut_item)
        file_name = part_number + '.nc1'
        nc_file_path = os.path.join(nc_folder, file_name)
        if is_exist_nc(nc_file_path):
            nc = Nc(nc_file_path)
            nc_data = nc.file_data
            nc_inf = nc.file_information()
            part = gen_butler_part_to_lysaght(nc_inf)
            part.sort_holes()
            part.group_holes_by_y()
            double_list = part.convert_to_dtr_holes()

            # 检查pattern
            no_pattern_list += double_list
            no_pattern_list = check_patterns(tool_list, part.dtr_holes, no_pattern_list)
            no_pattern_list = [dict(t) for t in {tuple(d.items()) for d in no_pattern_list}]  # 字典列表去重
            # no_pattern_list = sorted(no_pattern_list, key=lambda e: (
            # e.__getitem__('Dia'), e.__getitem__('Gauge'), e.__getitem__('Diff')), reverse=True)
            if no_pattern_list:
                # print('There are no pattern list:', no_pattern_list)
                continue

            for dtr_hole in part.dtr_holes:
                # print('dtr_hole.group_type-->{0}'.format(dtr_hole.group_type))inf
                dia = dtr_hole.dia
                gauge = dtr_hole.gauge
                group_y = dtr_hole.group_y
                group_y_r = dtr_hole.group_y_reference

                if dtr_hole.group_type == 'double hole':  # 对孔---------------
                    tool_num = get_dtr_tool_id(tool_list, dtr_hole.dia, dtr_hole.gauge, dtr_hole.group_y)
                    if tool_num > 0:
                        # part_item = Part(part_name=part.part_no, tool_number=tool_num,
                        #                  x_offset=dtr_hole.group_x / mm_inch,
                        #                  x_reference=dtr_hole.group_x_reference, permanent=True,
                        #                  y_offset=dtr_hole.group_y / mm_inch,
                        #                  y_reference=dtr_hole.group_y_reference)

                        part_item = Part(part_name=part.part_no, tool_number=tool_num,
                                         x_offset=dtr_hole.group_x / mm_inch,
                                         x_reference=dtr_hole.group_x_reference, permanent=True,
                                         y_offset=0.0,
                                         y_reference=CENTER_P)

                        part_list.append(part_item)
                    else:
                        print('This type of double tool_id is not defined, dia=', dia, ' gauge=',
                              gauge, ' group_y=', group_y, ' group_y_r=', group_y_r, ' at part=', part.part_no)
                        return 0
                else:  # 单孔------------------------------
                    if group_y_r == CENTER_N:
                        group_y = - group_y
                    tool_num = get_dtr_tool_id(tool_list, dtr_hole.dia, dtr_hole.gauge, group_y)
                    if tool_num > 0:
                        # part_item = Part(part_name=part.part_no, tool_number=tool_num,
                        #                  x_offset=dtr_hole.x / mm_inch,
                        #                  x_reference=dtr_hole.x_reference, permanent=True,
                        #                  y_offset=dtr_hole.y / mm_inch,
                        #                  y_reference=dtr_hole.y_reference)
                        part_item = Part(part_name=part.part_no, tool_number=tool_num,
                                         x_offset=dtr_hole.x / mm_inch,
                                         x_reference=dtr_hole.x_reference, permanent=True,
                                         y_offset=0.0,
                                         y_reference=CENTER_P)
                        part_list.append(part_item)
                    else:
                        print('This type of single tool_id is not defined, dia=', dia, ' gauge=',
                              gauge, ' group_y=', group_y, ' group_y_r=', group_y_r, ' at part=', part.part_no)
                        return 0
    # print('Type of part list: ', (type(part_list)))
    if not part_list:
        part_list = None
    return return_list, no_pattern_list, part_list


def gen_butler_part_to_lysaght(nc_info):
    if nc_info.header.code_profile == 'C':
        # 判断反转
        pass
    if nc_info.header.code_profile == 'SO':
        pass
    # 获取web宽, flange宽, web厚度
    flange_width = nc_info.header.flange_width
    web_thickness = nc_info.header.web_thickness
    profile_height = nc_info.header.profile_height
    pro_file = re.findall(r'\d+\.?\d*', nc_info.header.profile)
    if len(pro_file) == 2:
        profile_height = float(pro_file[0])  # nc_info.header.profile_height  #
        web_thickness = float(pro_file[1])  # nc_info.header.web_thickness  #
    if len(pro_file) == 3:
        profile_height = float(pro_file[0])  # nc_info.header.profile_height  #
        web_thickness = float(pro_file[2])  # nc_info.header.web_thickness  #

    # print(profile_height, flange_width)
    part = lpart.Part(nc_info.header.drawing, int(nc_info.header.length), web_thickness,
                      nc_info.header.quantity, nc_info.header.profile, '')
    # print(type(part))
    if nc_info.holes:
        plan_holes = get_nc_plane_holes(nc_info.holes)
        # 处理腹板 v--正面， h--反面
        if plan_holes[2]:  # v
            for v_hole in plan_holes[2]:
                if v_hole.reference == 'o':
                    v_hole_y = profile_height / 2 - round(v_hole.y)
                elif v_hole.reference == 'u':
                    v_hole_y = -(profile_height / 2 - round(v_hole.y))
                elif v_hole.reference == 's':
                    # v_hole_y = round(v_hole.y)
                    v_hole_y = profile_height / 2 - round(v_hole.y)
                else:
                    v_hole_y = 0.0
                hole_v = lpart.Hole('WEB', v_hole.x, float(round(v_hole_y)), float(round(v_hole.diameter)))
                part.add_hole(hole_v)

        if plan_holes[3]:  # h
            for h_hole in plan_holes[3]:
                if h_hole.reference == 'o':
                    h_hole_y = profile_height / 2 - round(h_hole.y)
                elif h_hole.reference == 'u':
                    h_hole_y = -(profile_height / 2 - round(h_hole.y))
                elif h_hole.reference == 's':
                    # h_hole_y = round(h_hole.y)
                    h_hole_y = profile_height / 2 - round(h_hole.y)
                else:
                    h_hole_y = 0.0
                part.add_hole(lpart.Hole('WEB', h_hole.x, float(round(h_hole_y)), float(round(h_hole.diameter))))

        # 处理上翼缘 o--上
        if plan_holes[0]:  # o   ---算法未确定
            for o_hole in plan_holes[0]:
                if o_hole.reference == 'o':
                    o_hole_y = flange_width - o_hole.y + profile_height / 2 - 2 * web_thickness
                elif o_hole.reference == 'u':
                    o_hole_y = o_hole.y + profile_height / 2 - 2 * web_thickness
                elif o_hole.reference == 's':
                    o_hole_y = flange_width / 2 + profile_height / 2 - 2 * web_thickness
                else:
                    o_hole_y = 0.0
                part.add_hole(lpart.Hole('OF', o_hole.x, float(round(o_hole_y)), float(round(o_hole.diameter))))
        # 处理下翼缘 u--下
        if plan_holes[1]:  # u   ---算法未确定
            for u_hole in plan_holes[1]:
                if u_hole.reference == 'o':
                    u_hole_y = -(flange_width - round(u_hole.y) + profile_height / 2 - 2 * web_thickness)
                elif u_hole.reference == 'u':
                    u_hole_y = -(round(u_hole.y) + profile_height / 2 - 2 * web_thickness)
                elif u_hole.reference == 's':
                    u_hole_y = -(flange_width / 2 + profile_height / 2 - 2 * web_thickness)
                else:
                    u_hole_y = 0.0
                u_hole_y = - u_hole_y
                part.add_hole(lpart.Hole('IF', u_hole.x, float(round(u_hole_y)), float(round(u_hole.diameter))))
    return part


def get_nc_plane_holes(nc_holes):
    plane_holes = []
    v_holes = []
    u_holes = []
    o_holes = []
    h_holes = []
    for single_hole in nc_holes:
        # print(single_hole.plane)
        # print(single_hole.reference)
        if single_hole.plane == 'o' and single_hole.reference == 's' and single_hole.hole_type == '':
            o_holes.append(single_hole)
        if single_hole.plane == 'o' and single_hole.reference == 'o' and single_hole.hole_type == '':
            o_holes.append(single_hole)
        if single_hole.plane == 'o' and single_hole.reference == 'u' and single_hole.hole_type == '':
            o_holes.append(single_hole)
        if single_hole.plane == 'u' and single_hole.reference == 's' and single_hole.hole_type == '':
            u_holes.append(single_hole)
        if single_hole.plane == 'u' and single_hole.reference == 'o' and single_hole.hole_type == '':
            u_holes.append(single_hole)
        if single_hole.plane == 'u' and single_hole.reference == 'u' and single_hole.hole_type == '':
            u_holes.append(single_hole)
        if single_hole.plane == 'v' and single_hole.reference == 'o' and single_hole.hole_type == '':
            v_holes.append(single_hole)
        if single_hole.plane == 'v' and single_hole.reference == 'u' and single_hole.hole_type == '':
            v_holes.append(single_hole)
        if single_hole.plane == 'v' and single_hole.reference == 's' and single_hole.hole_type == '':
            v_holes.append(single_hole)
        if single_hole.plane == 'h' and single_hole.reference == 'o' and single_hole.hole_type == '':
            h_holes.append(single_hole)
        if single_hole.plane == 'h' and single_hole.reference == 'u' and single_hole.hole_type == '':
            h_holes.append(single_hole)
        if single_hole.plane == 'h' and single_hole.reference == 's' and single_hole.hole_type == '':
            h_holes.append(single_hole)

    plane_holes.append(o_holes)
    plane_holes.append(u_holes)
    plane_holes.append(v_holes)
    plane_holes.append(h_holes)

    # print(o_holes)
    return plane_holes


def check_patterns(tool_list, dtr_holes, no_pattern_list_re):
    for dtr_hole in dtr_holes:
        group_y = dtr_hole.group_y
        if dtr_hole.group_y_reference == CENTER_N:
            group_y = -group_y
        tool_num = get_dtr_tool_id(tool_list, dtr_hole.dia, dtr_hole.gauge, group_y)
        if tool_num < 0:
            temp = {'dia': dtr_hole.dia, 'gauge': dtr_hole.gauge, 'diff': group_y}
            no_pattern_list_re.append(temp)
    return no_pattern_list_re


def list_dict_duplicate_removal(data_list):
    run_function = lambda x, y: x if y in x else x + [y]
    return reduce(run_function, [[], ] + data_list)


if __name__ == '__main__':
    # test04
    # from CamGen.NCBase import *
    # from pprint import pprint
    # file_with_path = "E:/Desktop/BYD重庆璧山5#&6#/1900660801-2212-007C 璧山5# 2.5mm厚C墙筋1~13轴/C墙筋-NC FILES 2.5mm/WQ17000.nc1"
    # if is_exist_nc(file_with_path):
    #     # print('OK')
    #     nc = Nc(file_with_path)
    #     nc_data = nc.file_data
    #     nc_info = nc.file_information()
    #     part_lysaght = gen_butler_part_to_lysaght(nc_info)
    #     part_lysaght.sort_holes()
    #     part_lysaght.group_holes_by_y()
    #     part_lysaght.convert_to_dtr_holes()
    #     for hole in part_lysaght.dtr_holes:
    #         print(hole)
    # else:
    #     print('No')

    # test03
    # oracle_data_import('zyq', 'zyq123', 'zanweb\stlsojsvr04', 'DFactory', '../testfiles/1000002.csv')

    # test02
    # tool_dtr = get_dtr_tools('../DTRTools.csv')
    # print(tool_dtr)
    # tool_id = get_dtr_tool_id(tool_dtr, 16.0, 230.0)
    # print(tool_id)

    # test01
    #   lysaght_orders = Order()
    # lysaght_to_dtr(lysaght_orders, file_path=None)
    pass
