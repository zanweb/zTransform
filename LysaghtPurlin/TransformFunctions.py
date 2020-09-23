#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :   2019/10/25 9:22
# @Author   :   ZANWEB
# @File     :   TransformFunctions.py in zTransform
# @IDE      :   PyCharm
import copy
import os
import sys
import re
from functools import reduce
from operator import itemgetter

import LysaghtPurlin.Part as lpart
from CamGen.NCBase import Nc, is_exist_nc
from DTRGen.Order import *
from DTRGen.Part import *
from LysaghtPurlin import Batch
from LysaghtPurlin import Bundle
from LysaghtPurlin import Order
from Zfile import zCSV, zFBase
from zBase.constant import MM_INCH, CENTER_N, CENTER_P

from PyQt5.QtWidgets import QWidgetItem, QTreeWidgetItemIterator

SPLICE_LENGTH = 4000 / MM_INCH      # 拼接限制长度(长)
SPLICE_LENGTH_S = 2000 / MM_INCH    # 拼接限制长度(短)
MIN_LENGTH = 1500 / MM_INCH         # 长/短件分界点
MAX_SPLICE_QTY = 5                  # 最多拼接件数/件
sys.setrecursionlimit(3000)


def merge_cut_list_items(cut_list_org):
    cut_list = CutList()
    # org_cut_list = sorted(cut_list_org.cut_list, key='item_id')
    org_cut_list = cut_list_org.cut_list
    org_cut_list.sort(key=attrgetter('item_id'))
    org_cut_list.sort(key=attrgetter('length'), reverse=False)
    for index, group in groupby(org_cut_list, attrgetter('item_id')):
        l_group = list(group)
        if len(l_group) == 1:
            cut_list.append(l_group[0])
        else:
            qty = 0
            # print(l_group)
            tmp = l_group[0]
            for item in l_group:
                tmp = item
                qty += item.quantity
            tmp.quantity = qty
            cut_list.append(tmp)
    cut_list.cut_list.sort(key=attrgetter('length'), reverse=True)
    return cut_list


def process_half_cut(cut_list_org, parts_org):
    # 判断半切清单
    # 先理出1.5m以下的list(auto_no, part_num, length, qty)
    # 相同材料，半切匹配，无法匹配的再与同材料大于1.5m的匹配，再无法匹配，列清单
    new_cut_list = CutList()
    new_parts = Parts()
    material_cut_list = []
    unable_splice = []
    # print(cut_list_org.cut_list)
    cut_list = merge_cut_list_items(cut_list_org)
    cut_list.cut_list.sort(key=attrgetter('material'))
    for raw_index, raw_group in groupby(cut_list.cut_list, attrgetter('material')):
        material_cut_list.append(list(raw_group))
    for raw_group in material_cut_list:
        # 每组材料
        print(raw_group)
        raw_group.sort(key=attrgetter('length'), reverse=True)
        raw_group.sort(key=attrgetter('bundle'))
        for bundle_index, bundle_group in groupby(raw_group, attrgetter('bundle')):
            bundle_list = list(bundle_group)
            group_cut_list, group_parts, group_unable_splice = core_calculate_for_half_cut_1(bundle_list, parts_org)
            new_cut_list.extend(group_cut_list)
            new_parts.append(group_parts)
            unable_splice.extend(group_unable_splice)
    return new_cut_list, new_parts, unable_splice


def core_calculate_for_half_cut_1(raw_group, parts):
    half_cut_long = []  # 长件 >=1500
    half_cut_short = []  # 短件

    new_parts_r = []
    new_items_r = []
    unable_splice_r = []

    # 按长度分
    for cut_item in raw_group:
        if cut_item.length >= MIN_LENGTH:
            half_cut_long.append(cut_item)
        else:
            half_cut_short.append(cut_item)
    # 处理拼接
    if half_cut_short:
        new_items_t, new_parts_t, unable_splice_t = splice_in_short(half_cut_short, parts, new_items_r, new_parts_r, unable_splice_r)
        half_cut_long.extend(new_items_t)
        new_items_r = half_cut_long
        parts.extend(new_parts_t)
        new_parts_r = parts
    else:
        new_items_r = half_cut_long
        new_parts_r = parts
    return new_items_r, new_parts_r, unable_splice_r


def splice_in_short(items, parts, new_items, new_parts, unable_splice):
    if len(items) == 0:
        return new_items, new_parts, unable_splice
    else:
        one_item = items.pop(0)
        qty = one_item.quantity
        length = one_item.length
        div_s, mode_s = divmod(SPLICE_LENGTH, length)
        if div_s > MAX_SPLICE_QTY:
            div = MAX_SPLICE_QTY
        else:
            div = int(div_s)
        count = qty//div
        if count == 0:
            if len(items) == 0:
                if (qty * length) < MIN_LENGTH:
                    unable_splice.append(one_item)
                    return splice_in_short(items, parts, new_items, new_parts, unable_splice)
                else:
                    new_item, new_part = splice_qty(one_item, int(qty), parts)
                    new_items.append(new_item)
                    new_parts.append(new_part)
                    return splice_in_short(items, parts, new_items, new_parts, unable_splice)
            else:
                total_length = one_item.length*one_item.quantity
                total_qty = one_item.quantity
                splice_list_tmp = [(one_item, one_item.quantity)]
                if one_item.length > 500/MM_INCH:
                    max_length = SPLICE_LENGTH
                else:
                    max_length = SPLICE_LENGTH_S
                while total_length <= max_length:
                    if len(items) > 0:
                        item_tmp = items.pop(0)
                        qty_tmp = item_tmp.quantity
                        total_length_t = total_length
                        total_qty_t = total_qty
                        total_length += item_tmp.length*item_tmp.quantity
                        total_qty += int(item_tmp.quantity)
                        if total_length > max_length:
                            div_t = (max_length-total_length_t)//item_tmp.length
                            if div_t > 0:
                                splice_list_tmp.append((item_tmp, int(div_t)))
                            if (item_tmp.quantity - div_t) > 0:
                                item_r = copy.deepcopy(item_tmp)
                                item_r.quantity = int(item_tmp.quantity - div_t)
                                items.insert(0, item_r)
                            # 拼接MULTI
                            new_items_t, new_parts_t = splice_qty_multi(splice_list_tmp, parts)
                            new_items.append(new_items_t)
                            new_parts.append(new_parts_t)
                            return splice_in_short(items, parts, new_items, new_parts, unable_splice)
                        else:
                            splice_list_tmp.append((item_tmp, int(qty_tmp)))
                    else:
                        break
                        # unable_splice.append(one_item)
                        # return splice_in_short(items, parts, new_items, new_parts, unable_splice)
                # 拼接MULTI
                new_items_t, new_parts_t = splice_qty_multi(splice_list_tmp, parts)
                new_items.append(new_items_t)
                new_parts.append(new_parts_t)
                # print('和下个拼接,还未完成!', splice_list_tmp)
                return splice_in_short(items, parts, new_items, new_parts, unable_splice)
        else:
            new_item, new_part = splice_qty(one_item, int(div), parts)
            new_item.quantity = int(count)
            new_items.append(new_item)
            new_parts.append(new_part)
            rest = int(one_item.quantity - div * count)
            if rest > 0:
                one_item.quantity = rest
                items.insert(0, one_item)

            return splice_in_short(items, parts, new_items, new_parts, unable_splice)


def splice_qty_multi(item_qty_list, parts):
    # list of (item, qty)
    new_item = copy.deepcopy(item_qty_list[0][0])
    new_part = Parts()
    new_item_id = ''
    new_item_length = 0
    new_part_list = []
    for item, qty in item_qty_list:
        new_item_t, new_part_t = splice_qty(item, qty, parts)
        new_item_id = new_item_id + ',' + new_item_t.item_id
        # new_item_length = new_item_length + new_item_t.length
        new_item_length = new_item_t.length
        new_part_list.append((new_part_t, new_item_length))
    new_item.quantity = 1
    new_item.length = new_item_length
    if len(new_item_id) > 20:
        new_item.item_id = new_item_id[1:20]
        new_item.items_user1 = new_item_id
    else:
        new_item.item_id = new_item_id[1:]
    # TODO: splice new part list
    length = 0
    for i in range(len(new_part_list)):
        if i == 0:
            new_part = new_part_list[0][0]
            length = new_part_list[0][1]
        else:
            new_part_t = new_part_list[i][0]
            new_part = splice_parts(new_part, new_part_t, new_item.item_id, length)
            length = length + new_part_list[i][1]
            # length = new_part_list[i][1]
    new_item.part_number = new_item.item_id
    for pattern in new_part.parts:
        pattern.part_name = new_item.part_number
    new_item.length = length
    return new_item, new_part


def splice_qty_2p(item_1, qty_1, item_2, qty_2, parts):
    tm_1 = copy.deepcopy(item_1)
    tm_2 = copy.deepcopy(item_2)
    p_1 = seek_part_by_cut_item(tm_1, parts)
    p_2 = seek_part_by_cut_item(tm_2, parts)
    if qty_1 == 1:
        new_item_1 = tm_1
        new_item_1.quantity = 1
        new_part_1 = p_1
    else:
        new_item_1, new_part_1 = splice_qty(tm_1, qty_1, parts)
    if qty_2 == 1:
        new_item_2 = tm_2
        new_item_2.quantity = 2
        new_part_2 = p_2
    else:
        new_item_2, new_part_2 = splice_qty(tm_2, qty_2, parts)
    new_item = copy.deepcopy(new_item_1)
    new_item.item_id = new_item_1.item_id + ',' + new_item_2.item_id
    new_item.length = new_item_1.length + new_item_2.length
    new_item.part_name = new_item.item_id
    new_part = splice_parts(p_1, p_2, new_item.item_id, new_item.length)
    return new_item, new_part


def splice_qty(item, qty, parts):
    new_item = copy.deepcopy(item)
    new_item.item_id = new_item.item_id + '*' + str(int(qty))
    new_item.part_number = new_item.item_id
    new_item.quantity = 1
    new_item.length = new_item.length * qty
    part = seek_part_by_cut_item(item, parts)
    new_part = copy.deepcopy(part)
    for i in range(1, qty):
        new_part = splice_parts(part, new_part, new_item.item_id, item.length)
    return new_item, new_part


def core_calculate_for_half_cut(raw_group, parts):
    half_cut_long = []  # 长件 >=1500
    half_cut_short = []  # 短件

    new_parts_r = []
    new_items_r = []
    unable_splice_r = []

    # 按长度分
    for cut_item in raw_group:
        if cut_item.length >= 1500 / MM_INCH:
            half_cut_long.append(cut_item)
        else:
            half_cut_short.append(cut_item)
    # 处理拼接
    if not half_cut_short:
        # 如果没有短件
        new_items_r = half_cut_long
        new_parts_r = parts
    else:
        # 如果有短件
        if not half_cut_long:
            # 没有长件,只有短件, 无法拼接
            print('只有短件, 无法拼接')
            unable_splice_r = raw_group
            # return raw_group, parts, unable_splice
        else:
            new_parts = Parts()
            new_items = []
            new_items, new_parts, half_cut_long, half_cut_short = splice_diff_lists_qty_times(half_cut_long,
                                                                                              half_cut_short, parts,
                                                                                              new_parts, new_items)

            new_items, new_parts, half_cut_long, half_cut_short = splice_diff_lists_one_by_one(half_cut_long,
                                                                                               half_cut_short, parts,
                                                                                               new_parts, new_items)
            # new_items = half_cut_long.extend(new_items)
            half_cut_long.extend(new_items)
            new_items_r = half_cut_long
            parts.append(new_parts)
            new_parts_r = parts
            unable_splice_r = half_cut_short
    # 处理清单/parts合并, 及无法拼接的信息
    pass
    return new_items_r, new_parts_r, unable_splice_r


def splice_diff_lists_one_by_one(item_list_long, item_list_short, parts, new_parts, new_items):
    half_cut_long, half_cut_short, parts, new_parts, new_items = splice_diff_lists_one_by_one_iter(item_list_long,
                                                                                                   item_list_short,
                                                                                                   parts,
                                                                                                   new_parts, new_items)

    return new_items, new_parts, half_cut_long, half_cut_short


def splice_diff_lists_one_by_one_iter(item_list_long, item_list_short, parts, new_parts, new_items):
    if not item_list_long:
        return item_list_long, item_list_short, parts, new_parts, new_items
    if not item_list_short:
        return item_list_long, item_list_short, parts, new_parts, new_items

    tmp_long = item_list_long.pop(-1)
    tmp_short = item_list_short.pop(0)
    # if tmp_long.item_id == '5QSL-39':
    #     print('debug')
    div = (SPLICE_LENGTH - tmp_long.length) // tmp_short.length
    if tmp_short.quantity <= div:
        if tmp_short.quantity < MAX_SPLICE_QTY:
            qty_short = tmp_short.quantity
        else:
            qty_short = MAX_SPLICE_QTY-1
    else:
        if div <= 0:
            qty_short = 0
            item_list_short.insert(1, tmp_short)
            item_list_long.append(tmp_long)
            return splice_diff_lists_one_by_one_iter(item_list_long, item_list_short, parts, new_parts, new_items)
        elif div < MAX_SPLICE_QTY:
            qty_short = int(div)
        else:
            qty_short = MAX_SPLICE_QTY - 1

    # 拼接
    tmp_item, tmp_part = splice(tmp_long, tmp_short, qty_short, parts)
    # 计算拼接的数量
    div_p, mod_p = divmod(tmp_short.quantity, qty_short)
    if tmp_long.quantity <= div_p:
        div_t = tmp_long.quantity
    else:
        div_t = div_p
    tmp_long.quantity -= div_t
    tmp_short.quantity -= qty_short * div_t
    tmp_item.quantity = div_t
    if tmp_long.quantity == 0:
        if tmp_short.quantity == 0:
            # 当前长短都匹配好
            new_items.append(tmp_item)
            new_parts.append(tmp_part)
            return splice_diff_lists_one_by_one_iter(item_list_long, item_list_short, parts, new_parts, new_items)
        else:
            # 当前短件剩余
            new_items.append(tmp_item)
            new_parts.append(tmp_part)
            item_list_short.insert(0, tmp_short)
            return splice_diff_lists_one_by_one_iter(item_list_long, item_list_short, parts, new_parts, new_items)

    else:  # 当前长件剩余
        if tmp_short.quantity == 0:
            # 当前短件匹配好
            new_items.append(tmp_item)
            new_parts.append(tmp_part)
            item_list_long.append(tmp_long)
            return splice_diff_lists_one_by_one_iter(item_list_long, item_list_short, parts, new_parts, new_items)
        else:  # 当前短件剩余
            new_items.append(tmp_item)
            new_parts.append(tmp_part)
            item_list_long.append(tmp_long)
            item_list_short.insert(0, tmp_short)
            return splice_diff_lists_one_by_one_iter(item_list_long, item_list_short, parts, new_parts, new_items)


def splice(long_item, short_item, short_qty, parts):
    new_item = ''
    new_part = ''
    if short_qty == 1:
        part1 = seek_part_by_cut_item(long_item, parts)
        part2 = seek_part_by_cut_item(short_item, parts)
        name = long_item.item_id + ',' + short_item.item_id
        part1_length = long_item.length
        new_part = splice_parts(part1, part2, name, part1_length)
        new_length = part1_length + short_item.length
        new_item = copy.deepcopy(long_item)
        new_item.item_id = name
        new_item.part_number = name
        new_item.length = new_length
    else:
        part = seek_part_by_cut_item(short_item, parts)
        name = long_item.item_id + ',' + short_item.item_id + '*' + str(short_qty)
        part_length = short_item.length
        new_part = copy.deepcopy(part)
        for qty in range(1, int(short_qty)):
            new_part = splice_parts(new_part, part, name, part_length)
            part_length += part_length
        part = seek_part_by_cut_item(long_item, parts)
        part_length = long_item.length
        new_part = splice_parts(part, new_part, name, part_length)
        new_item = copy.deepcopy(long_item)
        new_item.item_id = name
        new_item.part_number = name
        new_item.length = long_item.length + short_item.length * short_qty
    return new_item, new_part


def splice_diff_lists_qty_times(item_list_long, item_list_short, parts, new_parts, new_items):
    items_long = item_list_long
    items_short = item_list_short
    if items_long:
        if items_short:
            for index_s in range(0, len(items_short)):
                short_quantity = items_short[index_s].quantity
                for qty_times in range(1, 3):
                    reminder = short_quantity % qty_times
                    if reminder == 0:
                        for index_l in range(0, len(items_long)):
                            if short_quantity == items_long[index_l].quantity * qty_times:
                                # 如果数量相等,两个列表中:
                                # 去除相应项,加入new_items, new_parts
                                new_part = None
                                item_long_tmp = items_long.pop(index_l)
                                part_long = seek_part_by_cut_item(item_long_tmp, parts)
                                item_short_tmp = items_short.pop(index_s)
                                part_short = seek_part_by_cut_item(item_short_tmp, parts)
                                item_tmp = copy.deepcopy(item_long_tmp)
                                item_tmp.item_id = item_long_tmp.item_id + ',' + item_short_tmp.item_id + '*' + str(
                                    qty_times)
                                item_tmp.part_number = item_tmp.item_id
                                item_tmp.length = item_long_tmp.length + item_short_tmp.length * qty_times
                                if qty_times == 1:
                                    new_part = splice_parts(part_long, part_short, item_tmp.item_id, item_long_tmp.length)
                                if qty_times == 2:
                                    new_part = splice_parts(part_long, part_short, item_tmp.item_id,
                                                            item_long_tmp.length)
                                    new_part = splice_parts(new_part, part_short, item_tmp.item_id,
                                                            item_long_tmp.length + item_short_tmp.length)
                                if qty_times == 3:
                                    new_part = splice_parts(part_long, part_short, item_tmp.item_id,
                                                            item_long_tmp.length)
                                    new_part = splice_parts(new_part, part_short, item_tmp.item_id,
                                                            item_long_tmp.length + item_short_tmp.length)
                                    new_part = splice_parts(new_part, part_short, item_tmp.item_id,
                                                            item_long_tmp.length + item_short_tmp.length * 2)
                                new_items.append(item_tmp)
                                new_parts.append(new_part)
                                new_items, new_parts, items_long, items_short = splice_diff_lists_qty_times(
                                    item_list_long, item_list_short, parts, new_parts, new_items)
                                return new_items, new_parts, items_long, items_short

            return new_items, new_parts, items_long, items_short
        else:
            return new_items, new_parts, items_long, items_short
    else:
        return new_items, new_parts, items_long, items_short


def splice_in_group(cut_item_group, parts, new_parts):
    new_cut_items = []
    single_cut_items = []
    single_item = None
    for cut_item in cut_item_group:
        if cut_item.quantity == 1:
            # 只有一件
            single_cut_items.append(cut_item)
        else:
            # 件数>1件, 两两自拼, 单数加一个三拼, 添加到新items, 生成新part
            # 判断是否数量是2的倍数
            is_double = cut_item.quantity % 2
            if is_double == 0:
                # 如果能成对
                single_part = None
                new_parts_qty = int(cut_item.quantity / 2)
                for part in parts:
                    if part.part_name == cut_item.item_id:
                        single_part = part
                new_part = splice_parts(single_part, single_part, cut_item.item_id + '*2', cut_item.length)
                new_cut_item = cut_item
                new_cut_item.item_id = cut_item.item_id + '*2'
                new_cut_item.length = cut_item.length * 2
                new_cut_item.quantity = new_parts_qty
                new_cut_item.part_label = cut_item.part_label + '*2'
                new_cut_items.append(new_cut_item)
                new_parts.append(new_part)
            else:
                # 如果不成对
                # 先加个3拼
                new_parts_qty = int(cut_item.quantity / 2)
                single_part = None
                for part in parts:
                    if part.part_name == cut_item.item_id:
                        single_part = part
                new_part = splice_parts(single_part, single_part, cut_item.item_id + '*2', cut_item.length)
                new_part = splice_parts(new_part, single_part, cut_item.item_id + '*3', cut_item.length * 2)

                new_cut_item = cut_item
                new_cut_item.item_id = cut_item.item_id + '*3'
                new_cut_item.length = cut_item.length * 3
                new_cut_item.quantity = 1
                new_cut_item.part_label = cut_item.part_label + '*3'
                new_cut_items.append(new_cut_item)
                new_parts.append(new_part)

                # 再加双拼
                new_part = splice_parts(single_part, single_part, cut_item.item_id + '*2', cut_item.length)
                single_part = None
                new_parts_qty = int(cut_item.quantity / 2)
                # for part in parts:
                #     if part.part_name == cut_item.item_id:
                #         single_part = part
                # new_part = splice_parts(single_part, single_part, cut_item.item_id + '*3', cut_item.length)

                new_cut_item = cut_item
                new_cut_item.item_id = cut_item.item_id + '*2'
                new_cut_item.length = cut_item.length * 2
                new_cut_item.quantity = new_parts_qty
                new_cut_item.part_label = cut_item.part_label + '*2'
                new_cut_items.append(new_cut_item)
                new_parts.append(new_part)

    # 处理单件的
    if single_cut_items:
        if len(single_cut_items) == 1:
            single_item = single_cut_items[0]
        else:
            # 依次处理不同单件列表
            new_items, new_part_list = splice_diff_parts(single_cut_items, parts)
            new_cut_items.extend(new_items)
            new_parts.extend(new_part_list)

    return new_cut_items, new_parts, single_item


def splice_diff_parts(single_items_list, parts):
    new_items_list = []
    new_parts = []
    reminder_list = []
    reminder = len(single_items_list) / 2
    if reminder == 1:
        # 先取3 个
        part_0 = seek_part_by_cut_item(single_items_list[0], parts)
        part_1 = seek_part_by_cut_item(single_items_list[1], parts)
        part_2 = seek_part_by_cut_item(single_items_list[2], parts)
        new_item_tmp = single_items_list[0]
        new_item_tmp.item_id = single_items_list[0].item_id + single_items_list[1].item_id + single_items_list[
            2].item_id
        new_item_tmp.length = single_items_list[0].length + single_items_list[1].length + single_items_list[2].length
        new_item_tmp.part_label = single_items_list[0].part_label + single_items_list[1].item_id + single_items_list[
            2].item_id
        new_items_list.append(new_item_tmp)

        part_tmp = splice_parts(part_0, part_1, 'tmp', part_0.length)
        part_tmp = splice_parts(part_tmp, part_2, new_item_tmp.item_id, new_item_tmp.length)
        new_parts.append(part_tmp)

        reminder_list = single_items_list[3:]
    else:
        reminder_list = single_items_list

    # 剩下的两个两个处理
    if reminder_list:
        step = 2
        tmp_list = [list[i:i + step] for i in range(0, len(reminder_list), step)]
        for tmp in tmp_list:
            new_item_tmp = tmp[0]
            new_item_tmp.item_id = tmp[0].item_id + tmp[1].item_id
            new_item_tmp.length = tmp[0].length + tmp[1].length
            new_item_tmp.part_label = tmp[0].part_label + tmp[1].item_id
            new_items_list.append(new_item_tmp)

            part_tmp = splice_parts(tmp[0], tmp[1], new_item_tmp.item_id, new_item_tmp.length)
            new_parts.append(part_tmp)

    return new_items_list, new_parts


def seek_part_by_cut_item(cut_item, parts):
    single_part = None
    for parts_list in parts.parts:
        for l_parts in parts_list.parts:
            for part in l_parts.parts:
                if part.part_name == cut_item.item_id:
                    single_part = l_parts
                    return single_part
    return single_part


def splice_parts(parts1, parts2, part_name, part1_length):
    new_part = copy.deepcopy(parts1)
    tmp_part = copy.deepcopy(parts2)

    for part in new_part.parts:
        part.part_name = part_name

    part = Part(part_name=part_name, tool_number=74, x_offset=part1_length)
    new_part.parts.append(part)

    for part in tmp_part.parts:
        part.part_name = part_name
        part.x_offset = part.x_offset + part1_length
        new_part.parts.append(part)

    return new_part


def calculate_diff_num(half_cut_long, half_cut_short):
    # 计算长件及短件的数量
    qty_cut_long = 0
    qty_cut_short = 0
    if half_cut_long:
        for cut_long in half_cut_long:
            qty_cut_long += int(cut_long['Fa Qty'])
    else:
        qty_cut_long = 0

    if half_cut_short:
        for cut_short in half_cut_short:
            qty_cut_short += int(cut_short['Fa Qty'])

    # 短件与长件的差
    diff_short_long = qty_cut_short - qty_cut_long
    # 拼接零件中,是否有长件
    if half_cut_short:
        # 如果有,看长件是否太少,太少的话,长件/短件内部拼接, 从普通件中再加
        if diff_short_long > 0:
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
    cut_list_sorted_bundle = sorted(cut_list_sorted_length, key=itemgetter('Bundle'))
    cut_list_sorted = sorted(cut_list_sorted_bundle, key=itemgetter('Raw Material'))

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
                           action=action, part_label='^N1^' + part_number)
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
            crash_parts.append(part)
    return crash_parts


def get_dtr_single_tool_id(tool_list, dia, loc):
    """
    获取单孔工具号
    :param loc:
    :param tool_list:单孔工具号列表
    :param dia: 孔径
    :return: 返回工具号，未定义的返回-1
    """
    for tool in tool_list:
        if tool['Dia'] == dia:
            if tool['Loc'] == loc:
                return tool['ToolID']
    return -1


def get_dtr_tools_single(file_with_path):
    csv_f = zCSV.CsvFile(file_with_path)
    tool_list = csv_f.get_single_tool_id()
    # print(tool_list)
    return tool_list


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


def check_dtr_undefined_holes_single(parts, tool_list_single):
    no_pattern_list = []
    for part in parts:
        single_list = part.check_tool_id_single(tool_list_single)
        no_pattern_list += single_list
        no_pattern_list = [dict(t) for t in {tuple(d.items()) for d in no_pattern_list}]  # 字典列表去重
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
    undefined_holes_list = []
    part_list = Parts()
    for part in parts:
        # part.sort_holes()
        # part.group_holes_by_y()
        # part.convert_to_dtr_holes()
        # double_list = part.convert_to_dtr_holes(tool_list)
        pattern, undefined_holes = part.convert_to_dtr_pattern(tool_list)
        part_list.append(pattern)
        if undefined_holes:
            undefined_holes_list.append(undefined_holes)

    return part_list, undefined_holes_list


def gen_dtr_pattern_list_crash(parts, tool_list):
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
        pattern, undefined_holes = part.convert_to_dtr_pattern_crash(tool_list)
        part_list.append(pattern)
    return part_list, undefined_holes


def lysaght_csv_from_oracle_to_dtr(cut_list, parts):
    """
    转换lysaght-csv项目到DTR列表
    :param cut_list: Oracle清单
    :param parts: lysaght-csv零件
    :return: DTR切割清单，DTR未定义孔， DTR-pattern清单
    """
    # global new_cut_list
    tool_list = get_dtr_tools('./DTRTools.csv')
    lysaght_dia_list = get_lysaght_dias('./LysaghtHoleDia.csv')
    tool_list_single = get_dtr_tools_single('./DTRSingleTools.csv')

    return_list = CutList()
    part_list = Parts()
    no_pattern_list = []
    # 判断半切清单
    # 先理出1.5m以下的list(auto_no, part_num, length, qty)
    # 相同材料，半切匹配，无法匹配的再与同材料大于1.5m的匹配，再无法匹配，列清单

    # 生成零件清单
    # 1. 转换到实际孔径，检查零件中未定义的孔
    parts_checked = prepare_lysaght_holes(parts, lysaght_dia_list)

    # 是否需要crash? False--需要, True--不需要
    if False:
        parts_crash = []
        no_pattern_list = []
    else:
        parts_crash = check_lysaght_parts_crash(parts_checked)
        no_pattern_list = check_dtr_undefined_holes_single(parts_crash, tool_list_single)
    parts_no_crash = list(set(parts_checked).difference(set(parts_crash)))
    no_pattern_list += check_dtr_undefined_holes(parts_no_crash, tool_list)
    # 检查未定义孔径
    if no_pattern_list:
        # 1.1 如果有未定义的孔
        return return_list, no_pattern_list, part_list
    else:
        # 1.2 如果没有未定义的孔
        if parts_no_crash:
            part_list_temp, undefined_holes = gen_dtr_pattern_list(parts_no_crash, tool_list)
            part_list.append(part_list_temp)
        if parts_crash:
            # part_list_temp = gen_dtr_pattern_list_crash(parts_crash, tool_list_single)
            part_list_temp, undefined_holes = gen_dtr_pattern_list_crash(parts_crash, tool_list)
            part_list.append(part_list_temp)
            undefined_holes = [
                dict(t) for t in {
                    tuple(
                        d.items()) for d in undefined_holes}]
            if undefined_holes:
                return return_list, undefined_holes, part_list
                pass

    # 生成制作清单
    if parts_crash:
        parts_crash_number = [part.part_no for part in parts_crash]
    else:
        parts_crash_number = []
    cut_list_new = []
    # 修改cut_list信息，标识crash
    for cut_item in cut_list:
        part_number = cut_item['Mark No'].strip()
        if part_number in parts_crash_number:
            cut_item['Item Cat'] = cut_item['Item Cat'].strip() + '_C'
        cut_list_new.append(cut_item)
    return_list = gen_dtr_cut_list(cut_list_new, org='LKQ')

    return return_list, no_pattern_list, part_list


def convert_nc_from_oracle_to_dtr(cut_list, nc_folder, org='LKQ'):
    """
    lysaght-nc项目转换导入DTR列表
    :param org: 组织名
    :param cut_list: lysaght-oracle获取的清单
    :param nc_folder: nc文件夹
    :return: DTR切割清单，DTR未定义孔， DTR-pattern清单
    """
    # global new_cut_list
    tool_list = get_dtr_tools('./DTRTools.csv')
    # tool_list_single = tool_list
    tool_list_single = get_dtr_tools_single('./DTRSingleTools.csv')

    lysaght_dia_list = get_lysaght_dias('./LysaghtHoleDia.csv')

    return_list = CutList()
    part_list = Parts()
    # part_list = []
    no_pattern_list = []
    part_number_list = []  # 避免零件重复

    # 生成零件清单
    if org == 'LKQ':
        # 1. 转换到实际孔径，检查零件中未定义的孔
        parts_checked = convert_nc_files_to_lysaght_parts(cut_list, nc_folder, org='LKQ')
        parts = prepare_lysaght_holes(parts_checked, lysaght_dia_list)
    else:
        parts = convert_nc_files_to_lysaght_parts(cut_list, nc_folder, org)
    # 不需要crash, True--不需要, flase -- 需要
    if False:
        parts_crash = []
    else:
        parts_crash = check_lysaght_parts_crash(parts)
        no_pattern_list = check_dtr_undefined_holes_single(parts_crash, tool_list_single)
    parts_no_crash = list(set(parts).difference(set(parts_crash)))
    no_pattern_list += check_dtr_undefined_holes(parts_no_crash, tool_list)

    if no_pattern_list:
        # 1.1 如果有未定义的孔
        return return_list, no_pattern_list, part_list
    else:
        # 1.2 如果没有未定义的孔
        if parts_no_crash:
            part_list_temp, undefined_holes_list = gen_dtr_pattern_list(parts_no_crash, tool_list)
            part_list.append(part_list_temp)
        if parts_crash:
            # part_list_temp = gen_dtr_pattern_list_crash(parts_crash, tool_list_single)
            part_list_temp, undefined_holes_list = gen_dtr_pattern_list_crash(parts_crash, tool_list)
            part_list.append(part_list_temp)
        if undefined_holes_list:
            undefined_holes_list = [
                dict(t) for t in {
                    tuple(
                        d.items()) for d in undefined_holes_list}]
        if undefined_holes_list:
            return return_list, undefined_holes_list, part_list
    # 修改part_list
    # 生成制作清单
    if parts_crash:
        parts_crash_number = [part.part_no for part in parts_crash]
    else:
        parts_crash_number = []
    cut_list_new = []
    # 修改cut_list信息，标识crash
    for cut_item in cut_list:
        if org == 'LKQ':
            part_number = cut_item['Mark No'].strip()
        else:
            part_number = cut_item['Fa Item'][0:7].strip()
        if part_number in parts_crash_number:
            cut_item['Item Cat'] = cut_item['Item Cat'].strip() + '_C'
        cut_list_new.append(cut_item)
    if org == 'LKQ':
        return_list = gen_dtr_cut_list(cut_list_new, org='LKQ')
    else:
        return_list = gen_dtr_cut_list(cut_list_new, org)

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
        part = gen_nc_part_to_lysaght(nc_inf, org)
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


def gen_butler_order_cut_list(cut_list, nc_folder, org='LKQ'):
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
                           action=action, part_label='^N1^' + part_number)
        return_list.append(cut_item)
        file_name = part_number + '.nc1'
        nc_file_path = os.path.join(nc_folder, file_name)
        if is_exist_nc(nc_file_path) and (part_number not in part_number_list):
            nc = Nc(nc_file_path)
            nc_data = nc.file_data
            nc_inf = nc.file_information()
            part = gen_nc_part_to_lysaght(nc_inf, org)
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


def gen_nc_part_to_lysaght(nc_info, org='LKQ'):
    """
    转换nc文件到lysaght-part格式
    :param org: 组织结构
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
                if org == 'SJG':
                    if nc_info.header.code_profile == 'SO':
                        if v_hole.diameter == 14:
                            v_hole.diameter = 16

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
                if org == 'SJG':
                    if nc_info.header.code_profile == 'SO':
                        if h_hole.diameter == 14:
                            h_hole.diameter = 16
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
            height = single_hole.height
            angle = single_hole.angle
            x = single_hole.x
            if (angle == 90) and (width == 0):
                single_hole.x = x + height / 2
            else:
                single_hole.x = x + width / 2
            # 花孔 6*25 长圆孔作花孔处理
            if (diameter == 6) and (width == 19):
                single_hole.diameter = 7777
            else:
                if (angle == 90) and (width == 0):
                    single_hole.diameter = diameter * 100 + (diameter + height)
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

    # 避免孔重复--单个面
    o_holes = delete_double_holes(o_holes)
    u_holes = delete_double_holes(u_holes)
    v_holes = delete_double_holes(v_holes)
    h_holes = delete_double_holes(h_holes)

    # 避免孔重复--v,h面合起来看
    h_holes = delete_repeat_holes_in_v_h(v_holes, h_holes)

    # 添加到组
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


def delete_repeat_holes_in_v_h(v_holes, h_holes):
    """
    清除v,h面内重复的孔
    :param v_holes: 原始v面孔
    :param h_holes: 原始h面孔
    :return: 新的h面的孔
    """
    # 以v面为基础,删除h面里重复的孔
    new_holes = []
    v_holes_attrs = []
    for hole in v_holes:
        v_holes_a = (hole.hole_type, hole.x, hole.y, hole.diameter)
        v_holes_attrs.append(v_holes_a)
    for hole in h_holes:
        h_holes_a = (hole.hole_type, hole.x, hole.y, hole.diameter)
        if h_holes_a not in v_holes_attrs:
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


def search_treewidgt_child(treewidgt, text):
    item = QTreeWidgetItemIterator(treewidgt)
    while item.value():
        if item.value() == text:
            item.Selected(True)
        item += 1


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
