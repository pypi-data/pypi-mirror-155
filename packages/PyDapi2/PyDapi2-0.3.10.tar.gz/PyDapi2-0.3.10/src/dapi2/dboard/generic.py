'''Module to define the generic class of Dassym's electronic board representation.

:author: F. Voillat
:date: 2021-02-24 Creation
'''

from .base import BaseDBoard, DBoardPreferredDapiMode


class GenericBoard(BaseDBoard):
    '''Generic class board.
    
    This class is used when the type of card could not be determined.
    ''' 
    number = '00'
    '''Board type number (str)'''

    def __init__(self, dapi, dmode=DBoardPreferredDapiMode.REGISTER):
        '''Constructor'''
        super().__init__(dapi, dmode)
        self.speed_range.set(0,40000)         