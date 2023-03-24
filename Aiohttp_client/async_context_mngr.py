import asyncio
# import aiohttp
import socket
from asyncio import AbstractEventLoop


class ConnectionSocket:
    def __init__(self, server_socket: socket):
        self._connection: socket = None
        self.server_socket = server_socket

    async def __aenter__(self):
        print('Ожидание нового подключения')
        loop: AbstractEventLoop = asyncio.get_event_loop()
        connection, address = await loop.sock_accept(self.server_socket)
        connection.setblocking(False)
        self._connection = connection
        print(f'Подключение от {address} успешно')
        return self._connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()
        print('Подключение закрыто')


async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('127.0.0.1', 8000)
    server_socket.bind(server_address)
    server_socket.listen()

    loop: AbstractEventLoop = asyncio.get_event_loop()
    async with ConnectionSocket(server_socket) as client:
        data = await loop.sock_recv(client, 1024)
        print(data)


if __name__ == '__main__':
    asyncio.run(main())
