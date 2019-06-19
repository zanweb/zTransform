from zSplitting_login import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys
import configparser

# from main_window_code import *


class LoginDialog(QtWidgets.QWidget, Ui_Dialog):

    def __init__(self):
        super(LoginDialog, self).__init__()
        self.setupUi(self)

        # buttons = self.button_box.buttons()
        # buttons.accepted.connect(self.accept)
        # buttons.rejected.connect(self.reject)
        # self.pushButton.clicked.connect(self.login_init)
        self.pass_info = []
        self.line_edit_user.setFocus()
        self.line_edit_pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        # self.main_w = MainWindow()

    def accept(self):
        self.login_init()
        self.get_user_info()
        pass

    def reject(self):
        pass

    def login_info(self):
        reply = QMessageBox.information(self,  # 使用infomation信息框
                                        "Login OK",
                                        "You will login the Slitting...",  # + str(self.pass_info),
                                        QMessageBox.Ok)
        return reply

    def login_init(self):
        self.pass_info = []
        # self.pass_info.append(self.comboBox.currentText())
        if self.line_edit_pwd.text() == '' or self.line_edit_user.text() == '':
            QMessageBox.information(self,  # 使用infomation信息框
                                    "Login",
                                    "Please fill the Username and Password...",  # + str(self.pass_info),
                                    QMessageBox.Ok)
            self.line_edit_user.setFocus()
        else:
            self.pass_info.append(self.line_edit_user.text())
            self.pass_info.append(self.line_edit_pwd.text())
            # self.login_info()

            # self.main_w.show()
            self.hide()

    def get_user_info(self):
        cf = configparser.ConfigParser()
        cf.read('config.ini')
        self.pass_info.append(cf.get('DataSource', 'server'))
        self.pass_info.append(cf.get('DataSource', 'database'))
        try:
            import pymssql
            conn = pymssql.connect(host=self.pass_info[2], user=self.pass_info[0], password=self.pass_info[1],
                                   database=self.pass_info[3], as_dict=True)
            conn.close()
            QMessageBox.information(self,
                                    "Login Ok",
                                    "You login the database success! \n Now, welcome to cladding database...",
                                    QMessageBox.Ok)
            self.hide()
        except Exception as e:
            QMessageBox.information(self,
                                    "Login Error",
                                    "Can not Login the Database, \ncheck the network and user account/password!",
                                    QMessageBox.Ok)
            self.show()
        finally:
            return


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    login_show = LoginDialog()
    login_show.show()
    sys.exit(app.exec_())
