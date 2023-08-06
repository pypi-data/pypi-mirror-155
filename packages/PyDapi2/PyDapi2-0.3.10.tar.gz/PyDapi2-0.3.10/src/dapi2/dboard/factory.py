'''
Created on 24 févr. 2021

@author: fv
'''


from .common import DBoardException 
from dapi2 import dcom  
from dapi2.dcom.dserial import DSerialAcknoledgeError, DSerial

from .mb30 import Board30 #@UnusedImport
from .mb60 import Board60 #@UnusedImport
from .mb92 import Board92 #@UnusedImport
from .base import DBoardPreferredDapiMode, DBoard
from .generic import GenericBoard

class DBoardTypeError(DBoardException):
    pass

class DBoardFactory(object):
    '''Class to make DBoard object according DAPI2 responses
    
    :param DApi2 dapi: Object DAPI2 to communicate with the electronic board
    :param DBoardPreferredDapiMode dmode: The DAPI2 preferred mode
    :param callback_msg: callback function to display messages when the object DBoard is instantiated. 
     
    :return: The new board object. The class depends on the values of the `btr` and `bnr` registers.
    :rtype: BaseDBoard
    '''

    def __new__(self, dapi, dmode=DBoardPreferredDapiMode.REGISTER, callback_msg=None):
        '''Constructor'''
        
        self.dapi = dapi
        self.dapi.regs.reset()
        
        def _firstCom():
            if isinstance(self.dapi.dcom, DSerial):
            #if hasattr(self.dapi.comm, 'serial'):
                for bdr in dcom.COM_SPEEDS:
                    self.dapi.dcom.serial.baudrate = bdr
                    try:
                        self.dapi.readRegs(self.dapi.regs.btr, self.dapi.regs.bnr)
                        return True;
                    except DSerialAcknoledgeError:
                        if callback_msg:
                            callback_msg('Connection attempt @ {0:d} baud failed!'.format(bdr))
                        self.dapi.log.error('Connection attempt @ {0:d} baud failed!'.format(bdr))
                        continue
                raise DSerialAcknoledgeError(self, 'Constructor', 'Unable to connect to the board!')
            else:
                try:
                    self.dapi.readRegs(self.dapi.regs.btr, self.dapi.regs.bnr)
                    return True;
                except DSerialAcknoledgeError:
                    if callback_msg:
                            callback_msg('The attempt to read is failed')
                    self.dapi.log.error('The attempt to read is failed')
            
        if self.dapi.dcom is None:
            return None
        
        _firstCom()
        
        
        try:             
            if self.dapi.regs.btr.asString() != 'MB':
                raise DBoardTypeError(self, 'Constructor', 'The device must be a main board ! ({})!'.format(self.dapi.regs.btr.asString()))
            try:
                nr = self.dapi.regs.bnr.asString()
                return DBoard.getBoardClasses()[nr](self.dapi, dmode)
            except KeyError:
                raise DBoardTypeError(self, 'Constructor', '{0!s} is not a valid board type!'.format(self.dapi.regs.bnr.value)) 
        except DBoardTypeError as e:
            if self.dapi.dev_mode:
                return GenericBoard(self.dapi, dmode)
            else:
                raise e
            
    
    