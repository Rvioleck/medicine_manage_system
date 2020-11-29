from SQL import *
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

class Client:
    def __init__(self, sql: SQL):
        self.sql = sql

    def select(self, name = "", op=""):
        """
        查询客户信息，op="client"为特定查找
                   op="client_all"为全体查找
        """
        if op == 'client':
            """展示特定客户查询结果"""
            name = name.strip()
            rows = self.sql._write_out("select * from client where Cname = \'{}\'".format(name))
            # rows = [('0001', '参胶胶囊',...,)]
            if name == "":
                messagebox.showerror("错误", message="请输入客户姓名！")
                return
            if len(rows) == 0:
                messagebox.showerror("错误", message="未查询到{}".format(name))
                return
            show_one = Tk()
            show_one.iconbitmap(".\\药品.ico")
            show_one.title("查询结果")
            show_lframe = LabelFrame(show_one, text="{}的查询结果".format(name), labelanchor='n')

            info = zip(rows[0], ('客户编号', '客户姓名', '客户联系电话'), range(3))
            var_s = []
            for row, label, i in info:
                var = StringVar(show_one, value=row)
                var_s.append(var)
                frame_out = Frame(show_lframe)
                Label(frame_out, text=label + ": ", font=("仿宋", 12), width=10).pack(padx=5, pady=5, side=LEFT)
                Entry(frame_out, textvariable=var_s[i], font=("Times New Roman", 12), width=20, state='disabled').pack(
                    padx=5, pady=5, side=LEFT)
                frame_out.pack(padx=5, pady=5)
            show_lframe.pack(padx=20, pady=20)
            show_one.mainloop()
        elif op == 'client_all':
            """展示所有药品查询结果"""
            rows = self.sql._write_out("""select * from client_employee""")
            show_all = Tk()
            show_all.iconbitmap(".\\药品.ico")
            show_all.title("查询结果")
            tree_med = Treeview(show_all, show="headings", height=18)
            tree_med["column"] = ('客户编号', '客户姓名', '客户联系电话')
            # 设置列宽度
            tree_med.column('客户编号', width=80, anchor=CENTER)
            tree_med.column('客户姓名', width=80, anchor=CENTER)
            tree_med.column('客户联系电话', width=100, anchor=CENTER)
            # 插入数据
            for j, row in enumerate(rows):
                row = [str(i).strip() for i in row]
                tree_med.insert("", j, values=row)

            # 点击排序treeview
            def treeview_sort_column(tv, col, reverse):  # Treeview、列名、排列方式
                l = [(tv.set(k, col), k) for k in tv.get_children('')]
                print(tv.get_children(''))
                # 排序方式 如果是数字的话按照数字排序，是字符串的话，按照字符串排序
                l.sort(key=lambda t: int(t[0]) if str(t[0]).strip().isdigit() else str(t[0]), reverse=reverse)
                # rearrange items in sorted positions
                for index, (val, k) in enumerate(l):  # 根据排序后索引移动
                    tv.move(k, '', index)
                    print(k)
                tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

            for col in ('客户编号', '客户姓名', '客户联系电话'):
                tree_med.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree_med, _col, False))
            tree_med.pack()

    def alter(self, cli_no, med_no, med_num):
        if cli_no == "" or med_no == "" or med_num == "":
            messagebox.showerror("错误", message="请输入完整记录！")
            return
        if med_num.isdigit() == False:
            messagebox.showerror("错误", message="请输入正确的药品数量！")
            return
        # exec sp_trade_record '0001','0001',3
        isError = self.sql._write_in("exec sp_trade_record \'{}\',\'{}\',{}".format(cli_no, med_no, med_num))
        if isError != "error":
            messagebox.showinfo("成功", message="成功录入信息！")