from SQL import *
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

class Employee:
    def __init__(self, sql: SQL):
        self.sql = sql

    def select(self, name="", vars=[], op=""):
        if op == 'employee':
            if name == "":
                messagebox.showerror("错误", message="请输入员工姓名！")
                return
            rows = self.sql._write_out("exec sp_employee \'{}\'".format(name))
            if len(rows) == 0:
                messagebox.showerror("错误", message="未查询到{}".format(name))
                return
            show_one = Tk()
            show_one.iconbitmap(".\\药品.ico")
            show_one.title("查询结果")
            show_lframe = LabelFrame(show_one, text="{}的查询结果".format(name), labelanchor='n')
            info = zip(rows[0], ('员工编号', '员工姓名', '员工性别', '员工年龄', '员工学历', '员工职务'), range(6))
            var_s = []
            for row, label, i in info:
                var = StringVar(show_one, value=row)
                var_s.append(var)
                if i < 2 or vars[i - 2] == 1:
                    frame_out = Frame(show_lframe)
                    Label(frame_out, text=label + ": ", font=("仿宋", 12), width=10).pack(padx=5, pady=5, side=LEFT)
                    Entry(frame_out, textvariable=var_s[i], font=("Times New Roman", 12), width=20, state='disabled').pack(
                        padx=5, pady=5, side=LEFT)
                    frame_out.pack(padx=5, pady=5)
            show_lframe.pack(padx=20, pady=20)
            show_one.mainloop()

        elif op == 'employee_all':
            """展示所有员工信息结果"""
            # rows = self.sql._write_out("""select Mno '药品编号',Mname '药品名称',Manu '制造商', Prodate '生产日期',
            #                                                 Shelflife '保质期',Usage '用途',Price '价格',Storage '存量',location '存放位置'
            #                                                 from medicine""")
            rows = self.sql._write_out("""select Eno '员工编号',Ename '员工姓名',Esex '员工性别',
                                          Eage '员工年龄',Education '员工学历',Eposition '员工职务'
                                          from employee""")
            show_all = Tk()
            show_all.iconbitmap(".\\药品.ico")
            show_all.title("查询结果")
            tree_med = Treeview(show_all, show="headings", height=18)
            tree_med["column"] = ('员工编号', '员工姓名', '员工性别', '员工年龄', '员工学历', '员工职务')
            # 设置列宽度
            tree_med.column('员工编号', width=80, anchor=CENTER)
            tree_med.column('员工姓名', width=80, anchor=CENTER)
            tree_med.column('员工性别', width=80, anchor=CENTER)
            tree_med.column('员工年龄', width=200, anchor=CENTER)
            tree_med.column('员工学历', width=200, anchor=CENTER)
            tree_med.column('员工职务', width=200, anchor=CENTER)
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

            for col in ('员工编号', '员工姓名', '员工性别', '员工年龄', '员工学历', '员工职务'):
                tree_med.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree_med, _col, False))
            tree_med.pack()

    def alter(self, name: str, var="", op=""):
        """
        修改药品价格，op="price_alter"
        删除药品信息，op="delete"
        """
        if name == '':
            messagebox.showerror("错误", message="请输入完整信息！")
            return
        if op == 'price_alter':
            # update medicine set price = var
            # where Mname = 'name'
            if var.isdigit() == False:
                messagebox.showerror("错误", message="请输入正确的数字！")
                return
            number = int(var)
            isError = self.sql._write_in("update medicine set price = {}"
                                         "where Mname = \'{}\'".format(number, name))
            if isError != "error":
                messagebox.showinfo("成功", message="成功使{}价格更改为{}元".format(name, number))
        elif op == 'delete':
            # delete from medicine
            # where Mname = 'name'
            isError = self.sql._write_in("delete from medicine "
                                         "where Mname = \'{}\'".format(name))
            if isError != "error":
                messagebox.showinfo("成功", message="成功删除药品{}的信息".format(name))

