import time
from functools import wraps
def fn_timer(func):
    @wraps(func)
    def function_timer(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        t1 = time.perf_counter()
        elapsed_time = t1 - t0
        print(f"Total time running {func.__name__}: {elapsed_time:.2f} seconds")
        return result, elapsed_time

    return function_timer