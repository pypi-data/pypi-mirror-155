import functools
from datetime import datetime as dt


def singleton(cls):
    """Make a class a Singleton class (only one instance)"""
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if not wrapper.instance:
            wrapper.instance = cls(*args, **kwargs)
        return wrapper.instance
    wrapper.instance = None
    return wrapper


def ttime(func):
    """Calculate execution time for a function"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = dt.now()
        value = func(*args, **kwargs)
        final_time = dt.now() - start_time
        return  final_time.total_seconds(), value
    return wrapper
