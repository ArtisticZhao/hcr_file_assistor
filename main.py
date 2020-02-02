# coding:utf-8

###################################
# run with python 3.6 with pyqt5! #
###################################
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
# import ui
from ui.ui_main_drop import Ui_Dialog
from ui.drop_area import DropArea
from clib.call_c_lib import get_file_info


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)

        # setup UI
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # 添加文件拖拽区
        self.drop_area = DropArea(self)
        self.ui.verticalLayout_drop.addWidget(self.drop_area)  # 添加drop区到layout
        self.drop_area.dropped.connect(self.handle_drop)       # 注册droped信号的响应函数
        self.ui.pb_path_browser.clicked.connect(self.open_dir)    # 绑定浏览按钮

    def handle_drop(self, list_of_files):
        '''
        droped 信号的响应函数, 用于文件拖拽后的后续处理
        '''
        if len(list_of_files) > 1:
            self.ui.le_info.setText("拖入多个文件, 默认只去一个处理")

        res = get_file_info(list_of_files[0])  # 取得文件信息
        self.ui.le_filepath.setText(list_of_files[0])
        if isinstance(res, str):
            # 文件不存在
            self.ui.le_info.setText(res)
        else:
            self.ui.le_crc.setText(hex(res[0]))
            self.ui.le_file_len.setText("{}".format(res[1]))

    def open_dir(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择文件保存路径", "./")  # 选择目录
        self.ui.le_save_path.setText(dir_path)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())
