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
        self.add_file = Button(self.ctrl, text = '新建文件', font = ft)
        self.delete = Button(self.ctrl, text = '删除', font = ft, command = self.quit)
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
        # 设置布局
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
            if self.disk.cd_in(item_text[0]):
                print('>> cd ' + item_text[0])
                self.refesh()
            else:
                print('>> start ', item_text[0])

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
        flag, a = self.disk.mkdir(time_str)
        if flag:
            self.refesh()
            print('>> mkdir ' + time_str)
        else:
            print('>> 已存在该文件夹')
    
    # 单击鼠标右键 - 重命名文件或文件夹
    def rename(self, event): # 右键进入编辑状态
        for item in self.ftree.selection():
            item_text = self.ftree.item(item, "values")
            src_name = item_text[0]
        children = self.ftree.get_children()
        # 被选中节点的列编号，用于输入框定位
        column= self.ftree.identify_column(event.x)
        # 被选中节点的行编号，输入框定位与更新值
        row = children.index(self.ftree.selection()[0]) + 1
        cn = int(str(column).replace('#',''))
        rn = int(str(row).replace('I',''))
        entryedit = Entry(self.win, width = 25 + (cn - 1) * 16)
        entryedit.place(x = 105 + (cn - 1) * 130, y = 88 + rn * 20)
        def save_edit():
            dst_name = entryedit.get()
            self.ftree.set(item, column = column, value = dst_name)
            self.disk.rename(src_name, dst_name)
            print('>> rename(' + src_name + ', ' + dst_name + ')')
            entryedit.destroy()
            okb.destroy()
        okb = Button(self.win, text='OK', width = 4, command = save_edit)
        okb.place(x = 285 + (cn - 1) * 242, y = 82 + rn * 20)

    # 绑定事件，运行窗口
    def show(self):
        self.ftree.bind('<Double-1>', self.cd_in)  # 双击鼠标左键
        self.ftree.bind('<Button-3>', self.rename)  # 单击鼠标右键
        self.win.mainloop()
    
    # 退出
    def quit(self):
        self.win.quit()


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
        # 布局
        self.l_title.pack(side = TOP, pady = 45)
        self.f_user_name.pack(side = TOP)
        self.l_name.pack(side = LEFT)
        self.e_user_name.pack(side = RIGHT)
        self.f_user_pwd.pack(side = TOP, pady = 15)
        self.l_pwd.pack(side = LEFT)
        self.e_user_pwd.pack(side = RIGHT)
        self.b_login.pack(side = TOP)

    def show(self):
        self.win.mainloop()

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
        if user_name in user_info and user_info[user_name][0] == user_pwd:
            user = User(user_name, user_info[user_name][1])
            main_window = MainWindow(user)
            # main_window = MainWindow(user)
            # main_window.show()


if __name__ == "__main__":
    # login = loginWindow()
    # login.show()
    user = User('root', 'rw')
    main_window = MainWindow(user)
    main_window.show()
    # os.system('type nul>root/test.go')