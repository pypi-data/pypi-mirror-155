import sys

from annosSQL.test.tesys import Ut001

u=Ut001()
u.handler()
data1=u.allUser()
data2=u.iduser(1)
# r=u.inserts("cai,0987654321,9")
print(data2)
print(data1)
# print(sys.modules)
# d2=u.Tinsert([('qqq','qewqwrqr',19),('jjjj','1232141',88)])
# print(d2)