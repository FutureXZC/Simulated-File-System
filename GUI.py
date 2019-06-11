# -*- coding: UTF-8 -*-
from tkinter import ttk
from tkinter import *
from backEnd import *

class MainWindow():
    def __init__(self, user):
        # 获取后台信息
        self.disk = OSManager(user)
        # 生成窗体
        self.win = Tk()
        # self.win.title('Simulated File Management System')
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
        self.add_folder = Button(self.ctrl, text = '新建文件夹', font = ft)
        self.add_file = Button(self.ctrl, text = '新建文件', font = ft)
        self.delete = Button(self.ctrl, text = '删除', font = ft)
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
        self.l_dir_text.set(self.disk.here.path + self.disk.here.name)
        self.ls()

    # 绑定事件，运行窗口
    def show(self):
        self.ftree.bind('<Double-1>', self.cd_in)
        self.win.mainloop()


if __name__ == "__main__":
    user = User('root', 'rw')
    main_window = MainWindow(user)
    main_window.show()