import socket
from _thread import start_new_thread
import sys
from config import *

if len(sys.argv) > 1:
    NAME = sys.argv[1]
else:
    NAME = 'Unknown'

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def recv_data(client_socket) :
    while True :
        data = client_socket.recv(BUF_SIZE)
        print(repr(data.decode()).replace('"',''))

start_new_thread(recv_data, (client_socket,))
client_socket.send(NAME.encode())
print (f'{NAME}님이 접속하였습니다.')

while True:
    message = input('')
    if message == 'quit':
        break

    client_socket.send(message.encode())
client_socket.close()
