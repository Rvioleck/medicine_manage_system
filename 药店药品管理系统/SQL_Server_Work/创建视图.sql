use 药品存销信息管理系统
go
--创建药品信息视图1用于员工进行药品信息查询
create view medicine_employee
as select Mno '药品编号',Mname '药品名称',Manu '制造商', Prodate '生产日期',
Shelflife '保质期',Usage '用途',Price '价格',Storage '存量',location '存放位置'
from medicine

select * from medicine_employee

--创建药品信息视图2用于客户进行药品信息查询
create view medicine_client
as select  Mno '药品编号',Mname '药品名称',Manu '制造商',
Prodate '生产日期',Shelflife '保质期',Usage '用途',Price '价格'
from medicine

select * from medicine_client

--创建药品出入库交易信息用于员工进行查询
create view medicine_employee2
as select Mno '药品编号',Mname '药品名称',
Storage '存量', Innumber '累计入库数量',Outnumber '累计出库数量'
from medicine

select * from medicine_employee2

--创建员工信息视图用于经理查询
create view employee_manager
as select  A.Eno '员工编号',A.Ename '员工姓名',A.Esex '员工性别',
A.Eage '员工年龄',A.Education '员工学历',A.Epno '经理编号',B.Ename '经理姓名'
from employee A,employee B
where A.Eposition = '员工' and A.Epno =B.Eno

select * from employee_manager

--创建客户信息视图用于员工查询
create view client_employee
as select Cno '客户编号',Cname '客户姓名',Cphone '客户联系电话'
from client

select * from client_employee

--创建交易记录视图
create view client_trade
as select Cname, Mname, Cbuytime, Cbuynumber
from trade_record, client, medicine
where trade_record.Cno = client.Cno and trade_record.Mno = medicine.Mno