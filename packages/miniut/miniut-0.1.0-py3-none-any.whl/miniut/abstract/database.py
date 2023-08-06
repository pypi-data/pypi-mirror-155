import functools

from miniut.metaclasses import SingletonMeta



class DBAbs(metaclass=SingletonMeta):

    def session(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            self.open_cxnx()
            val = func(*args, **kwargs)
            self.close_cxnx()
            return val
        return wrapper

    def open_cxnx(self):
        raise NotImplemented()

    def close_cxnx(self):
        raise NotImplemented()
