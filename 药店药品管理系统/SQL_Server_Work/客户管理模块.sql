use ҩƷ������Ϣ����ϵͳ
go

--�ͻ�����ģ��
--��ѯ����ҩƷ��Ϣ
select Mno 'ҩƷ���',Mname 'ҩƷ����',Manu '��������',
Prodate '��������',Shelflife '������', Usage '��;',Price '�۸�'
from medicine

--�޸Ľ�����Ϣ
exec trade_record_info '0002','0001',5

--��ѯ������Ϣ
select * from trade_record
