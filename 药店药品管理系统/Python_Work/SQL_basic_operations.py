from SQL import *

class SQL_basic_operations:
    """
    sql数据库基础操作类，在程序第一次初始化时检测数据库
    创建初始表
    插入初始数据
    创建触发器
    创建存储过程
    创建视图
    创建索引
    """
    def __init__(self, sql: SQL):
        # 参数为需要初始化的数据库
        self.sql = sql;

    def create_basic_table(self):
        # 创建初始表
        with open('D:\Python\药店药品管理系统\药店药品管理系统\SQL_Server_Work\建表.sql', encoding='utf-8', mode='r') as f:
            sql_creat_list = f.read().split('\n')
            self.sql._write_in("\n".join(sql_creat_list[3:58]))
            f.close()

    def insert_basic_data(self):
        # 插入初始数据
        with open('D:\Python\药店药品管理系统\药店药品管理系统\SQL_Server_Work\插入数据.sql', encoding='utf-8', mode='r') as f:
            sql_insert_data = f.read().split('\n')
            sql_insert_med = "\n".join(sql_insert_data[3:14])
            sql_insert_emp = "\n".join(sql_insert_data[15:21])
            sql_insert_cli = "\n".join(sql_insert_data[22:34])
            self.sql._write_in(sql_insert_med)
            self.sql._write_in(sql_insert_emp)
            self.sql._write_in(sql_insert_cli)
            f.close()

    def create_trigger(self):
        # 创建触发器
        with open('D:\Python\药店药品管理系统\药店药品管理系统\SQL_Server_Work\创建触发器.sql', encoding='utf-8', mode='r') as f:
            sql_creat_trigger = f.read().split('\n')
            self.sql._write_in("\n".join(sql_creat_trigger[4:18]))
            f.close()

    def create_stored_procedure(self):
        # 创建存储过程
        with open('D:\Python\药店药品管理系统\药店药品管理系统\SQL_Server_Work\创建存储过程.sql', encoding='utf-8', mode='r') as f:
            sql_creat_sp = f.read().split('\n')
            sql_sp_medicine = "\n".join(sql_creat_sp[5:10]) # sp_medicine以药品名称为参数，查看药品信息
            sql_sp_employee = "\n".join(sql_creat_sp[14:19]) # sp_employee以员工名称为参数，查看员工信息
            sql_sp_client_trade = "\n".join(sql_creat_sp[23:28]) # sp_client_trade以客户姓名为参数，查看交易信息
            sql_sp_medicine_storage = "\n".join(sql_creat_sp[32:37]) # sp_medicine_storage建立以数量和药品名称，插入新添加的药品信息
            sql_sp_trade_record = "\n".join(sql_creat_sp[43:45]) # sp_trade_record建立以客户姓名，药品名称，药品数量为参数，插入新的交易信息
            self.sql._write_in(sql_sp_medicine)
            self.sql._write_in(sql_sp_employee)
            self.sql._write_in(sql_sp_client_trade)
            self.sql._write_in(sql_sp_medicine_storage)
            self.sql._write_in(sql_sp_trade_record)
            f.close()

    def create_views(self):
        # 创建视图
        with open('D:\Python\药店药品管理系统\药店药品管理系统\SQL_Server_Work\创建视图.sql', encoding='utf-8', mode='r') as f:
            sql_creat_view = f.read().split('\n')
            sql_view_med_emp = "\n".join(sql_creat_view[3:7])
            sql_view_med_cli = "\n".join(sql_creat_view[11:15])
            sql_view_med_emp2 = "\n".join(sql_creat_view[19:23])
            sql_view_emp_man = "\n".join(sql_creat_view[27:32])
            sql_view_cli_emp = "\n".join(sql_creat_view[36:39])
            sql_view_cli_tra = "\n".join(sql_creat_view[43:47])
            self.sql._write_in(sql_view_med_emp)
            self.sql._write_in(sql_view_med_cli)
            self.sql._write_in(sql_view_med_emp2)
            self.sql._write_in(sql_view_emp_man)
            self.sql._write_in(sql_view_cli_emp)
            self.sql._write_in(sql_view_cli_tra)
            f.close()

    def create_indices(self):
        # 建立索引
        with open('D:\Python\药店药品管理系统\药店药品管理系统\SQL_Server_Work\建立索引.sql', encoding='utf-8', mode='r') as f:
            sql_creat_index = f.read().split('\n')
            self.sql._write_in("\n".join(sql_creat_index[1:4]))
            f.close()

    @staticmethod
    def do_all():
        sql = SQL(host='(local)', user='sa', pwd='123456', db='mmdb')
        sqlbo = SQL_basic_operations(sql)
        sqlbo.create_basic_table()
        sqlbo.insert_basic_data()
        sqlbo.create_trigger()
        sqlbo.create_stored_procedure()
        sqlbo.create_views()
        sqlbo.create_indices()

# if __name__ == '__main__':
#     sql = SQL(host='(local)', user='sa', pwd='123456', db='mmdb')
#     sqlbo = SQL_basic_operations(sql)
#     sqlbo.create_basic_table()
#     sqlbo.insert_basic_data()
#     sqlbo.create_trigger()
#     sqlbo.create_stored_procedure()
#     sqlbo.create_views()
#     sqlbo.create_indices()
#     rows = sql._write_out("select * from medicine_employee")
#     print(rows)
