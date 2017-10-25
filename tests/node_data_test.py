import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest
import remotefile
import time

class TestFileManager(unittest.TestCase):
 
   def setUp(self):
      pass
   
   def test_portMap(self):
      node = apx.Node('TestNode')
      node.dataTypes.append(apx.DataType('InactiveActive_T','C(0,3)'))      
      node.providePorts.append(apx.ProvidePort('VehicleSpeed','S','=65535'))
      node.providePorts.append(apx.ProvidePort('MainBeam','T[0]','=3'))
      node.providePorts.append(apx.ProvidePort('FuelLevel','C'))
      node.providePorts.append(apx.ProvidePort('ParkBrakeActive','T[0]','=3'))
      node.requirePorts.append(apx.RequirePort('RheostatLevelRqst','C','=255'))
      node.requirePorts.append(apx.RequirePort('StrSignal','a[4]','=""'))
      node.requirePorts.append(apx.RequirePort('RecordSignal','{"Name"a[8]"Id"L"Data"S[3]}','={"",0xFFFFFFFF,{0,0,0}}'))
      nodeData = apx.NodeData(node)
      


if __name__ == '__main__':
    unittest.main()   

