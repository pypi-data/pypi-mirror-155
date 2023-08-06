'''The module `dmsg` implements the DAPI2 message. 

:date: 2021-01-30 Creation
:author: F. Voillat
'''

from .common import CRC_INITIAL, HDR_CHAR, NAK_CHAR,\
    MsgReaderState, ACK_CHAR, crcByte
from .message import AckMsg, NakMsg, ExtendedMessage, BaseMessage
 
    
class MsgReader(object):
    '''Class to read DAPI2 messages
    
    :param side: The side of communication
    :type side: Dapi2Side

    :param state: Initial reader state
    :type state: MsgReaderState
    
    :param crc_initial: Initial CRC value.
    :type crc_initial: int
    '''
    
    @classmethod
    def isHexChar(cls, c):
        '''Check if char is allowed hexa char.
        
        :param c: The char ASCII code
        :type c: int
        
        :return: True if the char is a valid hexa char.
        :rtype: bool
        '''
        return (48 <= c <=  57) or (65 <= c <= 90)
    
    @classmethod
    def hexCharToInt(cls, c):
        '''Convert an hexa char to integer.
        
        :param c: The char ASCII code
        :type c: int
        
        :return: The decimal value of hexa char (0 to 15).
        :rtype: int
        '''
        if c >= 65:
            return c - 55
        else:
            return c - 48
    
    # @classmethod
    # def crcChar(self, c, crc):
        # '''Compute the CRC for the hexa char.
        #
        # :param c: The char ASCII code
        # :type c: int
        #
        # :param crc: The actual value of CRC.
        # :type crc: int
        #
        # :return: The new CRC.
        # :rtype: int
        # '''
        # return CRC_TAB[(crc >> 8) ^ c] ^ (crc << 8) & 0xffff
        #
    def __init__(self, side, state=MsgReaderState.IDLE, crc_initial=CRC_INITIAL):
        self.side = side
        self.pos = 0
        self._buf = bytearray()
        self._counter = 0
        self.state = state
        self.nibble = None
        self.crc = self.crc_initial = crc_initial
        self._msg = None
        
        
    def reset(self, state=MsgReaderState.IDLE, side=None):
        '''Reset the reader
        
        :param state: Initial reader state
        :type state: MsgReaderState
        '''
        if side is not None:
            self.side = side
        self.pos = 0
        self._counter = 0
        self._buf = bytearray()
        self.state = state
        self.nibble = None
        self.crc = self.crc_initial
        self._msg = None
        
    def start(self, c):
        '''Place the reader at the start of the reading process
        
        :param byte c: first character read
        '''
        self.pos = 0
        self._buf = bytearray([c])
        
        
    def getMessage(self, reset=False, state=MsgReaderState.IDLE):
        '''Returns the read message
        
        :param reset: If `True`, resets the reader before returning the read message.
        :type reset: bool
        
        :param state: Initial reader state, if reset is requested.
        :type state: MsgReaderState        
        
        :return: The read message.
        :rtype: BaseMessage
        '''
        ret = self._msg
        if reset:
            self.reset(state)
        return ret
        
    def readBuffer(self, buffer):
        '''Execute the reading process for all the characters in the buffer
        
        :param bytes buffer: The buffer whose characters must be read
        '''
        for c in buffer:
            self.putChar(c)
        if self.state == MsgReaderState.COMPLETE:
            return self._msg 
    
    def putChar(self, c):
        '''Put a character in the reader
        
        :param c: The char ASCII code
        :type c: int        
        '''
        
        if c == HDR_CHAR:
            self.reset(MsgReaderState.EMPTY)
            self.start(c)
        elif c == ACK_CHAR:
            self.reset(MsgReaderState.ACKNOWLEDGEMENT)
            self.start(c)
            self._msg = AckMsg()
            
        elif c == NAK_CHAR:
            self.reset(MsgReaderState.ACKNOWLEDGEMENT)
            self.start(c)
            self._msg = NakMsg()
        elif self.isHexChar(c) and MsgReaderState.IDLE < self.state < MsgReaderState.COMPLETE:
            self._buf.append(c)
            if self.state < MsgReaderState.CHECK:
                self.crc = crcByte(c, self.crc)
            if self.nibble is None:
                self.nibble = self.hexCharToInt(c) << 4
            else:
                b = self.nibble + self.hexCharToInt(c)
                self.nibble = None
                if self.state == MsgReaderState.EMPTY:
                    self._msg = BaseMessage.factory(b, self.side)
                    self.state = MsgReaderState.FUNC
                else:    
                    self._msg._setByte(self.pos, b)

                # print('P:{0:d} F:{1:02X} A:{2:02X} / L={3:d} / B={4:s} / b={5:s}'.format(
                    # self.pos, self._msg.func(), self._msg.getAddr(),
                    # len(self._msg._buffer), buffer2str(self._msg.buffer), buffer2str(self._buf) )) 
                
                self.pos += 1

                
                if self.state == MsgReaderState.FUNC:
                    if isinstance(self._msg, ExtendedMessage):
                        self.state = MsgReaderState.EXT
                    else: 
                        self.state = MsgReaderState.ADDR
                elif self.state == MsgReaderState.EXT:
                    self.state = MsgReaderState.DEV
                elif self.state == MsgReaderState.ADDR:
                    self._counter = 0
                    if self._msg.dataLen() > 0:
                        self.state = MsgReaderState.DATA
                    else:
                        self.state = MsgReaderState.CHECK
                elif self.state == MsgReaderState.DATA:
                    self._counter += 1
                    if self._counter >= self._msg.dataLen():
                        self.state = MsgReaderState.CHECK
                        self._counter = 0
                elif self.state == MsgReaderState.CHECK:
                    self._counter += 1
                    if self._counter == BaseMessage.CRC_SIZE:
                        if self.crc == self._msg.crc():
                            self.state = MsgReaderState.COMPLETE
                            
                        else:
                            self.state = MsgReaderState.ERROR
                else:
                    self.state = MsgReaderState.ERROR
                    
                #print( self.pos, self._counter,  self.state, hex(self.crc), list((hex(x) for x in self._buffer[:self.pos]) ) )
        else:
            pass    
    def isType(self, mtype):
        '''Check the message type.
        :param MsgType mtype: message type to compare
        :return: True, if the message is of the same type.
        '''
        return self._msg.type() == mtype    
        
    @property
    def msg(self):
        '''The message being processed'''
        return self._msg

