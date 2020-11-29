import pymssql
from tkinter import messagebox

class SQL:
    """
    数据库类
    连接数据库
    写入操作：建表，插入数据，
    """
    def __init__(self, host, user, pwd, db):
        # 构造函数参数数据库：(本地)服务器，用户名，密码，数据库
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    # def __create_database(self):
    #     self.conn = pymssql.connect(host=self.host, user=self.user,
    #                                     password=self.pwd)
    #     cur = self.conn.cursor();
    #     cur.execute("create database " + self.db)
    #     cur.close()
    #     self.conn.close()
    #     print("成功创建表" + self.db)

    def __get_connect(self):
        # 进行数据库连接并且返回游标
        try:
            # 打开数据库连接
            self.conn = pymssql.connect(host=self.host, user=self.user,
                                        password=self.pwd, database=self.db)
            print("成功连接数据库: " + self.db);
            # 创建cursor游标
            cur = self.conn.cursor()
            if not cur:
                raise(NameError, "Failed to connect!")
            else:
                # 返回操作游标
                print("成功返回游标")
                return cur
        except pymssql.OperationalError as error:
            print("There is no datebase named: " + self.db);

    def _write_in(self, sql_in):
        try:
            cur = self.__get_connect()
            # 执行数据库更改语句
            cur.execute(sql_in)
            # 提交到数据库执行
            self.conn.commit()
            # print("Successfully write in the information!")
            print("成功写入数据！")
            # 关闭游标和数据库连接
            cur.close()
            self.conn.close()
        except pymssql.OperationalError as error:
            # (2714, b"There is already an object named 'employee' in the database.DB-Lib error message 20018, severity 16:"
            #        b"General SQL Server error: Check messages from the SQL Server\n")
            # if error.args[0] not in ( 2627, 1913):
            messagebox.showerror("错误", message="请检查输入的药品名称是否正确！")
            print(error.args)
            return "error"
        except pymssql.IntegrityError as error:
            # if error.args[0] == 2627:
            #     # 2627为重复字段返回的错误
            #     print("插入的数据无效！")
            # else:
            # if error.args[0] != 2627:
            messagebox.showerror("错误", message="请检查输入的药品名称是否正确！")
            print(error.args)
            return "error"
        except:
            messagebox.showerror("错误", message="未知的错误！")
            return "error"

    def _write_out(self, sql_out):
        try:
            cur = self.__get_connect()
            # 执行数据库更改语句
            cur.execute(sql_out)
            # 获取查询结果
            rows = cur.fetchall()
            # 关闭游标和数据库连接
            cur.close()
            self.conn.close()
            return rows
        except pymssql.OperationalError as error:
            # if error.args[0] not in (2714, 2627, 1913):
            messagebox.showerror("错误", message="请检查输入的药品名称是否正确！")
            print(error.args)
            return "error"
        except pymssql.IntegrityError as error:
            messagebox.showerror("错误", message="请检查输入的药品名称是否正确!")
            print(error.args)
            return "error"


# if __name__ == '__main__':
#
#     sql = SQL(host='(local)', user='sa', pwd='123456', db='mmdb')
#     # sql_creat = creat_table()
#     rows = sql._write_out("select * from employee_manager")
#     print(rows)