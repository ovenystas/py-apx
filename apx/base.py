import autosar
import math
import re


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
   elif item['type']=='s': retval= 'sint16'
   elif item['type']=='S': retval = 'sint16'
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
      return ProvidePort(self.name, self.dsg, self.attr)


class ProvidePort(Port):
   """
   APX provide port
   """
   def __init__(self, name, dataSignature, attributes=None):
      super().__init__('P',name, dataSignature, attributes)
   def mirror(self):
      return RequirePort(self.name, self.dsg, self.attr)

     
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
         (signature,remain)=DataSignature._parseDataSignature(dsg)
         if len(remain)>0:
            raise Exception("string '%s' not fully parsed"%dsg)
         self.data=signature
         self.str=dsg
         self.parent=parent
      else:
         raise NotImplementedError(type(dsg))
      
   def __str__(self):
      return self.str
     
   def packLen(self,typeList=None):
      result=0
      stack = []      
      i = iter([self.data])
      
      while True:
         try:
            node = next(i)
         except StopIteration:
            try:
               i = stack.pop()
               continue
            except IndexError:
               break
         if node['type']=='record':
            stack.append(i)
            i=iter(node['elements'])
         else:
            elemSize=self.calcElemSize(node,typeList)
            result+=elemSize
               
      return result

   def calcElemSize(self,node,typeList):
      if node['type']=='C' or node['type']=='c' or node['type']=='E' or node['type']=='a' or node['type']=='b': elemSize=1
      elif node['type']=='S' or node['type']=='s': elemSize=2
      elif node['type']=='L' or node['type']=='l': elemSize=4
      elif node['type']=='u' or node['type']=='U': elemSize=8
      elif node['type']=='n': elemSize=4
      elif node['type']=='N': elemSize=8
      elif node['type']=='typeRef':
         if not isinstance(typeList,list):
            raise ValueError("typeList must be of type list")
         dataType=typeList[self.data['refId']]
         return self.calcElemSize(dataType.dsg.data,typeList)
      else:
         elemSize=0
         for elem in node['elements']:
            elemSize+=self.calcElemSize(elem,typeList)
      if node['isArray']:
         return elemSize*node['arrayLen']
      else:      
         return elemSize
      
      
   def ctypename(self,typeList=None):
      """
      Returns the C type name of the data signature as a string. This return value can be used for code generation in C/C++ code.
      """
      if self.data['type']=='typeRef':
         return typeList[self.data['refId']].name
      else:
         return _derive_c_typename(self.data)
   def isComplexType(self,typeList=None):
      """
      Returns True of the type is record, array or string. Otherwise it returns False
      """
      obj=self.resolveType(typeList)
      if ( (obj.data['type']=='record') or (obj.data['type']=='string') or
            ( ('isArray' in obj.data) and (obj.data['isArray']==True) ) ):
         return True
      return False
   def isArray(self,typeList=None):
      """
      Returns True of the type is array. Otherwise it returns False
      """
      obj=self.resolveType(typeList)
      if ('isArray' in obj.data) and (obj.data['isArray']==True):
         return True
      return False
   def resolveType(self,typeList=None):
      """
      Returns type object
      """
      if self.data['type']=='typeRef':
         if typeList is not None:
            obj=typeList[self.data['refId']].dsg
         elif self.typeList is not None:
            obj=self.typeList[self.data['refId']].dsg
         else:
            raise ValueError('no typelist avaliable')
         
      else:
         obj=self
      return obj

   @staticmethod
   def _parseRecordSignature(remain):
      elements=[]
      while len(remain)>0:
         (name,remain)=match_pair(remain,'"','"')
         if len(remain)>0:            
            (elem,remain)=ApxDataSignature._parseDataSignature(remain)
            if elem == None:
               if remain[0] == '}':
                  return {'type':'record','elements':elements,'isArray':False},remain[1:]
               else:
                  raise Exception('syntax error while parsing record')
            else:
               elem['name']=name
               elements.append(elem)
      return (None,remain)
   
   @staticmethod
   def _parseExtendedTypeCode(c,data):
      values=re.split(r'\s*,\s*',data)
      if len(values)<2:
         raise Exception("min,max missing from %s"%data)
      attr = {'min':int(values[0]),'max':int(values[1])}
      return {'type':c,'isArray':False,'attr':attr}
   
   @staticmethod   
   def _parseDataSignature(s):
      remain=s
      c=remain[0]      
      if c=='{': #start of record 
         remain = remain[1:]
         return ApxDataSignature._parseRecordSignature(remain)      
      if c=='T': #typeRef         
         (data,remain2)=match_pair(remain[1:],'[',']')
         if data!=None and len(remain2)==0:            
            return({'type':'typeRef','refId':int(data)},remain2)
         else:
            raise Exception("parse failure '%s'"%remain)
      else:
         typeCodes=['a','c','s','l','u','n','C','S','L','U','N']
         try:
            i = typeCodes.index(c)
         except ValueError:
            return (None,remain)
         if (len(remain)>1) and (remain[1]=='['):
               (data,remain)=match_pair(remain[1:],'[',']')
               return ({'type':c,'isArray':True,'arrayLen':int(data)},remain)
         if (len(remain)>1) and (remain[1]=='('):
               (data,remain)=match_pair(remain[1:],'(',')')
               return (DataSignature._parseExtendedTypeCode(c,data),remain)
         else:
            remain=remain[1:]
            return ({'type':c,'isArray':False},remain)         
         
class PortAttribute:
   """
   Port attributes are attributes declared on a line starting with either 'R' or 'P'
   """   
   _p2=re.compile(r'0x([0-9A-Fa-f]+)|(\d+)|"([^"]*)"')
   _p3=re.compile(r'\[(\d+)\]')
   def _parseInitValue(self,remain):      
      remain=remain.lstrip()   
      if remain.startswith('{'):
         (match,remain2)=match_pair(remain,'{','}')
         elements=[]         
         while len(match)>0:
            match=match.lstrip()
            (elem,match)=self._parseInitValue(match)
            elements.append(elem)
            match=match.lstrip()
            if match.startswith(','):
               match=match[1:]
               match=match.lstrip()
            elif len(match)==0:
               return ({'type':'record','elements':elements},remain2)
            else:
               raise SyntaxError
      else:
         m=PortAttribute._p2.match(remain)
         if m:
            remain=remain[m.end():]
            if m.group(1):
               return ({'type': 'integer', 'value': int(m.group(1),16)},remain)
            elif m.group(2):
               return ({'type': 'integer', 'value': int(m.group(2),10)},remain)
            elif m.group(3):
               return ({'type': 'string', 'value': m.group(3)},remain)
      return (None,remain)         

   
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
            m=ApxPortAttribute._p3.match(remain)
            if m:
               self.queueLength=m.group(1)
               remain=remain[m.end():]
            break
         elif remain.startswith('P'):
            self.isParameter=True
            remain=remain[1:]
         else:
            raise SyntaxError
   def __str__(self):
      return self.str
   
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
               raise SyntaxError
            else:
               self.valueTable = []
               strings = result.split(',')
               for string in strings:
                  (name,remain2)=parse_str(string)
                  self.valueTable.append(name)
         else:
            raise SyntaxError




