#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :   2020/02/10 9:22
# @Author   :   ZANWEB
# @File     :   TransformFunctions.py in zTransform
# @IDE      :   PyCharm


import os
import sys
from itertools import groupby
from operator import itemgetter

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog

from DTRGen import TransformFunctions
from Zfile import zCSV, zFBase
from zCpurlin_ui import Ui_MainWindow


class z_c_purlin(QMainWindow):
    def __init__(self, parent=None):
        super(z_c_purlin, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.oracle_file = ''
        self.source_folder = ''
        self.dist_folder = ''
        self.data_source_type = ''
        self.lysaght_parts = []

        self.item_list = []

        data_source = ['NC', 'CSV']
        self.ui.combo_box_source_type.addItems(data_source)

    @pyqtSlot()
    def on_push_button_select_oracle_file_clicked(self):
        try:
            self.oracle_file, _ = QFileDialog.getOpenFileName(None, '请指定所需的Oracle文件:', '', '(*.CSV *.csv)')
            if self.oracle_file:
                self.ui.line_edit_oracle_file.setText(self.oracle_file)
                self.ui.statusbar.showMessage('已经指定ORACLE文件!')
        except Exception as e:
            QMessageBox.information(self, '出错', str(e))

    @pyqtSlot()
    def on_push_button_source_dir_clicked(self):
        self.source_folder = QFileDialog.getExistingDirectory(None, '请指定源文件目录:')
        if self.source_folder:
            self.ui.line_edit_source_dir.setText(self.source_folder)
            self.ui.statusbar.showMessage('已经指定源文件目录!')

    @pyqtSlot()
    def on_push_button_dist_dir_clicked(self):
        self.dist_folder = QFileDialog.getExistingDirectory(None, '请指定目标目录:')
        if self.dist_folder:
            self.ui.line_edit_dist_dir.setText(self.dist_folder)
            self.ui.statusbar.showMessage('已经指定目标目录!')

    @pyqtSlot()
    def on_push_button_exit_clicked(self):
        rep = QMessageBox.warning(self, '退出', '即将退出应用程序?', QMessageBox.No | QMessageBox.Yes)
        if rep == QMessageBox.Yes:
            exit(0)
        if rep == QMessageBox.No:
            return

    @pyqtSlot()
    def on_push_button_run_clicked(self):
        if not self.oracle_file:
            QMessageBox.warning(self, '出错:', '请输入Oracle文件!')
            self.ui.line_edit_oracle_file.setFocus()
            return
        if not self.source_folder:
            QMessageBox.warning(self, '出错:', '请输入源数据目录!')
            self.ui.line_edit_source_dir.setFocus()
            return
        if not self.dist_folder:
            QMessageBox.warning(self, '出错:', '请输入目标数据目录!')
            self.ui.line_edit_dist_dir.setFocus()
            return
        self.data_source_type = self.ui.combo_box_source_type.currentText()
        self.run()

    def run(self):
        c_lysaght_parts = []
        total_qty = 0
        self.get_item_list()
        item_exist, item_not_exist = self.check_source_files_exit()
        sorted_item_list = []
        for item in self.item_list:
            item['Unit Length'] = int(item['Unit Length'])
        for index_mtl, mtl_group in groupby(self.item_list, key=itemgetter('Raw Material')):
            # print(index_mtl)
            sorted_item_list.extend(sorted(list(mtl_group), key=itemgetter('Unit Length'), reverse=True))
        self.item_list = sorted_item_list
        # return

        if not item_not_exist:
            if self.data_source_type == 'NC':
                org = self.item_list[0]['ORG']
                if org != 'LKQ':
                    org = 'SJG'
                self.lysaght_parts = TransformFunctions.convert_nc_files_to_lysaght_parts(self.item_list,
                                                                                          self.source_folder, org=org)
            if self.data_source_type == 'CSV':
                if not self.lysaght_parts:
                    QMessageBox.warning(self, '错误:', '没有lysaght_parts!')
            for each_part in self.lysaght_parts:
                if each_part.part_no in item_exist:
                    # 看是否需要加预处理?
                    each_part.sort_holes()
                    each_part.group_holes_by_y()
                    part_str = each_part.convert_to_c_pattern(tool_list='')
                    # one_part_info = [part_str, each_part.quantity, each_part.part_length, item_no, bundle]
                    one_part_info = [each_part.part_no, part_str, each_part.section, each_part.part_length]
                    c_lysaght_parts.append(one_part_info)
        order_no = self.item_list[0]['So']
        customer = self.item_list[0]['Batch']

        for item in self.item_list:
            total_qty += int(item['Qty'])

        pre_project_info = ''
        line_str = []
        line_str_list = []

        for item in self.item_list:
            if item['ORG'] == 'LKQ':
                part_no = item['Mark No']
            else:
                part_no = item['Item']
            for part in c_lysaght_parts:
                if part[0] == part_no:
                    project_info = str(order_no) + ',' + part[2] + ',' + str(customer) + ',,' + str(order_no) + ','
                    if project_info == pre_project_info:
                        project_info = ',,,,,'
                    else:
                        if line_str:
                            line_str_list.append(line_str)
                            line_str = []
                    line_str_tmp = project_info + part[0] + ',' + str(part[3]) + ',' + item['Qty'] + ',' + part[1] + ','
                    line_str_tmp += item['Bundle'] + ',,,,Standard,,' + str(total_qty) + ',' + str(total_qty) + ','
                    line_str_tmp += str(part[3])
                    line_str.append(line_str_tmp)
                    if project_info != ',,,,,':
                        pre_project_info = project_info
        if line_str_list:
            # print(line_str_list)
            try:
                for line_str in line_str_list:
                    # print(line_str)
                    os.chdir(self.dist_folder)
                    file_name = str(line_str[0].split(',')[1]) + '.csv'
                    file_name = file_name.replace('*', '_')
                    print(file_name)
                    path = os.path.join(os.getcwd(), file_name)
                    with open(path, 'w', newline='') as csvfile:
                        for row in line_str:
                            csvfile.write(row + '\n')
                        csvfile.close()
                QMessageBox.information(self, '保存:', '文件已保存!\n确定后将打开目标文件夹!')
                os.chdir(self.dist_folder)
                folder_path = os.getcwd()
                os.system("start explorer %s" % folder_path)
            except Exception as e:
                QMessageBox.warning(self, '保存出错:', '文件未保存!!!\n' + str(e))
                return 0

    def get_item_list(self):
        seq_file = self.oracle_file
        if seq_file:
            csv_file = zCSV.CsvFile(seq_file)
            csv_file.del_lines_begin(8)
            self.item_list = csv_file.get_seq_list()
        else:
            QMessageBox.warning(self, '错误', '没有制作清单文件!\n请指定Oracel制作清单文件!', QMessageBox.Ok)
            return 0

    def get_item_names(self):
        item_names = []
        for each_item in self.item_list:
            if each_item['ORG'] == 'LKQ':
                item_names.append(each_item['Mark No'])
            else:
                item_names.append(each_item['Item'])
        item_names = list(set(item_names))
        return item_names

    def check_source_files_exit(self):
        file_exist = []
        file_not_exist = []
        item_names = self.get_item_names()
        if self.data_source_type == 'NC':
            nc_file_list = zFBase.get_indicate_ext_file(self.source_folder, 'nc1')
            if nc_file_list:
                for each_item in item_names:
                    if each_item in nc_file_list:
                        file_exist.append(each_item)
                    else:
                        file_not_exist.append(each_item)
                return file_exist, file_not_exist
            else:
                QMessageBox.warning(self, 'nc文件:', '目录中没有NC文件!')
                return 0
        if self.data_source_type == 'CSV':
            # 从csv的文件夹中读取
            all_parts = []  # 所有csv文件中的parts（lyasght）
            all_parts_no = []
            csv_files = zFBase.get_indicate_ext_file(self.source_folder, 'csv')
            if csv_files:
                for csv in csv_files:
                    csv_file_path = self.source_folder + '/' + str(csv) + '.csv'
                    csv_file = zCSV.CsvFile(csv_file_path)
                    csv_parts = csv_file.get_lysaght_punch()
                    all_parts.extend(csv_parts)
                    all_parts_no = [no.part_no for no in all_parts]
                # print(all_parts_no)
                miss_parts = list(set(item_names).difference(set(all_parts_no)))
                if miss_parts:
                    QMessageBox.warning(self, '工程数据缺失', '缺失如下零件csv数据, 请补充数据！！！\n' + str(miss_parts), QMessageBox.Ok)
                    return 0
                else:
                    self.lysaght_parts = all_parts
                    return item_names, miss_parts


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Form = QtWidgets.QWidget()
    ui = z_c_purlin()
    Form = ui
    ui.show()
    sys.exit(app.exec_())
