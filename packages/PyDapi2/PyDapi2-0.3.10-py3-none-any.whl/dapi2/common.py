from enum import IntEnum
import datetime as DT


REG_SIZE = 2
'''Register size in byte'''

REG_MAX_VALUE = 0xFFFF
'''Register max value'''

def wordToDate(value):
    '''Converts date encoded in a 16-bits (word) integer to Date.
    
    :param int value: The date  encoded in a word.
    :return: The converted Date, if *value* is between 1 and 65534, otherwise None.   
    :rtype: Date
    '''  
    if value==0 or value==0xffff: 
        return None
    else:
        try:
            return DT.date( 2000+((value & 0xfe00)//0x200), (value & 0x1e0)//0x20, (value & 0x1f) )
        except ValueError:
            return None

def dateToWord(value):
    '''Converts a date to 16-bits (word) integer.
    
    .. math::
    
        W = {(Year-2000) \\times 2^{9} + Month \\times 2^{9} + Day}
    
    :param Date value: The date to convert.
    :return: The date encoded in word.  
    :rtype: int
    '''
    return ((value.year-2000) * 0x200 + value.month * 0x20 + value.day) & 0xffff

def versionToWord(major, minor):
    '''Converts major and minor version number to 16-bits (word) integer.
    
    :param int major: Major version number
    :param int minor: Minor version number
    :return: The version number encoded in word.
    :rtype: int
    '''
    return ((major & 0xFF)<<8) | (minor & 0xFF)   

def wordToVersion(value):
    '''Converts  16-bits (word) integer to major and minor version number.
    
    :param int value: The word to convert
    :return: The version number in 2-tuple of integer.
    :rtype: tuple
    '''
    return (value >> 8, value & 0xFF)   

def versionToStr(ver):
    '''Converts version to str.
    
    :param tuple ver: The version tuple with major and minor number to convert.
    :return: The version in format n.mm
    :rtype: str
    '''
    return "{0:d}.{1:02d}".format(*ver)


class DIntEnum(IntEnum):
    
    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))    
    
    @classmethod
    def listLower(cls):
        return list(map(lambda c: c.name.lower(), cls))    

    @classmethod
    def listUpper(cls):
        return list(map(lambda c: c.name.upper(), cls))    


class DApi2Side(DIntEnum): 
    '''Enumeration of both sides of DAPI2 communication'''
    MASTER = 0
    '''The 'MASTER' side, usually the PC.'''
    SLAVE = 1
    '''The 'SLAVE' side, generally the Dassym electronic card.'''
    
    def reverse(self):
        '''Return the other end of the link
        
        :return: Dapi2Side.MASTER if SLAVE else Dapi2Side.SLAVE
        :rtype: Dapi2Side
        '''
        return DApi2Side.MASTER if self == DApi2Side.SLAVE else  DApi2Side.SLAVE
    
    
class DApi2ErrorLevel(DIntEnum):
    '''Error level'''
    
    OK = 0
    '''No error'''
    
    INFO = 1
    '''Just an information.'''  
    
    WARNING = 2
    '''A warning can be resolved without intervention.'''
    
    ERROR = 3
    '''An error is acknowledged by deactivating the workspace.'''
    
    FATAL = 4
    '''A fatal error requires restarting the board.'''
    
    @classmethod
    def levelOf(cls, error):
        '''Returns the error level according the error code.
        
        :param int error. The error number of which we want to know the level.
        
        :return: The error level.
        :rtype: DApi2ErrorLevel 
        '''
        if error == 0:
            return DApi2ErrorLevel.OK
        else:
            return DApi2ErrorLevel( (error >> 6)+1 )
    
    @property
    def label(self):
        '''The label of this error level.'''
        return self.name.title()

    @property
    def help(self):
        '''Help message according error level'''
        return {
            self.OK : 'No error.',
            self.INFO : 'Normal state, just an information. No action needed.',
            self.WARNING : 'Warning state. No action needed.',
            self.ERROR : 'Error state. The board must be placed in "standby" to clear the error.',
            self.FATAL : 'Fatal error state. The board must be shutdown to clear the error.',
            }[self]    


class DApiException(Exception):
    '''Base class for the exceptions of the DApi2 package.
    
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
            return '{1!s} - {2!s}\n{3!s}'.format(self.__class__.__name__, self.object.__class__.__name__, self.context, self.message)
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
        '''Returns the message explaining the exception.'''
        return self.args[2]    
    
    