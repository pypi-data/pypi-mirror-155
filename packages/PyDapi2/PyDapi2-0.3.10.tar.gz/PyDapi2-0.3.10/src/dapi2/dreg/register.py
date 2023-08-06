'''
Created on 8 févr. 2021

@author: fv
'''

from .base import BaseRegElement, DRegException, DRegAccess, DRegChangedSignal
from .. import dreg
from ..common import REG_MAX_VALUE  
 

class DRegUndefinedError(DRegException):
    pass

class Register(BaseRegElement):
    '''Class for registers group in DAPI2 registers structure.
    
    :param parent: Registers parent element.
    :type parent: Regsisters
    
    :param name: Group name
    :type name: str

    :param addr: Group base address in registers array.
    :type addr: int

    :param size: Group size, number of registers slot in group (optional).
    :type size: int

    :param dict descriptions: Multilingual Element description (otional). 
           The dictionary key is language code {fr,de,it,...} or None for the default language, by convention the English. 

    :param shortname: Group short name (otional).
    :type shortname: str

    :param access: Register access mode (default:DRegAccess.READ).
    :type access: DRegAccess
    '''
    
    
    def __init__(self, name, parent=None, addr=None, size=1, descriptions=None, shortname=None, min=0, max=REG_MAX_VALUE, access=dreg.DRegAccess.READ): #@ReservedAssignment
        assert parent is None or isinstance(parent, (dreg.RegContainer, dreg.RegGroup, dreg.RegisterArray )), 'parent is '+type(parent).__name__
        super().__init__(name, parent, addr, size, descriptions, shortname)
        self._access = access
        self.min = min
        self.max = max 
        self._modified = False
        self._undefined = True
        self._changed = DRegChangedSignal(self)
        
        
    def _stringData(self, lang=None):
        try:
            return '0x{3:04x}({3:d}) ; addr:{0:02X} ×{1:d} {2!s} '.format(
                    self.addr, 
                    self.size, 
                    'R-' if self.readonly else 'RW',
                    self.value) 
        except Exception as e:
            return  "!!Register:" + str(e)+ "!!"
        
    def _valueChanged(self, old):
        if self.container.eventsEnabled:
            self.changed.emit(old)
        
    def isModified(self):
        return self._modified
    
    def isUndefined(self):
        return self._undefined

    def isDefined(self):
        return not self._undefined

    
    def asString(self):
        return chr(self.value // 256) + chr( self.value & 0xff )  
    
    def alter(self, value):
        return self.set(value)
    
    def internalSet(self, value, modified=False):
        old = self.container.values[self.addr]
        self._modified = modified and old != value 
        if self._undefined or old != value:
            self.container.values[self.addr] = value
            self._valueChanged(old)
        self._undefined = False
        return value
            
    def set(self, value):
        return self.internalSet(value, True)
    
    def setMin(self):
        return self.set(self.min)

    def setMax(self):
        return self.set(self.max)
    
    def clear(self):
        return self.set(0)
    
    def get(self):
        if self._undefined:
            raise DRegUndefinedError(self, 'get', 'Undefined value in register '+self.name)
        return self.container.values[self.addr]      
    
    @property
    def access(self):
        '''The register access mode'''
        return self._access
    
    @property
    def changed(self):
        return self._changed
        
class ReservedRegister(Register):
    
    pass

class RegisterBits(object):
    
    def __init__(self, parent):
        self._parent = parent
        self._bits = []
        self._index = {}
        
    def __getattr__(self, name):
        return self.getBit(name)

    def __call__(self, name):
        return self.getBit(name)

    def __getitem__(self, index):
        return self._bits[index]
    
    def __len__(self):
        return len(self._bits)
    
    def __iter__(self):
        for bit in self._bits:
            yield bit         

        
    def _getNextFreeAddr(self):
        if len(self._bits)==0:
            return 0
        else:
            return self._bits[-1].addr + self._bits[-1].size

    def add(self, *bits):
        '''Adds bits to this bits field register
        
        :param bit: One or more bits to be added to the bits field register
        :type bit: RegBit
        
        :return: The next address (position) after the last added bit
        :rtype: int
        '''
        for bit in bits:
            if bit.addr is None:
                bit.setAddress(self._getNextFreeAddr())
            self._bits.append(bit)
            self._index[bit.name] = bit
            
            self._bits.sort(key=lambda x: x.addr)
        return bit.addr+bit.size

    
    def getBit(self, name):
        '''Returns the bit  according to its name.
        
        :param str name: the bit name to return
        
        :return: The bit found
        :rtype: RegBit
        '''
        return self._index[name]

        
class BitFieldRegister(Register):
    
    def __init__(self, name, parent=None, addr=None, size=1, descriptions=None, shortname=None, access=DRegAccess.READ):
        super().__init__(name, parent, addr, size, descriptions, shortname, access)
        self._bits = RegisterBits(self)
        
    def __len__(self):
        return len(self._bits)
    
    def __iter__(self):
        for bit in self._bits:
            yield bit         
        
    def _stringData(self, lang=None):
        try:
            return super()._stringData() + " ; count:{}".format(len(self)) 
        except Exception as e:
            return  "!!BitFieldRegister:" + str(e)+ "!!"     
        
    def getBit(self, name):
        '''Returns the bit  according to its name.
        
        :param str name: the bit name to return
        
        :return: The bit found
        :rtype: RegBit
        '''
        return self._bits.getBit(name)
        
        
    def toStringChildren(self, indent=1, prefix='', end='', depth=0, lang=None):
        '''Returns a pretty listing of registers (children) of this group.
        
        :param indent: Indentation level (optional, default: 1)
        :type indent: int
        
        :param prefix: Prefix for the child's name (optional, default: null string)
        :type prefix: str
        
        :param end: String applied on the end of child's representation (optional, default: null string)
        :type end: str
        
        :param depth: The depth of exploration of children and grandchildren (optional, default: 0 = no exploration)
        :type depth: int
        
        :return: A string with the listing of groups and registers.
        :rtype: str
        '''        
        if len(self._bits)>=10:
            idx_fmt = '{0:02d} ‒ '
        else:
            idx_fmt = '{0:d} ‒ '
        return prefix + '\n'.join( [x.toString(indent,idx_fmt.format(i),depth=depth-1, lang=lang) for (i,x) in enumerate(self._bits)]  ) + end      
                   

    def add(self, *bits):
        '''Adds bits to this bits field register
        
        :param bit: One or more bits to be added to the bits field register
        :type bit: RegBit
        
        :return: The next address (position) after the last added bit
        :rtype: int
        '''
        return self._bits.add(*bits)
    
    
    @property
    def bits(self):
        return self._bits 
        
class RegisterArray(Register):
    def __init__(self, name, parent=None, addr=None, size=1, descriptions=None, shortname=None, access=dreg.DRegAccess.READ):
        super().__init__(name, parent, addr, size, descriptions, shortname, access)
        self._regs = []
        
        for i in range(self.size):
            reg = Register(self.name+str(i), self, self.addr+i, size=1, shortname=self.shortname+str(i), access=access)
            self._regs.append(reg)

    def __getitem__(self, index):
        return self._regs[index]
    
    def __len__(self):
        return len(self._regs)
    
    def __iter__(self):
        for dreg in self._regs:
            yield dreg     
            
    def isUndefined(self):
        for r in self:
            if r.isUndefined():
                return True
        return False
    
    def _stringData(self, lang=None):
        try:
            s = '['+','.join( '0x{0:04x}({0:d})'.format(r.value) for r in self)+"]"
            return s + ' ; addr:{0:02X} ×{1:d} {2!s} '.format(
                    self.addr, 
                    self.size, 
                    'R-' if self.readonly else 'RW') 
        except Exception as e:
            return  "!!RegisterArray:" + str(e)+ "!!"    
    
    def setAddr(self, value):
        Register.setAddr(self, value)
        for i, r in enumerate(self):
            r.setAddr(self.addr+i)
    
    def alter(self, values):
        return self.set(values)
        
    def set(self, values):
        for i, v in enumerate(values):
            self._regs[i].set(v)
        self._undefined = False
        
    def internalSet(self, values, modified=False):
        self._modified = modified
        for i, v in enumerate(values):
            self._regs[i].internalSet(v, modified)
        self._undefined = False
        
    def get(self):
        return list([ self._regs[i].get() for i in range(self.size) ])

class RegBitChoice():
    def __init__(self, name, value, bit=None, descriptions=None, shortname=None ):
        self._bit = bit
        self.value = value
        self.name = name
        if isinstance(descriptions, dict): 
            self._descriptions = descriptions
        else:
            self._descriptions = {None:descriptions}   
        if shortname is None:
            self.shortname = name[:3]
        else:
            self.shortname = shortname
            
    def __str__(self):
        return '{0:d}:{1:s}'.format(self.value,self.name)
            
    def __lt__(self, other):
        return self.value < other.value
    
    def __eq__(self, other):
        return self.value == other.value    
    
    def getDescription(self, lang=None):
        try:
            return self._descriptions[lang]
        except KeyError:
            return self._descriptions[None]     
        
    @property
    def descriptions(self):
        return self._descriptions
    
    @property
    def descr(self):
        return self.getDescription()          


class RegBit(BaseRegElement):
    def __init__(self, name, parent=None, addr=None, size=1, descriptions=None, shortname=None, choices={}):
        super().__init__(name, parent, addr, size, descriptions, shortname)
        self.choices = choices
        if shortname is None:
            self.shortname = name[:3]
        else:
            self.shortname = shortname
        self._mask = ((1<<self._size)-1) << self._addr
        
#     def __str__(self):
#         try:
#             return '{p:2d}-{n:s}:{v!s}'.format(n=self.name, p=self.pos, v=self.choices[self.value])
#         except KeyError:
#             return ('{1:2d}-{0}:{2:0'+str(self._size)+'b} (0x{2:x})').format(self.name, self.pos, self.value)

    
    def __lt__(self, other):
        return self.name < other.name
    
    def __eq__(self, other):
        return self.name == other.name
    
    def _stringData(self, lang=None):
        return "{0:d}".format(self.get())
    
    def internalSet(self, value, modified=False):
        assert value >= 0 and value < (1<<self._size), 'RegBit.internalSet:{} is an invalid value for the flag {}.{}'.format(value,self._owner.reg.name,self.name)
        return self._parent.internalSet((self._parent.value & ~self._mask) | (value << self.addr), modified)
    
    def alter(self, value):
        return self.set(value)
        
    def set(self, value=1):
        assert value >= 0 and value < (1<<self._size), 'RegBit.set:{} is an invalid value for the flag {}.{}'.format(value,self._owner.reg.name,self.name)
        return self._parent.set((self._parent.value & ~self._mask) | (value << self.addr) )
    
    def toggle(self):
        return self._parent.set(self._parent.value ^ self._mask)
        
    def clear(self):
        return self.set(0)
        
    def get(self):
        return (self._parent.value & self._mask) >> self.addr
    
    def strValue(self):
        return '{v!s}'.format(v=self.choices[self.value])
    
    @property
    def mask(self):
        return self._mask  
    
class ReservedRegBit(RegBit):
    pass

    
        