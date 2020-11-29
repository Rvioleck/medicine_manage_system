--给三个基本表建立唯一索引，均按照编号升序的顺序
create unique index medMno on medicine(Mno)
create unique index employEno on employee(Eno)
create unique index clientCno on client(Cno)
