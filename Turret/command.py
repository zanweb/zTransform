#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :   2020/3/16 10:29
# @Author   :   ZANWEB
# @File     :   command.py in zTransform
# @IDE      :   PyCharm
from math import sqrt, atan, degrees, ceil
from PyQt5.QtWidgets import QMessageBox

JJ_SHORT = 33
CLIP_MARGE = 80
PART_MARGE = 20
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


def hole_parameter(mm, high, jj_length, gauge, gauge_number):
    hole_side_marge = (jj_length - gauge * gauge_number) / 2
    critical_value_side_marge = mm * JJ_SHORT / high
    if critical_value_side_marge > hole_side_marge:
        hole_y_diff = (mm * 12 - high * hole_side_marge) / 2 / jj_length
        hole_x_diff = (12 * high + hole_side_marge * mm) / 2 / jj_length
    else:
        hole_x_diff = 12 * jj_length / (high / 2) + mm / 2 * (hole_side_marge - 12 * mm / 2 / (high / 2))
        hole_y_diff = mm / 2 * (hole_side_marge * high / 2 - 12 * mm / 2)
        hole_y_diff = - hole_y_diff
    return hole_x_diff, hole_y_diff


def side_parameter(mm, high, jj_length, tool_width, tool_length):
    dx = mm / 2 / jj_length * ((tool_length / 2 * high / mm) - tool_width / 2)
    dy = tool_length / 2 * mm / 2 / jj_length
    return dx, dy


def jj_parameter(mm, high, jj_length, tool_width, tool_length):
    dx = mm / 2 / jj_length * (1 + tool_length / 2) + high / 2 / jj_length * (JJ_SHORT + tool_width / 2)
    dy = high / 2 / jj_length * (1 + tool_length / 2) - mm / 2 / jj_length * (JJ_SHORT + tool_width / 2)
    return dx, dy


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
    jj_dx, jj_dy = jj_parameter(mm, high, jj_length, tool_width, tool_length)

    # 开始
    code = []
    angle = degrees(atan(high / mm))
    j_num = int((jj_length - 2 - tool_length) / tool_length)
    j_diff = (jj_length - 2 - tool_length) / j_num

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
        side_tmp = loc(x_centre_d + mm / 2 + side_dx, y_centre_u + side_dy)
        side_tmp = side_tmp + 'T12C' + format(float(90 - angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width)) + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + side_dx + dx_tool, y_centre_u + high / 2 + side_dy + dy_tool)
        side_code.append(side_tmp)

        side_tmp = loc(x_centre_d - mm / 2 - side_dx, y_centre_u - side_dy)
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - side_dx - dx_tool, y_centre_u - high / 2 - side_dy - dy_tool)
        side_code.append(side_tmp)

        side_tmp = loc(x_centre_d + mm / 2 + side_dx, y_centre_d + side_dy)
        side_tmp = side_tmp + 'C' + format(float(90 - angle), '0.2f')
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + side_dx + dx_tool, y_centre_d + high / 2 + side_dy + dy_tool)
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - mm / 2 - side_dx, y_centre_d - side_dy)
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - side_dx - dx_tool, y_centre_d - high / 2 - side_dy - dy_tool)
        side_code.append(side_tmp)
        # ============

        side_tmp = loc(x_centre_d - side_dx - dx_tool, y_centre_u + high / 2 + side_dy + dy_tool)
        side_tmp = side_tmp + 'T12C' + format(float(90 + angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width)) + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - mm / 2 - side_dx, y_centre_u + side_dy)
        side_code.append(side_tmp)

        side_tmp = loc(x_centre_d + side_dx + dx_tool, y_centre_u - high / 2 - side_dy - dy_tool)
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + mm / 2 + side_dx, y_centre_u - side_dy)
        side_code.append(side_tmp)

        side_tmp = loc(x_centre_d - side_dx - dx_tool, y_centre_d + side_dy + dy_tool)
        side_tmp = side_tmp + 'C' + format(float(90 + angle), '0.2f')
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - mm / 2 - side_dx, y_centre_d + side_dy)
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + side_dx + dx_tool, y_centre_d - high / 2 - side_dy - dy_tool)
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + mm / 2 + side_dx, y_centre_d - side_dy)
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

    if 1250 < mm <= 2500:
        # j_num = int((jj_length - 2 - tool_length) / tool_length)
        # j_diff = (jj_length - 2 - tool_length) / j_num

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
        side_tmp = loc(x_centre_d - side_dx-dx_tool, y_centre_u + high / 2 + side_dy+dy_tool)
        side_tmp = side_tmp + 'T12C' + format(float(90 + angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width), '0.2f') + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - mm / 2 - side_dx, y_centre_u + side_dy)
        side_code.append(side_tmp)

        side_tmp = loc(x_centre_d - mm / 2 - side_dx, y_centre_u - side_dy)
        side_tmp = side_tmp + 'T12C' + format(float(90 - angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width), '0.2f') + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - side_dx-dx_tool, y_centre_u - high / 2 - side_dy-dy_tool)
        side_code.append(side_tmp)
        # side-down =============
        side_tmp = loc(x_centre_d - side_dx-dx_tool, y_centre_d + high / 2 + side_dy+dy_tool)
        side_tmp = side_tmp + 'T12C' + format(float(90 + angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width), '0.2f') + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - mm / 2 - side_dx, y_centre_d + side_dy)
        side_code.append(side_tmp)

        side_tmp = loc(x_centre_d - mm / 2 - side_dx, y_centre_d - side_dy)
        side_tmp = side_tmp + 'T12C' + format(float(90 - angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width), '0.2f') + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d - side_dx-dx_tool, y_centre_d - high / 2 - side_dy-dy_tool)
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
        # x_centre_d = 0  # ????????????????????????????????????????
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
        side_tmp = loc(x_centre_d + mm / 2 + side_dx, y_centre_u + side_dy)
        side_tmp = side_tmp + 'T12C' + format(float(90 - angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width), '0.2f') + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + side_dx+dx_tool, y_centre_u + high / 2 + side_dy+dy_tool)
        side_code.append(side_tmp)

        side_tmp = loc(x_centre_d + side_dx+dx_tool, y_centre_u - high / 2 - side_dy-dy_tool)
        side_tmp = side_tmp + 'C' + format(float(90 + angle), '0.2f')
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + mm / 2 + side_dx, y_centre_u - side_dy)
        side_code.append(side_tmp)

        # side-down ====================================
        side_tmp = loc(x_centre_d + mm / 2 + side_dx, y_centre_d + side_dy)
        side_tmp = side_tmp + 'T12C' + format(float(90 - angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width), '0.2f') + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + side_dx+dx_tool, y_centre_d + high / 2 + side_dy+dy_tool)
        side_code.append(side_tmp)

        side_tmp = loc(x_centre_d + side_dx+dx_tool, y_centre_d - high / 2 - side_dy-dy_tool)
        side_tmp = side_tmp + 'T12C' + format(float(90 + angle), '0.2f') + '(REC X' + format(float(tool_length),
                                                                                             '0.2f') + 'Y' + format(
            float(tool_width), '0.2f') + ')'
        side_code.append(side_tmp)
        side_tmp = loc(x_centre_d + mm / 2 + side_dx, y_centre_d - side_dy)
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
        code_tmp = 'M99'
        code.append(code_tmp)
        print(code)

    if 2500 < mm <= 3750:
        pass
    if 3750 < mm <= 5000:
        pass

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
    mm = 1060
    high = 212
    tool_width = 5.08
    tool_length = 35.56
    gauge_number = None
    gauge = None
    jj_length = jj(mm, high)
    code = g810974(mm, high, jj_length, tool_width, tool_length, gauge_number, gauge)
    save(code, mm)
