"""
    Chat Server
"""

import socket
import utils
from _thread import start_new_thread
from config import HOST, PORT, IP_INDEX, PORT_INDEX
from logger import make_logger

client_socket_managers = []
logger = make_logger("server")

def threaded(socket_manager, client_addr):
    '''
        Thread function for handling client socket
    '''
    socket_controller = utils.SocketController()            # invoker
    socket_manager = utils.SocketManager(socket_manager)     # receiver
    recv_command = utils.RecvCommand(socket_manager)        # command
    socket_controller.setCommand(recv_command)
    client_name, _ = socket_controller.doCommand()
    entering_message = f"{client_name}:{client_addr}님이 접속하였습니다."
    logger.info(entering_message)

    while True:
        try:
            socket_controller.setCommand(recv_command)
            _, message = socket_controller.doCommand()
            if not message:
                logger.info(f"{client_name}님이 나갔습니다.")
                break
            logger.info(f'{client_name}({client_addr[IP_INDEX]}:{client_addr[PORT_INDEX]}) : {repr(message)}')
            socket_controller.setCommand(utils.SendCommand(socket_manager,client_name,message))
            for client in client_socket_managers :
                if client != socket_manager :
                    socket_controller.setCommand(utils.SendCommand(client, client_name, message))
                    socket_controller.doCommand()
        except Exception:
            logger.info(f"{client_name}님이 나갔습니다.")
            break

    if socket_manager in client_socket_managers :
        client_socket_managers.remove(socket_manager)
        logger.info(f'Rest Clients : {len(client_socket_managers)}')
    socket_manager.close()

logger.info('>> Server Start')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET: IP Version 4, SOCK_STREAM: TCP 패킷 허용. row/"stream"/데이터그램 socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #포트 여러번 바인드하면 발생하는 에러 방지
server_socket.bind((HOST, PORT))
server_socket.listen() # 클라이언트를 기다림. 인수로는 동시 접속할 최대한의 클라이언트 수. 실제 송수신은 accept을 통해서

try:
    while True:
        logger.info('>> Wait')
        client_socket, addr = server_socket.accept()
        client_socket_managers.append(client_socket)
        start_new_thread(threaded, (client_socket, addr))
        logger.info(f"참가자 수 : {len(client_socket_managers)}")
except Exception as e :
    logger.debug(f'Error : {e}')
finally:
    server_socket.close()
