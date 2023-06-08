"""
    Chat Client
"""

import socket
import sys
import json
from _thread import start_new_thread
from config import HOST, PORT, BUF_SIZE
from logger import make_logger

if len(sys.argv) > 1:
    NAME = sys.argv[1]
else:
    NAME = 'Unknown'

logger = make_logger(NAME)
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def recv_data(client_socket) :
    '''
        Thread function for receiving data from server
    '''
    while True :
        try:
            data = client_socket.recv(BUF_SIZE)
            data = json.loads(data)
            logger.info(f"{data['name']} : {repr(data['msg'])}")
        except Exception:
            logger.debug("client 종료")
            break

start_new_thread(recv_data, (client_socket,))
client_socket.send(json.dumps({'name':NAME}).encode())
logger.info(f'{NAME}님이 접속하였습니다.')

while True:
    message = {'data':input('')}
    logger.debug(message['data'])
    if message['data'] == 'quit':
        break
    client_socket.send(json.dumps(message).encode())
client_socket.close()
