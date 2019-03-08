class IReader:
    def read(self):
        pass


class NcRead(IReader):
    def __init__(self):
        pass

    def read(self):
        print('read nc file')


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
    def write(self):
        print('Write Peddinghaus File')


class FMIWrite(IWriter):
    def write(self):
        print('Write FMI File')


class DataFactory:
    def get_data(self):
        pass

    def set_data(self):
        pass


class PeddinghausData(DataFactory):
    def get_data(self):
        temp = NcRead()
        return temp

    def set_data(self):
        temp = PedWrite()
        return temp


class FMIData(DataFactory):
    def __init__(self):
        self.data_head = DataHead()

    def get_data(self):
        temp = NcRead()
        return temp

    def set_data(self):
        temp = FMIWrite()
        return temp


class DataHead:
    batch = ''
    order = ''


if __name__ == "__main__":
    data = FMIData()
    reader = data.get_data()
    writer = data.set_data()
    reader.read()
    writer.write()
