'''
Created on 15 mars 2021

@author: fv
'''
from .common import BaseBoardItem


        
class Memory(object):
    '''Memory for recording setpoints
    
    :param container 
    :param index int: memory index number
    :param size int: size of memory. Number of registers to store.
    '''
    
    SIZE = 16
    PAGE_SIZE = 4
    NB_PAGES = SIZE // PAGE_SIZE
    SMR_MASK = 0x0500 # In the "SMR" register, only bits #8 (reverse) and #10 (light) are relevant
    
    def __init__(self, container, index):
        self._container = container
        self._index = index
        self._values = []
        
    def read(self):
        self._values = []
        for p in range(self.SIZE // self.PAGE_SIZE): 
            self._values.extend(self.board.dapi.cmd.memoryRead(self.workspace.number, self._index, p))
        
            
    def isCurrent(self):
        if self._values[0] & self.SMR_MASK != self.board.regs.setpoints.values[0] & self.SMR_MASK:
            return False  
        return self._values[1:] == self.board.regs.setpoints.values[1:]
        
    def isDefined(self):
        return len(self._values)==self.SIZE 
    
    @property
    def board(self):
        return self._container.board
    
    @property
    def workspace(self):
        return self._container.workspace
    
    @property
    def index(self):
        return self._index

    

class Memories(object):
    '''Container to maintain the set points memories.
    
    :param workspace BaseWorkspace: the container's proprietary workspace
    ''' 
    def __init__(self, workspace):
        self._workspace = workspace
        self._slots = []
        for i in range(self._workspace.NB_USER_MEMORY_SLOTS):
            self._slots.append(Memory(self, i))
            
    def __getitem__(self, index):
        return self._slots[index]
    
    def __len__(self):
        return len(self._slots)
    
    def __iter__(self):
        for mem in self._slots:
            yield mem

    def readAll(self):
        for m in self:
            if not m.isDefined():
                m.read()

    @property
    def board(self):
        return self._workspace.board

    @property
    def workspace(self):
        return self._workspace
        

class BaseWorkspace(BaseBoardItem):
    '''Base class for board's Workspace.
    
    :param BaseBoard board: The board.
    :param str name: The workspace name.
    :param int number: The workspace number = PAR value used to activate the workspace
    :param int pcr: The configuartion code  
    
    .. inheritance-diagram:: BaseWorkspace
        :parts: 1
    
    
    '''
        
    NB_USER_MEMORY_SLOTS = 8
    '''Number of user's memory slots.'''
    
    def __init__(self, board, name=None, number=None, pcr=None):
        super().__init__(board, name)
        self._number = number
        self._pcr = pcr
        self._memories = Memories(self)        

    def __str__(self):
        return self.name
    
    def isFunctional(self):
        '''Check if workspace is functional.
        
        :return: True, if workspace is functional ; False otherwise.
        :rtype bool
        '''
        if self.board.regs.ctr.isUndefined():
            self.board.getRegisters('ctr')
        return self.board.regs.ctr.value != 0x0000       

    @property
    def standby(self):
        return False
    @property
    def active(self):
        return self is self._board.getWorkspace()      
    @property
    def number(self):
        return self._number
    @property
    def par(self):
        return self._number
    @property
    def pcr(self):
        return self._pcr
    @property
    def memories(self):
        return self._memories

class Workspace(BaseWorkspace):
    '''Class for a functional Workspace.
    
    :param BaseBoard board: The board. 
    :param str name: The workspace name.
    :param int par: The workspace number = PAR value used to activate the workspace
    :param int pcr: The configuartion code   
    
    
    .. inheritance-diagram:: Workspace
        :parts: 1

    '''
    
    def __init__(self, board, name=None, number=None, pcr=None):
        super().__init__(board, name, number, pcr)
        self.log.debug('PAR={0:d}, PCR={1:04x}'.format(number, pcr.value))
        self.cfg = [0]*4

        

            
        #TODO: for i in range(board.wcaCount): 
            # self.wca.append( MemoryWC(i, self.wca)  )
            #self.eeprom.wca_list.append(self.wca)        
            
            
        

    
#     def set_captor_mode(self, mode):
#         self._pcr['CAPTOR'].set(mode.value)
        #
    # def get_captor_mode(self):
        # return dboard.Sensors(self._pcr['CAPTOR'].value)
        #
#     def set_reference_mode(self, mode):
#         self._pcr['REFERENCE'].set(mode.value)
        
    # def get_reference_mode(self):
        # return dboard.SpeedRequestMode(self._pcr['REFERENCE'].value)
    
    def get_temp_running(self):
        return self._pcr['TMP_RUN'].value
    def get_temp_idle(self):
        return self._pcr['TMP_IDLE'].value
        

    @property
    def ppa(self):
        return self._pcr.value & 0x000f
     
    @property
    def rdt(self):
        return (self._pcr.value & 0x0f00) >> 8
    
    @property
    def idt(self):
        return (self._pcr.value & 0xf000) >> 12
    
    @property
    def description(self):
        return 'Workspace #{par:d}\nIdle temperature multiplicator: {idt:d}\nRun temperature multiplicator: {rdt:d}'.format(par=self.par,idt=self.idt, rdt=self.rdt)

    
         
class StandbyWorkspace(BaseWorkspace):
    '''Class for the *standby* workspace
    
    :param BaseBoard board: The board. 
    
    .. inheritance-diagram:: StandbyWorkspace
        :parts: 1
    
    '''        
     
    def __init__(self, board):
        super().__init__(board, 'Standby', 0, None)
        self.log.debug('Construct')

    def isFunctional(self):
        '''Alwayse return False. This workspace is never functional.'''
        return False
     
    @property
    def standby(self):
        return True
    @property
    def description(self):
        return 'Standby'    
    
class WorkspacesContainer(BaseBoardItem):
    '''Container class for workspaces of board
    
    .. inheritance-diagram:: WorkspacesContainer
        :parts: 1
    
    '''
    def __init__(self, board, name=None):
        super().__init__(board, name)
        self._items = []
        
    def __getitem__(self, index):
        self._items[index]
    
    def __setitem__(self, index, value):
        self._items[index] = value
    
    def __len__(self):
        return len(self._items)
    
    def __iter__(self):
        return iter(self._items)
    
    def getByPAR(self, par):
        for w in self._items:
            if w.par == par:
                return w
    
    def clear(self):
        self._items.clear()
    
    def append(self, item):
        self._items.append(item)
        
    @property
    def count(self):
        return len(self._items)

        