'''Module for class DSerial. This module implements the serial communications between PC and Dassym's board. 

:author: F. Voillat
:date: 2021-02-19 Creation
'''

from enum import IntEnum
import time

from .base import BaseDCom, DApi2Side, DComException, DComError, RESPONSE_TIMEOUT
from ..dmsg import AckMsg, NakMsg
from ..dmsg import MsgReaderState



class DSerialException(DComException):
    '''Base class for DSerial module exceptions.'''
    pass

class DSerialAcknoledgeError(DSerialException):
    '''Exception for negative acknowledgment.'''
    pass

class DSerialResponseTimeoutError(DSerialException):
    '''Exception for a timeout expired before receiving the response message.'''
    pass

class DSerialRecieveTimeoutError(DSerialException):
    '''Exception for a timeout expired before receiving the next character of a message.''' 
    pass

class DSerialState(IntEnum):
    '''Sate of :class:`DSerial` '''
    SENDING     = -4
    RECEIVING   = -3
    WAIT        = -2
    ACK         = -1
    
    OK          =  0
    
    ERR_NO_ACK  = 10
    ERR_BAD_ACK = 11
    ERR_NAK     = 12
    ERR_CRC     = 20


    
ACKNOWLEDGE_TIMEPOUT = 0.2 #s
'''Default timeout for receiving an acknowledgment.''' 

RECEIVE_TIMEOUT = 0.05 #s
'''Default timeout for receiving the next char of message.'''

COM_SPEEDS = [115200, 57600, 38400, 19200, 9600]
'''Standard serial communication speeds'''


class DSerial(BaseDCom):
    '''Class for serial communications between PC and Dassym's board.

    :param Dapi2Side side: Communication side (default: MASTER).
    :param function trace_callback: Callback function for tracing.
    :param int response_timeout: Response timeout (default = :data:`RESPONSE_TIMEOUT`).
    :param int ack_timeout: Acknowledge timeout (default = :data:`ACKNOWLEDGE_TIMEPOUT`).
    :param int receive_tmeout: Next char receiving timeout (default = :data:`RECEIVE_TIMEOUT`).
    '''

    def __init__(self, serial, side=DApi2Side.MASTER, trace_callback=None, response_timeout=RESPONSE_TIMEOUT, ack_timeout=ACKNOWLEDGE_TIMEPOUT, receive_tmeout=RECEIVE_TIMEOUT):
        '''Constructor'''
        super().__init__(side, trace_callback, response_timeout)
        self.log.debug('Initialize on {0!s}'.format(serial))
        self.state = DSerialState.OK
        self.ack_timeout = ack_timeout
        self.receive_timeout = receive_tmeout
        self.serial = serial
        self.writer.stream = serial
        self.reset()
        self._ack_messages = {
            False: NakMsg(),
            True: AckMsg()
            }
        
    def __str__(self):
        try:
            return super().__str__() +":"+self.serial.port+":"+str(self.serial.baudrate)
        except:    
            return BaseDCom.__str__(self)
        
    def open(self):
        '''Open serial port'''
        self.log.info('Open serial to port {0!s}'.format(self.serial.port))
        self.serial.open()
        self.log.debug('... serial port open')
        self.reset()
        self.log.debug('... seriel port reseted')
        for i in range(10):
            if self.serial.isOpen():
                break
            time.sleep(1)
            self.log.warning('Attempting until the serial port is open ({0:d}/10) ...'.format(i))
        self.log.info( "Serial port is open on {0!s}@{1:d}bd".format(self.serial.port, self.serial.baudrate) )
            
        
    def close(self):
        '''Close serial port'''
        self.log.info('Close serial to port {0!s}'.format(self.serial.port))
        self.serial.close()

    def reset(self, state=DSerialState.OK):
        '''Resets the serial communications
        
        :param state: New state fixed after reset.
        :type state: DSerialState
        '''
        super().reset()
        self.state = state
        if self.isOpen():
            self.serial.reset_input_buffer()
            self.serial.reset_output_buffer()
        
    def waitAcknowledge(self,):
        '''Waits for an acknowledgment message to be received'''
        self.state = DSerialState.WAIT
        self.serial.timeout = self.ack_timeout
        self.reader.reset()
        readed = self.serial.read(1)
        self.reader.readBuffer(readed)
        if self.reader.state == MsgReaderState.ACKNOWLEDGEMENT:
            msg = self.reader.getMessage(True)
            self.traceReceived(msg)
            if isinstance(msg, AckMsg): 
                self.state = DSerialState.OK
                return True
            else:
                self.state = DSerialState.ERR_BAD_ACK
                return False
        self.state = DSerialState.ERR_NO_ACK
        return False
        
        
    
    def sendAcknowledge(self, ok=True):
        '''sending of a positive or negative acknowledgment message
        
        :param ok: If true, positive acknowledgment
        :type ok: bool
        '''
        self.serial.write(self._ack_messages[ok]._buffer)
        self.traceSent(self._ack_messages[ok])
        self.state = DSerialState.OK if ok else DSerialState.ERR_NAK
    
    def isOpen(self):
        '''Check if serial port is open.
        
        :return: True, if serial port is open
        :rtype: bool
        ''' 
        return self.serial.isOpen()
    
    def isOnError(self):
        '''Check if communications is on error state.
        
        :return: True, if communications is on error state.
        :rtype: bool
        ''' 

        return self.state > DSerialState.OK
    
    def isOk(self):
        '''Check if communications is on `OK` state.
        
        :return: True, if communications is on `OK` state.
        :rtype: bool
        ''' 
        return self.state == DSerialState.OK
    
    
    
    def sendMessage(self, msg, attempts=5):
        '''Send a message.
        
        :param msg: Message to send.
        :type msg:  BaseMessage
        
        :param attempts: Number of attempts before getting into error.
        :type attempts: int
        '''
        assert attempts > 0
        
        msg_buf = self.writer.encodeSerial(msg)
       
        for attempt in range(attempts):
            try:
                #self.reset()
                self.state = DSerialState.SENDING
                self.serial.write(msg_buf)
                self.traceSent(msg_buf)
                if self.waitAcknowledge():
                    return True
            except DSerialAcknoledgeError:
                self.log.error("Error transmitting! Try #{0:d}".format(attempt+1))
                continue
        raise DSerialAcknoledgeError(self, 'sendMessage', 'No positive acknowledgment received after {0:d} attempts'.format(attempts))
            
            
    def receiveMessage(self, expected_type, attempts=5):
        '''Receiving a message
        
        
        :param expected_type: expected type of message
        :type expected_type: MsgType
        :param attempts: Number of attempts before getting into error.
        :type attempts: int
        
        :return: The message received.
        :rtype: BaseMessage        
        '''
        
        assert attempts > 0
        for attempt in range(attempts):
            self.state = DSerialState.WAIT
            self.serial.timeout = self.response_timeout
            buf = self.serial.read(1)
            if len(buf)==0:
                raise DSerialResponseTimeoutError()
            self.reader.putChar(buf[0])
            self.serial.timeout = self.receive_timeout
            while(self.reader.state < MsgReaderState.COMPLETE):
                self.state = DSerialState.RECEIVING
                buf = self.serial.read(1)
                if len(buf)==0:
                    raise DSerialRecieveTimeoutError(self,'receiveMessage', 'The rest of the message no longer arrives' )
                self.reader.putChar(buf[0])
            
            if self.reader.state == MsgReaderState.ERROR: 
                self.log.error("Error transmitting! Try #{0:d}".format(attempt+1))
                self.sendAcknowledge(False)
                continue
            else:
                self.traceReceived(self.reader._buf)
                self.sendAcknowledge(True)
                if not self.reader.isType(expected_type):
                    raise DComError(self,'receiveMessage', 'The message ({0:s}) is not of the expected type ({1:s})!'.format(expected_type.name, self.reader.msg.type().name))
                return self.reader.getMessage()
            
        raise DSerialAcknoledgeError(self, 'receiveMessage', 'No properly formed responses were received after {0:d} attempts'.format(attempts))
    
