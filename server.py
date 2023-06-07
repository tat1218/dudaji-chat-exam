import socket
from _thread import start_new_thread
from config import *

client_sockets = [] 

def threaded(client_socket, addr, NAME): 
    entering_message = f"{NAME}:{addr}님이 접속하였습니다."
    print(entering_message)

    while True:
        try:
            data = client_socket.recv(BUF_SIZE) #1024byte
            if not data:
                print(f"{NAME}님이 나갔습니다.")
                break
            print(f'{NAME} [{addr[IP_INDEX]}:{addr[PORT_INDEX]}] {repr(data.decode())}')
            for client in client_sockets :
                if client != client_socket :
                    message = f'{NAME}: {repr(data.decode())}'
                    client.send(message.encode())

        except Exception as e:
            print(f"{NAME}님이 나갔습니다.")
            break

    if client_socket in client_sockets :
        client_sockets.remove(client_socket)
        print('Rest Clients : ',len(client_sockets))
    client_socket.close()

print('>> Server Start')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET: IP Version 4, SOCK_STREAM: TCP 패킷 허용. row/"stream"/데이터그램 socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #포트 여러번 바인드하면 발생하는 에러 방지
server_socket.bind((HOST, PORT))
server_socket.listen() # 클라이언트를 기다림. 인수로는 동시 접속할 최대한의 클라이언트 수. 실제 송수신은 accept을 통해서

try:
    while True:
        print('>> Wait')
        client_socket, addr = server_socket.accept()
        NAME = client_socket.recv(BUF_SIZE)
        NAME = repr(NAME.decode())
        client_sockets.append(client_socket)
        start_new_thread(threaded, (client_socket, addr, NAME))
        print("참가자 수 : ", len(client_sockets))
except Exception as e :
    print ('에러는? : ',e)
finally:
    server_socket.close()

