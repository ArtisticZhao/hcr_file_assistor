# coding: utf-8
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from urllib.parse import unquote  # 解决中文路径


class DropArea(QLabel):
    dropped = pyqtSignal(list)

    def __init__(self, parent=None):
        super(DropArea, self).__init__(parent=parent)
        self.setAcceptDrops(True)
        self.setText('拖拽文件到此')
        self.setStyleSheet("border:2px solid gray; background-color: lightgray; ")
        self.setMinimumSize(230, 230)
        self.setAlignment(Qt.AlignCenter)

    def dragEnterEvent(self, QDragEnterEvent):
        QDragEnterEvent.acceptProposedAction()  # 没有这句会导致dropEvent不响应

    def dropEvent(self, QDropEvent):
        txt_path = QDropEvent.mimeData().text().replace('file:///', '/')  # 替换掉文件开头
        # print(unquote(txt_path))  # 解决中文路径问题
        list_of_files = list(filter(None, unquote(txt_path).split('\r\n')))  # 以\r\n进行字符串分割,得到文件列表
        self.dropped.emit(list_of_files)  # 发送列表
