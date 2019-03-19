import os
import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtWidgets import QFileDialog

from CamGen import DataTransform
from Zfile.zFBase import check_file_exist
from zTransform import Ui_zTransform


class z_transform(QMainWindow):
    def __init__(self, parent=None):
        super(z_transform, self).__init__(parent)
        self.ui = Ui_zTransform()
        self.ui.setupUi(self)

        self.directory_source_folder = ''
        self.directory_dist_folder = ''

        data_source = ['LYSAGHT ENG', 'BUTLER TEK']
        dist_machine = ['DTR', 'C PURLING']

        self.ui.combo_box_data_source.addItems(data_source)
        self.ui.combo_box_dist_machine.addItems(dist_machine)

    @pyqtSlot()
    def on_push_button_source_folder_clicked(self):
        """ 定位源目录"""
        self.directory_source_folder = QFileDialog.getExistingDirectory(None, '请指定源文件目录:')
        self.ui.lineEdit_source_folder.setText(self.directory_source_folder)
        self.ui.statusbar.showMessage('Source folder is OK!')

    @pyqtSlot()
    def on_push_button_dist_folder_clicked(self):
        """定位目标目录"""
        self.directory_dist_folder = QFileDialog.getExistingDirectory(None, '请指定目标文件目录:')
        self.ui.lineEdit_dist_folder.setText(self.directory_dist_folder)
        self.ui.statusbar.showMessage('Dist folder is OK!')

    @pyqtSlot()
    def on_push_button_start_clicked(self):
        current_source_data = self.ui.combo_box_data_source.currentText()
        current_dist_machine = self.ui.combo_box_dist_machine.currentText()
        current_message = 'Data Source: ' + current_source_data + ', Machine: ' + current_dist_machine
        self.ui.statusbar.showMessage(current_message + ' : Running Now...')
        if (self.ui.lineEdit_source_folder.text() is None) or self.ui.lineEdit_source_folder.text() == '':
            QMessageBox.warning(None, '警告', '请选择源文件夹！', QMessageBox.Ok)
            self.ui.push_button_source_folder.setFocus()
            self.ui.statusbar.showMessage('请选择源文件夹！')
            return
        if (self.ui.lineEdit_dist_folder.text() is None) or self.ui.lineEdit_dist_folder.text() == '':
            QMessageBox.warning(None, '警告', '请选择目标文件夹！', QMessageBox.Ok)
            self.ui.push_button_dist_folder.setFocus()
            self.ui.statusbar.showMessage('请选择目标文件夹！')
            return
        if self.check_init():
            is_ready = self.run()
            if is_ready:
                self.ui.statusbar.showMessage('Transform Process Finished!')
                is_open_dist_folder = QMessageBox.question(self, '打开转换目录', '转换完成！是否打开转换后的目录?（y/n）',
                                                           QMessageBox.Yes | QMessageBox.No)
                if is_open_dist_folder == QMessageBox.Yes:
                    os.chdir(self.directory_dist_folder)
                    explorer_fold = os.getcwd()
                    os.system("explorer.exe %s" % explorer_fold)
        else:
            self.ui.statusbar.showMessage('请检查文件是否齐全！')

    def run(self):
        current_source_data = self.ui.combo_box_data_source.currentText()
        current_dist_machine = self.ui.combo_box_dist_machine.currentText()
        # print(current_source_data, current_dist_machine)
        if current_source_data == r'LYSAGHT ENG':
            if current_dist_machine == r'DTR':
                data = DataTransform.LysaghtDTRData()
                reader = data.get_data()
                writer = data.set_data()
                order = reader.read(self.directory_source_folder + '/')
                for one_order in order:
                    writer.write(one_order, self.directory_dist_folder + '/')
            else:
                QMessageBox.information(self, '信息', current_dist_machine + ': 此机器的转换还未完成！')
                return False
        else:
            QMessageBox.information(self, '信息', current_source_data + ': 此数据源的转换还未完成！')
            return False
        return True

    def check_init(self):
        foo1 = check_file_exist('./DTRTools.csv')
        foo2 = check_file_exist('./LysaghtHoleDia.csv')
        if foo1 and foo2:
            return True
        return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Form = QtWidgets.QWidget()
    ui = z_transform()
    Form = ui
    ui.show()
    sys.exit(app.exec_())
