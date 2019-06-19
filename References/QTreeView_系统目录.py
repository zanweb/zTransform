import sys

from PyQt5.QtWidgets import *

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # window系统提供的模式
    model = QDirModel()
    # 创建一个QTreeView的控件
    tree = QTreeView()
    # 为控件添加模式
    tree.setModel(model)

    tree.setWindowTitle('QTreeView例子')
    tree.resize(640, 480)

    tree.show()
    sys.exit(app.exec_())
