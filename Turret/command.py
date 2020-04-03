#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :   2020/3/16 10:29
# @Author   :   ZANWEB
# @File     :   command.py in zTransform
# @IDE      :   PyCharm
from math import sqrt, atan, degrees, ceil
from PyQt5.QtWidgets import QMessageBox

JJ_SHORT = 33
CLIP_MARGE = 70
PART_MARGE = 10
UP_MARGE = 20
LEFT_MARGE = 20
RIGHT_MARGE = 20


def laa(x, y, tool_angle=0.0, d=0.0, angle=0.0, qty=1):
    tmp_list = []
    if tool_angle == 0:
        tmp_txt = 'X' + format(float(x), '0.2f') + 'Y' + format(float(y), '0.2f')
    else:
        tmp_txt = 'X' + format(float(x), '0.2f') + 'Y' + format(float(y), '0.2f') + 'C' \
                  + format(float(tool_angle), '0.2f')

    tmp_list.append(tmp_txt)
    tmp_txt = 'LAA/' + format(float(d), '0.2f') + ' ' + format(float(angle), '0.2f') + ' ' + str(qty)
    tmp_list.append(tmp_txt)
    return tmp_list


def loc(x, y):
    loc_tmp = 'X' + format(float(x), '0.2f') + 'Y' + format(float(y), '0.2f')
    return loc_tmp


def jj(mm, high):
    jj_temp = sqrt((mm / 2) * (mm / 2) + (high / 2) * (high / 2))
    return jj_temp


def part_size(tool_width, jj_length, mm, high):
    part_high = mm / 2 / jj_length * (JJ_SHORT + tool_width)
    part_high += part_high * 2 + high
    part_width = high / 2 / jj_length * (JJ_SHORT + tool_width)
    part_width += part_width * 2 + mm
    return part_high, part_width


def x_centre_0(part_width):
    x_centre_0_tmp = part_width / 2 + LEFT_MARGE
    return x_centre_0_tmp


def y_centre_0(part_high):
    y_centre_0_tmp = part_high / 2 + CLIP_MARGE
    return y_centre_0_tmp


def hole_gauge(mm):
    gauge = 0
    if mm < 900:
        gauge = 75
    if 900 <= mm < 1500:
        gauge = 100
    if mm >= 1500:
        gauge = 150
    return gauge


def gauge_num(jj_length, gauge):
    num = int((jj_length - 80) / gauge)
    return num


def gauge_num_dx(dx_length, gauge, jj_length, mm):
    d_length = jj_length / (mm / 2) * dx_length
    num = int(d_length / gauge)
    return num


def hole_parameter(mm, high, jj_length, gauge, gauge_number):
    hole_side_marge = (jj_length - gauge * gauge_number) / 2
    critical_value_side_marge = mm * 12 / high
    if critical_value_side_marge > hole_side_marge:
        # hole_y_diff = (mm * 12 - high * hole_side_marge) / 2 / jj_length
        # hole_y_diff = (6 * mm - high * hole_side_marge) / jj_length
        # hole_x_diff = (12 * high + hole_side_marge * mm) / 2 / jj_length
        dy = (high / 2 / jj_length) * (critical_value_side_marge - hole_side_marge)
        dx = jj_length / (mm / 2) * critical_value_side_marge - (mm / 2) / jj_length * (
                critical_value_side_marge - hole_side_marge)
    else:
        # hole_x_diff = 12 * jj_length / (mm / 2) + mm / 2 * (hole_side_marge - 12 * mm / 2 / (high / 2))
        # hole_x_diff = 12 * jj_length / (high / 2) + (mm / 2 / jj_length) * (hole_side_marge - critical_value_side_marge)
        # hole_y_diff = mm / 2 * (hole_side_marge * high / 2 - 12 * mm / 2)
        # hole_y_diff = (high / 2 / jj_length) * (hole_side_marge - critical_value_side_marge)
        # hole_y_diff = - hole_y_diff
        dy = ((high / 2) / jj_length) * (hole_side_marge - critical_value_side_marge)
        dx = 12 * jj_length / (high / 2) + (mm / 2) / jj_length * (hole_side_marge - critical_value_side_marge)
        dy = - dy
    return dx, dy


def hole_parameter_s(mm, high, jj_length, gauge, gauge_number):
    hole_side_marge = (jj_length - gauge * gauge_number) / 2
    critical_value_side_marge = high * 12 / mm
    if hole_side_marge > critical_value_side_marge:
        dx = (hole_side_marge - 12 * high / mm) * mm / 2 / jj_length
        dy = 12 * jj_length / (mm / 2) + (hole_side_marge - 12 * high / mm) * (high / 2) / jj_length
    else:
        dx = 0
        dy = 0
    return dx, dy


def side_parameter(mm, high, jj_length, tool_width, tool_length):
    # dx = mm / 2 / jj_length * ((tool_length / 2 * high / mm) - tool_width / 2)
    # dy = tool_length / 2 * mm / 2 / jj_length
    dx = high / 2 / jj_length * (high / mm * tool_width / 2 + tool_length / 2) - jj_length / mm * tool_width
    dy = mm / 2 / jj_length * (tool_length / 2 + high / 2 / mm * tool_width)
    return dx, dy


def side_parameter_s(mm, high, jj_length, tool_width, tool_length):
    dx = jj_length / mm / 2 * tool_width + high / 2 / jj_length * (tool_length / 2 - (high / mm * tool_width / 2))
    dy = mm / 2 / jj_length * (tool_length / 2 - (high / mm * tool_width / 2))
    return dx, dy


def jj_parameter(mm, high, jj_length, tool_width, tool_length):
    dx = mm / 2 / jj_length * (1 + tool_length / 2) + high / 2 / jj_length * (JJ_SHORT + tool_width / 2)
    dy = mm / 2 / jj_length * (JJ_SHORT + tool_width / 2) - high / 2 / jj_length * (1 + tool_length / 2)
    return dx, dy


def jj_parameter_s(mm, high, jj_length, tool_width, tool_length):
    dx = (mm / 2) / jj_length * (3 + tool_length / 2 - (JJ_SHORT + tool_width / 2) * high / mm)
    dy = jj_length / (mm / 2) * (tool_width / 2 + JJ_SHORT) + high / mm * dx
    return dx, dy


def jj_length_dff(mm, high, jj_length, length):
    dx = mm / 2 / jj_length * length
    dy = high / jj_length * length
    return dx, dy


def jj_num_dx(dx_length, keep_len, jj_length, mm, tool_length):
    length = jj_length / (mm / 2) * dx_length - keep_len - tool_length / 2
    num = ceil(length / tool_length)
    gge = length / num
    return num, gge


def g810974(mm, high, jj_length, tool_width, tool_length, gauge_number=None, gauge=None):
    # 准备
    part_high, part_width = part_size(tool_width, jj_length, mm, high)
    x_centre_d = x_centre_0(part_width)
    y_centre_d = y_centre_0(part_high)
    y_centre_u = y_centre_d + PART_MARGE + part_high

    dx_tool = high / 2 / jj_length * tool_width
    dy_tool = mm / 2 / jj_length * tool_width

    if gauge:
        gauge_t = gauge
    else:
        gauge_t = hole_gauge(mm)
    if gauge_number:
        gauge_number_t = gauge_number
    else:
        gauge_number_t = gauge_num(jj_length, gauge_t)

    hole_dx, hole_dy = hole_parameter(mm, high, jj_length, gauge_t, gauge_number_t)
    side_dx, side_dy = side_parameter(mm, high, jj_length, tool_width, tool_length)
    side_dx_s, side_dy_s = side_parameter_s(mm, high, jj_length, tool_width, tool_length)
    jj_dx, jj_dy = jj_parameter(mm, high, jj_length, tool_width, tool_length)
    hole_dx_s, hole_dy_s = hole_parameter_s(mm, high, jj_length, gauge_t, gauge_number_t)
    jj_dx_s, jj_dy_s = jj_parameter_s(mm, high, jj_length, tool_width, tool_length)

    # 开始
    code = []
    angle = degrees(atan(high / mm))
    j_num = ceil((jj_length - 2 - tool_length) / tool_length)
    j_diff = (jj_length - 2 - tool_length) / j_num
    d_diff = 1.5 / j_num
    j_diff = j_diff - d_diff

    if mm <= 1250:
        hole_code = []
        # hole-up
        code_tmp = laa(x_centre_d + hole_dx, y_centre_u + high / 2 + hole_dy, 0.0, gauge_t, angle=-angle,
                       qty=gauge_number_t)
        code_tmp = [code_tmp[0] + "T16(DIA X 6)", code_tmp[1]]
        hole_code.extend(code_tmp)
        code_tmp = laa(x_centre_d - hole_dx, y_centre_u + high / 2 + hole_dy, 0.0, gauge_t, angle=180 + angle,
                       qty=gauge_number_t)
        hole_code.extend(code_tmp)
        code_tmp = laa(x_centre_d - hole_dx, y_centre_u - high / 2 - hole_dy, 0.0, gauge_t, angle=180 - angle,
                       qty=gauge_number_t)
        hole_code.extend(code_tmp)
        code_tmp = laa(x_centre_d + hole_dx, y_centre_u - high / 2 - hole_dy, 0.0, gauge_t, angle=angle,
                       qty=gauge_number_t)
        hole_code.extend(code_tmp)
        # hole-down
        code_tmp = laa(x_centre_d + hole_dx, y_centre_d + high / 2 + hole_dy, 0.0, gauge_t, angle=-angle,
                       qty=gauge_number_t)
        hole_code.extend(code_tmp)
        code_tmp = laa(x_centre_d - hole_dx, y_centre_d + high / 2 + hole_dy, 0.0, gauge_t, angle=180 + angle,
                       qty=gauge_number_t)
        hole_code.extend(code_tmp)
        code_tmp = laa(x_centre_d - hole_dx, y_centre_d - high / 2 - hole_dy, 0.0, gauge_t, angle=180 - angle,
                       qty=gauge_number_t)
        hole_code.extend(code_tmp)
        code_tmp = laa(x_centre_d + hole_dx, y_centre_d - high / 2 - hole_dy, 0.0, gauge_t, angle=angle,
                       qty=gauge_number_t)
        hole_code.extend(code_tmp)
        print(hole_code)
        # side++++++++++++++++++++++++++
        side_code = []
        side_tmp = loc(x_centre_d + mm / 2 + side_dx_s, y_centre_u + side_dy_s)
        side_tmp = side_tmp + 'T12C' + format(float(90 - angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width)) + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + side_dx + dx_tool, y_centre_u + high / 2 + side_dy + dy_tool)
        side_code.append(side_tmp)

        side_tmp = loc(x_centre_d - mm / 2 - side_dx_s, y_centre_u - side_dy_s)
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - side_dx - dx_tool, y_centre_u - high / 2 - side_dy - dy_tool)
        side_code.append(side_tmp)

        side_tmp = loc(x_centre_d + mm / 2 + side_dx_s, y_centre_d + side_dy_s)
        side_tmp = side_tmp + 'C' + format(float(90 - angle), '0.2f')
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + side_dx + dx_tool, y_centre_d + high / 2 + side_dy + dy_tool)
        side_code.append(side_tmp)

        side_tmp = loc(x_centre_d - mm / 2 - side_dx_s, y_centre_d - side_dy_s)
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - side_dx - dx_tool, y_centre_d - high / 2 - side_dy - dy_tool)
        side_code.append(side_tmp)
        # ============

        side_tmp = loc(x_centre_d - side_dx - dx_tool, y_centre_u + high / 2 + side_dy + dy_tool)
        side_tmp = side_tmp + 'T12C' + format(float(90 + angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width)) + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - mm / 2 - side_dx_s, y_centre_u + side_dy_s)
        side_code.append(side_tmp)

        side_tmp = loc(x_centre_d + side_dx + dx_tool, y_centre_u - high / 2 - side_dy - dy_tool)
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + mm / 2 + side_dx_s, y_centre_u - side_dy_s)
        side_code.append(side_tmp)

        side_tmp = loc(x_centre_d - side_dx - dx_tool, y_centre_d + high / 2 + side_dy + dy_tool)
        side_tmp = side_tmp + 'C' + format(float(90 + angle), '0.2f')
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - mm / 2 - side_dx_s, y_centre_d + side_dy_s)
        side_code.append(side_tmp)

        side_tmp = loc(x_centre_d + side_dx + dx_tool, y_centre_d - high / 2 - side_dy - dy_tool)
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + mm / 2 + side_dx_s, y_centre_d - side_dy_s)
        side_code.append(side_tmp)

        print(side_code)
        # JJ
        # j_num = int((jj_length - 2 - tool_length) / tool_length)
        # j_diff = (jj_length - 2 - tool_length) / j_num

        jj_code = []
        jj_tmp = laa(x_centre_d + jj_dx, y_centre_u + high / 2 + jj_dy, -angle, j_diff, -angle, j_num)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d - jj_dx, y_centre_u + high / 2 + jj_dy, 180 + angle, j_diff, 180 + angle, j_num)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d - jj_dx, y_centre_u - high / 2 - jj_dy, 180 - angle, j_diff, 180 - angle, j_num)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d + jj_dx, y_centre_u - high / 2 - jj_dy, angle, j_diff, angle, j_num)
        jj_code.extend(jj_tmp)

        jj_tmp = laa(x_centre_d + jj_dx, y_centre_d + high / 2 + jj_dy, -angle, j_diff, -angle, j_num)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d - jj_dx, y_centre_d + high / 2 + jj_dy, 180 + angle, j_diff, 180 + angle, j_num)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d - jj_dx, y_centre_d - high / 2 - jj_dy, 180 - angle, j_diff, 180 - angle, j_num)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d + jj_dx, y_centre_d - high / 2 - jj_dy, angle, j_diff, angle, j_num)
        jj_code.extend(jj_tmp)
        print(jj_code)

        code_tmp = 'O' + str(mm)
        code.append(code_tmp)
        code_tmp = 'X' + str(1250) + 'Y' + str(1280) + 'M02'
        code.append(code_tmp)
        code.extend(hole_code)
        code.extend(side_code)
        code.extend(jj_code)
        code_tmp = 'C0.M03'
        code.append(code_tmp)
        code_tmp = 'M99'
        code.append(code_tmp)

        print(code)

    elif 1250 < mm <= 2500:
        # LEFT -------------------------------------------------------------------------------------------------
        # hole ++++++++++++++++++++++++++++++++++
        hole_code = []
        # hole-up ========
        code_tmp = laa(x_centre_d - hole_dx, y_centre_u + high / 2 + hole_dy, 0.0, gauge_t, angle=180 + angle,
                       qty=gauge_number_t)
        code_tmp = [code_tmp[0] + "T16(DIA X 6)", code_tmp[1]]  # ???????????????
        hole_code.extend(code_tmp)
        code_tmp = laa(x_centre_d - hole_dx, y_centre_u - high / 2 - hole_dy, 0.0, gauge_t, angle=180 - angle,
                       qty=gauge_number_t)
        hole_code.extend(code_tmp)
        # hole-down ======
        code_tmp = laa(x_centre_d - hole_dx, y_centre_d + high / 2 + hole_dy, 0.0, gauge_t, angle=180 + angle,
                       qty=gauge_number_t)
        hole_code.extend(code_tmp)
        code_tmp = laa(x_centre_d - hole_dx, y_centre_d - high / 2 - hole_dy, 0.0, gauge_t, angle=180 - angle,
                       qty=gauge_number_t)
        hole_code.extend(code_tmp)
        print(hole_code)
        # side +++++++++++++++++++++++++++++++++++
        # side - up ============
        side_code = []
        side_tmp = loc(x_centre_d - side_dx - dx_tool, y_centre_u + high / 2 + side_dy + dy_tool)
        side_tmp = side_tmp + 'T12C' + format(float(90 + angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width), '0.2f') + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - mm / 2 - side_dx_s, y_centre_u + side_dy_s)
        side_code.append(side_tmp)

        side_tmp = loc(x_centre_d - mm / 2 - side_dx_s, y_centre_u - side_dy_s)
        side_tmp = side_tmp + 'T12C' + format(float(90 - angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width), '0.2f') + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - side_dx - dx_tool, y_centre_u - high / 2 - side_dy - dy_tool)
        side_code.append(side_tmp)
        # side-down =============
        side_tmp = loc(x_centre_d - side_dx - dx_tool, y_centre_d + high / 2 + side_dy + dy_tool)
        side_tmp = side_tmp + 'T12C' + format(float(90 + angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width), '0.2f') + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - mm / 2 - side_dx_s, y_centre_d + side_dy_s)
        side_code.append(side_tmp)

        side_tmp = loc(x_centre_d - mm / 2 - side_dx_s, y_centre_d - side_dy_s)
        side_tmp = side_tmp + 'T12C' + format(float(90 - angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width), '0.2f') + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - side_dx - dx_tool, y_centre_d - high / 2 - side_dy - dy_tool)
        side_code.append(side_tmp)

        print(side_code)
        # JJ ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        jj_code = []
        # JJ-up =============================
        jj_tmp = laa(x_centre_d - jj_dx, y_centre_u + high / 2 + jj_dy, 180 + angle, j_diff, 180 + angle, j_num)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d - jj_dx, y_centre_u - high / 2 - jj_dy, 180 - angle, j_diff, 180 - angle, j_num)
        jj_code.extend(jj_tmp)

        jj_tmp = laa(x_centre_d - jj_dx, y_centre_d + high / 2 + jj_dy, 180 + angle, j_diff, 180 + angle, j_num)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d - jj_dx, y_centre_d - high / 2 - jj_dy, 180 - angle, j_diff, 180 - angle, j_num)
        jj_code.extend(jj_tmp)
        print(jj_code)
        #
        code_tmp = 'O' + str(mm)
        code.append(code_tmp)
        code_tmp = 'X' + format(float(1250), '0.0f') + 'Y' + format(
            float(1280)) + 'M02'
        code.append(code_tmp)
        code.extend(hole_code)
        code.extend(side_code)
        code.extend(jj_code)
        code_tmp = loc(x_centre_d, 100) + 'M03'  # *******************??????????????????????????????????????
        code.append(code_tmp)
        code_tmp = 'REP/DX' + format(float(part_width - 1250), '0.2f')
        code.append(code_tmp)

        # RIGHT --------------------------------------------------------------------------------------------------
        hole_code = []
        # HOLE ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # hole-up =======================================
        code_tmp = laa(x_centre_d + hole_dx, y_centre_u + high / 2 + hole_dy, 0.0, gauge_t, angle=-angle,
                       qty=gauge_number_t)
        code_tmp = [str(code_tmp[0]) + "T16(DIA X 6)", code_tmp[1]]
        hole_code.extend(code_tmp)
        code_tmp = laa(x_centre_d + hole_dx, y_centre_u - high / 2 - hole_dy, 0.0, gauge_t, angle=angle,
                       qty=gauge_number_t)
        hole_code.extend(code_tmp)
        # hole-down
        code_tmp = laa(x_centre_d + hole_dx, y_centre_d + high / 2 + hole_dy, 0.0, gauge_t, angle=-angle,
                       qty=gauge_number_t)
        hole_code.extend(code_tmp)
        code_tmp = laa(x_centre_d + hole_dx, y_centre_d - high / 2 - hole_dy, 0.0, gauge_t, angle=angle,
                       qty=gauge_number_t)
        hole_code.extend(code_tmp)
        print(hole_code)
        # side ++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # side-up ==============================
        side_code = []
        side_tmp = loc(x_centre_d + mm / 2 + side_dx_s, y_centre_u + side_dy_s)
        side_tmp = side_tmp + 'T12C' + format(float(90 - angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width), '0.2f') + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + side_dx + dx_tool, y_centre_u + high / 2 + side_dy + dy_tool)
        side_code.append(side_tmp)

        side_tmp = loc(x_centre_d + side_dx + dx_tool, y_centre_u - high / 2 - side_dy - dy_tool)
        side_tmp = side_tmp + 'C' + format(float(90 + angle), '0.2f')
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + mm / 2 + side_dx_s, y_centre_u - side_dy_s)
        side_code.append(side_tmp)

        # side-down ====================================
        side_tmp = loc(x_centre_d + mm / 2 + side_dx_s, y_centre_d + side_dy_s)
        side_tmp = side_tmp + 'T12C' + format(float(90 - angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width), '0.2f') + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + side_dx + dx_tool, y_centre_d + high / 2 + side_dy + dy_tool)
        side_code.append(side_tmp)

        side_tmp = loc(x_centre_d + side_dx + dx_tool, y_centre_d - high / 2 - side_dy - dy_tool)
        side_tmp = side_tmp + 'T12C' + format(float(90 + angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width), '0.2f') + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + mm / 2 + side_dx_s, y_centre_d - side_dy_s)
        side_code.append(side_tmp)

        print(side_code)
        # JJ +++++++++++++++++++++++++++++++++++++++++++++++++++
        # j_num = ceil((jj_length - 1 - tool_length) / tool_length)
        # j_diff = (jj_length - 1 - tool_length) / j_num

        jj_code = []
        # jj-up =======================
        jj_tmp = laa(x_centre_d + jj_dx, y_centre_u + high / 2 + jj_dy, -angle, j_diff, -angle, j_num)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d + jj_dx, y_centre_u - high / 2 - jj_dy, angle, j_diff, angle, j_num)
        jj_code.extend(jj_tmp)
        # jj-down ==========================
        jj_tmp = laa(x_centre_d + jj_dx, y_centre_d + high / 2 + jj_dy, -angle, j_diff, -angle, j_num)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d + jj_dx, y_centre_d - high / 2 - jj_dy, angle, j_diff, angle, j_num)
        jj_code.extend(jj_tmp)
        print(jj_code)
        code.extend(hole_code)
        code.extend(side_code)
        code.extend(jj_code)

        code_tmp = 'C0.M03'
        code.append(code_tmp)
        code_tmp = 'X' + format(float(part_width), '0.2f') + 'Y1280M03'
        code.append(code_tmp)
        code_tmp = 'FRM/X1250'
        code.append(code_tmp)
        code_tmp = 'X1250Y1280M30'
        code.append(code_tmp)
        # code_tmp = 'M99'
        # code.append(code_tmp)
        print(code)

    elif 2500 < mm <= 3750:
        hole_code = []
        dx_axis = mm / 6
        gauge_num_dx_t = gauge_num_dx(x_centre_d - hole_dx_s - dx_axis, gauge_t, jj_length, mm)
        # 左-----------------------------------------------------------------------------------------------
        # hole ++++ up ------
        code_tmp = laa(x_centre_d - mm / 2 + hole_dx_s, y_centre_u + hole_dy_s, 0.0, gauge_t, angle=angle,
                       qty=gauge_num_dx_t)
        code_tmp = [code_tmp[0] + "T16(DIA X 6)", code_tmp[1]]
        hole_code.extend(code_tmp)

        code_tmp = laa(x_centre_d - mm / 2 + hole_dx_s, y_centre_u - hole_dy_s, 0.0, gauge_t, angle=-angle,
                       qty=gauge_num_dx_t)
        hole_code.extend(code_tmp)
        # hole ++++ down ------
        code_tmp = laa(x_centre_d - mm / 2 + hole_dx_s, y_centre_d + hole_dy_s, 0.0, gauge_t, angle=angle,
                       qty=gauge_num_dx_t)
        code_tmp = [code_tmp[0] + "T16(DIA X 6)", code_tmp[1]]
        hole_code.extend(code_tmp)

        code_tmp = laa(x_centre_d - mm / 2 + hole_dx_s, y_centre_d - hole_dy_s, 0.0, gauge_t, angle=-angle,
                       qty=gauge_num_dx_t)
        hole_code.extend(code_tmp)

        # side punch +++ up ------
        side_code = []
        side_tmp = loc(x_centre_d - mm / 2 - side_dx_s, y_centre_u + side_dy_s)
        side_tmp = side_tmp + 'T12C' + format(float(90 + angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width)) + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - mm / 2 - side_dx_s, y_centre_u - side_dy_s)
        side_tmp = side_tmp + 'T12C' + format(float(90 - angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width)) + ')'
        side_code.append(side_tmp)
        # side punch +++ down ------
        side_tmp = loc(x_centre_d - mm / 2 - side_dx_s, y_centre_d + side_dy_s)
        side_tmp = side_tmp + 'T12C' + format(float(90 + angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width)) + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - mm / 2 - side_dx_s, y_centre_d - side_dy_s)
        side_tmp = side_tmp + 'T12C' + format(float(90 - angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width)) + ')'
        side_code.append(side_tmp)

        # jj punch +++ up --------
        jj_code = []
        j_num_dx, j_diff_dx = jj_num_dx(mm / 2 - dx_axis - jj_dx_s, 0.5, jj_length, mm, tool_length)
        jj_tmp = laa(x_centre_d - mm / 2 + jj_dx_s, y_centre_u + jj_dy_s, angle, j_diff_dx, angle, j_num_dx)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d - mm / 2 + jj_dx_s, y_centre_u - jj_dy_s, -angle, j_diff_dx, -angle, j_num_dx)
        jj_code.extend(jj_tmp)
        # jj punch +++ down --------
        jj_tmp = laa(x_centre_d - mm / 2 + jj_dx_s, y_centre_d + jj_dy_s, angle, j_diff_dx, angle, j_num_dx)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d - mm / 2 + jj_dx_s, y_centre_d - jj_dy_s, -angle, j_diff_dx, -angle, j_num_dx)
        jj_code.extend(jj_tmp)

        code_tmp = 'O' + str(mm)
        code.append(code_tmp)
        code_tmp = 'X' + format(float(1250), '0.0f') + 'Y' + format(
            float(1280)) + 'M02'
        code.append(code_tmp)
        code.extend(hole_code)
        code.extend(side_code)
        code.extend(jj_code)
        # *******************??????????????????????????????????????
        code_tmp = loc(x_centre_d - dx_axis, 100) + 'M03'
        code.append(code_tmp)
        code_tmp = 'REP/DX' + format(float(part_width / 3), '0.2f')
        code.append(code_tmp)

        # 中-----------------------------------------------------------------------------------------------
        # hole +++ up -----------------
        hole_code = []
        gauge_num_dx_t = gauge_num_dx(dx_axis, gauge_t, jj_length, mm)
        code_tmp = laa(x_centre_d + hole_dx, y_centre_u + high / 2 + hole_dy, 0.0, gauge_t, angle=-angle,
                       qty=gauge_num_dx_t)
        code_tmp = [code_tmp[0] + "T16(DIA X 6)", code_tmp[1]]  # ???????????????
        hole_code.extend(code_tmp)
        code_tmp = laa(x_centre_d - hole_dx, y_centre_u + high / 2 + hole_dy, 0.0, gauge_t, angle=180 + angle,
                       qty=gauge_num_dx_t)
        hole_code.extend(code_tmp)

        code_tmp = laa(x_centre_d - hole_dx, y_centre_u - high / 2 - hole_dy, 0.0, gauge_t, angle=180 - angle,
                       qty=gauge_num_dx_t)
        hole_code.extend(code_tmp)
        code_tmp = laa(x_centre_d + hole_dx, y_centre_u - high / 2 - hole_dy, 0.0, gauge_t, angle=angle,
                       qty=gauge_num_dx_t)
        hole_code.extend(code_tmp)
        # hole +++ down ---------------
        code_tmp = laa(x_centre_d + hole_dx, y_centre_d + high / 2 + hole_dy, 0.0, gauge_t, angle=-angle,
                       qty=gauge_num_dx_t)
        code_tmp = [code_tmp[0] + "T16(DIA X 6)", code_tmp[1]]  # ???????????????
        hole_code.extend(code_tmp)
        code_tmp = laa(x_centre_d - hole_dx, y_centre_d + high / 2 + hole_dy, 0.0, gauge_t, angle=180 + angle,
                       qty=gauge_num_dx_t)
        hole_code.extend(code_tmp)

        code_tmp = laa(x_centre_d - hole_dx, y_centre_d - high / 2 - hole_dy, 0.0, gauge_t, angle=180 - angle,
                       qty=gauge_num_dx_t)
        hole_code.extend(code_tmp)
        code_tmp = laa(x_centre_d + hole_dx, y_centre_d - high / 2 - hole_dy, 0.0, gauge_t, angle=angle,
                       qty=gauge_num_dx_t)
        hole_code.extend(code_tmp)
        # side +++ up --------------------------
        side_code = []
        side_tmp = loc(x_centre_d + side_dx + dx_tool, y_centre_u + high / 2 + side_dy + dy_tool)
        side_tmp = side_tmp + 'T12C' + format(float(90 - angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width), '0.2f') + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - side_dx - dx_tool, y_centre_u + high / 2 + side_dy + dy_tool)
        side_tmp = side_tmp + 'C' + format(float(90 + angle), '0.2f')
        side_code.append(side_tmp)

        side_tmp = loc(x_centre_d - side_dx - dx_tool, y_centre_u - high / 2 - side_dy - dy_tool)
        side_tmp = side_tmp + 'C' + format(float(90 - angle), '0.2f')
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + side_dx + dx_tool, y_centre_u - high / 2 - side_dy - dy_tool)
        side_tmp = side_tmp + 'C' + format(float(90 + angle), '0.2f')
        side_code.append(side_tmp)
        # side +++ down --------------------------
        side_tmp = loc(x_centre_d + side_dx + dx_tool, y_centre_d + high / 2 + side_dy + dy_tool)
        side_tmp = side_tmp + 'C' + format(float(90 - angle), '0.2f')
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - side_dx - dx_tool, y_centre_d + high / 2 + side_dy + dy_tool)
        side_tmp = side_tmp + 'C' + format(float(90 + angle), '0.2f')
        side_code.append(side_tmp)

        side_tmp = loc(x_centre_d - side_dx - dx_tool, y_centre_d - high / 2 - side_dy - dy_tool)
        side_tmp = side_tmp + 'C' + format(float(90 - angle), '0.2f')
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + side_dx + dx_tool, y_centre_d - high / 2 - side_dy - dy_tool)
        side_tmp = side_tmp + 'C' + format(float(90 + angle), '0.2f')
        side_code.append(side_tmp)

        # jj +++ up -------------
        jj_code = []
        j_num_dx, j_diff_dx = jj_num_dx(dx_axis - jj_dx, 0.5, jj_length, mm, tool_length)
        jj_tmp = laa(x_centre_d + jj_dx, y_centre_u + high / 2 + jj_dy, -angle, j_diff_dx, -angle, j_num_dx)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d - jj_dx, y_centre_u + high / 2 + jj_dy, 180 + angle, j_diff_dx, 180 + angle, j_num_dx)
        jj_code.extend(jj_tmp)

        jj_tmp = laa(x_centre_d - jj_dx, y_centre_u - high / 2 - jj_dy, 180 - angle, j_diff_dx, 180 - angle, j_num_dx)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d + jj_dx, y_centre_u - high / 2 - jj_dy, angle, j_diff_dx, angle, j_num_dx)
        jj_code.extend(jj_tmp)

        # jj +++ down -------------
        jj_tmp = laa(x_centre_d + jj_dx, y_centre_d + high / 2 + jj_dy, -angle, j_diff_dx, -angle, j_num_dx)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d - jj_dx, y_centre_d + high / 2 + jj_dy, 180 + angle, j_diff_dx, 180 + angle, j_num_dx)
        jj_code.extend(jj_tmp)

        jj_tmp = laa(x_centre_d - jj_dx, y_centre_d - high / 2 - jj_dy, 180 - angle, j_diff_dx, 180 - angle, j_num_dx)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d + jj_dx, y_centre_d - high / 2 - jj_dy, angle, j_diff_dx, angle, j_num_dx)
        jj_code.extend(jj_tmp)

        code.extend(hole_code)
        code.extend(side_code)
        code.extend(jj_code)
        code_tmp = loc(x_centre_d + dx_axis, 100) + 'M03'  # *******************??????????????????????????????????????
        code.append(code_tmp)
        code_tmp = 'REP/DX' + format(float(part_width / 3), '0.2f')
        code.append(code_tmp)
        # 右-----------------------------------------------------------------------------------------------
        hole_code = []
        gauge_num_dx_t = gauge_num_dx(mm / 2 - hole_dx_s - dx_axis, gauge_t, jj_length, mm)
        # hole ++++ up ------
        code_tmp = laa(x_centre_d + mm / 2 - hole_dx_s, y_centre_u + hole_dy_s, 0.0, gauge_t, angle=180 - angle,
                       qty=gauge_num_dx_t)
        code_tmp = [code_tmp[0] + "T16(DIA X 6)", code_tmp[1]]
        hole_code.extend(code_tmp)

        code_tmp = laa(x_centre_d + mm / 2 - hole_dx_s, y_centre_u - hole_dy_s, 0.0, gauge_t, angle=180 + angle,
                       qty=gauge_num_dx_t)
        hole_code.extend(code_tmp)
        # hole ++++ down ------
        code_tmp = laa(x_centre_d + mm / 2 - hole_dx_s, y_centre_d + hole_dy_s, 0.0, gauge_t, angle=180 - angle,
                       qty=gauge_num_dx_t)
        code_tmp = [code_tmp[0] + "T16(DIA X 6)", code_tmp[1]]
        hole_code.extend(code_tmp)

        code_tmp = laa(x_centre_d + mm / 2 - hole_dx_s, y_centre_d - hole_dy_s, 0.0, gauge_t, angle=180 + angle,
                       qty=gauge_num_dx_t)
        hole_code.extend(code_tmp)

        # side punch +++ up ------
        side_code = []
        side_tmp = loc(x_centre_d + mm / 2 + side_dx_s, y_centre_u + side_dy_s)
        side_tmp = side_tmp + 'T12C' + format(float(90 - angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width)) + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + mm / 2 + side_dx_s, y_centre_u - side_dy_s)
        side_tmp = side_tmp + 'T12C' + format(float(90 + angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width)) + ')'
        side_code.append(side_tmp)
        # side punch +++ down ------
        side_tmp = loc(x_centre_d + mm / 2 + side_dx_s, y_centre_d + side_dy_s)
        side_tmp = side_tmp + 'T12C' + format(float(90 - angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width)) + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + mm / 2 + side_dx_s, y_centre_d - side_dy_s)
        side_tmp = side_tmp + 'T12C' + format(float(90 + angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width)) + ')'
        side_code.append(side_tmp)

        # jj punch +++ up --------
        jj_code = []
        j_num_dx, j_diff_dx = jj_num_dx(mm / 2 - dx_axis - jj_dx_s, 0.5, jj_length, mm, tool_length)
        jj_tmp = laa(x_centre_d + mm / 2 - jj_dx_s, y_centre_u + jj_dy_s, 180 - angle, j_diff_dx, 180 - angle, j_num_dx)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d + mm / 2 - jj_dx_s, y_centre_u - jj_dy_s, 180 + angle, j_diff_dx, 180 + angle, j_num_dx)
        jj_code.extend(jj_tmp)
        # jj punch +++ down --------
        jj_tmp = laa(x_centre_d + mm / 2 - jj_dx_s, y_centre_d + jj_dy_s, 180 - angle, j_diff_dx, 180 - angle, j_num_dx)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d + mm / 2 - jj_dx_s, y_centre_d - jj_dy_s, 180 + angle, j_diff_dx, 180 + angle, j_num_dx)
        jj_code.extend(jj_tmp)

        code.extend(hole_code)
        code.extend(side_code)
        code.extend(jj_code)

        code_tmp = 'C0.M03'
        code.append(code_tmp)
        code_tmp = 'X' + format(float(part_width/3*2+1250), '0.2f') + 'Y1280M03'
        code.append(code_tmp)
        code_tmp = 'FRM/X1250'
        code.append(code_tmp)
        code_tmp = 'X1250Y1280M30'
        code.append(code_tmp)

    elif 3750 < mm <= 5000:
        hole_code = []
        dx_axis = mm / 4
        gauge_num_dx_t = gauge_num_dx(x_centre_d - hole_dx_s - dx_axis, gauge_t, jj_length, mm)
        # 左-----------------------------------------------------------------------------------------------
        # hole ++++ up ------
        code_tmp = laa(x_centre_d - mm / 2 + hole_dx_s, y_centre_u + hole_dy_s, 0.0, gauge_t, angle=angle,
                       qty=gauge_num_dx_t)
        code_tmp = [code_tmp[0] + "T16(DIA X 6)", code_tmp[1]]
        hole_code.extend(code_tmp)

        code_tmp = laa(x_centre_d - mm / 2 + hole_dx_s, y_centre_u - hole_dy_s, 0.0, gauge_t, angle=-angle,
                       qty=gauge_num_dx_t)
        hole_code.extend(code_tmp)
        # hole ++++ down ------
        code_tmp = laa(x_centre_d - mm / 2 + hole_dx_s, y_centre_d + hole_dy_s, 0.0, gauge_t, angle=angle,
                       qty=gauge_num_dx_t)
        code_tmp = [code_tmp[0] + "T16(DIA X 6)", code_tmp[1]]
        hole_code.extend(code_tmp)

        code_tmp = laa(x_centre_d - mm / 2 + hole_dx_s, y_centre_d - hole_dy_s, 0.0, gauge_t, angle=-angle,
                       qty=gauge_num_dx_t)
        hole_code.extend(code_tmp)

        # side punch +++ up ------
        side_code = []
        side_tmp = loc(x_centre_d - mm / 2 - side_dx_s, y_centre_u + side_dy_s)
        side_tmp = side_tmp + 'T12C' + format(float(90 + angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width)) + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - mm / 2 - side_dx_s, y_centre_u - side_dy_s)
        side_tmp = side_tmp + 'T12C' + format(float(90 - angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width)) + ')'
        side_code.append(side_tmp)
        # side punch +++ down ------
        side_tmp = loc(x_centre_d - mm / 2 - side_dx_s, y_centre_d + side_dy_s)
        side_tmp = side_tmp + 'T12C' + format(float(90 + angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width)) + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - mm / 2 - side_dx_s, y_centre_d - side_dy_s)
        side_tmp = side_tmp + 'T12C' + format(float(90 - angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width)) + ')'
        side_code.append(side_tmp)

        # jj punch +++ up --------
        jj_code = []
        j_num_dx, j_diff_dx = jj_num_dx(mm / 2 - dx_axis - jj_dx, 0.5, jj_length, mm, tool_length)
        jj_tmp = laa(x_centre_d - mm / 2 + jj_dx_s, y_centre_u + jj_dy_s, angle, j_diff_dx, angle, j_num_dx)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d - mm / 2 + jj_dx_s, y_centre_u - jj_dy_s, -angle, j_diff_dx, -angle, j_num_dx)
        jj_code.extend(jj_tmp)
        # jj punch +++ down --------
        jj_tmp = laa(x_centre_d - mm / 2 + jj_dx_s, y_centre_d + jj_dy_s, angle, j_diff_dx, angle, j_num_dx)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d - mm / 2 + jj_dx_s, y_centre_d - jj_dy_s, -angle, j_diff_dx, -angle, j_num_dx)
        jj_code.extend(jj_tmp)

        code_tmp = 'O' + str(mm)
        code.append(code_tmp)
        code_tmp = 'X' + format(float(1250), '0.0f') + 'Y' + format(
            float(1280)) + 'M02'
        code.append(code_tmp)
        code.extend(hole_code)
        code.extend(side_code)
        code.extend(jj_code)
        # *******************??????????????????????????????????????
        code_tmp = loc(x_centre_d - dx_axis, 100) + 'M03'
        code.append(code_tmp)
        code_tmp = 'REP/DX' + format(float(part_width / 4), '0.2f')
        code.append(code_tmp)

        # 中---左--------------------------------------------------------------------------------------------
        # hole +++ up -----------------
        hole_code = []
        gauge_num_dx_t = gauge_num_dx(dx_axis, gauge_t, jj_length, mm)
        code_tmp = laa(x_centre_d - hole_dx, y_centre_u + high / 2 + hole_dy, 0.0, gauge_t, angle=180 + angle,
                       qty=gauge_num_dx_t)
        code_tmp = [code_tmp[0] + "T16(DIA X 6)", code_tmp[1]]  # ???????????????
        hole_code.extend(code_tmp)

        code_tmp = laa(x_centre_d - hole_dx, y_centre_u - high / 2 - hole_dy, 0.0, gauge_t, angle=180 - angle,
                       qty=gauge_num_dx_t)
        hole_code.extend(code_tmp)
        # hole +++ down ---------------
        code_tmp = laa(x_centre_d - hole_dx, y_centre_d + high / 2 + hole_dy, 0.0, gauge_t, angle=180 + angle,
                       qty=gauge_num_dx_t)
        code_tmp = [code_tmp[0] + "T16(DIA X 6)", code_tmp[1]]  # ???????????????
        hole_code.extend(code_tmp)

        code_tmp = laa(x_centre_d - hole_dx, y_centre_d - high / 2 - hole_dy, 0.0, gauge_t, angle=180 - angle,
                       qty=gauge_num_dx_t)
        hole_code.extend(code_tmp)
        # side +++ up --------------------------
        side_code = []
        side_tmp = loc(x_centre_d - side_dx - dx_tool, y_centre_u + high / 2 + side_dy + dy_tool)
        side_tmp = side_tmp + 'T12C' + format(float(90 + angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width), '0.2f') + ')'
        side_code.append(side_tmp)

        side_tmp = loc(x_centre_d - side_dx - dx_tool, y_centre_u - high / 2 - side_dy - dy_tool)
        side_tmp = side_tmp + 'C' + format(float(90 - angle), '0.2f')
        side_code.append(side_tmp)
        # side +++ down --------------------------
        side_tmp = loc(x_centre_d - side_dx - dx_tool, y_centre_d + high / 2 + side_dy + dy_tool)
        side_tmp = side_tmp + 'C' + format(float(90 + angle), '0.2f')
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - side_dx - dx_tool, y_centre_d - high / 2 - side_dy - dy_tool)
        side_tmp = side_tmp + 'C' + format(float(90 - angle), '0.2f')
        side_code.append(side_tmp)

        # jj +++ up -------------
        jj_code = []
        j_num_dx, j_diff_dx = jj_num_dx(dx_axis - jj_dx, 0.5, jj_length, mm, tool_length)
        jj_tmp = laa(x_centre_d - jj_dx, y_centre_u + high / 2 + jj_dy, 180 + angle, j_diff_dx, 180 + angle, j_num_dx)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d - jj_dx, y_centre_u - high / 2 - jj_dy, 180 - angle, j_diff_dx, 180 - angle, j_num_dx)
        jj_code.extend(jj_tmp)

        # jj +++ down -------------
        jj_tmp = laa(x_centre_d - jj_dx, y_centre_d + high / 2 + jj_dy, 180 + angle, j_diff_dx, 180 + angle, j_num_dx)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d - jj_dx, y_centre_d - high / 2 - jj_dy, 180 - angle, j_diff_dx, 180 - angle, j_num_dx)
        jj_code.extend(jj_tmp)

        code.extend(hole_code)
        code.extend(side_code)
        code.extend(jj_code)
        code_tmp = loc(x_centre_d, 100) + 'M03'  # *******************??????????????????????????????????????
        code.append(code_tmp)
        code_tmp = 'REP/DX' + format(float(part_width / 4), '0.2f')
        code.append(code_tmp)

        # 中===右 ===========================================
        # hole +++ up ---------------
        hole_code = []
        code_tmp = laa(x_centre_d + hole_dx, y_centre_u + high / 2 + hole_dy, 0.0, gauge_t, angle=-angle,
                       qty=gauge_num_dx_t)
        code_tmp = [code_tmp[0] + "T16(DIA X 6)", code_tmp[1]]  # ???????????????
        hole_code.extend(code_tmp)
        code_tmp = laa(x_centre_d + hole_dx, y_centre_u - high / 2 - hole_dy, 0.0, gauge_t, angle=angle,
                       qty=gauge_num_dx_t)
        hole_code.extend(code_tmp)
        # hole +++ down -------------
        code_tmp = laa(x_centre_d + hole_dx, y_centre_d + high / 2 + hole_dy, 0.0, gauge_t, angle=-angle,
                       qty=gauge_num_dx_t)
        hole_code.extend(code_tmp)
        code_tmp = laa(x_centre_d + hole_dx, y_centre_d - high / 2 - hole_dy, 0.0, gauge_t, angle=angle,
                       qty=gauge_num_dx_t)
        hole_code.extend(code_tmp)
        # side +++ up ---------------
        side_code = []
        side_tmp = loc(x_centre_d + side_dx + dx_tool, y_centre_u + high / 2 + side_dy + dy_tool)
        side_tmp = side_tmp + 'T12C' + format(float(90 - angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width), '0.2f') + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + side_dx + dx_tool, y_centre_u - high / 2 - side_dy - dy_tool)
        side_tmp = side_tmp + 'C' + format(float(90 + angle), '0.2f')
        side_code.append(side_tmp)
        # side +++ down -------------
        side_tmp = loc(x_centre_d + side_dx + dx_tool, y_centre_d + high / 2 + side_dy + dy_tool)
        side_tmp = side_tmp + 'C' + format(float(90 - angle), '0.2f')
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + side_dx + dx_tool, y_centre_d - high / 2 - side_dy - dy_tool)
        side_tmp = side_tmp + 'C' + format(float(90 + angle), '0.2f')
        side_code.append(side_tmp)

        # jj +++ up -----------------
        jj_code = []

        jj_tmp = laa(x_centre_d + jj_dx, y_centre_u + high / 2 + jj_dy, -angle, j_diff_dx, -angle, j_num_dx)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d + jj_dx, y_centre_u - high / 2 - jj_dy, angle, j_diff_dx, angle, j_num_dx)
        jj_code.extend(jj_tmp)
        # jj +++ down ---------------
        jj_tmp = laa(x_centre_d + jj_dx, y_centre_d + high / 2 + jj_dy, -angle, j_diff_dx, -angle, j_num_dx)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d + jj_dx, y_centre_d - high / 2 - jj_dy, angle, j_diff_dx, angle, j_num_dx)
        jj_code.extend(jj_tmp)

        # adjust move clip -------------
        code.extend(hole_code)
        code.extend(side_code)
        code.extend(jj_code)
        code_tmp = loc(x_centre_d + dx_axis, 100) + 'M03'  # *******************??????????????????????????????????????
        code.append(code_tmp)
        code_tmp = 'REP/DX' + format(float(part_width / 4), '0.2f')
        code.append(code_tmp)

        # 右-----------------------------------------------------------------------------------------------
        hole_code = []
        gauge_num_dx_t = gauge_num_dx(mm / 2 - hole_dx_s - dx_axis, gauge_t, jj_length, mm)
        # hole ++++ up ------
        code_tmp = laa(x_centre_d + mm / 2 - hole_dx_s, y_centre_u + hole_dy_s, 0.0, gauge_t, angle=180 - angle,
                       qty=gauge_num_dx_t)
        code_tmp = [code_tmp[0] + "T16(DIA X 6)", code_tmp[1]]
        hole_code.extend(code_tmp)

        code_tmp = laa(x_centre_d + mm / 2 - hole_dx_s, y_centre_u - hole_dy_s, 0.0, gauge_t, angle=180 + angle,
                       qty=gauge_num_dx_t)
        hole_code.extend(code_tmp)
        # hole ++++ down ------
        code_tmp = laa(x_centre_d + mm / 2 - hole_dx_s, y_centre_d + hole_dy_s, 0.0, gauge_t, angle=180 - angle,
                       qty=gauge_num_dx_t)
        code_tmp = [code_tmp[0] + "T16(DIA X 6)", code_tmp[1]]
        hole_code.extend(code_tmp)

        code_tmp = laa(x_centre_d + mm / 2 - hole_dx_s, y_centre_d - hole_dy_s, 0.0, gauge_t, angle=180 + angle,
                       qty=gauge_num_dx_t)
        hole_code.extend(code_tmp)

        # side punch +++ up ------
        side_code = []
        side_tmp = loc(x_centre_d + mm / 2 + side_dx_s, y_centre_u + side_dy_s)
        side_tmp = side_tmp + 'T12C' + format(float(90 - angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width)) + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + mm / 2 + side_dx_s, y_centre_u - side_dy_s)
        side_tmp = side_tmp + 'T12C' + format(float(90 + angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width)) + ')'
        side_code.append(side_tmp)
        # side punch +++ down ------
        side_tmp = loc(x_centre_d + mm / 2 + side_dx_s, y_centre_d + side_dy_s)
        side_tmp = side_tmp + 'T12C' + format(float(90 - angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width)) + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + mm / 2 + side_dx_s, y_centre_d - side_dy_s)
        side_tmp = side_tmp + 'T12C' + format(float(90 + angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width)) + ')'
        side_code.append(side_tmp)

        # jj punch +++ up --------
        jj_code = []
        # j_num_dx, j_diff_dx = jj_num_dx(x_centre_d - mm / 2 - jj_dx, 0.5, jj_length, mm, tool_length)
        jj_tmp = laa(x_centre_d + mm / 2 - jj_dx_s, y_centre_u + jj_dy_s, 180 - angle, j_diff_dx, 180 - angle, j_num_dx)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d + mm / 2 - jj_dx_s, y_centre_u - jj_dy_s, 180 + angle, j_diff_dx, 180 + angle, j_num_dx)
        jj_code.extend(jj_tmp)
        # jj punch +++ down --------
        jj_tmp = laa(x_centre_d + mm / 2 - jj_dx_s, y_centre_d + jj_dy_s, 180 - angle, j_diff_dx, 180 - angle, j_num_dx)
        jj_code.extend(jj_tmp)
        jj_tmp = laa(x_centre_d + mm / 2 - jj_dx_s, y_centre_d - jj_dy_s, 180 + angle, j_diff_dx, 180 + angle, j_num_dx)
        jj_code.extend(jj_tmp)

        code.extend(hole_code)
        code.extend(side_code)
        code.extend(jj_code)

        code_tmp = 'C0.M03'
        code.append(code_tmp)
        code_tmp = 'X' + format(float(part_width/4*3+1250), '0.2f') + 'Y1280M03'
        code.append(code_tmp)
        code_tmp = 'FRM/X1250'
        code.append(code_tmp)
        code_tmp = 'X1250Y1280M30'
        code.append(code_tmp)
    else:
        print('These Length Parts haven"t been programmed!')

    return code


def save(code_org, length):
    file_name = './' + str(length) + '.txt'
    try:
        with open(file_name, 'w', newline='') as txt_file:
            for line in code_org:
                txt_file.write(line + '\r\n')
            txt_file.close()
    except Exception as e:
        QMessageBox.warning(None, '保存出错:', '文件未保存!!!\n' + str(e))
        return 0


if __name__ == '__main__':
    mm_list = [155, 315, 340, 360, 375, 400, 425, 455, 470, 490, 525, 535, 550, 570, 580, 595, 600, 605, 610, 635, 645,
               655, 675, 685, 700, 720, 730, 750, 770, 780, 800, 820, 840, 845, 865, 880, 895, 915, 940, 965, 995, 1000,
               1005, 1010, 1020, 1035, 1060, 1070, 1080, 1100, 1110, 1125, 1140, 1160, 1170, 1210, 1220, 1240, 1260,
               1310, 1335, 1360, 1420, 1450, 1470, 1495, 1520, 1555, 1580, 1600, 1650, 1675, 1715, 1755, 1785, 1800,
               1830,
               1870, 1950, 1990, 2005, 2045, 2050, 2100, 2150, 2180, 2200, 2235, 2260, 2310, 2350, 2400, 2450, 1490]
    mm_list_2500 = [2530, 2550, 2600, 2630, 2690, 2750, 2760, 2950, 3285, 3580, 3745, 3805, 3945, 4145, 4925]

    mm_list_test = [2600]
    for mm in mm_list_test:
        high = 212
        tool_width = 5.08
        tool_length = 35.56
        gauge_number = None
        gauge = None
        jj_length = jj(mm, high)
        code = g810974(mm, high, jj_length, tool_width, tool_length, gauge_number, gauge)
        save(code, mm)
