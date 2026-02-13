from datetime import datetime
from functools import wraps

def function_logger(filepath):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = datetime.now()
            result = func(*args, **kwargs)
            end = datetime.now()
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(f"{func.__name__}\n")
                f.write(f"{start}\n")
                if args and kwargs:
                    f.write(f"{args}\n{kwargs}\n")
                elif args:
                    f.write(f"{args}\n")
                elif kwargs:
                    f.write(f"{kwargs}\n")
                f.write(f"{result if result is not None else '-'}\n")
                f.write(f"{end}\n")
                f.write(f"{end - start}\n")
            return result
        return wrapper
    return decorator

if __name__ == '__main__':
    @function_logger('test.log')
    def greeting_format(name):
        return f'Hello, {name}!'

    greeting_format('John')
