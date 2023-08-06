'''

:author:  F. Voillat
:date: 2022-02-04 Creation
:copyright: Dassym SA 2021
'''

class DSignal(object):
    
    def __init__(self, name=None):
        self.name = name
        self._callbacks = []


    def isCOnnected(self, callback):
        return callback in self._callbacks
            
            
    def connect(self, callback):
        if not self.isCOnnected(callback):
            self._callbacks.append(callback)
        
    def disconnect(self, callback):
        try:
            self._callbacks.remove(callback)
        except ValueError:
            pass
        
    def emit(self, *args, **kwargs):
        for callback in self.callbacks:
            callback(*args, **kwargs)
    
    @property
    def callbacks(self):
        return self._callbacks
    
  

