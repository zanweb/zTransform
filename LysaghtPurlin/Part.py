__author__ = "zanweb <zanweb@163.com>"

import os
import re

import math
# from operator import attrgetter
import operator
from itertools import groupby, combinations
from operator import attrgetter

# from DTRGen.TransformFunctions import get_lysaght_real_dia
from DTRGen import TransformFunctions
from DTRGen.Part import Part as DPart, Parts as DParts
# from zBase.base import String, Integer, Float
# from zBase.base import String, Integer, Float
from zBase import zbase
from zBase.constant import *


class Hole(object):
    location = zbase.String('location')
    x = zbase.Float('x')
    y = zbase.Float('y')
    dia = zbase.Float('dia')

    def __init__(self, location='', x=0.0, y=0.0, dia=0.0):
        self.location = location
        self.x = x
        self.y = y
        self.dia = dia

    def __str__(self):
        return str(self.location) + ',' + str(self.x) + \
               ',' + str(self.y) + ',' + str(self.dia)


class DTRHole(Hole):
    x_reference = zbase.Integer('x_reference')
    y_reference = zbase.Integer('y_reference')
    gauge = zbase.Float('gauge')
    group_type = zbase.String('type')

    group_x = zbase.Float('group_x')
    group_y = zbase.Float('group_y')
    group_x_reference = zbase.Integer('group_x_reference')
    group_y_reference = zbase.Integer('group_y_reference')

    def __init__(self, dia=0.0, x=0.0, y=0.0, x_reference=0, y_reference=0, location='', gauge=0.0,
                 group_type='', group_x=0.0,
                 group_y=0.0, group_x_reference=0, group_y_reference=0):
        super(DTRHole, self).__init__(dia=0.0, x=0.0, y=0.0, location='')
        self.location = location
        self.dia = dia
        self.x = x
        self.y = y
        self.x_reference = x_reference
        self.y_reference = y_reference
        self.group_y_reference = group_y_reference
        self.group_x_reference = group_x_reference
        self.group_y = group_y
        self.group_x = group_x
        self.group_type = group_type
        self.gauge = gauge

    def __str__(self):
        return str(self.location) + ',' + str(self.x) + ',' + str(self.x_reference) + ',' + str(self.y) + ',' + str(
            self.y_reference) + ',' + str(self.dia) + ',' + str(self.gauge) + ',' + str(self.group_type) + ',' + str(
            self.group_x) + ',' + str(self.group_x_reference) + ',' + str(self.group_y) + ',' + str(
            self.group_y_reference)


class Part(object):
    """ Lysaght Part """
    part_no = zbase.String('part_no')
    part_length = zbase.Integer('part_length')
    part_thickness = zbase.Float('part_thickness')
    quantity = zbase.Integer('quantity')
    section = zbase.String('section')
    material = zbase.String('material')

    def __init__(self, part_no, part_length, part_thickness,
                 quantity, section, material):
        self.material = material
        self.part_no = part_no
        self.part_length = part_length
        self.part_thickness = part_thickness
        self.quantity = quantity
        self.section = section
        self.holes = []
        self.holes_group_y = []

        self.dtr_holes = []

    def add_hole(self, hole):
        if not isinstance(hole, Hole):
            raise TypeError('You must import a Hole type!')
        self.holes.append(hole)

    def sort_holes(self):
        compare = operator.attrgetter('dia', 'x', 'y')
        self.holes.sort(key=compare, reverse=False)

    def check_y_offset_crash(self):
        hole_group_y = []
        # is_crash = False
        # 按x分组
        for x_index, x_group in groupby(self.holes, key=attrgetter('x')):
            hole_group_y.append(list(x_group))
        # 计算每组孔y-offset
        for holes in hole_group_y:
            combins_holes = [c for c in combinations(holes, 2)]
            for combins_hole in combins_holes:
                if ((combins_hole[0].y < 0) != (combins_hole[1].y < 0)) and (
                        combins_hole[0].y != 0) and (combins_hole[1].y != 0):  # y值相反+-
                    if abs(combins_hole[0].y - combins_hole[1].y) <= 70:
                        return True
        return False

    def convert_to_dtr_pattern_with_single_tools(self, tool_list):
        undefinde_holes = []
        part_list = []
        for hole in self.holes:
            tool_num = TransformFunctions.get_dtr_single_tool_id(
                tool_list, hole.dia)
            if tool_num > 0:
                part_item = DPart(part_name=self.part_no, tool_number=tool_num,
                                  x_offset=hole.x / MM_INCH,
                                  x_reference=hole.x_reference, permanent=True,
                                  y_offset=hole.y,
                                  y_reference=hole.y_reference)

                part_list.append(part_item)
            else:
                temp = {
                    'dia': hole.dia
                }
                undefinde_holes.append(temp)
        return part_list

    def convert_to_dtr_holes(self, tool_list):
        # self.dtr_holes = []
        double_list = []
        # tool_list = TransformFunctions.get_dtr_tools('./DTRTools.csv')
        for one_group in self.holes_group_y:
            # print('one_group len -->{0}'.format(len(one_group)))
            dtr_hole = DTRHole()
            if len(one_group) == 1:
                dtr_hole = self.single_dtr_hole(one_group[0])
                self.dtr_holes.append(dtr_hole)
            if len(one_group) == 2:
                dtr_double_holes, undefined_double_holes = self.double_dtr_holes(
                    tool_list, one_group)
                self.dtr_holes.extend(dtr_double_holes)
                double_list.extend(undefined_double_holes)
                # dtr_hole.__dict__ = one_group[1].__dict__
                # dtr_hole.group_type = 'double hole'
                # dtr_hole.x_reference = LEADING_EDGE
                # dtr_hole.y_reference = CENTER_P
                # dtr_hole.group_x = dtr_hole.x
                # dtr_hole.group_y = 0.0
                # dtr_hole.group_x_reference = LEADING_EDGE
                # dtr_hole.group_y_reference = CENTER_P
                # if one_group[0].y == - one_group[1].y:
                #     # x轴对称 ------------
                #     dtr_hole.gauge = math.fabs(one_group[1].y) * 2
                # else:
                #     # x轴偏心 ------------
                #     dtr_hole.gauge = math.fabs(one_group[1].y - one_group[0].y)
                #     dtr_hole.group_y = one_group[1].y - dtr_hole.gauge / 2
                #
                # # y为负数时
                # if dtr_hole.group_y < 0:
                #     group_y = math.fabs(dtr_hole.group_y)
                #     dtr_hole.group_y_reference = CENTER_N
                # else:
                #     group_y = dtr_hole.group_y
                # # dtr_hole.group_y = group_y
                #
                # is_normal_gauge = TransformFunctions.get_dtr_tool_id(tool_list, dtr_hole.dia, dtr_hole.gauge,
                #                                                      dtr_hole.group_y)
                # if is_normal_gauge == -1:
                #     t_double = {'Dia':dtr_hole.dia, 'Gauge': dtr_hole.gauge, 'Diff':dtr_hole.group_y}
                #     double_list.append(t_double)
                #     # 如果不是常规间距，按单孔处理 -------------------
                #
                #     dtr_hole = self.single_dtr_hole(one_group[0])
                #     self.dtr_holes.append(dtr_hole)
                #     dtr_hole = self.single_dtr_hole(one_group[1])
                #     self.dtr_holes.append(dtr_hole)
                #     continue
                #
                # self.dtr_holes.append(dtr_hole)

            if len(one_group) > 2:
                # TODO: 判断是否有成组的孔
                dtr_double_holes, undefined_double_holes = self.more_dtr_holes(
                    tool_list, one_group)
                self.dtr_holes.extend(dtr_double_holes)
                double_list.extend(undefined_double_holes)

                # for i in range(0, len(one_group)):
                #     dtr_hole = self.single_dtr_hole(one_group[i])
                #     self.dtr_holes.append(dtr_hole)
        return double_list

    def double_dtr_holes(self, tool_list, one_group):
        # 若是翼板上的孔作单孔处理
        undefined_holes = []
        dtr_holes = []
        dtr_hole = DTRHole()
        if str(one_group[0]).split(',')[0] != 'WEB' or str(
                one_group[1]).split(',')[0] != 'WEB':
            dtr_hole = self.single_dtr_hole(one_group[0])
            dtr_holes.append(dtr_hole)
            dtr_hole = self.single_dtr_hole(one_group[1])
            dtr_holes.append(dtr_hole)
        else:
            dtr_hole.__dict__ = one_group[1].__dict__
            dtr_hole.group_type = 'double hole'
            dtr_hole.x_reference = LEADING_EDGE
            dtr_hole.y_reference = CENTER_P
            dtr_hole.group_x = dtr_hole.x
            dtr_hole.group_y = 0.0
            dtr_hole.group_x_reference = LEADING_EDGE
            dtr_hole.group_y_reference = CENTER_P
            if one_group[0].y == - one_group[1].y:
                # x轴对称 ------------
                dtr_hole.gauge = math.fabs(one_group[1].y) * 2
            else:
                # x轴偏心 ------------
                dtr_hole.gauge = math.fabs(one_group[1].y - one_group[0].y)
                dtr_hole.group_y = one_group[1].y - dtr_hole.gauge / 2

            # y为负数时
            if dtr_hole.group_y < 0:
                group_y = math.fabs(dtr_hole.group_y)
                dtr_hole.group_y_reference = CENTER_N
            else:
                group_y = dtr_hole.group_y
            # dtr_hole.group_y = group_y

            is_normal_gauge = TransformFunctions.get_dtr_tool_id(tool_list, dtr_hole.dia, dtr_hole.gauge,
                                                                 dtr_hole.group_y)
            if is_normal_gauge == -1:
                if dtr_hole.gauge >= 70:
                    t_double = {
                        'Dia': dtr_hole.dia,
                        'Gauge': dtr_hole.gauge,
                        'Diff': dtr_hole.group_y}
                    undefined_holes.append(t_double)
                else:
                    # 如果不是常规间距，按单孔处理 -------------------
                    dtr_hole = self.single_dtr_hole(one_group[0])
                    dtr_holes.append(dtr_hole)
                    dtr_hole = self.single_dtr_hole(one_group[1])
                    dtr_holes.append(dtr_hole)
            else:
                dtr_holes.append(dtr_hole)
        return dtr_holes, undefined_holes

    def more_dtr_holes(self, tool_list, one_group):
        """
        判断一组孔中是否有成对的孔，没有就作单孔处理
        :param one_group:大于2个的lysaght格式的一组孔
                tool_list:预定义的孔
        :return:
                1. dtr_holes-->list         单个的或一对的DTR孔
                2. undefined_holes -->list   需要预定义的孔
        ideas：
                1. 翼板上的孔作单孔处理
                2. 腹板上
        """
        # 若是翼板上的孔作单孔处理
        undefined_holes = []
        dtr_holes = []
        dtr_hole = DTRHole()
        # 先处理翼板上的孔
        web_holes_group = []
        for one_hole in one_group:
            if str(one_hole).split(',')[0] != 'WEB':
                dtr_hole = self.single_dtr_hole(one_hole)
                dtr_holes.append(dtr_hole)
            else:
                web_holes_group.append(one_hole)
        # 处理腹板上的孔
        self.more_web_dtr_holes(
            tool_list,
            web_holes_group,
            dtr_holes,
            undefined_holes)
        # length_group = len(web_holes_group)
        # combins = [c for c in combinations(web_holes_group, 2)]
        # print(combins)
        # for i in range(0, length_group-2):
        #     for j in range(i+1, length_group):
        #         dtr_hole, undefined_hole = self.double_dtr_holes(tool_list, [one_group[i], one_group[j]])
        #         if not undefined_hole:
        #             dtr_holes.extend(dtr_hole)
        #             # undefined_holes.extend(undefined_hole)
        #         # else:

        return dtr_holes, undefined_holes

    def more_web_dtr_holes(self, tool_list, group_holes,
                           dtr_holes, undefined_holes):
        return self.more_web_dtr_holes_iter(
            tool_list, group_holes, dtr_holes, undefined_holes)

    def more_web_dtr_holes_iter(
            self, tool_list, group_holes, dtr_holes, undefined_holes):
        new_group_holes = group_holes

        if len(new_group_holes) == 0:
            return dtr_holes, undefined_holes
        if len(new_group_holes) == 1:
            dtr_hole = self.single_dtr_hole(new_group_holes[0])
            dtr_holes.append(dtr_hole)
            return dtr_holes, undefined_holes
        undefined_combins = []
        combins_holes = [c for c in combinations(group_holes, 2)]
        for combins_hole in combins_holes:
            # y轴是否有x轴对称的孔，y值相反+-
            if ((combins_hole[0].y < 0) != (combins_hole[1].y < 0)) and (
                    combins_hole[0].y != 0) and (combins_hole[1].y != 0):  # y轴是否有x轴对称的孔，y值相反+-
                # 判断是否有预定义
                dia = combins_hole[0].dia
                gauge = math.fabs(combins_hole[0].y - combins_hole[1].y)
                group_y = combins_hole[1].y - gauge / 2
                is_normal_gauge = TransformFunctions.get_dtr_tool_id(tool_list, dia, gauge,
                                                                     group_y)
                if is_normal_gauge > 0:
                    dtr_hole, undefined_hole = self.double_dtr_holes(
                        tool_list, list(combins_hole))
                    dtr_holes.extend(dtr_hole)
                    new_group_holes = list(
                        set(group_holes).difference(set(list(combins_hole))))
                    return self.more_web_dtr_holes_iter(
                        tool_list, new_group_holes, dtr_holes, undefined_holes)
                else:
                    undefined_combins.append(combins_hole)

        if undefined_combins:
            normal_gauge_combins = []
            for combins_hole in undefined_combins:
                dia = combins_hole[0].dia
                gauge = math.fabs(combins_hole[0].y - combins_hole[1].y)
                group_y = combins_hole[1].y - gauge / 2
                if gauge in [75, 100, 110, 120]:
                    undefined_hole = {
                        'Dia': dia, 'Gauge': gauge, 'Diff': group_y}
                    undefined_holes.append(undefined_hole)
                    new_group_holes = list(
                        set(group_holes).difference(set(list(combins_hole))))
                    return self.more_web_dtr_holes_iter(
                        tool_list, new_group_holes, dtr_holes, undefined_holes)

        return self.more_web_dtr_holes_iter(
            tool_list, new_group_holes, dtr_holes, undefined_holes)

    def single_dtr_hole(self, one_of_group):
        dtr_hole = DTRHole()
        dtr_hole.__dict__ = one_of_group.__dict__
        dtr_hole.group_type = 'single hole'
        dtr_hole.x_reference = LEADING_EDGE
        dtr_hole.y_reference = CENTER_P
        dtr_hole.group_x = 0.0
        dtr_hole.group_y = one_of_group.y
        dtr_hole.group_x_reference = LEADING_EDGE
        dtr_hole.group_y_reference = CENTER_P
        dtr_hole.gauge = 0.0
        if one_of_group.y < 0:
            dtr_hole.y_reference = CENTER_N
            dtr_hole.group_y_reference = CENTER_N
            dtr_hole.group_y = math.fabs(one_of_group.y)
            dtr_hole.y = math.fabs(one_of_group.y)
        return dtr_hole

    def group_holes_by_y(self):
        for dia_index, dia_group in groupby(self.holes, key=attrgetter('dia')):
            for x_index, x_group in groupby(dia_group, key=attrgetter('x')):
                self.holes_group_y.append(list(x_group))
                # print(self.holes_group_y)

    def change_dia_no_to_real_dia(self, dia_list):
        try:
            for one_hole in self.holes:
                one_hole.dia = TransformFunctions.get_lysaght_real_dia(
                    dia_list, one_hole.dia)
        except Exception as e:
            print(e)
        finally:
            return

    def special_change(self):
        try:
            for one_hole in self.holes:
                # lysaght的数据数据需要将y轴上下翻转下, DTR的Rgt不改的话
                one_hole.y = -one_hole.y
                # if (one_hole.dia == 1622) and (one_hole.y == 0):
                #     one_hole.dia = 18.0
                # if (one_hole.dia == 1622) and (one_hole.y != 0):
                #     one_hole.dia = 1822.0
                #     one_hole.x = one_hole.x + 37.5
                if (one_hole.dia == 7777) and (one_hole.y != 0):
                    one_hole.x = one_hole.x + 37.5
        except Exception as e:
            print(e)
        finally:
            return

    def check_tool_id(self, tool_list):
        """
        检查未定义工具号的孔
        :param tool_list:
        :return: 字典{'dia', 'gauge', 'diff'} 的列表
        """
        no_pattern_list_re = []
        for dtr_hole in self.dtr_holes:
            group_y = dtr_hole.group_y
            if dtr_hole.group_y_reference == CENTER_N:
                group_y = -group_y
            tool_num = TransformFunctions.get_dtr_tool_id(
                tool_list, dtr_hole.dia, dtr_hole.gauge, group_y)
            if tool_num < 0:
                # if dtr_hole.gauge >= 70:
                temp = {
                    'dia': dtr_hole.dia,
                    'gauge': dtr_hole.gauge,
                    'diff': group_y}
                no_pattern_list_re.append(temp)
        return no_pattern_list_re

    def check_tool_id_single(self, tool_list_single):
        no_pattern_list_re = []
        for hole_single in self.holes:
            tool_num = TransformFunctions.get_dtr_single_tool_id(tool_list_single, hole_single.dia)
            if tool_num < 0:
                temp = {
                    'dia': hole_single.dia
                }
                no_pattern_list_re.append(temp)
        return no_pattern_list_re

    def convert_to_dtr_pattern(self, tool_list):
        """
        转化为DTR的pattern字符串
        :param tool_list:
        :return: pattern字符串列表， 合并 part_list.parts.extend(part_listN.parts
        """
        undefinde_holes = []
        part_list = DParts()
        for dtr_hole in self.dtr_holes:
            # print('dtr_hole.group_type-->{0}'.format(dtr_hole.group_type))inf
            dia = float(dtr_hole.dia)
            gauge = dtr_hole.gauge
            group_y = dtr_hole.group_y
            group_y_r = dtr_hole.group_y_reference

            if dtr_hole.group_type == 'double hole':  # 对孔---------------
                tool_num = TransformFunctions.get_dtr_tool_id(
                    tool_list, dtr_hole.dia, dtr_hole.gauge, dtr_hole.group_y)
                if tool_num > 0:
                    part_item = DPart(part_name=self.part_no, tool_number=tool_num,
                                      x_offset=dtr_hole.group_x / MM_INCH,
                                      x_reference=dtr_hole.group_x_reference, permanent=True,
                                      y_offset=0.0,
                                      y_reference=CENTER_P)

                    part_list.append(part_item)
                else:
                    temp = {
                        'dia': dtr_hole.dia,
                        'gauge': dtr_hole.gauge,
                        'diff': group_y}
                    undefinde_holes.append(temp)

            else:  # 单孔------------------------------
                if group_y_r == CENTER_N:
                    group_y = - group_y
                tool_num = TransformFunctions.get_dtr_tool_id(
                    tool_list, dtr_hole.dia, dtr_hole.gauge, group_y)
                if tool_num > 0:
                    part_item = DPart(part_name=self.part_no, tool_number=tool_num,
                                      x_offset=dtr_hole.x / MM_INCH,
                                      x_reference=dtr_hole.x_reference, permanent=True,
                                      y_offset=0.0,
                                      y_reference=CENTER_P)
                    part_list.append(part_item)
                else:
                    temp = {
                        'dia': dtr_hole.dia,
                        'gauge': dtr_hole.gauge,
                        'diff': group_y}
                    undefinde_holes.append(temp)
        return part_list

    def convert_to_dtr_pattern_crash(self, tool_list):
        """
        转化为DTR的pattern字符串
        :param tool_list: 单孔工具号
        :return: pattern字符串列表， 合并 part_list.parts.extend(part_listN.parts
        """
        undefinde_holes = []
        part_list = DParts()
        for hole_single in self.holes:
            tool_num = TransformFunctions.get_dtr_single_tool_id(tool_list, hole_single.dia)

            if tool_num > 0:
                x_refer = LEADING_EDGE
                if hole_single.y > 0:
                    y_refer = CENTER_N
                else:
                    y_refer = CENTER_P
                y_offset = abs(hole_single.y)
                part_item = DPart(part_name=self.part_no, tool_number=tool_num,
                                  x_offset=hole_single.x / MM_INCH,
                                  x_reference=x_refer, permanent=True,
                                  y_offset=y_offset / MM_INCH,
                                  y_reference=y_refer)

                part_list.append(part_item)
            else:
                temp = {
                    'dia': hole_single.dia
                }
                undefinde_holes.append(temp)
        return part_list

def test():
    tool_list = TransformFunctions.get_dtr_tools('./DTRTools.csv')
    part = Part('abc123', 8265, 2.4, 21, 'C200190', '')
    part.add_hole(Hole('OF', 35.0, 158.0, 8.0))
    part.add_hole(Hole('OF', 635.0, 158.0, 8.0))
    part.add_hole(Hole('OF', 1235.0, 158.0, 8.0))
    part.add_hole(Hole('OF', 1835.0, 158.0, 8.0))
    part.add_hole(Hole('WEB', 2000.0, 115.0, 16.0))
    part.add_hole(Hole('WEB', 2000.0, -115.0, 16.0))
    part.add_hole(Hole('WEB', 2500.0, 115.0, 16.0))
    part.add_hole(Hole('WEB', 2500.0, -115.0, 16.0))
    part.add_hole(Hole('WEB', 3000.0, 0.0, 22.0))
    part.add_hole(Hole('IF', 7000.0, 158.0, 14.0))
    part.add_hole(Hole('IF', 7000.0, -158.0, 14.0))
    part.sort_holes()
    part.group_holes_by_y()
    part.convert_to_dtr_holes(tool_list)
    return part


if __name__ == '__main__':
    # from operator import attrgetter
    # from itertools import groupby

    holes_dtr = test().dtr_holes
    for hole in holes_dtr:
        print(hole)
    # for index_x in holes_dtr:
    #     print('{0}'.format(index_x))
    # print('---------------')
    # for index_dia, attr in groupby(holes_dtr, key=attrgetter('dia')):
    #     print(index_dia, '--')
    #     # for i in attr:
    #     for index_x, group_dia in groupby(attr, key=attrgetter('x')):
    #         print(index_x, '----')
    #         for item in group_dia:
    #             print(' ', item)
    # print(holes_dtr)
