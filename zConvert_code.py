import os

from PyQt5.QtWidgets import QMessageBox, QFileDialog

from CamGen import DataTransform
from Zfile import zFBase, zCSV
from zConvert import *
from LysaghtPurlin.TransformFunctions import nc_file_header_profile


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    # class MainWindow(QtWidgets.QWidget, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.in_folder = ''
        self.out_folder = ''
        self.item_list = []  # dic list {Item, Qty, Unit length, Thk}
        self.make_item_list = []
        self.z_profile = []
        self.z_mtl = {}
        self.home_name = {}

        self.pushButton_NCPath.clicked.connect(self.browse_nc_path)
        self.pushButton_ConvertPath.clicked.connect(self.browse_convert_path)
        self.pushButton_Run.clicked.connect(self.run)

    def browse_nc_path(self):
        QMessageBox.information(self, '信息', '请指定NC文件目录！', QMessageBox.Yes)
        self.lineEdit_NCPath.setText(QFileDialog.getExistingDirectory(None, '请指定NC文件目录:'))
        self.in_folder = self.lineEdit_NCPath.text()

    def browse_convert_path(self):
        QMessageBox.information(self, '信息', '请指定输出文件目录！', QMessageBox.Yes)
        self.lineEdit_ConvertPath.setText(QFileDialog.getExistingDirectory(None, '请指定输出文件目录:'))
        self.out_folder = self.lineEdit_ConvertPath.text()

    def get_item_list(self):
        seq_file = zFBase.get_indicate_ext_file(self.in_folder, 'CSV')
        if seq_file:
            file_name = seq_file[0] + '.csv'
            file_full_path = os.path.join(self.in_folder, file_name)
            csv_file = zCSV.CsvFile(file_full_path)
            csv_file.del_lines_begin(8)
            self.item_list = csv_file.get_seq_list()
            # print(self.item_list)
        else:
            QMessageBox.warning(self, '错误', '没有制作清单文件!\n请在NC文件夹内添加制作清单文件！\n程序将关闭！', QMessageBox.Ok)
            exit()

    def convert_tsc(self):
        if self.make_item_list:
            # print(self.make_item_list)
            for item in self.make_item_list:
                file_name = item['Item'] + '.nc1'
                file_full_path = os.path.join(self.in_folder, file_name)
                out_file_name = item['Item'] + '.xml'
                out_file_path = self.out_folder + '/' + str(item['Thk']) + '_' + item['Sorts']
                if not os.path.exists(out_file_path):
                    os.makedirs(out_file_path)
                out_file_full_path = os.path.join(out_file_path, out_file_name)

                # print(out_file_full_path)

                data = DataTransform.TSCIIData()
                reader = data.get_data()
                writer = data.set_data()
                nc_info = reader.read(file_full_path)
                # need change width and qty
                self.get_z_mtl_info(self.z_profile, nc_info.header.profile)
                if not self.z_mtl:
                    profile_height, flange_width, web_thickness = nc_file_header_profile(nc_info.header)
                    self.z_mtl['Width'] = flange_width
                    self.z_mtl['profile_height'] = profile_height
                    self.z_mtl['web_thickness'] = web_thickness

                nc_info.header.order = item['So']  # 图纸中的还是清单中？
                nc_info.header.quantity = item['Qty']
                nc_info.header.profile_height = self.z_mtl['Width']
                if abs(nc_info.header.length - float(item['Unit Length'])) > 0.5:  # 长度是否需要更改？
                    QMessageBox.warning(self, '警告:', nc_info.header.drawing + ':清单长度与NC文件中的长度不同，\n将采用NC文件中的长度！')
                writer.write(nc_info, out_file_full_path, self.home_name)
        else:
            QMessageBox.warning(self, '错误', '制作清单为空，请修改！', QMessageBox.Ok)
            exit()
        self.finish_check()

    def get_z_profile_list(self):
        file_name = 'Z.csv'
        if not os.path.isfile(file_name):
            QMessageBox.warning(self, '警告', file_name + '  文件不存在！\n请将它拷贝到安装目录下！', QMessageBox.Yes)
            exit()
        csv_file = zCSV.CsvFile(file_name)
        self.z_profile = csv_file.get_z_list()

    def get_z_mtl_info(self, z_profile_list, z_profile):
        for sec in z_profile_list:
            if sec['Section'] == z_profile:
                self.z_mtl = sec

    def get_hole_name(self):
        file_name = 'holeName.csv'
        if not os.path.isfile(file_name):
            QMessageBox.warning(self, '警告', file_name + '  文件不存在！\n请将它拷贝到安装目录下！', QMessageBox.Ok)
            exit()
        csv_file = zCSV.CsvFile(file_name)
        self.home_name = csv_file.get_hole_name()
        return self.home_name

    def check_nc_exit(self):
        if self.item_list:
            for item in self.item_list:
                file_name = item['Item'] + '.nc1'
                file_full_path = os.path.join(self.in_folder, file_name)
                if not os.path.isfile(file_full_path):
                    answer = QMessageBox.warning(self, '警告', file_name + '文件不存在!\n继续（Y/N)?',
                                                 QMessageBox.Yes | QMessageBox.No)
                    if answer == QMessageBox.Yes:
                        continue
                    else:
                        self.make_item_list = []
                        break
                self.make_item_list.append(item)

    def finish_check(self):
        answer = QMessageBox.question(self, '信息', '文件转换成功，请检查输出文件夹！\n继续转换？(Y/N)?',
                                      QMessageBox.Yes | QMessageBox.No)
        explorer_fold = self.lineEdit_ConvertPath.text()
        os.chdir(explorer_fold)
        explorer_fold = os.getcwd()

        os.system("explorer %s" % explorer_fold)
        # print(explorer_fold)
        if answer == QMessageBox.No:
            os._exit(0)
            exit()

    def run(self):
        self.get_hole_name()
        self.get_z_profile_list()
        self.get_item_list()
        self.check_nc_exit()
        self.convert_tsc()
        # self.finish_check()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_show = MainWindow()
    main_show.show()

    sys.exit(app.exec_())
