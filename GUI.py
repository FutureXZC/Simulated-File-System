# !/usr/bin/env python
# -*- coding: UTF-8 -*-
from tkinter import ttk
from tkinter import *
from backEnd import *
import datetime


class MainWindow():
    """
    文件管理系统的主窗体(GUI)，
    显示当前用户、当前文件路径、当前路径下的文件及文件详细信息，
    提供双击鼠标左键打开文件夹或运行程序、单击鼠标右键重命名文件功能，
    提供可以新建或删除文件或文件夹的按钮，实现在模拟文件系统中的增删改查，
    实现针对不同用户不同权限的可视化操作。
    本类的所有方法均调用后端OSManager的方法
    @method get_win: 获取当前窗体实例
    @method ls: 展示当前目录下属于当前用户的所有文件
    @method cd_in: 双击鼠标左键 - 进入下一级 或 运行目标程序
    @method ca_back: 点击返回按钮 - 返回上一级
    @method refresh: 刷新当前文件列表
    @method mkdir: 新建文件夹，默认文件名为当前系统时间
    @method touch: 创建新文件，默认创建文本文件，文件名为当前系统时间
    @method f_delete: 删除文件，向后端传入选中的对象，
                    然后根据后端返回的状态码判断操作完成与否并输出
    @method rename: 单击鼠标右键，重命名文件或文件夹
    @method show: 绑定表格上的事件，运行窗口
    """

    def __init__(self, user):
        """
        初始化函数，生成窗体及相关元素
        """
        # 获取后台信息
        self.disk = OSManager(user)
        # 生成窗体
        self.win = Tk()
        self.win.title('模拟文件系统')
        self.win.geometry('800x350')
        self.win.resizable(width=False, height=False)
        ft = ('Microsoft YaHei', 10)  # 全局字体
        # 顶部label
        self.l_user = Label(self.win, text = self.disk.here.user.name, 
                        bg = 'Plum', font = ft)
        self.l_now = Label(self.win, text = '当前目录：', 
                        bg = 'Lavender', font = ft)
        self.l_dir_text = StringVar()  # 动态更新当前路径
        self.l_dir_text.set(self.disk.here.path + self.disk.here.name)
        self.l_dir = Label(self.win, textvariable = self.l_dir_text, 
                        bg = 'LightCyan', font = ft, width = 90, anchor = 'w')
        # 操作按钮
        self.ctrl = Frame(self.win)  # 控制面板，用于布局
        self.back = Button(self.ctrl, text = '<--',
                        font = ft, command = self.cd_back)
        self.add_folder = Button(self.ctrl, text = '新建文件夹',
                        font = ft, command = self.mkdir)
        self.add_file = Button(self.ctrl, text = '新建文件',
                        font = ft, command = self.touch)
        self.delete = Button(self.ctrl, text = '删除', font = ft,
                        command = self.f_delete)
        # 文件信息表初始化
        self.ftree = ttk.Treeview(self.win, show = 'headings')
        self.ftree['columns'] = ('fname', 'fdate', 'ftype', 'fsize', 'fauthor')
        self.ftree.column('fname', width = 268)
        self.ftree.column('fdate', width = 150)
        self.ftree.column('ftype', width = 80)
        self.ftree.column('fsize', width = 80)
        self.ftree.column('fauthor', width=80)
        self.ftree.heading('fname', text = '文件名', anchor = 'w')
        self.ftree.heading('fdate', text = '修改日期', anchor = 'w')
        self.ftree.heading('ftype', text = '类型', anchor = 'w')
        self.ftree.heading('fsize', text = '大小', anchor = 'w')
        self.ftree.heading('fauthor', text = '拥有者', anchor = 'w')
        # 使用grid布局
        self.l_user.grid(row = 0, column = 0, sticky = W)
        self.l_now.grid(row = 1, column = 0, sticky = W)
        self.l_dir.grid(row = 1, column = 1, sticky = W)
        self.ctrl.grid(row = 2, column = 1, sticky = W)
        self.back.grid(row = 0, column = 0, sticky = W)
        self.add_folder.grid(row = 0, column = 1, sticky = W)
        self.add_file.grid(row = 0, column = 2, sticky = W)
        self.delete.grid(row = 0, column = 3, sticky = W)
        self.ftree.grid(row = 3, column = 1, columnspan = 5)
        # 展示文件信息
        self.ls()

    def get_win(self):
        """
        获取当前窗体实例
        @return: 当前窗体实例
        """
        return self.win

    def ls(self):
        """
        展示当前目录下属于当前用户的所有文件
        """
        print('>> ls')
        fname, fdate, ftype, fsize, fauthor = self.disk.ls()
        for i in range(len(fname)):
            self.ftree.insert('', i, text='', 
                values=(fname[i], fdate[i], ftype[i], fsize[i], fauthor[i]))

    def cd_in(self, event):
        """
        双击鼠标左键 - 进入下一级 或 运行目标程序
        """
        for item in self.ftree.selection():
            item_text = self.ftree.item(item,"values")
            flag = self.disk.cd_in(item_text[0])
            if flag == 2:
                print('>> cd ' + item_text[0])
                self.refesh()
            elif flag == 1:
                print('>> start ', item_text[0])
            else:
                print('>> 权限不足，无法运行。')

    def cd_back(self):
        """
        点击返回按钮 - 返回上一级
        """
        if self.disk.here._type == 'root':
            print('>> 已到根目录')
        else:
            print('>> cd ..')
            self.disk.cd_back()
            self.refesh()
    
    def refesh(self):
        """
        刷新当前文件列表
        """
        x = self.ftree.get_children()
        for item in x:
            self.ftree.delete(item)
        x = self.ftree.get_children()
        self.l_dir_text.set(self.disk.here.path + self.disk.here.name)
        self.ls()

    def mkdir(self):
        """
        新建文件夹，默认文件名为当前系统时间
        """
        time_str = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        if self.disk.mkdir_or_touch(time_str, 1):
            self.refesh()
            print('>> mkdir ' + time_str)
        else:
            print('>> 权限不足，无法新建文件夹。')

    def touch(self):
        """
        创建新文件，默认创建文本文件，文件名为当前系统时间
        """
        time_str = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        if self.disk.mkdir_or_touch(time_str, 2):
            self.refesh()
            print('>> touch ' + time_str)
        else:
            print('>> 权限不足，无法新建文件。')
    
    def f_delete(self):
        """
        删除文件，向后端传入选中的对象，
        然后根据后端返回的状态码判断操作完成与否并输出
        """
        for item in self.ftree.selection():
            item_text = self.ftree.item(item, "values")
            src_name = item_text[0]
            src_type = item_text[2]
        # 返回状态码，若为2则删除文件夹，若为1则删除文件，若为0则无权限删除
        flag =  self.disk.delete(src_name, src_type)
        if flag == 2:
            print('>> rd /s /q ' + src_name)
            self.refesh()
        elif flag == 1:
            print('>> del ' + src_name)
            self.refesh()
        else:
            print('>> 权限不足，无法删除。')

    def rename(self, event):
        """
        单击鼠标右键，重命名文件或文件夹
        """
        for item in self.ftree.selection():
            item_text = self.ftree.item(item, "values")
            src_name = item_text[0]
        children = self.ftree.get_children()
        # 被选中节点的列编号，用于输入框定位
        column= self.ftree.identify_column(event.x)
        # 被选中节点的行编号，用于输入框定位与更新值
        row = children.index(self.ftree.selection()[0]) + 1
        cn = int(str(column).replace('#',''))
        rn = int(str(row).replace('I',''))
        entry_edit = Entry(self.win, width = 25 + (cn - 1) * 16)
        entry_edit.place(x = 105 + (cn - 1) * 130, y = 88 + rn * 20)
        # 按钮事件，用于触发文件名修改
        def save_edit():
            dst_name = entry_edit.get()
            flag = self.disk.rename(src_name, dst_name)
            if flag == 2:
                self.ftree.set(item, column = column, value = dst_name)
                print('>> rename(' + src_name + ', ' + dst_name + ')')
            elif flag == 1:
                print('>> 文件名已存在。')
            else:
                print('>> 权限不足，无法修改。')
            entry_edit.destroy()
            b_ok.destroy()
        # "OK"按键
        b_ok = Button(self.win, text='OK', width = 4, command = save_edit)
        b_ok.place(x = 285 + (cn - 1) * 242, y = 82 + rn * 20)

    def show(self):
        """
        绑定表格上的事件，运行窗口
        """
        self.ftree.bind('<Double-1>', self.cd_in)  # 双击鼠标左键
        self.ftree.bind('<Button-3>', self.rename)  # 单击鼠标右键
        self.win.mainloop()


class LoginWindow():
    """
    文件管理系统的登录窗口(GUI)，生成窗体，在输入框内输入用户名和密码，
    若用户名和密码匹配成功则销毁当前窗体，进入主界面（即生成MainWindow）
    @method show: 运行窗体
    @method login: 登录，若用户名和密码匹配成功则进入主界面
    """

    def __init__(self):
        """
        初始化窗体，生成相关控件
        """
        # 生成窗体
        self.win = Tk()
        self.win.title('登录')
        self.win.geometry('450x300')
        self.win.resizable(width=False, height=False)
        ft = ('Microsoft YaHei', 12)  # 全局字体
        # 顶部Label
        self.l_title = Label(self.win, text = '欢迎登录模拟文件系统',
                             font = ('Microsoft YaHei', 16))
        # 用户名输入
        self.f_user_name = Frame(self.win)
        self.l_name = Label(self.f_user_name, text = '用户名：', font = ft)
        self.e_user_name = Entry(self.f_user_name)
        # 密码输入
        self.f_user_pwd = Frame(self.win)
        self.l_pwd = Label(self.f_user_pwd, text = '密   码：', font = ft)
        self.e_user_pwd = Entry(self.f_user_pwd)
        # 登录按钮
        self.b_login = Button(self.win, text = '登录',
                        font = ft, command = self.login)
        # 使用pack布局
        self.l_title.pack(side = TOP, pady = 45)
        self.f_user_name.pack(side = TOP)
        self.l_name.pack(side = LEFT)
        self.e_user_name.pack(side = RIGHT)
        self.f_user_pwd.pack(side = TOP, pady = 15)
        self.l_pwd.pack(side = LEFT)
        self.e_user_pwd.pack(side = RIGHT)
        self.b_login.pack(side = TOP)

    def show(self):
        """
        运行窗体
        """
        self.win.mainloop()

    def login(self):
        """
        登录，若用户名和密码匹配成功则进入主界面
        """
        user_name = self.e_user_name.get()
        user_pwd = self.e_user_pwd.get()
        user_info = {}
        with open('user_info.txt') as f:
            line = f.readline()
            while line:
                line_tmp = line.strip('\n').split(' ')
                user_info[line_tmp[0]] = [line_tmp[1], line_tmp[2]]
                line = f.readline()
        # 判断用户名和密码是否匹配，若是则退出当前窗口，将用户信息登录到主界面
        if user_name in user_info and user_info[user_name][0] == user_pwd:
            print(user_info[user_name][1])
            user = User(user_name, user_info[user_name][1])
            self.win.quit()
            self.win.destroy()
            main_window = MainWindow(user)
            main_window.show()


if __name__ == "__main__":
    """
    主函数内只需生成登录窗口即可
    """
    login = LoginWindow()
    login.show()
