import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class TreeWidget(QMainWindow):
    myControls = {}

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle('TreeWidget')
        self.tree = QTreeWidget()
        self.myControls['tree'] = self.tree
        self.tree.setColumnCount(2)  # 说明是树形的表，
        self.tree.setHeaderLabels(['Key', 'Value'])  # 是表，则有表头
        # 根节点的父是 QTreeWidget对象
        root = QTreeWidgetItem(self.tree)

        root.setText(0, 'root')
        child1 = QTreeWidgetItem(root)  # 指出父结点
        child1.setText(0, 'child1')
        child1.setText(1, 'name1')
        child2 = QTreeWidgetItem(root)
        child2.setText(0, 'child2')
        child2.setText(1, 'name2')
        child3 = QTreeWidgetItem(root)
        child3.setText(0, 'child3')
        child4 = QTreeWidgetItem(child3)
        child4.setText(0, 'child4')
        child4.setText(1, 'name4')
        # 以下两句是主窗口的设置
        self.tree.addTopLevelItem(root)
        self.setCentralWidget(self.tree)

        # 带图标是这形式QAction(QIcon("ss.png"), "add", self)
        addAction = QAction("增加", self)
        addAction.triggered.connect(self.on_addAction_triggered)

        editAction = QAction("修改", self)
        editAction.triggered.connect(self.on_editdAction_triggered)

        deleteAction = QAction("删除", self)
        deleteAction.triggered.connect(self.on_deleteAction_triggered)

        findAction = QAction("查找", self)
        findAction.triggered.connect(self.on_findAction_triggered)

        toolbar = self.addToolBar("aa")
        toolbar.addAction(addAction)
        toolbar.addAction(editAction)
        toolbar.addAction(deleteAction)
        toolbar.addAction(findAction)

    def on_addAction_triggered(self):
        currNode = self.tree.currentItem()
        addChild1 = QTreeWidgetItem()
        addChild1.setText(0, 'addChild1_key')
        addChild1.setText(1, 'addChild1_val')
        currNode.addChild(addChild1)

    def on_editdAction_triggered(self):
        currNode = self.tree.currentItem()
        currNode.setText(0, 'editkey')
        currNode.setText(1, 'editvalue')

    def on_deleteAction_triggered(self):
        currNode = self.tree.currentItem()
        parent1 = currNode.parent();
        parent1.removeChild(currNode)

    def on_findAction_triggered(self):
        # MatchRegExp 正则查找，MatchRecursive递归遍历，最后是指树表的第几列值
        # 本例是 查找第0中 所有开头含有”child“文字的节点
        nodes = self.tree.findItems("^child[\w|\W]*", Qt.MatchRegExp | Qt.MatchRecursive, 0)
        for node in nodes:
            QMessageBox.information(self, '', node.text(0))


app = QApplication(sys.argv)
tp = TreeWidget()
tp.show()
app.exec_()
