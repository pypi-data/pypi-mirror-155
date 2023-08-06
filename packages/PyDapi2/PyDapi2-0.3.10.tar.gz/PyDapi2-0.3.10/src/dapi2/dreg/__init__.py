'''The `dreg` module implements the registers management. 

:author: F. Voillat
'''

from .base import BaseRegElement, DRegException, DRegAccess
from .container import RegContainer
from .group import RegGroup
from .register import Register, ReservedRegister, RegisterArray, BitFieldRegister, RegBit, RegBitChoice, ReservedRegBit
from .reader import RegContainerReader, newRegContainerFromFile