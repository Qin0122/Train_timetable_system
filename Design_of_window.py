from tkinter import *
from tkinter import messagebox
import tkinter as tk
import datetime
# 导入自定义的模块
import Train_system
import re

class Application(tk.Frame):
    # master等待接收根窗口对象，app_1等待接收自定义导入的模块
    def __init__(self, master=None, app_1=None):
        tk.Frame.__init__(self,master)
        self.master = master
        self.pack()
        # 调用在根窗口创建组件的函数
        self.createWidget()
        # 初始化一个title1列表，作为窗口中的提示信息
        self.title1 = ['车次号（例：K6025）', '起点站', '终点站', '列车类型', '发车时间(例：2022-4-16 8:30)', '到站时间(例：2022-4-16 10:30)', '里程（Km）',
                     '历时（例：1小时30分）', '价格（元）']
# 创建组件
    def createWidget(self):
        '''在根窗口创建按钮组件，通过按钮组件定位点击事件，调用事件方法'''

        Button(self, text='录入列车信息', command=self.info_record, font=('黑体', 12)).grid(row=0, column=0, pady=10)
        Button(self, text='查看所有列车信息', command=self.info_search_all, font=('黑体', 12)).grid(row=1, column=0, pady=10)
        Button(self, text='车次查询（车次号、起点站和终点站）', command=self.info_search, font=('黑体', 12)).grid(row=2, column=0, pady=10)
        Button(self, text='修改列车信息', command=self.info_modify, font=('黑体', 12)).grid(row=3, column=0, pady=10)
        Button(self, text='删除列车信息', command=self.info_del, font=('黑体', 12)).grid(row=4, column=0)


# 录入信息
    def info_record(self):
        root_1 = tk.Toplevel() # 实例化一个顶级弹出的类窗口
        root_1.geometry('500x270') # 设置窗口大小
        root_1.title('信息录入') # 设置窗口标题
        Label(root_1, text='请点击“确定”按钮检查修改的信息是否有误\n无误后再点击“录入”按钮', font=('黑体', 12), bg='black', fg='white').grid(row=0, column=0)
        # 通过for循环将self.title1中的元素排列好
        for i in range(len(self.title1)):
            Label(root_1, text=self.title1[i], font=('黑体', 12)).grid(row=i+1, column=0)
        # 实例化Entry的接收对象，StringVar表示接收的是一个字符型变量，InVar表示接收的是一个整型变量
        v1 = StringVar() # 接收车次号
        v2 = StringVar() # 接收起始站
        v3 = StringVar() # 接收终点站
        v4 = StringVar() # 接收列车类型
        v5 = StringVar() # 接收发车时间
        v6 = StringVar() # 接收到站时间
        v7 = IntVar() # 接收里程
        v8 = StringVar() # 接收历时
        v9 = IntVar() # 接收价格
        # 设置一个列表li_1，用来存放Entry的接收对象
        li_1 =  [v1, v2, v3, v4, v5, v6, v7, v8, v9]
        # 创建Entry组件，通过for循环，将组件排列好，等待用户输入数据
        for index, v in enumerate(li_1):
            Entry(root_1, textvariable=v).grid(row=index+1, column=1)

        def recode_1():
            # 列表li_2，用来接收用户输入的信息，即Entry接收的信息
            li_2 = [v1.get(), v2.get(), v3.get(), v4.get(), datetime.datetime.strptime(v5.get(), "%Y-%m-%d %H:%M"),
                    datetime.datetime.strptime(v6.get(), "%Y-%m-%d %H:%M"), v7.get(), v8.get(), v9.get()]
            # 调用app_1类中的info_record方法，传入接收的信息li_2，将传入的信息写入文件
            app_1.info_record(li_2)
            # 传入完成后弹出一个结果窗口
            messagebox.showinfo('录入情况', '信息录入成功！')
            # 点击弹出结果窗口的确定后退出
            root_1.destroy()
        # 设置一个确定按钮，用来检查输入的信息是否有误
        Button(root_1, text='确定', command=lambda: self.judge_wrong(li_1)).grid(row=10, column=0, sticky=NS)
        Button(root_1, text='录入', command=recode_1).grid(row=10, column=1, sticky=NSEW)
        root_1.mainloop()


# 查询列车信息
    def info_search_all(self):
        root_2 = Toplevel() # 实例化一个顶级弹出的类窗口
        root_2.title('列车信息表') # 设置窗口标题
        root_2.geometry('1500x400') # 设置窗口大小

        '''-----给root_2窗口设置滚轮-----'''
        s1 = Scrollbar(root_2)
        s1.pack(side=RIGHT, fill=Y)
        # HORIZONTAL 设置水平方向的滚动条，默认是竖直
        s2 = Scrollbar(root_2, orient=HORIZONTAL)
        s2.pack(side=BOTTOM, fill=X)
        # 创建文本框
        # wrap 设置不自动换行
        textpad = Text(root_2, width=200, yscrollcommand=s1.set, xscrollcommand=s2.set, wrap='none')
        textpad.pack(expand=YES, fill=BOTH)
        textpad.configure(font=('黑体', 12))
        s1.config(command=textpad.yview)
        s2.config(command=textpad.xview)

        # 调用app_1类的info_search_all方法，获取列车信息库中的信息，并返回一个信息列表
        li_info = app_1.info_search_all()
        for i in li_info:
            n = 0 # 用来控制索引
            for j in range(len(i)):
                if n==8:
                    textpad.insert(INSERT,'\t'*2 + str(i[n])+ '\n') # 在文本框中插入信息
                    break
                elif n==4 or n==6:
                    textpad.insert(INSERT, '\t'*3 + str(i[n]) + '\t'*3 + str(i[n+1]))
                elif n==0:
                    textpad.insert(INSERT, str(i[n]) + '\t' * 2 + str(i[n + 1]))
                else:
                    textpad.insert(INSERT, '\t'*2 + str(i[n]) + '\t'*2 + str(i[n+1]))
                n += 2
        root_2.mainloop()


# 车次查询（车次号、起点站和终点站）
    def info_search(self):
        root_3 = Toplevel() # 实例化一个顶级弹出的类窗口
        root_3.geometry('300x250')
        v_1 = StringVar() # 接收车次信息
        v_2 = StringVar() # 接收起点站信息
        v_3 = StringVar() # 接收终点站信息
        # 将以上的三个变量放入列表li_1中
        li_1 = [v_1, v_2, v_3]
        Label(root_3, text='可根据车次号或\n起始站和终点站查询车次信息', fg='white',bg='black',font=('黑体', 12)).grid(row=0,column=1,pady=10)
        Label(root_3, text='车次号', font=('黑体', 12)).grid(row=1,column=0,pady=10)
        Label(root_3, text='起始站', font=('黑体', 12)).grid(row=2,column=0,pady=10)
        Label(root_3, text='终点站', font=('黑体', 12)).grid(row=3,column=0)
        # 通过for循环，排列Entry框
        for index, v in enumerate(li_1):
            Entry(root_3, textvariable=v).grid(row=index+1, column=1, pady=10)
        # 定义一个func函数，设置一个查询结果窗口
        def func():
            root_4 = Toplevel()
            # root_4.withdraw() # 防止两个根窗口同时开启
            root_4.title('查询结果')
            root_4.geometry('1500x400')
            li_2 = [v_1.get(), v_2.get(), v_3.get()] # 将用户输入的信息放入列表li_2中

            '''给窗口root_4设置滚轮'''
            s_1 = Scrollbar(root_4)
            s_1.pack(side=RIGHT, fill=Y)
            # HORIZONTAL 设置水平方向的滚动条，默认是竖直
            s_2 = Scrollbar(root_4, orient=HORIZONTAL)
            s_2.pack(side=BOTTOM, fill=X)
            # 创建文本框
            # wrap 设置不自动换行
            text01 = Text(root_4, width=200, yscrollcommand=s_1.set, xscrollcommand=s_2.set, wrap='none')
            text01.pack(expand=YES, fill=BOTH)
            text01.configure(font=('黑体', 12))
            s_1.config(command=text01.yview)
            s_2.config(command=text01.xview)
            # 通过调用app_1类的info_search方法，传递用户输入的信息，获取返回结果（列表信息）
            li_info = app_1.info_search(li_2)
            # 如果返回的是一个空列表，则弹出错误信息
            if li_info == []:
                root_4.withdraw()
                messagebox.showinfo('查询结果', '没有您所要查找的信息')
            else:
                # 创建一个表头列表li_3
                li_3 = ['车次号', '起点站', '终点站', '列车类型', '发车时间', '到站时间', '里程',
                        '历时', '价格（元）']
                li_info.insert(0, li_3) # 将表头列表插入到返回的列表信息中
                # 通过for循环，将获取的信息放入文本框text01中，并排布整齐
                for i in li_info:
                    n = 0
                    for j in range(len(i)):
                        if n == 8:
                            text01.insert(INSERT, '\t' * 3 + str(i[n]) + '\n')
                            break
                        elif n == 4 or n == 6:
                            text01.insert(INSERT, '\t' * 3 + str(i[n]) + '\t' * 3 + str(i[n + 1]))
                        elif n == 0:
                            text01.insert(INSERT, str(i[n]) + '\t' * 3 + str(i[n + 1]))
                        else:
                            text01.insert(INSERT, '\t' * 3 + str(i[n]) + '\t' * 3 + str(i[n + 1]))
                        n += 2
            root_4.mainloop()

        # 设置一个查询按钮，绑定func事件
        Button(root_3, text='查询', command=func).grid(row=4, column=1, sticky=NS)
        root_3.mainloop()


# 修改列车信息
    def info_modify(self):
        self.root_5 = Toplevel()
        self.root_5.title('修改列车信息')
        self.root_5.geometry('150x100')
        Label(self.root_5, text='请输入车次号',font=('黑体', 12), fg='white', bg='black').grid(row=0,column=1)
        self.v_1 = StringVar()
        Entry(self.root_5, textvariable=self.v_1).grid(row=1, column=1)
        # 定义一个search函数，用来判断用户输入的车次号是否存在，不存在则弹出提示窗口，存在则调用info_recode_1方法
        def search():
            li_1 = app_1.search(self.v_1.get())
            if li_1 == []:
                messagebox.showinfo('错误', '该车次号不存在！')
            else:
                self.info_recode_1(li_1)
        # 根据输入的车次号查询
        Button(self.root_5, text='确定', command=search).grid(row=3, column=1)
        self.root_5.mainloop()


    # 设置一个info_search_1函数，通过用户输入的车次信息查找并修改
    def info_recode_1(self, li_1):
        root_6 = tk.Toplevel()  # 顶级弹出的类窗口
        root_6.geometry('500x270')
        Label(root_6, text='请点击“确定”按钮检查修改的信息是否有误\n无误后再点击“录入”按钮', font=('黑体', 12), bg='black', fg='white').grid(row=0, column=0)
        root_6.title('修改列车信息')
        for i in range(len(self.title1)):
            Label(root_6, text=self.title1[i], font=('黑体', 12)).grid(row=i+1, column=0)
        # 实例化Entry的接收对象，StringVar表示接收的是一个字符型变量，InVar表示接收的是一个整型变量
        v1 = StringVar() # 接收车次号
        v2 = StringVar() # 接收起始站
        v3 = StringVar() # 接收终点站
        v4 = StringVar() # 接收列车类型
        v5 = StringVar() # 接收发车时间
        v6 = StringVar() # 接收到站时间
        v7 = IntVar() # 接收里程
        v8 = StringVar() # 接收历时
        v9 = IntVar() # 接收价格
        # 设置一个列表li_1，用来存放Entry的接收对象
        li_2 =  [v1, v2, v3, v4, v5, v6, v7, v8, v9]
        # 创建Entry组件，通过for循环，将组件排列好，等待用户输入数据
        for index, v in enumerate(li_2):
            Entry(root_6, textvariable=v).grid(row=index+1, column=1)
        # 给Entry组件设置默认值
        v1.set(li_1[0])
        v2.set(li_1[1])
        v3.set(li_1[2])
        v4.set(li_1[3])
        v5.set(str(li_1[4])[:16])
        v6.set(str(li_1[5])[:16])
        v7.set(li_1[6])
        v8.set(li_1[7])
        v9.set(li_1[8])

        # 将修改的信息保存
        def recode_2():
            li_3 = [v1.get(), v2.get(), v3.get(), v4.get(), datetime.datetime.strptime(v5.get(), "%Y-%m-%d %H:%M"),
                    datetime.datetime.strptime(v6.get(), "%Y-%m-%d %H:%M"), v7.get(), v8.get(), v9.get()]
            app_1.info_modify(li_3)
            messagebox.showinfo('修改情况', '修改成功！')
            # 点击弹出窗口的确定后退出
            root_6.destroy()
        # 设置一个确定按钮，用来检查输入的信息是否有误
        Button(root_6, text='确定', command=lambda: self.judge_wrong(li_2)).grid(row=10, column=0, sticky=NS)
        # 设置修改按钮，绑定recode_2事件
        Button(root_6, text='修改', command=recode_2).grid(row=10, column=1, sticky=NSEW)
        root_6.mainloop()


# 删除列车信息
    def info_del(self):
        root_7 = Toplevel()
        root_7.title('删除列车信息')
        root_7.geometry('350x100')
        Label(root_7, text='请输入车次号',font=('黑体', 12), fg='white', bg='black').grid(row=0,column=2)
        v_1 = StringVar()
        Entry(root_7, textvariable=v_1).grid(row=1, column=2)
        # 定义一个funb函数，用来判断用户输入的车次号是否存在，存在则删除，不存在则弹出提示窗口
        def funb():
            li = app_1.search(v_1.get())
            if li == []:
                messagebox.showinfo('错误','该车次号不存在！')
            else:
                app_1.del_info(v_1.get())
                messagebox.showinfo('删除结果','删除成功！')
                root_7.destroy()
        Button(root_7, text='确定', command=funb).grid(row=3, column=2)
        root_7.mainloop()


# 判断错误 li_info是一个列表，里面存放的是要录入或修改的数据，主要判断录入或修改时所填写的信息是否有误
    def judge_wrong(self, li_info):
        def inner(): # 设置一个inner函数判断用户输入的信息是否有误，有误则弹出错误提示框并返回0，无误则返回一个1
            # 循环每一个Entry值，若有空则弹出提示窗口
            for i in li_info:
                if i.get() == '' or i.get() == 0:
                    messagebox.showinfo('错误', '信息未填写完整，请将信息填写完整！！')
                    return 0
            # 对车次号判错
            if len(li_info[0].get()) != 5 :
                messagebox.showinfo('车次号错误', '请输入五位的列车号！')
                return 0
            elif bool(re.search('[A-Z]', li_info[0].get())) == False:
                messagebox.showinfo('车次号错误', '车次号的第一位应为大写的英文字母！')
                return 0
            # 对发车时间和到站时间进行判错，使用异常
            try:
                datetime.datetime.strptime(li_info[4].get(), "%Y-%m-%d %H:%M")
                datetime.datetime.strptime(li_info[5].get(), "%Y-%m-%d %H:%M")
            except:
                messagebox.showinfo('时间错误', '请输入正确的时间格式：年-月-日 时:分')
                return 0
            # 以上信息没有错误则返回1
            return 1
        result = inner()
        if result == 1:
            messagebox.showinfo('正确', '输入的信息无误！')


if __name__ == '__main__':
    root = Tk() # 实例化一个根窗口对象
    root.title('列车信息系统')
    root.geometry('400x300+200+300')
    # 实例化导入的自定义模块中的对象
    app_1 = Train_system.Train()
    # 实例化对象
    app = Application(root, app_1)
    # 调用组建的mainloop()方法，进入事件循环
    root.mainloop()
