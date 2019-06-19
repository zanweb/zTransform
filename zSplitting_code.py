import sys
import time
from itertools import groupby
from operator import itemgetter

# from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QTreeWidgetItemIterator, QFileDialog, QAction, \
    QMessageBox

from DBbase import dbFunctions
from Zfile import zCSV
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

        self.list_make = []

    def setup_default_ui(self):
        self.ui.radio_button_trim.setChecked(True)
        self.ui.check_box_lkq.setChecked(True)

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

    def get_multi_product_data(self, org, catalog, work_center):
        rs_result_multi_product = []

        if work_center == 'Slitting':
            show_fields = ['[Raw Material]', '[Order Num]',
                           "CASE WHEN [ORG] = 'LKQ' THEN [Mark No] ELSE [Fa Item]  END AS Item",
                           '[Fa Qty]', '[Fa Job]', '[Sort Id]', '[Sort Complete]', '[AutoNo]', '[Prd Width]',
                           '[Unit Length]']
            params_name = [r"[Sort Complete]", '[ORG]', '[Item Cat]', '[Group]']
            params_type = ['%s', '%s', '%s', '%s']
            params = (' ', org, catalog, self.user_group)

            rs = dbFunctions.oracle_data_read(self.user, self.pass_word, self.server, self.database, show_fields,
                                              params_name, params_type, params)
            # pprint(rs)
            rs_by_material = sorted(rs, key=itemgetter('Raw Material', 'Order Num'))
            for mat, group_mat in groupby(rs_by_material, key=itemgetter('Raw Material')):
                mate = []
                for order, group_order in groupby(group_mat, key=itemgetter('Order Num')):
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
        self.slitting_tree_widget_ui()
        self.root = QTreeWidgetItem(self.ui.tree_widget)
        self.root.setText(0, '未计划')
        # self.ui.tree_widget.addTopLevelItem(self.root)

        self.add_item(self.root, data)
        self.ui.tree_widget.expandAll()

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
        if self.work_center == 'Slitting':
            self.slitting_save_to_csv()

    def slitting_save_to_csv(self):
        file_with_path = QFileDialog.getExistingDirectory(None, '请指定目标文件目录:')
        file_with_path += '/' + time.strftime('%y%m%d%H%M%S', time.localtime())  # str(random.randint(0, 9))
        file_with_path += '.CSV'
        csv_save = zCSV.CsvFile(file_with_path)
        ok = csv_save.write_slitting_list(self.list_make)
        if ok:
            QMessageBox.information(self, '保存文件信息', '文件已保存！\n' + file_with_path, QMessageBox.Ok)
            fin = self.update_oracle_date_complete(self.list_make)
            if not fin:
                QMessageBox.information(self, '数据库更新信息', '数据库更新完成！', QMessageBox.Ok)
            else:
                QMessageBox.warning(self, '数据库更新警告', '数据库更新问题！\n 请联系相关人员！', QMessageBox.Ok)
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
            item.setText(0, text)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Form = QtWidgets.QWidget()
    ui = z_splitting()
    Form = ui
    ui.show()
    ui.ui_login.show()
    # ui.show()

    sys.exit(app.exec_())
