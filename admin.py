# !/usr/bin/env python
# -*- coding: UTF-8 -*-
import re


class Admin():
    """
    管理员操作，包括登录和对用户信息的增删改查
    @attribute user_info: 存储用户信息，字典，format: {用户名:[密码，权限]}
    @method login: 登录验证，返回登录成功与否的结果
    @method update_user_info_file: 更新用户数据文件user_info.txt
    @method new_user: 创建一个新用户
    @method del_user: 删除一个已有用户
    @method edit_user: 修改一个现有用户的密码和权限，不可重命名
    @method view: 查看现有用户的详细信息
    """

    user_info = {}

    def __init__(self):
        """
        获取user_info.txt文件，初始化用户信息字典user_info
        """
        with open('user_info.txt', 'r') as f:
            line = f.readline()
            while line:
                line_tmp = line.strip('\n').split(' ')
                self.user_info[line_tmp[0]] = [line_tmp[1], line_tmp[2]]
                line = f.readline()
    
    def login(self):
        """
        实现管理员的登录验证
        @returns True: 验证通过，登录成功，可以进行后续操作
        @returns False: 验证失败，登录失败，不可以进行后续操作
        """
        root = input('管理员账号：')
        pwd = input('管理员密码：')
        if root == 'root' and pwd == self.user_info[root][0]:
            print('登录成功。')
            return True
        else:
            print('管理员账号或密码错误！按任意键退出程序。')
            return False

    def update_user_info_file(self):
        """
        使用用户信息字典user_info更新user_info.txt文件
        """
        with open('user_info.txt', 'w') as f:
            info = self.user_info
            for item in info:
                f.write(item + ' ' + info[item][0] + ' ' +info[item][1] + '\n')

    def new_user(self):
        """
        创建一个新用户，新用户不可与现有的用户重名
        """
        name = input('请输入要创建的用户名：')
        if not name in self.user_info:
            pwd = input('请设置登录密码：')
            authority = input('请设置用户权限：')
            obj = re.match(r'[rwx]+$', authority)
            if obj:
                s = set(authority)
                authority = ''.join(s)
                self.user_info[name] = [pwd, authority]
                self.update_user_info_file()
                print('创建成功。')
            else:
                print('创建失败，用户权限只能为‘rwx’的组合。')
        else:
            print('创建失败，用户名已存在。')
    
    def del_user(self):
        """
        删除一个现有用户
        """
        name = input('请输入要删除的用户名称：')
        if name in self.user_info:
            del self.user_info[name]
            self.update_user_info_file()
            print('删除成功。')
        else:
            print('删除失败，不存在该用户。')

    def edit_user(self):
        """
        修改一个现有用户的信息，只能更改密码和权限，不可重命名
        """
        name = input('请输入要修改信息的用户：')
        if name in self.user_info:
            pwd = input('请输入该用户的新密码：')
            authority = input('请输入该用户的新权限：')
            obj = re.match(r'[rwx]+$', authority)
            if obj:
                s = set(authority)
                authority = ''.join(s)
                self.user_info[name] = [pwd, authority]
                self.update_user_info_file()
                print('修改成功。')
            else:
                print('修改失败，用户权限只能为‘rwx’的组合。')
        else:
            print('不存在该用户。')

    def view(self):
        """
        查看现有用户的详细信息
        """
        print('用户名\t密码\t权限')
        info = self.user_info
        for item in info:
            print(item + '\t' + info[item][0] + '\t' + info[item][1])
    

if __name__ == "__main__":
    root = Admin()
    if root.login():
        switch = {
            'view': root.view,
            'new': root.new_user,
            'del': root.del_user,
            'edit': root.edit_user
        }
        print('命令集：')
        print('new-新建用户 del-删除用户 ')
        print('edit-修改用户信息 view-查看现有用户的详细信息')
        print('quit-退出')
        command = input('请输入操作命令：')
        while not command == 'quit':
            if command in switch:
                switch[command]()
            else:
                print('命令有误！请按命令集内容输入正确的命令！')
            command = input('请输入操作命令：')
