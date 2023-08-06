'''Module for class DSocket. This module implements the network socket communications between PC and remote Dassym's board. 

:author: T. Marti

:date: 2021-??-?? Creation

'''


from .base import BaseDCom, DApi2Side, DComException, DComError
from dapi2.dmsg.message import BaseMessage

SEND_CONN_REQUEST = "sendconn"
SELECT_CONN_REQUEST = "selectconn:"

GET_CONN_NO_AVAILABLE_CONNECTION = "errornoavailableconnection"
TRANSFER_NO_CONNECTION_SET = "errornoconnectionset"
SELECT_CONN_OUT_OF_BOUND = "errornoconnectiononindex"
SELECT_CONN_UPDATED_STORAGE = "errorupdatedsocketstorage"


class DSocketException(DComException):
    '''Base class for DSocket module exceptions.'''
    pass

class DSocketExceptionNoAvailableConnection(DSocketException):
    '''Exception for no available external connection on proxy.'''
    pass

class DSocketExceptionNoConnectionSet(DSocketException):
    '''Exception for no connection selected on proxy.'''
    pass

class DSocketExceptionUpdatedStorage(DSocketException):
    '''Exception for storage update on proxy.'''
    pass

class DSocketExceptionSelectIndexOutOfBound(DSocketException):
    '''Exception for selected connection out of bound.'''
    pass




class DSocket(BaseDCom):
    '''Class for socket communications between PC and Dassym's proxy.

    :param socket socket: Socket used by DSocket for communicate to the proxy
    :param Dapi2Side side: Communication side (default: MASTER).
    :param function trace_callback: Callback function for tracing.
    :param int response_timeout: Response timeout (default = :data:`RESPONSE_TIMEOUT`).
    '''
    def __init__(self, socket, side=DApi2Side.MASTER, trace_callback=None, response_timeout=5):
        '''Constructor'''
        super().__init__(side, trace_callback, response_timeout)
        self.socket = socket
        self.patched = False
        self.msgType = None
        self.isConnected = True
                
    def _send(self, msg):
        """Send a message on the socket
        
        :param bytes msg: Encoded message to send on the socket
        """
        self.socket.sendall(msg)
        
    def _recv(self):
        """Receive message on the socket on the delay
        
        :return bytes: message receive on the socket
        """
        self.socket.settimeout(5)
        data = self.socket.recv(1024)
        self.socket.settimeout(None)
        return data
    
    def isOpen(self):
        '''Check if socket port is open.
        
        :return: True, if serial port is open
        :rtype: bool
        ''' 
        return self.isConnected
    
    def isOnError(self):
        '''Check if communications is on error state.
        
        :return: True, if communications is on error state.
        :rtype: bool
        ''' 

        return False
    
    def isOk(self):
        '''Check if communications is on `OK` state.
        
        :return: True, if communications is on `OK` state.
        :rtype: bool
        ''' 
        return True
    
    def get_ext_conn(self):
        """Get the external connexion of the proxy
        
        :return list: contain tuple (index, name)
        """
        self._send(SEND_CONN_REQUEST.encode())
        data = self._recv().decode()
        
        if data == GET_CONN_NO_AVAILABLE_CONNECTION:
            self.close()
            raise DSocketExceptionNoAvailableConnection(self, "No external connection available", "The proxy don't have any connexion from the external connected")
        
        listElements = []
        for elem in data.split(':'):
            if elem != '':
                splittedElem = elem.split('/')
                listElements.append((splittedElem[0], splittedElem[1]))
        return listElements
        
    def select_ext_conn(self, index):
        """Select the desired connection on the proxy
        """
        self._send((SELECT_CONN_REQUEST + str(index)).encode())
        data = self._recv().decode()
        
        if data == SELECT_CONN_UPDATED_STORAGE:
            raise DSocketExceptionUpdatedStorage(self, "Updated storage", "The storage have been update or the external connections have not been recovered")
        if data == SELECT_CONN_OUT_OF_BOUND:
            raise DSocketExceptionSelectIndexOutOfBound(self, "Select index out of bound", "The index send for the selecting the external socket is out of bound")
        if data == 'ACK':
            self.patched = True
    
    def sendMessage(self, msg, attempts=5):
        """BaseDCom overwrite function
        """
        if self.patched:
            assert attempts > 0
            
            self.msgType = msg.type()
            
            msg_buf = self.writer.encodeSocket(msg)
            
            self._send(msg_buf)
        else:
            raise DSocketExceptionNoConnectionSet(self, "The patche aren't connected", "The external connexion aren't set on the proxy")
            
    
    def receiveMessage(self, expected_type=1, attempts=5):
        """BaseDCom overwrite function
        """
        if self.patched:
            msg = self._recv()
            constructedMessage = BaseMessage.factoryRaw(bytearray.fromhex(msg.decode('ascii')), DApi2Side.SLAVE)
            
            if constructedMessage.type() != self.msgType:
                raise DComError(self,'receiveMessage', 'The message ({0:s}) is not of the expected type ({1:s})!'.format(self.msgType, constructedMessage.type()))
            else:
                return constructedMessage
        else:
            raise DSocketExceptionNoConnectionSet(self, "The patche aren't connected", "The external connexion aren't set on the proxy")
             
             
        
    def close(self):
        """close the socket
        """
        if self.socket != None:
            self.isConnected = False
            self.socket.close()
            self.socket = None
    
