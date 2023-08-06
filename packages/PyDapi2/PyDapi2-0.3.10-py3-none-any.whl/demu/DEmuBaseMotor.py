'''
Created on 31 mars 2021

@author: tm
'''

class DEmuBaseMotor(object):
    '''
    classdocs
    '''
    def __init__(self, ppa="3x"):      
        self.speed = 0
        self.torque = 0
        self.ppa = ppa
                
    def start(self):
        pass
    
    def stop(self):
        pass
    
    def speed(self, value):
        pass
    
    def torque(self, value):
        pass