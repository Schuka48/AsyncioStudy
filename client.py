import socket


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('127.0.0.1', 8080))
    except Exception as e:
        print(e)

    try:
        while True:
            command = input('$ ')
            client.sendall(command.encode())
            print(client.recv(1024).decode())
    except KeyboardInterrupt:
        print('Exit')
        client.close()


if __name__ == '__main__':
    main()
