import os

# author:               Gris
# Email:                1572990942@qq.com
# datetime:             2021/12/19 下午5:00
# system:               Archlinux
# Interpreter version:  3.9.9
# Pgm Version:          V1.0


""" INTRODUCTION
    获取制定文件夹大小,单位M
"""


def get_dir_size(dir_):
    """
    :param dir_:    目标文件夹
    :return:        文件夹大小，单位M(非占用空间)
    """
    size = 0
    for root, dirs, files in os.walk(dir_):
        size += sum([os.path.getsize(os.path.join(root, file_)) for file_ in files])
    return size / 1024 / 1024


if __name__ == "__main__":
    print(get_dir_size("."))
    pass
