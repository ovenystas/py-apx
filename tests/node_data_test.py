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
      self.assertEqual(node.providePorts[0].dsg.structFmtStr, '<H') #unsigned short
      self.assertEqual(node.providePorts[1].dsg.structFmtStr, '<B') #unsigned char
      self.assertEqual(node.providePorts[2].dsg.structFmtStr, '<B') #unsigned char
      self.assertEqual(node.providePorts[3].dsg.structFmtStr, '<B') #unsigned char
      self.assertEqual(node.requirePorts[0].dsg.structFmtStr, '<B') #unsigned char
      self.assertEqual(node.requirePorts[1].dsg.structFmtStr, '<4s') #char[4]
      self.assertEqual(node.requirePorts[2].dsg.structFmtStr, '<8sI3H') #char[8],unsigned int, unsigned short[3]
      nodeData.writeProvidePort(0,1)
      


if __name__ == '__main__':
    unittest.main()   

