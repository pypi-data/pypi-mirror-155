import sys
from types import MappingProxyType
from typing import Sequence
from .str_tools import *


class ListDictToTab:

    def __init__(self, seq, tab_title, index_title, content_title, isVertical, cell_layout, width_limit, file, extra_dict):
        self.__seq = seq
        self.__tab_title = tab_title
        self.__index_title = index_title
        self.__content_title = content_title
        self.__isVertical = isVertical
        self.__cell_layout = cell_layout
        self.__width_limit = width_limit
        self.__file = file
        self.__extra_dict = extra_dict  # 方便移植源代码
        self.__tab = ""

    def printOut(self):
        self.__tab = self.__get_tab()
        print(self.__tab, file=self.__file)

    def __get_tab(self):
        if self.__isVertical:
            return self.__get_vertical()
        else:
            return self.__get_horizontal()

    def __get_vertical(self):
        """
        +------------------------+------+--- --+
        | 属性                   | 简写 |默认值|
        +------------------------+------+------+
        | self.__tab_title       |i     |  ""  |
        +------------------------+------+------+
        | self.__index_title     |j     |  ""  |
        +------------------------+------+------+
        | self.__content_title   |k     |  ""  |
        +------------------------+------+------+

        +-----+-----+-----+-----+-----+-----+-----+-----+-----+
        |  i  |  0  |  0  |  0  |  0  |login|login|login|login|
        +-----+-----+-----+-----+-----+-----+-----+-----+-----+
        |  j  |  0  |login|  0  |login|  0  |login|  0  |login|
        +-----+-----+-----+-----+-----+-----+-----+-----+-----+
        |  k  |  0  |  0  |login|login|  0  |  0  |login|login|
        +-----+-----+-----+-----+-----+-----+-----+-----+-----+
        |CASE |  A  |  X  |  A  |  B  |  A  |  X  |  X  |  C  |
        +-----+-----+-----+-----+-----+-----+-----+-----+-----+

        CASE A:
        +---------+
        |   ...   |
        +---------+
        |   ...   |
        +---------+
            ...

        CASE B:
        +---------+---------+
        |   ...   |   ...   |
        +---------+---------+
        |   ...   |   ...   |
        +---------+---------+
            ...       ...

        CASE C
        +---------+---------+
        |        ...        |
        +---------+---------+
        |   ...   |   ...   |
        +---------+---------+
        |   ...   |   ...   |
        +---------+---------+
            ...       ...
        """

        i, j, k, l, m = self.__tab_title, self.__index_title, self.__content_title, self.__seq, self.__extra_dict

        # 根据上图，先将奇奇怪怪的组合默认归类到ABC类：
        if not i and j and not k:
            k = self.__content_title = "内容(default name)"
        elif i and j and not k:
            k = self.__content_title = "内容(default name)"
        elif i and not j and k:
            j = self.__index_title = "索引(default name)"

        if m:
            if not k: k = self.__content_title = "内容(default name)"
            if not j: j = self.__index_title = "索引(default name)"

        # 最后根据上图，进行形状分类:
        if i and j and k:
            return self.__vertical_C()
        elif not i and j and k:
            return self.__vertical_B()
        else:
            return self.__vertical_A()

    def __get_horizontal(self):
        """
        +------------------------+------+--- --+
        | 属性                   | 简写 |默认值|
        +------------------------+------+------+
        | self.__tab_title       |i     |  ""  |
        +------------------------+------+------+
        | self.__index_title     |j     |  ""  |
        +------------------------+------+------+
        | self.__content_title   |k     |  ""  |
        +------------------------+------+------+

        +-----+-----+-----+-----+-----+-----+-----+-----+-----+
        |  i  |  0  |  0  |  0  |  0  |  1  |  1  |  1  |  1  |
        +-----+-----+-----+-----+-----+-----+-----+-----+-----+
        |  j  |  0  |  1  |  0  |  1  |  0  |  1  |  0  |  1  |
        +-----+-----+-----+-----+-----+-----+-----+-----+-----+
        |  k  |  0  |  0  |  1  |  1  |  0  |  0  |  1  |  1  |
        +-----+-----+-----+-----+-----+-----+-----+-----+-----+
        |CASE |  A  |  X  |  A  |  B  |  A  |  X  |  X  |  C  |
        +-----+-----+-----+-----+-----+-----+-----+-----+-----+

        CASE A:
        +---------+---------+
        |   ...   |   ...   |   ...
        +---------+---------+

        CASE B:
        +---------+---------+
        |   ...   |   ...   |   ...
        +---------+---------+
        |   ...   |   ...   |   ...
        +---------+---------+

        CASE C
        +-------+---------+---------+
        |       |   ...   |   ...   |   ...
        |  ...  +---------+---------+
        |       |   ...   |   ...   |   ...
        +-------+---------+---------+
        """
        i, j, k, l, m = self.__tab_title, self.__index_title, self.__content_title, self.__seq, self.__extra_dict

        # 根据上图，先将奇奇怪怪的组合默认归类到ABC类：
        if not i and j and not k:
            k = self.__content_title = "元素(default_name)"
        elif i and j and not k:
            k = self.__content_title = "元素(default_name)"
        elif i and not j and k:
            j = self.__index_title = "索引(default_name)"

        if m:
            if not k: k = self.__content_title = "元素(default_name)"
            if not j: j = self.__index_title = "索引(default_name)"

        # 最后根据上图，进行形状分类:
        if i and j and k:
            return self.__horizontal_C()
        elif not i and j and k:
            return self.__horizontal_B()
        else:
            return self.__horizontal_A()

    def __vertical_A(self):
        """ shape is:
                    +---------+
                    |   ...   |
                    +---------+
                    |   ...   |
                    +---------+
                        ...
            case is:
                     +-----+-----+-----+-----+
                     |  i  |  0  |  0  |  login  |
                     +-----+-----+-----+-----+
                     |  j  |  0  |  0  |  0  |
                     +-----+-----+-----+-----+
                     |  k  |  0  |  login  |  0  |
                     +-----+-----+-----+-----+
                     |CASE |  A1 |  A2 |  A3 |
                     +-----+-----+-----+-----+
        """

        def case_a1():
            if self.__width_limit:
                width = self.__width_limit
            else:
                width = get_max_size(self.__seq)
            tab = ""
            sep = get_sep([width])
            tab += sep
            for item in self.__seq:
                body = get_body([item], [width], self.__cell_layout)
                tab += "\n" + body + "\n" + sep
            return tab

        def case_a2():
            if self.__width_limit:
                width = max(self.__width_limit, get_sizes(self.__content_title)[2])
            else:
                width = max(get_max_size(self.__seq), get_sizes(self.__content_title)[2])
            tab = ""
            sep = get_sep([width])
            head = get_body([self.__content_title], [width], self.__cell_layout)
            tab += sep + "\n" + head + "\n" + sep
            for item in self.__seq:
                body = get_body([item], [width], self.__cell_layout)
                tab += "\n" + body + "\n" + sep
            return tab

        def case_a3():
            if self.__width_limit:
                width = max(self.__width_limit, get_sizes(self.__tab_title)[2])
            else:
                width = max(get_max_size(self.__seq), get_sizes(self.__tab_title)[2])
            tab = ""
            sep = get_sep([width])
            head = get_body([self.__tab_title], [width], self.__cell_layout)
            tab += sep + "\n" + head + "\n" + sep
            for item in self.__seq:
                body = get_body([item], [width], self.__cell_layout)
                tab += "\n" + body + "\n" + sep
            return tab

        # CASE A1
        if not (self.__tab_title or self.__index_title or self.__content_title):
            return case_a1()

        # CASE A2
        elif self.__content_title and not (self.__tab_title or self.__index_title):
            return case_a2()

        # CASE A3
        elif self.__tab_title and not (self.__index_title or self.__content_title):
            return case_a3()

    def __vertical_B(self):
        """ shape as:
                    +---------+---------+
                    |   ...   |   ...   |
                    +---------+---------+
                    |   ...   |   ...   |
                    +---------+---------+
                        ...       ...
            case is:
                    +-----+-----+
                    |  i  |  0  |
                    +-----+-----+
                    |  j  |  login  |
                    +-----+-----+
                    |  k  |  login  |
                    +-----+-----+
                    |CASE |  B  |
                    +-----+-----+
               """

        width1 = max(get_sizes(self.__index_title)[2], get_max_size(self.__extra_dict.keys()),
                     get_sizes(str(len(self.__seq)))[2])

        if self.__width_limit:  # 设置宽度仅对元素有效，且优先级低于标题
            width2 = max(self.__width_limit, get_sizes(self.__content_title)[2])
        else:  # 自适应长度
            width2 = max(get_max_size(self.__seq), get_max_size(self.__extra_dict.values()),
                         get_sizes(self.__content_title)[2])
        i = 1
        sep = get_sep([width1, width2])
        tab = sep + "\n" + get_body([self.__index_title, self.__content_title], [width1, width2],
                                    layout=self.__cell_layout) + "\n" + sep
        for item in self.__seq:
            tab += "\n" + get_body([i, item], [width1, width2], layout=self.__cell_layout) + "\n" + sep
            i += 1
        for k, v in self.__extra_dict.items():
            tab += "\n" + get_body([k, v], [width1, width2], layout=self.__cell_layout) + "\n" + sep
        return tab

    def __vertical_C(self):
        """ shape is:
                    +---------+---------+
                    |        ...        |
                    +---------+---------+
                    |   ...   |   ...   |
                    +---------+---------+
                    |   ...   |   ...   |
                    +---------+---------+
                        ...       ...
            ase is:
                    +-----+-----+
                    |  i  |  login  |
                    +-----+-----+
                    |  j  |  login  |
                    +-----+-----+
                    |  k  |  login  |
                    +-----+-----+
                    |CASE |  C  |
                    +-----+-----+
        """
        width1 = max(get_sizes(self.__index_title)[2], get_max_size(self.__extra_dict.keys()),
                     get_sizes(str(len(self.__seq)))[2])

        if self.__width_limit:  # 设置宽度仅对元素有效，且优先级低于标题
            width2 = max(self.__width_limit, get_sizes(self.__content_title)[2])
        else:  # 自适应长度
            width2 = max(get_max_size(self.__seq), get_max_size(self.__extra_dict.values()),
                         get_sizes(self.__content_title)[2])

        diff = get_sizes(self.__tab_title)[2] - (width1 + width2)
        if diff > 0:
            width2 += diff - 1
        # if (diff := get_sizes(self.__tab_title)[2] - (width1 + width2)) > 0:
        #     width2 += diff - 1

        sep1 = get_sep([width1 + width2 + 1])  # 第一个分隔符不一样，中间少一个"+"
        sep = get_sep([width1, width2])
        hair = get_body([self.__tab_title], [width1 + width2 + 1], layout=self.__cell_layout)
        head = get_body([self.__index_title, self.__content_title], [width1, width2], layout=self.__cell_layout)
        tab = sep1 + "\n" + hair + "\n" + sep + "\n" + head + "\n" + sep

        i = 1
        for item in self.__seq:
            tab += "\n" + get_body([i, item], [width1, width2], layout=self.__cell_layout) + "\n" + sep
            i += 1
        for k, v in self.__extra_dict.items():
            tab += "\n" + get_body([k, v], [width1, width2], layout=self.__cell_layout) + "\n" + sep
        return tab

    def __horizontal_A(self):
        """
            shape is:
                +---------+---------+
                |   ...   |   ...   |   ...
                +---------+---------+
            case is:
                +-----+-----+-----+-----+
                |  i  |  0  |  0  |  login  |
                +-----+-----+-----+-----+
                |  j  |  0  |  0  |  0  |
                +-----+-----+-----+-----+
                |  k  |  0  |  login  |  0  |
                +-----+-----+-----+-----+
                |CASE |  A1 |  A2 |  A3 |
                +-----+-----+-----+-----+
            flow is:
                到这里时，limit==0或limit>3,self.__seq是一个序列，self.__extra_dict为空

                CASE A1: i = j = k = 0
                CASE A2: i = j = 0, k = login
                CASE A3: i = login, j = k = 0
        """
        if self.__width_limit == 0:
            widths: list = [get_max_size([self.__content_title, self.__tab_title])] + [get_sizes(item)[2] for item in
                                                                                       self.__seq]
        else:
            widths: list = [get_max_size([self.__content_title, self.__tab_title])] + [self.__width_limit] * len(
                self.__seq)
        widths = widths if widths[0] != 0 else widths[1::]  # 可能一个标题也没有,则删除第一个0元素
        sep: str = get_sep(widths)
        body_contents = [max(self.__tab_title, self.__content_title)] if (
                self.__content_title or self.__tab_title) else []
        body_contents.extend(self.__seq)
        body = get_body(body_contents, widths, layout=self.__cell_layout)

        return sep + "\n" + body + "\n" + sep

    def __horizontal_B(self):
        """
         shape is:
             +---------+---------+
             |   ...   |   ...   |   ...
             +---------+---------+
             |   ...   |   ...   |   ...
             +---------+---------+
         case is:
             +-----+-----+
             |  i  |  0  |
             +-----+-----+
             |  j  |  login  |
             +-----+-----+
             |  k  |  login  |
             +-----+-----+
             |CASE |  B  |
             +-----+-----+
         flow is:
             到这里时，limit==0或limit>3,self.__seq不确定，self.__extra_dict不确定，但至少有一个是True
                """
        # 第一列宽度 = max(标题名长度, 索引名长度)
        widths = [get_max_size([self.__content_title, self.__index_title])]

        # 将获取宽度和内容放在一起，代码变复杂，但仅遍历一次数据-->效能提高
        contents_line1 = [self.__index_title]
        contents_line2 = [self.__content_title]

        contents_line1.extend(range(1, len(self.__seq) + 1))
        contents_line1.extend(self.__extra_dict.keys())
        contents_line2.extend(self.__seq)
        contents_line2.extend(self.__extra_dict.values())

        if self.__width_limit:  # 如果设置内容宽度限制
            widths += [self.__width_limit] * (len(self.__seq) + len(self.__extra_dict))
        else:  # 未设置宽度 -->自适应宽度
            i = 1
            for item in self.__seq:  # 用遍历迭代方式写更具有通用性
                widths += [max(len(str(i)), get_sizes(item)[2])]
                i += 1
            for k, v in self.__extra_dict.items():
                widths += [max(get_sizes(k)[2], get_sizes(v)[2])]
        sep = get_sep(widths)
        body_line1 = get_body(contents_line1, widths, layout=self.__cell_layout)
        body_line2 = get_body(contents_line2, widths, layout=self.__cell_layout)

        return sep + "\n" + body_line1 + "\n" + sep + "\n" + body_line2 + "\n" + sep

    def __horizontal_C(self):
        """ shape is:
                     +--------------------   ...
                     |            tab_title
                     +----------------+--------+
                     |  index_title   |   login    |   ...
                     +----------------+--------+
                     | contents_title |   e1   |   ...
                     +----------------+--------+
             ase is:
                     +-----+-----+
                     |  i  |  login  |
                     +-----+-----+
                     |  j  |  login  |
                     +-----+-----+
                     |  k  |  login  |
                     +-----+-----+
                     |CASE |  C  |
                     +-----+-----+
               """
        if self.__width_limit:
            # 顶层宽度 == 第一列宽度 + login + (限制宽度 + login) * 值的个数 - login == 第一列宽度 + (限制宽度 + login) * 值的个数
            width_top = get_max_size([self.__content_title, self.__index_title]) + (self.__width_limit + 1) * (
                    len(self.__seq) + len(self.__extra_dict))
            sep = get_sep([width_top])
            body_top = get_body([self.__tab_title], [width_top])  # 顶层内容强制居中
            button = self.__horizontal_B()
            return sep + "\n" + body_top + "\n" + button
        else:
            button = self.__horizontal_B()
            sep_old = button.split("\n", 1)[0]
            sep = "+" + "-" * (len(sep_old) - 2) + "+"
            width_top = len(sep) - 2
            body_top = get_body([self.__tab_title], [width_top])  # 顶层内容强制居中
            return sep + "\n" + body_top + "\n" + button


class Matrix2D:
    def __init__(self, seq2D, width, layout, isMatrix, file, cond):
        self.__seq2D = seq2D
        self.__width_limit = width
        self.__layout = layout
        self.__isMatrix = isMatrix
        self.__file = file
        self.__tab = ""
        self.__cond = cond

    def printOut(self):
        self.__tab = self.__getTable()
        print(self.__tab, file=self.__file)

    def __getTable(self):

        # 获取子序列最大宽度
        max_len = max([len(item) for item in self.__seq2D])

        # 当不设置宽度限制-->自适应宽度
        if not self.__width_limit:
            tab = ""
            # 求解自适应的宽度[int]
            widths_temp = []
            for item in self.__seq2D:
                item_widths = [len(str(value)) for value in item]
                if len(item_widths) < max_len: item_widths.extend([3] * (max_len - len(item_widths)))
                widths_temp.append(item_widths)
            widths = []
            for item in zip(*widths_temp):
                widths.append(max(item))  # 获取到自适应宽度

            # 当结果以矩阵状呈现时
            if self.__isMatrix:  # 结果应是矩阵形状
                tab = sep = get_sep(widths)
                for item in self.__seq2D:
                    if len(item) < max_len:
                        item_copy = [value for value in item]  # 手动深拷贝成列表,因为可能是一个元组之类的不可变对象
                        item_copy += [" "] * (max_len - len(item))
                        body = get_body(item_copy, widths, layout=self.__layout, cond=self.__cond)
                    else:
                        body = get_body(item, widths, layout=self.__layout, cond=self.__cond)
                    tab += "\n" + body + "\n" + sep
                return tab

            # 当结果是自适应每行列数时，每行可能有长有短
            else:
                widths_old = []
                widths_last = None
                for item in self.__seq2D:
                    widths_new = widths[:len(item)]
                    if len(widths_new) > len(widths_old):
                        sep = get_sep(widths_new)
                    else:
                        sep = get_sep(widths_old)
                    body = get_body(item, widths_new, layout=self.__layout, cond=self.__cond)
                    tab += sep + "\n" + body + "\n"
                    widths_last = widths_new
                    widths_old = widths_new
                tab += get_sep(widths_last)
                return tab

        # 当设置宽度限制-->每列宽度是一致的
        else:
            tab = ""
            if self.__isMatrix:  # 限制宽度，且为矩阵形状
                tab = sep = get_sep([self.__width_limit] * max_len)
                for item in self.__seq2D:
                    if len(item) < max_len:
                        item_copy = [value for value in item]  # 手动深拷贝成列表
                        item_copy += [" "] * (max_len - len(item))
                        body = get_body(item_copy, [self.__width_limit], layout=self.__layout, cond=self.__cond)
                    else:
                        body = get_body(item, [self.__width_limit], layout=self.__layout, cond=self.__cond)
                    tab += "\n" + body + "\n" + sep
                return tab

            # self.__general_layout == "a":    # 限制宽度，但是子列表长度不一时，不补充较短的部分
            else:
                widths_old = []
                widths_last = None
                for item in self.__seq2D:
                    widths_new = len(item) * [self.__width_limit]
                    if len(widths_new) > len(widths_old):
                        sep = get_sep(widths_new)
                    else:
                        sep = get_sep(widths_old)
                    body = get_body(item, widths_new, layout=self.__layout, cond=self.__cond)
                    tab += sep + "\n" + body + "\n"
                    widths_last = widths_new
                    widths_old = widths_new
                tab += get_sep(widths_last)
                return tab

class IteContainDict:
    def __init__(self, ite, tab_title, index_title, content_title, layout, width, file, con):
        self.__ite = ite
        self.__tab_title = tab_title
        self.__index_title = index_title
        self.__content_title = content_title
        self.__cell_layout = layout
        self.__width_limit = width
        self.__file = file
        self.__tab = ""
        self.__con = con

    def printOut(self):
        self.__tab = self.__getTable()
        print(self.__tab, file=self.__file)

    def __getTable(self):
        # 将对象转化成字典
        if not len(self.__ite):
            return
        if isinstance(self.__ite[0], dict):     # [{}]
            pass
        else:
            self.__ite = [item.__dict__ for item in self.__ite]

        # 获取对象属性key_list，所有对象属性以第一个对象属性为基准
        key_list = None
        for item in self.__ite:
            key_list = [key for key in item.keys()]
            break

        # 第一列宽度
        width1 = get_max_size([self.__index_title, str(len(self.__ite))])   # 根据table_title可能会调整

        # 如果未设置宽度限制-->自适应每列宽度
        if not self.__width_limit:
            widths_contents = [get_sizes(key)[2] for key in key_list]  # 只是键的，值的长度一般会更大
            for i in range(len(key_list)):
                for item in self.__ite:
                    size = get_sizes(item.get(key_list[i]))[2]
                    widths_contents[i] = max(widths_contents[i], size)

        # 如果设置了宽度限制
        else:
            widths_contents = [self.__width_limit] * len(key_list)

        i, j = self.__tab_title, self.__index_title

        tab = ""
        if not (i or j):
            return self.__noti_notj(key_list, widths_contents)
        elif i and not j:
            return self.__i_notj(key_list, tab, widths_contents)
        elif not i and j:
            return self.__noti_andj(key_list, tab, width1, widths_contents)
        else:   # i and j
            diff = get_sizes(self.__tab_title)[2] - width1 - sum(widths_contents) - len(key_list)
            if diff > 0:
                width1 += diff
            total_width = [width1 + sum(widths_contents) + len(key_list)]
            sep1 = get_sep(total_width)
            hair = get_body([self.__tab_title], total_width, self.__cell_layout)
            head = get_body([self.__index_title] + key_list, [width1] + widths_contents, layout=self.__cell_layout)
            sep = get_sep([width1] + widths_contents)
            tab += sep1 + "\n" + hair + "\n" + sep + "\n" + head + "\n" + sep
            x = 1
            for item in self.__ite:
                item = self.__con(item) if self.__con else item  # 增加外部控制打印内容
                content = [x]
                x += 1
                for i in range(len(key_list)):
                    content.append(item.get(key_list[i], "null"))
                body = get_body(content, [width1] + widths_contents, layout=self.__cell_layout)
                tab += "\n" + body + "\n" + sep
            return tab

    def __noti_andj(self, key_list, tab, width1, widths_contents):
        sep = get_sep([width1] + widths_contents)
        head = get_body([self.__index_title] + key_list, [width1] + widths_contents, layout=self.__cell_layout)
        tab += sep + "\n" + head + "\n" + sep
        x = 1
        for item in self.__ite:
            item = self.__con(item) if self.__con else item  # 增加外部控制打印内容
            content = [x]
            x += 1
            for i in range(len(key_list)):
                content.append(item.get(key_list[i], "null"))
            body = get_body(content, [width1] + widths_contents, layout=self.__cell_layout)
            tab += "\n" + body + "\n" + sep
        return tab

    def __i_notj(self, key_list, tab, widths_contents):
        sep = get_sep([sum(widths_contents) + len(key_list) -1])
        content1 = get_body([self.__tab_title], [sum(widths_contents) + len(key_list) -1], layout=self.__cell_layout)
        tab += sep + "\n" + content1 + "\n"
        tab_button = self.__noti_notj(key_list, widths_contents)
        tab += tab_button
        return tab

    def __noti_notj(self, key_list, widths_contents):
        tab = ""
        sep = get_sep(widths_contents)
        hair = get_body(key_list, widths_contents, layout=self.__cell_layout)
        tab += sep + "\n" + hair + "\n" + sep
        for item in self.__ite:
            item = self.__con(item) if self.__con else item  # 增加外部控制打印内容
            content = []
            for i in range(len(key_list)):
                content.append(item.get(key_list[i], "null"))
            body = get_body(content, widths_contents, layout=self.__cell_layout)
            tab += "\n" + body + "\n" + sep
        return tab

# ------------------------------入口1---------------------------------
def printList(seq: Sequence,
              # tab_title="主标题(default name)",
              # index_title="索引(default name)",
              # content_title="内容(default name)",
              tab_title="Items",
              index_title="Index",
              content_title="Value",
              width=0,
              isVertical=True or False,
              layout='c' or 'l' or 'r',
              file=sys.stdout,
              ) ->None:
    """
        以二维列表形状打印列表

    :param seq: 一维序列
    :param tab_title: 表格标题
    :param index_title: 索引标题
    :param content_title: 内容标题
    :param width: 自定义宽度，若不写，默认自适应宽度
    :param isVertical: 是否转置
    :param layout: 单元格布局
    :param file: 指定写入的对象,同print()中的file
    :return:None
    """
    if not isinstance(seq, Sequence): raise Exception(f"传入数据类型错误，期望传入Sequence类，实际传入了{type(seq)}")
    if layout not in ('c', 'l', 'r'): raise Exception(f"传入参数错误，期望传入'c' or 'l' or 'r'，实际传入了{layout}")
    if width != 0 and width < 3: width = 3
    ListDictToTab(seq=seq,
                  file=file,
                  extra_dict={},
                  width_limit=width,
                  cell_layout=layout,
                  tab_title=tab_title,
                  isVertical=isVertical,
                  index_title=index_title,
                  content_title=content_title,
                  ).printOut()

# ------------------------------入口2---------------------------------
def printDict(dic,
              # tab_title="主标题(default name)",
              # key_title="键(default name)",
              # value_title="值(default name)",
              tab_title="Items",
              key_title="Key",
              value_title="Value",
              width=0,
              layout='c' or 'l' or 'r',
              file=sys.stdout,
              isVertical=True,
              ):
    if not isinstance(dic, dict): raise Exception(f"传入数据类型错误，期望传入dict类，实际传入了{type(dic)}")
    if layout not in ('c', 'l', 'r'): raise Exception(f"传入参数错误，期望传入'c' or 'l' or 'r'，实际传入了{layout}")
    if width != 0 and width < 3: width = 3
    ListDictToTab(seq=[],
                  file=file,
                  extra_dict=dic,
                  isVertical=isVertical,
                  width_limit=width,
                  cell_layout=layout,
                  tab_title=tab_title,
                  index_title=key_title,
                  content_title=value_title,
                  ).printOut()

# ------------------------------入口3---------------------------------
def printMatrix(seq: Sequence,
                width=0,
                layout='c' or 'l' or 'r',
                isRectangle=True,
                file=sys.stdout,
                cond=None
                ) ->None:
    """
        以矩阵形状打印二维序列

    :param seq:二维序列
    :param width:每列宽度
    :param layout:单元格布局
    :param isRectangle:每行列数相等还是自适应列数
    :param file:输出目标，同print 的file参数
    :param cond:客制化显示结果,如 lambda x: x**2
    """

    if not isinstance(seq, Sequence): raise Exception(f"传入数据类型错误，期望传入dict类，实际传入了{type(seq)}")
    step = len(seq)//100 + 1
    for i in range(0, len(seq), step):
        if not isinstance(seq[i], Sequence): raise Exception(f"传入数据类型错误，期望传入Sequence类，实际传入了{type(seq[i])}")
    if width != 0 and width < 3: width = 3
    Matrix2D(seq2D=seq,
             width=width,
             layout=layout,
             isMatrix=isRectangle,
             file=file,
             cond=cond
             ).printOut()

# ------------------------------入口4---------------------------------
def printObjects(seq: Sequence,
                 tab_title="Objects",
                 index_title="Attribute",
                 content_title="Value",
                 layout='c' or 'l' or 'r',
                 width=0,
                 file=sys.stdout,
                 con=None):  # 额外限制条件
    """
                  :param seq: 包含自定义对象的序列，如[{}]
                  :param tab_title: 表格主标题,为空字符串时不显示主标题
                  :param index_title: 索引标题,为空字符串时不显示主标题
                  :param content_title: 内容标题,为空字符串时不显示主标题
                  :param layout: 单元格布局
                  :param width: 单元格宽度
                  :param file: 指定写入的对象,同print()中的file
                  :param con: 输出时的限制条件(仅对内容起作用)
                  :return:None
                  """

    if not seq: raise Exception(f'传入了空Sequence{seq}')
    if not isinstance(seq, Sequence): raise Exception(f"传入数据类型错误，期望传入Sequence类，实际传入了{type(seq)}")
    if width != 0 and width < 3: width = 3
    IteContainDict(ite=seq,
                   tab_title=tab_title,
                   index_title=index_title,
                   content_title=content_title,
                   layout=layout,
                   width=width,
                   file=file,
                   con=con
                   ).printOut()
