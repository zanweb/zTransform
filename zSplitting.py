# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zSplitting.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_zSplitting(object):
    def setupUi(self, zSplitting):
        zSplitting.setObjectName("zSplitting")
        zSplitting.resize(1121, 803)
        self.centralwidget = QtWidgets.QWidget(zSplitting)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 80, 1111, 571))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tree_widget = QtWidgets.QTreeWidget(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree_widget.sizePolicy().hasHeightForWidth())
        self.tree_widget.setSizePolicy(sizePolicy)
        self.tree_widget.setMinimumSize(QtCore.QSize(800, 0))
        self.tree_widget.setBaseSize(QtCore.QSize(500, 0))
        self.tree_widget.setObjectName("tree_widget")
        self.tree_widget.headerItem().setText(0, "1")
        self.horizontalLayout.addWidget(self.tree_widget)
        self.tree_view = QtWidgets.QTreeView(self.horizontalLayoutWidget)
        self.tree_view.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree_view.sizePolicy().hasHeightForWidth())
        self.tree_view.setSizePolicy(sizePolicy)
        self.tree_view.setObjectName("tree_view")
        self.horizontalLayout.addWidget(self.tree_view)
        self.push_button_load = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_load.setGeometry(QtCore.QRect(50, 690, 75, 23))
        self.push_button_load.setObjectName("push_button_load")
        self.push_button_get = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_get.setGeometry(QtCore.QRect(170, 690, 75, 23))
        self.push_button_get.setObjectName("push_button_get")
        self.group_box_org = QtWidgets.QGroupBox(self.centralwidget)
        self.group_box_org.setGeometry(QtCore.QRect(10, 10, 271, 61))
        self.group_box_org.setObjectName("group_box_org")
        self.check_box_sjg = QtWidgets.QCheckBox(self.group_box_org)
        self.check_box_sjg.setGeometry(QtCore.QRect(20, 30, 71, 16))
        self.check_box_sjg.setObjectName("check_box_sjg")
        self.check_box_lkq = QtWidgets.QCheckBox(self.group_box_org)
        self.check_box_lkq.setGeometry(QtCore.QRect(140, 30, 71, 16))
        self.check_box_lkq.setObjectName("check_box_lkq")
        self.group_box_catlog = QtWidgets.QGroupBox(self.centralwidget)
        self.group_box_catlog.setGeometry(QtCore.QRect(280, 10, 251, 61))
        self.group_box_catlog.setObjectName("group_box_catlog")
        self.radio_button_zees = QtWidgets.QRadioButton(self.group_box_catlog)
        self.radio_button_zees.setGeometry(QtCore.QRect(10, 30, 89, 16))
        self.radio_button_zees.setObjectName("radio_button_zees")
        self.radio_button_cees = QtWidgets.QRadioButton(self.group_box_catlog)
        self.radio_button_cees.setGeometry(QtCore.QRect(90, 30, 89, 16))
        self.radio_button_cees.setObjectName("radio_button_cees")
        self.radio_button_trim = QtWidgets.QRadioButton(self.group_box_catlog)
        self.radio_button_trim.setGeometry(QtCore.QRect(170, 30, 89, 16))
        self.radio_button_trim.setObjectName("radio_button_trim")
        self.combo_box_workcenter = QtWidgets.QComboBox(self.centralwidget)
        self.combo_box_workcenter.setGeometry(QtCore.QRect(630, 30, 201, 22))
        self.combo_box_workcenter.setObjectName("combo_box_workcenter")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(550, 30, 71, 20))
        self.label.setObjectName("label")
        self.push_button_transform = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_transform.setGeometry(QtCore.QRect(280, 690, 75, 23))
        self.push_button_transform.setObjectName("push_button_transform")
        zSplitting.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(zSplitting)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1121, 23))
        self.menubar.setObjectName("menubar")
        zSplitting.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(zSplitting)
        self.statusbar.setObjectName("statusbar")
        zSplitting.setStatusBar(self.statusbar)
        self.tool_bar = QtWidgets.QToolBar(zSplitting)
        self.tool_bar.setObjectName("tool_bar")
        zSplitting.addToolBar(QtCore.Qt.TopToolBarArea, self.tool_bar)

        self.retranslateUi(zSplitting)
        QtCore.QMetaObject.connectSlotsByName(zSplitting)

    def retranslateUi(self, zSplitting):
        _translate = QtCore.QCoreApplication.translate
        zSplitting.setWindowTitle(_translate("zSplitting", "MainWindow"))
        self.push_button_load.setText(_translate("zSplitting", "加载数据"))
        self.push_button_get.setText(_translate("zSplitting", "获取数据"))
        self.group_box_org.setTitle(_translate("zSplitting", "ORG"))
        self.check_box_sjg.setText(_translate("zSplitting", "SJG"))
        self.check_box_lkq.setText(_translate("zSplitting", "LKQ"))
        self.group_box_catlog.setTitle(_translate("zSplitting", "Catlog"))
        self.radio_button_zees.setText(_translate("zSplitting", "Zees"))
        self.radio_button_cees.setText(_translate("zSplitting", "Cees"))
        self.radio_button_trim.setText(_translate("zSplitting", "Trim"))
        self.label.setText(_translate("zSplitting", "WorkCenter:"))
        self.push_button_transform.setText(_translate("zSplitting", "转换数据"))
        self.tool_bar.setWindowTitle(_translate("zSplitting", "toolBar"))

