"""
    Chat Server
"""

import socket
from _thread import start_new_thread

import utils
from config import HOST, PORT, IP_INDEX, PORT_INDEX
from logger import make_logger

client_socket_managers = []
logger = make_logger("server")

def threaded(socket_manager:utils.SocketManager, client_addr):
    '''
        Thread function for handling client socket
    '''
    client_name, _ = socket_manager.recv()
    entering_message = f"{client_name}:{client_addr}님이 접속하였습니다."
    logger.info(entering_message)

    warning_count = 0

    while True:
        try:
            name, message = socket_manager.recv()
            if name is None:
                warning_count += 1
                logger.info(f"{client_name}님이 너무 긴 메시지를 보내려 했습니다. 경고 {warning_count}회")
                socket_manager.send("server", f"메시지가 너무 깁니다. 경고 {warning_count}회. 3회 경고시 접속이 종료됩니다.")

                if warning_count >= 3:
                    logger.info(f"{client_name}님이 강퇴당했습니다.")
                    break
                continue

            logger.info(f'{client_name}({client_addr[IP_INDEX]}:{client_addr[PORT_INDEX]}) : {repr(message)}')
            
            if message == "quit":
                logger.info(f"{client_name}님이 접속을 종료했습니다.")
                break

            for client_socket_manager in client_socket_managers :
                if client_socket_manager != socket_manager :
                    client_socket_manager.send(client_name,message)

        except Exception as e_thread:
            logger.debug(e_thread)
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
        socket_manager = utils.SocketManager(client_socket)     # receiver
        client_socket_managers.append(socket_manager)
        start_new_thread(threaded, (socket_manager, addr))
        logger.info(f"참가자 수 : {len(client_socket_managers)}")
except Exception as e :
    logger.debug(f'Error : {e}')
finally:
    server_socket.close()
