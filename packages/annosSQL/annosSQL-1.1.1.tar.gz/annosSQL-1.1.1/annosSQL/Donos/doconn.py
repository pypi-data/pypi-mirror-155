import sys
from itertools import chain

import pymysql

class ConnectClassDriverLoadError(Exception):pass

class ChooseDriver():
    def __init__(self) -> None:
        self.fun=None
    def __call__(self, fun,*args, **kwargs):
        self.fun=fun
        fun=self.choose
        return fun
    def choose(self,obj) -> object:
        try:
            return getattr(obj,obj.driver)()
        except Exception as e:
            raise ConnectClassDriverLoadError(
                'Connection error, the driver cannot be found or is not supported: %s' %
                (e)
            )

class Connection():
    def __init__(self,driver,*args,**kwargs) -> None:
        self.driver=driver.lower()
        self.args=args
        self.kwargs=kwargs
        self.conn=None
        self.fun=None

    def __call__(self, fun,*args, **kwargs):
        self.fun=fun
        self.create_conn(self)
        fun=self.result
        return fun
    def __ioc__(self) -> None:pass

    def result(self) -> object:return self.conn

    @ChooseDriver()
    def create_conn(self) -> object:pass

    def mysql(self) -> object:
            self.conn=pymysql.connect(
                host=self.kwargs['host'],
                user=self.kwargs['user'],
                password=self.kwargs['password'],
                port=self.kwargs['port'],
                database=self.kwargs['database']
            )
            sys.modules[str(self.fun).split(" ")[1].split('.')[0]+"."+self.__class__.__module__+'.'+self.__class__.__name__+'-mysql']=self.conn

    def oracle(self) -> object:pass

    def sqlLite(self) -> object:pass

    @classmethod
    def connect(self,fun):
        def _w(obj,driver,*args,**kwargs):
            if not sys.modules.__contains__(str(obj.cla).split(' ')[1].split('.')[0]+'.'+self.__module__+'.'+self.__name__+'-'+driver):
                raise ConnectClassDriverLoadError(
                    'Connection information not found: %s' % (str(obj.cla).split(' ')[1].split('.')[0]+'.'+self.__module__+'.'+self.__name__+'-'+driver)
                )
            conn = sys.modules[str(obj.cla).split(' ')[1].split('.')[0]+'.'+self.__module__+'.'+self.__name__+'-'+driver]
            return conn
        return _w

class ExecSQL():
    def __init__(self):pass
    def __call__(self, fun,*args, **kwargs):
        fun=self.exec
        return fun
    def exec(self,fun,sql) ->any:
        if fun.driver=='mysql':
            if isinstance(sql,str):
                return self.execMySql(fun, sql, fun.driver)
            else:
                return self.execMySql1(fun,sql,fun.driver)
        if fun.driver=='oracle':
            pass
        if fun.driver=='sqllite':
            pass

    def execMySql(self,fun,sql,driver) -> any:
        returnType = fun.cla.__annotations__['return']
        conn = fun.connect_pool(driver)
        cur_type=None
        try:
            if returnType.__name__ == 'dict':
                cur_type =pymysql.cursors.DictCursor
            cursor=conn.cursor(cursor=cur_type)
            reint=cursor.execute(sql)
            conn.commit()
            result=cursor.fetchall()
            if returnType.__name__ == 'list':
                return list(chain.from_iterable(result))
            if returnType.__name__ == 'int':
                return reint
            if returnType.__name__ == 'bool':
                if reint>0:
                    return True
                else:
                    return False
            return result
        except Exception as e:
            conn.rollback()
            raise e
    def execMySql1(self,fun,parm,driver) -> any:
        returnType = fun.cla.__annotations__['return']
        cur_type = None
        sql,data=parm[0],parm[1]
        conn = fun.connect_pool(driver)
        try:
            if returnType.__name__ == 'dict':
                cur_type =pymysql.cursors.DictCursor
            cursor=conn.cursor(cursor=cur_type)
            reint=cursor.executemany(sql,data)
            conn.commit()
            result=cursor.fetchall()
            if returnType.__name__ == 'list':
                return list(chain.from_iterable(result))
            if returnType.__name__ == 'dict':
                return result
            if returnType.__name__ == 'bool':
                if reint>0:
                    return True
                else:
                    return False
            return reint
        except Exception as e:
            conn.rollback()
            raise e












