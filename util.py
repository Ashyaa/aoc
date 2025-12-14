from functools import wraps
from time import perf_counter


def show(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = perf_counter()
        result = f(*args, **kw)
        te = perf_counter()
        print(f"{f.__name__}() = {result}")
        print(f"Runtime: {(te - ts):.09f}s")
        print()
        return result

    return wrap
