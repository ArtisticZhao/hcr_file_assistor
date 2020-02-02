# coding:utf-8

###################################
# run with python 3.6 with pyqt5! #
###################################
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
# import ui
from ui.ui_main_drop import Ui_Dialog


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)

        # setup UI
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.te_drop_area.textChanged.connect(self.editchange)  # 响应变更事件
        self.ui.pb_path_browser.clicked.connect(self.open_file)    # 绑定浏览按钮

    def editchange(self):
        '''
        文件拖拽区变更事件
        '''
        if 0 == self.ui.te_drop_area.toPlainText().find('file:///'):
            self.ui.te_drop_area.setText(
                self.ui.te_drop_area.toPlainText().replace('file:///', '/'))

    def open_file(self):
        file_path = QFileDialog.getExistingDirectory(
            self, "选取文件夹", "./")  # 选择目录

        print('savepath: {}'.format(file_path))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())
