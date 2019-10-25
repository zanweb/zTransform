import os
import sys
import time
from itertools import groupby
from operator import itemgetter

# from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QTreeWidgetItemIterator, QFileDialog, QAction, \
    QMessageBox

from DBbase import dbFunctions
from DTRGen.TransformFunctions import lysaght_csv_from_oracle_to_dtr, convert_nc_from_oracle_to_dtr, \
    check_lysaght_parts_crash
from Zfile import zCSV, zFBase
from zSplitting import Ui_zSplitting
from zSplitting_login_code import LoginDialog


class z_splitting(QMainWindow):
    def __init__(self, parent=None):
        super(z_splitting, self).__init__(parent)
        self.ui = Ui_zSplitting()
        self.ui.setupUi(self)
        self.ui_login = LoginDialog()
        self.root = None
        # self.tree_widget_ui()
        self.setup_default_ui()
        self.toolbar_ui()
        self.user = None
        self.pass_word = ''
        self.server = ''
        self.database = ''
        self.user_group = ''
        self.user_res = ''

        self.catalog = None
        self.org = None
        self.work_center = None
        self.data_source = None

        self.list_make = []
        self.out_folder = ''
        self.nc_folder = ''
        self.csv_folder = ''

    def setup_default_ui(self):
        self.ui.radio_button_trim.setChecked(True)
        self.ui.check_box_lkq.setChecked(True)
        self.ui.radio_button_nc.setChecked(True)

        work_centers = ['Slitting', 'DTR', 'CPurlin', 'ZPurlin']
        self.ui.combo_box_workcenter.addItems(work_centers)

    def get_org_status(self):
        lkq = self.ui.check_box_lkq.checkState()
        sjg = self.ui.check_box_sjg.checkState()
        if lkq != 0:
            if sjg != 0:
                self.org = ('LKQ', 'SJG')
            else:
                self.org = 'LKQ'
        else:
            if sjg != 0:
                self.org = 'SJG'

    def get_catalog_status(self):
        zees = self.ui.radio_button_zees.isChecked()
        cees = self.ui.radio_button_cees.isChecked()
        trim = self.ui.radio_button_trim.isChecked()
        if zees:
            self.catalog = 'ZEES'
        if cees:
            self.catalog = 'CEES'
        if trim:
            self.catalog = 'TRIM'

    def get_data_source(self):
        nc = self.ui.radio_button_nc.isChecked()
        csv = self.ui.radio_button_csv.isChecked()
        if nc:
            self.data_source = 'NC'
        if csv:
            self.data_source = 'CSV'

    def get_work_center(self):
        self.work_center = self.ui.combo_box_workcenter.currentText()

    def get_user_info(self):
        self.user = self.ui_login.pass_info[0]
        self.pass_word = self.ui_login.pass_info[1]
        self.server = self.ui_login.pass_info[2]
        self.database = self.ui_login.pass_info[3]

    def get_user_role(self):
        show_fields = ['UserGroup', 'UserRes']
        params_name = ['UserName']
        params_type = ['%s']
        params = self.user

        role = dbFunctions.user_info_read(self.user, self.pass_word, self.server, self.database, show_fields,
                                          params_name, params_type, params)
        self.user_group = role[0]['UserGroup'].strip(' ')
        self.user_res = role[0]['UserRes'].strip(' ')

    def toolbar_ui(self):
        import_oracle = QAction('导入', self)
        import_oracle.triggered.connect(self.on_import_oracle_triggered)
        toolbar = self.ui.tool_bar
        toolbar.addAction(import_oracle)

    def on_import_oracle_triggered(self):
        if not self.user:
            self.get_user_info()
            self.get_user_role()

        # print(self.user_res, self.user_group)
        file_name, file_type = QFileDialog.getOpenFileName(self, '选取文件', 'C:/', 'CSV Files(*.CSV)')
        # print('import file--> ', file_name, ' ---- file type', file_type)
        insert_return = dbFunctions.oracle_data_import(self.user, self.pass_word, self.server, self.database,
                                                       self.user_group, file_name)
        if insert_return != -1:
            QMessageBox.information(self, '数据导入信息', '数据导入成功！', QMessageBox.Ok)
        else:
            QMessageBox.warning(self, '数据导入警告', '数据导入未成功！', QMessageBox.Ok)

    def slitting_tree_widget_ui(self):
        self.ui.tree_widget.headerItem().setText(0, '---材料---订单---编号---')
        self.ui.tree_widget.headerItem().setText(1, 'Sort Id')
        self.ui.tree_widget.headerItem().setText(2, 'Item')
        self.ui.tree_widget.headerItem().setText(3, 'Fa Qty')
        self.ui.tree_widget.headerItem().setText(4, 'Prd Width')
        self.ui.tree_widget.headerItem().setText(5, 'Unit Length')
        self.ui.tree_widget.width = 850
        self.ui.tree_widget.setColumnWidth(0, 300)

    def c_z_tree_widget_ui(self):
        self.ui.tree_widget.headerItem().setText(0, '---SO---Batch---Coil---编号---')
        self.ui.tree_widget.headerItem().setText(1, 'Sort Id')
        self.ui.tree_widget.headerItem().setText(2, 'Item')
        self.ui.tree_widget.headerItem().setText(3, 'Fa Qty')
        self.ui.tree_widget.headerItem().setText(4, 'Prd Width')
        self.ui.tree_widget.headerItem().setText(5, 'Unit Length')
        self.ui.tree_widget.width = 850
        self.ui.tree_widget.setColumnWidth(0, 300)

    def get_multi_product_data(self, org, catalog, work_center):
        rs_result_multi_product = []

        show_fields = ['[Raw Material]', '[Order Num]',
                       "CASE WHEN [ORG] = 'LKQ' THEN [Mark No] ELSE LEFT([Fa Item],7)  END AS Item",
                       '[Fa Qty]', '[Fa Job]', '[Sort Id]', '[Sort Complete]', '[AutoNo]', '[Prd Width]',
                       '[Unit Length]', '[Batch Id]']
        params_name = [r"[Sort Complete]", '[ORG]', '[Item Cat]', '[Group]']
        params_type = ['%s', '%s', '%s', '%s']
        params = (' ', org, catalog, self.user_group)

        rs = dbFunctions.oracle_data_read(self.user, self.pass_word, self.server, self.database, show_fields,
                                          params_name, params_type, params)

        if work_center == 'Slitting':
            # pprint(rs)
            rs_by_material = sorted(rs, key=itemgetter('Raw Material', 'Order Num'))
            for mat, group_batch in groupby(rs_by_material, key=itemgetter('Raw Material')):
                mate = []
                for order, group_order in groupby(group_batch, key=itemgetter('Order Num')):
                    l_dic = []
                    for each in group_order:
                        dic = {}
                        for item in each.items():
                            key, value = item
                            if value:
                                dic[key] = str(value).strip(' ')
                            else:
                                dic[key] = ''
                        l_dic.append(dic)
                    mate.append((str(order), [], l_dic))
                rs_result_multi_product.append((mat, mate, {}))

            # pprint(rs_result)
        else:
            if work_center == 'DTR':
                rs_by_material = sorted(rs, key=itemgetter('Batch Id', 'Raw Material'))
                for order_num, group_order in groupby(rs_by_material, key=itemgetter('Order Num')):
                    so = []
                    for batch_num, group_batch in groupby(group_order, key=itemgetter('Batch Id')):
                        batch = []
                        for material_num, group_material in groupby(group_batch, key=itemgetter('Raw Material')):
                            l_dic = []
                            for each in group_material:
                                dic = {}
                                for item in each.items():
                                    key, value = item
                                    if value:
                                        dic[key] = str(value).strip(' ')
                                    else:
                                        dic[key] = ''
                                l_dic.append(dic)
                            batch.append((str(material_num), [], l_dic))
                        so.append((str(batch_num), batch, {}))
                    rs_result_multi_product.append((order_num, so, {}))

        return rs_result_multi_product

    @pyqtSlot()
    def on_push_button_load_clicked(self):
        if not self.user:
            self.get_user_info()
            self.get_user_role()
        self.get_catalog_status()
        self.get_org_status()
        self.get_work_center()

        data = self.get_multi_product_data(self.org, self.catalog, self.work_center)

        if self.root:
            self.root = None
            self.ui.tree_widget.clear()
        if self.work_center == 'Slitting':
            self.slitting_tree_widget_ui()
        else:
            self.c_z_tree_widget_ui()
        self.root = QTreeWidgetItem(self.ui.tree_widget)
        self.root.setText(0, '未计划')
        # self.ui.tree_widget.addTopLevelItem(self.root)

        self.add_item(self.root, data)
        # self.ui.tree_widget.expandAll()

    @pyqtSlot()
    def on_push_button_get_clicked(self):
        self.list_make = []
        item = QTreeWidgetItemIterator(self.ui.tree_widget)
        while item.value():
            tmp = {}
            if item.value().checkState(0) == Qt.Checked:
                if item.value().childCount() == 0:
                    tmp = {
                        'AutoNo': item.value().text(0),
                        'Sort Id': item.value().text(1),
                        'Item': item.value().text(2),
                        'Fa Qty': item.value().text(3),
                        'Prd Width': item.value().text(4),
                        'Unit Length': item.value().text(5),
                    }
                    # pprint(tmp)
                    # print(item.value().childCount())
            if tmp:
                self.list_make.append(tmp)
            item = item.__iadd__(1)
        if self.list_make:
            print(self.list_make)
            QMessageBox.information(self, '获取信息', '已经获取所选数据，请及时处理！', QMessageBox.Ok)
            # self.save_to_csv()
        else:
            QMessageBox.warning(self, '获取信息', '你没有选择任何内容!', QMessageBox.Ok)

    @pyqtSlot()
    def on_push_button_transform_clicked(self):
        self.get_data_source()
        if self.work_center == 'Slitting':
            self.slitting_save_to_csv()
        if self.work_center == 'DTR':
            # 如果是Butler的NC文件
            if self.org == 'SJG':
                self.process_nc_to_dtr()
            if self.org == 'LKQ':
                # '''
                # TODO: 处理LKQ格式清单
                # '''
                # 获取关键字段
                if self.data_source == 'CSV':
                    self.process_csv_to_dtr()
                else:
                    self.process_nc_to_dtr()

    @pyqtSlot()
    def on_push_button_complete_clicked(self):
        ok = QMessageBox.question(self, '数据库数据信息', '所选内容将在数据库标注为完工，是否进行？', QMessageBox.Yes, QMessageBox.No)
        if ok == QMessageBox.Yes:
            if self.list_make:
                fin = self.update_oracle_date_complete(self.list_make)
                if not fin:
                    QMessageBox.information(self, '数据库更新信息', '数据库更新完成！', QMessageBox.Ok)
                else:
                    QMessageBox.warning(self, '数据库更新警告', '数据库更新问题！\n 请联系相关人员！', QMessageBox.Ok)
            else:
                QMessageBox.information(self, '无数据警告', '没有数据！\n 请选择数据后再操作！', QMessageBox.Ok)
                return
        else:
            return

    def check_nc_files_exite(self, list_make_files, nc_folder):
        list_exit_files = []
        list_no_files = []
        list_nc_files = zFBase.get_indicate_ext_file(nc_folder, 'nc1')
        if list_nc_files:
            for file in list_make_files:
                if file in list_nc_files:
                    list_exit_files.append(file)
                else:
                    list_no_files.append(file)
        return list_exit_files, list_no_files

    def slitting_save_to_csv(self):
        file_with_path = QFileDialog.getExistingDirectory(None, '请指定目标文件目录:')
        file_with_path += '/' + time.strftime('%y%m%d%H%M%S', time.localtime())  # str(random.randint(0, 9))
        file_with_path += '.CSV'
        csv_save = zCSV.CsvFile(file_with_path)
        ok = csv_save.write_slitting_list(self.list_make)
        if ok:
            QMessageBox.information(self, '保存文件信息', '文件已保存！\n' + file_with_path, QMessageBox.Ok)
            # fin = self.update_oracle_date_complete(self.list_make)
            # if not fin:
            #     QMessageBox.information(self, '数据库更新信息', '数据库更新完成！', QMessageBox.Ok)
            # else:
            #     QMessageBox.warning(self, '数据库更新警告', '数据库更新问题！\n 请联系相关人员！', QMessageBox.Ok)
        else:
            QMessageBox.warning(self, '保存文件', '文件未保存！\n 请联系相关人员！', QMessageBox.Ok)

    def update_oracle_date_complete(self, list_make):
        list_auto = []
        for dic in list_make:
            list_auto.append(dic['AutoNo'])
        update_fields = ['[Sort Complete]']
        update_values = ['Y']
        params_name = ['AutoNo']
        params_type = ['%s']
        params = list_auto

        back = dbFunctions.oracle_data_update(self.user, self.pass_word, self.server, self.database, update_fields,
                                              update_values, params_name, params_type,
                                              params,
                                              option=None)
        return back

    def add_item(self, parent, element):
        if isinstance(parent, QTreeWidgetItem):
            # parent.setText(0, text)
            parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        for text, children, infos in element:
            item = QTreeWidgetItem()
            item.setText(0, str(text))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(0, Qt.Unchecked)
            parent.addChild(item)
            if children:
                self.add_item(item, children)
            else:
                if infos:
                    for info in infos:
                        item_info = QTreeWidgetItem()
                        item_info.setText(0, info['AutoNo'])
                        item_info.setText(1, info['Sort Id'])
                        item_info.setText(2, info['Item'])
                        item_info.setText(3, info['Fa Qty'])
                        item_info.setText(4, info['Prd Width'])
                        item_info.setText(5, info['Unit Length'])

                        item_info.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                        item_info.setCheckState(0, Qt.Unchecked)
                        item.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                        item.addChild(item_info)

    def process_nc_to_dtr(self):
        # 获取关键字段
        list_auto = []
        for dic in self.list_make:
            list_auto.append(dic['AutoNo'])
        # 获取制作列表的构件名
        list_make_files = []
        for dic in self.list_make:
            list_make_files.append(dic['Item'][0:7])
        # 获取NC文件夹
        self.nc_folder = QFileDialog.getExistingDirectory(None, '请指定NC文件目录：')
        # 检查NC文件是否存在
        # 获取存在的文件名列表和不存在的文件名列表
        exit_files, no_files = self.check_nc_files_exite(list_make_files, self.nc_folder)
        if no_files:
            str_nofiles = ''
            for no_file in no_files:
                str_nofiles += str(no_file) + '\n'
            QMessageBox.warning(self, 'NC文件', 'NC文件缺失警告！\n' + str_nofiles, QMessageBox.Ok)
            print(str(no_files))
        else:
            if exit_files:
                QMessageBox.information(self, 'NC文件', 'NC文件齐全,开始转换。', QMessageBox.Ok)
                # 指定输出文件夹
                self.out_folder = QFileDialog.getExistingDirectory(self, '获取转换后的文件夹:')
                # 获取制作清单数据结构
                list_auto_int = [int(x) for x in list_auto]
                # print(list_auto_int)
                tuple_auto = tuple(list_auto_int)
                read_return = dbFunctions.oracle_data_read_in_auto(self.user, self.pass_word, self.server,
                                                                   self.database, tuple_auto)
                # print(read_return)
                # NC文件转DTR
                try:
                    cut_list, no_pattern_list, parts = convert_nc_from_oracle_to_dtr(read_return, self.nc_folder,
                                                                                     self.org)

                    self.save_dtr_files(cut_list, no_pattern_list, parts)
                except Exception as e:
                    print(e)
            else:
                QMessageBox.warning(self, 'NC文件', '目录内没有NC文件！', QMessageBox.Ok)

    def process_csv_to_dtr(self):
        list_auto = []
        for dic in self.list_make:
            list_auto.append(dic['AutoNo'])
        # 获取制作列表的构件名
        list_make_files = []
        for dic in self.list_make:
            list_make_files.append(dic['Item'])
        list_make_files = list(set(list_make_files))  # 零件去重
        print(list_make_files)
        # 从csv的文件夹中读取
        all_parts = []  # 所有csv文件中的parts（lyasght）
        all_parts_no = []
        self.csv_folder = QFileDialog.getExistingDirectory(None, '请指定csv文件目录：')
        csv_files = zFBase.get_indicate_ext_file(self.csv_folder, 'csv')
        for csv in csv_files:
            csv_file_path = self.csv_folder + '/' + str(csv) + '.csv'
            csv_file = zCSV.CsvFile(csv_file_path)
            csv_parts = csv_file.get_lysaght_punch()
            all_parts.extend(csv_parts)
            all_parts_no = [no.part_no for no in all_parts]
        print(all_parts_no)
        miss_parts = list(set(list_make_files).difference(set(all_parts_no)))
        if miss_parts:
            QMessageBox.warning(self, '工程数据缺失', '缺失如下零件csv数据, 请补充数据！！！\n' + str(miss_parts), QMessageBox.Ok)
            return 0

        # 获取清单数据
        QMessageBox.information(self, '工程数据文件', '工程数据文件齐全,开始转换。', QMessageBox.Ok)
        # 指定输出文件夹
        self.out_folder = QFileDialog.getExistingDirectory(self, '获取转换后的文件夹:')
        # 获取制作清单数据结构
        list_auto_int = [int(x) for x in list_auto]
        # print(list_auto_int)
        tuple_auto = tuple(list_auto_int)
        read_return = dbFunctions.oracle_data_read_in_auto(self.user, self.pass_word, self.server,
                                                           self.database, tuple_auto)
        all_parts_make = []
        for part in all_parts:
            if part.part_no in list_make_files:
                all_parts_make.append(part)

        try:
            # 检查lysaght-parts是否crash
            crash_parts = check_lysaght_parts_crash(all_parts_make)
            if crash_parts:
                QMessageBox(self, '警告', '下列零件孔位y轴上有碰撞\n' + str(crash_parts))
                return
            else:
                cut_list, no_pattern_list, parts = lysaght_csv_from_oracle_to_dtr(read_return, all_parts_make)
                self.save_dtr_files(cut_list, no_pattern_list, parts)
        except Exception as e:
            print(e)

    def save_dtr_files(self, cut_list, no_pattern_list, parts):
        if no_pattern_list:
            str_show = ''
            for no_pattern in no_pattern_list:
                str_show += str(no_pattern) + '\n'
            QMessageBox.warning(self, '警告', '有未定义的孔位\n' + str_show, QMessageBox.Ok)
            return 1
        print(cut_list, parts)
        cut_list_file = 'D' + '0' * 7 + '.ORD'
        cut_list_file_path = os.path.join(self.out_folder, cut_list_file)
        cut_list.save_as(cut_list_file_path)
        parts_file = 'D' + '0' * 7 + '.PRT'
        parts_file_path = os.path.join(self.out_folder, parts_file)
        parts.save_as(parts_file_path)
        QMessageBox.information(self, '完成', '已经完成！', QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Form = QtWidgets.QWidget()
    ui = z_splitting()
    Form = ui
    ui.show()
    ui.ui_login.show()
    # ui.show()

    sys.exit(app.exec_())
