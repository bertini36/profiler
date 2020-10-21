# -*- coding: UTF-8 -*-

import time

from loguru import logger


def timeit(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        logger.info(f'Time {func.__name__}: {round(t2-t1, 2)}s')
        return result

    return wrapper
