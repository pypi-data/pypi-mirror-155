'''
Created on 6 févr. 2021

@author: fv
'''

from .base import BaseRegElement
from ..  import dreg 
from dapi2.dreg.register import ReservedRegister

class RegContainer(BaseRegElement):
    '''Class representing the registers of the electronic card according to the DAPI2 protocol.
    
    
    :param owner: 
    :type owner: object
    '''


    def __init__(self, owner, size=0, groups=[]):
        '''
        Constructor
        '''
        super().__init__('registers', parent=None, addr=0, size=size)
        self._owner = owner
        self._values = [0] * self.size
        self._regs = [ReservedRegister('reserved')] * self.size
        self._groups = {}
        self._arrays = {}
        self._index = {}
        self._disable_events_cnt = 0
        
        for group in groups:
            group.setParent(self)
            self.add(group)

    def __call__(self, *name):
        if len(name) == 1:
            return self.__getattr__(name[0])
        elif len(name) > 1:
            return list(self.__getattr__(n) for n in name) 
        else:
            return None
        
    def __getitem__(self, addr):
        return self._regs[addr]
     
    def __len__(self):
        return len(self._regs)  
    
    def __iter__(self):
        for reg in self._regs:
            yield reg 
            
    def __getattr__(self, name):
        try:
            return self.getRegister(name)
        except (KeyError, IndexError):
            try:
                return self._groups[name]
            except KeyError:
                return self._arrays[name]
            
    def _stringData(self):
        try:
            return 'size:{0:d}'.format(self.size) 
        except Exception as e:
            return  "!!Container:" + str(e)+ "!!"
        
    def toStringChildren(self, indent=1, prefix='', end='', depth=0):
        '''Returns a pretty listing of groups and registers (children) of this container.
        
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
        if len(self._groups)>0:
            children = self._groups.values()
        else:
            children = self._regs
        if len(children)>=100:
            idx_fmt = '{0:03d} ‒ '
        elif len(children)>=10:
            idx_fmt = '{0:02d} ‒ '
        else:
            idx_fmt = '{0:d} ‒ '
        return prefix + '\n'.join( [x.toString(indent,idx_fmt.format(i),depth=depth-1) for (i,x) in enumerate(children)]  ) + end
    
    def clear(self):
        '''Clear registers.'''
        
        self._size = 0
        self._values.clear()
        self._regs.clear()
        self._groups.clear()
        
    def reset(self):
        self._values = [0] * self.size
        
    def add(self, *elements):
        '''Adds elements into this container.
        
        :param elements: one or more element that should be added to the container
        :type elements: BaseRegElement
        
        :return: The next address to the last added element.
        :rtype: int
        '''
        for element in elements:
            assert isinstance(element, BaseRegElement), 'element is '+str(type(element))
            element.setParent(self)
            if element.addr is None:
                element.setAddr(self.size)
            next_addr = element.addr+element.size
            if next_addr > self._size:
                self.setSize(next_addr)
            
            if isinstance(element, dreg.RegGroup):
                self._groups[element.name] = element
            elif isinstance(element, dreg.RegisterArray):
                self._arrays[element.name] = element
                for r in element:
                    self._regs[r.addr] = r
                    self._index[r.name] = r.addr
            elif isinstance(element, dreg.Register):
                self._regs[element.addr] = element
                self._index[element.name] = element.addr
            else:
                raise TypeError('An object of class {0!s} cannot be added to the container.'.format(type(element).__name__))
        return next_addr
        
    def setSize(self, value):
        '''Set the new size of the container.
        
        :param value: The new size.
        :type value: int
        
        The size can only increase.
        '''
        if value < self.size:
            raise ValueError('Size can only increased!')
        elif value != self.size:
            self._values.extend([0]*(value-self.size))
            self._regs.extend([ReservedRegister('reserved')]*(value-self.size))
            super().setSize(value)
            
    def getRegister(self, reg):
        '''Returns a register according to its name or address.
        
        :param reg: the name or address of the register to return
        
        :return: The register found
        :rtype: Register
        '''
        if isinstance(reg, int):
            return self[reg]
        else:
            return self._regs[self._index[reg]]
        
    def getBit(self, name):
        '''Returns the register's bit according to its name.
        
        :param str name: The bit name (reg.bit)
        
        :return: The register's bit found
        :rtype: RegBit
        '''
        rname, bname = name.split('.')
        reg = self(rname)
        return  reg(bname) 
            
            
    
    def modifiedRegs(self):
        return (r for r in self.regs if r.isModified())
    
    def disableEvents(self):
        self._disable_events_cnt += 1
        return self._disable_events_cnt
    
    def eventsEnabled(self):
        if self._disable_events_cnt > 0:
            self._disable_events_cnt -= 1
        return self._disable_events_cnt
    
    
        
    @property
    def container(self):
        return self
    
    @property
    def owner(self):
        return self._owner
        
    @property
    def groups(self):
        return self._groups
        
    @property
    def regs(self):
        return self._regs
        
        
    @property
    def values(self):
        return self._values
        


        
        