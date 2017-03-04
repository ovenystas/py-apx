import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest
import autosar

class TestParser(unittest.TestCase):
 
   def setUp(self):
      pass
 
   def test_parse_node(self):
      text="""APX/1.2
N"TestSWC"
T"Percent_T"C
T"CoolantTemp_T"C
T"InactiveActive_T"C(0,3):VT("InactiveActive_Inactive","InactiveActive_Active","InactiveActive_Error","InactiveActive_NotAvailable")
T"OnOff_T"C(0,3):VT("OnOff_Off","OnOff_On","OnOff_Error","OnOff_NotAvailable"
T"EngineSpeed_T"S
T"VehicleSpeed_T"S
R"FuelLevel"T[0]:=255
R"CoolantTemp"T[1]:=255
R"ParkBrakeState"T[2]:=3
R"MainBeamState"T[3]:=3
P"EngineSpeed"T[4]:=0xFFFF
P"VehicleSpeed"T[5]:=0xFFFF
"""

      apx_parser = apx.Parser()
      node = apx_parser.loads(text)
      self.assertIsInstance(node, apx.Node)
      self.assertEqual(node.name, "TestSWC")
      self.assertEqual(len(node.dataTypes), 6)
      self.assertEqual(len(node.requirePorts), 4)
      self.assertEqual(len(node.providePorts), 2)
      

      
      

if __name__ == '__main__':
    unittest.main()