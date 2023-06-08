"""
    Chat Client
"""

import socket
import sys
import json
from _thread import start_new_thread, allocate_lock
from config import HOST, PORT, BUF_SIZE
from logger import make_logger
import utils

if len(sys.argv) > 1:
    NAME = sys.argv[1]
else:
    NAME = 'Unknown'

logger = make_logger(NAME)
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
socket_controller = utils.SocketController()
socket_manager = utils.SocketManager(client_socket)
socket_control_lock = allocate_lock()

def recv_data(client_socket) :
    '''
        Thread function for receiving data from server
    '''
    recv_command = utils.RecvCommand(socket_manager)
    while True :
        try:
            socket_controller.setCommand(recv_command)
            name, message = socket_controller.doCommand()
            logger.info(f"{name} : {repr(message)}")
        except Exception:
            logger.debug("client 종료")
            break

start_new_thread(recv_data, (client_socket,))
socket_controller.setCommand(utils.SendCommand(socket_manager,NAME,""))
socket_controller.doCommand()
logger.info(f'{NAME}님이 접속하였습니다.')

while True:
    message = input('')
    logger.debug(message)
    if message == 'quit':
        break
    socket_controller.setCommand(utils.SendCommand(socket_manager,NAME,message))
    socket_controller.doCommand()
client_socket.close()
