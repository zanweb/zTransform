__author__ = "zanweb <zanweb@163.com>"

# from operator import attrgetter
import operator
from itertools import groupby
from operator import attrgetter

import math

from Base.base import String, Integer, Float
from Base.constant import *


class Hole(object):
    location = String('location')
    x = Float('x')
    y = Float('y')
    dia = Float('dia')

    def __init__(self, location='', x=0.0, y=0.0, dia=0.0):
        self.location = location
        self.x = x
        self.y = y
        self.dia = dia

    def __str__(self):
        return str(self.location) + ',' + str(self.x) + ',' + str(self.y) + ',' + str(self.dia)


class DTRHole(Hole):
    x_reference = Integer('x_reference')
    y_reference = Integer('y_reference')
    gauge = Float('gauge')
    group_type = String('type')

    group_x = Float('group_x')
    group_y = Float('group_y')
    group_x_reference = Integer('group_x_reference')
    group_y_reference = Integer('group_y_reference')

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
    part_no = String('part_no')
    part_length = Integer('part_length')
    part_thickness = Float('part_thickness')
    quantity = Integer('quantity')
    section = String('section')
    part_material = String('material')

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
        for one_group in self.holes_group_y:
            # print('one_group len -->{0}'.format(len(one_group)))
            dtr_hole = DTRHole()
            if len(one_group) == 1:
                dtr_hole.__dict__ = one_group[0].__dict__
                dtr_hole.group_type = 'single hole'
                dtr_hole.x_reference = LEADING_EDGE
                dtr_hole.y_reference = CENTER_P
                dtr_hole.group_x = 0.0
                dtr_hole.group_y = 0.0
                dtr_hole.group_x_reference = LEADING_EDGE
                dtr_hole.group_y_reference = CENTER_P
                dtr_hole.gauge = 0.0
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
                self.dtr_holes.append(dtr_hole)

    def group_holes_by_y(self):
        for dia_index, dia_group in groupby(self.holes, key=attrgetter('dia')):
            for x_index, x_group in groupby(dia_group, key=attrgetter('x')):
                self.holes_group_y.append(list(x_group))
                # print(self.holes_group_y)


def test():
    part = Part('abc123', 8265, 2.4, 21, 'C200190')
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
