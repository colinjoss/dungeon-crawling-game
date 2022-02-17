import time
import functools


def func_timer(func):
    """Decorator that times how long it takes for a function to complete."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(elapsed_time)
    return wrapper
