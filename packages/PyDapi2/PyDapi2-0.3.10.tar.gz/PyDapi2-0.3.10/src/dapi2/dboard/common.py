'''Module to define the common parts of Dassym's electronic board representation.

:author: F. Voillat
:date: 2021-02-24 Creation
'''
from enum import IntEnum, IntFlag
import logging



class DBoardException(Exception):
    '''Base class for the exceptions of the dboard package.
    
    :param obj: Object from which the exception was thrown.
    :type obj: object 
    :param context: Context (mainly the method) from which the exception was thrown.
    :type context: str
    :param message: Message explaining the exception.
    :type message: str
    '''
    
    def __init__(self, obj, context, message, *others):
        super(Exception, self).__init__(obj, context, message, *others)
        return

    def __str__(self):
        try:
            return '{0:s}::{1!s} - {2!s}\n{3!s}'.format(self.__class__.__name__, self.args[0], self.args[1], self.args[2])
        except:
            return Exception.__str__(self)

    @property
    def object(self):
        '''Returns the object from which the exception was thrown.'''
        return self.args[0]
    @property
    def context(self):
        '''Returns the context (mainly the method) from which the exception was thrown.'''
        return self.args[1]
    @property
    def message(self):
        '''Rreturns the message explaining the exception.'''
        return self.args[2]  

class DBoardPreferredDapiMode(IntEnum):
    '''Preferred mode for using the DAPI'''
    REGISTER = 0 
    '''Control the electronic board through the registers.'''
    COMMAND = 1
    '''If possible, control the electronic board using the commands.'''


class ValueRange(object):
    '''Class to store a values range
    
    :param int lower: The low value
    :param int upper: The high value
    '''
    
    def __init__(self, lower, upper):
        self.set(lower, upper)
            
    def set(self, lower, upper):
        '''Sets the lower and upper values of the range. If necessary, order the values.

        :param int lower: The low value
        :param int upper: The high value
        '''
        if lower <= upper:
            self.lower = lower
            self.upper = upper
        else:
            self.lower = upper
            self.upper = lower
    
    @property
    def size(self):
        '''The size of the range.'''
        return self.upper - self.lower +1

class SystemModeConfig(IntFlag):
    '''System Mode configuration Flags. According DAPI2 SMR register.'''
    
    START =       2**0 
    HOLDING =     2**3
    ROCKING =     2**4
    AUTOBOOST =   2**5
    AUTOSTOP =    2**6
    AUTOREVERSE = 2**7
    REVERSE =     2**8      
    QUADRATIC =   2**9
    LIGHT =       2**10
    FREEWHEEL =   2**11
    INDIRECT =    2**12
    LIGHTAUTO =   2**14
       
    @classmethod
    def get_descr(cls, value, index):
        DESCR_HELPS = {
            SystemModeConfig.START      : ('Start',       'Start',      'S',  ),
            SystemModeConfig.HOLDING    : ('Holding',     'Holding',    'H',  ),
            SystemModeConfig.ROCKING    : ('Rocking',     'Rocking',    'R',  ), 
            SystemModeConfig.AUTOBOOST  : ('Autoboost',   'Autoboost',  'AB', ),
            SystemModeConfig.AUTOSTOP   : ('Autostop',    'Autostop',   'AS', ),
            SystemModeConfig.AUTOREVERSE: ('Autorevers',  'Autoreverss','AR', ),
            SystemModeConfig.REVERSE    : ('Reverse',     'Reverse',    'R',  ),
            SystemModeConfig.QUADRATIC  : ('Quadratic',   'Quadratic',  'Q',  ), 
            SystemModeConfig.LIGHT      : ('Light',       'Light',      'L',  ), 
            SystemModeConfig.FREEWHEEL  : ('Freewheel',   'Freewheel',  'F',  ),
            SystemModeConfig.INDIRECT   : ('Indirect',    'Indirect',   'I',  ),
            SystemModeConfig.LIGHTAUTO  : ('LighAuto',    'LighAuto',   'AL', ),
        }
        return DESCR_HELPS[value][index]
    
    @property
    def descr(self):
        return self.get_descr(self, 0)
    @property
    def help(self):
        return self.get_descr(self, 1)
    @property
    def shortname(self):
        return self.get_descr(self, 2)
    
class LastReset(IntEnum):
    '''Last board reset cause.''' 
    
    DAPI = 0
    POWERUP = 1
    SOFTWARE = 2
    WATCHDOG = 4
    POWERDISTURBANCE = 5

    @classmethod
    def get_descr(cls, value, index):
        DESCR_HELPS = {
            LastReset.DAPI             : ('DAPI',              'software by DAPI',                ),
            LastReset.POWERUP          : ('Power Up',          'hardware after power up',         ),
            LastReset.SOFTWARE         : ('Software',          'software',                        ),
            LastReset.WATCHDOG         : ('Watch dog',         'Software by after watch dog ',    ),
            LastReset.POWERDISTURBANCE : ('Power disturbance', 'harware after power disturbance', ),
        }
        return DESCR_HELPS[value][index]
    
    @property
    def descr(self):
        return self.get_descr(self, 0)
    @property
    def help(self):
        return self.get_descr(self, 1)
    
    
class CalibrationProcessState(IntEnum):
    '''State of the calibration process'''
    ERROR = -3
    WARNING = -2
    ABORTED = -1
    IDLE = 0
    PENDING = 1
    COMPLETED = 9
    

    
class BaseBoardItem(object):
    '''Base class for board's items.
    
    :param BaseBoard board: The owner's board of the element
    :name str name: The element name
    '''
    def __init__(self, board, name=None):
        self._log = logging.getLogger(self.__class__.__name__)
        self._log.debug('Construct ' + (name or '') )
        self._board = board
        self._name = name or self.__class__.__name__ 
    
    @property
    def board(self):
        '''The board that owns the item.'''
        return self._board
    
    @property
    def com(self):
        '''Shortcuts to the communication system of the board owner of the element.'''
        return self.board.com

    @property
    def name(self):
        '''The item's name'''
        return self._name
    
    @property
    def log(self):
        '''The item's logger'''
        return self._log      
