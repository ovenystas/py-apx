import autosar
import apx
import math
from copy import deepcopy

def _getIntegerTypeCode(dataType):
   """
   using an autosar integer datatype, calculate how many bits are required
   to store its value and based on that, calculate what APX type code to use.
   """
   global args
   if dataType.minVal >= 0:
      bits = _calcUIntTypeLen(dataType)      
      if bits <=8:
         if (dataType.minVal>0) or (dataType.maxVal<255):
            return 'C(%d,%d)'%(dataType.minVal,dataType.maxVal)
         else:
            return 'C'
      elif bits <=16:
         return 'S'
      elif bits <=32:
         return 'L'
      elif bits <=64:
         return 'U'
   elif dataType.minVal<0:
      bits = _calcIntTypeLen(dataType)      
      if bits <=8:
         if (dataType.minval>-128) or dataType.maxVal<127:
            return 'c(%d,%d)'%(dataType.minval,dataType.maxVal)
         else:
            return 'c'
      elif bits <=16:
         return 's'
      elif bits <=32:
         return 'l'
      elif bits <=64:
         return 'u'
   else:
      print("not implemented (min=%s)"%dataType.minval)

def _calcUIntTypeLen(dataType):
   """
   returs number of bits needed to represent the autosar integer
   type value.
   """
   if isinstance(dataType,autosar.datatype.IntegerDataType):
      if dataType.minVal == 0:
         return int(math.ceil(math.log(dataType.maxVal,2)))
   return None

def _calcIntTypeLen(dataType):
   """
   same as _calcUIntTypeLen but for signed integers
   """
   if isinstance(dataType,autosar.datatype.IntegerDataType):
      if dataType.minval < 0:
         return int(math.ceil(math.log(abs(dataType.maxVal),2)))+1
   return None

class Node:
   def __init__(self,name):
      self.name=name
      self.dataTypes = []
      self.requirePorts=[]
      self.providePorts=[]
      self.dataTypeMap = {}      
   
   def _updateDataType(self, ws, port):
      portInterface = ws.find(port.portInterfaceRef)
      if isinstance(portInterface,autosar.portinterface.SenderReceiverInterface):
         if len(portInterface.dataElements)==1:         
            dataType = ws.find(portInterface.dataElements[0].typeRef)
            assert(dataType is not None)
            if dataType.name not in self.dataTypeMap:
               item = apx.AutosarDataType(ws,dataType)
               item.id=len(self.dataTypes)
               self.dataTypeMap[dataType.name]=item
               self.dataTypes.append(item)
               assert (item is not None)
               return item
            else:
               item = self.dataTypeMap[dataType.name]
               assert (item is not None)
               return item
         elif len(portInterface.dataElements)>1:
            raise NotImplementedError('SenderReceiverInterface with more than 1 element not supported')
      return None
   
   def _calcAttributeFromAutosarPort(self,ws,port):
      """
      returns string
      """
      if (len(port.comspec)==1) and isinstance(port.comspec[0],autosar.component.DataElementComSpec):
         if port.comspec[0].initValueRef is not None:
            initValue = ws.find(port.comspec[0].initValueRef)
            return "="+self._deriveInitValueFromAutosarConstant(initValue)
      return None
   
   def _deriveInitValueFromAutosarConstant(self,item):      
      if isinstance(item,autosar.constant.IntegerValue):
         if (item.value>255):
            return "0x%02X"%item.value
         else:
            return "%d"%item.value
      elif isinstance(item,autosar.constant.StringValue):
            return '="%s"'%item.value
      elif isinstance(item,autosar.constant.RecordValue):
         tmp = [self._deriveInitValue(x) for x in item.elements]
         return "{"+','.join(tmp)+"}"
      elif isinstance(item,autosar.constant.ArrayValue):
         tmp = [self._deriveInitValue(x) for x in item.elements]
         return "{"+','.join(tmp)+"}"
      else:
         raise NotImplementedError(str(type(item)))

   
   def import_autosar_swc(self, swc, ws=None):
      assert(isinstance(swc, autosar.component.AtomicSoftwareComponent))
      for port in swc.providePorts:
         self.add_autosar_port(port, ws)
      for port in swc.requirePorts:
         self.add_autosar_port(port, ws)
   
   def add_autosar_port(self, port, ws=None):
      """
      adds an autosar port to the node
      """
      if ws is None:
         ws=port.rootWS()
      assert(ws is not None)
      dataType=self._updateDataType(ws, port)
      if dataType is not None:         
         if isinstance(port, autosar.component.RequirePort):
            apx_port = apx.RequirePort(port.name, "T[%s]"%dataType.id, self._calcAttributeFromAutosarPort(ws, port))
            self.requirePorts.append(apx_port)
         elif isinstance(port, autosar.component.ProvidePort):
            apx_port = apx.ProvidePort(port.name, "T[%s]"%dataType.id, self._calcAttributeFromAutosarPort(ws, port))
            self.providePorts.append(apx_port)
         else:
            raise ValueError('invalid type '+str(type(port)))
   
   def add_require_port(self, name, dsg, attr=None):
      pass
  
  
   def add_type(self, dataType):
      if dataType.name not in self.dataTypeMap:
         dataType.id=len(self.dataTypes)
         self.dataTypeMap[dataType.name]=dataType
         self.dataTypes.append(dataType)
   
   def write(self, fp):
      """
      writes node as text in fp
      """
      print('N"%s"'%self.name, file=fp)
      for dataType in self.dataTypes:
         print(str(dataType), file=fp)
      for port in self.providePorts:
         print(str(port), file=fp)
      for port in self.requirePorts:
         print(str(port), file=fp)
   
   def lines(self):
      """
      returns context as list of strings (one line at a time)
      """
      lines = ['N"%s"'%self.name]      
      for dataType in self.dataTypes:
         lines.append(str(dataType))
      for port in self.providePorts:
         lines.append(str(port))
      for port in self.requirePorts:
         lines.append(str(port))
      return lines
   
   def mirror(self, name):
      """
      clones the node in a version where all provide and require ports are reversed
      """
      mirror = Node(name)
      mirror.dataTypes = deepcopy(self.dataTypes)
      mirror.requirePorts = [port.mirror() for port in self.providePorts]
      mirror.providePorts = [port.mirror() for port in self.requirePorts]
      for dataType in mirror.dataTypes:
         mirror.dataTypeMap[dataType.name]=dataType
      return mirror
      
   
class AutosarPort:
   """
   An AUTOSAR port (base type)
   """
   def __init__(self,name,typeId):
      self.name = name
      self.typeId = typeId



class AutosarRequirePort(AutosarPort):
   def __init__(self, name, typeId, ws=None, port=None):
      super().__init__(name,typeId)
      if (ws is not None) and (port is not None):
         self.attr = self._calcAttribute(ws,port)
   
   def __str__(self):
      if self.attr is not None:
         return 'R"%s"T[%d]:%s'%(self.name,self.typeId,self.attr)
      else:
         return 'R"%s"T[%d]'%(self.name,self.typeId)
   
   def mirror(self):
      other = AutosarProvidePort(self.name, self.typeId)
      other.attr = self.attr
      return other

class AutosarProvidePort(AutosarPort):
   def __init__(self, name, typeId, ws=None, port=None):
      super().__init__(name,typeId)
      if (ws is not None) and (port is not None):
         self.attr = self._calcAttribute(ws,port)
   
   def __str__(self):
      if self.attr is not None:
         return 'P"%s"T[%d]:%s'%(self.name,self.typeId,self.attr)
      else:
         return 'P"%s"T[%d]'%(self.name,self.typeId)

   def mirror(self):
      other = AutosarRequirePort(self.name, self.typeId)
      other.attr = self.attr
      return other

class AutosarDataType:
   def __init__(self,ws,dataType):
      self.name=dataType.name
      self.dsg=self._calcDataSignature(ws,dataType)
      typeSemantics = ws.find('/DataType/DataTypeSemantics/%s'%dataType.name)
      if typeSemantics is not None:
         self.attr = self._calcAttribute(dataType,typeSemantics)
      else:
         self.attr=None      
   
   def __str__(self):
      if self.attr is not None:
         return 'T"%s"%s:%s'%(self.name,self.dsg,self.attr)
      else:
         return 'T"%s"%s'%(self.name,self.dsg)
   
   def _calcAttribute(self,dataType,typeSemantics):
      if isinstance(typeSemantics,autosar.datatype.CompuMethodConst):
         values=[]
         for elem in typeSemantics.elements:
            assert(isinstance(elem,autosar.datatype.CompuConstElement))
            values.append(elem.textValue)
         v=','.join(['"%s"'%x for x in values])
         return "VT(%s)"%v
      return None

   def _calcDataSignature(self,ws,dataType):      
      if isinstance(dataType,autosar.datatype.BooleanDataType):
         return 'C(0,1)'
      if isinstance(dataType,autosar.datatype.IntegerDataType):      
         return _getIntegerTypeCode(dataType)
      elif isinstance(dataType,autosar.datatype.ArrayDataType):
         typeCode = _getIntegerTypeCode(typeData.find(dataType['typeRef']))
         if typeCode != None:
            return "%s[%d]"%(typeCode,int(dataType.length))
         else:
            raise Exception("unsupported type: %s"%typeData.find(dataType['typeRef']))
      elif isinstance(dataType,autosar.datatype.StringDataType):
         typeCode = 'a'
         if typeCode != None:
            return "%s[%d]"%(typeCode,int(dataType.length)+1)            
      elif isinstance(dataType,autosar.datatype.RecordDataType):
         result="{"
         for elem in dataType.elements:
            #remove _RE from end of element names
            if elem.name.endswith('_RE'):
               elem.name=elem.name[:-3]
            childType = ws.find(elem.typeRef)
            result+='"%s"%s'%(elem.name, self._calcDataSignature(ws, childType))            
         result+="}"
         return result
      else: raise Exception('unhandled data type: %s'%type(dataType))
      return ""


   