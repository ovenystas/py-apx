from apx.base import *
from apx.vm_base import *


class Compiler:
   def __init__(self):
      pass
   
   def exec(self, port):
      """
      Compiles APX port into a byte-code program
      """
      if isinstance(port, RequirePort):
         return self.compileUnpackProg(port.data_element)
      elif isinstance(port, ProvidePort):
         return self.compilePackProg(port.data_element)
      else:
         raise ValueError('Not an APX port')
   
   def compilePackProg(self, dataElement):
      self.prog = bytearray()
      self._packDataElement(dataElement, True)
      tmp = self.prog
      self.prog = None
      return bytes(tmp)
   
   def compileUnpackProg(self, dataElement):
      self.prog = bytearray()
      self._unpackDataElement(dataElement, True)
      tmp = self.prog
      self.prog = None
      return bytes(tmp)
   
   def _packProgHeader(self, progLen, insert=False):
      tmp = bytearray()
      tmp.append(OPCODE_PACK_PROG)
      tmp.append( (progLen) & 0xFF)
      tmp.append( (progLen >> 8) & 0xFF)
      tmp.append( (progLen >> 16) & 0xFF)
      tmp.append( (progLen >> 24) & 0xFF)
      
      if insert:
         self.prog = tmp + self.prog
      else:
         self.prog.extend(tmp)

   def _unpackProgHeader(self, progLen, insert=False):
      tmp = bytearray()      
      tmp.append(OPCODE_UNPACK_PROG)
      tmp.append( (progLen) & 0xFF)
      tmp.append( (progLen >> 8) & 0xFF)
      tmp.append( (progLen >> 16) & 0xFF)
      tmp.append( (progLen >> 24) & 0xFF)
      if insert:
         self.prog = tmp + self.prog
      else:
         self.prog.extend(tmp)
      
   def _packDataElement(self, dataElement, header):
      if dataElement.isArray():
         return self._packArray(dataElement, header)    
      else:
         return self._packSingleElement(dataElement, header)
   
   def _unpackDataElement(self, dataElement, header):
      if dataElement.isArray():
         return self._unpackArray(dataElement, header)    
      else:
         return self._unpackSingleElement(dataElement, header)
   
   def _packSingleElement(self, dataElement, header):
      if dataElement.typeCode == REFERENCE_TYPE_CODE:
         assert(isinstance(dataElement.typeReference, DataType))
         dataElement = dataElement.typeReference.dsg.dataElement
      
      if dataElement.typeCode == UINT8_TYPE_CODE:
         if header: self._packProgHeader(UINT8_LEN)
         self.prog.append(OPCODE_PACK_U8)
         return UINT8_LEN
      elif dataElement.typeCode == UINT16_TYPE_CODE:
         if header: self._packProgHeader(UINT16_LEN)
         self.prog.append(OPCODE_PACK_U16)
         return UINT16_LEN
      elif dataElement.typeCode == UINT32_TYPE_CODE:
         if header: self._packProgHeader(UINT32_LEN)
         self.prog.append(OPCODE_PACK_U32)
         return UINT32_LEN
      elif dataElement.typeCode == SINT8_TYPE_CODE:
         if header: self._packProgHeader(SINT8_LEN)
         self.prog.append(OPCODE_PACK_S8)
         return SINT8_LEN
      elif dataElement.typeCode == SINT16_TYPE_CODE:
         if header: self._packProgHeader(SINT16_LEN)
         self.prog.append(OPCODE_PACK_S16)
         return SINT16_LEN
      elif dataElement.typeCode == SINT32_TYPE_CODE:
         if header: self._packProgHeader(SINT32_LEN)
         self.prog.append(OPCODE_PACK_S32)
         return SINT32_LEN
      elif dataElement.typeCode == RECORD_TYPE_CODE:
         packLen = 0
         self.prog.append(OPCODE_RECORD_ENTER)
         for childElement in dataElement.elements:
            self._recordSelect(childElement)
            packLen += self._packDataElement(childElement, False)
         self.prog.append(OPCODE_RECORD_LEAVE)
         if header: self._packProgHeader(packLen, insert = True)
         return packLen
      else:
         raise NotImplementedError(dataElement.typeCode)
      
   def _unpackSingleElement(self, dataElement, header):
      if dataElement.typeCode == REFERENCE_TYPE_CODE:
         assert(isinstance(dataElement.typeReference, DataType))
         dataElement = dataElement.typeReference.dsg.dataElement

      if dataElement.typeCode == UINT8_TYPE_CODE:
         if header: self._unpackProgHeader(UINT8_LEN)
         self.prog.append(OPCODE_UNPACK_U8)
         return UINT8_LEN
      elif dataElement.typeCode == UINT16_TYPE_CODE:
         if header: self._unpackProgHeader(UINT16_LEN)
         self.prog.append(OPCODE_UNPACK_U16)
         return UINT16_LEN
      elif dataElement.typeCode == UINT32_TYPE_CODE:
         if header: self._unpackProgHeader(UINT32_LEN)
         self.prog.append(OPCODE_UNPACK_U32)
         return UINT32_LEN
      elif dataElement.typeCode == SINT8_TYPE_CODE:
         if header: self._unpackProgHeader(SINT8_LEN)
         self.prog.append(OPCODE_UNPACK_S8)
         return SINT8_LEN
      elif dataElement.typeCode == SINT16_TYPE_CODE:
         if header: self._unpackProgHeader(SINT16_LEN)
         self.prog.append(OPCODE_UNPACK_S16)
         return SINT16_LEN
      elif dataElement.typeCode == SINT32_TYPE_CODE:
         if header: self._unpackProgHeader(SINT32_LEN)
         self.prog.append(OPCODE_UNPACK_S32)
         return SINT32_LEN
      elif dataElement.typeCode == RECORD_TYPE_CODE:
         packLen = 0
         self.prog.append(OPCODE_RECORD_ENTER)
         for childElement in dataElement.elements:
            self._recordSelect(childElement)
            packLen += self._unpackDataElement(childElement, False)
         self.prog.append(OPCODE_RECORD_LEAVE)
         if header: self._unpackProgHeader(packLen, insert = True)
         return packLen
      else:
         raise NotImplementedError(dataElement.typeCode)      
  
   def _packArray(self, dataElement, header):
      arrayLen = dataElement.arrayLen
      if dataElement.typeCode == UINT8_TYPE_CODE:
         if header: self._packProgHeader(UINT8_LEN * arrayLen)
         return self._packU8AR(arrayLen)         
      elif dataElement.typeCode == UINT16_TYPE_CODE:
         if header: self._packProgHeader(UINT16_LEN * arrayLen)
         return self._packU16AR(arrayLen)
      elif dataElement.typeCode == UINT32_TYPE_CODE:
         if header: self._packProgHeader(UINT32_LEN * arrayLen)
         return self._packU32AR(arrayLen)
      elif dataElement.typeCode == SINT8_TYPE_CODE:
         if header: self._packProgHeader(SINT8_LEN * arrayLen)         
         return self._packS8AR(arrayLen)
      elif dataElement.typeCode == SINT16_TYPE_CODE:
         if header: self._packProgHeader(SINT16_LEN * arrayLen)
         return self._packS16AR(arrayLen)
      elif dataElement.typeCode == SINT32_TYPE_CODE:
         if header: self._packProgHeader(SINT32_LEN * arrayLen)
         return self._packS32AR(arrayLen)
      elif dataElement.typeCode == STRING_TYPE_CODE:
         if header: self._packProgHeader(UINT8_LEN * arrayLen)
         return self._packSTR(arrayLen)
      else:
         raise NotImplementedError(dataElement.typeCode)

   def _unpackArray(self, dataElement, header):
      arrayLen = dataElement.arrayLen
      if dataElement.typeCode == UINT8_TYPE_CODE:
         if header: self._unpackProgHeader(UINT8_LEN * arrayLen)
         return self._unpackU8AR(arrayLen)         
      elif dataElement.typeCode == UINT16_TYPE_CODE:
         if header: self._unpackProgHeader(UINT16_LEN * arrayLen)
         return self._unpackU16AR(arrayLen)
      elif dataElement.typeCode == UINT32_TYPE_CODE:
         if header: self._unpackProgHeader(UINT32_LEN * arrayLen)
         return self._unpackU32AR(arrayLen)
      elif dataElement.typeCode == SINT8_TYPE_CODE:
         if header: self._unpackProgHeader(SINT8_LEN * arrayLen)         
         return self._unpackS8AR(arrayLen)
      elif dataElement.typeCode == SINT16_TYPE_CODE:
         if header: self._unpackProgHeader(SINT16_LEN * arrayLen)
         return self._unpackS16AR(arrayLen)
      elif dataElement.typeCode == SINT32_TYPE_CODE:
         if header: self._unpackProgHeader(SINT32_LEN * arrayLen)
         return self._unpackS32AR(arrayLen)
      elif dataElement.typeCode == STRING_TYPE_CODE:
         if header: self._unpackProgHeader(UINT8_LEN * arrayLen)
         return self._unpackSTR(arrayLen)
      else:
         raise NotImplementedError(dataElement.typeCode)
   
   def _packU8AR(self, arrayLen):
      self.prog.append(OPCODE_PACK_U8AR)
      self.prog.append( (arrayLen) & 0xFF)
      self.prog.append( (arrayLen >> 8) & 0xFF)      
      return UINT8_LEN * arrayLen

   def _unpackU8AR(self, arrayLen):
      self.prog.append(OPCODE_UNPACK_U8AR)
      self.prog.append( (arrayLen) & 0xFF)
      self.prog.append( (arrayLen >> 8) & 0xFF)      
      return UINT8_LEN * arrayLen

   def _packU16AR(self, arrayLen):
      self.prog.append(OPCODE_PACK_U16AR)
      self.prog.append( (arrayLen) & 0xFF)
      self.prog.append( (arrayLen >> 8) & 0xFF)      
      return UINT16_LEN * arrayLen

   def _unpackU16AR(self, arrayLen):
      self.prog.append(OPCODE_UNPACK_U16AR)
      self.prog.append( (arrayLen) & 0xFF)
      self.prog.append( (arrayLen >> 8) & 0xFF)      
      return UINT16_LEN * arrayLen

   def _packU32AR(self, arrayLen):
      self.prog.append(OPCODE_PACK_U32AR)
      self.prog.append( (arrayLen) & 0xFF)
      self.prog.append( (arrayLen >> 8) & 0xFF)      
      return UINT32_LEN * arrayLen

   def _unpackU32AR(self, arrayLen):
      self.prog.append(OPCODE_UNPACK_U32AR)
      self.prog.append( (arrayLen) & 0xFF)
      self.prog.append( (arrayLen >> 8) & 0xFF)      
      return UINT32_LEN * arrayLen

   def _packS8AR(self, arrayLen):
      self.prog.append(OPCODE_PACK_S8AR)
      self.prog.append( (arrayLen) & 0xFF)
      self.prog.append( (arrayLen >> 8) & 0xFF)      
      return SINT8_LEN * arrayLen

   def _unpackS8AR(self, arrayLen):
      self.prog.append(OPCODE_UNPACK_S8AR)
      self.prog.append( (arrayLen) & 0xFF)
      self.prog.append( (arrayLen >> 8) & 0xFF)      
      return SINT8_LEN * arrayLen

   def _packS16AR(self, arrayLen):
      self.prog.append(OPCODE_PACK_S16AR)
      self.prog.append( (arrayLen) & 0xFF)
      self.prog.append( (arrayLen >> 8) & 0xFF)      
      return SINT16_LEN * arrayLen

   def _unpackS16AR(self, arrayLen):
      self.prog.append(OPCODE_UNPACK_S16AR)
      self.prog.append( (arrayLen) & 0xFF)
      self.prog.append( (arrayLen >> 8) & 0xFF)      
      return SINT16_LEN * arrayLen

   def _packS32AR(self, arrayLen):
      self.prog.append(OPCODE_PACK_S32AR)
      self.prog.append( (arrayLen) & 0xFF)
      self.prog.append( (arrayLen >> 8) & 0xFF)      
      return SINT32_LEN * arrayLen

   def _unpackS32AR(self, arrayLen):
      self.prog.append(OPCODE_UNPACK_S32AR)
      self.prog.append( (arrayLen) & 0xFF)
      self.prog.append( (arrayLen >> 8) & 0xFF)      
      return SINT32_LEN * arrayLen

   def _packSTR(self, arrayLen):
      self.prog.append(OPCODE_PACK_STR)
      self.prog.append( (arrayLen) & 0xFF)
      self.prog.append( (arrayLen >> 8) & 0xFF)      
      return UINT8_LEN * arrayLen

   def _unpackSTR(self, arrayLen):
      self.prog.append(OPCODE_UNPACK_STR)
      self.prog.append( (arrayLen) & 0xFF)
      self.prog.append( (arrayLen >> 8) & 0xFF)      
      return UINT8_LEN * arrayLen
   
   def _recordSelect(self, childElement):
      self.prog.append(OPCODE_RECORD_SELECT)      
      self.prog.extend(map(ord, childElement.name))
      self.prog.append(0) #string null terminator
   
   

