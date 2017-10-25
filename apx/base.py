import autosar
import math
import re
import sys
import copy

INVALID_TYPE_CODE = -1
UINT8_TYPE_CODE = 0
UINT16_TYPE_CODE = 1
UINT32_TYPE_CODE = 2
UINT64_TYPE_CODE = 3
SINT8_TYPE_CODE = 4
SINT16_TYPE_CODE = 5
SINT32_TYPE_CODE = 6
SINT64_TYPE_CODE = 7
STRING_TYPE_CODE = 8
RECORD_TYPE_CODE = 9
REFERENCE_TYPE_CODE = 10

VTYPE_INVALID = -1
VTYPE_SCALAR = 0
VTYPE_LIST = 1
VTYPE_MAP = 2

MAX_RECURSE_DEPTH = 10

def match_pair(s,left,right):
   if (len(s)>0) and (s[0]==left):
      count=1
      for i in range(1,len(s)):
         if s[i]==right:
            count-=1
            if count==0:
               return (s[1:i],s[i+1:])
         elif s[i]==left:
            count+=1 #nested pair
      return (None,"")
   return (None,s)

def parse_str(s):
   return match_pair(s,'"','"')



def _derive_c_typename(item):
   """
   returns the C typename for simple data types
   """
   if   item['type']=='c': retval = 'sint8'
   elif item['type']=='C': retval = 'uint8'
   elif item['type']=='s': retval = 'sint16'
   elif item['type']=='S': retval = 'uint16'
   elif item['type']=='l': retval = 'sint32'
   elif item['type']=='L': retval = 'uint32'
   elif item['type']=='a': retval = 'uint8'
   else:
      raise NotImplementedError(str(item['type']))
   if item['isArray']:
      retval+='[%d]'%item['arrayLen']
   return retval


class Port:
   """
   APX port base type
   """
   def __init__(self, portType, name, dataSignature, attributes=None):
      self.portType = portType    #string containing 'P' for provide port or 'R' for require port
      self.name = name            #name of the port
      self.dsg = DataSignature(dataSignature)
      self.attr = PortAttribute(attributes) if attributes is not None else None

   def __str__(self):
      if self.attr is not None:
         dsg=str(self.dsg)
         attr=str(self.attr)
         return '%s"%s"%s:%s'%(self.portType, self.name, dsg, attr)
      else:
         return '%s"%s"%s'%(self.portType, self.name, str(self.dsg))


class RequirePort(Port):
   """
   APX require port
   """
   def __init__(self, name, dataSignature, attributes=None):
      super().__init__('R',name, dataSignature, attributes)
   def mirror(self):
      return ProvidePort(self.name, str(self.dsg), str(self.attr) if self.attr is not None else None)


class ProvidePort(Port):
   """
   APX provide port
   """
   def __init__(self, name, dataSignature, attributes=None):
      super().__init__('P',name, dataSignature, attributes)
   def mirror(self):
      return RequirePort(self.name, str(self.dsg), str(self.attr) if self.attr is not None else None)


class DataType:
   """
   APX datatype
   """
   def __init__(self, name, dataSignature, attributes=None):
      self.name = name
      self.dsg = DataSignature(dataSignature, self)
      self.attr = attributes

   def __str__(self):
      if self.attr is not None:
         return 'T"%s"%s:%s'%(self.name, str(self.dsg), str(self.attr))
      else:
         return 'T"%s"%s'%(self.name, str(self.dsg))

class DataSignature:
   """
   APX Datasignature
   """
   def __init__(self, dsg, parent=None):
      if isinstance(dsg, str):
         (dataElement,remain)=DataSignature.parseDataSignature(dsg)
         if len(remain)>0:
            raise RunTimeError("string '%s' not fully parsed"%dsg)
         assert(isinstance(dataElement, DataElement))
         self.dataElement=dataElement
         self.str=dsg
      elif isinstance(dsg, DataElement):
         self.dataElement=copy.deepcopy(DataElement)
         self.str=None
      else:
         raise NotImplementedError(type(dsg))
      self.parent=parent      

   def __str__(self):
      return self.str

   def packLen(self,typeList=None):
      result=0
      stack = []
      i = iter([self.dataElement])

      while True:
         try:
            dataElement = next(i)
         except StopIteration:
            try:
               i = stack.pop()
               continue
            except IndexError:
               break
         if dataElement.typeCode == RECORD_TYPE_CODE:
            stack.append(i)
            i=iter(dataElement.elements)
         else:
            elemSize=self._calcElemSize(dataElement,typeList)
            result+=elemSize
      return result

   def _calcElemSize(self,dataElement,typeList):
      typeCodes = [UINT8_TYPE_CODE, UINT16_TYPE_CODE, UINT32_TYPE_CODE, UINT64_TYPE_CODE,
                     SINT8_TYPE_CODE, SINT16_TYPE_CODE, SINT32_TYPE_CODE, SINT64_TYPE_CODE,
                     STRING_TYPE_CODE]
      typeSizes = [1, 2, 4, 8, 1, 2, 4, 8, 1]
      if dataElement.typeCode == REFERENCE_TYPE_CODE:
         if not isinstance(typeList,list):
            raise ValueError("typeList must be of type list")
         dataType = dataElement.resolveType(typeList)         
         return self._calcElemSize(dataType.dsg.dataElement,typeList)
      elif dataElement.typeCode == RECORD_TYPE_CODE:
         elemSize = 0
         for childElement in dataElement.elements:
            elemSize+=self._calcElemSize(childElement, typeList)
      else:
         try:
               i = typeCodes.index(dataElement.typeCode)
         except ValueError:
               raise NotImplementedError(dataElement.typeCode)
         elemSize =  typeSizes[i]  
      
      if dataElement.isArray():
         return elemSize*dataElement.arrayLen
      else:
         return elemSize


   def ctypename(self,typeList=None):
      """
      Returns the C type name of the data signature as a string. This return value can be used for code generation in C/C++ code.
      """
      if self.dataElement.isReference:
         return self.dataElement.resolveType().name
      else:
         return _derive_c_typename(self.data)
   
   def isComplexType(self, typeList = None):
      return self.dataElement.isComplexType(typeList)

   def isArray(self, typeList = None):
      return self.dataElement.isArray(typeList)

   def createInitData(self, initValue, typeList = None):
      return self.dataElement.createInitData(initValue, typeList)

   def resolveDataElement(self, typeList = None):
      return self.dataElement.resolveDataElement(typeList)

   @staticmethod
   def _parseRecordSignature(remain):
      recordElement = DataElement.Record()
      while len(remain)>0:
         (name,remain)=match_pair(remain,'"','"')
         if len(remain)>0:
            (childElement,remain)=DataSignature.parseDataSignature(remain)            
            if childElement is None:
               if remain[0] == '}':
                  return (recordElement,remain[1:])
               else:
                  raise RunTimeError('syntax error while parsing record')
            else:
               assert(isinstance(childElement, DataElement))
               childElement.name = name               
               recordElement.elements.append(childElement)
      return (None,remain)

   @staticmethod
   def _parseExtendedTypeCode(text):
      values=re.split(r'\s*,\s*',text)
      if len(values)<2:
         raise Exception("min,max missing from %s"%text)
      minVal = int(values[0])
      maxVal = int(values[1])
      return (minVal, maxVal)
      

   @staticmethod
   def parseDataSignature(s):
      remain=s
      c=remain[0]
      if c=='{': #start of record
         remain = remain[1:]
         return DataSignature._parseRecordSignature(remain)
      if c=='T': #typeRef
         (data,remain2)=match_pair(remain[1:],'[',']')
         if data is not None and len(remain2)==0:            
            (data2,remain3)=match_pair(data,r'"',r'"')
            if data2 is not None:
               assert(len(remain3)==0)
               return DataElement.TypeReference(data2), remain2
            else:
               return DataElement.TypeReference(int(data)), remain2            
         else:
            raise Exception("parse failure '%s'"%remain)
      else:
         typeCodesChar=['C','S','L','U','c','s','l','u','a']
         typeCodeInt = [UINT8_TYPE_CODE, UINT16_TYPE_CODE, UINT32_TYPE_CODE, UINT64_TYPE_CODE,
                     SINT8_TYPE_CODE, SINT16_TYPE_CODE, SINT32_TYPE_CODE, SINT64_TYPE_CODE,
                     STRING_TYPE_CODE]
         try:
            i = typeCodesChar.index(c)
         except ValueError:
            return (None,remain)
         remain=remain[1:]
         if (len(remain)>0) and (remain[0]=='('):
               (data,remain)=match_pair(remain[0:],'(',')')
               if data is None:
                  raise ParseError("Expecting ')' near: "+remain)
               (minVal,maxVal) = DataSignature._parseExtendedTypeCode(data)
         else:
            (minVal,maxVal) = (None, None)
         if (len(remain)>0) and (remain[0]=='['):
               (value,remain)=match_pair(remain[0:],'[',']')
               if value is None:
                  raise ParseError("Expecting ']' near: "+remain)
               arrayLen=int(value)
         else:
            arrayLen = None
         dataElement = DataElement(None, typeCodeInt[i], minVal, maxVal, arrayLen)
         return (dataElement, remain)

  

class DataElement:
   """
   This class describes the type of data that is contained in a data signature. A data signature contains one data element.
   """
   def __init__(self, name=None, typeCode = INVALID_TYPE_CODE, minVal = None, maxVal = None, arrayLen = None, elements = None, reference=None):
      self.name = name
      if reference is not None:         
         self.typeCode = REFERENCE_TYPE_CODE
         assert(isinstance(reference, (int, str)))
         self.typeReference = reference
         self.minVal = None
         self.maxVal = None
         self.arrayLen = None
      else:      
         self.typeCode = typeCode
         self.minVal = minVal
         self.maxVal = maxVal
         self.arrayLen = arrayLen
         self.typeReference = None
      
      if elements is not None:
         self.elements = list(elements)
      else:
         self.elements = None
   
   @property
   def arrayLen(self):
      return self._arrayLen
   
   @arrayLen.setter
   def arrayLen(self, value):
      if value is not None:            
         if value < 0:
            raise ValueError('invalid length: %s'%value)
         self._arrayLen = value
      else:
          self._arrayLen = None
   
   def isArray(self, typeList = None):
      dataElement = self.resolveDataElement(typeList)
      return dataElement._arrayLen is not None
      
   def isRecord(self, typeList = None):
      dataElement = self.resolveDataElement(typeList)
      return dataElement.typeCode == RECORD_TYPE_CODE

   def isComplexType(self, typeList = None):
      return self.isArray() or self.isRecord()
   
   @property
   def isReference(self):
      return self.typeCode == REFERENCE_TYPE_CODE
      
   @classmethod
   def UInt8(cls, name=None, minVal = None, maxVal = None, arrayLen = None):
      return cls(name, UINT8_TYPE_CODE, minVal, maxVal, arrayLen)

   @classmethod
   def UInt16(cls, name=None, minVal = None, maxVal = None, arrayLen = None):
      return cls(name, UINT16_TYPE_CODE, minVal, maxVal, arrayLen)

   @classmethod
   def UInt32(cls, name=None, minVal = None, maxVal = None, arrayLen = None):
      return cls(name, UINT32_TYPE_CODE, minVal, maxVal, arrayLen)

   @classmethod
   def String(cls, name=None, arrayLen = None):
      return cls(name, STRING_TYPE_CODE, None, None, arrayLen)

   @classmethod
   def SInt8(cls, name=None, minVal = None, maxVal = None, arrayLen = None):
      return cls(name, SINT8_TYPE_CODE, minVal, maxVal, arrayLen)

   @classmethod
   def SInt16(cls, name=None, minVal = None, maxVal = None, arrayLen = None):
      return cls(name, SINT16_TYPE_CODE, minVal, maxVal, arrayLen)

   @classmethod
   def SInt32(cls, name=None, minVal = None, maxVal = None, arrayLen = None):
      return cls(name, SINT32_TYPE_CODE, minVal, maxVal, arrayLen)

   @classmethod
   def Record(cls, name=None, elements = None):
      self = cls(name, RECORD_TYPE_CODE)
      if elements is not None:
         self.elements = list(elements)
      else:
         self.elements = []
      return self

   @classmethod
   def TypeReference(cls, reference, name=None):
      self = cls(name, reference = reference)      
      return self
   
   def append(self, elem):
      if self.typeCode == RECORD_TYPE_CODE:
         self.elements.append(elem)
      else:
         raise RunTimeError('DataElement is not a record element')

   def resolveType(self, typeList):
      """
      Returns type object
      """
      if self.typeCode == REFERENCE_TYPE_CODE:
         if typeList is not None:
            if isinstance(self.typeReference, int):
               obj=typeList[self.typeReference]
            else:
               raise NotImplementedError(type(self.typeReference))
         else:
            raise ValueError('typeList argument must not be None')
      else:
         raise ValueError('Not a reference type')
      return obj

   def resolveDataElement(self, typeList):
      dataElement, count = self,0
      while(count < MAX_RECURSE_DEPTH):
         count+=1
         if dataElement.typeCode == REFERENCE_TYPE_CODE:
            dataType = dataElement.resolveType(typeList)
            dataElement = dataType.dsg.dataElement
         else:
            break
      if (count >= MAX_RECURSE_DEPTH) and dataElement.typeCode == REFERENCE_TYPE_CODE:
         raise RunTimeError('Max recurse depth reached')
      return dataElement

   def createInitData(self, initValue, typeList = None):
      data = bytearray()
      if (self.typeCode == RECORD_TYPE_CODE):
         if (initValue.valueType != VTYPE_LIST):
            raise ValueError('invalid init value type: list expected')
         if len(initValue.elements) != len(self.elements):
            raise ValueError('Incorrect number of record elements in init_value: got %d, expected %s'%(len(initValue.elements), len(self.dataElement.elements)))
         for i,dataElement in enumerate(self.elements):
            data.extend(DataElement._createInitDataInner(dataElement, initValue.elements[i], typeList))
      else:
         data.extend(DataElement._createInitDataInner(self, initValue, typeList))
      return data

   @staticmethod
   def _createInitDataInner(dataElement, initValue, typeList = None, is_array_elem=False):
      data = bytearray()
      if (dataElement.typeCode == RECORD_TYPE_CODE):
         raise NotImplementedError('RECORD_TYPE_CODE')
      elif (dataElement.typeCode == STRING_TYPE_CODE):
            if not initValue.isString:
               raise ValueError('invalid init value type: expected string')
            if len(initValue.value) > dataElement.arrayLen:
               print('Warning: init value "%s" will be truncated to %d bytes'%(initValue.value, dataElement.arrayLen), file=sys.stderr)
            for i in range(dataElement.arrayLen):
               if i<len(initValue.value):
                  data.append(ord(initValue.value[i]))
               else:
                  data.append(0)
      elif (dataElement.typeCode in [UINT8_TYPE_CODE, UINT16_TYPE_CODE, UINT32_TYPE_CODE, SINT8_TYPE_CODE, SINT16_TYPE_CODE, SINT32_TYPE_CODE]):
         if (dataElement.isArray()) and (not is_array_elem):
            if (initValue.valueType != VTYPE_LIST):
               raise ValueError('invalid init value type: expected list')
            for initElem in initValue.elements:
               data.extend(DataElement._createInitDataInner(dataElement, initElem, typeList, True))
         else:
            if initValue.valueType != VTYPE_SCALAR:
               raise ValueError('invalid init value type: got %s, expected integer'%(initValue.value))
            if dataElement.typeCode==UINT8_TYPE_CODE or dataElement.typeCode==SINT8_TYPE_CODE:
               data.append(int(initValue.value) & 0xFF)
            elif dataElement.typeCode==UINT16_TYPE_CODE or dataElement.typeCode==SINT16_TYPE_CODE:
               #TODO: implement big endian support
               data.append(int(initValue.value) & 0xFF)
               data.append(int(initValue.value)>>8 & 0xFF)
            elif dataElement.typeCode==UINT32_TYPE_CODE or dataElement.typeCode==SINT32_TYPE_CODE:
               #TODO: implement big endian support
               data.append(int(initValue.value) & 0xFF)
               data.append(int(initValue.value)>>8 & 0xFF)
               data.append(int(initValue.value)>>16 & 0xFF)
               data.append(int(initValue.value)>>24 & 0xFF)
            else:
               raise NotImplementedError(dataElement.typeCode)
      elif dataElement.typeCode == REFERENCE_TYPE_CODE:
         resolvedType = dataElement.resolveType(typeList)
         return DataElement._createInitDataInner(resolvedType.dsg.dataElement, initValue, typeList, is_array_elem)
      else:
         raise NotImplementedError(dataElement.typeCode)
      return data

class InitValue:
   def __init__(self, valueType, value = None):
      self.valueType = valueType
      self.value = value
      if valueType == VTYPE_LIST:
         self.elements = []
      else:
         self.elements = None
   @property
   def isString(self):
      return isinstance(self.value, str)
   
   @classmethod
   def Int(cls, value):
      return cls(VTYPE_SCALAR, int(value))

   @classmethod
   def String(cls, value):
      return cls(VTYPE_SCALAR, str(value))

   @classmethod
   def List(cls):
      return cls(VTYPE_LIST)
      

class PortAttribute:
   """
   Port attributes are attributes declared on a line starting with either 'R' or 'P'
   """
   _p2=re.compile(r'0x([0-9A-Fa-f]+)|(\d+)|"([^"]*)"')
   _p3=re.compile(r'\[(\d+)\]')

   def __init__(self,text):
      self.isQueued=False
      self.isParameter=False
      self.queueLength=None
      self.initValue=None
      self.str = str(text)
      if text==None or len(text)==0:
         return
      remain=text
      while len(remain)>0:
         remain=remain.lstrip()
         if remain.startswith('='):
            remain=remain[1:]
            (initValue,remain)=self._parseInitValue(remain)
            self.initValue=initValue
         elif remain.startswith('Q'):
            self.isQueued=True
            remain=remain[1:]
            m=PortAttribute._p3.match(remain)
            if m:
               self.queueLength=m.group(1)
               remain=remain[m.end():]
            break
         elif remain.startswith('P'):
            self.isParameter=True
            remain=remain[1:]
         else:
            raise ParseError

   def __str__(self):
      return self.str

   def _parseInitValue(self,remain):
      remain=remain.lstrip()
      if remain.startswith('{'):
         (match,remain2)=match_pair(remain,'{','}')
         initValue = InitValue.List()
         while len(match)>0:
            match=match.lstrip()
            (elem,match)=self._parseInitValue(match)
            initValue.elements.append(elem)
            match=match.lstrip()
            if match.startswith(','):
               match=match[1:]
               match=match.lstrip()
            elif len(match)==0:
               return (initValue,remain2)
            else:
               raise ParseError
      else:
         m=PortAttribute._p2.match(remain)
         if m:
            remain=remain[m.end():]
            if m.group(1) is not None:
               return (InitValue.Int(int(m.group(1),16)),remain)
            elif m.group(2) is not None:
               return (InitValue.Int(int(m.group(2),10)),remain)
            elif m.group(3) is not None:
               return (InitValue.String(m.group(3)),remain)
      return (None,remain)

class TypeAttribute(object):
   """
   Type attributes are attributes declared on a line starting with letter 'T'
   """
   def __init__(self,text):
      self.valueTable = None
      self.str=str(text)
      if text==None or len(text)==0:
         return
      remain = text
      while len(remain)>0:
         if remain.startswith('VT('):
            (result,remain) = match_pair(remain[2:],'(',')')
            if result == None:
               raise ParseError
            else:
               self.valueTable = []
               strings = result.split(',')
               for string in strings:
                  (name,remain2)=parse_str(string)
                  self.valueTable.append(name)
         else:
            raise ParseError




class ParseError(RuntimeError):
   pass