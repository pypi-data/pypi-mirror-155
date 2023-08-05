import os
import time
# 作者：  Gris
# 日期：  2021/12/2
# 时间：  22:35
# py版本: 3.10

"""
    要求：
        编写一个程序，循环写入日志（my.log）。每2秒写写入一行，要求写入每一行都要显示出来
        程序结束后（强行结束），重写运行时继续往下写，序号衔接
    格式：
        1. 2020-12-28 18:18:22 
"""

def get_last_number(target_file):
    """ 寻找log文件上一次结束的序号，格式必须是 n.xxx，n是一个整数

    :param target_file: 目标文件，必须提前以ab+或wb+方式打开过的
    :return:
    """

    if target_file.tell() == 0: return 1

    while 1:  # 否则寻找上一次结束的序号
        try:
            target_file.seek(-2, 1)
        except OSError:
            return 2  # 若打开前只有一行，则便偏移量会越界抛出错误
        byte_ = target_file.read(1)
        if byte_ != b"\n": continue  # 寻找上上一次的b"\n"
        return int(target_file.read().split(b".")[0]) + 1


def write_log(target_file, content="", head=0, hastime=True, sleep_time=0):
    """ 无情的写log机器，若连续写建议手动提供head信息，以节省资源

    :param target_file: 目标文件，必须提前以ab+或wb+方式打开过的
    :param content:  要写入的内容，字符串
    :param head:  要写入的首部信息，格式:"n."，若未定义，则自动搜寻上一次结束的序号
    :param hastime: 存入的log自带时间标记
    :param sleep_time: 写入时定义阻塞时间
    """

    num = head if head else 1 if target_file.tell() == 0 else get_last_number(target_file)
    if hastime:
        log_line = str(num) + "." + '"' + content + '"'
    else:
        log_line = str(num) + "." + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '"' + content + '"'
    target_file.write(log_line.encode() + b"\n")
    time.sleep(sleep_time)


def __test():
    # 被写入log的文件名,不存在则创建,存在则接着写log
    file_name = "./test.log"
    # 写log的死循环
    with open(file_name, "ab+") as f:
        for i in range(5):
            write_log(target_file=f, sleep_time=2)
        for i in range(6, 10):
            write_log(target_file=f, head=i, sleep_time=2)
    # 检查是否是按照规定格式写的
    with open(file_name, "rt") as f:
        for i in range(1, 10):
            line = f.readline()
            if line.startswith(str(i) + "."):
                continue
            else:
                print("test module write_log failed..., please check the code")
                break
        else:
            print("test module write_log succeed, you can use it now!")
    os.remove("./test.log")


# --------------------------------test---------------------------------------
if __name__ == "__main__":
   __test()
