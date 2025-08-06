import functools
import asyncio
from time import time

def timer(func):
    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            st = time()
            result = await func(*args, **kwargs)
            print(f"[async] elapsed time for '{func.__name__}': {time() - st:.4f}s")
            return result
        return async_wrapper
    else:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            st = time()
            result = func(*args, **kwargs)
            print(f"[sync] elapsed time for '{func.__name__}': {time() - st:.4f}s")
            return result
        return sync_wrapper
