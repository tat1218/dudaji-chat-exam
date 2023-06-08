import abc
import socket
import json
from config import BUF_SIZE

class Command(abc.ABC):
    '''
        Command Interface
    '''
    @abc.abstractmethod
    def execute(self):
        pass

class SocketManager:
    '''
        Receiver : concrete logic for send and recv
    '''
    def __init__(self, socket:socket.socket):
        self.socket = socket
    
    def send(self, name, message) -> None:
        data = {'name':name,'message':message}
        self.socket.send(json.dumps(data).encode('UTF-8'))

    def recv(self):
        data = self.socket.recv(BUF_SIZE)
        data = json.loads(data)
        return data['name'], data['message']

class SendCommand(Command):
    '''
        Send Command : send data with socket
    '''
    def __init__(self, socket_manager:SocketManager, name:str, message:str):
        self.socket_manager = socket_manager
        self.name = name
        self.message = message

    def execute(self):
        self.socket_manager.send(self.name, self.message)

class RecvCommand(Command):
    '''
        Recv Command : receive data with socket
    '''
    def __init__(self, socket_manager:SocketManager):
        self.socket_manager = socket_manager

    def execute(self):
        return self.socket_manager.recv()
    
class SocketController:
    '''
        Invoker : request command
    '''
    def setCommand(self, command:Command):
        self.command = command 
    
    def doCommand(self):
        return self.command.execute()
