import pprint


class Head:
    def __init__(self):
        self.make_direction = 0
        self.sequence = -1  # the sequence in pch file ( 3 character)
        self.part_number = ''  #
        self.order_number = ''  # "000," + order_number(17 character) + "_a,"
        self.parent_mark = ''  # 10 character
        self.part_mark = ''  # part_mark(sub 2 character) + sequence ( 3 character)
        self.quantity = 0  # quantity (4 character)
        self.thickness = 0.0  # thickness (keep 4 after decimal point, 2 before)
        self.width = 0.0  # width (keep 1 after decimal point, 3 before)
        self.length = 0  # length (total 7 character include decimal point)
        self.user1 = ''  # user1 (5 character)


class Hole:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.diameter = 0.0
        self.type = ''
        # type as follows:
        # 'HE' -- line designation for a single hole
        # 'HA' -- line designation for a pair of holes usually 9/16"
        # 'HC' -- line designation for a pair of holes usually 13/16"
        # 'MI' -- ink mark inside
        # 'MO' -- ink mark outside


class Pch:
    def __init__(self):
        self.header = Head()
        self.holes = []
        self.write_file_lines = []
        self.hole_number = 0

    def trans_from_nc(self, nc_info):
        self.header.make_direction = nc_info.header.make_direction
        self.header.sequence = nc_info.header.sequence  # need change
        self.header.part_number = 0
        self.header.order_number = nc_info.header.order
        self.header.parent_mark = ''
        self.header.part_mark = nc_info.header.drawing
        self.header.quantity = nc_info.header.quantity
        self.header.thickness = nc_info.header.flange_thickness
        self.header.width = nc_info.header.flange_width
        self.header.length = nc_info.header.length

        self.hole_number = len(nc_info.holes)
        if self.hole_number > 0:
            for single_hole in nc_info.holes:
                hole = Hole()
                if single_hole.hole_type == '':
                    hole.x = single_hole.x
                    hole.y = single_hole.y
                    hole.diameter = single_hole.diameter
                    hole.type = 'HE'
                    self.holes.append(hole)

    def write_prepare(self):
        head_info = ''
        head_info += ('%3d' % self.header.sequence) + ','
        # head_info += '%03d' % str(self.header.part_number) + ','
        head_info += '000,' + self.header.order_number[0:16].rjust(17) + '_a,'
        head_info += self.header.parent_mark.rjust(10) + ','
        head_info += self.header.part_mark[0:2] + str(self.header.sequence).rjust(3) + ','
        head_info += str(self.header.quantity).rjust(4) + ','
        head_info += str(self.header.thickness).ljust(7, '0') + ','
        head_info += str(self.header.width).ljust(4, '0') + ','
        head_info += ('%.0f' % self.header.length).rjust(7) + ','
        head_info += self.header.user1.rjust(5) + ','

        self.write_file_lines.append(head_info)
        if self.header.make_direction == 1:  # revise
            for single_hole in self.holes:
                single_hole.x = self.header.length - single_hole.x

        for each_hole in self.holes:
            hole_line = each_hole.type + ','
            hole_line += ('%.4f' % each_hole.x).rjust(11) + ','
            hole_line += ('%.4f' % each_hole.y).rjust(11) + ','
            hole_line += ('%.4f' % each_hole.diameter).rjust(11) + ','
            self.write_file_lines.append(hole_line)

        part_end = '                                                    @'
        self.write_file_lines.append(part_end)

        # pprint.pprint(self.write_file_lines)
        return self.write_file_lines

    def save_file(self, file_with_path):
        file = open(file_with_path, 'w')
        self.write_file_lines = ((line + '\n') for line in self.write_file_lines)
        file.writelines(self.write_file_lines)
        file.close()
        print('save_file:' + file_with_path)