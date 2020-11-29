use 药品存销信息管理系统
go

--客户管理模块
--查询部分药品信息
select Mno '药品编号',Mname '药品名称',Manu '生产厂家',
Prodate '生产日期',Shelflife '保质期', Usage '用途',Price '价格'
from medicine

--修改交易信息
exec trade_record_info '0002','0001',5

--查询交易信息
select * from trade_record
