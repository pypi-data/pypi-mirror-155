'''Module for class DEmu. This module implements the connection to an emulate board. 

:author: T. Marti
:date: 2021-??-?? Creation
'''


from .base import BaseDCom, DApi2Side

class DEmu(BaseDCom):
    '''Class for socket communications between PC and Dassym's proxy.

    :param DEmuBase bemu: Card
    :param Dapi2Side side: Communication side (default: MASTER).
    :param function trace_callback: Callback function for tracing.
    :param int response_timeout: Response timeout (default = :data:`RESPONSE_TIMEOUT`).
    '''
    def __init__(self, bemu, side=DApi2Side.MASTER, trace_callback=None, response_timeout=5):
        '''Constructor'''
        super().__init__(side, trace_callback, response_timeout)
        self.msgType = None
        self.board = bemu
    
    def sendMessage(self, msg, attempts=5):
        """BaseDCom overwrite function
        """
        self.traceSent(self.writer.encodeSerial(msg))
        self.board.receiveMessage(msg)
        
            
    
    def receiveMessage(self, expected_type=1, attempts=5):
        """BaseDCom overwrite function
        """
        msg = self.board.sendMessage()
        self.traceReceived(self.writer.encodeSerial(msg))
        return msg
        
    
