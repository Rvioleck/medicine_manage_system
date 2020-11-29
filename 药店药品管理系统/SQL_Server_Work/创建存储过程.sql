use 药品存销信息管理系统
go

--建立存储过程
--建立药品名称作为参数的存储过程查看药品信息
create procedure sp_medicine(@Mname varchar(20))
as select Mno '药品编号',Mname '药品名称',Manu '制造商', Prodate '生产日期',
Shelflife '保质期',Usage '用途',Price '价格',Storage '存量',location '存放位置'
from medicine
where @Mname = Mname

exec sp_medicine '参胶胶囊'

--建立员工姓名作为参数的存储过程查看员工信息
create procedure sp_employee(@Ename varchar(10))
as select Eno '员工编号',Ename '员工姓名',Esex '员工性别',
Eage '员工年龄',Education '员工学历',Eposition '员工职务'
from employee
where @Ename = Ename

exec sp_employee '马云昊'

--建立客户姓名作为参数的存储过程查看客户信息和其交易记录
create procedure sp_client_trade(@Cname varchar(10))
as select client.Cno '客户编号',client.Cname '客户姓名',client.Cphone '客户联系电话',Mname'客户购买药品',
Cbuytime '客户购买时间',Cbuynumber '客户购买数量'
from client,trade_record,medicine
where @Cname = Cname and trade_record.Cno = client.Cno and trade_record.Mno = medicine.Mno

exec sp_client_trade '马冬梅'

--建立含参数的存储过程更新药品库存
create procedure sp_medicine_storage(@num int,@Mname varchar(20))
as update medicine set Storage = Storage + @num
where @Mname = Mname and Mname in (select Mname from medicine)
update medicine set Innumber = Innumber + @num
where @Mname = Mname and Mname in (select Mname from medicine)
--删除存储
drop procedure sp_medicine_storage
--调试存储
exec sp_medicine_storage 2,'参胶胶囊'

--建立以trade_record表的字段为参数的存储过程trade_record_info以插入交易记录
create procedure sp_trade_record(@Cno char(4),@Mno char(4),@Cbuynumber int)
as insert into trade_record values (@Cno,@Mno,GETDATE(),@Cbuynumber)
--删除存储
drop procedure sp_trade_record
--调试存储
exec sp_trade_record '0001','0001',3




