# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import datetime
import time


class User():
    """
    用户类，包含用户名和用户权限
    @attribute name: 用户名
    @attribute authority: 用户权限，只能是r、w和x三者的组合
                        权限r: 可读权限，默认每个用户都有，可以读取文件目录
                        权限w: 可写权限，可以读、增、删、改文件，不可执行文件
                        权限x: 可执行权限，除拥有上述权限外还可执行文件
    """

    def __init__(self, name, authority):
        """
        用传入的参数初始化用户实例
        @param name: 用于初始化用户名
        @param authority: 用于初始化用户权限
        """
        self.name = name
        self.authority = authority


class FCB():
    """
    文件控制块，存储文件/文件夹的相关信息
    @attribute user: 当前操作用户，User对象
    @attribute parent: 父级目录对象，根节点无父级目录，Folder对象
    @attribute name: 当前文件/文件夹对象的名称，字符串
    @attribute author: 当前文件/文件夹对象的拥有者，字符串
    @attribute date: 当前文件/文件夹对象的最后修改时间，字符串
    @attribute path: 从根节点至当前文件/文件夹对象的路径，字符串
    @method get_config: 获取当前路径下的配置文件config.txt
    @method update_config: 更新当前路径下的配置文件config.txt
    @method rename: 重命名当前对象的name
    @method back: 获取父目录的文件列表
    """

    def __init__(self, user, parent, name, author, date):
        """
        初始化文件控制块
        @param user: 用于初始化当前操作用户，User对象
        @param parent: 用于初始化父级目录对象，根节点无父级目录，Folder对象
        @param name: 用于初始化当前文件/文件夹对象的名称，字符串
        @param author: 用于初始化当前文件/文件夹对象的拥有者，字符串
        @param date: 用于初始化当前文件/文件夹对象的最后修改时间，字符串
        @param path: 用于初始化从根节点至当前文件/文件夹对象的路径，字符串
        """
        self.user = user
        self.parent = parent  # parent必须是一个文件夹
        self.name = name
        self.author = author
        self.date = date
        self.path = parent.path + parent.name + '/'
    
    def get_config(self, target_path):
        """
        获取目录的配置文件config.txt，内含文件对应的所有者信息
        @param target_path: config.txt的路径
        @returns f_author: 从config.txt中读出的文件拥有者信息，
                存储在字典f_author内，表现为'key-value': '文件名-拥有者'
        """
        f_author = {}
        with open(target_path, 'r') as f:
            line = f.readline()
            while line:
                line_tmp = line.strip('\n').split(' ')
                f_author[line_tmp[0]] = line_tmp[1]
                line = f.readline()
        return f_author

    def update_config(self, f_author):
        """
        更新目录的配置文件config.txt
        @param f_author: 用于更新的数据源，'key-value'为'文件名-拥有者'的字典
        """
        with open(self.path + self.name + '/config.txt', 'w') as f:
            for item in f_author:
                line = item + ' ' + f_author[item] + '\n'
                f.write(line)

    def rename(self, name):
        """
        重命名，并更新config.txt内对应文件的信息
        @param name: 将所选择的文件/文件夹重名为name
        """
        src_path = self.path + self.name
        src_name = self.name
        dst_name = self.path + name
        os.rename(src_path, dst_name)  # 调用系统api进行重命名
        self.name = name
        f_author = {}
        target_path = self.parent.path + self.parent.name + '/config.txt'
        with open(target_path, 'r') as f:
            line = f.readline()
            while line:
                line_tmp = line.strip('\n').split(' ')
                if line_tmp[0] == src_name:
                    f_author[self.name] = line_tmp[1]
                else:
                    f_author[line_tmp[0]] = line_tmp[1]
                line = f.readline()
        with open(target_path, 'w') as f:
            for item in f_author:
                line = item + ' ' + f_author[item] + '\n'
                f.write(line)

    def back(self):
        """
        返回上一级，调用系统api分别获取父级目录的文件夹和文件的列表
        @returns parent_list: 列表，其元素为父级目录的文件夹对象和文件对象
        """
        parent_list = []  # 父级目录的文件列表
        target_path = self.parent.path + self.parent.name + '/config.txt'
        f_author = self.get_config(target_path)  # 获取配置文件
        parent_path = self.parent.path + self.parent.name  # 父级目录路径
        for root, dirs, files in os.walk(parent_path):  
            for i in dirs:
                if self.user.name == f_author[i] or self.user.name == 'root':
                    path = self.parent.path  # 获取最后修改时间
                    t_stamp = os.path.getmtime(path)
                    t_array = time.localtime(t_stamp)
                    t_date = time.strftime('%Y-%m-%d %H:%M:%S', t_array)
                    a = Folder(self.user, self.parent, i, f_author[i], t_date)
                    parent_list.append(a)  # 将文件夹对象加入子节点
            for i in files:
                if self.user.name == f_author[i] or self.user.name == 'root':
                    path = self.parent.path
                    t_stamp = os.path.getmtime(path)
                    t_array = time.localtime(t_stamp)
                    t_date = time.strftime('%Y-%m-%d %H:%M:%S', t_array)
                    a = File(self.user, self.parent, i, f_author[i], t_date)
                    parent_list.append(a)  # 将文件对象加入子节点
            break
        return parent_list


class Folder(FCB):
    """
    文件夹实例，继承FCB，附加部分特性
    @attribute children: 存放文件夹下的文件，列表
    @attribute _type: 文件类型为“文件夹”，字符串
    @method get_children: 获取当前文件夹下的所有子文件
    """

    children = []  # 存放文件夹下的文件
    _type = 'folder'  # 文件类型为“文件夹” 

    def get_children(self):
        """
        获取当前文件夹下的所有子文件
        @returns self.children: 列表，选定的文件夹下的所有子文件，
                                其内元素为文件夹对象和文件对象
        """
        children_path = self.path + self.name
        target_path = children_path + '/config.txt'
        f_author = self.get_config(target_path)
        for root, dirs, files in os.walk(children_path):  
            # 若用户能看到此文件夹，则必为该文件夹的拥有者，因此无需做用户检查
            for i in dirs:
                if self.user.name == f_author[i] or self.user.name == 'root':
                    path = self.path + self.name + '/' + i  # 获取最后修改时间
                    t_stamp = os.path.getmtime(path)
                    t_array = time.localtime(t_stamp)
                    t_date = time.strftime('%Y-%m-%d %H:%M:%S', t_array)
                    a = Folder(self.user, self, i, f_author[i], t_date)
                    self.children.append(a)  # 将文件夹对象加入子节点
            for i in files:
                if self.user.name == f_author[i] or self.user.name == 'root':
                    path = self.path + self.name + '/' + i
                    t_stamp = os.path.getmtime(path)
                    t_array = time.localtime(t_stamp)
                    t_date = time.strftime('%Y-%m-%d %H:%M:%S', t_array)
                    a = File(self.user, self, i, f_author[i], t_date)
                    self.children.append(a)  # 将文件对象加入子节点
            break
        return self.children


class File(FCB):
    """
    文件实例，继承FCB，附加部分特性
    @attribute _type: 文件类型，由文件后缀决定，字符串
    @attribute size: 文件大小，单位为b，整型
    """
    
    def __init__(self, user, parent, name, author, date):
        """
        初始化文件实例
        @param user: 用于初始化当前操作用户，User对象
        @param parent: 用于初始化父级目录对象，根节点无父级目录，Folder对象
        @param name: 用于初始化当前文件/文件夹对象的名称，字符串
        @param author: 用于初始化当前文件/文件夹对象的拥有者，字符串
        @param date: 用于初始化当前文件/文件夹对象的最后修改时间，字符串
        @attribute path: 由父级文件夹路径和父级文件夹名字拼接获取，字符串
        @attribute _type: 文件类型，私有变量，由name的后缀获取，字符串
        @attribute size: 文件大小，单位为b，调用系统api得到，整型
        """
        self.user = user  # 当前用户
        self.parent = parent  # parent必须是一个文件夹
        self.name = name  # 文件名
        self.author = author  # 文件所有者
        self.date = date  # 文件最后修改时间
        self.path = parent.path + parent.name + '/'  # 文件路径
        t = self.name.split('.')
        self._type = t[len(t)-1]  # 文件类型
        self.size = os.path.getsize(self.path + self.name)  # 文件大小


class Root(Folder):
    """
    根节点，继承Folder，附加部分特性
    @method load: 初始化装载，完成对root节点的children的初始化
    """

    def __init__(self, user):
        """
        初始化根节点
        @attribute name: 根节点名字固定为空（即''）
        @attribute _type: 根节点类型为'root'
        @attribute path: 根节点路径固定为'root'
        @attribute children: 根节点的子节点列表初始化为空
        @attribute user: 当前用户user，由控制程序传入
        """
        self.name = ''
        self._type = 'root'
        self.path = 'root'
        self.children = []
        self.user = user
    
    def load(self):
        """
        系统初始化装载
        @returns self.children: 返回根节点的子节点列表，其元素为文件/文件夹对象
        """
        target_path = 'root/config.txt'
        f_author = self.get_config(target_path)
        for root, dirs, files in os.walk('root'):  
            for i in dirs:
                if self.user.name == f_author[i] or self.user.name == 'root':
                    path = self.path + '/' + i  # 获取最后修改时间
                    t_stamp = os.path.getmtime(path)
                    t_array = time.localtime(t_stamp)
                    t_date = time.strftime('%Y-%m-%d %H:%M:%S', t_array)
                    a = Folder(self.user, self, i, f_author[i], t_date)
                    self.children.append(a)  # 将文件夹对象加入子节点
            for i in files:
                if self.user.name == f_author[i] or self.user.name == 'root':
                    path = self.path + '/' + i
                    t_stamp = os.path.getmtime(path)
                    t_array = time.localtime(t_stamp)
                    t_date = time.strftime('%Y-%m-%d %H:%M:%S', t_array)
                    a = File(self.user, self, i, f_author[i], t_date)
                    self.children.append(a)  # 将文件对象加入子节点
            break
        return self.children


class OSManager():
    """
    控制程序
    @attribute user: 正在操作的用户，User实例
    @attribute main_board: 当前显示目录的节点列表，列表
    @attribute here: 当前节点位置，为Root/Folder/File实例对象
    @method ls: 展示当前目录下属于当前用户的所有文件
    @method cd_in: 进入下一级 或 运行目标程序
    @method cd_back: 返回上一级
    @method rename: 重命名，若当前用户有w权限则调用文件/文件夹本身的方法
    @method mkdir_or_touch: 创建文件夹/文件，若当前用户有w权限则调用系统api创建
    @method delete: 删除文件或文件夹，若用户有w权限则调用系统api完成删除
    """

    def __init__(self, user):
        """
        初始化控制程序
        @param user: 正在操作的用户，User实例
        """
        root = Root(user)
        self.user = user
        self.main_board = root.load()
        self.here = root

    def ls(self):
        """
        展示当前目录下属于当前用户的所有文件
        @returns name: 当前目录下文件/文件夹的名字列表
        @returns date: 当前目录下文件/文件夹的最后修改日期列表
        @returns _type: 当前目录下文件/文件夹的类型列表
        @returns size: 当前目录下文件/文件夹的大小列表，文件夹大小为空
        @returns author: 当前目录下文件/文件夹的拥有者列表
        """
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
            
    def cd_in(self, target_name):
        """
        进入下一级 或 运行目标程序
        @returns 2: 成功进入下一级目录
        @returns 1: 成功执行目标程序
        @returns 0: 没有权限执行程序
        """
        for item in self.main_board:
            if item.name == target_name:
                if item._type == 'folder':  # 若为目录，则进入下一级
                    self.here = item
                    self.main_board.clear()
                    self.main_board = item.get_children()
                    return 2
                else:  # 若为可执行程序，则运行程序
                    if 'x' in self.user.authority:
                        target_path = item.path + target_name
                        os.system('start ' + target_path)
                        return 1
                    else:  # 没有权限执行程序
                        return 0
                        
    def cd_back(self):
        """
        返回上一级
        """
        self.main_board.clear()
        self.main_board = self.here.back()
        self.here = self.here.parent

    def rename(self, src_name, dst_name):
        """
        重命名，若当前用户有w权限则调用文件/文件夹本身的方法
        @returns 2: 成功调用自身的rename方法修改名字
        @returns 1: 文件名已存在，修改失败
        @returns 0: 权限不足，修改失败
        """
        # 检查权限
        if 'w' in self.user.authority:
            # 获取文件名列表
            ls_list = []
            for item in self.main_board:
                ls_list.append(item.name)
            # 要求重命名的文件不可与当前文件或文件夹同名
            for item in self.main_board:
                if item.name == src_name:
                    # 若文件名已存在，则拒绝修改
                    if dst_name in ls_list:
                        return 1
                    # 若文件名不存在，则调用自身的rename方法修改
                    else:
                        item.rename(dst_name)
                        return 2
        # 权限不足
        else:
            return 0

    def mkdir_or_touch(self, dir_name, status):
        """
        创建文件夹/文件，若当前用户有w权限则调用系统api创建
        创建的文件/文件夹默认用当前系统时间命名，创建的文件默认为txt文件
        @returns True: 创建成功
        @returns False: 权限不足，创建失败
        """
        if 'w' in self.user.authority:
            # 获取路径
            if status == 2:  # 若为创建文件，默认创建文本文件
                dir_name = dir_name + '.txt'
            target_path = self.here.path + self.here.name + '/' + dir_name
            # 创建
            if status == 2:  # 创建文件
                os.system('type nul>' + target_path)  
                t_stamp = os.path.getmtime(target_path)
                t_array = time.localtime(t_stamp)
                t = time.strftime('%Y-%m-%d %H:%M:%S', t_array)
                a = File(self.user, self.here, dir_name, self.user.name, t)
            elif status ==1:  # 创建文件夹
                os.makedirs(target_path, 0o777)
                t_stamp = os.path.getmtime(target_path)
                t_array = time.localtime(t_stamp)
                t = time.strftime('%Y-%m-%d %H:%M:%S', t_array)
                a = Folder(self.user, self.here, dir_name, self.user.name, t)
            # 将新建文件或文件夹对象加入主界面对象列表
            self.main_board.append(a)
            config_path = self.here.path + self.here.name + '/config.txt'
            f_author = self.here.get_config(config_path)
            f_author[dir_name] = self.user.name
            self.here.update_config(f_author)
            # 为新建的文件夹创建config
            if status == 1:
                with open(target_path + '/config.txt', 'w') as f:
                    f.write('config.txt root')
            return True
        else:
            return False

    def delete(self, src_name, src_type):
        """
        删除文件或文件夹，若用户有w权限则调用系统api完成删除
        @returns 2: 成功删除文件夹
        @returns 1: 成功删除文件
        @returns 0: 权限不足，删除失败
        """
        if 'w' in self.user.authority:
            # 此处斜杠方向需转换
            path = self.here.path.replace('/', '\\') + self.here.name
            print(path)
            # 删除文件夹
            if src_type == 'folder':
                print('rd /s /q ' + path + '\\' + src_name)
                os.system('rd /s /q ' + path + '\\' + src_name)
            # 删除文件
            else:
                os.system('del ' + path + '\\' + src_name)
            # 更新主面板的对象列表
            for item in self.main_board:
                if item.name == src_name:
                    a = item
                    break
            config_path = self.here.path + self.here.name + '/config.txt'
            f_author = self.here.get_config(config_path)
            del f_author[src_name]
            self.here.update_config(f_author)
            self.main_board.remove(a)
            if src_type == 'folder':  # 删除文件夹
                return 2
            else:  # 删除文件
                return 1
        else:  # 无权限
            return 0
         