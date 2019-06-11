# -*- coding: utf-8 -*-
import os
import datetime
import time
import tkinter


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
        f_author = {}
        parent_path = self.parent.path + self.parent.name
        with open(parent_path + '/config.txt', 'r') as f:
            line = f.readline()
            while line:
                line_tmp = line.strip('\n').split(' ')
                f_author[line_tmp[0]] = line_tmp[1]
                line = f.readline()
        for root, dirs, files in os.walk(parent_path):  
            for i in dirs:
                if self.author == f_author[i] or self.author == 'root':
                    path = self.parent.path  # 获取最后修改时间
                    time_stamp = os.path.getmtime(path)
                    time_array = time.localtime(time_stamp)
                    a = Folder(self.parent, i, f_author[i], time.strftime('%Y-%m-%d %H:%M:%S', time_array))
                    parent_list.append(a)  # 将文件夹对象加入子节点
            for i in files:
                if self.author == f_author[i] or self.author == 'root':
                    path = self.parent.path
                    time_stamp = os.path.getmtime(path)
                    time_array = time.localtime(time_stamp)
                    a = File(self.parent, i, f_author[i], time.strftime('%Y-%m-%d %H:%M:%S', time_array))
                    parent_list.append(a)  # 将文件对象加入子节点
            break
        return parent_list


# 文件夹
class Folder(FCB):
    children = []  # 存放文件夹下的文件
    _type = 'folder'  # 文件类型为“文件夹” 

    # 获取当前文件夹下的所有子文件
    def get_children(self):
        for root, dirs, files in os.walk(self.path + self.name):  
            # 若用户能看到此文件夹，则必为该文件夹的拥有者，因此无需做用户检查
            for i in dirs:
                path = self.path + self.name + '/' + i  # 获取最后修改时间
                time_stamp = os.path.getmtime(path)
                time_array = time.localtime(time_stamp)
                a = Folder(self, i, self.author, time.strftime('%Y-%m-%d %H:%M:%S', time_array))
                self.children.append(a)  # 将文件夹对象加入子节点
            for i in files:
                path = self.path + self.name + '/' + i
                time_stamp = os.path.getmtime(path)
                time_array = time.localtime(time_stamp)
                a = File(self, i, self.author, time.strftime('%Y-%m-%d %H:%M:%S', time_array))
                self.children.append(a)  # 将文件对象加入子节点
            break
        return self.children


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

    # def read(self):
    #     with open(self.path, 'r') as f:
    #         print(f.read())
    

# 根节点
class Root():
    def __init__(self, author):
        self.name = ''
        self.type = 'root'
        self.path = 'root'
        self.children = []
        self.author = author
    
    # 系统初始化装载
    def load(self):
        f_author = {}
        with open('root/config.txt', 'r') as f:
            line = f.readline()
            while line:
                line_tmp = line.strip('\n').split(' ')
                f_author[line_tmp[0]] = line_tmp[1]
                line = f.readline()
        for root, dirs, files in os.walk('root'):  
            for i in dirs:
                if self.author == f_author[i] or self.author == 'root':
                    path = self.path + '/' + i  # 获取最后修改时间
                    time_stamp = os.path.getmtime(path)
                    time_array = time.localtime(time_stamp)
                    a = Folder(self, i, f_author[i], time.strftime('%Y-%m-%d %H:%M:%S', time_array))
                    self.children.append(a)  # 将文件夹对象加入子节点
            for i in files:
                if self.author == f_author[i] or self.author == 'root':
                    path = self.path + '/' + i
                    time_stamp = os.path.getmtime(path)
                    time_array = time.localtime(time_stamp)
                    a = File(self, i, f_author[i], time.strftime('%Y-%m-%d %H:%M:%S', time_array))
                    self.children.append(a)  # 将文件对象加入子节点
            break
        return self.children


# 控制程序
class OSManager():
    def __init__(self, user):
        root = Root(user.name)
        self.user = user
        self.main_board = root.load()
        self.here = root
        self.cd_in('测试文件夹1')

    # 展示当前目录下属于当前用户的所有文件
    def ls(self):
        print('>>> ls')
        print('当前目录：', self.here.name)
        name = []
        date = []
        _type = []
        size = []
        author = []
        for item in self.main_board:
            if self.user.name == item.author or self.user.name == 'root':
                name.append(item.name)
                date.append(item.date)
                author.append(item.author)
                if item._type == 'folder':
                    _type.append('folder')
                    size.append('')
                else:
                    _type.append(item._type)
                    size.append(item.size)
        return name, date, _type, size, author
                
            
    # 进入下一级
    def cd_in(self, target_name):
        print('>>> cd ' + target_name)
        for item in self.main_board:
            if item.name == target_name:
                self.here = item
                self.main_board.clear()
                self.main_board = item.get_children()
                break
    
    # 返回上一级
    def cd_back(self):
        print('>>> cd ..')
        self.main_board.clear()
        self.main_board = self.here.back()
        self.here = self.here.parent

    # def mkdir(self, dir_name):
    #     print('>>> mkdir' + dir_name)


# 用户类，包含用户名和用户权限
class User():
    def __init__(self, name, authority):
        self.name = name
        self.authority = authority
