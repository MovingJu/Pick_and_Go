def timer(func):
    def wrapper(*args, **kwargs):
        from time import time
        st = time()
        result = func(*args, **kwargs)
        print(f"elapsed time for function '{func.__name__}': {time() - st:.4f}s")
        return result
    return wrapper
