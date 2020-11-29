from SQL import *
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

class Medicine:
    def __init__(self, sql: SQL):
        self.sql = sql

    def select(self, nameVar="", op=""):
        """
        查询药品信息，op="medicine"为特定查找
                   op="medicine_all"为全体查找
        """
        if op == 'medicine':
            """展示特定药品查询结果"""
            name = nameVar.strip()
            rows = self.sql._write_out("exec sp_medicine \'{}\'".format(name))
            # rows = [('0001', '参胶胶囊',...,)]
            if name == "":
                messagebox.showerror("错误", message="请输入药品名称！")
                return
            if len(rows) == 0:
                messagebox.showerror("错误", message="未查询到{}".format(name))
                return
            show_one = Tk()
            show_one.iconbitmap(".\\药品.ico")
            show_one.title("查询结果")
            show_lframe = LabelFrame(show_one, text="{}的查询结果".format(name), labelanchor='n')

            info = zip(rows[0], ('药品编号', '药品名称', '制造商', '生产日期', '保质期', '用途', '价格(元)', '存量(瓶)', '存放位置'), range(9))
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
        elif op == 'medicine_all':
            """展示所有药品查询结果"""
            rows = self.sql._write_out("""select Mno '药品编号',Mname '药品名称',Manu '制造商', Prodate '生产日期',
                                                Shelflife '保质期',Usage '用途',Price '价格',Storage '存量',location '存放位置'
                                                from medicine""")
            show_all = Tk()
            show_all.iconbitmap(".\\药品.ico")
            show_all.title("查询结果")
            tree_med = Treeview(show_all, show="headings", height=18)
            tree_med["column"] = ('药品编号', '药品名称', '制造商', '生产日期', '保质期', '用途', '价格', '库存量', '存放位置')
            # 设置列宽度
            tree_med.column('药品编号', width=80, anchor=CENTER)
            tree_med.column('药品名称', width=80, anchor=CENTER)
            tree_med.column('制造商', width=80, anchor=CENTER)
            tree_med.column('生产日期', width=200, anchor=CENTER)
            tree_med.column('保质期', width=200, anchor=CENTER)
            tree_med.column('用途', width=200, anchor=W)
            tree_med.column('价格', width=100, anchor=CENTER)
            tree_med.column('库存量', width=100, anchor=CENTER)
            tree_med.column('存放位置', width=100, anchor=CENTER)
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

            for col in ('药品编号', '药品名称', '制造商', '生产日期', '保质期', '用途', '价格', '库存量', '存放位置'):
                tree_med.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree_med, _col, False))
            tree_med.pack()


    def alter(self, med_name: str, number: str, op: str):
        if med_name == '' or number == '':
            messagebox.showerror("错误", message="请输入完整信息！")
            return
        if number.isdigit() == False:
            messagebox.showerror("错误", message="请输入正确的数字！")
            return
        number = int(number)
        if op == 'in':
            # exec sp_medicine_storage 2,'参胶胶囊'
            isError = self.sql._write_in("exec sp_medicine_storage {},\'{}\'".format(number, med_name))
            if isError != "error":
                messagebox.showinfo("成功", message="成功使{}的库存增加{}瓶".format(med_name, number))

        elif op == 'out':
            # update medicine set storage = storage - 2
            # where Mname = '参胶胶囊'
            isError = self.sql._write_in("update medicine set storage = storage - {}"
                               "where Mname = \'{}\'".format(number, med_name))
            if isError != "error":
                messagebox.showinfo("成功", message="成功使{}的库存减少{}瓶".format(med_name, number))