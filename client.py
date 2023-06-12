"""
    Chat Client
"""

import socket
import argparse
import sys
from _thread import start_new_thread

import utils
from config import HOST, PORT
from logger import make_logger

parser = argparse.ArgumentParser()
parser.add_argument("--name",type=str,default="Unknown",help="User name. Default=Unknown")
args = parser.parse_args()
NAME = args.name
logger = make_logger(NAME)
if len(NAME) > 10:
    logger.info("이름은 10자 이하로 설정해주세요.")
    sys.exit()

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
socket_controller = utils.SocketController()
socket_manager = utils.SocketManager(client_socket)
recv_command = utils.RecvCommand(socket_manager)

def recv_data() :
    '''
        Thread function for receiving data from server
    '''
    while True :
        try:
            socket_controller.set_command(recv_command)
            name, message = socket_controller.do_command()
            logger.info(f"{name} : {repr(message)}")
        except Exception:
            logger.debug("client 종료")
            break

start_new_thread(recv_data, ())
socket_controller.set_command(utils.SendCommand(socket_manager,NAME,""))
socket_controller.do_command()
logger.info(f'{NAME}님이 접속하였습니다.')

while True:
    try:
        message = input('')
        logger.debug(message)
        if message == 'quit':
            break
        socket_controller.set_command(utils.SendCommand(socket_manager,NAME,message))
        socket_controller.do_command()
    except ConnectionResetError as re:
        logger.info("Server shuts down.")
        logger.debug(f"ERROR : {re}")
        break
    except ConnectionAbortedError as ae:
        logger.info("경고 3회 누적으로 밴 당했습니다.")
        logger.debug(f"ERROR : {ae}")
        break
socket_manager.close()
