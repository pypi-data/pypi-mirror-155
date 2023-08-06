'''The *dapi2* package implements the DAPI2 protocol and register management. 

:author: F. Voillat
:copyright: ® 2021  Dassym SA

This program is free software: you can redistribute it and/or modify
it under the terms of the **GNU General Public License** as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You can consult the GNU General Public License on http://www.gnu.org/licenses/gpl-3.0.html.
'''


from ._version import VERSION, __ver__, __version__

from .dcom import COM_SPEEDS, DComError
from .common import DApi2Side, DApiException, REG_SIZE, REG_MAX_VALUE, dateToWord, versionToStr, versionToWord,\
        wordToVersion, wordToDate 
    
from .signal import DSignal
    
from .dmsg import  MsgType, MsgReaderState,ACK_CHAR, NAK_CHAR, CRC_INITIAL,\
                        ReadRegMessage, ValueRegMessage, BaseMessage, MsgReader, WriteRegMessage, WrittenRegMessage,\
                        CommandMessage, AckMsg, NakMsg, buffer2str
                        
     
    
    
from .dreg import BaseRegElement, RegContainer, RegContainerReader, Register, RegGroup, RegisterArray

from .dapi2 import DApi2, DApiAccessLevel
from .dcom import DSerial, DSocket, DComTracingDirection, TRACE_INGOING_RAW_FMT, TRACE_OUTGOING_RAW_FMT,\
        TRACE_INGOING_NORMAL_FMT, TRACE_OUTGOING_NORMAL_FMT, TRACE_INGOING_COLOR, TRACE_OUTGOING_COLOR, TRACE_RESET_COLOR,\
        TRACE_INERROR_COLOR, TRACE_OUTERROR_COLOR
        
from .derror import *
from .dboard import *

