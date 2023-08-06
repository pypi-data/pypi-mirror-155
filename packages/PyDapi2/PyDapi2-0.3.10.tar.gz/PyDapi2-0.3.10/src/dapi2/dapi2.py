'''Module for DApi2 object class. 

:author: F. Voilat
:date: 2021-02-24 Creation
'''

import logging
from itertools import groupby
from operator import itemgetter
from os.path import os


from . import dmsg, REG_SIZE
from .dreg import RegContainer, RegContainerReader, RegisterArray


from .common import DApi2Side
from . import _version 
from .common import dateToWord, versionToWord, DIntEnum
from .derror import DApiCommandError, DErrorsContainer



class DApi2(object):
    '''Class for DAPI2 object. 
    
    This object is used to handle and manage the registers and commands of the DAPI2 protocol
    
    :param DBaseCom dcom: Communication channel  
    '''


    def __init__(self, dcom, regsfile=None, dev_mode=False, errorsfile=None):
        '''Constructor'''
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug('Initialize')
        self.regs = RegContainer(self)
        self.lastError = 0
        
        self.cmd = DApi2Commands(self)
        
        if regsfile is None:
            regsfile = os.path.join(os.path.dirname(__file__), 'dreg','regs.xml')
        
        _ = RegContainerReader(container=self.regs, filename=regsfile)
        
        if errorsfile is None:
            errorsfile = os.path.join(os.path.dirname(__file__), 'errors.xml')        
        self.derrors = DErrorsContainer(self, errorsfile) 
        
        self.dcom = dcom
        self.dev_mode = dev_mode
        
    def version(self):
        '''Returns the DAPI2 version'''
        return _version.__version__
        
        
    def sendMessage(self, msg):
        '''Sends a message to the `SLAVE` and waits its response.
        
        :param BaseMasterMessage msg: The message to send.
        
        :return The response message received from the `SLAVE`
        :rtype: BaseSlaveMessage.
        '''
        assert self.dcom.side == DApi2Side.MASTER
        self.dcom.sendMessage(msg)
        res = self.dcom.receiveMessage(msg.type())
        if res.isError():
            self.lastErrorNo = res.getError()
        else:
            self.lastErrorNo = 0
        return res 
        
        
    def readRegGroup(self, group):
        '''Read all registers of a group.
        
        :param RegGroup group: The registers group (:class:`~dapi2.dreg.group.RegGroup`). 
        '''
        self.readRegs(group.regs)
        
    def readRegs(self, *regs, length=0): 
        '''Read a list of registers.
        
        :note: The registers in list must be continuous. 
        
        :param Register or list regs: The list of registers (:class:`~dapi2.dreg.register.Register`). 
        '''    
        def _readRegs(regs):
            msg = dmsg.ReadRegMessage(regs[0].addr, len(regs)*REG_SIZE)
            msg = self.sendMessage(msg)
            for i, reg in enumerate(regs):
                v = msg.getData(i*REG_SIZE, REG_SIZE)
                reg.internalSet(v)
        
        if len(regs) == 0:
            return 
        #assert (length == 0 or len(regs)==1) and isinstance(regs[0], BaseRegElement), 'regs[0]='+str(regs[0])
        #print(len(regs) == 1 or any((isinstance(item,BaseRegElement) for item in regs)))
        if length > 0:
            regs = self.regs[regs[0].addr:regs[0].addr+length]
        elif len(regs) == 1 and isinstance(regs[0], (list,tuple)):
            regs = regs[0]
        else:
            regs = list(regs)
            
        
        regs.sort()
        if isinstance(regs[0], RegisterArray):
            cregs = [list(regs[0])]
        else:
            cregs = [[regs[0]]]
        for r in regs[1:]:
            if isinstance(r, RegisterArray):
                cregs.append(list(r))
            elif r.addr == cregs[-1][-1].addr+1:
                cregs[-1].append(r)
            else:
                cregs.append([r])
        #assert regs[-1].addr - regs[0].addr +1 == len(regs), 'Registers must be continuous'
        for regs in cregs:
            chunks = [regs[i:i + 4] for i in range(0, len(regs), 4)]  
            for chunk in chunks:
                _readRegs(chunk) 
        
    def readReg(self, reg):
        '''Read one register.
        
        :param Register reg: The register to read. 
        '''
        self.readRegs(reg)
        
    
    def writeRegs(self, regs):
        '''Write a list of registers.
        
        :note: The registers in list must be continuous. 
        
        :param list regs: The list of registers (:class:`~dapi2.dreg.register.Register`). 
        '''

        def _writeRegs(regs):
            #print('regs:',' '.join((str(x) for x in regs))  ) 
            msg = dmsg.WriteRegMessage(regs[0].addr, [r.get() for r in regs])
            msg = self.sendMessage(msg)
            for i, reg in enumerate(regs):
                v = msg.getData(i, REG_SIZE)
                reg.internalSet(v)
        
        
        regs.sort() 
        assert regs[-1].addr - regs[0].addr +1 == len(regs), 'Registers must be continuous'
        chunks = [regs[i:i + 4] for i in range(0, len(regs), 4)]  
        for chunk in chunks:
            if len(chunk)>0:
                _writeRegs(chunk) 
    
    def writeReg(self, reg, value=None):
        '''Write one register.
        
        :param Register reg: The register to write. 
        :param int value: The new value of the register before writing it. 
        '''
        if value is not None:
            reg.internalSet(value)
        self.writeRegs([reg])
        
    def syncRegs(self):
        tmp = enumerate(self.regs.modifiedRegs())
        for _, g in groupby(tmp, lambda x: x[0]-x[1].addr):
            regs = list(map(itemgetter(1), g))
            self.writeRegs(regs)
            
        

class DApiAccessLevel(DIntEnum):
    '''Enumeration for DAPI2 access level'''
    NO = 0
    '''No access or disconnected'''
    USER = 1
    '''*User* access level.'''
    SERVICE = 2
    '''*Service* access level.'''
    FACTORY = 3
    '''*Factory* access level.'''
    
    @property
    def label(self):
        '''Label according access level'''
        return {
            self.NO : 'No',
            self.USER : 'User',
            self.SERVICE : 'Service',
            self.FACTORY : 'Factory',
            }[self]    

    @property
    def help(self):
        '''Help message accordinDApiAccessLevelg access level'''
        return {
            self.NO : 'No access granted.',
            self.USER : 'Standard acces.',
            self.SERVICE : 'Large access for services.',
            self.FACTORY : 'Extended access for factory.',
            }[self]    
    
    @property
    def passwd(self):
        '''Passwords corresponding to the access level'''
        return {
            self.NO : 0x0000,
            self.USER : 0x0000,
            self.SERVICE : 0xe8e8,
            self.FACTORY : 0xf3f3,
            }[self]    


class DApiAdditionalBoard(DIntEnum):
    '''Enumeration for DAPI2 access level'''
    NO = 0
    AB12 = 1
    AB03 = 2
    
    @property
    def descr(self):
        '''Label according access level'''
        return {
            self.NO : 'No',
            self.AB12 : 'AB-12',
            self.AB03 : 'AB-03',
            }[self]    

    @property
    def help(self):
        '''Help message according access level'''
        return {
            self.NO : 'No additional board is present.',
            self.AB12 : 'Auxiliary inputs board (AB-12) is present.',
            self.AB03 : 'Dual lighting (AB-03) is present.',
            }[self]    
        
class MetaDApi2Commands(object):
    NULL                  = 0x00
    '''*Null* command'''
    REBOOT                = 0x01
    '''Board reboot'''
    
    STANDBY               = 0x02
    '''Set the system in stand-by mode'''
    
    PERIPHERAL_ACTIVATE   = 0x03
    '''Activates a peripheral.'''
    
    EMERGENCY             = 0x04
    '''Immediately disable the drivers and set the system in stand-by mode'''
    
    CONNECT               = 0x05
    '''Connection of the MASTER to the board'''
    
    DISCONNECT            = 0x06
    '''Disconnection of the MASTER from board'''
    
    GET_MC_SN             = 0x09
    '''Get the micro-controller unique identifier'''
    
    BOOT_FLASH            = 0x0a
    '''Puts the system in flash boot mode'''
    
    MOTOR_FREEWHEEL_STOP = 0x20
    '''Freewheel motor stop'''
    
    MOTOR_STOP           = 0x21
    '''Controlled motor stop'''
    
    MOTOR_START          = 0x22
    '''Starts the motor and sets the speed.'''
    
    MOTOR_INC_SPEED      = 0x23
    '''Increase motor speed'''
    
    MOTOR_DEC_SPEED      = 0x24
    '''Decrease motor speed'''
    
    MOTOR_REVERSE        = 0x25 
    '''Reverse the motor direction'''
    
    LIGHT_OFF            = 0x40
    '''Turn light off.'''
    
    LIGHT_ON             = 0x41
    '''Turn light on.'''
    
    LIGHT_INTENSITY      = 0x42
    '''Sets the light intensity'''
    
    LIGHT_ALTERNATE      = 0x43 
    '''Sets the alternate light'''    
    

    
    
    MEMORY_STORE          = 0x50 
    '''Store user set points into EEPROM.'''
    
    MEMORY_RECALL        = 0x51
    '''Recall user set points from EEPROM'''
    
    MEMORY_READ           = 0x52
    '''Read user set points from EEPROM'''
    
    MEMORY_RESET          = 0x53
    '''Reset user set points with factory values'''
    
    MEMORY_SET            = 0x54
    '''Gets any set point from EEPROM.'''
    
    MEMORY_GET            = 0x55
    '''Sets any set point to the EEPROM'''
    
    # DIAG_0                = 0x60
    # DIAG_1                = 0x61
    # DIAG_2                = 0x62
    # DIAG_3                = 0x63
    
    FACT_EEPROM_RESET     = 0x80
    FACT_SET_SYSINFO      = 0x81
    FACT_SET_SRVINFO      = 0x82
    FACT_CALIBRATION      = 0x83
    
    FLASH_BEGIN           = 0x90
    FLASH_DATA            = 0x91
    FLASH_END             = 0x92
    
    DEBUG_BURST           = 0xC0
    DEBUG_READ_WORD       = 0xC2
    DEBUG_WRITE_WORD      = 0xC3
        
class DApi2Commands(MetaDApi2Commands):
    

    _index = {
        MetaDApi2Commands.NULL   : "*Null* command",
        MetaDApi2Commands.REBOOT : "Board reboot",
        MetaDApi2Commands.STANDBY : "Set the system in stand-by mode",
        MetaDApi2Commands.PERIPHERAL_ACTIVATE : "Activates a peripheral.",
        MetaDApi2Commands.EMERGENCY : "Immediately disable the drivers and set the system in stand-by mode",
        MetaDApi2Commands.CONNECT : "Connection of the MASTER to the board",
        MetaDApi2Commands.DISCONNECT : "Disconnection of the MASTER from board",
        MetaDApi2Commands.GET_MC_SN : "Get the micro-controller unique identifier",
        MetaDApi2Commands.BOOT_FLASH : "Puts the system in flash boot mode",
        MetaDApi2Commands.MOTOR_FREEWHEEL_STOP : "Freewheel motor stop",
        MetaDApi2Commands.MOTOR_STOP : "Controlled motor stop",
        MetaDApi2Commands.MOTOR_START : "Starts the motor and sets the speed.",
        MetaDApi2Commands.MOTOR_INC_SPEED : "Increase motor speed",
        MetaDApi2Commands.MOTOR_DEC_SPEED : "Decrease motor speed",
        MetaDApi2Commands.MOTOR_REVERSE : "Reverse the motor direction",
        MetaDApi2Commands.LIGHT_OFF : "Turn light off.",
        MetaDApi2Commands.LIGHT_ON : "Turn light on.",
        MetaDApi2Commands.LIGHT_INTENSITY : "Sets the light intensity",
        MetaDApi2Commands.LIGHT_ALTERNATE : "Sets the alternate light",
        MetaDApi2Commands.MEMORY_STORE : "Store user set points into EEPROM.",
        MetaDApi2Commands.MEMORY_RECALL : "Recall user set points from EEPROM",
        MetaDApi2Commands.MEMORY_READ : "Read user set points from EEPROM",
        MetaDApi2Commands.MEMORY_RESET : "Reset user set points with factory values",
        MetaDApi2Commands.MEMORY_SET : "Gets any set point from EEPROM.",
        MetaDApi2Commands.MEMORY_GET : "Sets any set point to the EEPROM",
        MetaDApi2Commands.FACT_EEPROM_RESET : "Reset E²PROM to factory values",
        MetaDApi2Commands.FACT_SET_SYSINFO : "Sets factory information",
        MetaDApi2Commands.FACT_SET_SRVINFO : "Sets after-sale service information",
        MetaDApi2Commands.FACT_CALIBRATION : "Starts the calibration procedure",
        MetaDApi2Commands.FLASH_BEGIN : "Starts the flash programming procedure",
        MetaDApi2Commands.FLASH_DATA : "Send data for flash programming procedure",
        MetaDApi2Commands.FLASH_END : "Terminates the flash programming procedure",
        MetaDApi2Commands.DEBUG_BURST : "Debug: simulates a electrical burst",
        MetaDApi2Commands.DEBUG_READ_WORD : "Debug: read a word (16bit) from MCU memory",
        MetaDApi2Commands.DEBUG_WRITE_WORD : "Debug: write a word (16bit) into MCU memory",
    }
    
    def __init__(self, owner):
        assert isinstance(owner, DApi2)
        self.owner = owner
        
    def _sendCmd(self, msg, *exceptions):
        msg = self.owner.sendMessage(msg)
        if msg.isError():
            raise DApiCommandError.factory(msg, *exceptions)
        return msg
        
    def connect(self, level=DApiAccessLevel.USER, passwd=DApiAccessLevel.USER.passwd):
        msg = dmsg.CommandMessage(DApi2Commands.CONNECT)
        msg.setByte(level)
        msg.setWord(passwd)
        msg = self._sendCmd(msg, DApiCmdConnectionDeniedError)
        
        
    def disconnect(self):
        msg = dmsg.CommandMessage(DApi2Commands.DISCONNECT)
        msg = self._sendCmd(msg)
        
    def standby(self):
        msg = dmsg.CommandMessage(DApi2Commands.STANDBY)
        msg = self._sendCmd(msg)
    
    
    def peripheralActivate(self, value):
        if value != 0 and self.owner.regs.par.value != 0 and not self.owner.dev_mode:
            self.standby()
        msg = dmsg.CommandMessage(DApi2Commands.PERIPHERAL_ACTIVATE)
        msg.setWord(value)
        msg = self._sendCmd(msg)
        
            
        
    def getMcId(self, part):
        msg = dmsg.CommandMessage(DApi2Commands.GET_MC_SN)
        msg.setByte(part)
        msg = self._sendCmd(msg)
        return msg.getDataBytes()
        
    def bootflash(self):    
        msg = dmsg.CommandMessage(DApi2Commands.BOOT_FLASH)
        msg = self._sendCmd(msg)
         
    
    def factEerpomReset(self):    
        msg = dmsg.CommandMessage(DApi2Commands.FACT_EEPROM_RESET)
        msg = self._sendCmd(msg)
         
    
    def factSetSysinfo(self, sn, date, hv):    
        date = dateToWord(date)
        hv = versionToWord(*hv)
        msg = dmsg.CommandMessage(DApi2Commands.FACT_SET_SYSINFO)
        msg.setWord(sn)
        msg.setWord(date)
        msg.setWord(hv)
        msg = self._sendCmd(msg)
        self.owner.regs.snr.value = sn
        self.owner.regs.fdr.value = date
        self.owner.regs.hvr.value = hv
         

    def factSetSrvinfo(self, service, date, tag):    
        msg = dmsg.CommandMessage(DApi2Commands.FACT_SET_SRVINFO)
        msg.setWord(service)
        msg.setWord(dateToWord(date))
        msg.setWord(tag)
        msg = self._sendCmd(msg)
        
    
    def factCalibration(self, item, step):    
        msg = dmsg.CommandMessage(DApi2Commands.FACT_CALIBRATION)
        msg.setByte(item)
        msg.setByte(step)
        msg = self._sendCmd(msg, DApiCmdCalibrationItemError, DApiCmdCalibrationStepError)
        

    def factCtrl(self, ctrl, p0, p1):    
        msg = dmsg.CommandMessage(DApi2Commands.FACT_CTRL)
        msg.setByte(ctrl)
        msg.setByte(p0)
        msg.setWord(p1)
        msg = self._sendCmd(msg)
        
        
    def motorFreewheelStop(self):
        msg = dmsg.CommandMessage(DApi2Commands.MOTOR_FREEWHEEL_STOP)
        msg = self._sendCmd(msg)
        if self.owner.regs.smr.isUndefined():
            self.owner.readReg(self.owner.regs.smr)
        self.owner.regs.smr.bits.freewheel.set()
        self.owner.regs.smr.bits.start.clear()
        

    def motorStop(self):
        msg = dmsg.CommandMessage(DApi2Commands.MOTOR_STOP)
        msg = self._sendCmd(msg)
        if self.owner.regs.smr.isUndefined():
            self.owner.readReg(self.owner.regs.smr)
        self.owner.regs.smr.bits.freewheel.clear()
        self.owner.regs.smr.bits.start.clear()
        
        
    def motorStart(self, speed=0):
        msg = dmsg.CommandMessage(DApi2Commands.MOTOR_START)
        msg.setWord(speed)
        msg = self._sendCmd(msg)
        if self.owner.regs.smr.isUndefined():
            self.owner.readReg(self.owner.regs.smr)
        self.owner.regs.smr.bits.start.set()
        if speed != 0:
            self.owner.readReg(self.owner.regs.scr)
            #self.owner.regs.scr.value = speed
       
    def motorIncSpeed(self, inc=1):
        msg = dmsg.CommandMessage(DApi2Commands.MOTOR_INC_SPEED)
        msg.setWord(inc)
        msg = self._sendCmd(msg)
        self.owner.regs.scr.value += inc
    
    def motorDecSpeed(self, dec=1):
        msg = dmsg.CommandMessage(DApi2Commands.MOTOR_DEC_SPEED)
        msg.setWord(dec)
        msg = self._sendCmd(msg)
        self.owner.regs.scr.value -= dec
    
    def motorReverse(self):
        msg = dmsg.CommandMessage(DApi2Commands.MOTOR_REVERSE)
        msg = self._sendCmd(msg)
        if self.owner.regs.smr.isUndefined():
            self.owner.readReg(self.owner.regs.smr)
        self.owner.regs.smr.bits.reverse.toggle()
        
    def lightOff(self):
        msg = dmsg.CommandMessage(DApi2Commands.LIGHT_OFF)
        msg = self._sendCmd(msg)
        if self.owner.regs.smr.isUndefined():
            self.owner.readReg(self.owner.regs.smr)
        self.owner.regs.smr.bits.light.clear()
        
    def lightOn(self):
        msg = dmsg.CommandMessage(DApi2Commands.LIGHT_ON)
        msg = self._sendCmd(msg)
        if self.owner.regs.smr.isUndefined():
            self.owner.readReg(self.owner.regs.smr)
        self.owner.regs.smr.bits.light.set()

    def lightIntensity(self, intensity):
        msg = dmsg.CommandMessage(DApi2Commands.LIGHT_INTENSITY)
        msg.setWord(intensity)
        msg = self._sendCmd(msg)
        self.owner.regs.lir.value = intensity  
        

    def lightAlternate(self, alternate):
        msg = dmsg.CommandMessage(DApi2Commands.LIGHT_ALTERNATE)
        msg.setWord(alternate)
        msg = self._sendCmd(msg)
        self.owner.regs.alr.value = alternate
        

    def memoryStore(self, index):
        msg = dmsg.CommandMessage(DApi2Commands.MEMORY_STORE)
        msg.setByte(index)
        msg = self._sendCmd(msg)
        

    def memoryRecall(self, index):
        msg = dmsg.CommandMessage(DApi2Commands.MEMORY_RECALL)
        msg.setByte(index)
        msg = self._sendCmd(msg)
        

    def memoryRead(self, peripheral, memory, page):
        msg = dmsg.CommandMessage(DApi2Commands.MEMORY_READ)
        msg.setByte(peripheral)
        msg.setByte(memory)
        msg.setByte(page)
        msg = self._sendCmd(msg)
        return msg.getDataWords()
        
    def memoryReset(self):
        msg = dmsg.CommandMessage(DApi2Commands.MEMORY_RESET)
        msg = self.owner._sendCmd(msg)
        
    def memoryGet(self, peripheral, memory, page):
        msg = dmsg.CommandMessage(DApi2Commands.MEMORY_READ)
        msg.setByte(peripheral)
        msg.setByte(memory)
        msg.setByte(page)
        msg = self._sendCmd(msg)
        return msg.getDataBytes()
        
    def flashBegin(self, size):
        msg = dmsg.CommandMessage(DApi2Commands.FLASH_BEGIN)
        msg.setDWord(size)
        msg = self._sendCmd(msg, DApiCmdFlashError, DApiCmDFlashUnexpectedEndError)
        
    def flashData(self, buf):
        msg = dmsg.CommandMessage(DApi2Commands.FLASH_DATA)
        for b in buf:
            msg.setByte(b)
        msg = self._sendCmd(msg, DApiCmdFlashError, DApiCmDFlashUnexpectedEndError)
        
    def flashEnd(self):
        msg = dmsg.CommandMessage(DApi2Commands.FLASH_END)
        msg = self._sendCmd(msg, DApiCmdFlashError, DApiCmDFlashUnexpectedEndError)
        
        
    
class DApiCmdConnectionDeniedError(DApiCommandError):
    errorno = (0x81,0x81)
    name    = 'DAPI_CMD_CONNECTION_DENIED'
    label   = 'Connection denied'
    text    = 'Connection denied'    

class DApiCmdCalibrationItemError(DApiCommandError):
    errorno = (0x81,0x81)
    name    = 'DAPI_CMD_CALIBRATION_WRONG_ITEM'
    label   = 'Wrong item'
    text    = 'Wrong item'    

class DApiCmdCalibrationStepError(DApiCommandError):
    errorno = (0x82,0x82)
    name    = 'DAPI_CMD_CALIBRATION_WRONG_STEP'
    label   = 'Wrong step'
    text    = 'Wrong step'    

class DApiCmdFlashError(DApiCommandError):
    errorno = (0x81,0x81)
    name    = 'DAPI_CMD_FLASH_FAILURE'
    label   = 'Flash failure'
    text    = 'Flash failure'    
        
class DApiCmDFlashUnexpectedEndError(DApiCommandError):
    errorno = (0x82,0x82)
    name    = 'DAPI_CMD_FLASH_ENEXPECTED_END'
    label   = 'Flash unexpected end'
    text    = 'Flash unexpected end'    
        