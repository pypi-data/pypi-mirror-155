'''Module for making an emulated Dassym's Board

@author: tm
'''
import os

from dapi2.dreg import RegContainer, RegContainerReader
from dapi2.dmsg.common import MsgType
from dapi2.dmsg.message import BaseMessage
from dapi2.common import DApi2Side
from demu.DEmuPPA import DEmuPPA
from enum import IntEnum

class E_MESSAGE_ERROR(IntEnum):
    DAPI_ERR_OK = 0x00,
    DAPI_ERR_WRONG_ADDR = 0x01,
    DAPI_ERR_READ_ONLY = 0x02,
    DAPI_ERR_WRONG_VALUE = 0x03,
    DAPI_ERR_WRONG_CONTEXT = 0x04,
    DAPI_ERR_MALFORMED_MSG = 0x05,
    DAPI_ERR_ACCESS_DENIED = 0x06,
    DAPI_ERR_EEPROM_FAILURE = 0x07,
    
    DAPI_ERR_ABORTED = 0xfd,
    DAPI_ERR_COM_BROKEN = 0xfe,
    DAPI_ERR_UNDIFINED = 0xff

class DEmuBaseBoard(object):
    """Class for making an emulate Dassym's board
    """
    def __init__(self, motor):
        """constructor
        """
        # init regs
        self.regs = RegContainer(self)
        self.receivedMessage = None
        self.sendedMessage = None
        regsfile = os.path.join(os.path.dirname(__file__), '../dapi2/dreg','regs.xml')
        _ = RegContainerReader(container=self.regs, filename=regsfile)
        
        self.motor = motor
        
        self.__initRegs()
       
    def __initGeneral(self):
        """ Initialize the general registers of the board
        """
        first = 0x00
        last = 0x58
        
        for i in range(first, last):
            try:
                self.regs[i].set(0, True)
            except:
                continue
        
        self.regs.a64dcr.set(17, True)
        self.regs.a64dvr.set(1646, True)
        
        self.regs.a1tdcr.set(381, True)
        self.regs.a1tdvr.set(1294, True)
        
        self.regs.dcr.set(17, True)
        self.regs.dvr.set(1646, True)
        
        self.regs.prcr.set(403, True)
        self.regs.elcr.set(108, True)
        
        # maybe an0r and an1r
        
        self.regs.psvr.set(32000, True)
        
    def __initPpa(self):
        """Init the ppa according to the motor connected to the board
        """
        funcName = "ppa_" + self.motor.ppa
        getattr(DEmuPPA, funcName)(self.regs)
    
    def __dateEncoder(self, year, month, day):
        """Init the date according to the method describe on the dapi 2
        
        :param int year: Year of the date
        
        :param int month: Month of the date
        
        :param int day: Day of the date
        """
        return 2**9 * (year - 2000) + 2**5 * month + day 
    
    def __initSysInfo(self, boardName=30):
        """Init the sys registers
        
        :param int boardName: board name according to the factory
        """
        self.regs.sfr.set(int('0b0000000', 2), True) # SFR : System Flag Register
        self.regs.snr.set(1, True) # SNR : Serial Number Register
        self.regs.fdr.set(self.__dateEncoder(2012, 3, 16), True) # FDR : Factory Date Register
        self.regs.hvr.set(int('0b00000001', 2), True) # HVR : Hardware Version Register
        self.regs.svr.set(int('0b00000001', 2), True) # SVR : Software Version Register
        self.regs.sctr.set(0, True) # SCTR : System Configuration Tag Register
        self.regs.scsr.set(0, True) # SCSR : System Configuration Status Register
        self.regs.bvr.set(int('0b00000001', 2), True) # BVR : Bios Version Register
        self.regs.bbdr.set(self.__dateEncoder(2012, 3, 16), True) # BBDR : Bios Build Date Register
        self.regs.fbdr.set(self.__dateEncoder(2012, 3, 16), True) # FBDR : Firmware Build Date Register
        self.regs.btr.set("MB".encode('UTF-8'), True) # BTR : Board Type Register
        self.regs.bnr.set(str(boardName).encode('UTF-8'), True) # BNR : Board Name Register
        # self.regs.cfg.set(0, True) # CFG : Configuration Register !!Not used
    
    def __initRegs(self):
        """init the regs of the board
        """
        self.__initGeneral()
        self.__initPpa()
        self.__initSysInfo()
        
    def getRegisterName(self, addr):
        return str(self.regs[addr])
    
    def getReceivedData(self):
        return self.receivedMessage.getData(0, 2)
    
    def setError(self, error):
        self.sendedMessage = None
        self.sendedMessage = BaseMessage.factory(error, DApi2Side.SLAVE)
        self.sendedMessage.setAddr(self.receivedMessage.getAddr())
        
    def setReadError(self, error):
        self.setError(0x41)
        self.sendedMessage.setData(error, 0)
        
    def setCommandError(self, error):
        self.setError(0x61)
        self.sendedMessage.setData(error, 0)
        
    def setWriteError(self, error):
        self.setError(0xc1)
        self.sendedMessage.setData(error, 0)
        
    def receiveMessage(self, msg):
        """Call by the communication module when sending message
        
        :param BaseMessage msg: msg send by the client
        """
        self.sendedMessage = None
        
        self.receivedMessage = msg
        self.dispatche()
        
        self.receivedMessage = None
    
    def sendMessage(self):
        """call by the communication module when receive message
        """
        return self.sendedMessage
    
    def dispatche(self):
        """Dispatch the received message on the appropriate function
        """
        typeOfMessage = self.receivedMessage.type()
        
        if typeOfMessage == MsgType.READ:
            self.read()
        
        elif typeOfMessage == MsgType.XREAD:
            self.xread()
        
        elif typeOfMessage == MsgType.WRITE:
            self.write()
    
        elif typeOfMessage == MsgType.XWRITE:
            self.xwrite()
        
        elif typeOfMessage == MsgType.COMMAND:
            self.command()
        
        elif typeOfMessage == MsgType.XCOMMAND:
            self.xcommand()
        
        elif typeOfMessage == MsgType.RESERVED:
            self.reserved()
        
        elif typeOfMessage == MsgType.XRESERVED:
            self.xreserved()
    
    def read(self):
        """Do the stuff for a read message
        """
        self.sendedMessage = BaseMessage.factory(self.receivedMessage.func(), DApi2Side.SLAVE)
        addr = self.receivedMessage.getAddr()
        nbrBytes = self.receivedMessage.getData(0)
                
        self.sendedMessage.setAddr(addr)
        
        for i in range(0, int(nbrBytes / 2)):
            self.sendedMessage.setWord(self.regs[addr+i].get(), 0+i*2)
                        
    def xread(self):
        """Do the stuff for an extended read message
        """
        raise Exception("Not yet implemented")
        
    def write(self):
        """Do the stuff for a write message
        """
        dataLen = int(len(self.receivedMessage.getDataBytes()) / 2)
        addr = self.receivedMessage.getAddr()
        
        # make return message
        self.sendedMessage = BaseMessage.factory(self.receivedMessage.func(), DApi2Side.SLAVE)
        self.sendedMessage.setAddr(addr)
        
        # store data into regs
        try:
            for i in range(dataLen):
                getattr(self, "write_" + self.getRegisterName(addr + i))(self.receivedMessage.getData(i * 2, 2), i * 2)
        except AttributeError:
            self.setWriteError(E_MESSAGE_ERROR.DAPI_ERR_READ_ONLY)
        
    def write_par(self, value, index=0):
        """Write the par register
        
        :param int value: value to put on the register
        
        :param int index: index of the value in the message
        """
        if self.regs.par.value == 0 or self.regs.par.value > 0 and value == 0:
            self.regs.par.set(value, True)
            self.sendedMessage.setWord(self.regs.par.value, index)
        else:
            self.setWriteError(E_MESSAGE_ERROR.DAPI_ERR_WRONG_CONTEXT)
            
    def write_smr(self, value, index=0):
        """Write the smr register
        
        :param int value: value to put on the register
        
        :param int index: index of the value in the message
        """
        if value >= 0 and value <= 65535:
            self.regs.smr.set(value, True)
            self.sendedMessage.setWord(self.regs.smr.value, index)
            
    def write_scr(self, value, index=0):
        """Write the scr register
        
        :param int value: value to put on the register
        
        :param int index: index of the value in the message
        """
        if value >= self.regs[0x05].value and value <= self.regs[0x06].value:
            self.regs.scr.set(value, True)
            self.sendedMessage.setWord(self.regs.scr.value, index)
        else:
            self.setWriteError(E_MESSAGE_ERROR.DAPI_ERR_WRONG_VALUE)
    
    def write_ccr(self, value, index=0):
        """Write the ccr register
        
        :param int value: value to put on the register
        
        :param int index: index of the value in the message
        """
        if value >= 500 and value <= self.regs[0x07].value:
            self.regs.ccr.set(value, True)
            self.sendedMessage.setWord(self.regs.ccr.value, index)
        else:
            self.setWriteError(E_MESSAGE_ERROR.DAPI_ERR_WRONG_VALUE)
        
    def write_acr(self, value, index=0):
        """Write the acr register
        
        :param int value: value to put on the register
        
        :param int index: index of the value in the message
        """
        if value >= 1 and value <= self.regs[0x08].value:
            self.regs.acr.set(value, True)
            self.sendedMessage.setWord(self.regs.acr.value, index)
        else:
            self.setWriteError(E_MESSAGE_ERROR.DAPI_ERR_WRONG_VALUE)
            
    def write_lir(self, value, index=0):
        """Write the lir register
        
        :param int value: value to put on the register
        
        :param int index: index of the value in the message
        """
        if value >= 0 and value <= self.regs[0x09].value:
            self.regs.lir.set(value, True)
            self.sendedMessage.setWord(self.regs.lir.value, index)
        else:
            self.setWriteError(E_MESSAGE_ERROR.DAPI_ERR_WRONG_VALUE)
            
    def write_ldr(self, value, index=0):
        """Write the ldr register
        
        :param int value: value to put on the register
        
        :param int index: index of the value in the message
        """
        if value >= 0 and value <= 65535:
            self.regs.ldr.set(value, True)
            self.sendedMessage.setWord(self.regs.ldr.value, index)
        else:
            self.setWriteError(E_MESSAGE_ERROR.DAPI_ERR_WRONG_VALUE)
        
    def write_grnr(self, value, index=0):
        """Write the grnr register
        
        :param int value: value to put on the register
        
        :param int index: index of the value in the message
        """
        raise Exception("Not yet implemented")
    
    def write_grdr(self, value, index=0):
        """Write the grdr register
        
        :param int value: value to put on the register
        
        :param int index: index of the value in the message
        """
        raise Exception("Not yet implemented")
    
    def write_fwpr(self, value, index=0):
        """Write the fwpr register
        
        :param int value: value to put on the register
        
        :param int index: index of the value in the message
        """
        raise Exception("Not yet implemented")
    
    def write_bwpr(self, value, index=0):
        """Write the bwpr register
        
        :param int value: value to put on the register
        
        :param int index: index of the value in the message
        """
        raise Exception("Not yet implemented")
    
    def write_mdr(self, value, index=0):
        """Write the mdr register
        
        :param int value: value to put on the register
        
        :param int index: index of the value in the message
        """
        if value >= 0 and value <= 65535:
            self.regs.mdr.set(value, True)
            self.sendedMessage.setWord(self.regs.mdr.value, index)
        else:
            self.setWriteError(E_MESSAGE_ERROR.DAPI_ERR_WRONG_VALUE)
    
    def write_pdr(self, value, index=0):
        """Write the pdr register
        
        :param int value: value to put on the register
        
        :param int index: index of the value in the message
        """
        if value >= 0 and value <= 65535:
            self.regs.pdr.set(value, True)
            self.sendedMessage.setWord(self.regs.pdr.value, index)
        else:
            self.setWriteError(E_MESSAGE_ERROR.DAPI_ERR_WRONG_VALUE)
    
    def write_tmr(self, value, index=0):
        """Write the tmr register
        
        :param int value: value to put on the register
        
        :param int index: index of the value in the message
        """
        if value >= 0 and value <= 50:
            self.regs.tmr.set(value, True)
            self.sendedMessage.setWord(self.regs.tmr.value, index)
        else:
            self.setWriteError(E_MESSAGE_ERROR.DAPI_ERR_WRONG_VALUE)
    
    def write_alr(self, value, index=0):
        """Write the alr register
        
        :param int value: value to put on the register
        
        :param int index: index of the value in the message
        """
        if value == 0 or value == 256:
            self.regs.alr.set(value, True)
            self.sendedMessage.setWord(self.regs.alr.value, index)
        else:
            self.setWriteError(E_MESSAGE_ERROR.DAPI_ERR_WRONG_VALUE)
    
    def write_fscr(self, value, index=0):
        """Write the fscr register
        
        :param int value: value to put on the register
        
        :param int index: index of the value in the message
        """
        if value >= 0 and value <= self.regs[0x06].value:
            self.regs.fscr.set(value, True)
            self.sendedMessage.setWord(self.regs.fscr.value, index)
        else:
            self.setWriteError(E_MESSAGE_ERROR.DAPI_ERR_WRONG_VALUE)
    
    def xwrite(self):
        """Do the stuff for an extended write message
        """
        raise Exception("Not yet implemented")
    
    def command(self):
        """Do the stuff for a command message
        """
        raise Exception("Not yet implemented")
    
    def xcommand(self):
        """Do the stuff for an extended command message
        """
        raise Exception("Not yet implemented")
    
    def reserved(self):
        """Do the stuff for a reserved message
        """
        raise Exception("Not yet implemented")
    
    def xreserved(self):
        """Do the stuff for an extended reserved message
        """
        raise Exception("Not yet implemented")
    
    
        