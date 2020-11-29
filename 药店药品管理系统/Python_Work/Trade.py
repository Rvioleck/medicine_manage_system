from SQL import *
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import xlwt
import os
import sys

class Trade:
    def __init__(self, sql: SQL):
        self.sql = sql

    def select(self, name="", op=""):
        if op == 'client':
            if name == "":
                messagebox.showerror("错误", message="请输入信息！")
                return
            name = name.strip()
            rows = self.sql._write_out("""select * from client_trade
                                          where Cname = \'{}\'""".format(name))
            show_all = Tk()
            show_all.iconbitmap(".\\药品.ico")
            show_all.title("查询结果")
            tree_med = Treeview(show_all, show="headings", height=18)
            tree_med["column"] = ('客户姓名', '药品名称', '购买时间', '购买数量')
            # 设置列宽度
            tree_med.column('客户姓名', width=80, anchor=CENTER)
            tree_med.column('药品名称', width=80, anchor=CENTER)
            tree_med.column('购买时间', width=280, anchor=CENTER)
            tree_med.column('购买数量', width=100, anchor=CENTER)
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

            for col in ('客户姓名', '药品名称', '购买时间', '购买数量'):
                tree_med.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree_med, _col, False))
            tree_med.pack()

        elif op == 'medicine':
            if name == "":
                messagebox.showerror("错误", message="请输入信息！")
                return
            name = name.strip()
            rows = self.sql._write_out("""select * from client_trade
                                          where Mname = \'{}\'""".format(name))
            show_all = Tk()
            show_all.iconbitmap(".\\药品.ico")
            show_all.title("查询结果")
            tree_med = Treeview(show_all, show="headings", height=18)
            tree_med["column"] = ('客户姓名', '药品名称', '购买时间', '购买数量')
            # 设置列宽度
            tree_med.column('客户姓名', width=80, anchor=CENTER)
            tree_med.column('药品名称', width=80, anchor=CENTER)
            tree_med.column('购买时间', width=280, anchor=CENTER)
            tree_med.column('购买数量', width=100, anchor=CENTER)
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

            for col in ('客户姓名', '药品名称', '购买时间', '购买数量'):
                tree_med.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree_med, _col, False))
            tree_med.pack()


    def print(self, name="", op=""):
        if op == 'client':
            if name == "":
                messagebox.showerror("错误", message="请输入信息！")
                return
            name = name.strip()
            rows = self.sql._write_out("""select * from client_trade
                                           where Cname = \'{}\'""".format(name))
            wb = xlwt.Workbook()
            sheet1 = wb.add_sheet(name)
            sheet1.write(0,0,'客户姓名')
            sheet1.write(0,1,'药品名称')
            sheet1.write(0,2,'购买时间')
            sheet1.write(0,3,'购买数量')
            try:
                for i in range(len(rows)):
                    for j in range(len(rows[i])):
                        sheet1.write(i+1,j,str(rows[i][j]))
                wb.save(name + "购买记录.xls")
                messagebox.showinfo("成功", "成功输出文件到"+sys.path[0]+"\{}购买记录.xls".format(name))
            except:
                messagebox.showerror("异常", "打印错误！")

        elif op == 'medicine':
            if name == "":
                messagebox.showerror("错误", message="请输入信息！")
                return
            name = name.strip()
            rows = self.sql._write_out("""select * from client_trade
                                           where Mname = \'{}\'""".format(name))
            wb = xlwt.Workbook()
            sheet1 = wb.add_sheet(name)
            sheet1.write(0,0,'客户姓名')
            sheet1.write(0,1,'药品名称')
            sheet1.write(0,2,'购买时间')
            sheet1.write(0,3,'购买数量')
            try:
                for i in range(len(rows)):
                    for j in range(len(rows[i])):
                        sheet1.write(i+1,j,str(rows[i][j]))
                wb.save(name + "出售记录.xls")
                messagebox.showinfo("成功", "成功输出文件到"+sys.path[0]+"\{}出售记录.xls".format(name))
            except:
                messagebox.showerror("异常", "打印错误！")