'''
Created on 28 févr. 2021

@author: fv
'''
from .common import CRC_INITIAL, HDR_CHAR
from dapi2.dmsg.common import crcStr



class MsgWriter(object):
    '''Class to write DAPI2 messages
    
    :param side: The side of communication
    :type side: Dapi2Side

    :param crc_initial: Initial CRC value.
    :type crc_initial: int
    '''
    
    def __init__(self, side, crc_initial=CRC_INITIAL):
        self.side = side
        self.crc_initial = crc_initial
        
        
    # def computreCrc(self, msg):
        # crc = self.crc_initial 
        # for i in range(msg.DATA0_IDX+msg.dataLen()):
            # crc = CRC_TAB[(crc >> 8) ^ msg.buffer[i] ] ^ (crc << 8) & 0xffff
        # return crc    
       
    def encodeSerial(self, msg, crc_initial=CRC_INITIAL):    
        if crc_initial is not None:
            self.crc_initial = crc_initial
        out = ''.join('{:02X}'.format(x) for x in msg.buffer)
        crc = crcStr(out, self.crc_initial)
        #crc = dev.errorGenerator.crc(crc)
        crc = format(crc,'04X')
        return (chr(HDR_CHAR) + out + crc).encode('ascii')
        
        
    def encodeSocket(self, msg):
        out = ''.join('{:02X}'.format(x) for x in msg.buffer)
        return out.encode('ascii')
        
