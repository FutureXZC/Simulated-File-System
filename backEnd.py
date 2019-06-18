# -*- coding: utf-8 -*-
import os
import datetime
import time

# 文件控制块
class FCB():
    def __init__(self, user, parent, name, author, date):
        self.user = user
        self.parent = parent  # parent必须是一个文件夹
        self.name = name
        self.author = author
        self.date = date
        self.path = parent.path + parent.name + '/'
    
    # 获取目录的配置文件config.txt，内含文件对应的所有者信息
    def get_config(self, target_path):
        f_author = {}
        with open(target_path, 'r') as f:
            line = f.readline()
            while line:
                line_tmp = line.strip('\n').split(' ')
                f_author[line_tmp[0]] = line_tmp[1]
                line = f.readline()
        return f_author

    # 更新目录的配置文件config.txt
    def update_config(self, f_author):
        with open(self.path + self.name + '/config.txt', 'w') as f:  # 更新当前目录的config
            for item in f_author:
                line = item + ' ' + f_author[item] + '\n'
                f.write(line)

    # 重命名
    def rename(self, name):
        src_path = self.path + self.name
        src_name = self.name
        dst_name = self.path + name
        os.rename(src_path, dst_name)
        self.name = name
        f_author = {}
        with open(self.parent.path + self.parent.name + '/config.txt', 'r') as f:
            line = f.readline()
            while line:
                line_tmp = line.strip('\n').split(' ')
                if line_tmp[0] == src_name:
                    f_author[self.name] = line_tmp[1]
                else:
                    f_author[line_tmp[0]] = line_tmp[1]
                line = f.readline()
        with open(self.parent.path + self.parent.name + '/config.txt', 'w') as f:
            for item in f_author:
                line = item + ' ' + f_author[item] + '\n'
                f.write(line)
        return True

    # 返回上一级
    def back(self):
        parent_list = []  # 父级目录的文件列表
        target_path = self.parent.path + self.parent.name + '/config.txt'
        f_author = self.get_config(target_path)  # 获取配置文件
        parent_path = self.parent.path + self.parent.name
        for root, dirs, files in os.walk(parent_path):  
            for i in dirs:
                if self.user.name == f_author[i] or self.user.name == 'root':
                    path = self.parent.path  # 获取最后修改时间
                    time_stamp = os.path.getmtime(path)
                    time_array = time.localtime(time_stamp)
                    a = Folder(self.user, self.parent, i, f_author[i], time.strftime('%Y-%m-%d %H:%M:%S', time_array))
                    parent_list.append(a)  # 将文件夹对象加入子节点
            for i in files:
                if self.user.name == f_author[i] or self.user.name == 'root':
                    path = self.parent.path
                    time_stamp = os.path.getmtime(path)
                    time_array = time.localtime(time_stamp)
                    a = File(self.user, self.parent, i, f_author[i], time.strftime('%Y-%m-%d %H:%M:%S', time_array))
                    parent_list.append(a)  # 将文件对象加入子节点
            break
        return parent_list


# 文件夹
class Folder(FCB):
    children = []  # 存放文件夹下的文件
    _type = 'folder'  # 文件类型为“文件夹” 

    # 获取当前文件夹下的所有子文件
    def get_children(self):
        children_path = self.path + self.name
        target_path = children_path + '/config.txt'
        f_author = self.get_config(target_path)
        for root, dirs, files in os.walk(children_path):  
            # 若用户能看到此文件夹，则必为该文件夹的拥有者，因此无需做用户检查
            for i in dirs:
                if self.user.name == f_author[i] or self.user.name == 'root':
                    path = self.path + self.name + '/' + i  # 获取最后修改时间
                    time_stamp = os.path.getmtime(path)
                    time_array = time.localtime(time_stamp)
                    a = Folder(self.user, self, i, f_author[i], time.strftime('%Y-%m-%d %H:%M:%S', time_array))
                    self.children.append(a)  # 将文件夹对象加入子节点
            for i in files:
                if self.user.name == f_author[i] or self.user.name == 'root':
                    path = self.path + self.name + '/' + i
                    time_stamp = os.path.getmtime(path)
                    time_array = time.localtime(time_stamp)
                    a = File(self.user, self, i, f_author[i], time.strftime('%Y-%m-%d %H:%M:%S', time_array))
                    self.children.append(a)  # 将文件对象加入子节点
            break
        return self.children


# 文件
class File(FCB):
    def __init__(self, user, parent, name, author, date):
        self.user = user  # 当前用户
        self.parent = parent  # parent必须是一个文件夹
        self.name = name  # 文件名
        self.author = author  # 文件所有者
        self.date = date  # 文件最后修改时间
        self.path = parent.path + parent.name + '/'  # 文件路径
        t = self.name.split('.')
        self._type = t[len(t)-1]  # 文件类型
        self.size = os.path.getsize(self.path + self.name)  # 文件大小


# 根节点
class Root(FCB):
    def __init__(self, user):
        self.name = ''
        self._type = 'root'
        self.path = 'root'
        self.children = []
        self.user = user
    
    # 系统初始化装载
    def load(self):
        target_path = 'root/config.txt'
        f_author = self.get_config(target_path)
        for root, dirs, files in os.walk('root'):  
            for i in dirs:
                if self.user.name == f_author[i] or self.user.name == 'root':
                    path = self.path + '/' + i  # 获取最后修改时间
                    time_stamp = os.path.getmtime(path)
                    time_array = time.localtime(time_stamp)
                    a = Folder(self.user, self, i, f_author[i], time.strftime('%Y-%m-%d %H:%M:%S', time_array))
                    self.children.append(a)  # 将文件夹对象加入子节点
            for i in files:
                if self.user.name == f_author[i] or self.user.name == 'root':
                    path = self.path + '/' + i
                    time_stamp = os.path.getmtime(path)
                    time_array = time.localtime(time_stamp)
                    a = File(self.user, self, i, f_author[i], time.strftime('%Y-%m-%d %H:%M:%S', time_array))
                    self.children.append(a)  # 将文件对象加入子节点
            break
        return self.children


# 控制程序
class OSManager():
    def __init__(self, user):
        root = Root(user)
        self.user = user
        self.main_board = root.load()
        self.here = root

    # 展示当前目录下属于当前用户的所有文件
    def ls(self):
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
            
    # 进入下一级 或 运行目标程序
    def cd_in(self, target_name):
        for item in self.main_board:
            if item.name == target_name:
                if item._type == 'folder':  # 若为目录，则进入下一级
                    self.here = item
                    self.main_board.clear()
                    self.main_board = item.get_children()
                    return True
                else:  # 若为可执行程序，则运行程序
                    target_path = item.path + target_name
                    os.system('start ' + target_path)
                    return False
    
    # 返回上一级
    def cd_back(self):
        self.main_board.clear()
        self.main_board = self.here.back()
        self.here = self.here.parent

    # 重命名
    def rename(self, src_name, dst_name):
        # 获取文件名列表
        ls_list = []
        for item in self.main_board:
            ls_list.append(item.name)
        # 要求重命名的文件不可与当前文件或文件夹同名
        for item in self.main_board:
            if item.name == src_name:
                # 若文件名已存在，则拒绝修改
                if dst_name in ls_list:
                    return False
                # 若文件名不存在，则调用自身的rename方法修改
                else:
                    item.rename(dst_name)
                    return True

    # 创建文件夹或文件
    def mkdir_or_touch(self, dir_name, status):
        # 获取路径
        if status == 2:
            dir_name = dir_name + '.txt'
            target_path = self.here.path + self.here.name + '/' + dir_name
        elif status ==1:
            target_path = self.here.path + self.here.name + '/' + dir_name
        print(target_path)
        # 创建
        if status == 2:  # 创建文件
            os.system('type nul>' + target_path)  
            time_stamp = os.path.getmtime(target_path)  # 获取当前时间作为新文件名
            time_array = time.localtime(time_stamp)
            a = File(self.user, self.here, dir_name, self.user.name, time.strftime('%Y-%m-%d %H:%M:%S', time_array))
        elif status ==1:  # 创建文件夹
            os.makedirs(target_path, 0o777)
            time_stamp = os.path.getmtime(target_path)  # 获取当前时间作为文件夹名称
            time_array = time.localtime(time_stamp)
            a = Folder(self.user, self.here, dir_name, self.user.name, time.strftime('%Y-%m-%d %H:%M:%S', time_array))
        # 将新建文件或文件夹对象加入主界面对象列表
        self.main_board.append(a)
        f_author = self.here.get_config(self.here.path + self.here.name + '/config.txt')  # 更新当前目录的config
        f_author[dir_name] = self.user.name
        self.here.update_config(f_author)
        if status == 1:
            with open(target_path + '/config.txt', 'w') as f:  # 为新建的文件夹创建config
                f.write('config.txt root')

    # 删除文件或文件夹
    def delete(self, src_name, src_type):
        # 已经确保能看见的文件均属于自己了，而root无视拥有者，因此无需做拥有者的检查，只需检查权限
        if 'w' in self.user.authority or 'x' in self.user.authority:
            path = self.here.path.replace('/', '\\') + self.here.name  # 此处斜杠方向需转换
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
            f_author = self.here.get_config(self.here.path + self.here.name + '/config.txt')
            del f_author[src_name]
            self.here.update_config(f_author)
            self.main_board.remove(a)
            if src_type == 'folder':  # 删除文件夹
                return 2
            else:  # 删除文件
                return 1
        else:  # 无权限
            return 0


# 用户类，包含用户名和用户权限
class User():
    def __init__(self, name, authority):
        self.name = name
        self.authority = authority
    def login(self):
        pass
        
