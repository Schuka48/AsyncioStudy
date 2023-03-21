import asyncio
from asyncio import AbstractEventLoop

# from utilies import delay
import socket
import logging

tasks = []


async def echo(connection: socket, address: tuple[str, int], loop: AbstractEventLoop):
    try:
        while data := await loop.sock_recv(connection, 1024):
            print(f'receive: %s from address: %s' % (data, address))
            if data == b'boom\r\n':
                raise Exception('Неожиданная ошибка сети')
            await loop.sock_sendall(connection, data)
    except Exception as e:
        logging.exception(e)
    finally:
        connection.close()


async def listen_for_connections(server_socket: socket, loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Получен запрос на подключение от {address}")
        tasks.append(asyncio.create_task(echo(connection, address, loop)))


async def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setblocking(False)

    server_address = ('127.0.0.1', 8080)
    server.bind(server_address)
    server.listen()

    print(f'Start async server on {server_address}')
    try:
        await listen_for_connections(server, asyncio.get_running_loop())
    except KeyboardInterrupt:
        print('Exit')
        server.close()

if __name__ == '__main__':
    asyncio.run(main())
