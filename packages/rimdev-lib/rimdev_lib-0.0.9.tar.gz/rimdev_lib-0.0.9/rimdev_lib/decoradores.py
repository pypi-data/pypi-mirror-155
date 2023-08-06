import time
from datetime import datetime
import os
from types import FunctionType

def process_batch(*args, **kwargs):
    if len(args) > 0 and type(args[0]) is FunctionType:
        return __decorador(args[0])
    else:
        if len(args) == 1:
            return __decorador_param(args[0])
        elif len(args) > 1:
            raise Exception("Too many arguments")

        if 'log' in kwargs:
            return __decorador_param(kwargs['log'])
        elif 'log_name' in kwargs:
            return __decorador_param(kwargs['log_name'])
        else:
            raise Exception("No log name received")

def __decorador_param(log_name: str = None):
    def wrapper(func):
        def subwrapper(*args, **kwargs):
            print(f'path: {os.path.abspath(log_name)}')
            start = time.time()
            print(f"[{datetime.now()}] - Inicia la ejecución de {func.__name__}")
            result = func(*args, **kwargs)
            print(f'[{datetime.now()}] - Finaliza la ejecución de {func.__name__}, demoró {time.time() - start} segundos')
            return result
        return subwrapper
    return wrapper

def __decorador(func):
    def subwrapper(*args, **kwargs):
        print(f'path: {os.path.realpath(__file__)}')
        start = time.time()
        print(f"[{datetime.now()}] - Inicia la ejecución de {func.__name__}")
        result = func(*args, **kwargs)
        print(f'[{datetime.now()}] - Finaliza la ejecución de {func.__name__}, demoró {time.time() - start} segundos')
        return result
    return subwrapper
