import struct

from enum import Enum
from abc import ABC, abstractmethod

# Definições do protocolo
PROTOCOL_VERSION = 1
PROTOCOL_HEADER_FORMAT = '!BHB'
PROTOCOL_HEADER_LENGTH = struct.calcsize(PROTOCOL_HEADER_FORMAT)

# Tipos de Mensagem
NICKNAME_MESSAGE_TYPE = 1
CHAT_MESSAGE_TYPE = 2
CLIENT_CONNECTION_TYPE = 3
CLIENT_CLOSE_CONN_TYPE = 4

def getMessageClass(msg):
    if "\\nickname " in msg:
        print("nick")
        return NicknameMessage(msg.lstrip("\\nickname "))
    elif "\close" in msg:
        return CloseMessage(msg.lstrip("\close "))
    else:
        print("mesg")
        return ChatMessage(msg)

# Classe base do protocolo
class BaseProtocol(ABC):

    def __init__(self):
        self.version = 0
        self.length = 0
        self.type = 0

    @abstractmethod
    def get_bytes(self):
        pass

    @staticmethod
    @abstractmethod
    def from_buffer(msg):
        pass

# Classe que representa a mensagem de atribuição do nickname
class NicknameMessage(BaseProtocol):

    def __init__(self, nickname):
        super().__init__()
        self.version = PROTOCOL_VERSION
        self.type = NICKNAME_MESSAGE_TYPE
        self.length = PROTOCOL_HEADER_LENGTH + len(nickname.encode('utf8'))
        self.nickname = nickname

    def get_bytes(self):
        return struct.pack(f'{PROTOCOL_HEADER_FORMAT}{self.length - PROTOCOL_HEADER_LENGTH}s', self.version, self.length, self.type, self.nickname.encode('utf8'))

    @staticmethod
    def from_buffer(msg):
        data = struct.unpack(f'{PROTOCOL_HEADER_FORMAT}{len(msg) - PROTOCOL_HEADER_LENGTH}s', msg)
        return NicknameMessage(str(data[3],'utf8'))

# Classe que representa uma mensagem do chat
class ChatMessage(BaseProtocol):

    def __init__(self, msg):
        super().__init__()
        self.version = PROTOCOL_VERSION
        self.type = CHAT_MESSAGE_TYPE
        self.length = PROTOCOL_HEADER_LENGTH + len(msg.encode('utf8'))
        self.msg = msg
    
    def get_bytes(self):
        return struct.pack(f'{PROTOCOL_HEADER_FORMAT}{self.length - PROTOCOL_HEADER_LENGTH}s', self.version, self.length, self.type, self.msg.encode('utf8'))

    @staticmethod
    def from_buffer(msg):
        data = struct.unpack(f'{PROTOCOL_HEADER_FORMAT}{len(msg) - PROTOCOL_HEADER_LENGTH}s', msg)
        return ChatMessage(str(data[3],'utf8'))


class CloseMessage(BaseProtocol):

    def __init__(self, nick):
        super().__init__()
        self.version = PROTOCOL_VERSION
        self.type = CLIENT_CLOSE_CONN_TYPE
        self.length = PROTOCOL_HEADER_LENGTH
        self.nick = nick
    
    def get_bytes(self):
        return struct.pack(f'{PROTOCOL_HEADER_FORMAT}{self.length - PROTOCOL_HEADER_LENGTH}s', self.version, self.length, self.type, f"\close {self.nick}".encode('utf8'))

    @staticmethod
    def from_buffer(nick):
        data = struct.unpack(f'{PROTOCOL_HEADER_FORMAT}{len(nick) - PROTOCOL_HEADER_LENGTH}s', nick)
        return CloseMessage(nick)


