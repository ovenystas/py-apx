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
      node_data = apx.NodeData(node)
      self.assertEqual(len(node_data.inPortDataMap), 23)
      self.assertEqual(node_data.inPortDataMap[0].name, 'RheostatLevelRqst')
      self.assertEqual(node_data.inPortDataMap[0].portId, 0)
      for i in range(1, 5):
         self.assertEqual(node_data.inPortDataMap[i].name, 'StrSignal')
         self.assertEqual(node_data.inPortDataMap[i].portId, 1)
      for i in range(5, 23):
         self.assertEqual(node_data.inPortDataMap[i].name, 'RecordSignal')
         self.assertEqual(node_data.inPortDataMap[i].portId, 2)

if __name__ == '__main__':
    unittest.main()   

