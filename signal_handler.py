import asyncio
import signal
from asyncio import Task, AbstractEventLoop
from typing import Set


def cancel_task():
    print('Получен сигнал SIGINT!')
    tasks: Set[Task] = asyncio.all_tasks()
    print(f'Снимается {len(tasks)} задач.')
    [task.cancel() for task in tasks]


async def main():
    loop: AbstractEventLoop = asyncio.get_running_loop()

    loop.add_signal_handler(signal.SIGINT, cancel_task)

    await asyncio.sleep(10)


if __name__ == '__main__':
    asyncio.run(main())
