'''
Created on 31 mars 2021

@author: tm
'''

class DEmuPPA(object):
    @staticmethod
    def ppa_3x(regs):
        regs[0x02].set(2000, True)# speed constant
        regs[0x03].set(2000, True)# velocity constant
        regs[0x04].set(1000, True)# minimum motor speed
        regs[0x05].set(500, True)# minimum motor current
        regs[0x06].set(40000, True)# maximum motor speed
        regs[0x07].set(7000, True)# Maximum motor current
        regs[0x08].set(150, True)# Maximum motor acceleration
        regs[0x09].set(360, True)# maximum light current
        regs[0x0a].set(6000, True)# EKF low sensivity
        regs[0x0b].set(3000, True)# EMF hight sensivity
        regs[0x0c].set(500, True)# EMF Sensivity histerisys
        regs[0x0d].set(300, True)# Rotation acknoledge
        regs[0x0e].set(10, True)# Startup trials
        regs[0x0f].set(0, True)
        regs[0x10].set(0, True)
        regs[0x11].set(0, True)
        regs[0x12].set(38, True)# Temperature decay factor
        regs[0x13].set(580, True)# Temperature increase factor
        regs[0x14].set(0, True)
        regs[0x15].set(0, True)
        regs[0x16].set(1000, True)# Initial phase shift
        regs[0x17].set(20, True)# Phase shift factor
        regs[0x18].set(0, True)
        regs[0x19].set(0, True)
        regs[0x1a].set(80, True)#Correction floor
        regs[0x1b].set(16, True)#correction muliplier
        regs[0x1c].set(32, True)# correction divider
        regs[0x1d].set(256, True)# correction factor low
        regs[0x1e].set(1024, True)# correction faction higth
        regs[0x1f].set(0, True)# correction factor Derivative
        regs[0x20].set(64, True)# torque limitation factore
        regs[0x21].set(100, True)# stall acknoledge time
        
    
    @staticmethod
    def ppa_9x(self, regs):
        pass
    
    @staticmethod
    def ppa_6x(self, regs):
        pass