import csv
import re


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

    def get_seq_list(self):
        try:
            with open(self.file_with_path) as f:
                f_csv = csv.DictReader(f)
                name_unit_length = f_csv
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
                    info_line = {}
                    info_line['Section'] = row['Section']
                    info_line['Width'] = row['Width']
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
                    info_line = {}
                    info_line['HoleType'] = row['HoleType']
                    info_line['HoleName'] = row['HoleName']

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
                    info_line = {}
                    info_line['Dia'] = float(row['Dia'])
                    info_line['Gauge'] = float(row['Gauge'])
                    info_line['ToolID'] = int(row['ToolID'])
                    #
                    self.seq_info.append(info_line)
                f.close()
        except Exception as e:
            print(e)
        finally:
            return self.seq_info


if __name__ == '__main__':
    csv_f = CsvFile('E:/Zanweb/Bradbury_Import_Test/in_test/BSCN.csv')
    csv_info = csv_f.get_seq_list()
    for row in csv_info:
        print(row)

    csv_z = CsvFile('../Z.csv')
    csv_z_list = csv_z.get_z_list()
    for row in csv_z_list:
        print(row)

    csv_t = CsvFile('../Tool.csv')
    csv_tools = csv_t.get_tool_id()
    for row in csv_tools:
        print(row)
