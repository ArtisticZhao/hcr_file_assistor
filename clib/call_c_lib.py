# coding: utf-8
import os
from ctypes import cdll, c_char_p, pointer, c_uint32


def get_file_info(path):
    if os.path.exists(path):
        # 文件存在
        libc = cdll.LoadLibrary("clib/lib_crc.so")  # 加载动态库
        py_crc = c_uint32(0)  # 文件校验值
        f_len = c_uint32(0)   # 文件长度
        libc.get_crc_len(c_char_p(bytes(path, 'utf8')), pointer(py_crc), pointer(f_len))
        return (py_crc.value,  f_len.value)

    else:
        return "FILE NOT EXISTS!"
