# -*- coding: UTF-8 -*-
from tkinter import ttk
from tkinter import *
from backEnd import *
import datetime

class MainWindow():
    def __init__(self, user):
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
        self.back = Button(self.ctrl, text = '<--', font = ft, command = self.cd_back)
        self.add_folder = Button(self.ctrl, text = '新建文件夹', font = ft, command = self.mkdir)
        self.add_file = Button(self.ctrl, text = '新建文件', font = ft, command = self.touch)
        self.delete = Button(self.ctrl, text = '删除', font = ft, command = self.f_delete)
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

    # 获取当前窗体实例
    def get_win(self):
        return self.win

    # 展示当前目录下属于当前用户的所有文件
    def ls(self):
        print('>> ls')
        fname, fdate, ftype, fsize, fauthor = self.disk.ls()
        for i in range(len(fname)):
            self.ftree.insert('', i, text='', 
                values=(fname[i], fdate[i], ftype[i], fsize[i], fauthor[i]))

    # 双击鼠标左键 - 进入下一级 或 运行目标程序
    def cd_in(self, event):
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

    # 点击返回按钮 - 返回上一级
    def cd_back(self):
        if self.disk.here._type == 'root':
            print('>> 已到根目录')
        else:
            print('>> cd ..')
            self.disk.cd_back()
            self.refesh()
    
    # 刷新
    def refesh(self):
        x = self.ftree.get_children()
        for item in x:
            self.ftree.delete(item)
        x = self.ftree.get_children()
        self.l_dir_text.set(self.disk.here.path + self.disk.here.name)
        self.ls()

    # 新建文件夹
    def mkdir(self):
        time_str = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        if self.disk.mkdir_or_touch(time_str, 1):
            self.refesh()
            print('>> mkdir ' + time_str)
        else:
            print('>> 权限不足，无法新建文件夹。')

    # 创建新文件
    def touch(self):
        time_str = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        if self.disk.mkdir_or_touch(time_str, 2):
            self.refesh()
            print('>> touch ' + time_str)
        else:
            print('>> 权限不足，无法新建文件。')
    
    # 删除文件
    def f_delete(self):
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

    # 单击鼠标右键 - 重命名文件或文件夹
    def rename(self, event): # 右键进入编辑状态
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

    # 绑定事件，运行窗口
    def show(self):
        self.ftree.bind('<Double-1>', self.cd_in)  # 双击鼠标左键
        self.ftree.bind('<Button-3>', self.rename)  # 单击鼠标右键
        self.win.mainloop()


# 登录窗口
class loginWindow():
    def __init__(self):
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
        self.b_login = Button(self.win, text = '登录', font = ft, command = self.login)
        # 使用pack布局
        self.l_title.pack(side = TOP, pady = 45)
        self.f_user_name.pack(side = TOP)
        self.l_name.pack(side = LEFT)
        self.e_user_name.pack(side = RIGHT)
        self.f_user_pwd.pack(side = TOP, pady = 15)
        self.l_pwd.pack(side = LEFT)
        self.e_user_pwd.pack(side = RIGHT)
        self.b_login.pack(side = TOP)

    # 运行
    def show(self):
        self.win.mainloop()

    # 登录
    def login(self):
        user_name = self.e_user_name.get()
        user_pwd = self.e_user_pwd.get()
        user_info = {}
        with open('user_info.txt') as f:
            line = f.readline()
            while line:
                line_tmp = line.strip('\n').split(' ')
                user_info[line_tmp[0]] = [line_tmp[1], line_tmp[2]]
                line = f.readline()
        # 判断用户名和密码是否一致，若一致则推出当前窗口，将用户信息登录到主界面
        if user_name in user_info and user_info[user_name][0] == user_pwd:
            print(user_info[user_name][1])
            user = User(user_name, user_info[user_name][1])
            self.win.quit()
            self.win.destroy()
            main_window = MainWindow(user)
            main_window.show()


if __name__ == "__main__":
    # 主函数内只需生成登录窗口即可
    login = loginWindow()
    login.show()
    user = User('Tony', 'rw')