#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :   2019/10/25 9:22
# @Author   :   ZANWEB
# @File     :   TransformFunctions.py in zTransform
# @IDE      :   PyCharm


import os
import re
from functools import reduce
from operator import itemgetter
from itertools import groupby

import LysaghtPurlin.Part as lpart
from CamGen.NCBase import Nc, is_exist_nc
from DTRGen.Order import *
from DTRGen.Part import *
from LysaghtPurlin import Batch
from LysaghtPurlin import Bundle
from LysaghtPurlin import Order
from Zfile import zCSV, zFBase
from zBase.constant import MM_INCH, CENTER_N, CENTER_P

def gen_half_cut_list(cut_list):
    # 判断半切清单
    # 先理出1.5m以下的list(auto_no, part_num, length, qty)
    # 相同材料，半切匹配，无法匹配的再与同材料大于1.5m的匹配，再无法匹配，列清单
    for raw_index, raw_group in groupby(cut_list, itemgetter('Raw Material')):
        pass

def gen_dtr_cut_list(cut_list, org='LKQ'):
    """
    生成切割清单
    :param org: 所属组织
    :param cut_list: oracle中的清单
    :return: DTR切割清单
    """
    return_list = CutList()
    if org == 'LKQ':
        cut_list_sorted_mark = sorted(cut_list, key=itemgetter('Mark No'))
    else:
        cut_list_sorted_mark = sorted(cut_list, key=itemgetter('Fa Item'))
    cut_list_sorted_length = sorted(cut_list_sorted_mark, key=itemgetter('Unit Length'), reverse=True)
    cut_list_sorted = sorted(cut_list_sorted_length, key=itemgetter('Bundle'))

    for cut_part in cut_list_sorted:
        # print(cut_part)
        order_number = str(cut_part['Order Num'])
        batch_number = str(cut_part['Batch Id'])
        bundle = int(re.sub(r'\D', '', cut_part['Bundle']))
        quantity = cut_part['Fa Qty']
        length = cut_part['Unit Length']
        material = cut_part['Raw Material'].strip()
        product_code = cut_part['Item Cat'].strip()
        if org == 'LKQ':
            part_number = cut_part['Mark No'].strip()  # 来实零件号取Mark No
        else:
            part_number = cut_part['Fa Item'][0:7]  # 来实零件号取Mark No
        part_option = 'R'
        item_id = part_number
        action = 'C'
        cut_item = CutItem(order_number=batch_number, bundle=bundle, part_number=part_number,
                           quantity=quantity, length=length / MM_INCH,
                           material=material,
                           product_code=product_code, part_option=part_option, item_id=item_id,
                           action=action)
        return_list.append(cut_item)
    return return_list


def prepare_lysaght_holes(parts, lysaght_dia_list):
    """
    lysaght-csv中孔预处理
    :param parts: lysaght的part清单
    :param lysaght_dia_list: lysaght-csv 中的孔代号列表
    :return:
    """
    for part in parts:
        part.change_dia_no_to_real_dia(lysaght_dia_list)
        part.special_change()
    return parts


def check_lysaght_parts_crash(parts):
    crash_parts = []
    for part in parts:
        is_crash = part.check_y_offset_crash()
        if is_crash:
            crash_parts.append(part.part_no)
    return crash_parts


def get_dtr_single_tool_id(tool_list, dia):
    for tool in tool_list:
        if tool['Dia'] == dia:
            return tool['ToolID']
    return -1


def check_dtr_undefined_holes(parts, tool_list):
    """
    检查lysaght-parts中的未定义孔
    :param parts:  lysaght的零件列表
    :param tool_list: DTR孔的列表
    :return: 返回未定义孔列表
    """
    no_pattern_list = []
    for part in parts:
        part.sort_holes()
        part.group_holes_by_y()
        # part.convert_to_dtr_holes()
        double_list = part.convert_to_dtr_holes(tool_list)

        # 检查pattern
        no_pattern_list += double_list
        no_pattern_list += part.check_tool_id(tool_list)
        no_pattern_list = [
            dict(t) for t in {
                tuple(
                    d.items()) for d in no_pattern_list}]  # 字典列表去重
        if no_pattern_list:
            # print('There are no pattern list:', no_pattern_list)
            continue
    return no_pattern_list


def gen_dtr_pattern_list(parts, tool_list):
    """
    lysaght-parts转DTR孔
    :param parts: lysaght-part
    :param tool_list: DTR孔列表
    :return: 转换号的DTR-pattern列表
    """
    part_list = Parts()
    for part in parts:
        # part.sort_holes()
        # part.group_holes_by_y()
        # part.convert_to_dtr_holes()
        # double_list = part.convert_to_dtr_holes(tool_list)
        pattern = part.convert_to_dtr_pattern(tool_list)
        part_list.append(pattern)
    return part_list


def lysaght_csv_from_oracle_to_dtr(cut_list, parts):
    """
    转换lysaght-csv项目到DTR列表
    :param cut_list: Oracle清单
    :param parts: lysaght-csv零件
    :return: DTR切割清单，DTR未定义孔， DTR-pattern清单
    """
    tool_list = get_dtr_tools('./DTRTools.csv')
    lysaght_dia_list = get_lysaght_dias('./LysaghtHoleDia.csv')

    return_list = CutList()
    part_list = Parts()
    no_pattern_list = []
    # 判断半切清单
    # 先理出1.5m以下的list(auto_no, part_num, length, qty)
    # 相同材料，半切匹配，无法匹配的再与同材料大于1.5m的匹配，再无法匹配，列清单

    # 生成制作清单
    return_list = gen_dtr_cut_list(cut_list, org='LKQ')

    # 生成零件清单
    # 1. 转换到实际孔径，检查零件中未定义的孔
    parts_checked = prepare_lysaght_holes(parts, lysaght_dia_list)
    no_pattern_list = check_dtr_undefined_holes(parts_checked, tool_list)
    if no_pattern_list:
        # 1.1 如果有未定义的孔
        return return_list, no_pattern_list, part_list
    else:
        # 1.2 如果没有未定义的孔
        part_list = gen_dtr_pattern_list(parts_checked, tool_list)

    return return_list, no_pattern_list, part_list


def convert_nc_from_oracle_to_dtr(cut_list, nc_folder, org='LKQ'):
    """
    lysaght-nc项目转换导入DTR列表
    :param org: 组织名
    :param cut_list: lysaght-oracle获取的清单
    :param nc_folder: nc文件夹
    :return: DTR切割清单，DTR未定义孔， DTR-pattern清单
    """
    tool_list = get_dtr_tools('./DTRTools.csv')
    lysaght_dia_list = get_lysaght_dias('./LysaghtHoleDia.csv')

    return_list = CutList()
    part_list = Parts()
    # part_list = []
    no_pattern_list = []
    part_number_list = []  # 避免零件重复
    # 生成制作清单
    if org == 'LKQ':
        return_list = gen_dtr_cut_list(cut_list, org='LKQ')
    else:
        return_list = gen_dtr_cut_list(cut_list, org)

    # 生成零件清单
    if org == 'LKQ':
        # 1. 转换到实际孔径，检查零件中未定义的孔
        parts_checked = convert_nc_files_to_lysaght_parts(cut_list, nc_folder, org='LKQ')
        parts = prepare_lysaght_holes(parts_checked, lysaght_dia_list)
    else:
        parts = convert_nc_files_to_lysaght_parts(cut_list, nc_folder, org)

    no_pattern_list = check_dtr_undefined_holes(parts, tool_list)
    if no_pattern_list:
        # 1.1 如果有未定义的孔
        return return_list, no_pattern_list, part_list
    else:
        # 1.2 如果没有未定义的孔
        part_list = gen_dtr_pattern_list(parts, tool_list)

    return return_list, no_pattern_list, part_list


def convert_nc_files_to_lysaght_parts(cut_list, nc_folder, org='LKQ'):
    """
    将nc文件组转化未Lasght-part
    :param cut_list: oracle提取的清单
    :param nc_folder: nc文件所在文件夹
    :param org: 组织类型
    :return: 返回lysaght-parts
    """
    nc_files = []
    lysaght_parts = []
    for cut_part in cut_list:
        if org == 'LKQ':
            part_number = cut_part['Mark No'].strip() + '.nc1'  # 来实零件号取Mark No
        else:
            part_number = cut_part['Fa Item'][0:7] + '.nc1'  # butler零件号取'Fa Item'
        nc_files.append(part_number)
    # 去重
    nc_files.sort()
    nc_files = list_dict_duplicate_removal(nc_files)
    print(nc_files)

    for file_name in nc_files:
        nc_file_path = os.path.join(nc_folder, file_name)
        nc = Nc(nc_file_path)
        nc_data = nc.file_data
        nc_inf = nc.file_information()
        part = gen_nc_part_to_lysaght(nc_inf)
        lysaght_parts.append(part)
    return lysaght_parts


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
    tool_list = get_dtr_tools('./DTRTools.csv')
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
                    one_part.convert_to_dtr_holes(tool_list)
                    bundle.add_part(one_part)
                batch.add_bundle(bundle)
            order.add_batch(batch)
            orders.append(order)
    except Exception as e:
        print(e)
    finally:
        return orders


def gen_butler_order_cut_list(cut_list, nc_folder):
    # mm_inch = 25.4
    tool_list = get_dtr_tools('./DTRTools.csv')

    return_list = CutList()
    part_list = Parts()
    # part_list = []
    no_pattern_list = []
    part_number_list = []  # 避免零件重复
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
        if is_exist_nc(nc_file_path) and (part_number not in part_number_list):
            nc = Nc(nc_file_path)
            nc_data = nc.file_data
            nc_inf = nc.file_information()
            part = gen_nc_part_to_lysaght(nc_inf)
            part.sort_holes()
            part.group_holes_by_y()
            double_list = part.convert_to_dtr_holes(tool_list)

            # 检查pattern
            no_pattern_list += double_list
            no_pattern_list = check_patterns(
                tool_list, part.dtr_holes, no_pattern_list)
            no_pattern_list = [
                dict(t) for t in {
                    tuple(
                        d.items()) for d in no_pattern_list}]  # 字典列表去重
            # no_pattern_list = sorted(no_pattern_list, key=lambda e: (
            # e.__getitem__('Dia'), e.__getitem__('Gauge'),
            # e.__getitem__('Diff')), reverse=True)
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
                    tool_num = get_dtr_tool_id(
                        tool_list, dtr_hole.dia, dtr_hole.gauge, dtr_hole.group_y)
                    if tool_num > 0:
                        # part_item = Part(part_name=part.part_no, tool_number=tool_num,
                        #                  x_offset=dtr_hole.group_x / mm_inch,
                        #                  x_reference=dtr_hole.group_x_reference, permanent=True,
                        #                  y_offset=dtr_hole.group_y / mm_inch,
                        #                  y_reference=dtr_hole.group_y_reference)

                        part_item = Part(part_name=part.part_no, tool_number=tool_num,
                                         x_offset=dtr_hole.group_x / MM_INCH,
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
                    tool_num = get_dtr_tool_id(
                        tool_list, dtr_hole.dia, dtr_hole.gauge, group_y)
                    if tool_num > 0:
                        # part_item = Part(part_name=part.part_no, tool_number=tool_num,
                        #                  x_offset=dtr_hole.x / mm_inch,
                        #                  x_reference=dtr_hole.x_reference, permanent=True,
                        #                  y_offset=dtr_hole.y / mm_inch,
                        #                  y_reference=dtr_hole.y_reference)
                        part_item = Part(part_name=part.part_no, tool_number=tool_num,
                                         x_offset=dtr_hole.x / MM_INCH,
                                         x_reference=dtr_hole.x_reference, permanent=True,
                                         y_offset=0.0,
                                         y_reference=CENTER_P)
                        part_list.append(part_item)
                    else:
                        print('This type of single tool_id is not defined, dia=', dia, ' gauge=',
                              gauge, ' group_y=', group_y, ' group_y_r=', group_y_r, ' at part=', part.part_no)
                        return 0

            part_number_list.append(part_number)

    # print('Type of part list: ', (type(part_list)))
    if not part_list:
        part_list = None
    return return_list, no_pattern_list, part_list


def gen_nc_part_to_lysaght(nc_info):
    """
    转换nc文件到lysaght-part格式
    :param nc_info: 从nc文件获取的信息
    :return: 返回 lysaght-part类
    """
    bend_down_far_side = 0
    if nc_info.header.code_profile == 'C':
        # 判断反转
        bend_down_far_side = -1
        # DTR C檩条产品出来，开口向下
        # NC 默认开口向上
        # 远端和近端无需翻转
    if nc_info.header.code_profile == 'SO':
        # 判断上弯还是下弯
        bend_down_far_side = nc_file_z_bend(nc_info.ak)
        # 0 --> 远端下弯， -1 --> 远端上弯，
        # DTR Z檩条产品出来是远端下弯
        # DTR 如果NC远端下弯，远端和近端无需翻转，左右（x轴）翻转***
        # DTR 如果NC远端上弯，远端和近端无需要翻转，左右无需翻转

    profile_height, flange_width, web_thickness = nc_file_header_profile(nc_info.header)

    # print(profile_height, flange_width)
    part = lpart.Part(nc_info.header.drawing, int(nc_info.header.length), web_thickness,
                      nc_info.header.quantity, nc_info.header.profile, '')
    # print(type(part))
    if nc_info.holes:
        plan_holes = get_nc_plane_holes(nc_info.holes)
        # 处理腹板 v--正面， h--反面, 图纸下部为o基准
        if plan_holes[2]:  # v
            for v_hole in plan_holes[2]:
                if v_hole.reference == 'o':
                    v_hole_y = -(profile_height / 2 - round(v_hole.y))
                elif v_hole.reference == 'u':
                    v_hole_y = -(profile_height / 2 - round(v_hole.y))
                elif v_hole.reference == 's':
                    v_hole_y = -(profile_height / 2 - round(v_hole.y))
                else:
                    v_hole_y = 0.0

                if bend_down_far_side == 0:
                    # 左右翻转
                    v_hole.x = nc_info.header.length - v_hole.x

                hole_v = lpart.Hole(
                    'WEB', v_hole.x, float(
                        round(v_hole_y)), float(
                        round(
                            v_hole.diameter)))
                part.add_hole(hole_v)
        # 处理腹板，h - -反面,
        if plan_holes[3]:  # h
            for h_hole in plan_holes[3]:
                if h_hole.reference == 'o':
                    h_hole_y = -(profile_height / 2 - round(h_hole.y))
                elif h_hole.reference == 'u':
                    h_hole_y = -(profile_height / 2 - round(h_hole.y))
                elif h_hole.reference == 's':
                    h_hole_y = -(profile_height / 2 - round(h_hole.y))
                else:
                    h_hole_y = 0.0

                if bend_down_far_side == 0:
                    # 左右翻转
                    h_hole.x = nc_info.header.length - h_hole.x

                part.add_hole(
                    lpart.Hole(
                        'WEB', h_hole.x, float(
                            round(h_hole_y)), float(
                            round(
                                h_hole.diameter))))
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

                if bend_down_far_side == 0:
                    # 左右翻转
                    o_hole.x = nc_info.header.length - o_hole.x

                part.add_hole(
                    lpart.Hole(
                        'OF', o_hole.x, float(
                            round(o_hole_y)), float(
                            round(
                                o_hole.diameter))))
        # 处理下翼缘 u--下
        if plan_holes[1]:  # u   ---算法未确定
            for u_hole in plan_holes[1]:
                if u_hole.reference == 'o':
                    u_hole_y = -(flange_width - round(u_hole.y) +
                                 profile_height / 2 - 2 * web_thickness)
                elif u_hole.reference == 'u':
                    u_hole_y = -(round(u_hole.y) +
                                 profile_height / 2 - 2 * web_thickness)
                elif u_hole.reference == 's':
                    u_hole_y = -(flange_width / 2 +
                                 profile_height / 2 - 2 * web_thickness)
                else:
                    u_hole_y = 0.0

                if bend_down_far_side == 0:
                    # 左右翻转
                    u_hole.x = nc_info.header.length - u_hole.x

                part.add_hole(
                    lpart.Hole(
                        'IF', u_hole.x, float(
                            round(u_hole_y)), float(
                            round(
                                u_hole.diameter))))
    return part


def get_nc_plane_holes(nc_holes):
    plane_holes = []
    v_holes = []
    u_holes = []
    o_holes = []
    h_holes = []
    for single_hole in nc_holes:
        # 处理Dia为0的无效孔位
        if single_hole.diameter == 0:
            continue
        # 处理 NC 文件数据偏差###
        single_hole.x = float(round(single_hole.x))
        single_hole.y = float(round(single_hole.y))

        # 处理长圆孔及花孔
        if single_hole.special == 'l':
            diameter = single_hole.diameter
            width = single_hole.width
            x = single_hole.x
            single_hole.x = x + width / 2
            # 花孔 6*25 长圆孔作花孔处理
            if (diameter == 6) and (width == 19):
                single_hole.diameter = 7777
            else:
                single_hole.diameter = diameter * 100 + (diameter + width)

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

    # 避免孔重复
    o_holes = delete_double_holes(o_holes)
    u_holes = delete_double_holes(u_holes)
    v_holes = delete_double_holes(v_holes)
    h_holes = delete_double_holes(h_holes)

    plane_holes.append(o_holes)
    plane_holes.append(u_holes)
    plane_holes.append(v_holes)
    plane_holes.append(h_holes)

    # print(o_holes)
    return plane_holes


def delete_double_holes(holes):
    new_holes = []
    hole_attrs = []
    for hole in holes:
        hole_a = (hole.plane, hole.reference, hole.x, hole.y, hole.diameter)
        if hole_a not in hole_attrs:
            hole_attrs.append(hole_a)
            new_holes.append(hole)
    return new_holes


def check_patterns(tool_id_list, dtr_holes, no_pattern_list_re):
    for dtr_hole in dtr_holes:
        group_y = dtr_hole.group_y
        if dtr_hole.group_y_reference == CENTER_N:
            group_y = -group_y
        tool_num = get_dtr_tool_id(
            tool_id_list, dtr_hole.dia, dtr_hole.gauge, group_y)
        if tool_num < 0:
            if dtr_hole.gauge >= 70:
                temp = {
                    'dia': dtr_hole.dia,
                    'gauge': dtr_hole.gauge,
                    'diff': group_y}
                no_pattern_list_re.append(temp)
    return no_pattern_list_re


def list_dict_duplicate_removal(data_list):
    def run_function(x, y): return x if y in x else x + [y]

    return reduce(run_function, [[], ] + data_list)


def nc_file_header_profile(nc_header):
    flange_width = nc_header.flange_width
    web_thickness = nc_header.web_thickness
    profile_height = nc_header.profile_height
    profiles = re.findall(r'\d+\.?\d*', nc_header.profile)
    profiles_num = [float(x) for x in profiles]
    max_profiles_num = max(profiles_num)
    min_profiles_num = min(profiles_num)
    if min_profiles_num < 5:
        web_thickness = min_profiles_num
    if max_profiles_num > 150:
        profile_height = max_profiles_num
    list_wt_ph = [web_thickness, profile_height]
    remain_num = list(set(profiles_num).difference(set(list_wt_ph)))
    if remain_num:
        flange_width = max(remain_num)
    return profile_height, flange_width, web_thickness


def nc_file_z_bend(nc_aks):
    """
    判断nc远端Bend down 或 Bend up
    :param nc_aks:
    :return: 0 -- Bend down
             -1 -- Bend up
    """
    v_aks = []
    u_aks = []
    o_aks = []
    h_aks = []
    for single_ak in nc_aks:
        if single_ak.plane == 'v':
            v_aks.append(single_ak)
        if single_ak.plane == 'u':
            u_aks.append(single_ak)
        if single_ak.plane == 'o':
            o_aks.append(single_ak)
        if single_ak.plane == 'h':
            h_aks.append(single_ak)
    y_list = []
    for each_ak in v_aks:
        y_list.append(each_ak.y)
    max_y = max(y_list)
    if max_y < 30:  # Bend down of far side
        return 0
    else:  # Bend up of far side
        return -1


if __name__ == '__main__':
    # test06
    # from CamGen.NCBase import *
    #
    # file_with_path = "E:\Desktop\BSS_z_to_DTR/SV10939.nc1"
    # # file_with_path = "E:\Desktop\Cees\\1903982\\1901368801A(GIRT)-NCFiles/WG03500.nc1"
    # tool_list = get_dtr_tools('../DTRTools.csv')
    # if is_exist_nc(file_with_path):
    #     nc = Nc(file_with_path)
    #     nc_data = nc.file_data
    #     nc_info = nc.file_information()
    #     part = gen_nc_part_to_lysaght(nc_info)
    #     part.sort_holes()
    #     part.group_holes_by_y()
    #     part.convert_to_dtr_holes(tool_list)
    #     parrten = part.convert_to_dtr_pattern(tool_list)
    #     print(parrten)

    # test05
    # from CamGen.NCBase import *
    # from pprint import pprint
    #
    # # file_with_path = "E:\Desktop\BSS_z_to_DTR/SV10939.nc1"
    # file_with_path = "E:\Desktop\Cees\\1903982\\1901368801A(GIRT)-NCFiles/WG03500.nc1"
    #
    # if is_exist_nc(file_with_path):
    #     nc = Nc(file_with_path)
    #     nc_data = nc.file_data
    #     nc_info = nc.file_information()
    #     profile = nc_file_header_profile(nc_info.header)
    #     print(profile)

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
