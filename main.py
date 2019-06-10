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

    # 重命名
    def rename(self, name):
        self.name = name
    
    # 返回上一级
    def back(self):
        parent_list = []  # 父级目录的文件列表
        for root, dirs, files in os.walk(self.parent.path + self.parent.name):  
            for i in dirs:
                path = self.parent.path  # 获取最后修改时间
                time_stamp = os.path.getctime(path)
                time_array = time.localtime(time_stamp)
                a = Folder(self.parent, i, self.author, time.strftime("%Y-%m-%d %H:%M:%S", time_array))
                parent_list.append(a)  # 将文件夹对象加入子节点
            for i in files:
                path = self.parent.path
                time_stamp = os.path.getctime(path)
                time_array = time.localtime(time_stamp)
                a = File(self.parent, i, self.author, time.strftime("%Y-%m-%d %H:%M:%S", time_array))
                parent_list.append(a)  # 将文件对象加入子节点
            break
        return parent_list


# 文件夹
class Folder(FCB):
    child = []  # 存放文件夹下的文件
    _type = 'folder'  # 文件类型为“文件夹” 

    def get_child(self):
        for root, dirs, files in os.walk(self.path + self.name):  
            for i in dirs:
                path = self.path + self.name + '/' + i  # 获取最后修改时间
                time_stamp = os.path.getctime(path)
                time_array = time.localtime(time_stamp)
                a = Folder(self, i, self.author, time.strftime("%Y-%m-%d %H:%M:%S", time_array))
                self.child.append(a)  # 将文件夹对象加入子节点
            for i in files:
                path = self.path + self.name + '/' + i
                time_stamp = os.path.getctime(path)
                time_array = time.localtime(time_stamp)
                a = File(self, i, self.author, time.strftime("%Y-%m-%d %H:%M:%S", time_array))
                self.child.append(a)  # 将文件对象加入子节点
            break
        return self.child


# 文件
class File(FCB):
    def __init__(self, parent, name, author, date):
            self.parent = parent  # parent必须是一个文件夹
            self.name = name  # 文件名
            self.author = author  # 文件所有者
            self.date = date  # 文件最后修改时间
            self.path = parent.path + parent.name + '/'  # 文件路径
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
        self.path = 'root'
        self.child = []
    
    # 系统初始化装载
    def load(self):
        for root, dirs, files in os.walk("root"):  
            for i in dirs:
                path = self.path + '/' + i  # 获取最后修改时间
                time_stamp = os.path.getctime(path)
                time_array = time.localtime(time_stamp)
                a = Folder(self, i, 'root', time.strftime("%Y-%m-%d %H:%M:%S", time_array))
                self.child.append(a)  # 将文件夹对象加入子节点
            for i in files:
                path = self.path + '/' + i
                time_stamp = os.path.getctime(path)
                time_array = time.localtime(time_stamp)
                a = File(self, i, 'root', time.strftime("%Y-%m-%d %H:%M:%S", time_array))
                self.child.append(a)  # 将文件对象加入子节点
            break
        return self.child


# 控制程序
class OSManager():
    def __init__(self):
        root = Root()
        self.main_board = root.load()
        self.here = root

    def ls(self):
        print('>>> ls')
        print('当前目录：', self.here.name)
        for item in self.main_board:
            if item._type == 'folder':
                print(item.name, item._type, item.date, item.author, item.path, item.parent.name)
            else:
                print(item.name, item._type, item.date, item.author, item.size, item.path, item.parent.name)

    def cd(self, target_name):
        print('>>> cd ' + target_name)
        for item in self.main_board:
            if item.name == target_name:
                self.here = item
                self.main_board.clear()
                self.main_board = item.get_child()
                break
    
    def cd_(self):
        print('>>> cd ..')
        self.main_board.clear()
        self.main_board = self.here.back()
        self.here = self.here.parent


if __name__ == "__main__":
    disk = OSManager()
    disk.ls()
    disk.cd('测试文件夹1')
    disk.ls()
    disk.cd('内层文件夹1')
    disk.cd('内层文件夹2')
    disk.ls()
    disk.cd_()
    disk.ls()