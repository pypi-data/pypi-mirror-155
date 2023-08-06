import copy

from annosSQL.annosSQL.Innos.Interface import IOCHandler
from annosSQL.annosSQL.Donos.docache import CacheHandler
from annosSQL.annosSQL.Donos.doconn import Connection, ExecSQL


class ContextParameterError(Exception):pass
class SQLSyntaxAndParameterError(Exception):pass


class CheckUpSql():
    def __init__(self):pass
    @classmethod
    def SqlAllhandler(self,sql) -> str:return sql
    @classmethod
    def ASqlhandler(self,sql) -> str:
        table=sql.split(" ")[1]
        sql='select * from '+table
        return sql
    @classmethod
    def ISqlhandler(self,sql,p,args,kwargs) -> str:
        if not dict(p).__contains__("S") or p['S'].__name__!='str':
            raise SQLSyntaxAndParameterError(
                'Syntax error or parameter error: %s' % (p)
            )
        sql=str(sql)
        l=sql.index('S{')
        h=sql.index('}')
        step=sql[l+2:h]
        value=str(args[0].split(',')).replace('[',"").replace(']',"")
        if sql.find('[')!=-1:
            j=sql[sql.find('[')+1:sql.find(']')]
            sql=sql[:sql.find('[')]+sql[sql.find(']')+1:]
            j=j.split(',')
            ap=list(args[0].split(step))
            for i in j:
                ap[int(i) - 1] = int(ap[int(i) - 1])
            value=str(ap).replace('[',"").replace(']',"")
        return sql[:l]+value+sql[h+1:]

    @classmethod
    def LSqlhandler(self,sql,p,args,kwargs):
        if not dict(p).__contains__("L") or p['L'].__name__ != 'list':
            raise SQLSyntaxAndParameterError(
                'Syntax error or parameter error: %s' % (p)
            )
        sql = str(sql)
        l = sql.index('L{')
        h = sql.index('}')
        date=str(args[0]).replace('[', "").replace(']', "")
        return sql[:l] + date + sql[h + 1:]
    @classmethod
    def ISSqlhandler(self,sql,p,args,kwargs):
        if not dict(p).__contains__("T") or p['T'].__name__ != 'list' and p['T'].__name__ != 'tuple':
            raise SQLSyntaxAndParameterError(
                'Syntax error or parameter error: %s' % (p)
            )
        sql=str(sql).replace("T{","").replace("}","")
        data=None
        if len(args)!=0:
            data=args[0]
        if len(kwargs)!=0:
            data=kwargs[list(p.keys())[0]]
        return (sql,data)

class SqlGenerate():
    def __init__(self) -> None:pass

    def __call__(self, fun,*args, **kwargs):
        fun=self.sqlhandler
        return fun
    def checkup(self):
        def _w(obj,sql,p,args,kwargs):
            if len(p)==0 and sql.find("#{")==-1 and sql.find("}")  ==-1 and not 'A(select)'.lower() in sql.lower():
                return CheckUpSql.SqlAllhandler(sql)
            if len(p)==0 and 'A(select)'.lower() in sql.lower():
                return CheckUpSql.ASqlhandler(sql)
            if 'insert' in sql.lower() and 'S{' in sql:
                return CheckUpSql.ISqlhandler(sql,p,args,kwargs)
            if 'L{}' in sql:
                return CheckUpSql.LSqlhandler(sql,p,args,kwargs)
            if dict(p)[list(p.keys())[0]].__name__ in ['list','tuple'] and 'T{' and '%s' in sql:
                return CheckUpSql.ISSqlhandler(sql,p,args,kwargs)
            return self(obj,sql, p, args, kwargs)
        return _w

    @checkup
    def sqlhandler(self,sql,p,args,kwargs) -> str:
        parm=p.keys()
        key=list(p.keys())
        if  not tuple(args) and not  dict(kwargs):
            raise ContextParameterError(
                'Context parameter error: %s or %s' %
                (str(args),str(kwargs))
            )

        if len(parm)==len(args):
            parm=[i for i in args]
        if len(parm)==len(kwargs):
            parm=kwargs
        if len(parm)==len(args)+len(kwargs):
            T=[]
            [T.append(i) for i in args if args]
            [T.append(kwargs[i]) for i in kwargs]
            parm=T
        for i in range(0,len(parm)):
            if p[key[i]].__name__== "str":
                sql = str(sql).replace('{%s}' % (i + 1), "'{parm[%s]}'" % (i))
            else:
                sql=str(sql).replace('{%s}' % (i+1), '{parm[%s]}' % (i))
        sql=sql.format(parm=parm).replace("#",'')
        return sql

class TypeSQL():
    def __init__(self):pass
    def __call__(self, fun,*args, **kwargs):
        fun=self.returnType
        return fun
    def returnType(self,sql) -> object:
        if 'select' in sql.lower():
            return "select"
        if 'insert' in sql.lower():
            return "insert"
        if 'update' in sql.lower():
            return "update"
        if 'delete' in sql.lower():
            return 'delete'
        return 'other'

class execute():
    def __init__(self, sql, driver='mysql',cacheDriver=dict,*args, **kwargs) -> any:
        self.sql = sql
        self.sqlType = None
        self.driver=driver.lower()
        self.cla=None
        self.cacheSize=10 #空间大小
        self.cacheBit=0 #当前占用空间
        self.access=0  #最近访问的缓存空间
        self.accessNot=0 #最久访问
        self.cache={}  #缓存空间
        # self.logicTable=[]  #缓存逻辑表
        self.physicsTable=[] #缓存地址表
        self.id_cursor=0
    def __call__(self, fun,*args, **kwargs) -> type:
        self.cla=fun

        # print(fun.__annotations__)
        fun=self.fun
        self.__ioc__(self)
        return fun

    @IOCHandler()
    def __ioc__(self) -> None:pass
    def fun(self) -> any:pass
    def result(self, *args, **kwargs) -> any:return self

    def sqlHandler(self,*args,**kwargs) -> result:
        self.sqlType=self.TypeHandler(self.sql)
        parm=list(self.cla.__annotations__.keys())
        p = copy.deepcopy(self.cla.__annotations__)
        parm_count=len(args)+len(kwargs)
        if dict(self.cla.__annotations__).__contains__('return'):
            parm.remove('return')
            del p['return']
        if len(parm) != parm_count:
            raise ContextParameterError(
                'The function expects to get parameter %s and now gets %s' %
                (str(len(parm)),str(parm_count))
            )
        currentSql=self.syntaxHandler(self.sql,p,args,kwargs)
        data=self.cache_pool(self,currentSql)

        return data
    @SqlGenerate()
    def syntaxHandler(self) -> str:pass

    @Connection.connect
    def connect_pool(self,driver) -> any: pass

    @CacheHandler()
    def cache_pool(self,fun,sql) -> any:pass

    @ExecSQL()
    def execSql(self,sql) -> any:pass

    @TypeSQL()
    def TypeHandler(self,sql) -> str:pass

    def mapping(self, result): return result





