__author__ = "zanweb <zanweb@163.com>"

# from operator import attrgetter
import operator
from itertools import groupby
from operator import attrgetter

import math

# from DTRGen.TransformFunctions import get_lysaght_real_dia
from DTRGen import TransformFunctions
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
        return str(self.location) + ',' + str(self.x) + ',' + str(self.y) + ',' + str(self.dia)


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

    def __init__(self, part_no, part_length, part_thickness, quantity, section, material):
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

    def convert_to_dtr_holes(self):
        # self.dtr_holes = []
        tool_list = TransformFunctions.get_dtr_tools('./DTRTools.csv')
        for one_group in self.holes_group_y:
            # print('one_group len -->{0}'.format(len(one_group)))
            dtr_hole = DTRHole()
            if len(one_group) == 1:
                dtr_hole = self.single_dtr_hole(one_group[0])
                self.dtr_holes.append(dtr_hole)
            if len(one_group) == 2:
                dtr_hole.__dict__ = one_group[1].__dict__
                dtr_hole.group_type = 'double hole'
                dtr_hole.x_reference = LEADING_EDGE
                dtr_hole.y_reference = CENTER_P
                dtr_hole.group_x = dtr_hole.x
                dtr_hole.group_y = 0.0
                dtr_hole.group_x_reference = LEADING_EDGE
                dtr_hole.group_y_reference = CENTER_P
                if one_group[0].y == - one_group[1].y:
                    dtr_hole.gauge = math.fabs(one_group[1].y) * 2
                else:
                    dtr_hole.gauge = math.fabs(one_group[1].y - one_group[0].y)
                    dtr_hole.group_y = one_group[1].y - dtr_hole.gauge / 2
                is_normal_gauge = TransformFunctions.get_dtr_tool_id(tool_list, dtr_hole.dia, dtr_hole.gauge)
                if is_normal_gauge == -1:
                    dtr_hole = self.single_dtr_hole(one_group[0])
                    self.dtr_holes.append(dtr_hole)
                    dtr_hole = self.single_dtr_hole(one_group[1])
                    self.dtr_holes.append(dtr_hole)
                    continue

                self.dtr_holes.append(dtr_hole)

    def single_dtr_hole(self, one_of_group):
        dtr_hole = DTRHole()
        dtr_hole.__dict__ = one_of_group.__dict__
        dtr_hole.group_type = 'single hole'
        dtr_hole.x_reference = LEADING_EDGE
        dtr_hole.y_reference = CENTER_P
        dtr_hole.group_x = 0.0
        dtr_hole.group_y = 0.0
        dtr_hole.group_x_reference = LEADING_EDGE
        dtr_hole.group_y_reference = CENTER_P
        dtr_hole.gauge = 0.0
        return dtr_hole

    def group_holes_by_y(self):
        for dia_index, dia_group in groupby(self.holes, key=attrgetter('dia')):
            for x_index, x_group in groupby(dia_group, key=attrgetter('x')):
                self.holes_group_y.append(list(x_group))
                # print(self.holes_group_y)

    def change_dia_no_to_real_dia(self, dia_list):
        try:
            for one_hole in self.holes:
                one_hole.dia = TransformFunctions.get_lysaght_real_dia(dia_list, one_hole.dia)
        except Exception as e:
            print(e)
        finally:
            return


def test():
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
    part.convert_to_dtr_holes()
    return part


if __name__ == '__main__':
    # from operator import attrgetter
    # from itertools import groupby

    holes_dtr = test().holes
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
