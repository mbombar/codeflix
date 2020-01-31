import time

import re

def timeit(method):
    """
    Decorator used to time the execution of a function.
    """
    def timed(*args, **kwargs):
        ts = time.time()
        result = method(*args, **kwargs)
        te = time.time()
        print('%r  %2.2f ms' %
              (method.__name__, (te - ts) * 1000))
        return result
    return timed


def camel_to_snake(name):
    """
    Convert a name in CamelCase to snake_case.
    Example:
       * CamelCaseName --> camel_case_name
    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def dict_camel_to_snake(dict):
    """
    Convert a dictionary whose keys are in CamelCase to the very same dictionary, but with keys in snake_case
    """
    return {camel_to_snake(k): v for k, v in dict.items()}
