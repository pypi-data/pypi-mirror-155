'''Base class for DAPI2 communications 

:author: F. Voillat
:date: 2021-02-20 Creation
'''

import logging
import time
from enum import IntEnum


from ..common import DApi2Side, DApiException
from ..dmsg.reader import MsgReader
from ..dmsg.writer import MsgWriter



RESPONSE_TIMEOUT = 2.0 #s
'''Default reponse timeout'''

TRACE_INGOING_COLOR = '\033[33m'
TRACE_INERROR_COLOR = '\033[31m'
TRACE_OUTGOING_COLOR = '\033[36m'
TRACE_OUTERROR_COLOR = '\033[91m'
TRACE_RESET_COLOR = '\033[0m'

TRACE_INGOING_RAW_FMT     = '{time:9.3f} | <-- | {buf:30s}' + TRACE_RESET_COLOR
TRACE_OUTGOING_RAW_FMT    = '{time:9.3f} | --> | {buf:30s}' + TRACE_RESET_COLOR
TRACE_INGOING_NORMAL_FMT  = '{time:9.3f} | <-- | {buf:30s} | {msg!s}' + TRACE_RESET_COLOR 
TRACE_OUTGOING_NORMAL_FMT = '{time:9.3f} | --> | {buf:30s} | {msg!s}' + TRACE_RESET_COLOR
# TRACE_INGOING_DAPI_FMT    = TRACE_INGOING_COLOR  + '{time:9.3f} | <-- | {buf:30s} | {msg!s}' + TRACE_RESET_COLOR
# TRACE_OUTGOING_DAPI_FMT   = TRACE_OUTGOING_COLOR + '{time:9.3f} | --> | {buf:30s} | {msg!s}' + TRACE_RESET_COLOR


class DComException(DApiException):
    '''Base class for DCom module exceptions.'''
    pass

class DComError(DComException):
    '''Exception for communication error.'''
    pass

# class DComTracingMode(IntEnum):
    # '''Tracing mode of DAPI2 communication'''
    # NO = 0
    # '''No trace'''
    # RAW = 1
    # '''Raw trace : the transmitted characters'''
    # NORMAL = 2
    # '''Decoded message'''
    # DAPI = 3
    
class DComTracingDirection(IntEnum):
    '''Direction of tracing'''
    OUTGOING = 0
    '''Trace a sent message'''
    INGOING = 1
    '''Trace a received message'''

class BaseDCom(object):
    '''Base class for DAPI2 communications
    
    :param Dapi2Side side: Communication side (default: MASTER).
    :param function trace_callback: Callback function for tracing.
    :param int response_timeout: Response timeout (default = :data:`RESPONSE_TIMEOUT`).
    '''

    

    def __init__(self, side=DApi2Side.MASTER, trace_callback=None, response_timeout=RESPONSE_TIMEOUT):
        '''Constructor'''
        self.side = side
        self.log = logging.getLogger(self.__class__.__name__+":"+self.side.name)
        self.reader = MsgReader(self.side)
        self.writer = MsgWriter(self.side)
        self.trace_callback = trace_callback
        self.start_time = time.time()
        self.response_timeout = response_timeout
        
    def __str__(self):
        try:
            return self.__class__.__name__+":"+self.side.name
        except:
            return object.__str__(self)
        
    def __bool__(self):
        return self.isOpen()
        
    def open(self):
        '''Open communications'''
        pass
    
    def close(self):
        '''Close communications'''
        pass

    def isOpen(self):
        '''Check if serial port is open.
        
        :return: True, if serial port is open
        :rtype: bool
        ''' 
        return False
    
    def isOnError(self):
        '''Check if communications is on error state.
        
        :return: True, if communications is on error state.
        :rtype: bool
        ''' 
        return True
    
    def isOk(self):
        '''Check if communications is on `OK` state.
        
        :return: True, if communications is on `OK` state.
        :rtype: bool
        ''' 
        return False
        
    def reset(self):
        '''Resets DAPI2 communication'''
        self.reader.reset()
        self.start_time = time.time()
        
    def sendMessage(self, msg, attempts=5):
        '''Send a DAPI2 message.
        
        :param BaseMessage msg: message to send to the card
        
        :param int attempts: number of try to connect send the message
        '''
        assert False, 'Abstract method!'
        

    def receiveMessage(self, expected_type, attempts=5):
        '''Wait a DAPI2 response message.
        
        :param MsgType expected_type: Expected type
        
        :param int attempts: (default = 5).
        '''
        assert False, 'Abstract method!'
        
    def traceSent(self, msg):
        '''Traces the messages sent.
        
        :param BaseMessage msg: The message sent to trace.
        ''' 
        
        if self.trace_callback is None or msg is None:
            return
        if not isinstance(msg, (bytes, bytearray)):
            buf = msg.buffer
        else:
            buf = msg
            self.reader.reset(side=self.side)
            msg = self.reader.readBuffer(buf)
        self.trace_callback(time.time()-self.start_time, DComTracingDirection.OUTGOING, buf, msg)
        

    def traceReceived(self, msg):
        '''Traces received messages.
        
        :param BaseMessage msg: The received message to trace.
        '''
        if self.trace_callback is None:
            return
        if not isinstance(msg, (bytes, bytearray)):
            buf = msg.buffer
        else:
            buf = msg
            self.reader.reset(side=self.side.reverse())
            msg = self.reader.readBuffer(buf)
            
        self.trace_callback(time.time()-self.start_time, DComTracingDirection.INGOING, buf, msg)

            
            