import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest
import struct

def create_node_and_data():
   node = apx.Node('TestNode')
   node.add_type(apx.DataType('InactiveActive_T','C(0,3)'))
   node.append(apx.ProvidePort('VehicleSpeed','S','=65535'))
   node.append(apx.ProvidePort('MainBeam','T[0]','=3'))
   node.append(apx.ProvidePort('FuelLevel','C'))
   node.append(apx.ProvidePort('ParkBrakeActive','T[0]','=3'))
   node.append(apx.ProvidePort('ComplexRecordSignal','{"SensorData"{"x"S"y"S"z"S}"TimeStamp"L}'))
   node.append(apx.RequirePort('RheostatLevelRqst','C','=255'))
   node.append(apx.RequirePort('StrSignal','a[8]','=""'))
   node.append(apx.RequirePort('RecordSignal','{"Name"a[8]"Id"L"Data"S[3]}','={"",0xFFFFFFFF,{0,0,0}}'))
   return node

class TestNodeDataCompile(unittest.TestCase):

   def test_port_map_and_compiled_programs(self):
      node = create_node_and_data()

      self.assertEqual(node.find('VehicleSpeed').id, 0)
      self.assertEqual(node.find('RheostatLevelRqst').id, 0)

      node_data = apx.NodeData(node)
      self.assertEqual(len(node_data.inPortByteMap), 27)
      self.assertEqual(node_data.inPortByteMap[0].name, 'RheostatLevelRqst')
      self.assertEqual(node_data.inPortByteMap[0].id, 0)
      for i in range(1, 9):
         self.assertEqual(node_data.inPortByteMap[i].name, 'StrSignal')
         self.assertEqual(node_data.inPortByteMap[i].id, 1)
      for i in range(9, 27):
         self.assertEqual(node_data.inPortByteMap[i].name, 'RecordSignal')
         self.assertEqual(node_data.inPortByteMap[i].id, 2)
      
      self.assertEqual(len(node_data.outPortDataMap), 5)
      elem = node_data.outPortDataMap[0]
      self.assertEqual(elem.data_offset, 0)
      self.assertEqual(elem.data_len, 2)
      self.assertIs(elem.port, node.find('VehicleSpeed'))
      elem = node_data.outPortDataMap[1]
      self.assertEqual(elem.data_offset, 2)
      self.assertEqual(elem.data_len, 1)
      self.assertIs(elem.port, node.find('MainBeam'))
      elem = node_data.outPortDataMap[2]
      self.assertEqual(elem.data_offset, 3)
      self.assertEqual(elem.data_len, 1)
      self.assertIs(elem.port, node.find('FuelLevel'))
      elem = node_data.outPortDataMap[3]
      self.assertEqual(elem.data_offset, 4)
      self.assertEqual(elem.data_len, 1)
      self.assertIs(elem.port, node.find('ParkBrakeActive'))
      elem = node_data.outPortDataMap[4]
      self.assertEqual(elem.data_offset, 5)
      self.assertEqual(elem.data_len, 10)
      self.assertIs(elem.port, node.find('ComplexRecordSignal'))

      expected = bytes([apx.OPCODE_PACK_PROG, apx.UINT16_LEN,0,0,0,
                        apx.OPCODE_PACK_U16])
      self.assertEqual(node_data.outPortPrograms[0], expected)
      expected = bytes([apx.OPCODE_PACK_PROG, apx.UINT8_LEN,0,0,0,
                        apx.OPCODE_PACK_U8])
      self.assertEqual(node_data.outPortPrograms[1], expected)
      self.assertEqual(node_data.outPortPrograms[2], expected)
      self.assertEqual(node_data.outPortPrograms[3], expected)
      expected = bytes([apx.OPCODE_PACK_PROG, (3*apx.UINT16_LEN+apx.UINT32_LEN),0,0,0,
                        apx.OPCODE_RECORD_ENTER,
                        apx.OPCODE_RECORD_SELECT])+"SensorData\0".encode('ascii')+bytes([
                        apx.OPCODE_RECORD_ENTER,
                        apx.OPCODE_RECORD_SELECT])+"x\0".encode('ascii')+bytes([
                        apx.OPCODE_PACK_U16,
                        apx.OPCODE_RECORD_SELECT])+"y\0".encode('ascii')+bytes([
                        apx.OPCODE_PACK_U16,
                        apx.OPCODE_RECORD_SELECT])+"z\0".encode('ascii')+bytes([
                        apx.OPCODE_PACK_U16,
                        apx.OPCODE_RECORD_LEAVE,
                        apx.OPCODE_RECORD_SELECT])+"TimeStamp\0".encode('ascii')+bytes([
                        apx.OPCODE_PACK_U32,
                        apx.OPCODE_RECORD_LEAVE                        
                        ])
      self.assertEqual(node_data.outPortPrograms[4], expected)      
      
      expected = bytes([apx.OPCODE_UNPACK_PROG, apx.UINT8_LEN,0,0,0,
                        apx.OPCODE_UNPACK_U8])
      self.assertEqual(node_data.inPortPrograms[0], expected)
      expected = bytes([apx.OPCODE_UNPACK_PROG, 8,0,0,0,
                        apx.OPCODE_UNPACK_STR, 8,0])
      self.assertEqual(node_data.inPortPrograms[1], expected)
      expected = bytes([apx.OPCODE_UNPACK_PROG, (8+apx.UINT32_LEN+apx.UINT16_LEN*3),0,0,0,
                        apx.OPCODE_RECORD_ENTER,
                        apx.OPCODE_RECORD_SELECT])+"Name\0".encode('ascii')+bytes([
                        apx.OPCODE_UNPACK_STR, 8,0,
                        apx.OPCODE_RECORD_SELECT])+"Id\0".encode('ascii')+bytes([
                        apx.OPCODE_UNPACK_U32,
                        apx.OPCODE_RECORD_SELECT])+"Data\0".encode('ascii')+bytes([
                        apx.OPCODE_UNPACK_U16AR, 3,0,
                        apx.OPCODE_RECORD_LEAVE
                        ])
      self.assertEqual(node_data.inPortPrograms[2], expected)



class TestNodeDataRead(unittest.TestCase):
   
   def test_read_port_RheostatLevelRqst(self):
      node = create_node_and_data()
      port_RheostatLevelRqst = node.find('RheostatLevelRqst')
      node_data = apx.NodeData(node)
      input_file = node_data.inPortDataFile
      #verify init value
      self.assertEqual(node_data.read_require_port(port_RheostatLevelRqst), 255)
      #write to input file
      input_file.write(0, bytes([0]))
      self.assertEqual(node_data.read_require_port(port_RheostatLevelRqst), 0)
      input_file.write(0, bytes([10]))
      self.assertEqual(node_data.read_require_port(port_RheostatLevelRqst), 10)
      input_file.write(0, bytes([255]))
      self.assertEqual(node_data.read_require_port(port_RheostatLevelRqst), 255)

   def test_read_port_StrSignal(self):
      node = create_node_and_data()
      port_StrSignal = node.find('StrSignal')
      node_data = apx.NodeData(node)
      input_file = node_data.inPortDataFile
      #verify init value
      self.assertEqual(node_data.read_require_port(port_StrSignal), "")
      #write to input file
      input_file.write(1, 'Hello\0\0\0'.encode('utf-8'))
      self.assertEqual(node_data.read_require_port(port_StrSignal), "Hello")

      input_file.write(1, 'Selected'.encode('utf-8'))
      self.assertEqual(node_data.read_require_port(port_StrSignal), "Selected")

      input_file.write(1, 'a\0\0\0\0\0\0'.encode('utf-8'))
      self.assertEqual(node_data.read_require_port(port_StrSignal), "a")
      input_file.write(1, bytes(8))
      self.assertEqual(node_data.read_require_port(port_StrSignal), "")

   def test_read_RecordSignal(self):
      node = create_node_and_data()
      port_RecordSignal = node.find('RecordSignal')
      node_data = apx.NodeData(node)
      input_file = node_data.inPortDataFile
      #verify init value
      self.assertEqual(node_data.read_require_port(port_RecordSignal), {'Name': "", 'Id':0xFFFFFFFF, 'Data': [0,0,0]})
      name_offset = 9
      id_offset = 17
      data_offset = 21
      input_file.write(name_offset, "abcdefgh".encode('utf-8'))
      self.assertEqual(node_data.read_require_port(port_RecordSignal), {'Name': "abcdefgh", 'Id':0xFFFFFFFF, 'Data': [0,0,0]})
      input_file.write(id_offset, struct.pack("<L",0x12345678))
      self.assertEqual(node_data.read_require_port(port_RecordSignal), {'Name': "abcdefgh", 'Id':0x12345678, 'Data': [0,0,0]})
      input_file.write(data_offset, struct.pack("<HHH",0,0,1))
      self.assertEqual(node_data.read_require_port(port_RecordSignal), {'Name': "abcdefgh", 'Id':0x12345678, 'Data': [0,0,1]})
      input_file.write(data_offset, struct.pack("<HHH",18000,2,10))
      self.assertEqual(node_data.read_require_port(port_RecordSignal), {'Name': "abcdefgh", 'Id':0x12345678, 'Data': [18000,2,10]})
      
   def test_byte_to_port_all(self):
      node = create_node_and_data()
      node_data = apx.NodeData(node)
      input_file = node_data.inPortDataFile
      RheostatLevelRqst_data_offset = 0
      RheostatLevelRqst_data_len = 1
      StrSignal_data_offset = 1
      StrSignal_data_len = 8
      RecordSignal_data_offset = 9
      RecordSignal_data_len = 18
      total_len = RheostatLevelRqst_data_len+StrSignal_data_len+RecordSignal_data_len
      self.assertEqual(len(input_file.data), total_len)
      self.assertEqual(len(node_data.inPortByteMap), total_len)
      result = list(node_data.byte_to_port(0,total_len))

      self.assertEqual(len(result), 3)
      self.assertIs(result[0][0], node.find('RheostatLevelRqst'))
      self.assertIs(result[1][0], node.find('StrSignal'))
      self.assertIs(result[2][0], node.find('RecordSignal'))
      self.assertEqual(result[0][1], RheostatLevelRqst_data_offset)
      self.assertEqual(result[1][1], StrSignal_data_offset)
      self.assertEqual(result[2][1], RecordSignal_data_offset)
      self.assertEqual(result[0][2], RheostatLevelRqst_data_len)
      self.assertEqual(result[1][2], StrSignal_data_len)
      self.assertEqual(result[2][2], RecordSignal_data_len)
      
   def test_byte_to_port_RheostatLevelRqst(self):
      node = create_node_and_data()
      node_data = apx.NodeData(node)
      
      RheostatLevelRqst_data_offset = 0
      RheostatLevelRqst_data_len = 1
      result = list(node_data.byte_to_port(RheostatLevelRqst_data_offset, RheostatLevelRqst_data_len))
      self.assertEqual(len(result), 1)
      port, offset, length = result[0]
      self.assertIs(port, node.find('RheostatLevelRqst'))
      self.assertEqual(offset, RheostatLevelRqst_data_offset)
      self.assertEqual(length, RheostatLevelRqst_data_len)

   def test_byte_to_port_StrSignal(self):
      node = create_node_and_data()
      node_data = apx.NodeData(node)
      
      StrSignal_data_offset = 1
      StrSignal_data_len = 8
      for offset in range(StrSignal_data_offset, StrSignal_data_offset+StrSignal_data_len):
         result = list(node_data.byte_to_port(offset, 1))
         self.assertEqual(len(result), 1)
         port, offset, length = result[0]
         self.assertIs(port, node.find('StrSignal'))
         self.assertEqual(offset, StrSignal_data_offset)
         self.assertEqual(length, StrSignal_data_len)

   def test_byte_to_port_RecordSignal(self):
      node = create_node_and_data()
      node_data = apx.NodeData(node)
      
      RecordSignal_data_offset = 9
      RecordSignal_data_len = 18
      for offset in range(RecordSignal_data_offset, RecordSignal_data_offset+RecordSignal_data_len):
         result = list(node_data.byte_to_port(offset, 1))
         self.assertEqual(len(result), 1)
         port, offset, length = result[0]
         self.assertIs(port, node.find('RecordSignal'))
         self.assertEqual(offset, RecordSignal_data_offset)
         self.assertEqual(length, RecordSignal_data_len)
      
   def test_byte_to_port_invalid_args(self):
      node = create_node_and_data()
      node_data = apx.NodeData(node)
      self.assertEqual(len(node_data.inPortByteMap), 27)
      
      with self.assertRaises(ValueError) as context:
         result = list(node_data.byte_to_port(28,1))
      self.assertEqual(str(context.exception), "start_offset (28) is beyond length of file (27)")
      
      with self.assertRaises(ValueError) as context:
         result = list(node_data.byte_to_port(25,5))
      self.assertEqual(str(context.exception), "end_offset (30) is beyond length of file (27)")
            
      RecordSignal_data_offset = 9
      RecordSignal_data_len = 18
      result = list(node_data.byte_to_port(25,2))
      port, offset, length = result[0]
      self.assertIs(port, node.find('RecordSignal'))
      self.assertEqual(offset, RecordSignal_data_offset)
      self.assertEqual(length, RecordSignal_data_len)

   def test_callback(self):
      
      call_history = []
      
      @apx.NodeDataClient.register
      class Listener:
         def on_require_port_data(self, port, value):
            call_history.append((port, value))
      
      listener_obj = Listener()
      node = create_node_and_data()
      node_data = apx.NodeData(node)
      node_data.nodeDataClient = listener_obj
      input_file = node_data.inPortDataFile
      RheostatLevelRqst_data_offset = 0
      RheostatLevelRqst_data_len = 1
      StrSignal_data_offset = 1
      StrSignal_data_len = 8
      RecordSignal_data_offset = 9
      RecordSignal_data_len = 18
      #test write RheostatLevelRqst
      self.assertEqual(len(call_history), 0)
      input_file.write(0, bytes([0]))
      self.assertEqual(len(call_history), 1)
      self.assertEqual(call_history[-1][0], node.find('RheostatLevelRqst'))
      self.assertEqual(call_history[-1][1], 0)

      input_file.write(0, bytes([255]))
      self.assertEqual(len(call_history), 2)
      self.assertEqual(call_history[-1][0], node.find('RheostatLevelRqst'))
      self.assertEqual(call_history[-1][1], 255)
      
      #test write RecordSignal
      input_file.write(RecordSignal_data_offset, "Test".encode('utf-8'))
      self.assertEqual(len(call_history), 3)
      self.assertEqual(call_history[-1][0], node.find('RecordSignal'))
      self.assertEqual(call_history[-1][1], {'Name': "Test", 'Id': 0xFFFFFFFF, 'Data':[0,0,0]})
      input_file.write(RecordSignal_data_offset, "Abc\0\0\0\0\0".encode('utf-8')+struct.pack('<L',918)+struct.pack('<HHH', 1000, 2000, 4000))
      self.assertEqual(len(call_history), 4)
      self.assertEqual(call_history[-1][0], node.find('RecordSignal'))
      self.assertEqual(call_history[-1][1], {'Name': "Abc", 'Id': 918, 'Data':[1000,2000,4000]})

class TestNodeDataWrite(unittest.TestCase):
   
   def test_write_VehicleSpeed(self):
      node = create_node_and_data()
      node_data = apx.NodeData(node)
      VehicleSpeed_port = node.find('VehicleSpeed')
      VehicleSpeed_offset = 0
      VehicleSpeed_length = 2
      output_file = node_data.outPortDataFile
      #verify init value
      self.assertEqual(output_file.read(VehicleSpeed_offset, VehicleSpeed_length), bytes([0xFF, 0xFF]))
      node_data.write_provide_port(VehicleSpeed_port, 0x1234)      
      self.assertEqual(output_file.read(VehicleSpeed_offset, VehicleSpeed_length), bytes([0x34, 0x12]))
      

      
if __name__ == '__main__':
    unittest.main()