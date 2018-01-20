import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest

class TestApxClient(unittest.TestCase):
    
    def test_create_provide_ports(self):
        apx_text = """APX/1.2
N"TestNode"
T"VehicleSpeed_T"S
T"EngineSpeed_T"S
P"VehicleSpeed"T[0]
P"EngineSpeed"T[1]
"""
        client = apx.Client()
        client.create_node(apx_text)
        client.write(0, 0x1234)
        self.assertEqual(client.nodeData.outPortDataFile.read(0,2), bytes([0x34, 0x12]))
        self.assertEqual(client.nodeData.outPortDataFile.read(2,2), bytes([0, 0]))
        client.write('EngineSpeed', 0xFFFF)
        self.assertEqual(client.nodeData.outPortDataFile.read(0,2), bytes([0x34, 0x12]))
        self.assertEqual(client.nodeData.outPortDataFile.read(2,2), bytes([0xFF, 0xFF]))

    def test_create_require_ports(self):
        apx_text = """APX/1.2
N"TestNode"
T"VehicleSpeed_T"S
T"EngineSpeed_T"S
T"InactiveActive_T"C(0,3):VT("InactiveActive_Inactive","InactiveActive_Active","InactiveActive_Error","InactiveActive_NotAvailable")
R"VehicleSpeed"T[0]:=0xFFFF
R"EngineSpeed"T[1]:=0xFFFF
R"ParkBrakeState"T["InactiveActive_T"]:=3
"""
        client = apx.Client()
        client.create_node(apx_text)
        ParkBrakeState_port = client.find('ParkBrakeState')
        self.assertEqual(client.read(0), 0xFFFF)
        self.assertEqual(client.read(ParkBrakeState_port), 3)
        client.nodeData.inPortDataFile.write(0, bytes([0x34,0x12]))
        self.assertEqual(client.read(0), 0x1234)

if __name__ == '__main__':
    unittest.main()
