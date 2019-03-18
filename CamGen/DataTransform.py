from CamGen import FMIBase
from CamGen import LxmlBase
from CamGen import NCBase
from CamGen import PedBase
from DTRGen import TransformFunctions


def __init(self):
    self.info = None


class IReader:
    def read(self):
        pass


class NcRead(IReader):
    def __init__(self):
        pass

    def read(self, nc_file):
        nc = NCBase.Nc(nc_file)
        nc_data = nc.file_data
        nc_info = nc.file_information()
        return nc_info


class PedRead(IReader):
    def read(self):
        print('read peddinghous file')


class FMIRead(IReader):
    def read(self):
        print('read FMI file')


class IWriter:
    def write(self):
        pass


class NcWrite(IWriter):
    def write(self):
        print('Write Nc File')


class PedWrite(IWriter):
    def __init__(self):
        pass

    def write(self, nc_info, file_with_path):
        ped = PedBase.Ped()
        ped.trans_from_nc(nc_info)
        ped.write_prepare()
        ped.save_file(file_with_path)

        print('-------Write Peddinghaus File')


class FMIWrite(IWriter):
    def pre_write(self, nc_info):
        fmi_flange = FMIBase.Pch()
        fmi_flange.trans_from_nc(nc_info)
        writer_line = fmi_flange.write_prepare()
        return writer_line

    def write(self, nc_info, file_with_path):
        fmi_flange = FMIBase.Pch()
        fmi_flange.trans_from_nc(nc_info)
        writer_line = fmi_flange.write_prepare()
        fmi_flange.save_file(file_with_path)
        print('Write FMI File')
        return writer_line

    def save_file(self, write_line, file_with_path):
        fmi_flange = FMIBase.Pch()
        fmi_flange.write_file_lines = write_line
        fmi_flange.save_file(file_with_path)


class TSCIIWrite(IWriter):
    def write(self, nc_info, file_with_path, hole_name):
        xml = LxmlBase.XmlGen(file_with_path)
        xml.set_hole_name(hole_name)
        xml.trans_from_nc(nc_info)
        xml.gen_tree()
        # =========================================


class DataFactory:
    def get_data(self):
        pass

    def set_data(self):
        pass


class PedData(DataFactory):
    def get_data(self):
        temp = NcRead()
        return temp

    def set_data(self):
        temp = PedWrite()
        return temp


class FMIData(DataFactory):
    def __init__(self):
        # self.data_head = DataHead()
        pass

    def get_data(self):
        temp = NcRead()
        return temp

    def set_data(self):
        temp = FMIWrite()
        return temp


class TSCIIData(DataFactory):
    def get_data(self):
        temp = NcRead()
        return temp

    def set_data(self):
        temp = TSCIIWrite()
        return temp


class LysaghtRead(IReader):
    def read(self, file_path):
        temp = TransformFunctions.read_data_from_lysaght_engine(file_path)
        return temp


class DTRWrite(IWriter):
    def write(self, orders, file_path):
        temp = TransformFunctions.lysaght_to_dtr(orders, file_path)
        return temp


class LysaghtDTRData(DataFactory):
    def get_data(self):
        temp = LysaghtRead()
        return temp

    def set_data(self):
        temp = DTRWrite()
        return temp


if __name__ == "__main__":
    hole_name = {}

    data = TSCIIData()
    reader = data.get_data()
    writer = data.set_data()
    nc_info = reader.read('E:/Zanweb/Bradbury_Import_Test/20180316_NC/CK10504.nc1')
    writer.write(nc_info, 'E:/Zanweb/PythonProgram/Batch/Camgen/CK10504.xml', hole_name)
