import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest
import remotefile
import time

class TestNodeData(unittest.TestCase):

   def test_portMap(self):
      node = apx.Node('TestNode')
      node.add_type(apx.DataType('InactiveActive_T','C(0,3)'))
      node.append(apx.ProvidePort('VehicleSpeed','S','=65535'))
      node.append(apx.ProvidePort('MainBeam','T[0]','=3'))
      node.append(apx.ProvidePort('FuelLevel','C'))
      node.append(apx.ProvidePort('ParkBrakeActive','T[0]','=3'))
      node.append(apx.RequirePort('RheostatLevelRqst','C','=255'))
      node.append(apx.RequirePort('StrSignal','a[4]','=""'))
      node.append(apx.RequirePort('RecordSignal','{"Name"a[8]"Id"L"Data"S[3]}','={"",0xFFFFFFFF,{0,0,0}}'))
      self.assertEqual(node.find('VehicleSpeed').id, 0)
      self.assertEqual(node.find('RheostatLevelRqst').id, 0)

      node_data = apx.NodeData(node)
      self.assertEqual(len(node_data.inPortDataMap), 23)
      self.assertEqual(node_data.inPortDataMap[0].name, 'RheostatLevelRqst')
      self.assertEqual(node_data.inPortDataMap[0].id, 0)
      for i in range(1, 5):
         self.assertEqual(node_data.inPortDataMap[i].name, 'StrSignal')
         self.assertEqual(node_data.inPortDataMap[i].id, 1)
      for i in range(5, 23):
         self.assertEqual(node_data.inPortDataMap[i].name, 'RecordSignal')
         self.assertEqual(node_data.inPortDataMap[i].id, 2)

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
      expected = bytes([apx.OPCODE_UNPACK_PROG, 4,0,0,0,
                        apx.OPCODE_UNPACK_STR, 4,0])
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

if __name__ == '__main__':
    unittest.main()