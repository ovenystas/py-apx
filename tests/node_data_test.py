import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest
import remotefile
import time

def create_node_and_data():
   node = apx.Node('TestNode')
   node.add_type(apx.DataType('InactiveActive_T','C(0,3)'))
   node.append(apx.ProvidePort('VehicleSpeed','S','=65535'))
   node.append(apx.ProvidePort('MainBeam','T[0]','=3'))
   node.append(apx.ProvidePort('FuelLevel','C'))
   node.append(apx.ProvidePort('ParkBrakeActive','T[0]','=3'))
   port_RheostatLevelRqst = node.append(apx.RequirePort('RheostatLevelRqst','C','=255'))
   node.append(apx.RequirePort('StrSignal','a[8]','=""'))
   node.append(apx.RequirePort('RecordSignal','{"Name"a[8]"Id"L"Data"S[3]}','={"",0xFFFFFFFF,{0,0,0}}'))
   return node

class TestNodeData(unittest.TestCase):

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
      
      self.assertEqual(len(node_data.outPortDataMap), 4)
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

      expected = bytes([apx.OPCODE_PACK_PROG, apx.UINT16_LEN,0,0,0,
                        apx.OPCODE_PACK_U16])
      self.assertEqual(node_data.outPortPrograms[0], expected)
      expected = bytes([apx.OPCODE_PACK_PROG, apx.UINT8_LEN,0,0,0,
                        apx.OPCODE_PACK_U8])
      self.assertEqual(node_data.outPortPrograms[1], expected)
      self.assertEqual(node_data.outPortPrograms[2], expected)
      self.assertEqual(node_data.outPortPrograms[3], expected)
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

   def test_read_port_RheostatLevelRqst(self):
      node = create_node_and_data()
      port_RheostatLevelRqst = node.find('RheostatLevelRqst')
      node_data = apx.NodeData(node)
      input_file = node_data.inPortDataFile
      #verify init value
      self.assertEqual(node_data.readRequirePort(port_RheostatLevelRqst), 255)
      #write to input file
      input_file.write(0, bytes([0]))
      self.assertEqual(node_data.readRequirePort(port_RheostatLevelRqst), 0)
      input_file.write(0, bytes([10]))
      self.assertEqual(node_data.readRequirePort(port_RheostatLevelRqst), 10)
      input_file.write(0, bytes([255]))
      self.assertEqual(node_data.readRequirePort(port_RheostatLevelRqst), 255)

   def test_read_port_StrSignal(self):
      node = create_node_and_data()
      port_StrSignal = node.find('StrSignal')
      node_data = apx.NodeData(node)
      input_file = node_data.inPortDataFile
      #verify init value
      self.assertEqual(node_data.readRequirePort(port_StrSignal), "")
      #write to input file
      input_file.write(1, 'Hello\0\0\0'.encode('utf-8'))
      self.assertEqual(node_data.readRequirePort(port_StrSignal), "Hello")

      input_file.write(1, 'Restrict'.encode('utf-8'))
      self.assertEqual(node_data.readRequirePort(port_StrSignal), "Restrict")

      input_file.write(1, 'a\0\0\0\0\0\0'.encode('utf-8'))
      self.assertEqual(node_data.readRequirePort(port_StrSignal), "a")
      input_file.write(1, bytes(8))
      self.assertEqual(node_data.readRequirePort(port_StrSignal), "")
            
if __name__ == '__main__':
    unittest.main()