'''Module for implementation of message classes.

:author: F. Voilat

'''
from ..common import DApi2Side, REG_SIZE
from .common import MsgType, ACK_CHAR, NAK_CHAR


class BaseMessage(object):
    '''Base class for DAPI2 message.'''
    
    #FUNC_EXT_MASK =  0x10
    FUNC_TYPE_MASK = 0xB0
    '''Bit mask to extract message type'''
    
    FUNC_ERR_MASK = 0x40
    
    FUNC_LEN_MASK =  0x0F
    '''Bit mask to extract message length'''
    
    HEADER_SIZE = 3
    '''Size of header part of message'''
    
    FUNC_IDX = 0 
    '''Func byte index (position in message)'''
    
    ADDR_IDX = 1
    '''Address byte index (position in message)'''
    
    DATA0_IDX = 2
    '''First data index (position in message)'''
    
    MAX_DATA_SIZE = 8
    '''Maximum size of data (bytes)'''
    
    CRC_SIZE = 2
    '''CRC part size'''
    
    MAX_MSG_SIZE = HEADER_SIZE + MAX_DATA_SIZE + CRC_SIZE 
    '''Maximum message size'''
     
    code = '~' 
     
    @classmethod
    def factory(cls, func, side):
        '''Construct a `message` object according to the `func` value.
        
        :param func: Func value of message.
        :type func: int
        
        :param side: Specify the side of communication (MSATER ; SLAVE)
        :type side: Dapi2Side
        
        :return: A new instance of message. Tthe class is determined by the dictionary :py:data:`MSG_CLASSES_MAP`.
        '''
        if func & BaseMessage.FUNC_ERR_MASK != 0:
            msg = ErrorMessage()
            msg.setFunc(func)
        else:
            msg = MSG_CLASSES_MAP[side][MsgType(func & BaseMessage.FUNC_TYPE_MASK)]()
            msg.setFunc(func)
        return msg
    
    @classmethod
    def factoryRaw(cls, buffer, side):
        # buffer = bytearray(buffer)
        msg = cls.factory(buffer[cls.FUNC_IDX], side)
        msg._buffer[:] = buffer
        return msg
    
            
    def __init__(self):
        '''COnstrucor'''
        self._buffer = bytearray(self.HEADER_SIZE)

        
    def _setByte(self, index, value, mask=0xFF):    
        '''Set the value of a byte of the buffer
        
        :param index: byte index to modify
        :type index: int

        :param value: value to set in the byte `index` of the buffer
        :type value: int
        
        :param mask: Bit mask to apply before setting value (default: 0xFF)
        :type mask: int
        '''
        # if index >= len(self._buffer):
            # self.setDataLen(index-self.DATA0_IDX+1 )
        self._buffer[index] = (self._buffer[index] & ~mask) | (value & mask)

    def _setType(self, mtype):
        '''Set the message type.
        
        :param mtype: The message type.
        :type mtype: MsgType
        '''
        self._setByte(self.FUNC_IDX, mtype.value, self.FUNC_TYPE_MASK)
        

    
    def func(self, mask=0xFF):
        '''Returns the `func` value.
        
        :param mask: Bit mask to apply before returning the value `func` (default: 0xFF)
        :type mask: int
        '''
        return self._buffer[self.FUNC_IDX] & mask
    
    def isError(self):
        '''Check if message is an error response
        
        :return: True, if the message is an error response ; False, otherwise.
        :rtype: bool
        '''
        return self._buffer[self.FUNC_IDX] & self.FUNC_ERR_MASK != 0
    
    def setFunc(self, value, mask=0xFF):
        self._setByte(self.FUNC_IDX, value, mask)
        
        if len(self._buffer) <= self.HEADER_SIZE+self.CRC_SIZE+self.dataLen():
            self._buffer.extend(bytearray( self.HEADER_SIZE+self.CRC_SIZE+self.dataLen()-len(self._buffer)))        
        
    
    def type(self):
        '''Returns the message type.
        
        :return: The message type according `func` value.
        :rtype: MsgType
        '''
        return MsgType(self.func(self.FUNC_TYPE_MASK))
    
    def getAddr(self):
        '''Returns the address of reading or writing message.
        
        :return: The address.
        :rtype: int
        '''
        return self._buffer[self.ADDR_IDX]
    
    def setAddr(self, value):
        '''Sets the message address.
        
        :param int addr: The new message address.
        ''' 
        self._setByte(self.ADDR_IDX, value)
    
    def dataLen(self):
        '''Returns the data length.
        
        :return: The data length (0 to 8).
        :rtype: int
        '''
        return self.func(self.FUNC_LEN_MASK)

    def setDataLen(self, value):
        '''Sets the message data length. If necessary, extend the buffer 
        
        :param int value: The new data length.
        '''
        self.setFunc(value, self.FUNC_LEN_MASK)
        # if len(self._buffer) <= self.DATA0_IDX+value:
            # self._buffer.extend(bytearray(self.DATA0_IDX+value-len(self._buffer)))
    
    def getBytes(self, index, length=1):
        '''Returns a bytes array from internal buffer.
        
        :param int index: Index (position) of the first requested byte.
        
        :param int length: the length of the requested array
        
        :return: The requested bytes array.
        :rtype: bytearray
        '''
        return bytes(self._buffer[index:index+length])
    
    
    def getDataBytes(self):
        '''Returns all data bytes.
        
        :return: The portion of the buffer that contains the data.
        :rtype: bytes
        '''
        
        return bytes(self._buffer[self.DATA0_IDX:-self.CRC_SIZE-1])
    
    def getDataWords(self):
        '''Returns all data as words array.
        
        :return: The portion of the buffer that contains the data.
        :rtype: list of int (word)
        '''
        data = self.getDataBytes()
        return list( [int.from_bytes(w,'big') for w in zip(data[0::2],data[1::2])]  )
    
    
    def getData(self, index, size=1):
        '''Returns a data value.
        
        :param index: Index (position) of first byte of data.
        :type index: int
        
        :param size: Size of data (1:byte, 2:word)
        :type sit: int
        
        :return: The data value.
        :rtype: int
        ''' 
        return int.from_bytes(self.getBytes(self.DATA0_IDX+index, size),'big') 
    
    def getDataByte(self, index):
        return self.getData(index, 1)
    
    def getDataWord(self, index):
        return self.getData(index, 2)
    
    def getDataDWord(self, index):
        return self.getData(index, 4)
    
    def setData(self, value, index, size=1):
        assert value is not None
        if self.dataLen() < index+size:
            self.setDataLen(index+size)
        
        if isinstance(value, bytes):
            for i, b in enumerate(value):
                self._setByte(self.DATA0_IDX+index+i, b)
            return
        
        for i, b in enumerate(value.to_bytes(size, byteorder='big')):
            self._setByte(self.DATA0_IDX+index+i, b)
            
    def setByte(self, value, index=None):
        if index is None:
            index = self.dataLen()
        self.setData(value, index)

    def setWord(self, value, index=None):
        if index is None:
            index = self.dataLen()
        self.setData(value, index, 2)

    def setDWord(self, value, index=None):
        if index is None:
            index = self.dataLen()
        self.setData(value, index, 4)
    
    def crc(self):
        '''Returns th CRC value sent.
        
        :return: The CRC value sent.
        :rtype: int
        ''' 
        return int.from_bytes(self.getBytes(self.DATA0_IDX+self.dataLen(), 2),'big')
    
    # def setCrc(self, crc):
        # self._setByte(self.DATA0_IDX+self.dataLen(), crc >> 8)
        # self._setByte(self.DATA0_IDX+self.dataLen()+1, crc & 0xFF)
        #

    def getLength(self):
        '''Returns length''' 
        return self.dataLen()
    
    
    @property
    def buffer(self):
        '''Returns the relevant part of internal buffer.'''
        return self._buffer[:self.DATA0_IDX+self.dataLen()]

class AcknowledgmentMsg(BaseMessage):
    '''Base class to store an acknowledgment message'''
    
    HEADER_SIZE = 0
    MAX_DATA_SIZE = 0
    
    def type(self):
        '''Returns the message type.
        
        :return: Allways MsgType.ACKNOWLEDGEMENT
        :rtype: MsgType
        '''
        return MsgType.ACKNOWLEDGEMENT    
    
    @property
    def buffer(self):
        return self._buffer
            
class AckMsg(AcknowledgmentMsg):
    '''Class for positive acknowledgment'''
    def __init__(self):
        self._buffer = bytes((ACK_CHAR,))

    def __str__(self):
        return 'ACK'                     
            
class NakMsg(AcknowledgmentMsg):
    '''Class for negative acknowledgment'''
    def __init__(self):
        self._buffer = bytes((NAK_CHAR,))
        
    def __str__(self):
        return 'NAK'                     
                    


class BaseMasterMessage(BaseMessage):   
    '''Class for message sent by the `master`'''
    
    code = 'M'
    
    def __init__(self):
        super().__init__()


class BaseSlaveMessage(BaseMessage):   
    '''Class for message sent by the `slave`'''
    
    code = 'S'
    
    def __init__(self):
        super().__init__()

class ReadRegMessage(BaseMasterMessage):
    '''Class for read request message from `master`'''
    
    code = 'MR'
    
    def __init__(self, addr=None, length=1):
        super().__init__()
        self.setFunc(MsgType.READ+1)
        if addr is not None:
            self.setAddr(addr)
        assert length <= self.MAX_DATA_SIZE
        self.setData(length, 0)
    
    def __str__(self):
        return 'Read {1:d} bytes @0x{0:02X}'.format(self.getAddr(), self.getData(0)) 
    
    def getLength(self):
        return self.getData(0)
    
class ValueRegMessage(BaseSlaveMessage):
    '''Class for read reply message from `slave`'''
    
    code = 'SR'
    
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        d = ';'.join( '0x{0:04X}'.format(int.from_bytes(self.getBytes(self.DATA0_IDX+i*2,2),'big')) for i in range(self.dataLen()//2)  )
        return 'Values @0x{0:02X} = [{1:s}]'.format(self.getAddr(), d) 
    
    def getRegValue(self, index):
        return self.getData(index*REG_SIZE, REG_SIZE) 
    
    
class WriteRegMessage(BaseMasterMessage):
    '''Class for write message from `master`'''
    
    code = 'MW'
    
    def __init__(self, addr=None, values=[]):
        super().__init__()
        self.setFunc(MsgType.WRITE)
        if addr is not None:
            self.setAddr(addr)
        assert len(values)*REG_SIZE <= self.MAX_DATA_SIZE    
        self.setDataLen(len(values)*REG_SIZE)
        for i, v in enumerate(values):
            self.setRegValue(i, v)
            
    
    def __str__(self):
        d = ';'.join( '0x{0:04X}'.format(int.from_bytes(self.getBytes(self.DATA0_IDX+i*2,2),'big')) for i in range(self.dataLen()//2)  )
        return 'Write [{1:s}] @0x{0:02X}'.format(self.getAddr(), d) 
    
    def getRegValue(self, index):
        return self.getData(index*REG_SIZE, REG_SIZE) 
    
    def setRegValue(self, index, value):
        self.setData(value, index*REG_SIZE, REG_SIZE)


class WrittenRegMessage(BaseSlaveMessage):
    '''Class for write replay message from `slave`'''
    
    code = 'SW'
    
    def __init__(self):
        super().__init__()
    def __str__(self):
        d = ';'.join( '0x{0:04X}'.format(int.from_bytes(self.getBytes(self.DATA0_IDX+i*2,2),'big')) for i in range(self.dataLen()//2)  )
        return 'Written [{1:s}] @0x{0:02X}'.format(self.getAddr(), d) 
    

    def getRegValue(self, index):
        return self.getData(index*REG_SIZE, REG_SIZE) 


class CommandMessage(BaseMasterMessage):
    '''Class for command message from `master`'''
    
    code = 'MC'
    
    def __init__(self, cmd=None, values=[], vsize=1):
        super().__init__()
        self.setFunc(MsgType.COMMAND)
        if cmd is not None:
            self.setAddr(cmd)
        
        assert len(values)*vsize <= self.MAX_DATA_SIZE    
        self.setDataLen(len(values)*vsize)
        for i, v in enumerate(values):
            self.setData(v, i, vsize)
        
        
    def __str__(self):
        d = ';'.join( '0x{0:04X}'.format(int.from_bytes(self.getBytes(self.DATA0_IDX+i*2,2),'big')) for i in range(self.dataLen()//2)  )
        return 'Command 0x{0:02X} ({1:s})'.format(self.getAddr(), d) 

    
    def cmd(self):
        '''Returns the command number (=`addr`)
        
        :return: The command number
        :rtype: int
        '''
        return self.getAddr()

class ResponseMessage(BaseSlaveMessage):
    '''class for `slave`'s response to a command message'''
    
    code = 'SC'
    
    def __init__(self):
        super().__init__()
    def __str__(self):
        if self.dataLen() > 0:
            d = ';'.join(['0x{0:02X}'.format(b) for b in self.getDataBytes()] )
            return 'Response for 0x{0:02X} : {1:s} '.format(self.getAddr(), d) 
        else:
            return 'Response for 0x{0:02X}'.format(self.getAddr())
    
    def cmd(self):
        return self.getAddr()
    
    def getByte(self, index):
        '''Returns one byte (8 bits) from received data.
        
        :param int index: Index of byte in data.
        
        :return: The byte requested.
        :rtype: int
        '''
        return self._buffer[index]
    
    def getWord(self, index):
        '''Returns one word (16 bits) from received data.
        
        :param int index: Index (expressed in bytes) of word in data.
        
        :return: The word requested.
        :rtype: int
        '''
        return self.getData(index, 2) 
    

class ErrorMessage(BaseSlaveMessage):
    '''class for `slave`'s error response'''
    
    code = 'SE'
    
    def __init__(self):
        super().__init__()
        
    def __str__(self):
        return 'Error n° {0:02x} on {1:s} @ 0x{2:02x} !'.format(self.getError(), self.type().name.lower(), self.getAddr()) 
    
    def getError(self):
        return self.getData(0, 1)


class ExtendedMessage(BaseMessage):
    '''Base class for extended message'''
    HEADER_SIZE = 4
    FUNC_IDX = 0 
    EXT_IDX = 1
    DEV_IDX = 2
    ADDR_IDX = 3
    DATA0_IDX = 4

    MAX_MSG_SIZE = HEADER_SIZE + BaseMessage.MAX_DATA_SIZE + BaseMessage.CRC_SIZE 

    code = 'X'

    def __init__(self):
        super().__init__()
    
    def ext(self):
        return self._buffer[self.EXT_IDX]

    def dev(self):
        return self._buffer[self.DEV_IDX]
    


MASTER_MSG_CLASSES_MAP = {
    MsgType.READ     : ReadRegMessage,
    MsgType.WRITE    : WriteRegMessage,
    MsgType.COMMAND  : CommandMessage,
    }
'''Classes map for `master` message'''

SLAVE_MSG_CLASSES_MAP = {
    MsgType.READ     : ValueRegMessage,
    MsgType.WRITE    : WrittenRegMessage,
    MsgType.COMMAND  : ResponseMessage,
    }
'''Classes map for `slave` message'''

MSG_CLASSES_MAP = {
    DApi2Side.MASTER : MASTER_MSG_CLASSES_MAP,
    DApi2Side.SLAVE  : SLAVE_MSG_CLASSES_MAP,
    }
'''Message classes map'''
