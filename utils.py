"""
    Command Pattern Modules for send and recv
"""

import socket
import json
from config import BUF_SIZE, HEADER_LENGTH, MAX_LENGTH

class SocketManager:
    '''
        Receiver : concrete logic for send and recv
    '''
    def __init__(self, socket:socket.socket):
        self.socket = socket

    def send(self, name, message):
        '''
            send logic. input {name,message} pair
        '''

        data = {'name':name,'message':message}
        byte_data = json.dumps(data).encode()
        data_length = len(byte_data)
        send_length = self.socket.send(f"{data_length:<{HEADER_LENGTH}}".encode())
        if MAX_LENGTH < data_length:
            return -1
        start_idx = 0
        end_idx = BUF_SIZE
        while start_idx < data_length:
            send_length += self.socket.send(byte_data[start_idx:end_idx])
            start_idx = end_idx
            end_idx = min(end_idx+BUF_SIZE,data_length)
        return send_length

    def recv(self):
        '''
            recv logic. return {name,message} pair
        '''
        data_length = self.socket.recv(HEADER_LENGTH).decode()
        data_length = int(data_length)
        if MAX_LENGTH < data_length:
            return None, None
        byte_data = b''
        recv_length = 0
        while recv_length < data_length:
            recv_data = self.socket.recv(BUF_SIZE)
            byte_data += recv_data
            recv_length += len(recv_data)

        data = json.loads(byte_data)
        return data['name'], data['message']

    def close(self):
        '''
            close connection
        '''
        self.socket.close()