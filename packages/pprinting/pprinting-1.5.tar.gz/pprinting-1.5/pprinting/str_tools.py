import copy
import re
from typing import Iterable


def get_sizes(obj: object) -> tuple:
    """ 返回对象双字节长度、单字节长度、折合单字节长度

    双字节字符的正则模板'[^\x00-\xff]+'
    单字节字符的正则模板'[\x00-\xff]+'

    Example:
    >>> get_sizes("abc123,")
    (0, 7, 7)
    >>> get_sizes("abc123你好，")
    (3, 6, 12)
    """

    obj = str(obj)  # 传入的可能不是字符串
    p = re.compile('[^\x00-\xff]+')  # 双字节字符的正则
    double_byte_count = len(''.join(p.findall(obj)))  # p.findall(str)-->返回符合正则对象的子字符串
    single_byte_count = len(obj) - double_byte_count
    return double_byte_count, single_byte_count, double_byte_count * 2 + single_byte_count


def get_max_size(ite: Iterable) -> int:
    """返回可迭代对象元素的最大折合单字节长度
    """
    max_len = 0
    for item in ite:
        item_len = get_sizes(item)[2]
        if item_len > max_len: max_len = item_len
    return max_len


def get_sep(ite: Iterable) -> str:
    """ 根据指定长度获取表格分隔符,可迭代对象元素必须是int类型

    Example：
    >>> get_sep([5, 2])
    '+-----+--+'
    """

    return "".join(["+" + "-" * item for item in ite]) + "+"


def get_body(contents: Iterable, sizes: Iterable = None, layout='c' or 'l' or 'r', cond=None) -> str:
    """ 返回指定内容和长度的表体,若指定长度小于内容真实长度，以..或...结尾来表示

    若缺省sizes,根据contents内容自适应表体长度
    若给定sizes:
        若len(sizes) == len(contents) -->每条内容和指定长度一一匹配
        若len(sizes) < len(contents)  -->缺少的长度信息以l2最后一条为准
        若len(sizes) > len(contents)  -->多余的长度信息忽略掉
        若某条内容长度需要用...显示，且指定长度不足3,会抛出错误

    :param contents: 内容列表[obj]
    :param sizes:    长度列表[int]
    :param layout:   指定布局
    :param cond:     指定条件
    Example:
    >>> get_body(["name", 123345, "迈克尔杰克逊"])
    '|name|123345|迈克尔杰克逊|'
    >>> get_body(["name", 123345, "迈克尔杰克逊"], [8, 5, 8])
    '|  name  |123..|迈克尔..|'
    """

    # 标准化l1->contents, l2->sizes,转化成列表方标使用索引
    l1 = [item for item in contents]
    l2 = copy.deepcopy(sizes)
    if not l2:
        l2 = [get_sizes(item)[2] for item in l1]
    elif len(l2) == len(l1):
        ...
    elif len(l2) < len(l1):
        l2.extend([l2[-1]] * (len(l1) - len(l2)))
    elif len(l2) > len(l1):
        l2 = l2[:len(l1) + 1:]

    # 核心逻辑运算
    body = ""
    for i in range(len(l1)):
        real_len = get_sizes(l1[i])[2]
        content = l1[i]
        assign_len = l2[i]
        if cond: content = cond(content)
        content = str(content)
        if real_len <= assign_len:
            if layout == 'c':
                body += "|" + content.center(l2[i] - get_sizes(l1[i])[0])
            elif layout == 'l':
                body += "|" + content.ljust(l2[i] - get_sizes(l1[i])[0])
            elif layout == 'r':
                body += "|" + content.rjust(l2[i] - get_sizes(l1[i])[0])
        else:
            content_copy = copy.deepcopy(content)
            if assign_len < 3:
                raise Exception(f"内容需要用'...'显示，而指定长度是{assign_len}，它不足以显示'...', 请检查长度信息")
            while True:
                len_ = get_sizes(content_copy)[2]
                if not len_ > assign_len - 2:
                    break
                content_copy = content_copy[:-1:]

            # while (len_ := get_sizes(content_copy)[2]) > assign_len - 2:
            #     content_copy = content_copy[:-1:]  # 可能删除的是双字节长度字符，结束循环后需要再次判断长度
            content_copy += ".."  # ".."提示未显示完全
            len_ += 2
            if len_ < assign_len: content_copy += "."
            body += "|" + content_copy
    body += "|"
    return body


def filter_inputs(s: str, case: callable = str, condition: callable = None):
    """ 根据限制条件获取用户输入，会自动捕获错误并提示重新输入

    :param s: 输入时的提示信息
    :param case: 对input()的字符串进行格式转换
    :param condition: 额外条件
    :return:
    """
    while 1:
        try:
            res = case(input(s))
        except:
            print("输入值有误!")
            continue
        if condition and condition(res) or not condition:
            return res
        else:
            print("输入值超出参数范围!")
            continue
