import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest

class TestApxTester(unittest.TestCase):
    
    def test_ramp(self):
        apx_text = """APX/1.2
N"Tester"
T"VehicleSpeed_T"S
T"EngineSpeed_T"S
P"VehicleSpeed"T["VehicleSpeed_T"]:=65535
P"EngineSpeed"T["EngineSpeed_T"]:=65535
"""
        tester = apx.Tester(apx_text)
        node = tester.client.node
        self.assertIsInstance(node, apx.Node)
        tester.set('VehicleSpeed', 0)
        tester.ramp('VehicleSpeed', 65535, 100, 20)
        self.assertEqual(tester.get('VehicleSpeed'), 65535)

if __name__ == '__main__':
    unittest.main()
