from functools import wraps
from time import sleep


def retry_on_network_error(times):
    def wrapper_fn(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    print(f"Error, `{e}`")
                    sleep(0.1)
                    # err = e
            return ""
        return wrapper
    return wrapper_fn
