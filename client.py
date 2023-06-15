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
parser.add_argument("--host",type=str,default=HOST,help="Host IP. Default=Localhost")
parser.add_argument("--port",type=int,default=PORT,help="port to use. Default=9999")

args = parser.parse_args()
NAME = args.name
logger = make_logger(NAME)
if len(NAME) > 10:
    logger.info("이름은 10자 이하로 설정해주세요.")
    sys.exit()

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((args.host, args.port))
socket_manager = utils.SocketManager(client_socket)

def recv_data() :
    '''
        Thread function for receiving data from server
    '''
    while True :
        try:
            name, message = socket_manager.recv()
            logger.info(f"{name} : {repr(message)}")
        except Exception:
            logger.debug("client 종료")
            break

start_new_thread(recv_data, ())
socket_manager.send(NAME,"")
logger.info(f'{NAME}님이 접속하였습니다.')

while True:
    try:
        message = input('')
        logger.debug(message)
        if socket_manager.send(NAME,message) == -1:
            logger.info("에러가 발생하여 전송이 완료되지 않았습니다.")
        if message == 'quit':
            break
        
    except ConnectionResetError as re:
        logger.info("Server shuts down.")
        logger.debug(f"ERROR : {re}")
        break
    except ConnectionAbortedError as ae:
        logger.info("경고 3회 누적으로 밴 당했습니다.")
        logger.debug(f"ERROR : {ae}")
        break
socket_manager.close()
