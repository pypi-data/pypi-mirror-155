import time

from annosSQL.Innos.Interface import Interface, Handler
from annosSQL.Donos.doconn import Connection
from annosSQL.Donos.dosql import execute


@Interface()
class Ut001():
    @Handler()
    def handler(self)->list:pass

    @Connection(driver="mysql",host="127.0.0.1",user="root",password="123456",port=3306,database="czh")
    def conn(self) -> any:pass

    @execute(sql='select * from user where id=#{1} and name=#{2}')
    def p(self,id:int,name:str) -> list:pass

    @execute(sql="select * from user")
    def pp(self) -> list:pass

    @execute(sql="A(select) user")
    def ppp(self,A) -> list: pass

    @execute(sql="insert into table values(S{,}[1,2])")
    def p4(self, S:str) -> list: pass

    @execute(sql="insert into table values(L{})")
    def p5(self, L: list) -> list: pass

    @execute(sql='select * from aoa_user where user_id=#{1}')
    def test(self, id: int) -> list: pass

    @execute(sql='A(select) aoa_user')
    def test2(self, A) -> list: pass

    @execute(sql='insert into user(user,password,z) values(S{,}[3])')
    def inserts(self,S:str) -> list:pass

    @execute(sql="A(Select) user")
    def allUser(self,A)->dict:pass

    @execute(sql="select * from  user where id={1}")
    def iduser(self, id:int) -> dict: pass








    # @execute(sql='select * from user where id=#{2}')
    # def pp(self, i: int, ii: int) -> list: pass
    # #{} %s {}
    # #{}、 {} 普通占位符
    # %s 多行占位符 支持数据多行数据类型：列表与元组
    # select * from  ->  A(select) user
    # insert into table values(S{,}[])
    # insert into table values(C{})
    # insert into table values(L{})
    # insert into table values(T{%s,%s})

    @execute("insert into user (user,password,z) values(T{%s,%s,%s})")
    def Tinsert(self,T:list) -> int:pass



if __name__=='__main__':
    tt=time.time()
    s=Ut001()
    # print(id(s))
    s.handler()
    # print(s.conn())
    t=time.time()
    data=s.test(1)
    print(time.time()-t)

    t=time.time()
    data2=s.test(2)
    data3 = s.test(5)
    print(time.time()-t)

    t=time.time()
    data=s.test(1)
    print(time.time()-t)


    # data3=s.test2()
    print(data)
    print(data2)
    # print(data3)
    # s.inserts('chx10,123456,10')
    print(time.time()-tt)

#     0.0011932849884033203 0.002812623977661133



