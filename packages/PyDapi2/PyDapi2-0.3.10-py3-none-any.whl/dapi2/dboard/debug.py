'''

:author:  F. Voillat
:date: 2021-09-13 Creation
:copyright: Dassym SA 2021
'''
from .common import BaseBoardItem



class DebugValue(BaseBoardItem):
    
    def __init__(self, board, index, size=16):
        BaseBoardItem.__init__(self, board, name='Debug #{0:d}'.format(index))
        self._index = index
        self._size = size
        self.values = []
        self._callback_list = []
        self.board.regs.dmr[index].changed.connect(self.onRegisterChange)
        if self.board.regs.dmr[index].isDefined():
            self.onRegisterChange(self.board.regs.dmr[index], self.board.regs.dmr[index].value, self.board.regs.dmr[index].value )
    
    def __getitem__(self, index):
        return self.values[index]
    
    def __len__(self):
        return len(self.values)
    
    def setSize(self, size):
        self._size = size
        if self._size < len(self):
            self.values = self.values[:self._size]
   
    def connect(self, callback):
        if all(x != callback for x in self._callback_list):
            self._callback_list.append(callback)            

    def disconnect(self, callback):
        self._callback_list.remove(callback) 

    def onRegisterChange(self, reg, old_value=None, new_value=None):
        self.board.log.debug('DebugValue.onRegisterChange')
        if new_value is None:
            new_value = reg.value
        self.values = ([new_value]+self.values)[:self._size]
        
        for func in self._callback_list:
            func(self)      

    @property
    def value(self):
        try:
            return self.values[0]
        except IndexError:
            return None
        
    @property
    def index(self):
        return self._index