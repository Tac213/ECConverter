# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

node_id = 0


def gen_id():
    global node_id
    node_id += 1
    return node_id


class ExcelListNode(object):
    """
    Excel列表一个节点的数据
    """

    def __init__(self, path, parent=None):
        """
        构造器
        Args:
            path: [str]Excel相对路径
            parent: [ExcelListNode]父节点
        """
        self.path = path
        self.parent = parent
        self.node_id = gen_id()
        self.children = []

    def add_child(self, child):
        """
        增加子节点
        尾插
        Args:
            child: ExcelListNode
        Returns:
            None
        """
        child.parent = self
        self.children.append(child)

    def insert_child(self, index, child):
        """
        在某个索引值上插入子节点
        Args
            index: int
            child: ExcelListNode
        Returns:
            None
        """
        child.parent = self
        self.children.insert(index, child)

    def remove_child(self, index):
        """
        移除某个索引值上的子节点
        Args
            index: int
        Returns:
            None
        """
        del self.children[index]

    def children_count(self):
        """
        子节点个数
        Returns:
            int
        """
        return len(self.children)

    def row(self):
        """
        获取节点所在行的索引值
        如果是根节点则返回-1
        Returns:
            int
        """
        if not self.parent:
            return -1
        return self.parent.children.index(self)

    def clear_children(self):
        """
        移除所有子节点
        Returns:
            None
        """
        self.children.clear()

    def serialize(self):
        """
        序列化
        Returns:
            dict
        """
        data = {
            'path': self.path,
            'children': [],
        }
        for child in self.children:
            data['children'].append(child.serialize())
        return data
