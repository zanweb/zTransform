import os
import pprint


class Head:
    def __init__(self):
        self.make_direction = 0
        self.part_name = ''  # Up to 40 characters; the first 8 being used as the DOS file name
        self.structural_shape = ''  # up to 15 characters
        self.shape_type = ''  # Beam = B; Angle = L; Channel = C; Plate = P; Tube = T

        self.quantity_need = 1  # quantity of parts needed
        self.depth_section = 0.0  # depth of section ( or near leg size)
        self.web_thickness = 0.0  # web thickness (near leg thickness)
        self.flange_height = 0.0  # flange height (for leg size)
        self.flange_thickness = 0.0  # flange thickness(for leg thickness)
        self.not_used = 0  # not used
        self.lead_edge_miter = 0  # lead edge miter(degrees)
        self.trail_edge_miter = 0  # trail edge miter(degrees)
        self.length_section = 0  # length of section

        self.tool1_web = 0  # tool size
        self.tool1_bottom_flange = 0
        self.tool1_top_flange = 0
        self.tool2_web = 0
        self.tool2_bottom_flange = 0
        self.tool2_top_flange = 0
        self.tool3_web = 0
        self.tool3_bottom_flange = 0
        self.tool4_top_flange = 0

        # Tool 1 - web, bottom flange, top flange)
        # tool 2 - web, bottom flange, top flange)
        # tool 3 - web, bottom flange, top flange)
        # special tool types:
        # Round:  300
        # Obround: 250X150
        # Rectangular: 250-150
        # Countersink: 120S


class Hole:
    def __init__(self):
        self.x = 0.0  # x dimension
        self.y = 0.0  # y dimension
        self.surface = 0  # surface
        self.tool = 0  # tool
        self.option = 0  # option
        self.burn = ''  # burn

        # The Surface of the material is specified by the first digit immediately to the right of the decimal point.
        # Surfaces values are defined as follows:
        # 0 = Character Marking
        # 1 = Web top side (or near leg of an angel)
        # 2 = Bottom Flange
        # 3 = Top Flange(or the far leg of an angel)
        # 4 = Web bottom side
        # 5 = Burning/coping or free form marking

        # The Tool, is specified by th next two digites to the right of the decimal.
        # The Tool number corresponds to the tool diameters specified in the file header as described above.
        # Tool 0 specifies a layout mark
        # The Option, if used, is specified by the next digit, and controls the operation as defined below:
        # for holes:
        #       0 = x location from the left end , y from the datum side
        #       1 = x location from the right end, y from the datum side
        #       2 = x location from the left end, y from the non datum side
        #       3 = x location from the right end, y from the non datum side
        # for burning or free form marking
        #       0 = x location from the left end
        #       1 = x location from the right end
        # for character marking:
        #       0 = text normal orientation (reading left to right)
        #       1 = text rotated 90 degrees(CCW)
        #       2 = text rotated 180 degrees(CCW)
        #       3 = text rotated 270 degrees(CCW)

        # The Burn type/file name is specified when the surface value is 6.
        # The burn name is to the right of the Option value
        # Burn variables, if used follow the burn type/file name string separated by commas.
        # There may be up to 5 cope variables.
        # xxxxxggggggg.stto cope, v0,v1,v2,v3,v4


class Ped:
    def __init__(self):
        self.header = Head()
        self.holes = []
        self.hole_numbers = 0
        self.hole_diameters = []
        self.write_file_lines = []

    def trans_from_nc(self, nc_info):
        # header
        self.header.make_direction = nc_info.header.make_direction
        self.header.part_name = nc_info.header.drawing
        self.header.structural_shape = ('P' +
                                        '%.0f' % (nc_info.header.flange_width * 10) + 'X' + '%.0f' % (
                                                nc_info.header.flange_thickness * 10))
        self.header.shape_type = 'P'  # Beam = B; Angle = L; Channel = C; Plate = P; Tube = T

        self.header.quantity_need = nc_info.header.piece  # quantity of parts needed

        self.header.depth_section = nc_info.header.flange_width  # depth of section ( or near leg size)
        self.header.web_thickness = nc_info.header.web_thickness  # web thickness (near leg thickness)
        self.header.flange_height = nc_info.header.flange_width  # flange height (for leg size)
        self.header.flange_thickness = nc_info.header.flange_thickness  # flange thickness(for leg thickness)
        self.header.not_used = 0  # not used
        self.header.lead_edge_miter = 0  # lead edge miter(degrees)
        self.header.trail_edge_miter = 0  # trail edge miter(degrees)
        self.header.length_section = float(nc_info.header.length)  # length of section

        self.header.tool1_web = 0  # tool size
        self.header.tool1_bottom_flange = 0
        self.header.tool1_top_flange = 0
        self.header.tool2_web = 0
        self.header.tool2_bottom_flange = 0
        self.header.tool2_top_flange = 0
        self.header.tool3_web = 0
        self.header.tool3_bottom_flange = 0
        self.header.tool3_top_flange = 0

        # holes
        self.hole_numbers = len(nc_info.holes) + 1

        if self.hole_numbers > 1:
            for single_hole in nc_info.holes:
                hole = Hole()
                if single_hole.hole_type == '':
                    hole.surface = 1   # need function
                    hole.x = single_hole.x
                    hole.y = single_hole.y
                    if single_hole.diameter not in self.holes:
                        self.hole_diameters.append(single_hole.diameter)
                    hole.tool = 1 + self.hole_diameters.index(single_hole.diameter)
                    self.holes.append(hole)

    def write_prepare(self):
        self.write_file_lines.append(str(self.header.part_name))
        self.write_file_lines.append(self.header.structural_shape)
        self.write_file_lines.append(str(self.header.shape_type))

        parameter = ' '
        parameter += '%d' % self.header.quantity_need
        parameter += '  ' + '%.0f' % (self.header.depth_section * 100)
        parameter += '  ' + '%.0f' % (self.header.web_thickness * 100)
        parameter += '  ' + '%.0f' % (self.header.flange_height * 100)
        parameter += '  ' + '%.0f' % (self.header.flange_thickness*100)
        parameter += '  ' + '%.0f' % self.header.not_used
        parameter += '  ' + '%.0f' % self.header.lead_edge_miter
        parameter += '  ' + '%.0f' % self.header.trail_edge_miter
        parameter += '  ' + '%.0f' % (self.header.length_section * 10)

        if self.hole_diameters:
            str_dia = ''
            for each_dia in self.hole_diameters:
                str_dia = ('%.0f' % (each_dia * 10) + '  0  0')
            parameter += '  ' + str(str_dia)
        else:
            parameter += ' 0 0 0 0 0 0 0 0 0'

        self.write_file_lines.append(parameter)

        if self.hole_numbers > 1:
            self.write_file_lines.append(' ' + str(self.hole_numbers))
            if self.header.make_direction == 1:  # revise
                for single_hole in self.holes:
                    single_hole.x = self.header.length_section - single_hole.x
            for each_hole in self.holes:
                hole_line = ' '
                hole_line += '%.0f' % (each_hole.x * 1000)
                hole_line += ' ' + '%.0f' % (each_hole.y * 1000)
                hole_line += '.'
                hole_line += '%d' % each_hole.surface
                hole_line += '%02d' % each_hole.tool
                hole_line += '%d' % each_hole.option
                self.write_file_lines.append(hole_line)
        else:
            self.write_file_lines.append(' 1')
        pprint.pprint(self.write_file_lines)

    def save_file(self, file_with_path):
        file = open(file_with_path, 'w')
        self.write_file_lines = ((line + '\n') for line in self.write_file_lines)
        file.writelines(self.write_file_lines)
        file.close()
        print('save_file:' + file_with_path)
