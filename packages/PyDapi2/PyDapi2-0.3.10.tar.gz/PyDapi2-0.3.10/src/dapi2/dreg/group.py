'''Module for the class of group element

:author: F. Voillat
:date: 2021-02-17 Creation
'''
from .. import dreg
        
class RegGroup(dreg.BaseRegElement):
    '''Class for registers group in DAPI2 registers structure.
    
    :param parent: Registers parent element.
    :type parent: Regsisters
    
    :param name: Group name
    :type name: str

    :param addr: Group base address in registers array.
    :type addr: int

    :param size: Group size, number of registers slot in group (optional).
    :type size: int

    :param descr: Group  description (otional).
    :type descr: str

    :param shortname: Group short name (otional).
    :type shortname: str

    :param access: Group access mode (otional, default:DRegAccess.READ).
    :type readonly: DRegAccess
    '''
    
    
    def __init__(self, name, parent=None, addr=None, size=0, descriptions=None, shortname=None, access=dreg.DRegAccess.READ, regs=[]):
        assert parent is None or isinstance(parent, dreg.RegContainer), 'parent is '+type(parent).__name__
        super().__init__(name, parent=parent, addr=addr, size=size, descriptions=descriptions, shortname=shortname)
        self._access = access  
        self._regs = []
        
        for reg in regs:
            reg.setParent(self)
            self.add(reg)

    def __getitem__(self, index):
        return self._regs[index]
    
    def __len__(self):
        return len(self._regs)
    
    def __iter__(self):
        for dreg in self._regs:
            yield dreg 
    
    def _stringData(self):
        try:
            return 'addr:{0:02X} size:{1:d} {2!s}'.format(self.addr, self.size, 'readonly' if self.readonly else '') 
        except Exception as e:
            return  "!!Group:" + str(e)+ "!!"   
        
    def toStringChildren(self, indent=1, prefix='', end='', depth=0):
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
        if len(self._regs)>=100:
            idx_fmt = '{0:03d} ‒ '
        elif len(self._regs)>=10:
            idx_fmt = '{0:02d} ‒ '
        else:
            idx_fmt = '{0:d} ‒ '
        return prefix + '\n'.join( [x.toString(indent,idx_fmt.format(i),depth=depth-1) for (i,x) in enumerate(self.regs)]  ) + end      
   
        
    def add(self, *elements):
        '''Adds an elements to this group
        
        :param elements: One or more elements to be added to the group
        :type elements: BaseRegElement
        
        :return: The next address after the last added element
        :rtype: int
        '''
        for element in elements:
            if isinstance(element, (dreg.Register, dreg.RegisterArray, )):
                self._regs.append(element)
                if element.addr is None:
                    element.setAddr(self.size)
                if self.container:
                    self.container.add(element)
            else:
                raise TypeError('An object of class {0!s} cannot be added to the container.'.format(type(element).__name__))
            next_addr = element.addr+element.size
            if next_addr > self.addr + self._size:
                self.setSize(next_addr-self.addr)
        return next_addr
    
    @property
    def values(self):
        return self.container.values[self.addr:self.addr+self.size]
    
    @property        
    def regs(self):
        '''The list of registers of the group.'''
        return self._regs
    
    @property
    def access(self):
        '''The group access mode'''
        return self._access
    