import asyncio
import functools
import time
from typing import Callable, Any


async def delay(time: int) -> None:
    print('Start sleep for %s seconds' % time)
    await asyncio.sleep(time)
    print('Finished sleep for %s seconds' % time)


def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f'выполняется {func} с аргументами {args} {kwargs}')
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f'{func} завершилась за {total:.4f} с')
        return wrapped
    return wrapper
