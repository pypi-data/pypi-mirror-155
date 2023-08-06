'''Module for the base class of register structure elements

:author: F. Voillat
:date: 2021-01-17 Creation
'''

from enum import IntEnum

from ..common import DApiException
from ..signal import DSignal

class DRegException(DApiException):
    '''Base class for register's module exceptions.'''
    pass


class DRegAccess(IntEnum):
    '''Enumeration of register access mode'''
    
    NO    = 0
    READ  = 1
    WRITE = 2
    RW    = 3
    
class DRegChangedSignal(DSignal):
    
    def __init__(self, reg):
        self._reg = reg
        super().__init__(name='changed')
        
        
    def emit(self, old):
        for callback in self.callbacks:
            callback(self._reg, old, self._reg.value)

class BaseRegElement(object):
    '''Base class for registers structure elements.
    
    :param BaseRegElement parent: Parent element.
    
    :param str name: Element name
    
    :param int addr: Element address in registers array.

    :param int size: Element size, number of registers slot in group (optional, default: 1).

    :param dict descriptions: Multilingual Element description (otional). 
           The dictionary key is language code {fr,de,it,...} or None for the default language, by convention the English. 
    
    :param str shortname: Element short name (otional).
    '''
    
    def __init__(self, name, parent=None, addr=None, size=1, descriptions=None, shortname=None):
        '''Initialize'''
#         self.log = logging.getLogger('{0!s}:{1!s}'.format(self.__class__.__name__, name))
#         self.log.debug('Initialize')
        self._parent = parent
        self._addr = addr
        self._size = size
        if name is None:
            raise ValueError('The `name` argument must be defined.') 
        self.name = name
        self.shortname = shortname or name[:4]
        if isinstance(descriptions, dict): 
            self._descriptions = descriptions
        else:
            self._descriptions = {None:descriptions}        

    def __str__(self, lang=None):
        try:
            return '{0:s} {1:!s} (size:{2:d})'.format(self.name, self._stringData(lang=lang))
        except:
            return self.name
        
    def __lt__(self, other):
        return self.addr < other.addr
        
    def _stringData(self, lang=None):
        try:
            return '@{0:02x} (size:{1:d})'.format(self.addr, self.size) 
        except Exception as e:
            return  "!!Base:" + str(e)+ "!!"
        
        
    def add(self, element):
        assert False, 'Abstract method!'
        
    def getNext(self):
        try:
            return self.container[self.addr+1]
        except KeyError:
            return None
        
    def toStringChildren(self, indent=0, prefix='', end='', depth=0, lang=None):
        '''Returns a pretty listing of groups and registers (children) of this container.
        
        :param indent: Indentation level (optional, default: 1)
        :type indent: int
        
        :param prefix: Prefix for the child's name (optional, default: null string)
        :type prefix: str
        
        :param end: String applied on the end of child's representation (optional, default: null string)
        :type end: str
        
        :param depth: The exploration deep of children and grand-children (optional, default: 0 = no exploration)
        :type depth: int
        
        :return: A string with the listing of groups and registers.
        :rtype: str
        '''
        return ''
    
    def toString(self, indent=0, prefix='', end='', depth=0, lang=None):
        '''Returns a pretty representation of this object.
        
        :param indent: Indentation level (optional, default: 1)
        :type indent: int
        
        :param prefix: Prefix for the object's name (optional, default: null string)
        :type prefix: str
        
        :param end: String applied on the end representation (optional, default: null string)
        :type end: str
        
        :param depth: The depth of exploration of children and grandchildren (optional, default: 0 = no exploration)
        :type depth: int
        
        :return: A string with the listing of groups and registers.
        :rtype: str
        '''
        try:
            sChildren = ''
            sData = self._stringData(lang=lang)
            if sData != '':
                sData = " : " + str(sData)
            if depth > 0:
                sChildren = self.toStringChildren(indent+1, depth=depth-1, lang=lang)
            if sChildren != '':
                sChildren = '\n'+str(sChildren)
            return '\t' * indent + str(prefix) + self.__class__.__name__ +":"+ str(self.name) + sData + sChildren + end
        except Exception as e:
            return '\t' * indent + prefix + "!!Base:" + str(e)+ "!!" + str(self) + end
        
        
    def setParent(self, parent):
        self._parent = parent
        
    def set(self, value):
        self.container.values[self.addr] = value
        
    def get(self):
        return self.container.values[self.addr]        
    
    def getDescription(self, lang=None):
        try:
            return self._descriptions[lang]
        except KeyError:
            try:
                return self._descriptions[None]
            except KeyError:
                return None    
        
    @property
    def descriptions(self):
        return self._descriptions
    
    @property
    def descr(self):
        return self.getDescription()
    
    @property
    def parent(self):
        '''Parent (:class:`BaseRegElement`) of this element.'''
        return self._parent  
    
    @property
    def container(self):
        '''Container (:class:`~dapi2.reg.Registers`) of element.''' 
        if self.parent:
            return self.parent.container
        else:
            return None
  
    @property
    def addr(self):
        '''Element address (int) of this element in the DAPI2 registers structure.'''
        return self._addr

    @addr.setter
    def addr(self, value):
        self.setAddr(value)
        
    def setAddr(self, value):
        '''Set address of element.
        
        :param value: The new address of element.
        :type value: int
        '''
        self._addr = int(value)
        
    @property
    def size(self):
        '''Element size (int) of this element (number of registers).
        '''
        return self._size
    
    @size.setter 
    def size(self, value):
        self.setSize(value)
        
    def setSize(self, value):
        '''Set size (number of registers) of element.
        
        :param value: The new size of element.
        :type value: int
        '''
        self._size = int(value)
        
    
    @property
    def value(self):
        return self.get()
         
    @value.setter
    def value(self, value):
        self.set(value)
        

        