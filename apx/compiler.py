from apx.base import *

OPCODE_NOP = 0
OPCODE_PROG = 1
OPCODE_PACK_U8 = 2
OPCODE_PACK_U16 = 3
OPCODE_PACK_U32 = 4
OPCODE_PACK_S8 = 5
OPCODE_PACK_S16 = 6
OPCODE_PACK_S32 = 7
OPCODE_PACK_STR = 8
OPCODE_PACK_U8AR = 9
OPCODE_PACK_U16AR = 10
OPCODE_PACK_U32AR = 11
OPCODE_PACK_S8AR = 12
OPCODE_PACK_S16AR = 13
OPCODE_PACK_S32AR = 14
OPCODE_UNPACK_U8 = 15
OPCODE_UNPACK_U16 = 16
OPCODE_UNPACK_U32 = 17
OPCODE_UNPACK_S8 = 18
OPCODE_UNPACK_S16 = 19
OPCODE_UNPACK_S32 = 20
OPCODE_UNPACK_STR = 21
OPCODE_UNPACK_U8AR = 22
OPCODE_UNPACK_U16AR = 23
OPCODE_UNPACK_U32AR = 24
OPCODE_UNPACK_S8AR = 25
OPCODE_UNPACK_S16AR = 26
OPCODE_UNPACK_S32AR = 27
OPCODE_RECORD_ENTER = 28
OPCODE_RECORD_SELECT = 29
OPCODE_RECORD_LEAVE = 30
OPCODE_ARRAY_ENTER = 31
OPCODE_ARRAY_NEXT = 32
OPCODE_ARRAY_LEAVE = 33

VTYPE_INVALID = -1
VTYPE_SCALAR = 0
VTYPE_LIST = 1
VTYPE_MAP = 2

PACK_PROG = 0
UNPACK_PROG = 1

UINT8_LEN   = 1
UINT16_LEN  = 2
UINT32_LEN  = 4
SINT8_LEN   = 1
SINT16_LEN  = 2
SINT32_LEN  = 4


class Compiler:
   def __init__(self):
      pass
   
   def compilePackProg(self, dataElement):
      self.prog = bytearray()
      self._packDataElement(dataElement, True)
      tmp = self.prog
      self.prog = None
      return bytes(tmp)
   
   def _packDataElement(self, dataElement, header):
      if dataElement.isArray:
         return self._packArray(dataElement, header)    
      else:
         return self._packSingleElement(dataElement, header)
   
   def _packSingleElement(self, dataElement, header):
      if dataElement.typeCode == UINT8_TYPE_CODE:
         if header: self._packProgHeader(VTYPE_SCALAR, UINT8_LEN)
         self.prog.append(OPCODE_PACK_U8)
         return UINT8_LEN
      elif dataElement.typeCode == UINT16_TYPE_CODE:
         if header: self._packProgHeader(VTYPE_SCALAR, UINT16_LEN)
         self.prog.append(OPCODE_PACK_U16)
         return UINT16_LEN
      elif dataElement.typeCode == UINT32_TYPE_CODE:
         if header: self._packProgHeader(VTYPE_SCALAR, UINT32_LEN)
         self.prog.append(OPCODE_PACK_U32)
         return UINT32_LEN
      elif dataElement.typeCode == SINT8_TYPE_CODE:
         if header: self._packProgHeader(VTYPE_SCALAR, SINT8_LEN)
         self.prog.append(OPCODE_PACK_S8)
         return SINT8_LEN
      elif dataElement.typeCode == SINT16_TYPE_CODE:
         if header: self._packProgHeader(VTYPE_SCALAR, SINT16_LEN)
         self.prog.append(OPCODE_PACK_S16)
         return SINT16_LEN
      elif dataElement.typeCode == SINT32_TYPE_CODE:
         if header: self._packProgHeader(VTYPE_SCALAR, SINT32_LEN)
         self.prog.append(OPCODE_PACK_S32)
         return SINT32_LEN
      elif dataElement.typeCode == RECORD_TYPE_CODE:
         packLen = 0
         for childElement in dataElement.elements:
            self._packRecordSelect(childElement)
            packLen += self._packDataElement(childElement, False)
         if header: self._packProgHeader(VTYPE_MAP, packLen, insert = True)
         return packLen
      else:
         raise NotImplementedError(dataElement.typeCode)
  
   def _packArray(self, dataElement, header):
      arrayLen = dataElement.arrayLen
      if dataElement.typeCode == UINT8_TYPE_CODE:
         if header: self._packProgHeader(VTYPE_LIST, UINT8_LEN * arrayLen)
         return self._packU8AR(arrayLen)         
      elif dataElement.typeCode == UINT16_TYPE_CODE:
         if header: self._packProgHeader(VTYPE_LIST, UINT16_LEN * arrayLen)
         return self._packU16AR(arrayLen)
      elif dataElement.typeCode == UINT32_TYPE_CODE:
         if header: self._packProgHeader(VTYPE_LIST, UINT32_LEN * arrayLen)
         return self._packU32AR(arrayLen)
      elif dataElement.typeCode == SINT8_TYPE_CODE:
         if header: self._packProgHeader(VTYPE_LIST, SINT8_LEN * arrayLen)         
         return self._packS8AR(arrayLen)
      elif dataElement.typeCode == SINT16_TYPE_CODE:
         if header: self._packProgHeader(VTYPE_LIST, SINT16_LEN * arrayLen)
         return self._packS16AR(arrayLen)
      elif dataElement.typeCode == SINT32_TYPE_CODE:
         if header: self._packProgHeader(VTYPE_LIST, SINT32_LEN * arrayLen)
         return self._packS32AR(arrayLen)
      elif dataElement.typeCode == STRING_TYPE_CODE:
         if header: self._packProgHeader(VTYPE_LIST, UINT8_LEN * arrayLen)
         return self._packSTR(arrayLen)
      else:
         raise NotImplementedError(dataElement.typeCode)
   
   def _packU8AR(self, arrayLen):
      self.prog.append(OPCODE_PACK_U8AR)
      self.prog.append( (arrayLen >> 8) & 0xFF)
      self.prog.append( (arrayLen) & 0xFF)
      return UINT8_LEN * arrayLen

   def _packU16AR(self, arrayLen):
      self.prog.append(OPCODE_PACK_U16AR)
      self.prog.append( (arrayLen >> 8) & 0xFF)
      self.prog.append( (arrayLen) & 0xFF)
      return UINT16_LEN * arrayLen

   def _packU32AR(self, arrayLen):
      self.prog.append(OPCODE_PACK_U32AR)
      self.prog.append( (arrayLen >> 8) & 0xFF)
      self.prog.append( (arrayLen) & 0xFF)
      return UINT32_LEN * arrayLen

   def _packS8AR(self, arrayLen):
      self.prog.append(OPCODE_PACK_S8AR)
      self.prog.append( (arrayLen >> 8) & 0xFF)
      self.prog.append( (arrayLen) & 0xFF)
      return SINT8_LEN * arrayLen

   def _packS16AR(self, arrayLen):
      self.prog.append(OPCODE_PACK_S16AR)
      self.prog.append( (arrayLen >> 8) & 0xFF)
      self.prog.append( (arrayLen) & 0xFF)
      return SINT16_LEN * arrayLen

   def _packS32AR(self, arrayLen):
      self.prog.append(OPCODE_PACK_S32AR)
      self.prog.append( (arrayLen >> 8) & 0xFF)
      self.prog.append( (arrayLen) & 0xFF)
      return SINT32_LEN * arrayLen

   def _packSTR(self, arrayLen):
      self.prog.append(OPCODE_PACK_STR)
      self.prog.append( (arrayLen >> 8) & 0xFF)
      self.prog.append( (arrayLen) & 0xFF)
      return UINT8_LEN * arrayLen
   
   def _packRecordSelect(self, childElement):
      self.prog.append(OPCODE_RECORD_SELECT)      
      self.prog.extend(map(ord, childElement.name))
      self.prog.append(0) #string null terminator
   
   def _packProgHeader(self, variantTypeByte, progLen, insert=False):
      tmp = bytearray()
      tmp.extend([OPCODE_PROG, PACK_PROG])
      tmp.append(variantTypeByte)
      tmp.append( (progLen >> 16) & 0xFF)
      tmp.append( (progLen >> 8) & 0xFF)
      tmp.append( (progLen) & 0xFF)
      if insert:
         self.prog = tmp + self.prog
      else:
         self.prog.extend(tmp)
   