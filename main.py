import csv
import datetime
import os
import pickle
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
from mylib import *


def login(frame):
    # 框架放置
    frame.place(x=20, y=50)

    # 登录界面，用户、密码
    label1 = Label(frame, text='账号：', fg='black', font='Verdana 12 bold')
    label1.place(x=290, y=150)
    label2 = Label(frame, text='密码：', fg='black', font='Verdana 12 bold')
    label2.place(x=290, y=210)

    var_usr_name = StringVar()
    entry_usr_name = Entry(frame, textvariable=var_usr_name)
    entry_usr_name.place(x=340, y=150)

    var_usr_pwd = StringVar()
    entry_usr_pwd = Entry(frame, textvariable=var_usr_pwd, show='*')
    entry_usr_pwd.place(x=340, y=210)

    # 按钮,登录、注册、退出
    bt_login = Button(frame, text="登录",
                      command=lambda: usr_log_in(frame_login, frame_menu, frame_run, var_usr_name, var_usr_pwd),
                      fg='black',
                      font='Verdana 12 bold')
    bt_login.place(x=260, y=300)
    bt_sign_up = Button(frame, text="注册", command=usr_sign_up, fg='black', font='Verdana 12 bold')
    bt_sign_up.place(x=360, y=300)
    bt_sign_quit = Button(frame, text="退出", command=usr_sign_quit, fg='black', font='Verdana 12 bold')
    bt_sign_quit.place(x=460, y=300)


def menu(frame_login, frame_menu, frame_run):
    # 摧毁上一级页面
    frame_login.place_forget()

    # 框架放置
    frame_menu.place(x=20, y=50)
    frame_run.place(x=180, y=50)

    # button设置
    btn1 = Button(frame_menu, text='数据处理', font='Verdana 11 bold', command=lambda: run1(frame_run))
    btn1.place(x=15, y=50, width=120)
    btn2 = Button(frame_menu, text='查看结果', font='Verdana 11 bold', command=lambda: run2(frame_run))
    btn2.place(x=15, y=100, width=120)
    btn3 = Button(frame_menu, text='说明文档', font='Verdana 11 bold', command=lambda: run3(frame_run))
    btn3.place(x=15, y=150, width=120)
    btn3 = Button(frame_menu, text='关于我们', font='Verdana 11 bold', command=lambda: run4(frame_run))
    btn3.place(x=15, y=200, width=120)
    btn4 = Button(frame_menu, text='退出登录', font='Verdana 11 bold', command=lambda: run5(frame_login))
    btn4.place(x=15, y=250, width=120)

    lable = Label(frame_run, text='欢迎使用可视化特征选择工具', fg='black', font='Verdana 12 bold')
    lable.place(x=0, y=0, height=500, width=600)


def usr_log_in(frame_login, frame_menu, frame_run, var_usr_name, var_usr_pwd):
    usr_name = var_usr_name.get()
    user_pwd = var_usr_pwd.get()
    # 从本地字典获取用户信息，如果没有则新建本地数据库
    try:
        with open('info/usr_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
    except FileNotFoundError:
        os.mkdir('info')
        with open('info/usr_info.pickle', 'wb') as usr_file:
            usrs_info = {'admin': 'admin'}
            pickle.dump(usrs_info, usr_file)
    if usr_name in usrs_info:
        if user_pwd in usrs_info[usr_name]:
            tkinter.messagebox.showinfo(title='welcome', message=usr_name + '欢迎登录')
            menu(frame_login, frame_menu, frame_run)
        else:
            tkinter.messagebox.showerror(title='tip', message='密码错误,请重新输入！')
    elif usr_name == '' or user_pwd == '':
        tkinter.messagebox.showerror(title='tip', message='用户名或密码为空！')
    else:
        go_signup = tkinter.messagebox.askyesno('欢迎', '你还没注册，是否现在去注册？')
        if go_signup:
            usr_sign_up()


def usr_sign_up():
    # 确认注册时的相应函数
    def signtowcg():
        # 获取输入框内的内容
        nn = new_name.get()
        np = new_pwd.get()
        npf = new_pwd_confirm.get()

        # 本地加载已有用户信息,如果没有则已有用户信息为空
        try:
            with open('info/usr_info.pickle', 'rb') as usr_file:
                exist_usr_info = pickle.load(usr_file)
        except FileNotFoundError:
            exist_usr_info = {}

            # 检查用户名存在、密码为空、密码前后不一致
        if nn in exist_usr_info:
            tkinter.messagebox.showerror('错误', '用户名已存在')
        elif np == '' or nn == '':
            tkinter.messagebox.showerror('错误', '用户名或密码为空')
        elif np != npf:
            tkinter.messagebox.showerror('错误', '密码前后不一致')

        # 注册信息没有问题则将用户名密码写入数据库
        else:
            exist_usr_info[nn] = np
            with open('info/usr_info.pickle', 'wb') as usr_file:
                pickle.dump(exist_usr_info, usr_file)
            tkinter.messagebox.showinfo('欢迎', '注册成功')
            # 注册成功关闭注册框
            window_sign_up.destroy()

    # 新建注册界面
    window_sign_up = Toplevel(root)
    window_sign_up.geometry('350x200+450+300')
    window_sign_up.title('注册')
    # 用户名变量及标签、输入框
    new_name = StringVar()
    Label(window_sign_up, text='用户名：').place(x=10, y=10)
    Entry(window_sign_up, textvariable=new_name).place(x=150, y=10)

    # 密码变量及标签、输入框
    new_pwd = StringVar()
    Label(window_sign_up, text='请输入密码：').place(x=10, y=50)
    Entry(window_sign_up, textvariable=new_pwd, show='*').place(x=150, y=50)

    # 重复密码变量及标签、输入框
    new_pwd_confirm = StringVar()
    Label(window_sign_up, text='请再次输入密码：').place(x=10, y=90)
    Entry(window_sign_up, textvariable=new_pwd_confirm, show='*').place(x=150, y=90)

    # 确认注册按钮及位置
    bt_confirm_sign_up = Button(window_sign_up, text='确认注册',
                                command=signtowcg)
    bt_confirm_sign_up.place(x=150, y=130)


def usr_sign_quit():
    root.destroy()


def run1(frame):
    frame_clear(frame)

    # df = pd.DataFrame()
    var_file = StringVar()
    file_entry = Entry(frame, textvariable=var_file)
    file_entry.place(x=10, y=60, width=420, height=25)
    bt = Button(frame, text='选择文件路径', command=lambda: choose_file(var_file))
    bt.place(x=470, y=55)

    lb = Label(frame, text='算法选择', fg='black', font='Verdana 12 bold')
    lb.place(x=10, y=120)
    var_cbox = StringVar()
    cbox = ttk.Combobox(frame, textvariable=var_cbox)
    cbox['value'] = ('自适应算法', '单变量统计', '基于模型的特征选择', '迭代特征选择')
    cbox.place(x=90, y=120)
    cbox.current(0)

    lb2 = Label(frame, text='模型选择', fg='black', font='Verdana 12 bold')
    lb2.place(x=310, y=120)
    var_cbox2 = StringVar()
    cbox2 = ttk.Combobox(frame, textvariable=var_cbox2)
    cbox2['value'] = ('自适应模型', '随机森林', 'GBDT', 'xgboost', '支持向量机', '多层感知机')
    cbox2.place(x=390, y=120)
    cbox2.current(0)

    button = Button(frame, text='Running', fg='black', font='Verdana 12 bold', command=lambda: running(df))
    button.place(x=450, y=400, width=100, height=50)

    def choose_file(var_file):
        global df
        filename = filedialog.askopenfilename(title='选择文件')
        var_file.set(filename)
        if filename.split('.')[1] == 'csv':
            df = pd.read_csv(filename, index_col=False, header=0)
        elif filename.split('.')[1] == 'xlsx':
            df = pd.read_csv(filename, index_col=False, header=0)
        else:
            tkinter.messagebox.showerror('错误', '请输入.csv文件或.xlsx文件')

        lb3 = Label(frame, text='数据预览', fg='black', font='Verdana 12 bold')
        lb3.place(x=10, y=170)

        table_container = Frame(frame, width=542, height=180)
        table_container.place(x=10, y=200)

        colNames = df.columns.to_list()
        tree = ttk.Treeview(table_container, columns=colNames, show="headings")

        for _ in colNames:
            tree.column(_, width=70, anchor='center')
            tree.heading(_, text=_, anchor='center')
        for index, row in df.iterrows():
            tree.insert("", END, values=tuple(row))
        tree.place(relx=0, rely=0)

    def running(df):
        feature_select(df, cbox['value'].index(var_cbox.get()), cbox2['value'].index(var_cbox2.get()), var_file.get())
        tkinter.messagebox.showinfo('提示', '特征选择已完成！')

    def feature_select(df, p1, p2, filename):
        start = time.time()
        if p1 == 0 or p1 == 1:
            output_filename = univariate_statistics(df, filename)
        elif p2 == 2:
            output_filename = select_from_model(df, p2, filename)
        else:
            output_filename = select_from_RFECV(df, p2, filename)
        end = time.time()

        header = ["编号", "项目名称", "创建时间", "处理时间", "保存文件"]
        file_path = './info/history.csv'
        # 检查CSV文件是否存在
        if os.path.exists(file_path):
            # 读取CSV文件
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                # 获取数据列表和最大索引值
                data = [row for row in reader]
                max_index = max(int(row[0]) for row in data) if len(data) > 1 else 0
        else:
            max_index = 0
            data = []
        # 定义新行
        new_row = [max_index + 1, f'项目{max_index + 1}', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                   f'{round((end - start) / 60, 2)}min', output_filename]

        # 将新行插入到数据列表中
        data.append(new_row)

        # 将数据列表写回CSV文件
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)


def run2(frame):
    frame_clear(frame)

    tree = ttk.Treeview(frame, columns=("编号", "项目名称", "创建时间", "处理时间", "保存文件"), show='headings',
                        height=32)  # 创建表格对象
    tree.column("编号", width=50, anchor='center')  # 设置列
    tree.column("项目名称", width=125, anchor='center')
    tree.column("创建时间", width=175, anchor='center')
    tree.column("处理时间", width=125, anchor='center')
    tree.column("保存文件", width=125, anchor='center')
    tree.heading("编号", text="编号")  # 设置显示的表头名
    tree.heading("项目名称", text="项目名称")
    tree.heading("创建时间", text="创建时间")
    tree.heading("处理时间", text="处理时间")
    tree.heading("保存文件", text="保存文件")

    file_path = './info/history.csv'
    if os.path.exists(file_path):
        # 读取CSV文件
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            # 获取数据列表和最大索引值
            data = [row for row in reader]
            for i in data:
                tree.insert("", END, values=tuple(i))
    tree.place(x=0, y=0)


def run3(frame):
    frame_clear(frame)
    lb4 = Label(frame, text='功能三相应模块', fg='black', font='Verdana 12 bold')
    lb4.place(x=0, y=0, height=500, width=600)


def run4(frame):
    frame_clear(frame)
    lb4 = Label(frame, text='功能四相应模块', fg='black', font='Verdana 12 bold')
    lb4.place(x=0, y=0, height=500, width=600)


def run5(frame):
    frame_menu.place_forget()
    frame_run.place_forget()
    login(frame)


def frame_clear(frame):
    for widget in frame.winfo_children():
        widget.destroy()


if __name__ == '__main__':
    root = Tk()
    root.configure(background='SteelBlue')
    root.geometry('800x572+300+150')
    root.title('可视化特征选择工具')

    lb1 = Label(root, text='可视化特征选择工具', fg='black', font='Verdana 15 bold')
    lb1.place(x=20, y=5, height=40, width=760)

    # 登录界面框架
    frame_login = Frame(root, height=500, width=760)

    # 应用界面框架
    frame_menu = Frame(root, height=500, width=150)
    frame_run = Frame(root, height=500, width=600)

    # 登录
    # login(frame_login)
    menu(frame_login, frame_menu, frame_run)

    root.mainloop()
