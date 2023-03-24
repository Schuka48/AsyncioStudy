import asyncio
import signal
from asyncio import AbstractEventLoop
from typing import Set

import socket
import logging


class GracefulExit(Exception):
    pass


async def echo(connection: socket, address: tuple[str, int], loop: AbstractEventLoop):
    try:
        while data := await loop.sock_recv(connection, 1024):
            print(f'receive: %s from address: %s' % (data, address))
            if data == b'boom':
                raise Exception('Неожиданная ошибка сети')
            await loop.sock_sendall(connection, data)
    except Exception as e:
        logging.exception(e)
    finally:
        connection.close()


async def close_echo_tasks(tasks: Set[asyncio.Task]):
    waiters = [asyncio.wait_for(task, 2) for task in tasks]
    for task in waiters:
        try:
            await task
        except asyncio.exceptions.TimeoutError:
            pass


async def listen_for_connections(server_socket: socket, loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Получен запрос на подключение от {address}")
        asyncio.create_task(echo(connection, address, loop))


def shutdown():
    raise GracefulExit()


async def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setblocking(False)

    server_address = ('127.0.0.1', 8000)
    server.bind(server_address)
    server.listen()

    print(f'Start async server on {server_address}')

    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(getattr(signal, signame), shutdown)

    await listen_for_connections(server, asyncio.get_running_loop())


if __name__ == '__main__':
    loop: AbstractEventLoop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    except GracefulExit:
        loop.run_until_complete(close_echo_tasks(asyncio.all_tasks()))
