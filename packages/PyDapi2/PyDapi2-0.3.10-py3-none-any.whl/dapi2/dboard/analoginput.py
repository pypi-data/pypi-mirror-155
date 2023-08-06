'''

:author: fv
:date: Created on 16 juin 2021
'''
from .common import BaseBoardItem, CalibrationProcessState



class BaseAnalogInput(BaseBoardItem):
    CAL_NEEDED = False
    
    def __init__(self, board, name, reg, cal_state_index=0, factor=1/10000):
        super().__init__(board, name)
        self.reg = reg
        self.factor = factor
        self.cal_state_index = cal_state_index
        self.cal_process_state = CalibrationProcessState.IDLE
    
    def isCalibrated(self):
        return self._board.regs.sfr.value & (1<<(1+self.cal_id))
    
    def getValue(self, refresh=False):
        if refresh:
            self._board.readReg(self.reg)
        return float(self.reg.value * self.factor)
    
    def calibration(self, phase, param=None):
        assert False, 'TODO:calibration'
        
    @property
    def value(self):
        return self.getValue()
    
class PressureSensor(BaseAnalogInput):
    CAL_NEEDED = True
    def __init__(self, board, name, reg, cal_state_index=1, factor=1/100):
        super().__init__(board, name, reg, cal_state_index, factor)
    
class ElectricalSensor(BaseAnalogInput):
    CAL_NEEDED = False
    def __init__(self, board, name, reg, cal_state_index=0, factor=1/100):
        super().__init__(board, name, reg, cal_state_index, factor=factor)

class ReferenceSensor(BaseAnalogInput):
    CAL_NEEDED = False
    def __init__(self, board, name, reg, cal_state_index=0, factor=1/100):
        super().__init__(board, name, reg, cal_state_index, factor=factor)


class PowerSupply(BaseAnalogInput):
    CAL_NEEDED = False
    def __init__(self, board, name, reg, cal_state_index=0 ):
        super().__init__(board, name, reg, cal_state_index, factor=1/1000)
