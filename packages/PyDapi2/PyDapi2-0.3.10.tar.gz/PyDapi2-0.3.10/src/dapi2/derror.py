'''Module for DApi2 error. 

:author: F. Voilat
:date: 2021-03-05 Creation
'''
import lxml.etree as ET
from dapi2.common import DApi2ErrorLevel

class DApiComError(Exception):
    '''Base exception class for DAPI communication errors
    
    :param ErrorMessage errmsg: The error message.
        
    '''
    errorno = None
    name    = None
    label   = None
    text    = None
    
        
    @classmethod
    def getErrorClass(cls, errmsg):
        '''Find the class according to the error message.
        
        :param ErrorMessage errmsg: The error message.
        :return: The excepton class found
        '''
        return next(x for x in DApiComError.__subclasses__() if x.errorno[0] <= errmsg.getError() <= x.errorno[1]) 
    
    @classmethod
    def factory(cls, errmsg):
        '''Classmetoh to construct DApiComError according DAPI error code.
        
        :param ErrorMessage errmsg: The error message.
        :param \*exceptions: A list of specific exceptions.
        
        :return: The new exception according DAPI error.
        '''   
        
        assert 0 < errmsg.getError() < 0xc0 or errmsg.getError() >= 0xf0 
        errcls = DApiComError.getErrorClass(errmsg)
        return errcls(errmsg)

    
    def __init__(self, errmsg):
        super(Exception, self).__init__(errmsg)
        return
    
    def __str__(self):
        try:
            return '{0!s} - #0x1:02X} : {2!s}'.format(self.__class__.__name__, self.error, self.label)
        except:
            return Exception.__str__(self)    

    @property 
    def msg(self):
        '''The error message'''
        return self.args[0]
    
    @property
    def error(self):
        '''The error code'''
        return self.msg.getError()

    @property
    def addr(self):
        '''The message address'''
        return self.msg.getAddr()
    
            
    

class DApiComAddrError(DApiComError):
    errorno = (0x01,0x01)
    name    = 'DAPI_COM_WRONG_ADDR'
    label   = 'Wrong address'
    text    = 'Invalid address or command'

class DApiComReadonlyError(DApiComError):
    errorno = (0x02,0x02)
    name    = 'DAPI_COM_READ_ONLY'
    label   = 'Read only'
    text    = 'Try to write in a read only register' 

class DApiComValueError(DApiComError):
    errorno = (0x03,0x03)
    name    = 'DAPI_COM_WRONG_VALUE'
    label   = 'Wrong value'
    text    = 'No allowed value or wrong argument'

class DApiComContextError(DApiComError):
    errorno = (0x04,0x04)
    name    = 'DAPI_COM_WRONG_CONTEXT'
    label   = 'Wrong context'
    text    = 'This change or command is not allowed in this context'

class DApiComFormatError(DApiComError):
    errorno = (0x05,0x05)
    name    = 'DAPI_COM_MALFORMED_MSG'
    label   = 'Malformed message'
    text    = 'Malformed message'

class DApiComAccessError(DApiComError):
    errorno = (0x06,0x06)
    name    = 'DAPI_COM_ACCESS_DENIED'
    label   = 'Access denied'
    text    = 'Read/Write or command is not available with current access level'

class DApiComEepromError(DApiComError):
    errorno = (0x07,0x07)
    name    = 'DAPI_COM_EEPROM_FAILURE'
    label   = 'EEPROM failure'
    text    = 'EEPROM failure'
    

class DApiComAbortedError(DApiComError):
    errorno = (0xfd,0xfd)
    name    = 'DAPI_COM_ABORTED'
    label   = 'Aborted command'
    text    = 'Aborted command'

class DApiComComBrokenError(DApiComError):
    errorno = (0xfe,0xfe)
    name    = 'DAPI_COM_COM_BROKEN'
    label   = 'Borken Communication'
    text    = 'Communication is borken'
    
class DApiComUndefinedError(DApiComError):
    errorno = (0xff,0xff)
    name    = 'DAPI_COM_UDEFNED'
    label   = 'Undefined error'
    text    = 'Undefined error'


class DApiCommandError(DApiComError):
    '''Base exception class for DAPI commands errors
    
    :param ErrorMessage errmsg: The error message.
        
    '''    
    errorno = None
    name    = None
    label   = None
    text    = None    
    
    @classmethod
    def factory(cls, errmsg, *exceptions):
        '''Classmethod to construct DApiCommandError according DAPI error code.
        
        :param ErrorMessage errmsg: The error message.
        :param \*exceptions: A list of specific exceptions.
        
        :return: The new exception according DAPI error.
        :rtype: Child of DApiCommandError.
        '''   
        #assert 0 < errmsg.getError() < 0xc0, "errmsg.getError() => "+str(errmsg.getError()) 
        if errmsg.getError() < 0x80 or errmsg.getError() >= 0xFD:
            return DApiComError.factory(errmsg)
        else:
            for e in exceptions:
                if e.errorno[0] <= errmsg.getError() <= e.errorno[1]:
                    return e(errmsg)
        return DApiCommandError(errmsg)        
    
    
class DApiBoardWarningError(Exception):
    '''Base exception class for DAPI board warnings and errors
    
    :param int num: Warning/Error number
    :param str name: Warning/Error name
    :param DApiBardErrorLevel level: Warning/Error level
    :param str default_description: Default description
    '''

    @classmethod
    def loadXML(cls, xerror):
        s = xerror.get('id')
        if s[:2].lower() == '0x':
            num = int(s[2:],16)
        else:
            num = int(s,10)
        try:
            name = xerror.find('name').text
        except:
            raise Exception('The <name> element is missing in {0!s}!'.format(ET.tostring(xerror, pretty_print=True)))
        descr_list = xerror.findall('descr')
        if len(descr_list)==0:
            raise Exception('The <descr> element is missing in {0!s}!'.format(ET.tostring(xerror, pretty_print=True)))
        obj = DApiBoardWarningError(
            num=num,
            name=name,
            level = DApi2ErrorLevel[xerror.get('level')],  
            default_description = descr_list[0].text
            )
        
        for xdescr in descr_list:
            lang = xdescr.get('lang', None)
            obj._descr[lang] = xdescr.text
        
        return obj
    
    def __init__(self, num, name, level, default_description):
        super().__init__()
        self.args =[ num, name, level ]
        self._descr = {None:default_description}
    
    def __str__(self, lang=None):
        try:
            return '{0:s} #0x{1:02X} : {2!s}'.format(self.level.label, self.num, self.getDescription(lang))
        except:
            return Exception.__str__(self)    

    def getDescription(self, lang=None):
        try:
            return self._descr[lang]
        except KeyError:
            return self._descr[None]
        
    @property
    def num(self):
        return self.args[0]
    @property
    def name(self):
        return self.args[1]
    @property
    def level(self):
        return self.args[2]
    @property
    def descriptions(self):
        return self._descr    
    

class DErrorsContainer(object):
    '''Conatainer to store DAPI2 board errors and warnings.
    
    
    :param object owner: Owner of this container 
    '''


    def __init__(self, owner, errorsfile=None):
        '''
        Constructor
        '''
        super().__init__()
        self._owner = owner
        self._items = []
        self._errors = {}
        self._names = {}
        if errorsfile is not None:
            self.loadFromFile(errorsfile)
        
        
    def __getitem__(self, addr):
        return self._items[addr]
     
    def __len__(self):
        return len(self._items)  
    
    def __iter__(self):
        for item in self._items:
            yield item 
            
    def __call__(self, arg):
        if isinstance(arg, str): 
            return self._items[self._names[arg]]
        else:
            return self._items[self._errors[arg]]
        
    def __getattr__(self, name):
        return self._items[self._names[name]]
            
    def clear(self):
        self._items = []
        self._errors = {}
        self._names = {}
            
    def add(self, *errors):
        '''Adds errors into this container.
        
        :param DApiBoardWarningError errors: one or more error that should be added to the container
        '''            
        for error in errors:
            assert isinstance(error, DApiBoardWarningError)
            self._items.append(error)
            self._names[error.name] = self._errors[error.num] = len(self._items)-1 
        
        
    def loadFromFile(self, fname):
        if len(self._items)>0:
            self.clear()
        #TODO: select file reader regarding the format of file `filename`
        self.loadXML(ET.parse(fname))
        
    def loadXML(self, xtree):
        
        xroot = xtree.getroot()
        for xerror in xroot.findall('error'):
            error = DApiBoardWarningError.loadXML(xerror)
            self.add(error)
            
        
