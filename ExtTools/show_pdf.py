#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :   2020/9/24 16:08
# @Author   :   ZANWEB
# @File     :   show_pdf in anything_test
# @IDE      :   PyCharm

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import fitz


class MainWin(QWidget):
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        self.title = 'PDF Viewer'
        self.left = 250
        self.top = 50
        self.width = 1280
        self.height = 980

        self.image_ext_list = ['.bmp', '.jpg', '.png', '.gif']

        self.tree = QTreeView(self)
        self.label_pdf = QLabel()
        # self.label_pdf.setText('image')
        self.model = QFileSystemModel()
        self.doc = None
        self.current_page = 0

        self.ui_init()
        self.set_connects()

    def ui_init(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setBackgroundRole(QPalette.Dark)
        # self.show()
        # self.tree = QTreeView()
        # self.creat_tree_view()

        hbox = QHBoxLayout()
        self.creat_tree_view()
        hbox.addWidget(self.tree)
        hbox.addWidget(self.label_pdf)

        self.setLayout(hbox)

    def creat_tree_view(self):
        self.tree.setModel(self.model)
        self.model.setRootPath('')
        self.tree.setMaximumWidth(400)

    def set_connects(self):
        self.tree.doubleClicked.connect(self.tree_double_clicked)
        # self.tree.selectionModel().selectionChanged.connect(self.tree_double_clicked)
        self.tree.selectionModel().currentRowChanged.connect(self.tree_double_clicked)
        # self.tree.currentChanged.connect(self.tree_double_clicked)
        # self.tree.Clicked.connect(self.tree_double_clicked)
        # self.label_pdf.wheelEvent.connect(self.on_mouse_wheel)

    # @pyqtSlot(QModelIndex, QModelIndex)
    def tree_double_clicked(self, index, old_index=None):
        try:    # if qItemSelection
            new_index = index.indexes()[0]
        except: # if qModelIndex
            new_index = index
        path = self.model.filePath(index)
        print(path)
        is_dir = self.model.fileInfo(index).isDir()
        print(is_dir)
        if not is_dir:
            root, ext = os.path.splitext(path)
            if ext == '.pdf':
                # print('it\'s a pdf')
                self.set_pdf_info(path)
            if ext.lower() in self.image_ext_list:
                width = self.label_pdf.width()
                height = self.label_pdf.height()
                pix = QPixmap(path)
                fit_pix = pix.scaled(width,height,Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.label_pdf.setPixmap(fit_pix)
                self.label_pdf.setAlignment(Qt.AlignCenter)
                # self.label_pdf.setScaledContents(True)
                # image = cv2.imread(path)
                # cv2.imshow('图片', image)
                # cv2.waitKey(0)

    def set_pdf_info(self, file_path):
        self.doc = fitz.open(file_path)
        if self.doc.needsPass:  # check password protection
            # self.decrypt_doc()
            pass
        if self.doc.isEncrypted:  # quit if we cannot decrpt
            # self.Destroy()
            pass
            return
        page_no = 1
        self.fit_page(page_no)

    def fit_page(self, page_no):
        pixmap = self.show_image(page_no)
        width = self.label_pdf.width()
        height = self.label_pdf.height()
        fit_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label_pdf.setPixmap(fit_pixmap)
        self.label_pdf.setAlignment(Qt.AlignCenter)
        self.label_pdf.setFocus()

    def show_image(self, pno):
        page_no = int(pno) - 1
        self.dl_array = [0] * len(self.doc)
        if self.dl_array[page_no] == 0:
            self.dl_array[page_no] = self.doc[page_no].getDisplayList()
        dl = self.dl_array[page_no]
        zoom = int(100)
        rotate = int(0)
        trans = fitz.Matrix(zoom / 100.0, zoom / 100.0).preRotate(rotate)
        pix = dl.getPixmap(matrix=trans, alpha=False)
        fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
        qt_image = QImage(pix.samples, pix.width, pix.height, pix.stride, fmt)
        pixmap = QPixmap()
        pixmap.convertFromImage(qt_image)
        return pixmap

    def wheelEvent(self, event):
        print('wheelEvent() captured.')
        # if event.modifiers():  # & Qt.ControlModifier:
        if self.label_pdf.hasFocus():
            print('ok')
            self.on_mouse_wheel(event)

        else:
            super().wheelEvent(event)

    def on_mouse_wheel(self, evt):
        # process wheel as paging operations
        d = evt.angleDelta().y()  # int indicating direction
        if d < 0:
            self.next_page(evt)
        elif d > 0:
            self.pre_page(evt)
        return

    def next_page(self, event):  # means: page forward
        page = self.current_page + 1  # current page + 1
        page = min(page, self.doc.pageCount)  # cannot go beyond last page
        # self.TextToPage.Value = str(page)  # put target page# in screen
        # self.NeuesImage(page)  # refresh the layout
        self.current_page = page
        self.fit_page(page)
        # event.Skip()

    def pre_page(self, event):  # means: page back
        page = self.current_page - 1  # current page - 1
        page = max(page, 1)  # cannot go before page 1
        # self.TextToPage.Value = str(page)  # put target page# in screen
        # self.NeuesImage(page)
        self.current_page = page
        self.fit_page(page)
        # event.Skip()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWin()
    main_win.show()
    # window系统提供的模式
    # model = QDirModel()
    # model = QFileSystemModel()
    # model.setRootPath((QDir.rootPath()))
    # # 创建一个QTreeView()控件
    # tree = QTreeView()
    # # 为控件添加模式。
    # tree.setModel(model)
    # tree.setWindowTitle("QTreeView例子")
    # tree.resize(640, 480)
    # tree.show()

    sys.exit(app.exec_())
