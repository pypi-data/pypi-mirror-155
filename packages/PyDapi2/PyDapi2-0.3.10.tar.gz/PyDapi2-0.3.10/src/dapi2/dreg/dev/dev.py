'''
Created on 6 mars 2021

@author: fv

'''
from enum import IntFlag

class DevError(IntFlag):
    NO =             0x0000
    OUTCRC =         0x0001
    INCRC =          0x0002
    OUTACK_CHAR =    0x0004
    INACK_CHAR =     0x0008
    OUTSOH_CHAR =    0x0010
    INACK_TIMEOUT =  0x0020
    OUTACK_TIMEOUT = 0x0040
    
    
    DISABLE =    0x0000
    ONCE =       0x1000
    EVERYTIME  = 0x2000
    CONTINUOUS = 0x3000
    
    
    

class DevBaseErrorGenerator(object):
    '''
    classdocs
    '''


    def __init__(self, mode=DevError.NO):
        '''
        Constructor
        '''
        self.mode = mode
        
    def crc(self, crc):
        return crc
        
class DevNoErrorGenerator(DevBaseErrorGenerator):
    pass

class DevErrorGenerator(DevBaseErrorGenerator):
    
    def crcOut(self, crc):
        pass
        #if self.mode & DevError.OUTCRC

        
#errorGenerator = DevNoErrorGenerator()

