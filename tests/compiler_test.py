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
      self.assertEqual(prog, bytes([apx.OPCODE_PACK_PROG, apx.UINT8_LEN, 0, 0, 0, apx.OPCODE_PACK_U8]))

   def test_packU16(self):
      dataElement = apx.DataElement.UInt16()
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PACK_PROG, apx.UINT16_LEN, 0, 0, 0, apx.OPCODE_PACK_U16]))

   def test_packU32(self):
      dataElement = apx.DataElement.UInt32()
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PACK_PROG, apx.UINT32_LEN, 0, 0, 0, apx.OPCODE_PACK_U32]))

   def test_packS8(self):
      dataElement = apx.DataElement.SInt8(minVal=0, maxVal=3)
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PACK_PROG, apx.SINT8_LEN, 0, 0, 0, apx.OPCODE_PACK_S8]))

   def test_packS16(self):
      dataElement = apx.DataElement.SInt16()
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PACK_PROG, apx.SINT16_LEN, 0, 0, 0, apx.OPCODE_PACK_S16]))

   def test_packS32(self):
      dataElement = apx.DataElement.SInt32()
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PACK_PROG, apx.SINT32_LEN, 0, 0, 0, apx.OPCODE_PACK_S32]))

   def test_packU8AR(self):
      dataElement = apx.DataElement.UInt8(minVal=0, maxVal=3, arrayLen = 10)
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PACK_PROG, apx.UINT8_LEN * dataElement.arrayLen, 0, 0, 0, apx.OPCODE_PACK_U8AR, dataElement.arrayLen, 0]))

   def test_packU16AR(self):
      dataElement = apx.DataElement.UInt16(minVal=0, maxVal=3, arrayLen = 5)
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PACK_PROG, apx.UINT16_LEN * dataElement.arrayLen, 0, 0, 0, apx.OPCODE_PACK_U16AR, dataElement.arrayLen, 0]))

   def test_packU32AR(self):
      dataElement = apx.DataElement.UInt32(minVal=0, maxVal=3, arrayLen = 3)
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PACK_PROG, apx.UINT32_LEN * dataElement.arrayLen, 0, 0, 0, apx.OPCODE_PACK_U32AR, dataElement.arrayLen, 0]))

   def test_packS8AR(self):
      dataElement = apx.DataElement.SInt8(minVal=0, maxVal=3, arrayLen = 10)
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PACK_PROG, apx.SINT8_LEN * dataElement.arrayLen, 0, 0, 0, apx.OPCODE_PACK_S8AR, dataElement.arrayLen, 0]))

   def test_packS16AR(self):
      dataElement = apx.DataElement.SInt16(minVal=0, maxVal=3, arrayLen = 5)
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PACK_PROG, apx.SINT16_LEN * dataElement.arrayLen, 0, 0, 0, apx.OPCODE_PACK_S16AR, dataElement.arrayLen, 0]))

   def test_packS32AR(self):
      dataElement = apx.DataElement.SInt32(minVal=0, maxVal=3, arrayLen = 3)
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PACK_PROG, apx.SINT32_LEN * dataElement.arrayLen, 0, 0, 0, apx.OPCODE_PACK_S32AR, dataElement.arrayLen, 0]))

   def test_packString(self):
      dataElement = apx.DataElement.String(arrayLen = 20)
      compiler = apx.Compiler()
      prog = compiler.compilePackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_PACK_PROG, apx.UINT8_LEN * dataElement.arrayLen, 0, 0, 0, apx.OPCODE_PACK_STR, dataElement.arrayLen, 0]))

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
         apx.OPCODE_PACK_PROG, packLen, 0, 0, 0,
         apx.OPCODE_RECORD_ENTER,
         apx.OPCODE_RECORD_SELECT])+"SoundId".encode("ascii")+bytes([0,apx.OPCODE_PACK_U16,
         apx.OPCODE_RECORD_SELECT])+"Volume".encode("ascii")+bytes([0,apx.OPCODE_PACK_U8AR, 4, 0,
         apx.OPCODE_RECORD_SELECT])+"Repetitions".encode("ascii")+bytes([0,apx.OPCODE_PACK_U8, apx.OPCODE_RECORD_LEAVE])
      self.assertEqual(prog, expected)

class TestCompileUnpackProg(unittest.TestCase):

   def test_unpackU8(self):
      dataElement = apx.DataElement.UInt8(minVal=0, maxVal=3)
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_UNPACK_PROG, apx.UINT8_LEN, 0, 0, 0, apx.OPCODE_UNPACK_U8]))

   def test_unpackU16(self):
      dataElement = apx.DataElement.UInt16()
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_UNPACK_PROG, apx.UINT16_LEN, 0, 0, 0, apx.OPCODE_UNPACK_U16]))

   def test_unpackU32(self):
      dataElement = apx.DataElement.UInt32()
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_UNPACK_PROG, apx.UINT32_LEN, 0, 0, 0, apx.OPCODE_UNPACK_U32]))

   def test_unpackS8(self):
      dataElement = apx.DataElement.SInt8(minVal=0, maxVal=3)
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_UNPACK_PROG, apx.SINT8_LEN, 0, 0, 0, apx.OPCODE_UNPACK_S8]))

   def test_unpackS16(self):
      dataElement = apx.DataElement.SInt16()
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_UNPACK_PROG, apx.SINT16_LEN, 0, 0, 0, apx.OPCODE_UNPACK_S16]))

   def test_unpackS32(self):
      dataElement = apx.DataElement.SInt32()
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_UNPACK_PROG, apx.SINT32_LEN, 0, 0, 0, apx.OPCODE_UNPACK_S32]))

   def test_unpackU8AR(self):
      dataElement = apx.DataElement.UInt8(minVal=0, maxVal=3, arrayLen = 10)
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_UNPACK_PROG, apx.UINT8_LEN * dataElement.arrayLen, 0, 0, 0, apx.OPCODE_UNPACK_U8AR, dataElement.arrayLen, 0]))

   def test_unpackU16AR(self):
      dataElement = apx.DataElement.UInt16(minVal=0, maxVal=3, arrayLen = 5)
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_UNPACK_PROG, apx.UINT16_LEN * dataElement.arrayLen, 0, 0, 0, apx.OPCODE_UNPACK_U16AR, dataElement.arrayLen, 0]))

   def test_unpackU32AR(self):
      dataElement = apx.DataElement.UInt32(minVal=0, maxVal=3, arrayLen = 3)
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_UNPACK_PROG, apx.UINT32_LEN * dataElement.arrayLen, 0, 0, 0, apx.OPCODE_UNPACK_U32AR, dataElement.arrayLen, 0]))

   def test_unpackS8AR(self):
      dataElement = apx.DataElement.SInt8(arrayLen = 10)
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_UNPACK_PROG, apx.SINT8_LEN * dataElement.arrayLen, 0, 0, 0, apx.OPCODE_UNPACK_S8AR, dataElement.arrayLen, 0]))

   def test_unpackS16AR(self):
      dataElement = apx.DataElement.SInt16(arrayLen = 5)
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_UNPACK_PROG, apx.SINT16_LEN * dataElement.arrayLen, 0, 0, 0, apx.OPCODE_UNPACK_S16AR, dataElement.arrayLen, 0]))

   def test_unpackS32AR(self):
      dataElement = apx.DataElement.SInt32(arrayLen = 3)
      compiler = apx.Compiler()
      prog = compiler.compileUnpackProg(dataElement)
      self.assertIsInstance(prog, bytes)
      self.assertEqual(prog, bytes([apx.OPCODE_UNPACK_PROG, apx.SINT32_LEN * dataElement.arrayLen, 0, 0, 0, apx.OPCODE_UNPACK_S32AR, dataElement.arrayLen, 0]))

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
         apx.OPCODE_UNPACK_PROG, packLen, 0, 0, 0,
         apx.OPCODE_RECORD_ENTER,
         apx.OPCODE_RECORD_SELECT])+"SoundId\0".encode('ascii')+bytes([
         apx.OPCODE_UNPACK_U16,
         apx.OPCODE_RECORD_SELECT])+"Volume\0".encode('ascii')+bytes([
         apx.OPCODE_UNPACK_U8AR, 4, 0,
         apx.OPCODE_RECORD_SELECT])+"Repetitions\0".encode('ascii')+bytes([
         apx.OPCODE_UNPACK_U8,
         apx.OPCODE_RECORD_LEAVE,
      ])
      self.assertEqual(prog, expected)


class TestCompilerFromApxNode(unittest.TestCase):

   def test_compile_require_ports(self):
      compiler = apx.Compiler()
      node = apx.Node('TestNode')
      node.append(apx.DataType('TestType1_T', 'S(0,1000)'))
      node.append(apx.DataType('TestType2_T', 'a[32]'))
      port = node.append(apx.RequirePort('Signal1','C','=255'))
      prog = compiler.exec(port)
      expected = bytes([
         apx.OPCODE_UNPACK_PROG, 1, 0, 0, 0,
         apx.OPCODE_UNPACK_U8,
      ])
      self.assertEqual(prog, expected)
      port = node.append(apx.RequirePort('Signal2','T[0]','=255'))
      prog = compiler.exec(port)
      expected = bytes([
         apx.OPCODE_UNPACK_PROG, 2, 0, 0, 0,
         apx.OPCODE_UNPACK_U16,
      ])
      self.assertEqual(prog, expected)
      port = node.append(apx.RequirePort('Signal3', 'T["TestType2_T"]', '=""'))
      prog = compiler.exec(port)
      expected = bytes([
         apx.OPCODE_UNPACK_PROG, 32, 0, 0, 0,
         apx.OPCODE_UNPACK_STR, 32, 0
      ])
      self.assertEqual(prog, expected)

   def test_compile_provide_ports(self):
      compiler = apx.Compiler()
      node = apx.Node('TestNode')
      node.append(apx.DataType('TestType1_T', 'C'))
      node.append(apx.DataType('TestType2_T', 'C[10]'))
      node.append(apx.DataType('TestType3_T', 'S'))
      node.append(apx.DataType('TestType4_T', 'S[10]'))
      node.append(apx.DataType('TestType5_T', 'L'))
      node.append(apx.DataType('TestType6_T', 'L[10]'))
      node.append(apx.ProvidePort('U8Signal', 'T["TestType1_T"]'))
      node.append(apx.ProvidePort('U8ArraySignal', 'T["TestType2_T"]'))
      node.append(apx.ProvidePort('U16Signal', 'T["TestType3_T"]'))
      node.append(apx.ProvidePort('U16ArraySignal', 'T["TestType4_T"]'))
      node.append(apx.ProvidePort('U32Signal', 'T["TestType5_T"]'))
      node.append(apx.ProvidePort('U32ArraySignal', 'T["TestType6_T"]'))
      prog = compiler.exec(node.find('U8Signal'))
      expected = bytes([
         apx.OPCODE_PACK_PROG, apx.UINT8_LEN, 0, 0, 0,
         apx.OPCODE_PACK_U8
      ])
      self.assertEqual(prog, expected)

      prog = compiler.exec(node.find('U8ArraySignal'))
      expected = bytes([
         apx.OPCODE_PACK_PROG, apx.UINT8_LEN*10, 0, 0, 0,
         apx.OPCODE_PACK_U8AR, 10, 0
      ])
      self.assertEqual(prog, expected)

      prog = compiler.exec(node.find('U16Signal'))
      expected = bytes([
         apx.OPCODE_PACK_PROG, apx.UINT16_LEN, 0, 0, 0,
         apx.OPCODE_PACK_U16
      ])
      self.assertEqual(prog, expected)

      prog = compiler.exec(node.find('U16ArraySignal'))
      expected = bytes([
         apx.OPCODE_PACK_PROG, apx.UINT16_LEN*10, 0, 0, 0,
         apx.OPCODE_PACK_U16AR, 10, 0
      ])
      self.assertEqual(prog, expected)

      prog = compiler.exec(node.find('U32Signal'))
      expected = bytes([
         apx.OPCODE_PACK_PROG, apx.UINT32_LEN, 0, 0, 0,
         apx.OPCODE_PACK_U32
      ])
      self.assertEqual(prog, expected)

      prog = compiler.exec(node.find('U32ArraySignal'))
      expected = bytes([
         apx.OPCODE_PACK_PROG, apx.UINT32_LEN*10, 0, 0, 0,
         apx.OPCODE_PACK_U32AR, 10, 0
      ])
      self.assertEqual(prog, expected)

   def test_compile_record_provide_port(self):
      compiler = apx.Compiler()
      node = apx.Node('TestNode')
      node.append(apx.DataType('SoundId_T', 'S'))
      node.append(apx.DataType('Volume_T', 'C'))
      node.append(apx.DataType('Repetitions_T', 'C'))
      node.append(apx.DataType('SoundRequest_T', '{"SoundId"T["SoundId_T"]"Volume"T["Volume_T"]"Repetitions"T["Repetitions_T"]}'))
      node.append(apx.ProvidePort('SoundRequest', 'T["SoundRequest_T"]', '={65535,255,255}'))
      prog = compiler.exec(node.find('SoundRequest'))
      expected = bytes([
         apx.OPCODE_PACK_PROG, (apx.UINT16_LEN+apx.UINT8_LEN+apx.UINT8_LEN), 0, 0, 0,
         apx.OPCODE_RECORD_ENTER,
         apx.OPCODE_RECORD_SELECT])+"SoundId\0".encode('ascii')+bytes([
         apx.OPCODE_PACK_U16,
         apx.OPCODE_RECORD_SELECT])+"Volume\0".encode('ascii')+bytes([
         apx.OPCODE_PACK_U8,
         apx.OPCODE_RECORD_SELECT])+"Repetitions\0".encode('ascii')+bytes([
         apx.OPCODE_PACK_U8,
         apx.OPCODE_RECORD_LEAVE,
      ])
      self.assertEqual(prog, expected)

   def test_compile_record_require_port(self):
      compiler = apx.Compiler()
      node = apx.Node('TestNode')
      node.append(apx.DataType('SoundId_T', 'S'))
      node.append(apx.DataType('Volume_T', 'C'))
      node.append(apx.DataType('Repetitions_T', 'C'))
      node.append(apx.DataType('SoundRequest_T', '{"SoundId"T["SoundId_T"]"Volume"T["Volume_T"]"Repetitions"T["Repetitions_T"]}'))
      node.append(apx.RequirePort('SoundRequest', 'T["SoundRequest_T"]', '={65535,255,255}'))
      prog = compiler.exec(node.find('SoundRequest'))
      expected = bytes([
         apx.OPCODE_UNPACK_PROG, (apx.UINT16_LEN+apx.UINT8_LEN+apx.UINT8_LEN), 0, 0, 0,
         apx.OPCODE_RECORD_ENTER,
         apx.OPCODE_RECORD_SELECT])+"SoundId\0".encode('ascii')+bytes([
         apx.OPCODE_UNPACK_U16,
         apx.OPCODE_RECORD_SELECT])+"Volume\0".encode('ascii')+bytes([
         apx.OPCODE_UNPACK_U8,
         apx.OPCODE_RECORD_SELECT])+"Repetitions\0".encode('ascii')+bytes([
         apx.OPCODE_UNPACK_U8,
         apx.OPCODE_RECORD_LEAVE,
      ])
      self.assertEqual(prog, expected)

if __name__ == '__main__':
    unittest.main()
