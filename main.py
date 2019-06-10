# -*- coding: utf-8 -*-
import os
import datetime
import time

# 文件控制块
class FCB():
    def __init__(self, parent, name, author, date):
        self.parent = parent  # parent必须是一个文件夹
        self.name = name
        self.author = author
        self.date = date
        self.path = parent.path + parent.name + '/'

    def rename(self, name):
        self.name = name


# 文件夹
class Folder(FCB):
    child = []  # 存放文件夹下的文件
    _type = 'folder'  # 文件类型为“文件夹” 

    def get_child(self):
        for root, dirs, files in os.walk(self.path + self.name):  
            for i in dirs:
                path = self.path + i
                time_stamp = os.path.getctime(path)
                time_array = time.localtime(time_stamp)
                a = File(self, i, 'root', time.strftime("%Y-%m-%d %H:%M:%S", time_array))
                self.child.append(a)
            for i in files:
                path = self.path + i
                time_stamp = os.path.getctime(path)
                time_array = time.localtime(time_stamp)
                a = File(self, i, 'root', time.strftime("%Y-%m-%d %H:%M:%S", time_array))
                self.child.append(a)
            break
        return self.child


# 文件
class File(FCB):
    def __init__(self, parent, name, author, date):
            self.parent = parent  # parent必须是一个文件夹
            self.name = name  # 文件名
            self.author = author  # 文件所有者
            self.date = date  # 文件最后修改时间
            self.path = parent.path + parent.name  # 文件路径
            t = self.name.split('.')
            self._type = t[len(t)-1]  # 文件类型
            self.size = os.path.getsize(self.path + self.name)  # 文件大小

    def read(self):
        with open(self.path, 'r') as f:
            print(f.read())
    

# 根节点
class Root():
    def __init__(self):
        self.name = ''
        self.type = 'root'
        self.path = 'root/'
        self.child = []
        
    def load(self):
        for root, dirs, files in os.walk("root"):  
            for i in dirs:
                path = self.path + i
                time_stamp = os.path.getctime(path)
                time_array = time.localtime(time_stamp)
                a = File(self, i, 'root', time.strftime("%Y-%m-%d %H:%M:%S", time_array))
                self.child.append(a)
            for i in files:
                path = self.path + i
                time_stamp = os.path.getctime(path)
                time_array = time.localtime(time_stamp)
                a = File(self, i, 'root', time.strftime("%Y-%m-%d %H:%M:%S", time_array))
                self.child.append(a)
            break
        return self.child


if __name__ == "__main__":
    root = Root()
    main_board = root.load()
    for item in main_board:
        print(item.name, item._type, item.date, item.author, item.size)