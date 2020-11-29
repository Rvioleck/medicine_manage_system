use mmdb
go

create table employee		--员工表
(
	Eno nvarchar(4) not null primary key,          --员工编号
	Epno nvarchar(4),                              --员工经理编号
	Ename nvarchar(10) not null,                --员工姓名
	Esex nvarchar(2) not null,                     --员工性别
	Eage int not null,                         --员工年龄
	Education nvarchar(10) not null,            --员工学历
	Eposition nvarchar(10) not null             --员工职务
)
alter table employee add constraint fk_employee foreign key(Epno) references employee(Eno) ON DELETE NO ACTION
alter table employee add constraint ck1_employee check(Eno like '[0-9][0-9][0-9][0-9]')
alter table employee add constraint ck2_employee check(Epno like '[0-9][0-9][0-9][0-9]')
alter table employee add constraint ck3_employee check(Esex like '男'or Esex like '女')
alter table employee add constraint ck4_employee check(Eposition like '员工'or Eposition like '经理')


create table medicine		--药品表
(
	Mno nvarchar(4) not null primary key,  --药品编号
	Eno nvarchar(4),                       --员工编号
	Mname nvarchar(20) not null unique, --药品名称
	Manu nvarchar(10) not null,    --制造商
	Prodate datetime not null,  --生产日期
	Shelflife datetime not null,  --保质期
	Usage nvarchar(40),              --用途
	Price int,                      --价格
	Storage int,                    --存量
	location nvarchar(20),       --存放位置
	Innumber int,			--累计入库数量
	Outnumber int			--累计出库数量
)
alter table medicine add constraint fk_medicine foreign key(Eno) references Employee(Eno) ON DELETE CASCADE
alter table medicine add constraint ck1_medicine check(Mno like '[0-9][0-9][0-9][0-9]')
alter table medicine add constraint ck2_medicine check(Eno like '[0-9][0-9][0-9][0-9]')

create table client			--客户记录表
(
	Cno nvarchar(4) not null primary key,       --客户编号
	Cname nvarchar(10) not null,				--客户名字
	Cphone nvarchar(11) not null                --客户电话
)
alter table client add constraint ck1_client check(Cno like '[0-9][0-9][0-9][0-9]')
alter table client add constraint ck2_client check(Cphone like '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]')

create table trade_record   --交易记录表
(
	Cno nvarchar(4) not null check(Cno like '[0-9][0-9][0-9][0-9]'), --客户编号
	Mno nvarchar(4) not null check(Mno like '[0-9][0-9][0-9][0-9]'), --药品编号
	Cbuytime datetime not null,									 --购买药品的时间
	Cbuynumber int not null,                                     --购买药品的数量
)
alter table trade_record add constraint fk_tr1 foreign key(Cno) references Client(Cno) ON DELETE CASCADE
alter table trade_record add constraint fk_tr2 foreign key(Mno) references medicine(Mno) ON DELETE CASCADE
ALTER TABLE trade_record ADD oid int identity(1,1)  PRIMARY KEY;


	