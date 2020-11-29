use 药品存销信息管理系统
go

--创建交易触发器tri_in_med
create trigger tri_out_med
on trade_record
for insert
as
begin
	declare @a int;
	declare @Mno char(4);
	select @Mno = Mno from inserted
	select @a = cbuynumber from inserted
	update medicine set	Outnumber = Outnumber + @a
	where Mno = @Mno
	update medicine set Storage = Storage - @a
	where Mno = @Mno
end
--删除触发器
drop trigger tri_out_med
--调试触发器
insert into trade_record values
('0001','0001','2019-12-20',2)

