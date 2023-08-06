'''
Created on 7 févr. 2021

@author: fv
'''

import logging
import lxml.etree as ET

from .. import dreg
from os.path import os




def getXmlDescription(xelement, lang='en'):
    '''Get description of XML element according language.
    
    :param xelement: The XML element
    :type xelement: ElementTree
     
    :param lang: The desired language
    :type lang: str
    
    :return: The description in the specified language, otherwise the first one found or `None` if no description is found.
    :rtype: str
    '''
    xdescr = xelement.find( "descr[@lang='{}']".format(lang)  )
    if xdescr == None:
        xdescr = xelement.find( "descr[1]"  )
    if xdescr != None:
        return xdescr.text
    return None

def getXmlDescriptions(xelement):
    '''Get all descriptions of XML element.
    
    :param xelement: The XML element
    :type xelement: ElementTree
    '''
    ret = {}
    for xdescr in xelement.findall('descr'):
        ret[xdescr.get('lang', None)] = xdescr.text
    return ret

class BaseRegReader(object):
    '''Base class for register structure elements reader
    
    :param owner: Owner of reader.
    :type owner: BaseRegReader
    
    :param parent: Parent element of elements on reading.
    :type parent: BaseRegElement
    '''
    
    def __init__(self, owner, parent, element=None):
        self.log = logging.getLogger(self.__class__.__name__)
        #self.log.debug('Initialize')            
        self._owner = owner
        self._parent = parent         
        self._element = element
        
    @property
    def parent(self):
        '''Parent reader.'''
        return self._parent
        
    @property
    def element(self):
        '''Register structure element on reading.'''
        return self._element
    
    
class RegContainerReader(BaseRegReader):
    '''Object class for read and construct the registers structure.
    
    :param: container: The container or registers structure.
    :type container: RegContainer
    
    :param: filename: The file containing the definition of the registers.
    :type filename: str
    '''
    
    
    
    AVAILABLE_FILE_FORMAT = ('xml',)
    
    def __init__(self, container=None, filename=None):
        assert container is None or isinstance(container, dreg.RegContainer)
          
        super().__init__(None, None, container)
        
        if filename is not None:
            self.readFromFile(filename)
        
    
    def readFromFile(self, filename):
        '''Read the registers structure from file.
        
        :param filename: The filename (path) of file containing registers structure.
        :type filename: str
        '''
        if self.element is None:
            self._element = dreg.RegContainer(None)
        self.element.clear()
        
        #TODO: select file reader regarding the format of file `filename`
        self.readXML(ET.parse(filename))
        
        return self.element
            
        
    def readXML(self, xtree, addr=0):
        '''Read XML tree registers structure.
        
        :param xtree: The XML tree contaning the registers structure and description
        :type xtree: ElementTree

        :param addr: Base addrees of registers to read.
        :type addr: int
        '''
        size = None
        xroot = xtree.getroot()
        
        #self.log.debug('readXML:<'+xroot.tag+'>')
        
        try:
            size = int(xroot.get('size'),0) 
        except ValueError:
            pass
        if size is not None:
            self.element.setSize(size)
        
        rgroup = RegGroupReader(self, self.element)
        for xgroup in xroot.findall('group'):
            group = rgroup.readXml(xgroup, addr)
            addr = self.element.add(group)
            if addr > self.element.size:
                self.element.setSize(addr)
            
            

        
class RegGroupReader(BaseRegReader):
    '''Class to read groups of registers''' 

    def readXml(self, xgroup, addr=0):
        '''Read XML tree of group of registers.
        '''
        #self.log.debug('readXML:<'+xgroup.tag+' name="'+str(xgroup.get('name'))+'">')
        try:
            addr = int(xgroup.get('address'),0)
        except:
            pass
        self._element = dreg.RegGroup(
                        xgroup.get('name'),
                        self.parent, 
                        addr, 
                        size=int(xgroup.get('size','0'),0), 
                        descriptions=getXmlDescriptions(xgroup),
                        shortname=xgroup.get('shortname'),
                        access=dreg.DRegAccess[xgroup.get('access','READ')], 
                    )

                    
        rreg =  RegReader(self, self.element)
        for xreg in xgroup.findall('reg'):
            reg = rreg.readXml(xreg, addr)
            addr = self.element.add(reg)

        return self.element
    
    
class RegReader(BaseRegReader):
    '''Class to read registers''' 
    
    def readXml(self, xreg, addr=0):
        #self.log.debug('readXML:<'+xreg.tag+' name="'+str(xreg.get('name'))+'">')
        try:
            addr = int(xreg.get('address'),0)
        except:
            pass
        try:
            size = int(xreg.get('size'),0)
        except:
            size = 1
            
        name = xreg.get('name')
        
        if size == 1:
            if name is None:
                _class = dreg.ReservedRegister
                name = 'Reserved' 
            else:
                _class = dreg.Register
            
            if xreg.find('bit') is not None:
                _class = dreg.BitFieldRegister 
        elif size > 1:
            _class = dreg.RegisterArray 
        else:
            raise ValueError('Size must be greater than 0') 
        
        try:
            access = dreg.DRegAccess[xreg.get('access')] 
        except:
            access  = self.parent.access
        self._element = _class( name,
                         self.parent, 
                         addr, 
                         size=size, 
                         descriptions=getXmlDescriptions(xreg),
                         shortname=xreg.get('shortname'),
                         access =access ,
                         )
        
        if _class is dreg.BitFieldRegister:
            bit_addr = 0 
            rbit = BitFieldReader(self, self.element)
            for xbit in xreg.findall('bit'):
                bit = rbit.readXml(xbit, bit_addr)
                bit_addr = self.element.add(bit)

        return self.element


class BitFieldReader(BaseRegReader):
    
    def readXml(self, xbit, addr=0):
        #self.log.debug('readXML:<'+xbit.tag+' name="'+str(xbit.get('name'))+'">')
        size = int(xbit.get('size','1'),0)
        name = xbit.get('name')
        if name is not None:
            self._element = dreg.RegBit(name, self.parent, addr, size, descriptions=getXmlDescriptions(xbit),)
            self._element.choices = {}
            for xchoice in xbit.findall('choice'):
                v = int(xchoice.get('value','0'),0)
                self._element.choices[v] = xchoice.get('name')
        else: 
            self._element = dreg.ReservedRegBit('Reserved', self.parent, addr, size, descriptions=getXmlDescriptions(xbit),)
        return self.element
    
def newRegContainerFromFile(filename=None):
    if filename is None:
        filename = os.path.join(os.path.dirname(__file__), 'regs.xml')
    regs = dreg.RegContainer(None)
    reader = RegContainerReader(regs)
    reader.readFromFile(filename)
    return regs    
