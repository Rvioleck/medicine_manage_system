import emoji
import pickle
import pymssql
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from SQL import *
from Medicine import *
from Employee import *
from Client import *
from Trade import  *
from SQL_basic_operations import *

class MainFrame:
    def __init__(self, sql: SQL):
        self.sql = sql
        # SQL_basic_operations.do_all()

    def login(self):
        # 主界面
        login_menu = Tk()
        login_menu.title("欢迎使用药品信息管理系统！")
        login_menu.geometry('400x380')
        # 图片
        canvas = Canvas(login_menu, width=400, heigh=135, bg='white')
        img_file = PhotoImage(file='D:\Python\药店药品管理系统\药店药品管理系统\Python_Work\medicine.png')
        img = canvas.create_image(200, 0, anchor='n', image=img_file)
        canvas.pack(side='top')
        # 标签提示
        test = emoji.emojize(':hospital: 欢迎使用药品信息管理系统 :ambulance:', use_aliases=True)
        Label(login_menu, text=test, font=("仿宋", 18, 'bold')).pack(pady=5)
        Label(login_menu, text="请 输 入 账 号 密 码", font=("Arial", 16, 'bold')).pack(pady=5)
        # 账号提示与输入框
        f1 = Frame(login_menu)
        var_user_name = StringVar()
        var_user_name.set("fyz1831050115")
        Label(f1, text="账号: ", width=5, font=("Arial", 13)).pack(side=LEFT)
        Entry(f1, textvariable=var_user_name, font=("Times New Roman", 13)).pack(side=LEFT)
        # Entry(f1, textvariable=var_user_name, font=("Times New Roman", 13), state='disabled').pack(side=LEFT)
        f1.pack(pady=5)
        # 密码提示与输入框
        f2 = Frame(login_menu)
        var_user_pwd = StringVar()
        var_user_pwd.set("123456")
        Label(f2, text="密码: ", width=5, font=("Arial", 13)).pack(side=LEFT)
        Entry(f2, textvariable=var_user_pwd, font=("Times New Roman", 13), show='*').pack(side=LEFT)
        f2.pack(pady=10)

        def user_login():
            # 获取用户输入的usr_name和usr_pwd
            user_name = var_user_name.get()
            user_pwd = var_user_pwd.get()
            # 这里设置异常捕获，当我们第一次访问用户信息文件时是不存在的，所以这里设置异常捕获。
            # 中间的两行就是我们的匹配，即程序将输入的信息和文件中的信息匹配。
            try:
                with open('users_info.pickle', 'rb') as user_file:
                    users_info = pickle.load(user_file)
            except FileNotFoundError:
                # 这里就是我们在没有读取到`user_file`的时候，程序会创建一个`user_file`这个文件，并将管理员
                # 的用户和密码写入，即用户名为`admin`密码为`admin`。
                with open('users_info.pickle', 'wb') as user_file:
                    users_info = {'admin': 'admin'}
                    pickle.dump(users_info, user_file)
                    user_file.close()  # 必须先关闭，否则pickle.load()会出现EOFError: Ran out of input

            # 如果用户名和密码与文件中的匹配成功，则会登录成功，并跳出弹窗how are you? 加上你的用户名。
            if user_name in users_info:
                if user_pwd == users_info[user_name]:
                    messagebox.showinfo(title='登陆成功', message='您好！用户：' + user_name)
                    login_menu.destroy()
                    self.main()
                # 如果用户名匹配成功，而密码输入错误，则会弹出'Error, your password is wrong, try again.'
                else:
                    messagebox.showerror(message='您的密码输入错误！')
            else:  # 如果发现用户名不存在
                is_sign_up = messagebox.askyesno('用户名不存在', '您还未注册，是否现在注册？')
                # 提示需不需要注册新用户
                if is_sign_up:
                    user_sign_up()

        bframe = Frame(login_menu)
        button_login = Button(bframe, text='登录', command=user_login)
        button_login.pack(side=LEFT, padx=10)

        def user_sign_up():
            def sign_to():
                # 获取注册时所输入的信息
                np = new_pwd.get()
                npf = new_pwd_confirm.get()
                nn = new_name.get()
                # 这里是打开我们记录数据的文件，将注册信息读出
                with open('users_info.pickle', 'rb') as user_file:
                    exist_user_info = pickle.load(user_file)
                # 这里就是判断，如果两次密码输入不一致，则提示错误
                if np != npf:
                    messagebox.showerror('错误', '两次输入不一致！')
                # 如果用户名已经在我们的数据文件中，则提示错误
                elif nn in exist_user_info:
                    messagebox.showerror('错误', '用户名已被注册！')
                # 最后如果输入无以上错误，则将注册输入的信息记录到文件当中，并提示注册成功，然后销毁窗口。
                else:
                    exist_user_info[nn] = np
                    with open('users_info.pickle', 'wb') as user_file:
                        pickle.dump(exist_user_info, user_file)
                    messagebox.showinfo('成功', '注册成功！')
                    # 然后销毁窗口。
                    window_sign_up.destroy()

            # 定义长在窗口上的窗口
            window_sign_up = Toplevel(login_menu)
            window_sign_up.geometry('300x200')
            window_sign_up.title('注册')

            new_name = StringVar()  # 将输入的注册名赋值给变量
            new_name.set('fyz1831050115')
            Label(window_sign_up, text='用户名: ').place(x=10, y=10)  # 将`User name:`放置在坐标（10,10）。
            entry_new_name = Entry(window_sign_up, textvariable=new_name)  # 创建一个注册名的`entry`，变量为`new_name`
            entry_new_name.place(x=130, y=10)  # entry放置在坐标(150,10)

            new_pwd = StringVar()
            Label(window_sign_up, text='密码：').place(x=10, y=50)
            entry_user_pwd = Entry(window_sign_up, textvariable=new_pwd, show='*')
            entry_user_pwd.place(x=130, y=50)

            new_pwd_confirm = StringVar()
            Label(window_sign_up, text='再次输入密码: ').place(x=10, y=90)
            entry_user_pwd_confirm = Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
            entry_user_pwd_confirm.place(x=130, y=90)

            btn_comfirm_sign_up = Button(window_sign_up, text='注册', command=sign_to)
            btn_comfirm_sign_up.place(x=180, y=120)

        button_sign_up = Button(bframe, text='注册', command=user_sign_up)
        button_sign_up.pack(side=LEFT, padx=10)
        bframe.pack(pady=10)
        login_menu.mainloop()


    def main(self):
        main_menu = Tk()
        main_menu.title("药店药品管理系统")
        main_menu.iconbitmap("D:\Python\药店药品管理系统\药店药品管理系统\Python_Work\药品.ico")
        main_menu.geometry('480x710')
        """总页分为三个分页"""
        tabControl = Notebook(main_menu)
        med_tab = Frame(tabControl)
        emp_tab = Frame(tabControl)
        cli_tab = Frame(tabControl)

        tabControl.add(med_tab, text='药品存销管理页面', padding=5)
        tabControl.add(emp_tab, text='管理员权限页面', padding=5)
        tabControl.add(cli_tab, text='客户信息管理页面', padding=5)
        tabControl.pack(expand=True, fill=BOTH)
        """
        med_tab药品信息窗口
        """
        medicine = Medicine(sql=self.sql)
        # 药品信息查询窗口
        med_select_frame = LabelFrame(med_tab, text='药品信息查询', labelanchor="nw")
        frame1 = Frame(med_select_frame)
        Label(frame1, text="药品名称:", font=("仿宋", 12)).pack(side=LEFT, padx=5, pady=10)
        med_name = StringVar()
        Entry(frame1, textvariable=med_name, font=("仿宋", 12)).pack(side=LEFT, padx=10)
        frame1.pack(padx=5)
        Style().configure('my.TButton', font=("微软雅黑", 10))
        # Button(med_select_frame, command=lambda: medicine.select('medicine', med_name.get()), text='查询', style='my.TButton').pack(pady=10)
        Button(frame1, command=lambda: medicine.select(med_name.get(), 'medicine'),
                       text='查询', style='my.TButton').pack(pady=10,side=LEFT)
        emoji_text = emoji.emojize(':star2::star: 所有查询 :star::star2:', use_aliases=True)
        sub_select_frame = LabelFrame(med_select_frame, text=emoji_text, labelanchor='n')
        Button(sub_select_frame, command=lambda: medicine.select(op='medicine_all'),
                                 text='查询所有\n药品信息',
                                 style='my.TButton').pack(padx=30, pady=10)
        sub_select_frame.pack(pady=10)
        med_select_frame.pack(pady=10)

        # 图片
        img_frame = Frame(med_tab)
        img_frame.pack()
        img_file = PhotoImage(file='D:\Python\药店药品管理系统\药店药品管理系统\Python_Work\药.png')
        Label(img_frame, image=img_file).pack(side=LEFT)
        img_file2 = PhotoImage(file='D:\Python\药店药品管理系统\药店药品管理系统\Python_Work\药剂.png')
        Label(img_frame, image=img_file2).pack(side=LEFT)
        img_file3 = PhotoImage(file='D:\Python\药店药品管理系统\药店药品管理系统\Python_Work\药瓶.png')
        Label(img_frame, image=img_file3).pack(side=LEFT)

        # 药品信息修改窗口
        med_alter_frame = LabelFrame(med_tab, text='药品出库入库', labelanchor='nw')
        Label(med_alter_frame, text=emoji.emojize('药品进货入库\n     :hospital::arrow_left::pill:', use_aliases=True), font=("微软雅黑", 14)).pack()
        frame_base1 = Frame(med_alter_frame)
        frame1 = Frame(frame_base1)
        sub_frame1 = Frame(frame1)
        Label(sub_frame1, text="药品名称:", font=("仿宋", 12)).pack(side=LEFT, padx=5, pady=10)
        med_name2 = StringVar()
        Entry(sub_frame1, textvariable=med_name2, font=("仿宋", 12)).pack(padx=10, side=LEFT)
        sub_frame1.pack()
        sub_frame2 = Frame(frame1)
        Label(sub_frame2, text="入库数量:", font=("仿宋", 12)).pack(side=LEFT, padx=5, pady=10)
        med_in_number = StringVar()
        Entry(sub_frame2, textvariable=med_in_number, font=("仿宋", 12)).pack(side=LEFT, padx=10)
        sub_frame2.pack()
        frame1.pack(padx=5, side=LEFT)
        Button(frame_base1, command=lambda: medicine.alter(med_name2.get(), med_in_number.get(), 'in'),
                                text='修改',
                                style='my.TButton').pack(pady=10, side=LEFT)
        frame_base1.pack()
        Label(med_alter_frame, text=emoji.emojize('药品售卖出库\n     :hospital::arrow_right::pill:', use_aliases=True), font=("微软雅黑", 14)).pack()

        frame_base1 = Frame(med_alter_frame)
        frame1 = Frame(frame_base1)
        sub_frame1 = Frame(frame1)
        Label(sub_frame1, text="药品名称:", font=("仿宋", 12)).pack(side=LEFT, padx=5, pady=10)
        med_name3 = StringVar()
        Entry(sub_frame1, textvariable=med_name3, font=("仿宋", 12)).pack(padx=10, side=LEFT)
        sub_frame1.pack()
        sub_frame2 = Frame(frame1)
        Label(sub_frame2, text="出库数量:", font=("仿宋", 12)).pack(side=LEFT, padx=5, pady=10)
        med_out_number = StringVar()
        Entry(sub_frame2, textvariable=med_out_number, font=("仿宋", 12)).pack(side=LEFT, padx=10)
        sub_frame2.pack()
        frame1.pack(padx=5, side=LEFT)
        Button(frame_base1, command=lambda: medicine.alter(med_name3.get(), med_out_number.get(), 'out'),
               text='修改',
               style='my.TButton').pack(pady=10, side=LEFT)
        frame_base1.pack()

        med_alter_frame.pack(pady=10)
        """
        emp_tab管理员窗口
        """
        employee = Employee(sql=self.sql)
        # 管理员权限,修改药品价格
        emp_alter_med_frame = LabelFrame(emp_tab, text='药品信息修改', labelanchor='nw')
        emp_alter_med_frame.pack(padx=20, pady=10)
        emp_alter_price_frame = LabelFrame(emp_alter_med_frame, text="药品价格修改", labelanchor='n')
        emp_alter_price_frame.pack(padx=20, pady=10)
        frame_info = Frame(emp_alter_price_frame)
        frame_info.pack(side=LEFT)
        sub_frame1 = Frame(frame_info)
        sub_frame1.pack()
        Label(sub_frame1, text="药品名称：", font=("仿宋", 12), width=9).pack(side=LEFT, padx=5, pady=10)
        med_name4 = StringVar()
        Entry(sub_frame1, textvariable = med_name4, font=("仿宋", 12)).pack(side=LEFT, padx=10)
        sub_frame2 = Frame(frame_info)
        sub_frame2.pack()
        Label(sub_frame2, text="价格(元)：", font=("仿宋", 12), width=9).pack(side=LEFT, padx=5, pady=10)
        med_price = StringVar()
        Entry(sub_frame2, textvariable=med_price, font=("仿宋", 12)).pack(side=LEFT, padx=10)
        Button(emp_alter_price_frame, command=lambda: employee.alter(med_name4.get(), med_price.get(), 'price_alter'),
                           text="修改", style='my.TButton').pack(pady=10, side=LEFT)
        # 管理员权限，删除药品信息
        emp_delete_med_frame = LabelFrame(emp_alter_med_frame, text="药品信息删除", labelanchor='n')
        emp_delete_med_frame.pack(padx=20, pady=10)
        frame_info2 = Frame(emp_delete_med_frame)
        frame_info2.pack()
        Label(frame_info2, text="药品名称：", font=("仿宋", 12), width=9).pack(side=LEFT, padx=5, pady=10)
        med_name5 = StringVar()
        Entry(frame_info2, textvariable=med_name5, font=("仿宋", 12)).pack(side=LEFT, padx=10)
        Button(frame_info2, command=lambda: employee.alter(med_name5.get(), op='delete'),
               text="删除", style='my.TButton').pack(pady=10, side=LEFT)

        # 图片
        img_frame2 = Frame(emp_tab)
        img_frame2.pack()
        img_file4 = PhotoImage(file='D:\Python\药店药品管理系统\药店药品管理系统\Python_Work\男性-管理员.png')
        Label(img_frame2, image=img_file4).pack(side=LEFT,padx=25)
        img_file5 = PhotoImage(file='D:\Python\药店药品管理系统\药店药品管理系统\Python_Work\女性-管理员.png')
        Label(img_frame2, image=img_file5).pack(side=LEFT,padx=25)


        # 查询管理员信息
        emp_info_frame = LabelFrame(emp_tab, text='员工信息操作', labelanchor="nw")
        emp_info_frame.pack(padx=20, pady=10)
        emp_delete_info_frame = LabelFrame(emp_info_frame, text='员工信息查询', labelanchor='n')
        emp_delete_info_frame.pack(padx=20, pady=10)

        frame_cb = Frame(emp_delete_info_frame)
        frame_cb.pack(pady=5)
        var_sex = IntVar()
        var_age = IntVar()
        var_edu = IntVar()
        var_posi = IntVar()
        Checkbutton(frame_cb,
                    text="员工性别",
                    variable=var_sex,
                    onvalue=1,
                    offvalue=0).pack(padx=5, side=LEFT)
        Checkbutton(frame_cb,
                    text="员工年龄",
                    variable=var_age,
                    onvalue=1,
                    offvalue=0).pack(padx=5, side=LEFT)
        Checkbutton(frame_cb,
                    text="员工学历",
                    variable=var_edu,
                    onvalue=1,
                    offvalue=0).pack(padx=5, side=LEFT)
        Checkbutton(frame_cb,
                    text="员工职位",
                    variable=var_posi).pack(padx=5, side=LEFT)
        def get_vars():
            return [var_sex.get(), var_age.get(), var_edu.get(), var_posi.get()]

        frame0 = Frame(emp_delete_info_frame)
        frame0.pack()
        Label(frame0, text="员工姓名：", font=("仿宋", 12), width=9).pack(side=LEFT, padx=5, pady=10)
        emp_name = StringVar()
        Entry(frame0, textvariable=emp_name, font=("仿宋", 12)).pack(side=LEFT, padx=10)
        Button(frame0, command=lambda: [employee.select(name=emp_name.get(), vars=get_vars(), op='employee')],
               text="查询", style='my.TButton').pack(pady=10, side=LEFT)

        emoji_text2 = emoji.emojize(':star2::star: 所有查询 :star::star2:', use_aliases=True)
        sub_select_frame2 = LabelFrame(emp_delete_info_frame, text=emoji_text2, labelanchor='n')
        Button(sub_select_frame2, command=lambda: employee.select(vars=get_vars(), op='employee_all'),
                                 text='查询所有\n员工信息',
                                 style='my.TButton').pack(padx=30, pady=10)
        sub_select_frame2.pack(pady=10)
        """
        cli_tab客户信息窗口
        """
        client = Client(sql=self.sql)
        # 客户信息查询窗口
        cli_select_frame = LabelFrame(cli_tab, text='客户信息查询', labelanchor="nw")
        frame1 = Frame(cli_select_frame)
        Label(frame1, text="客户姓名:", font=("仿宋", 12)).pack(side=LEFT, padx=5, pady=10)
        cli_name = StringVar()
        Entry(frame1, textvariable=cli_name, font=("仿宋", 12)).pack(side=LEFT, padx=10)
        frame1.pack(padx=5)
        Style().configure('my.TButton', font=("微软雅黑", 10))
        Button(frame1, command=lambda: client.select(cli_name.get(), 'client'),
               text='查询', style='my.TButton').pack(pady=10, side=LEFT)
        emoji_text = emoji.emojize(':star2::star: 所有查询 :star::star2:', use_aliases=True)
        sub_select_frame2 = LabelFrame(cli_select_frame, text=emoji_text, labelanchor='n')
        Button(sub_select_frame2, command=lambda: client.select(op='client_all'),
               text='查询所有\n客户信息',
               style='my.TButton').pack(padx=30, pady=10)
        sub_select_frame2.pack(pady=10)
        cli_select_frame.pack(pady=10)
        # 客户交易记录录入窗口
        cli_trade_record_frame = LabelFrame(cli_tab, text='交易记录录入', labelanchor="nw")
        cli_trade_record_frame.pack()
        frame_cli_med = Frame(cli_trade_record_frame)
        frame_cli = Frame(frame_cli_med)
        Label(frame_cli, text="客户编号:", font=("仿宋", 12)).pack(side=LEFT, padx=5, pady=10)
        cli_no = StringVar()
        Entry(frame_cli, textvariable=cli_no, font=("仿宋", 12)).pack(side=LEFT, padx=10)
        frame_med = Frame(frame_cli_med)
        Label(frame_med, text="药品编号:", font=("仿宋", 12)).pack(side=LEFT, padx=5, pady=10)
        med_no = StringVar()
        Entry(frame_med, textvariable=med_no, font=("仿宋", 12)).pack(side=LEFT, padx=10)
        frame_med_num = Frame(frame_cli_med)
        Label(frame_med_num, text="药品数量:", font=("仿宋", 12)).pack(side=LEFT, padx=5, pady=10)
        med_num = StringVar()
        Entry(frame_med_num, textvariable=med_num, font=("仿宋", 12)).pack(side=LEFT, padx=10)
        frame_cli_med.pack(side=LEFT)
        frame_med.pack()
        frame_cli.pack()
        frame_med_num.pack()
        Button(cli_trade_record_frame, command=lambda: client.alter(cli_no.get(), med_no.get(), med_num.get()),
               text='记录', style='my.TButton').pack(pady=10, side=LEFT)

        # 客户交易信息查询打印
        trade = Trade(sql=self.sql)
        trade_record_select_print_frame = LabelFrame(cli_tab, text='交易记录查询打印', labelanchor="nw")
        trade_record_select_print_frame.pack(pady=10)
        cli_select_print_frame = LabelFrame(trade_record_select_print_frame, text="客户记录", labelanchor="nw")
        cli_select_print_frame.pack(padx=48, pady=10)
        frame_cli_p = Frame(cli_select_print_frame)
        frame_cli_p.pack()
        Label(frame_cli_p, text="客户姓名:", font=("仿宋", 12)).pack(side=LEFT, padx=5, pady=10)
        cli_name2 = StringVar()
        Entry(frame_cli_p, textvariable=cli_name2, font=("仿宋", 12)).pack(side=LEFT, padx=10)
        frame_cli_b = Frame(cli_select_print_frame)
        frame_cli_b.pack()
        Button(frame_cli_b, command=lambda: trade.select(cli_name2.get(), "client"),
               text='查询', style='my.TButton').pack(padx=5, pady=10, side=LEFT)
        Button(frame_cli_b, command=lambda: trade.print(cli_name2.get(), "client"),
               text='打印', style='my.TButton').pack(padx=5, pady=10, side=LEFT)

        med_select_print_frame = LabelFrame(trade_record_select_print_frame, text="药品记录", labelanchor="nw")
        med_select_print_frame.pack(padx=48, pady=10)
        frame_med_p = Frame(med_select_print_frame)
        frame_med_p.pack()
        Label(frame_med_p, text="药品名称:", font=("仿宋", 12)).pack(side=LEFT, padx=5, pady=10)
        med = StringVar()
        Entry(frame_med_p, textvariable=med, font=("仿宋", 12)).pack(side=LEFT, padx=10)
        frame_med_b = Frame(med_select_print_frame)
        frame_med_b.pack()
        Button(frame_med_b, command=lambda: trade.select(med.get(), "medicine"),
               text='查询', style='my.TButton').pack(padx=5, pady=10, side=LEFT)
        Button(frame_med_b, command=lambda: trade.print(med.get(), "medicine"),
               text='打印', style='my.TButton').pack(padx=5, pady=10, side=LEFT)
        """菜单条，注销和退出"""
        menu_bar = Menu(main_menu)
        filemenu = Menu(menu_bar, tearoff=0)
        filemenu.add_command(label='注销', command= lambda :[main_menu.destroy(), self.login()])
        filemenu.add_command(label='退出', command = main_menu.destroy)
        menu_bar.add_cascade(label='用户', menu=filemenu)

        main_menu.config(menu=menu_bar)
        main_menu.mainloop()


if __name__ == '__main__':
    # 数据库的基础操作
    # SQL_basic_operations.do_all()
    mf = MainFrame(sql=SQL(host='(local)', user='sa', pwd='123456', db='mmdb'))
    mf.login()
