# coding:utf-8

###################################
# run with python 3.6 with pyqt5! #
###################################
import sys
import os
import configparser  # 读写ini
import logging

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
# import ui
from ui.ui_main_drop import Ui_Dialog
from ui.drop_area import DropArea
from clib.call_c_lib import get_file_info

logging.basicConfig(
    level=logging.DEBUG,  # 控制台打印的日志级别
    filename='filecopy.log',
    filemode='a',  # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
    # a是追加模式，默认如果不写的话，就是追加模式
    format='%(asctime)s  [%(message)s]'
    # 日志格式
)


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)

        # setup UI
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # 添加文件拖拽区
        self.drop_area = DropArea(self)
        self.ui.verticalLayout_drop.addWidget(self.drop_area)  # 添加drop区到layout
        self.drop_area.dropped.connect(self.handle_drop)  # 注册droped信号的响应函数

        # 读取配置文件
        self.cf = configparser.ConfigParser()
        self.cf.read("config.ini")
        val = self.cf.get("baseconfig", "save_path")
        self.ui.le_save_path.setText(val)

        # 绑定按键
        self.ui.pb_path_browser.clicked.connect(self.open_dir)  # 绑定浏览按钮
        self.ui.pb_exec.clicked.connect(self.exec_copy)

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
        dir_path = QFileDialog.getExistingDirectory(self, "选择文件保存路径",
                                                    "./")  # 选择目录
        self.ui.le_save_path.setText(dir_path)
        # 保存的路径写入到ini文件, 下次软件启动时自动恢复
        self.cf.set("baseconfig", "save_path", dir_path)
        self.cf.write(open("config.ini", "w"))

    def exec_copy(self):
        # check
        src = self.ui.le_filepath.text()
        dst_dir = self.ui.le_save_path.text()
        dst = os.path.join(dst_dir,
                           'file_{}'.format(self.ui.le_filename.text()))
        if not os.path.exists(src):
            self.ui.le_info.setText("源文件不存在")
            return
        if not os.path.exists(dst_dir):
            self.ui.le_info.setText("目标文件夹不存在")
            return
        if not os.access(dst_dir, os.W_OK):
            self.ui.le_info.setText("目标不可写")
            return
        os.system('cp {} {}'.format(src, dst))
        logging.info("src: {}, dst: {}, crc: {}, len: {}".format(
            src, dst, self.ui.le_crc.text(), self.ui.le_file_len.text()))
        self.ui.le_info.setText("复制成功")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())
