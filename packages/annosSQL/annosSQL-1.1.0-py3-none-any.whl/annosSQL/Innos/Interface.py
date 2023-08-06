import sys

from annosSQL.annosSQL.Donos.doconn import Connection


class InterfaceClassSyntaxError(Exception):
    """Raised when adding API names to symbol that already has API names."""
    pass

class Interface():
    def __init__(self, *args, **kwargs) -> any:
        self.handlerNUm=0
        self.connNUm=0

    def __call__(self, fun, *args, **kwargs) -> type:
        filter_k = ['__module__', '__dict__', '__weakref__', '__doc__']
        for i in vars(fun).keys():
            if i in '__init__':
                raise InterfaceClassSyntaxError(
                    'Use @Interface annosSQL is not require realization %s() method.' %
                    (i))
            if i not in filter_k and '__self__' in dir(vars(fun).get(i)) and isinstance(vars(fun).get(i).__self__,Connection):
                vars(getattr(fun, i)).setdefault("fun", fun)
                self.connNUm+=1
                continue
            if i not in filter_k and '__self__' in dir(vars(fun).get(i)) and isinstance(vars(fun).get(i).__self__,Handler):
                vars(getattr(fun, i)).setdefault("fun", fun)
                self.handlerNUm+=1
                continue
            if i not in filter_k and not self.isEmptyFunction(getattr(fun, i)):
                raise InterfaceClassSyntaxError(
                    'The method %s.%s() should be an empty function.' %
                    (fun.__name__, i)
                )
            if i not in filter_k and not dict(getattr(fun, i).__annotations__).__contains__("return"):
                raise InterfaceClassSyntaxError(
                    'This method %s.%s() return type not defined,Correct definition: def %s(parameter:any): -> type:pass' %
                    (fun.__name__, i, i)
                )
        if self.handlerNUm<=0 or self.connNUm<=0:
            raise InterfaceClassSyntaxError(
                '%s class not found  handler method for annotation @handler or @Connection.' %
                (fun.__name__)
            )
        return fun

    @property
    def empty(self) -> None:pass
    def isEmptyFunction(self, func):
        e = lambda: None
        return func.__code__.co_code == e.__code__.co_code

class Handler():
    def __init__(self, *args, **kwargs) -> None:
        self.fun = None
    def __call__(self, fun, *args, **kwargs) -> object:
        fun.__globals__['Handler'] = fun.__name__
        fun = self.handler
        self.fun = fun
        return fun

    def __class__(self):return self
    def handler(self):
        filter_k = ['__module__', '__dict__', '__weakref__', '__doc__']
        try:
            cla=vars(self.fun)['fun']
            k_list=list(vars(cla).keys())
            [k_list.remove(i) for i in filter_k]
            for k in k_list:
                if not isinstance(vars(cla).get(k).__self__,Handler) and not isinstance(vars(cla).get(k).__self__,Connection):
                    z=vars(cla).get(k).__self__
                    _tmp=sys.modules[cla.__name__+'-'+z.__class__.__module__+'-'+z.__class__.__name__]
                    l='''cla.%s = _tmp['%s'].sqlHandler''' % (k, k)
                    exec(l)
            return cla
        except Exception as e:
            raise InterfaceClassSyntaxError(
                'Interface type not found %s. @Interface' % (e)
            )

class IOCHandler():
    def __init__(self) -> None:pass
    def __call__(self, fun,*args, **kwargs) -> object:
        fun=self.ioc_handler
        return fun
    def ioc_handler(self,obj):
        if not dict(sys.modules).__contains__(str(obj.cla).split(' ')[1].split('.')[0]+'-'+obj.__class__.__module__ + '-' + obj.__class__.__name__):
            # sys.modules[obj.__class__.__module__ + '-' + obj.__class__.__name__] = {}
            sys.modules[str(obj.cla).split(' ')[1].split('.')[0]+'-'+obj.__class__.__module__ + '-' + obj.__class__.__name__]={}
        # tmp = sys.modules[obj.__class__.__module__ + '-' + obj.__class__.__name__]
        # tmp[obj.cla.__name__] = obj
        # sys.modules[obj.__class__.__module__ + '-' + obj.__class__.__name__] = tmp
        tmp2=sys.modules[str(obj.cla).split(' ')[1].split('.')[0]+'-'+obj.__class__.__module__ + '-' + obj.__class__.__name__]
        tmp2[obj.cla.__name__] = obj
        sys.modules[str(obj.cla).split(' ')[1].split('.')[0]+'-'+obj.__class__.__module__ + '-' + obj.__class__.__name__] = tmp2



