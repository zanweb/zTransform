import csv
import re

# from LysaghtPurlin.Part import Hole, Part
from LysaghtPurlin import Part


class CsvFile:
    def __init__(self, file_with_path):
        self.file_with_path = file_with_path
        self.seq_info = []

    def del_lines_begin(self, to_be_deleted):
        data = open(self.file_with_path, 'rt').readlines()
        if data[0].find('BSCN Batch Production Data for Cladding Report') != -1:
            with open(self.file_with_path, 'wt') as handle:
                # handle.writelines(data[:to_be_deleted])
                handle.writelines(data[to_be_deleted + 1:])
                # handle.readline(0)
                handle.close()

    def get_oracle_data(self):
        try:
            with open(self.file_with_path) as f:
                f_csv = csv.DictReader(f)
                for row in f_csv:
                    info_line = {}
                    if str(row['Sort Complete']).strip(' ') != 'Y':
                        info_line['ORG'] = row['ORG'].strip(' ')
                        info_line['Order Num'] = int(row['Order Num'])
                        info_line['Item Cat'] = row['Item Cat'].strip(' ')
                        info_line['Batch Id'] = int(row['Batch Id'])
                        info_line['Sort Id'] = int(row['Sort Id'])
                        info_line['Seq'] = int(row['Seq'])
                        info_line['Dept'] = row['Dept'].strip(' ')
                        info_line['Res'] = row['Res'].strip(' ')
                        info_line['Res Desc'] = row['Res Desc'].strip(' ')
                        info_line['Raw Material'] = row['Raw Material'].strip(' ')
                        if row['Coil Width']:
                            info_line['Coil Width'] = int(row['Coil Width'])
                        else:
                            info_line['Coil Width'] = row['Coil Width'].strip(' ')
                        info_line['Coil Color'] = row['Coil Color'].strip(' ')
                        info_line['Sort Complete'] = row['Sort Complete'].strip(' ')
                        info_line['Fa Job'] = row['Fa Job'].strip(' ')
                        info_line['Fa Item'] = row['Fa Item'].strip(' ')
                        info_line['Item Desc'] = row['Item Desc'].strip(' ')
                        info_line['Mark No'] = row['Mark No'].strip(' ')
                        if row['Prd Width']:
                            info_line['Prd Width'] = int(row['Prd Width'])
                        else:
                            info_line['Prd Width'] = row['Prd Width'].strip(' ')
                        if row['Stack']:
                            info_line['Stack'] = int(row['Stack'])
                        else:
                            info_line['Stack'] = row['Stack'].strip(' ')
                        if row['Fa Seq']:
                            info_line['Fa Seq'] = int(row['Fa Seq'])
                        else:
                            info_line['Fa Seq'] = row['Fa Seq'].strip(' ')
                        if row['Line Seq']:
                            info_line['Line Seq'] = int(row['Line Seq'])
                        else:
                            info_line['Line Seq'] = row['Line Seq'].strip(' ')
                        info_line['Fa Qty'] = int(row['Fa Qty'])
                        info_line['Bundle'] = row['Bundle'].strip(' ')
                        info_line['Unit Length'] = int(row['Unit Length'])
                        self.seq_info.append(info_line)
                f.close()
        except Exception as e:
            print(e)
        finally:
            return self.seq_info

    def get_seq_list(self):
        try:
            with open(self.file_with_path) as f:
                f_csv = csv.DictReader(f)
                for row in f_csv:
                    info_line = {}
                    print(row)
                    if str(row['Sort Complete']).strip(' ') != 'Y':
                        info_line['Unit Length'] = row['Unit Length']
                        info_line['Qty'] = row['Fa Qty']
                        info_line['Item'] = str(row['Fa Item']).split('*')[0][:7]
                        info_line['So'] = row['Order Num']
                        info_line['Sorts'] = row['Sort Id']
                        if not re.findall(r'\d+\.\d+', str(row['Item Desc'])):
                            info_line['Thk'] = 0
                        else:
                            info_line['Thk'] = re.findall(r'\d+\.\d+', str(row['Item Desc']))[0]
                            # str(row['Item Desc'])[:5]
                        if row['Mark No']:
                            info_line['Mark No'] = row['Mark No']
                        if row['ORG']:
                            info_line['ORG'] = row['ORG']
                        info_line['Catalog'] = row['Item Cat']
                        info_line['Batch'] = row['Batch Id']
                        info_line['Sequence'] = row['Seq']
                        info_line['Department'] = row['Dept']
                        info_line['Reshape'] = row['Res']
                        info_line['Reshape Description'] = row['Res Desc']
                        info_line['Raw Material'] = row['Raw Material']
                        info_line['Coil Width'] = row['Coil Width']
                        if row['Coil Color']:
                            info_line['Coil Color'] = row['Coil Color']
                        info_line['Job'] = row['Fa Job']
                        info_line['Product Width'] = row['Prd Width']
                        info_line['Stack'] = row['Stack']
                        info_line['Factory Sequence'] = row['Fa Seq']
                        info_line['Line Sequence'] = row['Line Seq']

                        info_line['Bundle'] = re.findall(r'\d+', str(row['Bundle']))[0]

                        print(info_line['Item'])
                        self.seq_info.append(info_line)
                f.close()
        except Exception as e:
            print(e)
        finally:
            return self.seq_info

    def get_z_list(self):
        try:
            with open(self.file_with_path) as f:
                f_csv = csv.DictReader(f)

                for row in f_csv:
                    info_line = {'Section': row['Section'], 'Width': row['Width']}
                    # info_line['Depth'] = row['Depth']
                    # info_line['THK'] = row['THK']
                    # info_line['Flange Width'] = row['Flange Width']
                    # info_line['Leg'] = row['Leg']
                    #
                    self.seq_info.append(info_line)
                f.close()
        except Exception as e:
            print(e)
        finally:
            return self.seq_info

    def get_hole_name(self):
        try:
            with open(self.file_with_path) as f:
                f_csv = csv.DictReader(f)

                for row in f_csv:
                    info_line = {'HoleType': row['HoleType'], 'HoleName': row['HoleName']}

                    #
                    self.seq_info.append(info_line)
                f.close()
        except Exception as e:
            print(e)
        finally:
            return self.seq_info

    def get_tool_id(self):
        try:
            with open(self.file_with_path) as f:
                f_csv = csv.DictReader(f)

                for row in f_csv:
                    info_line = {'Dia': float(row['Dia']), 'Gauge': float(row['Gauge']), 'ToolID': int(row['ToolID']),
                                 'Diff': float(row['Diff'])}
                    #
                    self.seq_info.append(info_line)
                f.close()
        except Exception as e:
            print(e)
        finally:
            return self.seq_info

    def get_single_tool_id(self):
        try:
            with open(self.file_with_path) as f:
                f_csv = csv.DictReader(f)

                for row in f_csv:
                    info_line = {'Dia': float(row['Dia']), 'ToolID': int(row['ToolID'])}
                    #
                    self.seq_info.append(info_line)
                f.close()
        except Exception as e:
            print(e)
        finally:
            return self.seq_info

    def get_lysaght_dia_no(self):
        try:
            with open(self.file_with_path) as f:
                f_csv = csv.DictReader(f)
                for row in f_csv:
                    info_line = {'DiaNo': float(row['DiaNo']), 'Dia': float(row['Dia'])}
                    self.seq_info.append(info_line)
                f.close()
        except Exception as e:
            print(e)
        finally:
            return self.seq_info

    def get_lysaght_punch(self):
        try:
            with open(self.file_with_path) as f:
                lines = f.readlines()
                parts = []
                for line in lines:
                    item = line.replace('\r', '').replace('\n', '').replace('\t', '')
                    if item[-1] == ',':
                        item = item[0:-2]
                    item = item.split(',')
                    if len(item) % 5 != 0:
                        raise NameError('数据格式不对')
                    size = str(item[0]).split('*')
                    thick = float(size[len(size) - 1])
                    part = Part.Part(part_no=str(item[1]).upper(), part_length=int(item[2]), part_thickness=thick,
                                     quantity=int(item[3]),
                                     section=str(item[0]), material='')
                    if len(item) > 5:
                        for i in range(1, len(item) // 5):
                            if item[i * 5] == 'Hole':
                                hole = Part.Hole(location=item[1 * 5 + 1], x=float(item[i * 5 + 3]),
                                                 y=float(item[i * 5 + 4]),
                                                 dia=float(item[i * 5 + 2]))
                                part.add_hole(hole)
                    parts.append(part)
                f.close()
            self.seq_info = parts
        except NameError:
            print(item[1] + ': 请检查数据格式的长度！')
        except Exception as e:
            print(e)
        finally:
            return self.seq_info

    def get_lysaght_bundle_cz_info(self):
        try:
            with open(self.file_with_path) as f:
                lines = f.readlines()
                item = lines[0].split(',')

                self.seq_info = [int(item[4]), item[0][0]]

        except NameError:
            print('请检查数据文件是否正确！')
        except Exception as e:
            print(e)
        finally:
            f.close()
            return self.seq_info

    def write_slitting_list(self, dict_list):
        try:
            with open(self.file_with_path, 'w', newline='') as f:
                csv_write = csv.writer(f)
                for dic in dict_list:
                    if dic:
                        csv_write.writerow([dic['Item'], dic['Fa Qty'], dic['Prd Width'], dic['Unit Length']])
                f.close()

                return True
        except NameError:
            print('请检查数据文件是否正确！')
            return False
        except Exception as e:
            print(e)
            return False
        finally:
            f.close()


if __name__ == '__main__':
    # csv_f = CsvFile('E:/Zanweb/Bradbury_Import_Test/in_test/BSCN.csv')
    # csv_info = csv_f.get_seq_list()
    # for row in csv_info:
    #     print(row)
    #
    # csv_z = CsvFile('../Z.csv')
    # csv_z_list = csv_z.get_z_list()
    # for row in csv_z_list:
    #     print(row)
    #
    # csv_t = CsvFile('../DTRTools.csv')
    # csv_tools = csv_t.get_tool_id()
    # for row in csv_tools:
    #     print(row)
    # csv_p = CsvFile('../testfiles/punch.csv')
    # csv_part = csv_p.get_lysaght_punch()
    # print(csv_part)
    # for item_line in csv_part:
    #     print(item_line.part_no)

    csv_f = CsvFile('E:/Desktop/NC文件/1816474.csv')
    csv_info = csv_f.get_seq_list()
    for row in csv_info:
        print(row)
