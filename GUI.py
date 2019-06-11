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
        self.win.title('File Management System')
        self.win.geometry('800x350')
        self.win.resizable(width=False, height=False)
        ft = ('Microsoft YaHei', 10)  # 全局字体
        # 顶部label
        self.l_author = Label(self.win, text = self.disk.here.author, 
                            bg = 'Plum', font = ft)
        self.l_now = Label(self.win, text = '当前目录：', 
                            bg = 'Lavender', font = ft)
        self.l_dir_text = StringVar()
        self.l_dir_text.set(self.disk.here.path + self.disk.here.name)
        self.l_dir = Label(self.win, textvariable = self.l_dir_text, 
                            bg = 'LightCyan', font = ft, width = 90, anchor = 'w')

        # 操作按钮
        self.ctrl = Frame(self.win)
        self.back = Button(self.ctrl, text = '<--', font = ft, command = self.cd_back)                
        self.add_folder = Button(self.ctrl, text = '新建文件夹', font = ft)
        self.add_file = Button(self.ctrl, text = '新建文件', font = ft)
        self.delete = Button(self.ctrl, text = '删除', font = ft)
        # 文件信息表格初始化
        self.ftree = ttk.Treeview(self.win, show = 'headings')
        self.ftree['columns'] = ('fname', 'fdate', 'ftype', 'fsize', 'fauthor')
        self.ftree.column('fname', width = 270)
        self.ftree.column('fdate', width = 150)
        self.ftree.column('ftype', width = 80)
        self.ftree.column('fsize', width = 80)
        self.ftree.column('fauthor', width=80)
        self.ftree.heading('fname', text = '文件名')
        self.ftree.heading('fdate', text = '修改日期')
        self.ftree.heading('ftype', text = '类型')
        self.ftree.heading('fsize', text = '大小')
        self.ftree.heading('fauthor', text = '拥有者')
        # 设置布局
        self.l_author.grid(row = 0, column = 0, sticky = W)
        self.l_now.grid(row = 1, column = 0, sticky = W)
        self.l_dir.grid(row = 1, column = 1, sticky = W)
        self.ctrl.grid(row = 2, column = 1, sticky = W)
        self.back.grid(row = 0, column = 0, sticky = W)
        self.add_folder.grid(row = 0, column = 1, sticky = W)
        self.add_file.grid(row = 0, column = 2, sticky = W)
        self.delete.grid(row = 0, column = 3, sticky = W)
        self.ftree.grid(row = 3, column = 1, columnspan = 5)
        self.ls()

    # 展示当前目录下属于当前用户的所有文件
    def ls(self):
        fname, fdate, ftype, fsize, fauthor = self.disk.ls()
        print(fname)
        for i in range(len(fname)):
            self.ftree.insert('', i, text='', 
                values=(fname[i], fdate[i], ftype[i], fsize[i], fauthor[i]))

    # 进入下一级
    def cd_in(self):
        pass

    # 返回上一级
    def cd_back(self):
        self.disk.cd_back()
        x = self.ftree.get_children()
        for item in x:
            self.ftree.delete(item)
        self.l_dir_text.set(self.disk.here.path + self.disk.here.name)
        self.ls()
        self.win.update()

    # 运行窗口
    def show(self):
        self.win.mainloop()


if __name__ == "__main__":
    user = User('Tony', 'rw')
    mw = MainWindow(user)
    mw.show()