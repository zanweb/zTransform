import os
import re

bloc = ['ST',  # Beginning of piece description
        'EN',  # End of piece description
        'BO',  # bloc hole
        'SI',  # bloc numbering
        'AK',  # bloc external contour
        'IK',  # bloc internal contour
        'PU',  # bloc powder
        'KO',  # bloc mark
        'SC',  # bloc cut (Saw, Cutting)
        'TO',  # bloc Tolerance
        'UE',  # bloc Camber
        'PR',  # bloc Profile description
        'KA',  # bloc Bending
        # '**'  # Comment Line
        ]
profile = ['I',  # Profile I
           'L',  # Profile L
           'U',  # Profile U
           'B',  # Sheets, Plate, teared sheets, etc.
           'RU',  # Round
           'RO',  # Rounded Tube
           'M',  # Rectangular Tube
           'C',  # Profile C
           'T',  # Profile T
           'SO'  # Special Profile
           ]


class Header:  # bloc ST
    def __init__(self):
        self.stack = 0
        self.sequence = 0
        self.make_direction = 0
        self.order = ''  # order identification
        self.piece = 1  # piece identification
        self.drawing = ''  # drawing identification
        self.phase = ''  # phase identification
        self.quality = ''  # steel quality
        self.quantity = 1  # quantity of pieces
        self.profile = ''  # profile
        self.code_profile = ''  # code profile

        self.length = 0.0  # length, saw length
        self.profile_height = 0.0  # profile height
        self.flange_width = 0.0  # flange width
        self.flange_thickness = 0.0  # flange thickness
        self.web_thickness = 0.0  # web thickness
        self.radius = 0.0  # radius
        self.weight_by_meter = 0.0  # weight by meter
        self.painting_surface_by_meter = 0.0  # painting surface by meter
        self.web_start_cut = 0.0
        self.web_end_cut = 0.0
        self.flange_start_cut = 0.0
        self.flange_end_cut = 0.0
        self.text1 = ''  # text info on piece
        self.text2 = ''  # text info on piece
        self.text3 = ''  # text info on piece
        self.text4 = ''  # text info on piece


class Hole:  # bloc BO
    def __init__(self):
        self.plane = ''  # plane o=> top flange, v=>front web, u=>bottom flange, h=>behind web
        self.reference = ''
        # reference o => Dimension reference top edge,
        # '' => previous dimensions reference,
        # s => dimensions reference axis,
        # u => dimensions reference bottom edge
        self.hole_type = ''
        # '' => complete hole. d=diameter, t=0.0
        # g => thread, d=diameter, t=0.0
        # l => left threaded, d=diameter, t=0.0
        # m => mark, trace. d=0.0, t=0.0
        # s => counter. d=diameter, t=depth, countersink
        self.special = ''
        # l => slotted hole, rectangle.

        self.x = 0.0
        self.y = 0.0
        self.diameter = 0.0
        self.depth = 0.0
        self.width = 0.0
        self.height = 0.0
        self.angle = 0.0


class Contour:  # bloc AK IK
    def __init__(self):
        self.plane = ''
        # o => top flange
        # v => front web
        # u => bottom flange
        # h => behind web
        self.reference = ''
        # reference o => Dimension reference top edge,
        # '' => previous dimensions reference,
        # s => dimensions reference axis,
        # u => dimensions reference bottom edge
        self.tool = ''
        # t or w : tool for the notche, t => tangential, w => hereafter
        self.x = 0.0
        self.y = 0.0
        self.r = 0.0
        self.weld_angle1 = 0.0
        self.weld_y1 = 0.0
        self.weld_angle2 = 0.0
        self.weld_y2 = 0.0


class Mark:  # bloc PU KO
    def __init__(self):
        self.plane = ''
        # o => top flange
        # v => front web
        # u => bottom flange
        # h => behind web
        self.reference = ''
        # reference o => Dimension rference top edge,
        # '' => previous dimensions reference,
        # s => dimensions reference axis,
        # u => dimensions reference bottom edge
        self.x = 0.0
        self.y = 0.0
        self.r = 0.0


class Numeration:  # bloc SI
    def __init__(self):
        self.plane = ''
        # o => top flange
        # v => front web
        # u => bottom flange
        # h => behind web
        self.reference = ''
        # reference o => Dimension rference top edge,
        # '' => previous dimensions reference,
        # s => dimensions reference axis,
        # u => dimensions reference bottom edge
        self.position = ''
        # r => The Text follow the piece if turned
        # ''  => Text at the same position
        # z => Force all parameters, If one or more parameters are not done, The numeration is not done.
        self.x = 0.0
        self.y = 0.0
        self.angle = 0.0
        self.height = 0.0
        self.context = ''


class Cut:  # bloc SC
    def __init__(self):
        # specif. Pt. of the section
        self.sec_x = 0.0
        self.sec_y = 0.0
        self.sec_z = 0.0
        # data of the normal vector (from the section to outside)
        self.vect_x = 0.0
        self.vect_y = 0.0
        self.vect_z = 0.0


class Tolerance:  # bloc TO
    def __init__(self):
        self.min = 0.0
        self.max = 0.0


class Camber:  # bloc UE
    def __init__(self):
        self.plane = ''
        # o => top flange
        # v => front web
        # u => bottom flange
        # h => behind web
        self.x = 0.0
        self.y = 0.0


class Bend:  # bloc KA
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.angle = 0.0
        self.rad = 0.0


class Profile:  # bloc PR SO
    def __init__(self):
        self.signal = ''
        # + => Code for external Contour
        # - => Code for internal Contour
        self.y = 0.0
        self.z = 0.0
        self.r = 0.0


class Information:  # bloc IN
    def __init__(self):
        self.contents = ''


class GetSection:
    def get_section(self, file_info):
        pass


class GetHeader(GetSection):
    def get_section(self, file_info):
        # print('Get section ST')
        header = Header()

        header.order = file_info['ST'][0]
        header.piece = int(file_info['ST'][1])
        header.drawing = file_info['ST'][2]
        header.phase = file_info['ST'][3]
        header.quality = file_info['ST'][4]
        header.quantity = int(file_info['ST'][5])
        header.profile = file_info['ST'][6]
        header.code_profile = file_info['ST'][7]
        header.length = float(file_info['ST'][8])
        header.profile_height = float(file_info['ST'][9])
        header.flange_width = float(file_info['ST'][10])
        header.flange_thickness = float(file_info['ST'][11])
        header.web_thickness = float(file_info['ST'][12])
        header.radius = float(file_info['ST'][13])
        header.weight_by_meter = float(file_info['ST'][14])
        header.painting_surface_by_meter = float(file_info['ST'][15])
        header.web_start_cut = float(file_info['ST'][16])
        header.web_end_cut = float(file_info['ST'][17])
        header.flange_start_cut = float(file_info['ST'][18])
        header.flange_end_cut = float(file_info['ST'][19])
        header.text1 = file_info['ST'][20]
        header.text2 = file_info['ST'][21]
        header.text3 = file_info['ST'][22]
        header.text4 = file_info['ST'][23]
        return header


class GetHoles(GetSection):
    def get_section(self, file_info):
        # print('Get section BO')
        holes = []
        # single_hole = Hole()
        for hole in file_info['BO']:
            single_hole = Hole()
            single_hole_info = hole.split()
            single_hole.plane = single_hole_info[0]
            single_hole.x = float(re.findall(r"\d+\.?\d*", single_hole_info[1])[0])
            single_hole.reference = single_hole_info[1][-1]
            single_hole.y = float(re.findall(r"\d+\.?\d*", single_hole_info[2])[0])
            single_hole.diameter = float(re.findall(r"\d+\.?\d*", single_hole_info[3])[0])
            single_hole.hole_type = single_hole_info[2][-1] if str(single_hole_info[2][-1]).isalpha() else ''
            if len(single_hole_info) > 4:
                single_hole.depth = float(re.findall(r"\d+\.?\d*", single_hole_info[4])[0])
                single_hole.special = single_hole_info[4][-1]
                single_hole.width = float(re.findall(r"\d+\.?\d*", single_hole_info[5])[0])
                single_hole.height = float(re.findall(r"\d+\.?\d*", single_hole_info[6])[0])
                single_hole.angle = float(re.findall(r"\d+\.?\d*", single_hole_info[7])[0])
            holes.append(single_hole)
        # print(file_info)
        # print(holes)
        return holes


class GetExternalContour(GetSection):
    def get_section(self, file_info):
        aks = []
        # print(file_info['AK'])
        for ak in file_info['AK']:
            single_ak = Contour()
            single_ak_info = ak.split()
            if len(single_ak_info) > 7:
                single_ak.plane = single_ak_info[0]
                pre_plane = single_ak_info[0]
                single_ak.x = float(re.findall(r"\d+.?\d*", single_ak_info[1])[0])
                single_ak.reference = single_ak_info[1][-1]
                pre_reference = single_ak_info[1][-1]
                single_ak.y = float(re.findall(r"\d+.?\d*", single_ak_info[2])[0])
            else:
                single_ak.plane = pre_plane
                single_ak.reference = pre_reference
                single_ak.x = float(re.findall(r"\d+.?\d*", single_ak_info[0])[0])
                single_ak.y = float(re.findall(r"\d+.?\d*", single_ak_info[1])[0])
            aks.append(single_ak)
        return aks


class SectionUndef(GetSection):
    def get_section(self, file_info):
        print('Un_define Section.')
        return 0


class SectionFactory:
    section = {}
    section["ST"] = GetHeader()
    section["BO"] = GetHoles()
    section["AK"] = GetExternalContour()

    def create_section(self, cs):
        if cs in self.section:
            sec = self.section[cs]
        else:
            sec = SectionUndef()
        return sec


class Nc:  # nc file
    def __init__(self, file_with_path):
        self.file_with_path = file_with_path
        self.header = Header()
        self.holes = []
        self.mark = Mark
        self.ak = []
        self.file_info = {}

    # def __init__(self):
    #     self.header = Header()

    @property
    def file_data(self):
        file = open(self.file_with_path, 'r', encoding='gb2312')
        file_lines = []
        bloc_list = []

        bloc_name = ''
        for line in file:
            if line.strip() in bloc:
                if bloc_list:
                    if bloc_name in self.file_info.keys():
                        self.file_info[bloc_name].extend(bloc_list)
                    else:
                        self.file_info[bloc_name] = bloc_list
                bloc_name = line.strip()
                bloc_list = []
                continue
            if str(line.strip()).find('**') == -1:
                bloc_list.append(line.strip())
        file.close()
        # print(self.file_info)
        return self.file_info

    def file_information(self):
        info = None
        # print(self.file_info)
        for key in self.file_info:
            factory = SectionFactory()
            read_sec = factory.create_section(key)
            info = read_sec.get_section(self.file_info)
            if isinstance(info, Header):
                self.header = info
            if isinstance(info, list):
                if isinstance(info[0], Hole):
                    self.holes = info
                if isinstance(info[0], Contour):
                    self.ak = info
            # print(info)
        return self


def is_exist_nc(file_with_path):
    # os.path.isfile('test.txt')  # 如果不存在就返回False
    is_exist = os.path.exists(file_with_path)  # 如果目录不存在就返回False
    return is_exist


def has_hole_nc(file_with_path):
    bloc = ['ST',  # Beginning of piece description
            'EN',  # End of piece description
            'BO',  # bloc hole
            'SI',  # bloc numbering
            'AK',  # bloc external contour
            'IK',  # bloc internal contour
            'PU',  # bloc powder
            'K0',  # bloc mark
            'SC',  # bloc cut (Saw, Cutting)
            'TO',  # bloc Tolerance
            'UE',  # bloc Camber
            'PR',  # bloc Profile description
            'KA',  # bloc Bending
            # '**'  # Comment Line
            ]
    dia = []
    # dic_a = {}
    nc_file = open(file_with_path, 'r')
    is_bo = False
    has_hole = False
    for line in nc_file:
        if line.strip() in bloc:
            is_bloc = True
            bloc_name = line.strip()
            if bloc_name == 'BO':
                is_bo = True
                has_hole = True
            else:
                is_bo = False
            if bloc_name == 'EN':
                if has_hole:
                    dic_a = dict((float(a), dia.count(a)) for a in dia)
                    nc_file.close()
                    return dic_a
                else:
                    nc_file.close()
                    return has_hole
        else:
            if is_bo:
                bo = line.split()
                # print(bo)
                dia.append(bo[3])

    # print(dia)
    # dic_a = dict((a, dia.count(a)) for a in dia)
    # print(dic_a)


if __name__ == '__main__':
    from pprint import pprint
    from LysaghtPurlin.TransformFunctions import gen_nc_part_to_lysaght, check_patterns, get_dtr_tools

    # file_with_path = "E:/Zanweb/BMM test file/爱仕达11#NC文件/" + "L125.nc1"
    file_with_path = "E:\Desktop\易商2号库檩条测试梅花孔\\2-MM601.nc1"
    if is_exist_nc(file_with_path):
        print('OK')
        nc = Nc(file_with_path)
        nc_data = nc.file_data
        nc_info = nc.file_information()
        print(nc_info.header.code_profile, '-- profile_high --> ', re.findall(r'\d+\.?\d*', nc_info.header.profile)[0],
              ' -- flange_width--> ', nc_info.header.flange_width, ' -- thickness -->',
              re.findall(r'\d+\.?\d*', nc_info.header.profile)[1])
        pprint(nc_info.holes[0].plane)
        for hole in nc_info.holes:
            print(hole, hole.plane, hole.reference, hole.x, hole.y, hole.diameter, hole.special, hole.width)
        # holes = get_nc_plane_holes(nc_info.holes)
        # for hole_plan in holes:
        #     for hole in hole_plan:
        #         print(hole.x, hole.y, hole.diameter)

        mm_inch = 25.4
        tool_list = get_dtr_tools('./DTRTools.csv')

        no_pattern_list = []

        part = gen_nc_part_to_lysaght(nc_info)
        for part_hole in part.holes:
            print(part_hole)
        part.special_change()
        part.sort_holes()
        part.group_holes_by_y()
        double_list = part.convert_to_dtr_holes(tool_list)
        no_pattern_list += double_list
        no_pattern_list = check_patterns(
            tool_list, part.dtr_holes, no_pattern_list)
        no_pattern_list = [
            dict(t) for t in {
                tuple(
                    d.items()) for d in no_pattern_list}]  # 字典列表去重
        print(no_pattern_list)

    else:
        print('No')
