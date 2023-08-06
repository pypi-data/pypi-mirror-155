'''Module to define the class of MB-60 Dassym's electronic board representation.

:author: F. Voillat
:date: 2021-02-24 Creation
'''
from .base import DBoard, DacSignal, DBoardPreferredDapiMode


class DacSignalMb60(DacSignal):
    DPA_VIRT = 0
    DPA_REAP = 1
    PHI = 2
    DRAG = 3
    PWM_OPENING = 4
    
    

class Board60(DBoard):
    '''Class for MB-60 Dassym's board.
    
    .. inheritance-diagram:: Board60
        :parts: 1
    
    '''
    
    number = '60'
    '''Board type number (str)'''
    
    DAC_SIGNAL = DacSignalMb60

    def __init__(self, dapi, dmode=DBoardPreferredDapiMode.REGISTER):
        '''Constructor'''
        super().__init__(dapi, dmode)
        self.speed_range.set(0,40000)         