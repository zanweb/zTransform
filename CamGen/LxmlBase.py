from itertools import groupby
from operator import attrgetter

from PyQt5.QtWidgets import QMessageBox
from lxml import etree
from LysaghtPurlin.TransformFunctions import nc_file_header_profile


class Head:
    def __init__(self):
        self.make_direction = 0
        self.order = ''
        self.part_name = ''
        self.length = 0.0
        self.width = 0.0
        self.thickness = 0.0
        self.quantity = 0


class Hole:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0  # not needed

        self.type = ''  # F8D F14D F16O W16D W16O KHSX4


class XmlGen:
    def __init__(self, xml_name):
        self.xml_name = xml_name
        self.header = Head()
        self.holes = []
        self.web_hole_D = 'W16D'
        self.web_hole_O = 'W16O'
        self.web_hole_khsx4 = 'KHSX4'
        self.flange_hole_top_14 = 'F14D'
        self.flange_hole_top_8 = 'F8D'
        self.flange_hole_bottom_16 = 'F16O'
        self.up_to_down = True
        # o-plane no holes or has 8 diameter holes---False, o-plane on drive side
        # o-plane only 14 diameter holes -- True, o-plane on operate side

        self.undefined_holes = []

    def set_hole_name(self, hole_name):
        for hole in hole_name:
            if hole['HoleType'] == 'TopFlange_14':
                self.flange_hole_top_14 = hole['HoleName']
            if hole['HoleType'] == 'BottomFlange_16':
                self.flange_hole_bottom_16 = hole['HoleName']
            if hole['HoleType'] == 'WebNearTop_16':
                self.web_hole_D = hole['HoleName']
            if hole['HoleType'] == 'WebNearBottom_16':
                self.web_hole_O = hole['HoleName']
            if hole['HoleType'] == 'Web_4KeyHoleSlots':
                self.web_hole_khsx4 = hole['HoleName']
            if hole['HoleType'] == 'TopFlange_8':
                self.flange_hole_top_8 = hole['HoleName']
            # print(self.flange_hole_top_14)

    def up_or_down(self, holes, profile_high):
        # 80 在D8的一端
        # holes[0]-o, [1] - u, [2] - v, [3] - h
        o_holes = holes[0]
        u_holes = holes[1]
        v_holes = holes[2]
        h_holes = holes[3]

        vu_holes = h_holes + v_holes
        o_side = 40

        if vu_holes:
            holes_group_y = []
            for x_index, x_group in groupby(v_holes, key=attrgetter('x')):
                holes_group_y.append(list(x_group))
            for group in holes_group_y:
                if len(group) == 2:
                    max_y = max(group[0].y, group[1].y)
                    o_side = profile_high - max_y

        if not o_holes:
            self.up_to_down = False
        else:
            for single_hole in o_holes:
                if single_hole.diameter == 8:
                    self.up_to_down = False
                    break

                if single_hole.diameter == 14:
                    if o_side > 40:
                        self.up_to_down = False
                        break

    def add_top_side_holes(self, holes):
        for single_hole in holes:
            if single_hole.diameter == 14:
                hole = Hole()
                hole.x = single_hole.x
                hole.y = single_hole.y
                hole.type = self.flange_hole_top_14
                self.holes.append(hole)
            elif single_hole.diameter == 8:
                hole = Hole()
                hole.x = single_hole.x
                hole.y = single_hole.y
                hole.type = self.flange_hole_top_8
                self.holes.append(hole)
            else:
                self.undefined_holes.append(single_hole)

    def add_bottom_side_holes(self, holes):
        for single_hole in holes:
            if (single_hole.diameter == 14) or (single_hole.diameter == 16):
                hole = Hole()
                hole.x = single_hole.x
                hole.y = single_hole.y
                hole.type = self.flange_hole_bottom_16
                self.holes.append(hole)
            else:
                self.undefined_holes.append(single_hole)

    def add_web_holes_org(self, holes):
        pre_hole_x = 0.0
        pre_hole_y = 0.0
        for single_hole in holes:
            hole = Hole()
            # 腹板16孔处理 2018/11/03 加入腹板16孔径的兼容
            if (single_hole.diameter == 14) or (single_hole.diameter == 16):
                if single_hole.x == pre_hole_x:
                    continue
                hole.x = single_hole.x
                hole.y = 0.0
                hole.type = self.web_hole_D
                self.holes.append(hole)
                hole = Hole()
                hole.x = single_hole.x
                hole.y = 0.0
                hole.type = self.web_hole_O
                self.holes.append(hole)
                pre_hole_x = hole.x
            # 腹板腰圆孔处理
            elif (single_hole.diameter == 13.5) or (single_hole.special == 'l'):
                if single_hole.special == 'l':
                    # nc 中标准长圆孔处理
                    single_hole.x = single_hole.x + single_hole.width / 2
                if (single_hole.x == pre_hole_x) or (single_hole.x == (pre_hole_x + 75)):
                    continue
                hole.x = single_hole.x + 37.5
                hole.y = 0.0
                hole.type = self.web_hole_khsx4
                self.holes.append(hole)
                pre_hole_x = hole.x - 37.5
                pre_hole_y = single_hole.y
            else:
                self.undefined_holes.append(single_hole)

    def add_web_holes(self, holes):
        holes_group_y = []

        # 腹板孔按x坐标分组
        for x_index, x_group in groupby(holes, key=attrgetter('x')):
            holes_group_y.append(list(x_group))
        # 腹板孔处理
        pre_group_x = 0.0
        for group in holes_group_y:

            hole = Hole()
            # 腹板16孔处理 2018/11/03 加入腹板16孔径的兼容
            if (group[0].diameter == 14) or (group[0].diameter == 16):
                if group[0].x == pre_group_x:
                    continue
                hole.x = group[0].x
                hole.y = 0.0
                hole.type = self.web_hole_D
                self.holes.append(hole)
                hole = Hole()
                hole.x = group[0].x
                hole.y = 0.0
                hole.type = self.web_hole_O
                self.holes.append(hole)
                pre_group_x = hole.x
            # 腹板腰圆孔处理
            elif (group[0].diameter == 13.5) or (group[0].special == 'l'):
                if group[0].special == 'l':
                    # nc 中标准长圆孔处理
                    group[0].x = group[0].x  # 已经在get_plane_holes()中处理过了
                    # group[0].x = group[0].x + group[0].width / 2
                    # group[0].x = group[0].x + (group[0].diameter + group[0].width) / 2
                if (group[0].x == pre_group_x) or (abs(group[0].x - (pre_group_x + 75)) <= 1):
                    continue
                hole.x = group[0].x + 37.5
                hole.y = 0.0
                hole.type = self.web_hole_khsx4
                self.holes.append(hole)
                pre_group_x = group[0].x
            else:
                self.undefined_holes.append(group[0])

    def creat_element(self, element_name):
        return etree.Element(element_name)

    def creat_sub_element(self, sub_element_name, pre_element=None):
        return etree.SubElement(pre_element, sub_element_name)

    def set_element_attr(self, element, attr_name, attr_value):
        cur_element = element
        cur_element.set(attr_name, attr_value)

    def gen_xml(self, root):
        tree = etree.ElementTree(root)
        tree.write(self.xml_name, pretty_print=True, xml_declaration=True, encoding=u'utf-8')

    def trans_from_nc(self, nc_info):
        self.header.make_direction = nc_info.header.make_direction
        self.header.part_name = nc_info.header.drawing
        self.header.order = nc_info.header.order
        # if not nc_info.header.profile.find('*') == -1:
        #     if re.findall(r'\d+\.\d+', str(nc_info.header.profile).split('*')[1]):
        #         self.header.thickness = re.findall(r'\d+\.\d+', str(nc_info.header.profile).split('*')[1])[0]
        # if not nc_info.header.profile.find('X') == -1:
        #     if re.findall(r'\d+\.\d+', str(nc_info.header.profile).split('X')[1]):
        #         self.header.thickness = re.findall(r'\d+\.\d+', str(nc_info.header.profile).split('X')[1])[0]
        profile_height, flange_width, web_thickness = nc_file_header_profile(nc_info.header)
        self.header.thickness = web_thickness
        self.header.width = profile_height
        self.header.length = int(nc_info.header.length)
        self.header.quantity = int(nc_info.header.quantity)
        # deal with holes
        # print('deal with holes')
        plane_holes = self.get_plane_holes(nc_info.holes)
        make_direction = self.check_make_direction(nc_info.ak)
        if make_direction == -1:
            for each_plan in plane_holes:
                for each_hole in each_plan:
                    each_hole.x = self.header.length - each_hole.x

        self.up_or_down(plane_holes, profile_height)
        # print(plane_holes[2])
        if not self.up_to_down:
            self.add_top_side_holes(plane_holes[0])
            self.add_bottom_side_holes(plane_holes[1])
            self.add_web_holes(plane_holes[2])
        else:
            self.add_top_side_holes(plane_holes[1])
            self.add_bottom_side_holes(plane_holes[0])
            self.add_web_holes(plane_holes[2])

        # 判断是否有未定义的孔：
        if self.undefined_holes:
            info = ''
            for hole in self.undefined_holes:
                info += '\n' + 'Dia:' + str(hole.diameter) + ',Type:' + hole.hole_type + ',Plane:' + hole.plane
            QMessageBox.warning(None, '警告', self.header.part_name + '有未定义的孔\n' + info)
            return

    def get_plane_holes_org(self, nc_holes):
        plane_holes = []
        v_holes = []
        u_holes = []
        o_holes = []
        # h_holes = []
        for single_hole in nc_holes:
            # print(single_hole.plane)
            # print(single_hole.reference)
            # 处理NC偏差#
            single_hole.x = round(single_hole.x)
            # single_hole.y = round(single_hole.y)
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

        plane_holes.append(o_holes)
        plane_holes.append(u_holes)
        plane_holes.append(v_holes)
        # print(o_holes)
        return plane_holes

    def get_plane_holes(self, nc_holes):
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
        o_holes = self.delete_double_holes(o_holes)
        u_holes = self.delete_double_holes(u_holes)
        v_holes = self.delete_double_holes(v_holes)
        h_holes = self.delete_double_holes(h_holes)

        plane_holes.append(o_holes)
        plane_holes.append(u_holes)
        plane_holes.append(v_holes)
        plane_holes.append(h_holes)

        # print(o_holes)
        return plane_holes

    def delete_double_holes(self, holes):
        new_holes = []
        hole_attrs = []
        for hole in holes:
            hole_a = (hole.plane, hole.reference, hole.x, hole.y, hole.diameter)
            if hole_a not in hole_attrs:
                hole_attrs.append(hole_a)
                new_holes.append(hole)
        return new_holes


    def gen_tree(self):
        orders = self.creat_element('Orders')
        order = self.creat_sub_element('Order', orders)
        self.set_element_attr(order, 'OrderNumber', self.header.order)  # ===============
        job = self.creat_sub_element('Job', order)
        bundle = self.creat_sub_element('Bundle', job)
        part = self.creat_sub_element('Part', bundle)
        self.set_element_attr(part, 'Thickness', str(self.header.thickness))  # ===============
        self.set_element_attr(part, 'Width', str(self.header.width))  # ===============
        self.set_element_attr(part, 'Length', str(self.header.length))  # ===============
        self.set_element_attr(part, 'RequestedQty', str(self.header.quantity))  # ===============
        self.set_element_attr(part, 'PrintString', str(self.header.part_name))  # ===============
        # print_string = self.creat_sub_element('PrintString', part)
        # print_string.text = str(self.header.part_name)
        xml_holes = self.creat_sub_element('Holes', part)
        # print(self.holes)
        for single_hole in self.holes:
            xml_hole = self.creat_sub_element('Hole', xml_holes)
            self.set_element_attr(xml_hole, 'HoleType', single_hole.type)  # ===============
            self.set_element_attr(xml_hole, 'XOffset', str(single_hole.x))  # ===============
            self.set_element_attr(xml_hole, 'YOffset', '0')  # ===============
            self.set_element_attr(xml_hole, 'PartReference', 'Leading')
            self.set_element_attr(xml_hole, 'Station', 'TSC11')

        patterns = self.creat_sub_element('Patterns', part)

        notches = self.creat_sub_element('Notches', part)
        self.gen_xml(orders)

    def horizontal_Flip(self):
        pass

    def check_make_direction(self, nc_aks):
        # plane_aks = []
        v_aks = []
        u_aks = []
        o_aks = []
        for single_ak in nc_aks:
            if single_ak.plane == 'v':
                v_aks.append(single_ak)
            if single_ak.plane == 'u':
                u_aks.append(single_ak)
            if single_ak.plane == 'o':
                o_aks.append(single_ak)
        y_list = []
        for each_ak in v_aks:
            y_list.append(each_ak.y)
        max_y = max(y_list)
        if max_y < 30:  # Bend down of top flange
            return 0
        else:  # Bend up of top flange, horizontal flip
            return -1


# ===================================================================================


if __name__ == "__main__":
    pass
    # bb_tsc = XmlGen("bbtest.xml")

    # orders = bb_tsc.creat_element('Orders')
    # order = bb_tsc.creat_sub_element('Order', orders)
    # bb_tsc.set_element_attr(order, 'OrderNumber', "1223")  # ===============
    # job = bb_tsc.creat_sub_element('Job', order)
    # bundle = bb_tsc.creat_sub_element('Bundle', job)
    # part = bb_tsc.creat_sub_element('Part', bundle)
    #
    # bb_tsc.set_element_attr(part, 'Thickness', '1.5')  # ===============
    # bb_tsc.set_element_attr(part, 'Width', '369')  # ===============
    # bb_tsc.set_element_attr(part, 'Length', '6895')  # ===============
    # bb_tsc.set_element_attr(part, 'RequestedQty', '1')  # ===============
    # holes = bb_tsc.creat_sub_element('Holes', part)
    #
    # hole = bb_tsc.creat_sub_element('Hole', holes)
    # bb_tsc.set_element_attr(hole, 'HoleType', 'W16O')  # ===============
    # bb_tsc.set_element_attr(hole, 'XOffset', '410')  # ===============
    # bb_tsc.set_element_attr(hole, 'YOffset', '0')  # ===============
    # bb_tsc.set_element_attr(hole, 'PartReference', 'Leading')
    # bb_tsc.set_element_attr(hole, 'Station', 'TSC11')
    #
    # hole = bb_tsc.creat_sub_element('Hole', holes)
    # bb_tsc.set_element_attr(hole, 'HoleType', 'W16D')
    # bb_tsc.set_element_attr(hole, 'XOffset', '35')
    # bb_tsc.set_element_attr(hole, 'YOffset', '0')
    # bb_tsc.set_element_attr(hole, 'PartReference', 'Leading')
    # bb_tsc.set_element_attr(hole, 'Station', 'TSC11')
    #
    # patterns = bb_tsc.creat_sub_element('Patterns', part)
    #
    # # pattern01 = bb_tsc.creat_sub_element('Pattern', patterns)
    # # bb_tsc.set_element_attr(pattern01, 'EndOffset', '485')
    # # bb_tsc.set_element_attr(pattern01, 'RepeatOffset', '75')
    # # bb_tsc.set_element_attr(pattern01, 'LeadOffset', '410')
    # # bb_tsc.set_element_attr(pattern01, 'IsRepeat', 'True')
    # # bb_tsc.set_element_attr(pattern01, 'Reference', 'LeadTrail')
    # # bb_tsc.set_element_attr(pattern01, 'Name', 'W16D+W16O')
    # #
    # # pattern01 = bb_tsc.creat_sub_element('Pattern', patterns)
    # # bb_tsc.set_element_attr(pattern01, 'EndOffset', '3210')
    # # bb_tsc.set_element_attr(pattern01, 'RepeatOffset', '75')
    # # bb_tsc.set_element_attr(pattern01, 'LeadOffset', '3135')
    # # bb_tsc.set_element_attr(pattern01, 'IsRepeat', 'True')
    # # bb_tsc.set_element_attr(pattern01, 'Reference', 'LeadTrail')
    # # bb_tsc.set_element_attr(pattern01, 'Name', 'W16D+W16O')
    # #
    # # pattern01 = bb_tsc.creat_sub_element('Pattern', patterns)
    # # bb_tsc.set_element_attr(pattern01, 'EndOffset', '0')
    # # bb_tsc.set_element_attr(pattern01, 'RepeatOffset', '0')
    # # bb_tsc.set_element_attr(pattern01, 'LeadOffset', '35')
    # # bb_tsc.set_element_attr(pattern01, 'IsRepeat', 'False')
    # # bb_tsc.set_element_attr(pattern01, 'Reference', 'LeadTrail')
    # # bb_tsc.set_element_attr(pattern01, 'Name', 'W16D+W16O')
    # #
    # # pattern01 = bb_tsc.creat_sub_element('Pattern', patterns)
    # # bb_tsc.set_element_attr(pattern01, 'EndOffset', '1535')
    # # bb_tsc.set_element_attr(pattern01, 'RepeatOffset', '75')
    # # bb_tsc.set_element_attr(pattern01, 'LeadOffset', '785')
    # # bb_tsc.set_element_attr(pattern01, 'IsRepeat', 'True')
    # # bb_tsc.set_element_attr(pattern01, 'Reference', 'LeadTrail')
    # # bb_tsc.set_element_attr(pattern01, 'Name', 'W16D+W16O')
    #
    # notches = bb_tsc.creat_sub_element('Notches', part)
    # bb_tsc.gen_xml(orders)
