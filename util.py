from functools import wraps
from datetime import datetime


def show(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = datetime.now()
        result = f(*args, **kw)
        te = datetime.now()
        print(f"{f.__name__}() = {result}")
        print(f"Runtime: {te-ts}s")
        print()
        return result
    return wrap