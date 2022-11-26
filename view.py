import os
import pickle
import random
import time
import tkinter.messagebox
import webbrowser
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox, Progressbar, Treeview
from PIL import Image, ImageTk
from pyecharts import options as opts
from pyecharts.charts import HeatMap, Scatter
from pyecharts.faker import Faker
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot


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
        with open('./user/usr_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
    except FileNotFoundError:
        os.mkdir('./user')
        with open('./user/usr_info.pickle', 'wb') as usr_file:
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
            with open('usr_info.pickle', 'rb') as usr_file:
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
            with open('usr_info.pickle', 'wb') as usr_file:
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

    var_file = StringVar()
    file_entry = Entry(frame, textvariable=var_file)
    file_entry.place(x=10, y=60, width=400, height=25)
    bt = Button(frame, text='选择文件路径', command=lambda: choose_file(var_file))
    bt.place(x=450, y=55)

    def choose_file(var_file):
        filename = filedialog.askopenfilename(title='选择文件')
        var_file.set(filename)

    lb = Label(frame, text='算法选择', fg='black', font='Verdana 12 bold')
    lb.place(x=10, y=120)
    var_cbox = StringVar()
    cbox = Combobox(frame, textvariable=var_cbox)
    var_cbox = '自适应算法'
    cbox['value'] = ('自适应算法', '算法1', '算法2', '算法3', '算法4')
    cbox.place(x=90, y=120)
    cbox.current(0)

    progressbarOne = Progressbar(frame)
    progressbarOne.place(x=20, y=300, width=550, height=50)
    progressbarOne['maximum'] = 100
    progressbarOne['value'] = 0
    button = tkinter.Button(frame, text='Running', fg='black', font='Verdana 13 bold', command=lambda: show())
    button.place(x=420, y=370, width=150, height=100)

    def show():
        for i in range(100):
            progressbarOne['value'] = i + 1
            frame.update()
            time.sleep(-0.00001 * i * i + 0.1)
        tr = Toplevel(root)
        tr.geometry('320x200+530+300')
        tr.title('提示')
        tr_lb = Label(tr, text='特征选择已完成！', fg='black', font='Verdana 14 bold')
        tr_lb.place(x=0, y=0, width=320, height=160)


def run2(frame):
    frame_clear(frame)

    tree = Treeview(frame, columns=("编号", "项目名称", "创建时间", "处理时间", "文件大小"), show='headings',
                    height=32)  # 创建表格对象
    tree.column("编号", width=50, anchor='center')  # 设置列
    tree.column("项目名称", width=125, anchor='center')
    tree.column("创建时间", width=175, anchor='center')
    tree.column("处理时间", width=125, anchor='center')
    tree.column("文件大小", width=125, anchor='center')
    tree.heading("编号", text="编号")  # 设置显示的表头名
    tree.heading("项目名称", text="项目名称")
    tree.heading("创建时间", text="创建时间")
    tree.heading("处理时间", text="处理时间")
    tree.heading("文件大小", text="文件大小")
    tree.insert("", 0, values=("1", "项目一", "2022-5-20 13:23:02", "2min", "90MB"))
    tree.insert("", 1, values=("2", "项目二", "2022-5-20 13:23:02", "1min", "42MB"))
    tree.insert("", 2, values=("3", "项目三", "2022-5-20 13:23:02", "5min", "250MB"))
    tree.insert("", 3, values=("4", "项目四", "2022-5-20 13:23:02", "30sec", "20MB"))
    tree.place(x=0, y=0)

    # 热力图绘制函数
    def heat_map():
        heat_map_value = [[i, j, random.randint(0, 50)] for i in range(24) for j in range(7)]
        c = (
            HeatMap()
                .add_xaxis(Faker.clock)
                .add_yaxis(
                "series0",
                Faker.week,
                heat_map_value,
                label_opts=opts.LabelOpts(is_show=True, position="inside"),
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(title="HeatMap-Label 显示"),
                visualmap_opts=opts.VisualMapOpts(),
            )
        )
        make_snapshot(snapshot, c.render("./pages/HeatMap.html"), "./images/HeatMap.png")

    # 散点图绘制
    def scatter():
        data = [
            [10.0, 8.04],
            [8.0, 6.95],
            [13.0, 7.58],
            [9.0, 8.81],
            [11.0, 8.33],
            [14.0, 9.96],
            [6.0, 7.24],
            [4.0, 4.26],
            [12.0, 10.84],
            [7.0, 4.82],
            [5.0, 5.68],
        ]
        data.sort(key=lambda x: x[0])
        x_data = [d[0] for d in data]
        y_data = [d[1] for d in data]

        sc = (
            Scatter(init_opts=opts.InitOpts(width="1600px", height="1000px"))
                .add_xaxis(xaxis_data=x_data)
                .add_yaxis(
                series_name="",
                y_axis=y_data,
                symbol_size=20,
                label_opts=opts.LabelOpts(is_show=False),
            )
                .set_series_opts()
                .set_global_opts(
                xaxis_opts=opts.AxisOpts(
                    type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
                ),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
                tooltip_opts=opts.TooltipOpts(is_show=False),
            )
        )
        make_snapshot(snapshot, sc.render("./pages/Scatter.html"), "./images/Scatter.png")

    # 置空itm
    global itm
    itm = {}

    # 获取历史记录选择项
    def focus(event):
        global itm
        itm = tree.set(tree.focus())

    # 主页面查看按钮
    def click():
        if len(itm) != 0:
            frame_clear(frame)
            print(itm)
            # 创建新Frame--查看详情页面
            # 项目信息Label
            la2 = Label(frame,
                        text="编号:" + itm.get("编号") + "\t项目名称:" + itm.get("项目名称") + "\t创建时间:" + itm.get(
                            "创建时间") + "\t处理时间:" + itm.get("处理时间") + "   文件大小:" + itm.get("文件大小"))
            la2.place(x=0, y=0)
            la3 = Label(frame, text="图像类型:")
            la3.place(x=0, y=20)

            # 下拉单选框
            values = ["热力图", "散点图"]
            image_combobox = Combobox(frame, values=values, height=10, width=20, state='readonly', cursor='arrow')
            image_combobox.place(x=70, y=20)

            # 查看按钮绑定函数
            def print_choice():
                global img_open
                image = image_combobox.get()
                if image:
                    if image == "热力图":
                        heat_map()
                        url = "HeatMap.html"
                        width, height = 590, 400
                        img_open = Image.open("./images/HeatMap.png").resize((width, height))

                    elif image == "散点图":
                        scatter()
                        url = "Scatter.html"
                        width, height = 590, 400
                        img_open = Image.open("./images/Scatter.png").resize((width, height))

                    def open_url(event):
                        webbrowser.open("http://localhost:63342/feature_select/pages/" + url)

                    img_png = ImageTk.PhotoImage(img_open)
                    la_image = Label(frame, text=image_combobox.get(), image=img_png, width=590, height=400)
                    la_image.place(x=0, y=50)
                    btn_url = Button(frame, text='浏览器打开', width=10, relief=RAISED)
                    btn_url.place(x=400, y=20)
                    btn_url.bind("<Button-1>", open_url)
                else:
                    tkinter.messagebox.showinfo(title='注意', message='未选择图像类型!')

            # 查看按钮
            bt_search = Button(frame, text="查看", width=10, relief=RAISED)
            bt_search.place(x=270, y=20)
            bt_search.config(command=print_choice)
            # 返回按钮
            bt_back = Button(frame, text="返回", width=10, relief=RAISED)
            bt_back.place(x=460, y=460)
            bt_back.config(command=click_back)
        else:
            tkinter.messagebox.showinfo(title='注意', message='未选择历史记录')

    # 返回按钮绑定函数
    def click_back():
        # 关闭查看详情页面
        frame_clear(frame)
        run2(frame)

    tree.bind('<<TreeviewSelect>>', focus)
    # 选择按钮
    bt = Button(frame, text="选择查看", width=10, relief=RAISED)
    bt.place(x=250, y=460)
    bt.config(command=click)


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
    login(frame_login)
    # menu(frame_login, frame_menu, frame_run)

    root.mainloop()
