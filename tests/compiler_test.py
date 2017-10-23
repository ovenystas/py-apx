import os, sys, io
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest

class TestCompilePackProg(unittest.TestCase):
    
   def test_packU8(self):
      dataElement = apx.DataElement.UInt8(minVal=0, maxVal=3)
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.PACK_PROG, apx.VTYPE_SCALAR, 0,0,apx.UINT8_LEN, apx.OPCODE_PACK_U8]))

   def test_packU16(self):
      dataElement = apx.DataElement.UInt16()
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.PACK_PROG, apx.VTYPE_SCALAR, 0,0,apx.UINT16_LEN, apx.OPCODE_PACK_U16]))

   def test_packU32(self):
      dataElement = apx.DataElement.UInt32()
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.PACK_PROG, apx.VTYPE_SCALAR, 0,0,apx.UINT32_LEN, apx.OPCODE_PACK_U32]))

   def test_packS8(self):
      dataElement = apx.DataElement.SInt8(minVal=0, maxVal=3)
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.PACK_PROG, apx.VTYPE_SCALAR, 0,0,apx.SINT8_LEN, apx.OPCODE_PACK_S8]))

   def test_packS16(self):
      dataElement = apx.DataElement.SInt16()
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.PACK_PROG, apx.VTYPE_SCALAR, 0,0,apx.SINT16_LEN, apx.OPCODE_PACK_S16]))

   def test_packS32(self):
      dataElement = apx.DataElement.SInt32()
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.PACK_PROG, apx.VTYPE_SCALAR, 0,0,apx.SINT32_LEN, apx.OPCODE_PACK_S32]))

   def test_packU8AR(self):
      dataElement = apx.DataElement.UInt8(minVal=0, maxVal=3, arrayLen = 10)
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.PACK_PROG, apx.VTYPE_LIST, 0,0,apx.UINT8_LEN * dataElement.arrayLen, apx.OPCODE_PACK_U8AR, 0, dataElement.arrayLen]))

   def test_packU16AR(self):
      dataElement = apx.DataElement.UInt16(minVal=0, maxVal=3, arrayLen = 5)
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.PACK_PROG, apx.VTYPE_LIST, 0,0,apx.UINT16_LEN * dataElement.arrayLen, apx.OPCODE_PACK_U16AR, 0, dataElement.arrayLen]))

   def test_packU32AR(self):
      dataElement = apx.DataElement.UInt32(minVal=0, maxVal=3, arrayLen = 3)
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.PACK_PROG, apx.VTYPE_LIST, 0,0,apx.UINT32_LEN * dataElement.arrayLen, apx.OPCODE_PACK_U32AR, 0, dataElement.arrayLen]))

   def test_packS8AR(self):
      dataElement = apx.DataElement.SInt8(minVal=0, maxVal=3, arrayLen = 10)
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.PACK_PROG, apx.VTYPE_LIST, 0,0,apx.SINT8_LEN * dataElement.arrayLen, apx.OPCODE_PACK_S8AR, 0, dataElement.arrayLen]))

   def test_packS16AR(self):
      dataElement = apx.DataElement.SInt16(minVal=0, maxVal=3, arrayLen = 5)
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.PACK_PROG, apx.VTYPE_LIST, 0,0,apx.SINT16_LEN * dataElement.arrayLen, apx.OPCODE_PACK_S16AR, 0, dataElement.arrayLen]))

   def test_packS32AR(self):
      dataElement = apx.DataElement.SInt32(minVal=0, maxVal=3, arrayLen = 3)
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.PACK_PROG, apx.VTYPE_LIST, 0,0,apx.SINT32_LEN * dataElement.arrayLen, apx.OPCODE_PACK_S32AR, 0, dataElement.arrayLen]))
            
   def test_packString(self):
      dataElement = apx.DataElement.String(arrayLen = 20)
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.PACK_PROG, apx.VTYPE_LIST, 0,0,apx.UINT8_LEN * dataElement.arrayLen, apx.OPCODE_PACK_STR, 0, dataElement.arrayLen]))
   
   def test_packRecord(self):
      child1 = apx.DataElement.UInt16("SoundId")
      child2 = apx.DataElement.UInt8("Volume", arrayLen = 4)
      child3 = apx.DataElement.UInt8("Repetitions")
      packLen = apx.UINT16_LEN + 4*apx.UINT8_LEN + apx.UINT8_LEN
      dataElement = apx.DataElement.Record(elements = [child1, child2, child3])
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      expected = bytes([
         apx.OPCODE_PROG, apx.PACK_PROG, apx.VTYPE_MAP, 0, 0, packLen,
         apx.OPCODE_RECORD_SELECT,ord('S'),ord('o'),ord('u'),ord('n'),ord('d'),ord('I'),ord('d'),0,apx.OPCODE_PACK_U16,
         apx.OPCODE_RECORD_SELECT,ord('V'),ord('o'),ord('l'),ord('u'),ord('m'),ord('e'),0,apx.OPCODE_PACK_U8AR,0,4,
         apx.OPCODE_RECORD_SELECT,ord('R'),ord('e'),ord('p'),ord('e'),ord('t'),ord('i'),ord('t'),ord('i'),ord('o'),ord('n'),ord('s'),0,apx.OPCODE_PACK_U8,
      ])
      self.assertEqual(prog, expected)

class TestCompileUnpackProg(unittest.TestCase):
    
   def test_unpackU8(self):
      dataElement = apx.DataElement.UInt8(minVal=0, maxVal=3)
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.UNPACK_PROG, apx.VTYPE_SCALAR, 0, 0, apx.UINT8_LEN, apx.OPCODE_UNPACK_U8]))

   def test_unpackU16(self):
      dataElement = apx.DataElement.UInt16()
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.UNPACK_PROG, apx.VTYPE_SCALAR, 0,0,apx.UINT16_LEN, apx.OPCODE_UNPACK_U16]))

   def test_unpackU32(self):
      dataElement = apx.DataElement.UInt32()
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.UNPACK_PROG, apx.VTYPE_SCALAR, 0,0,apx.UINT32_LEN, apx.OPCODE_UNPACK_U32]))

   def test_unpackS8(self):
      dataElement = apx.DataElement.SInt8(minVal=0, maxVal=3)
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.UNPACK_PROG, apx.VTYPE_SCALAR, 0,0,apx.SINT8_LEN, apx.OPCODE_UNPACK_S8]))

   def test_unpackS16(self):
      dataElement = apx.DataElement.SInt16()
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.UNPACK_PROG, apx.VTYPE_SCALAR, 0,0,apx.SINT16_LEN, apx.OPCODE_UNPACK_S16]))

   def test_unpackS32(self):
      dataElement = apx.DataElement.SInt32()
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.UNPACK_PROG, apx.VTYPE_SCALAR, 0, 0, apx.SINT32_LEN, apx.OPCODE_UNPACK_S32]))

   def test_unpackU8AR(self):
      dataElement = apx.DataElement.UInt8(minVal=0, maxVal=3, arrayLen = 10)
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.UNPACK_PROG, apx.VTYPE_LIST, 0, 0, apx.UINT8_LEN * dataElement.arrayLen, apx.OPCODE_UNPACK_U8AR, 0, dataElement.arrayLen]))

   def test_unpackU16AR(self):
      dataElement = apx.DataElement.UInt16(minVal=0, maxVal=3, arrayLen = 5)
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.UNPACK_PROG, apx.VTYPE_LIST, 0, 0, apx.UINT16_LEN * dataElement.arrayLen, apx.OPCODE_UNPACK_U16AR, 0, dataElement.arrayLen]))

   def test_unpackU32AR(self):
      dataElement = apx.DataElement.UInt32(minVal=0, maxVal=3, arrayLen = 3)
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.UNPACK_PROG, apx.VTYPE_LIST, 0, 0, apx.UINT32_LEN * dataElement.arrayLen, apx.OPCODE_UNPACK_U32AR, 0, dataElement.arrayLen]))

   def test_unpackS8AR(self):
      dataElement = apx.DataElement.SInt8(arrayLen = 10)
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.UNPACK_PROG, apx.VTYPE_LIST, 0, 0, apx.SINT8_LEN * dataElement.arrayLen, apx.OPCODE_UNPACK_S8AR, 0, dataElement.arrayLen]))

   def test_unpackS16AR(self):
      dataElement = apx.DataElement.SInt16(arrayLen = 5)
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.UNPACK_PROG, apx.VTYPE_LIST, 0, 0, apx.SINT16_LEN * dataElement.arrayLen, apx.OPCODE_UNPACK_S16AR, 0, dataElement.arrayLen]))

   def test_unpackS32AR(self):
      dataElement = apx.DataElement.SInt32(arrayLen = 3)
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PROG, apx.UNPACK_PROG, apx.VTYPE_LIST, 0, 0, apx.SINT32_LEN * dataElement.arrayLen, apx.OPCODE_UNPACK_S32AR, 0, dataElement.arrayLen]))

   def test_unpackRecord(self):
      child1 = apx.DataElement.UInt16("SoundId")
      child2 = apx.DataElement.UInt8("Volume", arrayLen = 4)
      child3 = apx.DataElement.UInt8("Repetitions")
      packLen = apx.UINT16_LEN + 4*apx.UINT8_LEN + apx.UINT8_LEN
      dataElement = apx.DataElement.Record(elements = [child1, child2, child3])
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      expected = bytes([
         apx.OPCODE_PROG, apx.UNPACK_PROG, apx.VTYPE_MAP, 0, 0, packLen,
         apx.OPCODE_RECORD_SELECT,ord('S'),ord('o'),ord('u'),ord('n'),ord('d'),ord('I'),ord('d'),0,apx.OPCODE_UNPACK_U16,
         apx.OPCODE_RECORD_SELECT,ord('V'),ord('o'),ord('l'),ord('u'),ord('m'),ord('e'),0,apx.OPCODE_UNPACK_U8AR,0,4,
         apx.OPCODE_RECORD_SELECT,ord('R'),ord('e'),ord('p'),ord('e'),ord('t'),ord('i'),ord('t'),ord('i'),ord('o'),ord('n'),ord('s'),0,apx.OPCODE_UNPACK_U8,
      ])
      self.assertEqual(prog, expected)

if __name__ == '__main__':
    unittest.main()