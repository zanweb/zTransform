import sys
from collections import deque

from PyQt5 import QtGui, QtWidgets


class Window(QtWidgets.QWidget):
    def __init__(self, data):
        super(Window, self).__init__()
        self.tree = QtWidgets.QTreeView(self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.tree)
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Name', 'dbID'])
        self.tree.header().setDefaultSectionSize(180)
        self.tree.setModel(self.model)
        self.importData(data)
        self.tree.expandAll()

    def importData(self, data, root=None):
        self.model.setRowCount(0)
        if root is None:
            root = self.model.invisibleRootItem()
        seen = {}
        values = deque(data)
        while values:
            value = values.popleft()
            if value['level'] == 0:
                parent = root
            else:
                pid = value['parent_ID']
                if pid not in seen:
                    values.append(value)
                    continue
                parent = seen[pid]
            dbid = value['dbID']
            parent.appendRow([
                QtGui.QStandardItem(value['short_name']),
                QtGui.QStandardItem(str(dbid)),
            ])
            seen[dbid] = parent.child(parent.rowCount() - 1)


if __name__ == '__main__':
    data = [
        {'level': 0, 'dbID': 77, 'parent_ID': 6, 'short_name': '0:0:0:<new> to 6', 'long_name': '', 'order': 1,
         'pos': 0},
        {'level': 1, 'dbID': 88, 'parent_ID': 77, 'short_name': '1:1:1:Store13', 'long_name': '', 'order': 2, 'pos': 1},
        {'level': 0, 'dbID': 442, 'parent_ID': 6, 'short_name': '2:<new>', 'long_name': '', 'order': 1, 'pos': 2},
        {'level': 1, 'dbID': 522, 'parent_ID': 442, 'short_name': '3:<new>', 'long_name': '', 'order': 2, 'pos': 3},
        {'level': 2, 'dbID': 171, 'parent_ID': 522, 'short_name': '3:<new>', 'long_name': '', 'order': 1, 'pos': 3},
        {'level': 0, 'dbID': 456, 'parent_ID': 6, 'short_name': '4:<new>', 'long_name': '', 'order': 1, 'pos': 4},
        {'level': 1, 'dbID': 523, 'parent_ID': 456, 'short_name': '5:<new>', 'long_name': '', 'order': 3, 'pos': 5}
    ]

    app = QtWidgets.QApplication(sys.argv)
    window = Window(data)
    window.setGeometry(600, 50, 400, 250)
    window.show()
    sys.exit(app.exec_())
